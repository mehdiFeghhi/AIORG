from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.endpoints import router as api_router
from app.database import engine, Base  # Make sure this is the correct import
from app.logger import logger  # 👈 import the logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔧 Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created successfully.")
    except Exception as e:
        logger.exception("❌ Failed to create tables:")
    yield
    logger.info("🛑 Application shutdown initiated.")


# Create FastAPI instance with lifespan
app = FastAPI(
    title="Job Prediction API",
    description="An API to predict job satisfaction, improvement needs, and organizational profit.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Optional: Middleware to log every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"➡️ {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"⬅️ Response {response.status_code} for {request.method} {request.url}")
    return response


# Root endpoint
@app.get("/")
def read_root():
    logger.info("📥 Root endpoint hit.")
    return {"message": "Welcome to the Job Prediction API"}
