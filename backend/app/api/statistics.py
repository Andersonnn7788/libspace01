"""
Statistics API endpoints
Provides aggregated statistics and historical data
"""
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import List
import logging

from app.models.schemas import Statistics, ZoneStatistics, SeatAvailability
from app.dependencies import get_camera_service
from app.services.camera_service import CameraService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/current", response_model=Statistics)
async def get_current_statistics(
    camera_service: CameraService = Depends(get_camera_service)
):
    """
    Get current statistics including zone information
    
    Returns comprehensive statistics about seat availability across all zones
    """
    try:
        availability = camera_service.get_current_availability()
        
        if availability is None:
            raise HTTPException(
                status_code=503,
                detail="No statistics available yet"
            )
        
        # Calculate zone statistics (simplified - you can enhance this based on actual zones)
        zones = []
        for zone_config in settings.SEAT_ZONES:
            zone_name = zone_config["name"]
            zone_seats = zone_config["seats"]
            
            # Proportional distribution (you can implement actual zone detection)
            zone_occupied = int(availability.occupied_seats * (zone_seats / settings.TOTAL_SEATS))
            zone_available = zone_seats - zone_occupied
            zone_rate = (zone_occupied / zone_seats * 100) if zone_seats > 0 else 0.0
            
            zones.append(ZoneStatistics(
                zone_name=zone_name,
                total_seats=zone_seats,
                occupied_seats=zone_occupied,
                available_seats=zone_available,
                occupancy_rate=zone_rate
            ))
        
        return Statistics(
            current_availability=availability,
            zones=zones,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def get_statistics_summary(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get brief statistics summary"""
    try:
        availability = camera_service.get_current_availability()
        
        if availability is None:
            return {
                "status": "initializing",
                "message": "No data available"
            }
        
        return {
            "total_seats": availability.total_seats,
            "available_seats": availability.available_seats,
            "occupied_seats": availability.occupied_seats,
            "occupancy_rate": availability.occupancy_rate,
            "detections_count": len(availability.detections),
            "last_updated": availability.last_updated.isoformat(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zones")
async def get_zone_statistics(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get statistics for all zones"""
    try:
        availability = camera_service.get_current_availability()
        
        if availability is None:
            raise HTTPException(
                status_code=503,
                detail="No statistics available"
            )
        
        zones = []
        for zone_config in settings.SEAT_ZONES:
            zone_name = zone_config["name"]
            zone_seats = zone_config["seats"]
            
            zone_occupied = int(availability.occupied_seats * (zone_seats / settings.TOTAL_SEATS))
            zone_available = zone_seats - zone_occupied
            zone_rate = (zone_occupied / zone_seats * 100) if zone_seats > 0 else 0.0
            
            zones.append({
                "zone_name": zone_name,
                "total_seats": zone_seats,
                "occupied_seats": zone_occupied,
                "available_seats": zone_available,
                "occupancy_rate": round(zone_rate, 2)
            })
        
        return {
            "zones": zones,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting zone statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
