from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Tuple, Optional
from candidates.schemas import Candidate
from jobs.schemas import Job
from langchain_ollama import ChatOllama

from api.main import app

class GradingService:

    async def get_database(self) -> AsyncIOMotorDatabase:
        return app.state.db
    
    async def sync_resumes(self) -> Tuple[Optional[str], Optional[int]]:
        try:
            db = await self.get_database()
            jobs = await db.jobs.find().to_list(None)

            if jobs:
                for job in jobs:
                    print(f"Grading resumes for job {job.job.shortcode}")
                    candidates = await db.candidates.find({"shortcode": job.job.shortcode}).to_list(None)
                    print(f"Grading resumes for {len(candidates)} candidates")
                    for candidate in candidates:
                        # Grade the resume
                        candidate["grade"] = 100
                        await db.candidates.update_one({"id": candidate["id"]}, {"$set": candidate})
            return None, 200
        except Exception as e:
            error_msg = f"Error grading resumes: {str(e)}"
            print(error_msg)
            return error_msg, 500
        
    async def grade_resume(self, candidate: Candidate, job: Job) -> Tuple[int, str]:
        try:
            #Grading logic goes here
            return 200, "Resume graded successfully"
        except Exception as e:
            error_msg = f"Error grading resume: {str(e)}"
            print(error_msg)
            return 500, error_msg    