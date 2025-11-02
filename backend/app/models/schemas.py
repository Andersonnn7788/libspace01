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
    HOGGED = "hogged"  # Seat occupied by objects without a person
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


class Seat(BaseModel):
    """Detected seat/chair with occupancy information"""
    seat_id: int
    bbox: BoundingBox
    is_occupied: bool
    is_hogged: bool = False  # True if occupied by objects without a person
    confidence: float
    person_detection: Optional[Detection] = None
    hogging_objects: Optional[List[Detection]] = None  # Objects occupying the seat
    person_match_score: float = 0.0  # Confidence score for person-chair match
    object_match_score: float = 0.0  # Confidence score for object-chair match


class SeatAvailability(BaseModel):
    """Current seat availability summary"""
    total_seats: int
    occupied_seats: int
    hogged_seats: int = 0  # Seats occupied by objects without a person
    available_seats: int
    occupancy_rate: float = Field(..., ge=0, le=100)
    last_updated: datetime
    detections: List[Detection] = []
    seats: List[Seat] = []  # List of detected seats with occupancy status

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
