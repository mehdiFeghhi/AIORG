from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.AI.ModelDetails import ModelDetails
from typing import List, Dict, Optional
from datetime import datetime

router = APIRouter()


@router.get("/details_by_id", status_code=status.HTTP_200_OK)
async def find_model_details_by_id(
    query_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, str | int | float | None | Dict[str, float] | datetime]:
    """
    Fetch model details by its unique ID.

    Args:
        query_id (int): The unique ID of the model.
        db (Session): SQLAlchemy session (provided by Depends).
    Returns:
        dict: Model details in JSON format.
    """

    model_details = ModelDetails.find_model_by_id(db, query_id)


    print(f"res: {model_details}")

    if not model_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with ID {query_id} not found."
        )

    return {
        "address": model_details.address,
        "architecture": model_details.architecture,
        "accuracy_results": model_details.accuracy_results,
        "f1_score_results": model_details.f1_score_results,
        "precision_results": model_details.precision_results,
        "recall_results": model_details.recall_results,
        "t_test_results_accuracy": model_details.t_test_results_accuracy,
        "t_test_results_f1_score": model_details.t_test_results_f1_score,
        "confidence_level_accuracy": model_details.confidence_level_accuracy,
        "confidence_level_f1_score": model_details.confidence_level_f1_score,
        "num_all_samples": model_details.num_all_samples,
        "num_features": model_details.num_features,
        "split_test": model_details.split_test,
        "n_splits_t_test": model_details.n_splits_t_test,
        "number_of_labels": model_details.number_of_labels,
        "model_evaluation_date": model_details.model_evaluation_date,
        "version": model_details.version,
        "job_id": model_details.job_id,
        "exam_id": model_details.exam_id,
    }




@router.get("/details_by_exam_and_job", status_code=status.HTTP_200_OK)
async def find_models_by_exam_and_job(
    exam_id: Optional[int] = None,
    job_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> List[Dict[str, Optional[str] | int | Dict[str, float]]]:
    """
    Fetches model details based on exam_id and job_id.

    Args:
        exam_id (int, optional): The exam ID to filter models. Defaults to None.
        job_id (int, optional): The job ID to filter models. Defaults to None.
        db (Session): SQLAlchemy database session.

    Returns:
        list[dict]: List of dictionaries with model details.
    """
    models = ModelDetails.find_models_by_exam_and_job_id(db, exam_id, job_id)

    result = [
        {
            "model_id": model.id,
            "version": model.version,
            "model_name": model.name_object_predict,
            "accuracy_result": model.accuracy_results
        }
        for model in models
    ]
    return result