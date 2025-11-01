"""
Camera Service for Raspberry Pi Camera Module
Uses picamera2 for efficient camera handling on Raspberry Pi
"""
import cv2
import numpy as np
from picamera2 import Picamera2
from threading import Thread, Lock
import time
import logging
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from app.core.config import settings
from app.models.schemas import Detection, SeatAvailability, Seat
from app.services.detection_service import DetectionService

logger = logging.getLogger(__name__)


class CameraService:
    """Camera service for capturing and processing frames"""
    
    def __init__(self, detection_service: DetectionService):
        """
        Initialize camera service
        
        Args:
            detection_service: Detection service instance
        """
        self.detection_service = detection_service
        self.camera: Optional[Picamera2] = None
        self.running = False
        self.thread: Optional[Thread] = None
        self.lock = Lock()
        
        # Frame storage
        self.current_frame: Optional[np.ndarray] = None
        self.annotated_frame: Optional[np.ndarray] = None
        self.last_frame_time: Optional[datetime] = None

        # Detection storage
        self.current_detections: List[Detection] = []
        self.current_seats: List[Seat] = []
        self.current_availability: Optional[SeatAvailability] = None
        
        # Camera settings
        self.width = settings.CAMERA_WIDTH
        self.height = settings.CAMERA_HEIGHT
        self.fps = settings.CAMERA_FPS
        self.detection_interval = settings.DETECTION_INTERVAL
        
        # Initialize camera
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize Raspberry Pi camera"""
        try:
            logger.info("Initializing Raspberry Pi Camera...")
            self.camera = Picamera2()

            # Configure camera
            config = self.camera.create_preview_configuration(
                main={"size": (self.width, self.height), "format": "RGB888"}
            )
            self.camera.configure(config)

            # Apply rotation if needed
            if settings.CAMERA_ROTATION:
                # Rotation is handled in post-processing
                pass

            logger.info(f"Camera configured: {self.width}x{self.height} @ {self.fps} FPS")

        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            logger.warning("Camera will use fallback mode")
            self.camera = None
    
    def start(self):
        """Start camera capture thread"""
        if self.running:
            logger.warning("Camera service already running")
            return
        
        if not self.camera:
            logger.error("Camera not initialized")
            return
        
        try:
            self.camera.start()
            self.running = True
            self.thread = Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            logger.info("Camera service started")
        except Exception as e:
            logger.error(f"Failed to start camera: {e}")
            raise
    
    def stop(self):
        """Stop camera capture"""
        if not self.running:
            return
        
        logger.info("Stopping camera service...")
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=5)
        
        if self.camera:
            try:
                self.camera.stop()
            except:
                pass
        
        logger.info("Camera service stopped")
    
    def _capture_loop(self):
        """Main capture loop running in separate thread"""
        last_detection_time = 0
        
        while self.running:
            try:
                # Capture frame
                frame = self.camera.capture_array()
                
                # Apply rotation if needed
                if settings.CAMERA_ROTATION == 90:
                    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                elif settings.CAMERA_ROTATION == 180:
                    frame = cv2.rotate(frame, cv2.ROTATE_180)
                elif settings.CAMERA_ROTATION == 270:
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                
                # Convert RGB to BGR for OpenCV
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                with self.lock:
                    self.current_frame = frame_bgr.copy()
                    self.last_frame_time = datetime.now()
                
                # Perform detection at specified interval
                current_time = time.time()
                if current_time - last_detection_time >= self.detection_interval:
                    self._process_detection(frame_bgr)
                    last_detection_time = current_time
                
                # Control frame rate
                time.sleep(1 / self.fps)
                
            except Exception as e:
                logger.error(f"Error in capture loop: {e}")
                time.sleep(1)
    
    def _process_detection(self, frame: np.ndarray):
        """Process detection on frame"""
        try:
            # Run detection for both chairs and persons
            chair_detections, person_detections = self.detection_service.detect(frame)

            # Match persons to chairs
            seats = self.detection_service.match_persons_to_chairs(chair_detections, person_detections)

            # Calculate occupancy based on detected seats
            occupied, available, rate = self.detection_service.calculate_occupancy(seats)

            # Create annotated frame with seats
            annotated = self.detection_service.annotate_frame(frame, seats)

            # Add statistics overlay
            total_seats = len(seats)
            stats_text = [
                f"Total Seats: {total_seats} (detected)",
                f"Occupied: {occupied}",
                f"Available: {available}",
                f"Occupancy: {rate:.1f}%"
            ]

            y_offset = 30
            for text in stats_text:
                cv2.putText(
                    annotated,
                    text,
                    (10, y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )
                y_offset += 30

            # Combine all detections for backward compatibility
            all_detections = chair_detections + person_detections

            # Update stored data
            with self.lock:
                self.current_detections = all_detections
                self.current_seats = seats
                self.annotated_frame = annotated
                self.current_availability = SeatAvailability(
                    total_seats=total_seats,
                    occupied_seats=occupied,
                    available_seats=available,
                    occupancy_rate=rate,
                    last_updated=datetime.now(),
                    detections=all_detections,
                    seats=seats
                )

            # Save detection image if enabled
            if settings.SAVE_DETECTIONS:
                self._save_detection(annotated)

        except Exception as e:
            logger.error(f"Detection processing error: {e}")
    
    def _save_detection(self, frame: np.ndarray):
        """Save detection frame to disk"""
        try:
            save_path = Path(settings.DETECTION_SAVE_PATH)
            save_path.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = save_path / f"detection_{timestamp}.jpg"
            
            cv2.imwrite(str(filename), frame)
            logger.debug(f"Saved detection to {filename}")
        except Exception as e:
            logger.error(f"Failed to save detection: {e}")
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get current raw frame"""
        with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def get_annotated_frame(self) -> Optional[np.ndarray]:
        """Get current annotated frame"""
        with self.lock:
            return self.annotated_frame.copy() if self.annotated_frame is not None else None
    
    def get_current_availability(self) -> Optional[SeatAvailability]:
        """Get current seat availability"""
        with self.lock:
            return self.current_availability
    
    def get_current_detections(self) -> List[Detection]:
        """Get current detections"""
        with self.lock:
            return self.current_detections.copy()

    def get_current_seats(self) -> List[Seat]:
        """Get current detected seats with occupancy info"""
        with self.lock:
            return self.current_seats.copy()

    def is_running(self) -> bool:
        """Check if camera is running"""
        return self.running
    
    def capture_snapshot(self) -> Optional[np.ndarray]:
        """Capture a single snapshot"""
        return self.get_annotated_frame()
