from fastapi import APIRouter, HTTPException, status, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.AI import svm, xgboost_model, LSTM, MLP, decision_tree
from app.services.prediction_service import predict_job_utils
from app.services.pre_processing_data_service import make_dataset
from app.services.train_service import train_model
from app.utils.train_helper_method import ModelName
from app.models.files.data_file import DataFile
from app.utils.predict_helper_method import find_person_feature_last_exam
from pydantic import BaseModel
from app.logger import logger  # ✅ اضافه کردن لاگر
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR_NAME = "uploaded_models"
UPLOAD_DIR = os.path.join(BASE_DIR, UPLOAD_DIR_NAME)

class TrainRequest(BaseModel):
    job_id: int
    exam_id: int
    model_name: ModelName
    num_classes: int

@router.post("/train_job_satisfaction", status_code=status.HTTP_200_OK)
async def train_job_satisfaction(request: TrainRequest, db: Session = Depends(get_db)):    
    logger.info(f"Start training job satisfaction model: {request.model_name}")
    job_id, exam_id, model_name, num_classes = request.job_id, request.exam_id, request.model_name, request.num_classes

    X, Y = make_dataset(job_id, exam_id, 'satisfaction_score', db)
    base_directory_model = UPLOAD_DIR

    if model_name == ModelName.SVM:
        model = svm.SVMModel
    elif model_name == ModelName.XgBoost:
        model = xgboost_model.XGBoostModel
    elif model_name == ModelName.MLP:
        model = MLP.MLPModel
    elif model_name == ModelName.DecisionTree:
        model = decision_tree.DecisionTreeModel
    else:
        raise HTTPException(status_code=400, detail="Unsupported model")

    train_model(model, X, Y, job_id, exam_id, base_directory_model, num_classes, "satisfaction_score", db)
    logger.info("Training complete for job satisfaction.")
    return {"message": "Model trained and saved successfully"}


@router.post("/train_job_improvement", status_code=status.HTTP_200_OK)
async def train_job_improvement(request: TrainRequest, db: Session = Depends(get_db)):    
    logger.info(f"Start training job improvement model: {request.model_name}")
    job_id, exam_id, model_name, num_classes = request.job_id, request.exam_id, request.model_name, request.num_classes

    X, Y = make_dataset(job_id, exam_id, 'improvement_rank', db)
    base_directory_model = UPLOAD_DIR

    if model_name == ModelName.SVM:
        model = svm.SVMModel
    elif model_name == ModelName.XgBoost:
        model = xgboost_model.XGBoostModel
    elif model_name == ModelName.MLP:
        model = MLP.MLPModel
    elif model_name == ModelName.DecisionTree:
        model = decision_tree.DecisionTreeModel
    else:
        raise HTTPException(status_code=400, detail="Unsupported model")

    train_model(model, X, Y, job_id, exam_id, base_directory_model, num_classes, "job_improvement", db)
    logger.info("Training complete for job improvement.")
    return {"message": "Model trained and saved successfully"}


@router.post("/train_job_performance", status_code=status.HTTP_200_OK)
async def train_job_performance(request: TrainRequest, db: Session = Depends(get_db)):  
    logger.info(f"Start training job performance model: {request.model_name}")
    job_id, exam_id, model_name, num_classes = request.job_id, request.exam_id, request.model_name, request.num_classes

    X, Y = make_dataset(job_id, exam_id, 'job_efficiency_rank', db)
    base_directory_model = UPLOAD_DIR

    if model_name == ModelName.SVM:
        model = svm.SVMModel
    elif model_name == ModelName.XgBoost:
        model = xgboost_model.XGBoostModel
    elif model_name == ModelName.MLP:
        model = MLP.MLPModel
    elif model_name == ModelName.DecisionTree:
        model = decision_tree.DecisionTreeModel
    else:
        raise HTTPException(status_code=400, detail="Unsupported model")

    train_model(model, X, Y, job_id, exam_id, base_directory_model, num_classes, "job_performance", db)
    logger.info("Training complete for job performance.")
    return {"message": "Model trained and saved successfully"}


@router.get("/predict_job_satisfaction", status_code=status.HTTP_200_OK)
async def predict_one_person_job_satisfaction(person_id: int, model_id: int, exam_id: int, db: Session = Depends(get_db)):
    files_by_year = DataFile.get_files_by_exam_id(db, exam_id)
    person_data, found = find_person_feature_last_exam(person_id, files_by_year)

    if not found:
        logger.warning(f"Person {person_id} not found in exam {exam_id}")
        return {"message": "Prediction failed", "result": "This person didn't participate in this exam before."}

    try:
        result = predict_job_utils("satisfaction_score", person_data, model_id, db)
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Validation error: {str(ve)}")
    except Exception:
        logger.exception("Prediction error in predict_job_satisfaction")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Prediction error occurred.")

    return {"message": "Prediction successful", "result": result}


@router.get("/predict_job_improvement", status_code=status.HTTP_200_OK)
async def predict_one_person_job_improvement(person_id: int, model_id: int, exam_id: int, db: Session = Depends(get_db)):
    files_by_year = DataFile.get_files_by_exam_id(db, exam_id)
    person_data, found = find_person_feature_last_exam(person_id, files_by_year)

    if not found:
        logger.warning(f"Person {person_id} not found in exam {exam_id}")
        return {"message": "Prediction failed", "result": "This person didn't participate in this exam before."}

    try:
        result = predict_job_utils("job_improvement", person_data, model_id, db)
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Validation error: {str(ve)}")
    except Exception:
        logger.exception("Prediction error in predict_job_improvement")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Prediction error occurred.")

    return {"message": "Prediction successful", "result": result}


@router.get("/predict_job_performance", status_code=status.HTTP_200_OK)
async def predict_one_person_job_performance(person_id: int, model_id: int, exam_id: int, db: Session = Depends(get_db)):
    files_by_year = DataFile.get_files_by_exam_id(db, exam_id)
    person_data, found = find_person_feature_last_exam(person_id, files_by_year)

    if not found:
        logger.warning(f"Person {person_id} not found in exam {exam_id}")
        return {"message": "Prediction failed", "result": "This person didn't participate in this exam before."}

    try:
        result = predict_job_utils("job_performance", person_data, model_id, db)
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Validation error: {str(ve)}")
    except Exception:
        logger.exception("Prediction error in predict_job_performance")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Prediction error occurred.")

    return {"message": "Prediction successful", "result": result}
