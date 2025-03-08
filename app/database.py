# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://Tarh:@localhost:5432/Tarh")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
