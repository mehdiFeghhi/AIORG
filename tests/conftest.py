import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.files.exam_info import ExamDetails
from app.models.files.data_file import DataFile
from app.models.AI.ModelDetails import ModelDetails
from app.models.class_a import ClassA
from app.models.class_b import ClassB

from app.database import Base

# Test database URL (using in-memory SQLite database for testing)
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def db_session():
    """Fixture to create and drop the database for each test."""
    # Create tables in the correct order
    Base.metadata.create_all(engine, tables=[ ClassA.__table__, ClassB.__table__,ExamDetails.__table__, DataFile.__table__, ModelDetails.__table__])

    # Create a new session
    session = TestingSessionLocal()

    # Yield the session to the test
    yield session

    # Rollback and close the session after the test
    session.rollback()
    session.close()

    # Drop all tables after the test
    Base.metadata.drop_all(engine)
