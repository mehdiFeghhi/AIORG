from sqlalchemy import Column, String, Integer,UniqueConstraint
from sqlalchemy.orm import relationship,Session
from app.database import Base
from sqlalchemy.exc import IntegrityError


class ExamDetails(Base):
    __tablename__ = "exam_details"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    creator_name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    __table_args__ = (UniqueConstraint('title', name='_title_uc'),)

    # Relationship with DataFile
    data_files = relationship("DataFile", backref="exam_details", lazy='dynamic')
    # Relationship with ModelDetails
    model_detail = relationship("ModelDetails",backref="exam_details", lazy='dynamic')



    @classmethod
    def add_exam(cls, db: Session, title: str, creator_name: str, description: str = None):
        """
        Creates a new exam and adds it to the database.

        Args:
            db (Session): SQLAlchemy database session.
            title (str): The title of the exam.
            creator_name (str): The name of the creator of the exam.
            description (str, optional): A description of the exam.

        Returns:
            ExamDetails: The newly created exam.
        """
        # Create a new exam instance
        new_exam = cls(
            title=title,
            creator_name=creator_name,
            description=description
        )

        try:
            # Add the new exam to the session and commit
            db.add(new_exam)
            db.commit()
            db.refresh(new_exam)
        except IntegrityError:
            # Handle the case where the unique constraint is violated
            db.rollback()
            raise ValueError(f"An exam with the title '{title}' already exists.")

        return new_exam

    @classmethod
    def get_exam_list(cls, db: Session):
        """
        Retrieves a list of exams as dictionaries with their ID and name.

        Args:
            db (Session): SQLAlchemy database session.

        Returns:
            list[dict]: List of dictionaries with exam ID and name.
        """
        return db.query(cls.id, cls.title).all()