from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from typing import List, Dict, Union
from khayyam import JalaliDatetime
from app.database import get_db
from app.models.job_performance.job_performance import JobPerformance

router = APIRouter()

@router.post("/add", response_model=Dict[str, Union[str, int, float]])
def add_job_performance(
    person_id: int,
    job_efficiency_rank: float,
    improvement_rank: float,
    satisfaction_score: float,
    job_id: int,
    created_at: str,
    db: Session = Depends(get_db),
):
    """
    Add a new job performance record.
    """
    try:
        new_performance = JobPerformance.add_performance(
            db, person_id, job_efficiency_rank, improvement_rank, satisfaction_score, job_id, created_at
        )
        return {
            "id": new_performance.id,
            "person_id": new_performance.person_id,
            "job_efficiency_rank": new_performance.job_efficiency_rank,
            "improvement_rank": new_performance.improvement_rank,
            "satisfaction_score": new_performance.satisfaction_score,
            "job_id": new_performance.job_id,
            "created_at": new_performance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/performance/{job_id}/{metric}", response_model=Dict[int, List[Dict[str, Union[int, float]]]])
def get_performance_by_job(
    job_id: int, metric: str, db: Session = Depends(get_db)
):
    """
    Get job performance data by job ID, grouped by Persian calendar year.
    """
    try:
        return JobPerformance.get_performance_by_job_and_date(db, job_id, metric)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/performance_jobs", response_model=Dict[int, List[Dict[str, Union[int, float]]]])
def get_performance_by_jobs(
    performance_metric: str, 
    job_ids: Dict[str, List[int]], 
    db: Session = Depends(get_db)
):
    """
    Get job performance data by multiple job IDs, grouped by Persian calendar year.
    """
    try:
        list_job_ids = job_ids.get("list_job_ids", [])
        return JobPerformance.get_performance_by_jobs_and_date(db, list_job_ids, performance_metric)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/update/{person_id}/{job_id}", response_model=Dict[str, Union[int, float, str]])
def update_job_performance(
    person_id: int,
    job_id: int,
    created_at: str = Query(..., description="Date in YYYY-MM-DD format"),
    job_efficiency_rank: float = None,
    improvement_rank: float = None,
    satisfaction_score: float = None,
    db: Session = Depends(get_db)
):
    """
    Update a job performance record for a specific person in the same Jalali year based on created_at.
    """
    try:
        updated_record = JobPerformance.update_performance_by_person_and_date(
            db, person_id, job_id, created_at,
            job_efficiency_rank=job_efficiency_rank,
            improvement_rank=improvement_rank,
            satisfaction_score=satisfaction_score,
        )
        
        return {
            "id": updated_record.id,
            "person_id": updated_record.person_id,
            "job_efficiency_rank": updated_record.job_efficiency_rank,
            "improvement_rank": updated_record.improvement_rank,
            "satisfaction_score": updated_record.satisfaction_score,
            "job_id": updated_record.job_id,
            "created_at": updated_record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
