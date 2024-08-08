from typing import List, Optional, Tuple
from candidates.schemas import CandidatesList, Candidate
from jobs.schemas import Job
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne

from api.main import app

import os
import requests
import asyncio

class CandidateSerice:
    def __init__(self) -> None:
        self.api_key = os.getenv('WORKABLE_API_KEY')
        self.api_url = os.getenv('WORKABLE_URL')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    async def get_database(self) -> AsyncIOMotorDatabase:
        return app.state.db
    
    async def get_candidates(self) -> Tuple[Optional[CandidatesList], int, Optional[str]]:
        try:
            db = await self.get_database()
            candidates = await db.candidates.find().to_list(None)
            return CandidatesList(candidates=candidates), 200, None    
        except Exception as e:
            error_msg = f"Error fetching candidates: {str(e)}"
            print(error_msg)
            return None, 500, error_msg
        
    async def fetch_jobs(self) -> Tuple[List[Job]]:
        try: 
            db = await self.get_database()
            jobs = await db.jobs.find().to_list(None)
            return jobs
        except Exception as e:
            error_msg = f"Error fetching jobs: {str(e)}"
            print(error_msg)
            raise e
    
    async def fetch_candidates(self, url: str) -> Tuple[List[dict], Optional[str]]:
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            candidates = data.get('candidates', [])
            return candidates, data.get('paging', {}).get('next')
        except Exception as e:
            error_msg = f"Error fetching candidates: {str(e)}"
            print(error_msg)
            raise e
    
    async def fetch_all_candidates_for_job(self, shortcode) -> Tuple[List[Candidate]]:
        try:
            all_candidates = []
            url = f"{self.api_url}/candidates?shortcode={shortcode}"
            while url:
                await asyncio.sleep(1)
                candidates, next_url = await self.fetch_candidates(url)
                all_candidates.extend(candidates)
                url = next_url
            return all_candidates
        except Exception as e:
            error_msg = f"Error fetching candidates: {str(e)}"
            print(error_msg)
            raise e
        
    async def store_candidates(self, candidates: List[Candidate]) -> Tuple[int, int, int]:
        try:
            db = await self.get_database()
            
            if candidates:
                # Prepare bulk operations for upsert
                operations = [
                    UpdateOne(
                        {"id": candidate["id"]},
                        {"$setOnInsert": candidate},
                        upsert=True
                    ) for candidate in candidates
                ]
                
                # Perform bulk write
                result = await db.candidates.bulk_write(operations)
                
                print(f"Matched: {result.matched_count}, "
                    f"Modified: {result.modified_count}, "
                    f"Upserted: {result.upserted_count}")
                
                return result.matched_count, result.modified_count, result.upserted_count
            else:
                return 0, 0, 0
        except Exception as e:
            error_msg = f"Error storing candidates: {str(e)}"
            print(error_msg)
            raise e
                    
    async def sync_candidates(self) -> Tuple[Optional[str], int]:
        try:
            jobs = await self.fetch_jobs()
            print(f"Found {len(jobs)} jobs")
            if len(jobs) > 0:
                for job in jobs:
                    shortcode = job.get('shortcode')
                    print(f"Syncing candidates for job {shortcode}")
                    candidates = await self.fetch_all_candidates_for_job(shortcode)
                    print(f"Found {len(candidates)} candidates for job {shortcode}")
                    matched, modified, upserted = await self.store_candidates(candidates)
                    print(f"Matched: {matched}, Modified: {modified}, Upserted: {upserted}")
                return "Candidates synced successfully", 200
            else: 
                return "No jobs found", 200

        except Exception as e:
            error_msg = f"Error fetching jobs: {str(e)}"
            print(error_msg)
            return error_msg, 500
        
    async def fetch_candidate_details(self, id: str) -> list[Candidate]:
        try:
            response = self.session.get(f"{self.api_url}/candidates/{id}")
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            error_msg = f"Error fetching candidates: {str(e)}"
            print(error_msg)
            return None

    async def sync_candidate_details(self) -> Tuple[Optional[str], int]:
        try:
            db = await self.get_database()
            # candidates = await db.candidates.find({"$and": [{"resume_url": {"$exists": False}}, {"experience_entries": {"$exists": False}}, { "missingData": { "$exists": False }}]}).to_list(None)
            candidates = await db.candidates.find({"job.shortcode": 'C2A884697D'}).to_list(None)
            print(f"Found {len(candidates)} candidates without details")
            for candidate in candidates:
                await asyncio.sleep(1)
                candidate_id = candidate.get('id')
                data = await self.fetch_candidate_details(candidate_id)
                if not data:
                    print(f"Data not found for candidate {candidate_id}")
                    db.candidates.update_one({"id": candidate_id}, {"$set": {"missingData": True}})
                    continue
                candidate_data = data.get('candidate')
                print(f"adding details for candidate {candidate_id}, {candidate_data.get('resume_url')}")
                update = {
                    "$set": {
                        "resume_url": candidate_data.get('resume_url'),
                        "summary": candidate_data.get('summary'),
                        "education_entries": candidate_data.get('education_entries'),
                        "experience_entries": candidate_data.get('experience_entries'),
                        "skills": candidate_data.get('skills'),
                        "location": candidate_data.get('location')
                    }
                }
                await db.candidates.update_one({"id": candidate_id}, update)
            return None, 200
        except Exception as e:
            error_msg = f"Error syncing candidate details: {str(e)}"
            print(error_msg)
            return error_msg, 500