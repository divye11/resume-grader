from jobs.schemas import JobsList, JobDetail, CandidatesList
import os
import requests
from requests.exceptions import RequestException
from typing import Tuple, Optional

class JobService:
   def __init__(self) -> None:
      self.api_key = os.getenv('WORKABLE_API_KEY')
      self.api_url = os.getenv('WORKABLE_URL')
      self.session = requests.Session()
      self.session.headers.update({
         "Authorization": f"Bearer {self.api_key}",
         "Content-Type": "application/json"
      })

   async def get_jobs(self) -> Tuple[Optional[JobsList], int, Optional[str]]:
      url = f"{self.api_url}/jobs"
      try:
         response = self.session.get(url)
         response.raise_for_status()
         return response.json(), 200, None
      except RequestException as e:
         error_msg = f"Error fetching jobs: {str(e)}"
         print(error_msg)
         return None, 500, error_msg
   
   async def get_job_detail(self, job_id) -> Tuple[Optional[JobDetail], int, Optional[str]]:
      url = f"{self.api_url}/jobs/{job_id}"
      try:
         response = self.session.get(url)
         response.raise_for_status()
         return response.json(), 200, None
      except RequestException as e:
         if isinstance(e, requests.HTTPError) and e.response.status_code == 404:
            error_msg = f"Job with id {job_id} not found"
         else:
            error_msg = f"Error fetching job detail for job_id {job_id}: {str(e)}"
         print(error_msg)
         status_code = e.response.status_code if isinstance(e, requests.HTTPError) else 500
         return None, status_code, error_msg
      
   async def get_candidates_for_job(self, job_id, stage=None) -> Tuple[Optional[CandidatesList], int, Optional[str]]:
      url = f"{self.api_url}/candidates?job_id={job_id}"
      if stage:
         url += f"&stage={stage}"
      try:
         response = self.session.get(url)
         response.raise_for_status()
         return response.json(), 200, None
      except RequestException as e:
         error_msg = f"Error fetching candidates for job_id {job_id}{' and stage ' + stage if stage else ''}: {str(e)}"
         print(error_msg)
         return None, 500, error_msg