"""
Data models for seat detection and statistics
"""
from pydantic import BaseModel, Field, computed_field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class SeatStatus(str, Enum):
    """Seat status enumeration"""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    UNKNOWN = "unknown"


class BoundingBox(BaseModel):
    """Bounding box coordinates"""
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float


class Detection(BaseModel):
    """Single detection result"""
    class_name: str
    confidence: float
    bbox: BoundingBox


class SeatInfo(BaseModel):
    """Individual seat information"""
    seat_id: int
    status: SeatStatus
    zone: str
    last_updated: datetime


class SeatAvailability(BaseModel):
    """Current seat availability summary"""
    total_seats: int
    occupied_seats: int
    available_seats: int
    occupancy_rate: float = Field(..., ge=0, le=100)
    last_updated: datetime
    detections: List[Detection] = []

    @computed_field
    @property
    def status(self) -> str:
        """Compute status based on occupancy rate"""
        if self.occupancy_rate >= 90:
            return "full"
        elif self.occupancy_rate >= 50:
            return "busy"
        else:
            return "available"


class ZoneStatistics(BaseModel):
    """Statistics for a specific zone"""
    zone_name: str
    total_seats: int
    occupied_seats: int
    available_seats: int
    occupancy_rate: float


class Statistics(BaseModel):
    """Overall statistics"""
    current_availability: SeatAvailability
    zones: List[ZoneStatistics]
    timestamp: datetime


class CameraStatus(BaseModel):
    """Camera status information"""
    is_running: bool
    width: int
    height: int
    fps: int
    last_frame_time: Optional[datetime] = None


class DetectionResponse(BaseModel):
    """API response for detection"""
    success: bool
    message: str
    data: Optional[SeatAvailability] = None
