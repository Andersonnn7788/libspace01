"""
Camera Service for Raspberry Pi Camera Module
Uses picamera2 for efficient camera handling on Raspberry Pi
"""
import cv2
import numpy as np
from picamera2 import Picamera2
from threading import Thread, Lock, RLock
import time
import logging
from datetime import datetime
from typing import Optional, List, Tuple
from pathlib import Path
from collections import deque

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
        self.encode_thread: Optional[Thread] = None

        # Separate locks for different data to reduce contention
        self.frame_lock = Lock()  # For raw frame data
        self.encoded_lock = Lock()  # For pre-encoded JPEG data
        self.detection_lock = Lock()  # For detection data

        # Frame storage
        self.current_frame: Optional[np.ndarray] = None
        self.annotated_frame: Optional[np.ndarray] = None
        self.last_frame_time: Optional[datetime] = None

        # Pre-encoded frame cache (reduces encoding latency for streaming)
        self.encoded_raw_frame: Optional[bytes] = None
        self.encoded_annotated_frame: Optional[bytes] = None
        self.frame_needs_encoding = False

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

            # Start capture thread
            self.thread = Thread(target=self._capture_loop, daemon=True)
            self.thread.start()

            # Start encoding thread for pre-encoding frames
            self.encode_thread = Thread(target=self._encode_loop, daemon=True)
            self.encode_thread.start()

            logger.info("Camera service started with optimized streaming")
        except Exception as e:
            logger.error(f"Failed to start camera: {e}")
            raise
    
    def stop(self):
        """Stop camera capture"""
        if not self.running:
            return

        logger.info("Stopping camera service...")
        self.running = False

        # Wait for threads to stop
        if self.thread:
            self.thread.join(timeout=5)

        if self.encode_thread:
            self.encode_thread.join(timeout=5)

        if self.camera:
            try:
                self.camera.stop()
            except:
                pass

        logger.info("Camera service stopped")
    
    def _capture_loop(self):
        """Main capture loop running in separate thread"""
        last_detection_time = 0
        frame_interval = 1.0 / self.fps
        next_frame_time = time.time()

        while self.running:
            try:
                loop_start = time.time()

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

                # Update current frame (no copy to reduce overhead)
                with self.frame_lock:
                    self.current_frame = frame_bgr
                    self.last_frame_time = datetime.now()
                    self.frame_needs_encoding = True

                # Perform detection at specified interval
                current_time = time.time()
                if current_time - last_detection_time >= self.detection_interval:
                    self._process_detection(frame_bgr)
                    last_detection_time = current_time

                # Precise frame rate control (better than simple sleep)
                next_frame_time += frame_interval
                sleep_time = next_frame_time - time.time()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    # We're falling behind, reset timing
                    next_frame_time = time.time()

            except Exception as e:
                logger.error(f"Error in capture loop: {e}")
                time.sleep(1)

    def _encode_loop(self):
        """Background thread for pre-encoding frames to reduce streaming latency"""
        # Optimized JPEG encoding parameters for Raspberry Pi
        encode_params = [
            cv2.IMWRITE_JPEG_QUALITY, 60,
            cv2.IMWRITE_JPEG_OPTIMIZE, 1,  # Enable optimization
            cv2.IMWRITE_JPEG_PROGRESSIVE, 0  # Disable progressive for speed
        ]

        while self.running:
            try:
                # Check if we need to encode new frames
                needs_encoding = False
                with self.frame_lock:
                    needs_encoding = self.frame_needs_encoding

                if needs_encoding:
                    # Get frames to encode (quick lock)
                    with self.frame_lock:
                        raw_frame = self.current_frame
                        annotated_frame = self.annotated_frame
                        self.frame_needs_encoding = False

                    # Encode frames (outside lock to avoid blocking)
                    encoded_raw = None
                    encoded_annotated = None

                    if raw_frame is not None:
                        _, buffer = cv2.imencode('.jpg', raw_frame, encode_params)
                        encoded_raw = buffer.tobytes()

                    if annotated_frame is not None:
                        _, buffer = cv2.imencode('.jpg', annotated_frame, encode_params)
                        encoded_annotated = buffer.tobytes()

                    # Update encoded frames (quick lock)
                    with self.encoded_lock:
                        if encoded_raw is not None:
                            self.encoded_raw_frame = encoded_raw
                        if encoded_annotated is not None:
                            self.encoded_annotated_frame = encoded_annotated
                else:
                    # No new frames to encode, sleep briefly
                    time.sleep(0.01)

            except Exception as e:
                logger.error(f"Error in encode loop: {e}")
                time.sleep(0.1)

    def _process_detection(self, frame: np.ndarray):
        """Process detection on frame"""
        try:
            # Run detection for chairs, persons, and objects
            chair_detections, person_detections, object_detections = self.detection_service.detect(frame)

            # Match persons to chairs
            seats = self.detection_service.match_persons_to_chairs(chair_detections, person_detections)

            # Match objects to chairs to identify hogged seats
            seats = self.detection_service.match_objects_to_chairs(seats, object_detections)

            # Calculate occupancy based on detected seats (including hogged seats)
            occupied, hogged, available, rate = self.detection_service.calculate_occupancy(seats)

            # Create annotated frame with seats
            annotated = self.detection_service.annotate_frame(frame, seats)

            # Statistics are displayed in the web interface, no overlay needed on frame
            total_seats = len(seats)

            # Combine all detections for backward compatibility
            all_detections = chair_detections + person_detections + object_detections

            # Update detection data
            with self.detection_lock:
                self.current_detections = all_detections
                self.current_seats = seats
                self.current_availability = SeatAvailability(
                    total_seats=total_seats,
                    occupied_seats=occupied,
                    hogged_seats=hogged,
                    available_seats=available,
                    occupancy_rate=rate,
                    last_updated=datetime.now(),
                    detections=all_detections,
                    seats=seats
                )

            # Update annotated frame separately to trigger encoding
            with self.frame_lock:
                self.annotated_frame = annotated
                self.frame_needs_encoding = True

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
        """Get current raw frame (returns reference, not copy for performance)"""
        with self.frame_lock:
            return self.current_frame

    def get_annotated_frame(self) -> Optional[np.ndarray]:
        """Get current annotated frame (returns reference, not copy for performance)"""
        with self.frame_lock:
            return self.annotated_frame

    def get_encoded_frame(self, annotated: bool = True) -> Optional[bytes]:
        """
        Get pre-encoded JPEG frame (much faster than encoding on-demand)

        Args:
            annotated: If True, returns annotated frame, otherwise raw frame

        Returns:
            Pre-encoded JPEG bytes or None
        """
        with self.encoded_lock:
            if annotated:
                return self.encoded_annotated_frame
            else:
                return self.encoded_raw_frame

    def get_current_availability(self) -> Optional[SeatAvailability]:
        """Get current seat availability"""
        with self.detection_lock:
            return self.current_availability

    def get_current_detections(self) -> List[Detection]:
        """Get current detections"""
        with self.detection_lock:
            return self.current_detections.copy()

    def get_current_seats(self) -> List[Seat]:
        """Get current detected seats with occupancy info"""
        with self.detection_lock:
            return self.current_seats.copy()

    def is_running(self) -> bool:
        """Check if camera is running"""
        return self.running
    
    def capture_snapshot(self) -> Optional[np.ndarray]:
        """Capture a single snapshot"""
        return self.get_annotated_frame()
