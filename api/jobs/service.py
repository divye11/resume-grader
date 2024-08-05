import asyncio
import os
import requests
from requests.exceptions import RequestException
from typing import Tuple, Optional
from api.main import app
from jobs.schemas import Job, JobDetail, JobsList, CandidatesList
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from bs4 import BeautifulSoup 

class JobService:
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

   async def get_jobs(self) -> Tuple[Optional[JobsList], int, Optional[str]]:
      try:
         db = await self.get_database()
         jobs = await db.jobs.find().to_list(None)
         return JobsList(jobs=jobs), 200, None
      except RequestException as e:
         error_msg = f"Error fetching jobs: {str(e)}"
         print(error_msg)
         return None, 500, error_msg
   
   async def get_job_detail(self, job_id) -> Tuple[Optional[JobDetail], int, Optional[str]]:
      try:
         db = await self.get_database()
         job_detail = db.jobs.find_one({"shortcode": job_id})
         if job_detail is None:
            return None, 404, f"Job with id {job_id} not found"
         return job_detail, 200, None
      except RequestException as e:
         error_msg = f"Error fetching job detail for job_id {job_id}: {str(e)}"
         print(error_msg)
         status_code = 500
         return None, status_code, error_msg
      
   async def get_candidates_for_job(self, job_id, stage=None) -> Tuple[Optional[CandidatesList], int, Optional[str]]:
      try:
         db = await self.get_database()
         candidates = await db.candidates.find({"shortcode": job_id, "stage": stage}).to_list(None)
         return CandidatesList(candidates=candidates), 200, None
      except Exception as e:
         error_msg = f"Error fetching candidates for job_id {job_id}{' and stage ' + stage if stage else ''}: {str(e)}"
         print(error_msg)
         return None, 500, error_msg
   
   async def store_jobs(self, jobs: list[Job]) -> Tuple[int, int, int]:
      try: 
         db = await self.get_database()
         # Prepare bulk operations
         operations = [
            UpdateOne(
               {"id": job["id"]},
               {"$setOnInsert": job},
               upsert=True
            ) for job in jobs
         ]
         
         # Perform bulk write
         result = await db.jobs.bulk_write(operations)

         return result.matched_count, result.modified_count, result.upserted_count
      except Exception as e:
         error_msg = f"Error storing jobs: {str(e)}"
         print(error_msg)
         raise e

   async def fetch_jobs(self, url: str) -> Tuple[list[Job], Optional[str]]:
      try:
         response = self.session.get(url)
         response.raise_for_status()
         data = response.json()
         jobs = data.get('jobs', [])
         paging = data.get('paging', {})
         print(f"data is {data}")
         return jobs, paging.get('next')
      except RequestException as e:
         error_msg = f"Error fetching jobs: {str(e)}"
         print(error_msg)
         raise e

   async def sync_jobs(self) -> Tuple[Optional[str], int]:
        url = f"{self.api_url}/jobs?state=published"
        try:
            db = await self.get_database()
            latest_job_in_db = await db.jobs.find_one({}, sort=[("created_at", -1)])
            print("latest job is", latest_job_in_db)
            if latest_job_in_db:
               last_job_added = [latest_job_in_db]
               since_id = last_job_added[0]["id"]
               url += f"&since_id={since_id}"
            print(f"url is {url}")
            while url:
               await asyncio.sleep(1)
               jobs, next_url = await self.fetch_jobs(url)
               print(f"next url {next_url}")
               matched, modified, upserted = await self.store_jobs(jobs)
               print(f"Matched: {matched}, modified: {modified}, upserted: {upserted}")
               url = next_url
                         
            return f"Matched: {matched}, modified: {modified}, upserted: {upserted}", 200                
        except RequestException as e:
            error_msg = f"Error syncing jobs: {str(e)}"
            print(error_msg)
            return error_msg, 500

   async def fetch_job_detail(self, shortcode: str) -> Job:
      try:
         if not shortcode:
            raise ValueError("Shortcode cannot be empty")
         
         url = f"{self.api_url}/jobs/{shortcode}"
         response = self.session.get(url)
         response.raise_for_status()
         return response.json()
      
      except Exception as e:
         error_msg = f"Error fetching job description: {str(e)}"
         print(error_msg)
         raise e

   async def sync_job_descriptions(self) -> Tuple[Optional[str], int]:
      try:
         db = await self.get_database()
         jobs = await db.jobs.find().to_list(None)
         for job in jobs:
            await asyncio.sleep(1)
            job_id = job["shortcode"]
            job_details = await self.fetch_job_detail(job_id)
            parsed_description = BeautifulSoup(job_details.get("description"), "lxml").get_text()
            parsed_full_description = BeautifulSoup(job_details.get("full_description"), "lxml").get_text()
            update_fields = {
                "description": parsed_description,
                "full_description": parsed_full_description,
                "requirements": job_details.get("requirements"),
                "benefits": job_details.get("benefits"),
                "employment_type": job_details.get("employment_type"),
                "industry": job_details.get("industry"),
                "experience": job_details.get("experience")
            }
            await db.jobs.update_one(
                {"shortcode": job_id},
                {"$set": update_fields}
            )
         return None, 200
      except RequestException as e:
         error_msg = f"Error syncing job descriptions: {str(e)}"
         print(error_msg)
         raise e
      
   async def sync_job(self, shortcode) -> Tuple[Optional[str], int]:
      url = f"{self.api_url}/jobs/{shortcode}"
      try:
         response = self.session.get(url)
         response.raise_for_status()
         job = response.json()
         db = await self.get_database()
         await db.jobs.update_one(
            {"shortcode": shortcode},
            {"$set": job},
            upsert=True
         )
         return None, 200
      except RequestException as e:
         error_msg = f"Error syncing job {shortcode}: {str(e)}"
         print(error_msg)
         raise e