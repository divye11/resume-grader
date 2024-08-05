from fastapi import APIRouter, Depends, HTTPException
from grading.service import GradingService

router = APIRouter(prefix="/grading")

def get_grading_service() -> GradingService:
    return GradingService()

@router.get("/sync")
async def grade_resumes(service: GradingService = Depends(get_grading_service)):
    error_msg, status_code = await service.sync_resumes()
    if error_msg:
        raise HTTPException(status_code=status_code, detail=error_msg)
    return {"message": "Resumes graded successfully" }