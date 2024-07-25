from typing import List, Optional, Tuple
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

        async def fetch_candidates(url: str) -> Tuple[List[dict], Optional[str]]:
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

        async def store_candidates(candidates: List[dict]) -> Tuple[int, int, int]:
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

        async def sync_candidates(url) -> Tuple[Optional[str], int]:
            input_url = url            
            try:
                while input_url:
                    candidates, next_page = await fetch_candidates(input_url)
                    await store_candidates(candidates)
                    
                    if next_page:
                        await asyncio.sleep(1)  # Delay for 1 second before the next request
                        input_url = next_page
                    else:
                        input_url = None
                
                return None, 200
            except Exception as e:
                error_msg = f"Error syncing candidates: {str(e)}"
                print(error_msg)
                raise e

        try:
            await sync_candidates(url)
            return None, 200
        except Exception as e:
            error_msg = f"Error syncing candidates: {str(e)}"
            print(error_msg)
            return error_msg, 500