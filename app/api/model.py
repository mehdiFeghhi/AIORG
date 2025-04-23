from fastapi import APIRouter, HTTPException, status,Depends
from app.database import get_db
from enum import Enum
from sqlalchemy.orm import Session
from app.models.AI import svm,xgboost_model,LSTM,MLP,decision_tree
from app.services.prediction_service import predict_job_utils
from app.services.pre_processing_data_service import make_dataset
from app.services.train_service import train_model
from app.utils.train_helper_method import ModelName
from app.models.files.data_file import DataFile
from app.utils.predict_helper_method import find_person_feature_last_exam
from pydantic import BaseModel

router = APIRouter()


class TrainRequest(BaseModel):
    job_id: int
    exam_id: int
    model_name: ModelName
    num_classes: int

@router.post("/train_job_satisfaction", status_code=status.HTTP_200_OK)
async def train_job_satisfaction(
    request : TrainRequest,
    db: Session = Depends(get_db)
):    
    print("db in endpoint:", type(db))
    job_id = request.job_id
    exam_id = request.exam_id
    model_name = request.model_name
    num_classes = request.num_classes

    X,Y = make_dataset(job_id,exam_id,'satisfaction_score',db)
    base_directory_model = ""
        # Now, call the function that trains the model with these hyperparameters
    if model_name == ModelName.SVM:
        model = svm.SVMModel  # Example: Replace with your actual model initialization

    # elif model_name == ModelName.LSTM:
    #     model = LSTM.LSTMModel  # Example: Replace with your actual model initialization

    elif model_name == ModelName.XgBoost:
        model = xgboost_model.XGBoostModel  # Example: Replace with your actual model initialization


    elif model_name == ModelName.MLP:
        model = MLP.MLPModel

    elif model_name == ModelName.DecisionTree:
        model = decision_tree.DecisionTreeModel  # Example: Replace with your actual model initialization

    train_model(model,X,Y,job_id,exam_id,base_directory_model,num_classes,"satisfaction_score",db = db)


    return {"message": "Model trained and saved successfully"}


    




@router.post("/train_job_improvement", status_code=status.HTTP_200_OK)
async def train_job_improvement(
    request : TrainRequest,
    db: Session = Depends(get_db)
):    
    print("db in endpoint:", type(db))
    job_id = request.job_id
    exam_id = request.exam_id
    model_name = request.model_name
    num_classes = request.num_classes

    X,Y = make_dataset(job_id,exam_id,'improvement_rank',db)
    base_directory_model = ""
        # Now, call the function that trains the model with these hyperparameters
    if model_name == ModelName.SVM:
        model = svm.SVMModel  # Example: Replace with your actual model initialization

    # elif model_name == ModelName.LSTM:
    #     model = LSTM.LSTMModel  # Example: Replace with your actual model initialization

    elif model_name == ModelName.XgBoost:
        model = xgboost_model.XGBoostModel # Example: Replace with your actual model initialization

    elif model_name == ModelName.MLP:
        model = MLP.MLPModel  # Example: Replace with your actual model initialization

    elif model_name == ModelName.DecisionTree:
        model = decision_tree.DecisionTreeModel  # Example: Replace with your actual model initialization

    train_model(model,X,Y,job_id,exam_id,base_directory_model,num_classes,"job_improvement",db)


    return {"message": "Model trained and saved successfully"}


@router.post("/train_job_performance", status_code=status.HTTP_200_OK)
async def train_job_performance(
    request : TrainRequest,
    db: Session = Depends(get_db)
):  
    print("db in endpoint:", type(db))
    job_id = request.job_id
    exam_id = request.exam_id
    model_name = request.model_name
    num_classes = request.num_classes

    X,Y = make_dataset(job_id,exam_id,'job_efficiency_rank',db)
    base_directory_model = ""
        # Now, call the function that trains the model with these hyperparameters
    if model_name == ModelName.SVM:
        model = svm.SVMModel  # Example: Replace with your actual model initialization

    # elif model_name == ModelName.LSTM:
    #     model = LSTM.LSTMModel  # Example: Replace with your actual model initialization

    elif model_name == ModelName.XgBoost:
        model = xgboost_model.XGBoostModel  # Example: Replace with your actual model initialization


    elif model_name == ModelName.MLP:
        model = MLP.MLPModel  # Example: Replace with your actual model initialization


    elif model_name == ModelName.DecisionTree:
        model = decision_tree.DecisionTreeModel  # Example: Replace with your actual model initialization

    train_model(model,X,Y,job_id,exam_id,base_directory_model,num_classes,"job_performance",db)


    return {"message": "Model trained and saved successfully"}



@router.post("/predict_job_satisfaction", status_code=status.HTTP_200_OK)
async def predict_one_person_job_satisfaction(person_id: int, model_id: str, exam_id: str,db: Session = Depends(get_db)):
    """
    Predict job satisfaction, improvement status, and profit potential
    based on employee data.
    """
    # Step 1: 

    files_by_year = DataFile.get_files_by_exam_id(db,exam_id)

    person_data,flage_find = find_person_feature_last_exam(person_id,files_by_year)

    if not flage_find:
        return {"message": "Prediction faild", "result": "This person don't involve in this exam before."}

    try:
        # Step 2: Perform the prediction
        result = predict_job_utils("satisfaction_score",person_data, model_id,db)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )

    # Step 3: Return the result
    return {"message": "Prediction successful", "result": result}



@router.post("/predict_job_improvement", status_code=status.HTTP_200_OK)
async def predict_one_person_job_improvement(person_id: int, model_id: int, exam_id: int,db: Session = Depends(get_db)):
    """
    Predict job improvement, improvement status, and profit potential
    based on employee data.
    """
    # Step 1: 

    files_by_year = DataFile.get_files_by_exam_id(db,exam_id)

    person_data,flage_find = find_person_feature_last_exam(person_id,files_by_year)

    if not flage_find:
        return {"message": "Prediction faild", "result": "This person don't involve in this exam before."}

    try:
        # Step 2: Perform the prediction
        result = predict_job_utils("job_improvement",person_data, model_id,db)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )

    # Step 3: Return the result
    return {"message": "Prediction successful", "result": result}


@router.post("/predict_job_performance", status_code=status.HTTP_200_OK)
async def predict_one_person_job_performance(person_id: int, model_id: int, exam_id: int,db: Session = Depends(get_db)):
    """
    Predict job performance, improvement status, and profit potential
    based on employee data.
    """
    # Step 1: 

    files_by_year = DataFile.get_files_by_exam_id(db,exam_id)

    person_data,flage_find = find_person_feature_last_exam(person_id,files_by_year)

    if not flage_find:
        return {"message": "Prediction faild", "result": "This person don't involve in this exam before."}

    try:
        # Step 2: Perform the prediction
        result = predict_job_utils("job_performance",person_data, model_id,db)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )

    # Step 3: Return the result
    return {"message": "Prediction successful", "result": result}
