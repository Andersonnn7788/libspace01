"""
Seats API endpoints
Provides real-time seat availability information
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
import logging

from app.models.schemas import SeatAvailability, DetectionResponse
from app.dependencies import get_camera_service
from app.services.camera_service import CameraService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/availability", response_model=SeatAvailability)
async def get_seat_availability(
    camera_service: CameraService = Depends(get_camera_service)
):
    """
    Get current seat availability
    
    Returns real-time information about occupied and available seats
    """
    try:
        availability = camera_service.get_current_availability()
        
        if availability is None:
            raise HTTPException(
                status_code=503,
                detail="No availability data available yet. Please wait for first detection."
            )
        
        return availability
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting availability: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_seat_status(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get brief seat status"""
    try:
        availability = camera_service.get_current_availability()
        
        if availability is None:
            return {
                "status": "initializing",
                "message": "Waiting for first detection"
            }
        
        return {
            "status": "active",
            "total_seats": availability.total_seats,
            "available_seats": availability.available_seats,
            "occupied_seats": availability.occupied_seats,
            "occupancy_rate": availability.occupancy_rate,
            "last_updated": availability.last_updated.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detections")
async def get_detections(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get current detections"""
    try:
        detections = camera_service.get_current_detections()
        
        return {
            "count": len(detections),
            "detections": detections
        }
        
    except Exception as e:
        logger.error(f"Error getting detections: {e}")
        raise HTTPException(status_code=500, detail=str(e))
