from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings:
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_files")  # Default to 'uploaded_files'

settings = Settings()
