from sqlalchemy import Column, String, Integer, Float, DateTime, JSON,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from app.database import Base


class ModelDetails(Base):
    __tablename__ = "model_details"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_object_predict = Column(String, nullable=False)  # Model name or identifier
    address = Column(String, nullable=False)  # Model storage address
    feature_engineering_details_address = Column(String, nullable=False)
    architecture = Column(String, nullable=False)  # Model architecture type
    accuracy_results = Column(JSON, nullable=False)  # JSON data for accuracy metrics
    f1_score_results = Column(JSON, nullable=False)  # JSON data for F1 scores
    precision_results = Column(JSON, nullable=False)  # JSON data for precision metrics
    recall_results = Column(JSON, nullable=False)  # JSON data for recall metrics
    t_test_results_accuracy = Column(JSON, nullable=False)  # JSON data for T-test on accuracy
    t_test_results_f1_score = Column(JSON, nullable=False)  # JSON data for T-test on F1 scores
    confidence_level_accuracy = Column(Float, nullable=False)  # Confidence level for accuracy
    confidence_level_f1_score = Column(Float, nullable=False)  # Confidence level for F1 score
    num_all_samples = Column(Integer, nullable=False)  # Total number of samples used
    num_features = Column(Integer, nullable=False)  # Number of features in the dataset
    split_test = Column(Float, nullable=False)  # Test dataset split ratio
    n_splits_t_test = Column(Integer, nullable=False)  # Number of T-test splits
    number_of_labels = Column(Integer, nullable=False)  # Number of labels in the dataset
    model_evaluation_date = Column(DateTime, nullable=False)  # Date of model evaluation
    version = Column(String, nullable=False)  # Model version
    exam_id = Column(Integer, ForeignKey("exam_details.id"), nullable=False)  # Associated exam ID

    job_id = Column(Integer, nullable=False)  # Associated job ID
    
    @classmethod
    def add_record(cls, db: Session, card_info: dict):
        """
        Adds a new record to the database using the provided card_info.
        
        Args:
            db (Session): SQLAlchemy database session.
            card_info (dict): Dictionary containing model details.
        
        Returns:
            ModelDetails: The newly added record.
        """
        try:
            record = cls(**card_info)
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
        except Exception as e:
            db.rollback()  # در صورت خطا، تراکنش را بازگردانی کنید
            raise e  # خطا را مجدداً منتشر کنید


    @classmethod
    def find_model_by_id(cls, db: Session, model_id: int):
        """
        Finds a model by its main ID.
        
        Args:
            db (Session): SQLAlchemy database session.
            model_id (int): The primary ID of the model to find.
        
        Returns:
            ModelDetails: The found record, or None if no record exists.
        """
        return db.query(cls).filter(cls.id == model_id).first()
    
    @classmethod
    def find_models_by_exam_id(cls, db: Session, exam_id: int):
        """
        Finds all models by exam ID.
        
        Args:
            db (Session): SQLAlchemy database session.
            exam_id (str): The exam ID to filter models.
        
        Returns:
            list[ModelDetails]: List of matching records.
        """
        return db.query(cls).filter(cls.exam_id == exam_id).all()
    
    @classmethod
    def find_models_by_job_id(cls, db: Session, job_id: int):
        """
        Finds all models by job ID.
        
        Args:
            db (Session): SQLAlchemy database session.
            job_id (str): The job ID to filter models.
        
        Returns:
            list[ModelDetails]: List of matching records.
        """
        return db.query(cls).filter(cls.job_id == job_id).all()


    @classmethod
    def find_models_by_exam_and_job_id(cls, db: Session, exam_id: int = None, job_id: int = None):
        """
        Finds all models by exam ID, job ID, or both.
        
        Args:
            db (Session): SQLAlchemy database session.
            exam_id (str): The exam ID to filter models (optional).
            job_id (str): The job ID to filter models (optional).
        
        Returns:
            list[ModelDetails]: List of matching records.
        """
        query = db.query(cls)
        if exam_id:
            query = query.filter(cls.exam_id == exam_id)
        if job_id:
            query = query.filter(cls.job_id == job_id)
        return query.all()


    @classmethod
    def delete_model_by_id(cls, db: Session, model_id: int):
        model = db.query(cls).filter_by(id=model_id).first()
        if model:
            db.delete(model)
            db.commit()
            return True
        return False

    @classmethod
    def update_model(cls, db: Session, model_id: int, update_info: dict):
        model = db.query(cls).filter_by(id=model_id).first()
        if model:
            for key, value in update_info.items():
                if hasattr(model, key):  # بررسی وجود ویژگی در مدل
                    setattr(model, key, value)
            db.commit()
            db.refresh(model)
            return model
        return None
