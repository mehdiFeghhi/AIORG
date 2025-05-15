from fastapi import APIRouter
from app.api.exam_file import router as upload_file_router
from app.api.model import router as model_router
from app.api.search_model import router as search_model_router
from app.api.jop_performanc import router as job_performance_router
from app.logger import logger  # ✅ Import the logger

router = APIRouter()

# Include all routers with logging
logger.info("📁 Registering API routes...")

router.include_router(upload_file_router, prefix="/files", tags=["File Operations"])
logger.info("✅ /files routes registered.")

router.include_router(model_router, prefix="/model", tags=["Train & Predictions"])
logger.info("✅ /model routes registered.")

router.include_router(search_model_router, prefix="/search_model", tags=["Model Details"])
logger.info("✅ /search_model routes registered.")

router.include_router(job_performance_router, prefix="/job_performance", tags=["Job Performance"])
logger.info("✅ /job_performance routes registered.")
