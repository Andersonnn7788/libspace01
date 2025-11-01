"""
Configuration settings for the LibSpace backend
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Project info
    PROJECT_NAME: str = "LibSpace API"
    VERSION: str = "1.0.0"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://192.168.1.100:3000",  # Update with your network IP
    ]
    
    # Camera settings
    CAMERA_WIDTH: int = 1280
    CAMERA_HEIGHT: int = 720
    CAMERA_FPS: int = 15
    CAMERA_ROTATION: int = 0  # 0, 90, 180, 270
    
    # YOLO model settings
    MODEL_PATH: str = "models/yolov8n.pt"  # or yolov5s.pt, yolov8s.pt
    CONFIDENCE_THRESHOLD: float = 0.5  # General confidence threshold for detections
    IOU_THRESHOLD: float = 0.45  # Non-max suppression threshold

    # Detection settings
    DETECTION_INTERVAL: float = 3.5  # seconds between detections (optimized for latency)
    TARGET_CLASSES: List[str] = ["chair", "person"]  # YOLO classes to detect
    DETECT_CHAIRS: bool = True  # Enable chair/seat detection
    DETECT_PERSONS: bool = True  # Enable person detection

    # Chair-specific detection settings
    CHAIR_CONFIDENCE_THRESHOLD: float = 0.4  # Confidence threshold for chair detection
    PERSON_CONFIDENCE_THRESHOLD: float = 0.5  # Confidence threshold for person detection
    OCCUPANCY_IOU_THRESHOLD: float = 0.3  # Minimum overlap to consider a chair occupied

    # Seat configuration (DEPRECATED - will be dynamically detected)
    TOTAL_SEATS: int = 50  # This is now ignored; seats are detected dynamically
    SEAT_ZONES: List[dict] = [
        {"name": "Zone A", "seats": 20},
        {"name": "Zone B", "seats": 15},
        {"name": "Zone C", "seats": 15},
    ]
    
    # Storage
    SAVE_DETECTIONS: bool = True
    DETECTION_SAVE_PATH: str = "data/detections"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
