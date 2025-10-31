"""
FastAPI Main Application
LibSpace - Library Seat Availability Detection System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import seats, statistics, camera
from app.core.config import settings
from app.services.camera_service import CameraService
from app.services.detection_service import DetectionService
from app.dependencies import set_camera_service, set_detection_service, get_camera_service, get_detection_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting LibSpace Backend...")
    try:
        detection_service = DetectionService()
        camera_service = CameraService(detection_service)

        # Set services for dependency injection
        set_detection_service(detection_service)
        set_camera_service(camera_service)

        camera_service.start()
        logger.info("Services started successfully")
    except Exception as e:
        logger.error(f"Failed to start services: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down LibSpace Backend...")
    camera_service = get_camera_service()
    if camera_service:
        camera_service.stop()
    logger.info("Services stopped")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Library Seat Availability Detection System using Computer Vision",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(seats.router, prefix="/api/v1/seats", tags=["seats"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["statistics"])
app.include_router(camera.router, prefix="/api/v1/camera", tags=["camera"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LibSpace API",
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    camera_service = get_camera_service()
    detection_service = get_detection_service()
    return {
        "status": "healthy",
        "camera": camera_service.is_running() if camera_service else False,
        "detection": detection_service is not None
    }
