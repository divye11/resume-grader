from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Tuple, Optional
from candidates.schemas import Candidate
from jobs.schemas import Job
from langchain_community.document_loaders import PDFMinerLoader
from urllib.parse import urlparse
from io import BytesIO
import requests
import fitz 
from docx import Document 

from api.main import app
from grading.llm_service import LLmGradingService

class GradingService:

    def __init__(self) -> None:
        self.session = requests.Session()
        self.grading_service = LLmGradingService()
        

    async def get_database(self) -> AsyncIOMotorDatabase:
        return app.state.db
    
    async def sync_resumes(self) -> Tuple[Optional[str], Optional[int]]:
        try:
            db = await self.get_database()
            jobs = await db.jobs.find({"shortcode": "C2A884697D"}).to_list(None)
            if jobs:
                for job in jobs:
                    candidates = await db.candidates.find({"job.shortcode": job.get('shortcode')}).to_list(None)
                    print(f"Found {len(candidates)} candidates for job {job.get('title')}")
                    for candidate in candidates:
                        # Grade the resume
                        result =  await self.grade_resume(candidate, job)
                        print(f"Result summary: {result.get('summary')}, grade: {result.get('grade')}")

            return None, 200
        except Exception as e:
            error_msg = f"Error syncing resumes: {str(e)}"
            print(error_msg)
            return error_msg, 500, None
        
    async def grade_resume(self, candidate: Candidate, job: Job) -> Tuple[str, int]:
        try:
            resume = await self.fetch_resume(candidate)
            resume_content = await self.extract_resume_text(resume)
            description, full_description, title, employment_type, experience = self.fetch_job_context(job)
            job_context = f"Job Title: {title}\nJob Description: {full_description}\nEmployment Type: {employment_type}\nExperience Required: {experience}\nJob Description: {description}"
            response = await self.grading_service.grade_resume(resume_content, job_context)
            await self.store_candidate_data(resume_content, job, candidate, response)

            return response
        except Exception as e:
            error_msg = f"Error grading resume: {str(e)}"
            print(error_msg)
            return 500, error_msg    
                
    async def fetch_resume(self, candidate):
        try:
            resume_url = candidate.get('resume_url')
            if resume_url:
                print(f">>>>>>>Fetching resume from {resume_url}")
                # Use the signed URL directly to fetch the resume
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                response = requests.get(resume_url, headers=headers, timeout=100)  # Use requests to fetch the PDF
                response.raise_for_status()  # Raise an error for bad responses
                pdf_file = BytesIO(response.content)  # Read the content into a BytesIO object
                return pdf_file
            else:
                return None
        except Exception as e:
            error_msg = f"Error fetching resume: {str(e)}"
            print(error_msg)
            return None
        
    async def extract_resume_text(self, resume) -> str:
        try:
            if resume:
                # Check if the resume is a PDF or DOCX
                resume.seek(0)  # Reset the stream position
                resume_bytes = resume.getbuffer().tobytes()  # Convert to bytes
                if resume_bytes.startswith(b'%PDF'):  # Check for PDF magic number
                    doc = fitz.open(stream=resume)
                    text_by_page = []
                    for page in doc:
                        blocks = page.get_text("dict")["blocks"]
                        page_text = []
                        for block in blocks:
                            if block["type"] == 0:  # Text
                                for line in block["lines"]:
                                    for span in line["spans"]:
                                        page_text.append((span["bbox"], span["text"]))
                        
                        # Sort by vertical position, then horizontal
                        page_text.sort(key=lambda x: (x[0][1], x[0][0]))
                        text_by_page.append(" ".join(text for _, text in page_text))
                    
                    return "\n\n".join(text_by_page)
                elif resume_bytes.startswith(b'PK\x03\x04'):  # Check for DOCX magic number
                    # Handle DOCX files
                    doc = Document(resume)
                    text = []
                    for paragraph in doc.paragraphs:
                        text.append(paragraph.text)
                    return "\n\n".join(text)
        except Exception as e:
            error_msg = f"Error extracting resume text: {str(e)}"
            print(error_msg)
            return ""
    
    def fetch_job_context(self, job) -> Tuple[str, str, str, str, str]:
        try:
            description = job.get('description', "")
            full_description = job.get('full_description', "")
            title = job.get('title', "")
            employment_type = job.get('employment_type', "")
            experience = job.get('experience', "")
            return description, full_description, title, employment_type, experience
        except Exception as e:
            error_msg = f"Error fetching job context: {str(e)}"
            print(error_msg)
            return "", "", "", "", ""
        
    async def store_candidate_data(self, resume_content: str, job: Job, candidate: Candidate, result):
        try:
            print('storing candidate data')
            db = await self.get_database()
            await db.candidate_grades.insert_one({
                "resume_content": resume_content,
                "job_shortcode": job.get('shortcode'),
                "candidate_id": candidate.get('id'),
                "candidate_assessment": result.get('summary'),
                "grade": result.get('grade')
            })
            return 200
        except Exception as e:
            error_msg = f"Error storing candidate data: {str(e)}"
            print(error_msg)
            return 500