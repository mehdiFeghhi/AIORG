from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import Session
from khayyam import JalaliDatetime
from datetime import datetime
from app.database import Base

class JobPerformance(Base):
    __tablename__ = "job_performance"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, nullable=False)  # Reference to a person ID
    job_efficiency_rank = Column(Float, nullable=False)
    improvement_rank = Column(Float, nullable=False)
    satisfaction_score = Column(Float, nullable=False)
    job_id = Column(Integer, nullable=False)  # The ID of the job
    created_at = Column(DateTime, nullable=False)  # Timestamp for when the record was created

    @classmethod
    def add_performance(cls, db: Session, person_id: int, job_efficiency_rank: float, 
                        improvement_rank: float, satisfaction_score: float, job_id: int, created_at: str ):
        """
        Creates a new job performance record and adds it to the database.

        Args:
            db (Session): SQLAlchemy database session.
            person_id (int): The person ID of the employee.
            job_efficiency_rank (float): The rank for the employee's job efficiency (1-10).
            improvement_rank (float): The rank for the employee's improvement (1-10).
            satisfaction_score (float): The score for the employee's job satisfaction (1-10).
            job_id (int): The job ID associated with the performance record.
            created_at (str, optional): The creation timestamp in Jalali calendar format (yyyy/mm/dd).

        Returns:
            JobPerformance: The newly created job performance record.
        """
        try:
            # Convert the provided Jalali datetime string to Gregorian datetime
            jalali_datetime = JalaliDatetime.strptime(created_at, "%Y/%m/%d")
            gregorian_datetime = jalali_datetime.todatetime()  # Convert to Gregorian datetime
            
            # Extract Jalali year from the provided date
            jalali_year = jalali_datetime.year
            
            # Convert start and end of the Jalali year to Gregorian
            start_of_year = JalaliDatetime(jalali_year, 1, 1).todatetime()
            end_of_year = JalaliDatetime(jalali_year, 12, 29).todatetime()
            
            # Check if a record for the same person_id already exists in the same Jalali year
            existing_record = db.query(cls).filter(
                cls.person_id == person_id,
                cls.created_at >= start_of_year,
                cls.created_at <= end_of_year
            ).first()

            if existing_record:
                raise ValueError("A record for this person already exists in the same Jalali year.")
            
            # Create a new job performance instance
            new_performance = cls(
                person_id=person_id,
                job_efficiency_rank=job_efficiency_rank,
                improvement_rank=improvement_rank,
                satisfaction_score=satisfaction_score,
                job_id=job_id,
                created_at=gregorian_datetime  # Store the Gregorian datetime
            )

            # Add the new performance to the session and commit
            db.add(new_performance)
            db.commit()
            db.refresh(new_performance)

            return new_performance

        except ValueError as e:
            # Handle invalid Jalali date format or duplicate entry
            print(f"Error: {e}")
            raise e
   


    @classmethod
    def update_performance(cls, db: Session, record_id: int, **kwargs):
        """
        Updates an existing job performance record.
        """
        record = db.query(cls).filter(cls.id == record_id).first()
        if not record:
            raise ValueError("Record not found.")

        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
        
        db.commit()
        db.refresh(record)
        return record
    
    @classmethod
    def update_performance_by_person_and_date(cls, db: Session, person_id: int, job_id: int, created_at: str, **kwargs):
        """
        Updates an existing job performance record based on person_id and created_at within the same Jalali year.

        Args:
            db (Session): SQLAlchemy database session.
            person_id (int): The person ID to find the record.
            job_id (int): The job ID associated with the record.
            created_at (str): The creation timestamp in Jalali calendar format (yyyy/mm/dd).
            **kwargs: Fields to update (job_efficiency_rank, improvement_rank, satisfaction_score, etc.).

        Returns:
            JobPerformance: The updated job performance record.
        """
        try:
            # Convert the provided Jalali datetime string to Gregorian datetime
            try:
                jalali_datetime = JalaliDatetime.strptime(created_at, "%Y/%m/%d")
            except ValueError:
                raise ValueError("Invalid date format. Expected format: YYYY/MM/DD")

            gregorian_datetime = jalali_datetime.todatetime()  # Convert to Gregorian datetime

            # Extract Jalali year
            jalali_year = jalali_datetime.year

            # Convert start and end of the Jalali year to Gregorian
            start_of_year = JalaliDatetime(jalali_year, 1, 1).todatetime()
            # Handle Esfand (last month) dynamically to avoid day errors
            end_of_year = JalaliDatetime(jalali_year, 12, 29).todatetime()

            # Query for the existing record within the same Jalali year
            record = db.query(cls).filter(
                cls.person_id == person_id,
                cls.job_id == job_id,
                cls.created_at >= start_of_year,
                cls.created_at <= end_of_year
            ).first()

            if not record:
                raise ValueError("No record found for this person in the same Jalali year.")

            # Validate and update fields
            valid_fields = {"job_efficiency_rank", "improvement_rank", "satisfaction_score"}
            for key, value in kwargs.items():
                if key in valid_fields and value is not None:
                    setattr(record, key, value)

            db.commit()
            db.refresh(record)
            return record

        except ValueError as e:
            raise ValueError(f"Error updating job performance: {e}")


    @classmethod
    def get_performance_by_job_and_date(cls, db: Session, job_id: int, performance_metric: str):
        """
        Retrieves all people with the given job_id, organized by Persian calendar year.

        Args:
            db (Session): SQLAlchemy database session.
            job_id (int): The job ID to filter by.
            performance_metric (str): The performance metric to include in the results.
                Accepted values: 'job_efficiency_rank', 'improvement_rank', 'satisfaction_score'.

        Returns:
            dict: A dictionary where the keys are Persian calendar years and the values are
                lists of dictionaries with person_id and the requested performance metric.

        Raises:
            ValueError: If the performance_metric is not valid.
        """
        # Validate the requested performance metric
        if performance_metric not in ['job_efficiency_rank', 'improvement_rank', 'satisfaction_score']:
            raise ValueError(
                "Invalid performance_metric. Choose from 'job_efficiency_rank', 'improvement_rank', 'satisfaction_score'."
            )

        # Query the database for all records with the given job_id
        records = db.query(cls).filter(cls.job_id == job_id).all()

        # Organize results into the desired dictionary format
        performance_by_year = {}

        for record in records:
            # Extract the Persian calendar year from the created_at field
            persian_year = JalaliDatetime(record.created_at).year

            # Initialize the year's entry in the dictionary if it doesn't exist
            if persian_year not in performance_by_year:
                performance_by_year[persian_year] = []

            # Append the person's data with the requested performance metric
            performance_by_year[persian_year].append({
                'person_id': record.person_id,
                'performance_value': getattr(record, performance_metric)
            })

        return performance_by_year


    @classmethod
    def get_performance_by_jobs_and_date(cls, db: Session, job_ids: list, performance_metric: str):
        """
        Retrieves all people with the given job_ids, organized by Persian calendar year.

        Args:
            db (Session): SQLAlchemy database session.
            job_ids (list): A list of job IDs to filter by.
            performance_metric (str): The performance metric to include in the results.
                Accepted values: 'job_efficiency_rank', 'improvement_rank', 'satisfaction_score'.

        Returns:
            dict: A dictionary where the keys are Persian calendar years and the values are
                lists of dictionaries with job_id, person_id, and the requested performance metric.

        Raises:
            ValueError: If the performance_metric is not valid.
        """
        # Validate the requested performance metric
        if performance_metric not in ['job_efficiency_rank', 'improvement_rank', 'satisfaction_score']:
            raise ValueError(
                "Invalid performance_metric. Choose from 'job_efficiency_rank', 'improvement_rank', 'satisfaction_score'."
            )

        # Query the database for all records with the given job_ids
        records = db.query(cls).filter(cls.job_id.in_(job_ids)).all()

        # Organize results into the desired dictionary format
        performance_by_year = {}

        for record in records:
            # Extract the Persian calendar year from the created_at field
            persian_year = JalaliDatetime(record.created_at).year

            # Initialize the year's entry in the dictionary if it doesn't exist
            if persian_year not in performance_by_year:
                performance_by_year[persian_year] = []

            # Append the job_id, person's data, and the requested performance metric
            performance_by_year[persian_year].append({
                'job_id': record.job_id,
                'person_id': record.person_id,
                'performance_value': getattr(record, performance_metric)
            })

        return performance_by_year
    
    @classmethod
    def get_performance_by_person_and_year(cls, db: Session, person_id: int, year: int):
        """
        Retrieves the performance records of a specific person for a given Jalali year.
        """
        start_of_year = JalaliDatetime(year, 1, 1).todatetime()
        end_of_year = JalaliDatetime(year, 12, 29).todatetime()

        records = db.query(cls).filter(
            cls.person_id == person_id,
            cls.created_at >= start_of_year,
            cls.created_at <= end_of_year
        ).all()

        return [
            {
                'job_id': record.job_id,
                'job_efficiency_rank': record.job_efficiency_rank,
                'improvement_rank': record.improvement_rank,
                'satisfaction_score': record.satisfaction_score,
                'created_at': record.created_at
            } for record in records
        ]
    
    @classmethod
    def update_performance(cls, db: Session, record_id: int, **kwargs):
        """
        Updates an existing job performance record.
        """
        record = db.query(cls).filter(cls.id == record_id).first()
        if not record:
            raise ValueError("Record not found.")

        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
        
        db.commit()
        db.refresh(record)
        return record
