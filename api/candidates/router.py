
from fastapi import APIRouter, Depends, HTTPException
from jobs.schemas import CandidatesList
from candidates.service import CandidateSerice

router = APIRouter(prefix="/candidates")


def get_candidates_service() -> CandidateSerice:
    return CandidateSerice()

@router.get("/", response_model=CandidatesList)
async def get_candidates(service: CandidateSerice = Depends(get_candidates_service)):
    candidates, status_code, error_msg = await service.get_candidates()
    if error_msg:
        raise HTTPException(status_code=status_code, detail=error_msg)
    return candidates

@router.get("/sync")
async def sync_candidates(service: CandidateSerice = Depends(get_candidates_service)):
    error_msg, status_code = await service.sync_candidates()
    if error_msg:
        raise HTTPException(status_code=status_code, detail=error_msg)
    return {"message": "Candidates synced successfully"}

@router.get("/sync/details")    
async def sync_candidate_details(service: CandidateSerice = Depends(get_candidates_service)):
    error_msg, status_code = await service.sync_candidate_details()
    if error_msg:
        raise HTTPException(status_code=status_code, detail=error_msg)
    return {"message": "Candidate details synced successfully"}