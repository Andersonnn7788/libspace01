"""
FastAPI Dependencies
Provides dependency injection for services
"""
from app.services.camera_service import CameraService
from app.services.detection_service import DetectionService

# Global service instances
_camera_service: CameraService = None
_detection_service: DetectionService = None


def set_camera_service(service: CameraService):
    """Set the camera service instance"""
    global _camera_service
    _camera_service = service


def set_detection_service(service: DetectionService):
    """Set the detection service instance"""
    global _detection_service
    _detection_service = service


def get_camera_service() -> CameraService:
    """Get camera service instance for dependency injection"""
    return _camera_service


def get_detection_service() -> DetectionService:
    """Get detection service instance for dependency injection"""
    return _detection_service
