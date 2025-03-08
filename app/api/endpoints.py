from fastapi import APIRouter
from app.api.exam_file import router as upload_file_router
from app.api.model import router as modle_router
from app.api.search_model import router as search_model_router
from app.api.jop_performanc import router as job_performanc_router
router = APIRouter()

# Include all routers
router.include_router(upload_file_router, prefix="/files", tags=["File Operations"])
router.include_router(modle_router, prefix="/model", tags=["Train & Predictions"])
router.include_router(search_model_router, prefix="/search_model",tags=["Model Details"])
router.include_router(job_performanc_router,prefix="/job_performanc",tags=["Job Performance"])




