"""
Camera API endpoints
Provides camera control and frame streaming
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
import cv2
import logging
from typing import Optional
import io

from app.models.schemas import CameraStatus
from app.dependencies import get_camera_service
from app.services.camera_service import CameraService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/status", response_model=CameraStatus)
async def get_camera_status(
    camera_service: CameraService = Depends(get_camera_service)
):
    """Get camera status information"""
    try:
        return CameraStatus(
            is_running=camera_service.is_running(),
            width=settings.CAMERA_WIDTH,
            height=settings.CAMERA_HEIGHT,
            fps=settings.CAMERA_FPS,
            last_frame_time=camera_service.last_frame_time
        )
    except Exception as e:
        logger.error(f"Error getting camera status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/snapshot")
async def get_snapshot(
    annotated: bool = True,
    camera_service: CameraService = Depends(get_camera_service)
):
    """
    Get a single snapshot from the camera
    
    Args:
        annotated: If True, returns annotated frame with detections
    """
    try:
        if not camera_service.is_running():
            raise HTTPException(status_code=503, detail="Camera is not running")
        
        if annotated:
            frame = camera_service.get_annotated_frame()
        else:
            frame = camera_service.get_current_frame()
        
        if frame is None:
            raise HTTPException(status_code=503, detail="No frame available")
        
        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        
        return Response(
            content=buffer.tobytes(),
            media_type="image/jpeg",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting snapshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stream")
async def get_video_stream(
    annotated: bool = True,
    camera_service: CameraService = Depends(get_camera_service)
):
    """
    Get MJPEG video stream
    
    Args:
        annotated: If True, returns annotated stream with detections
    """
    def generate():
        """Generate MJPEG stream"""
        try:
            while camera_service.is_running():
                if annotated:
                    frame = camera_service.get_annotated_frame()
                else:
                    frame = camera_service.get_current_frame()
                
                if frame is not None:
                    # Encode frame
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                    
                    # Yield frame in MJPEG format
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + 
                           buffer.tobytes() + b'\r\n')
                
                # Small delay to control stream rate
                import time
                time.sleep(1 / settings.CAMERA_FPS)
                
        except Exception as e:
            logger.error(f"Stream error: {e}")
    
    if not camera_service.is_running():
        raise HTTPException(status_code=503, detail="Camera is not running")
    
    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.get("/info")
async def get_camera_info():
    """Get camera configuration information"""
    return {
        "width": settings.CAMERA_WIDTH,
        "height": settings.CAMERA_HEIGHT,
        "fps": settings.CAMERA_FPS,
        "rotation": settings.CAMERA_ROTATION,
        "detection_interval": settings.DETECTION_INTERVAL
    }
