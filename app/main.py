from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

# Create FastAPI instance
app = FastAPI(
    title="Job Prediction API",
    description="An API to predict job satisfaction, improvement needs, and organizational profit.",
    version="1.0.0",
)

# CORS Middleware (Optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Prediction API"}

