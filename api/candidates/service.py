from typing import Optional, Tuple
from candidates.schemas import CandidatesList
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
                
    async def sync_candidates(self) -> Tuple[Optional[str], int]:
        url = f"{self.api_url}/candidates"
        
        async def fetch_and_store_candidates(url: str):
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            candidates = data.get('candidates', [])
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

            # Check for paging and fetch next page if exists
            next_page = data.get('paging', {}).get('next')
            if next_page:
                await asyncio.sleep(1)  # Delay for 1 second before the next request
                await fetch_and_store_candidates(next_page)

        try:
            await fetch_and_store_candidates(url)
            return None, 200
        except Exception as e:
            error_msg = f"Error syncing candidates: {str(e)}"
            print(error_msg)
            return error_msg, 500