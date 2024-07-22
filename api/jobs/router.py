from fastapi import APIRouter, Depends, HTTPException
from jobs.schemas import JobsList, JobDetail, CandidatesList
from jobs.service import JobService

router = APIRouter(prefix="/jobs")

def get_job_service() -> JobService:
    return JobService()

@router.get("/", response_model=JobsList)
async def get_jobs(service: JobService = Depends(get_job_service)):
    jobs, status_code, error_msg = await service.get_jobs()
    if error_msg:
        raise HTTPException(status_code=status_code, detail=error_msg)
    return jobs

@router.get("/{job_id}", response_model=JobDetail)
async def get_job_detail(job_id: str, service: JobService = Depends(get_job_service)):
    job, status_code, error_msg = await service.get_job_detail(job_id)
    if error_msg:
        raise HTTPException(status_code=status_code, detail=error_msg)
    return job

@router.get("/{job_id}/candidates", response_model=CandidatesList)
async def get_candidates_for_job(job_id: str, stage: str = None, service: JobService = Depends(get_job_service)):
    candidates, status_code, error_msg = await service.get_candidates_for_job(job_id, stage)
    if error_msg:
        raise HTTPException(status_code=status_code, detail=error_msg)
    return candidates