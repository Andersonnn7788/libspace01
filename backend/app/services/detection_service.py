"""
YOLO Detection Service using OpenCV and Ultralytics YOLO
Handles object detection for seat occupancy detection
"""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Optional
import logging
from pathlib import Path

from app.core.config import settings
from app.models.schemas import Detection, BoundingBox

logger = logging.getLogger(__name__)


class DetectionService:
    """YOLO-based detection service for seat occupancy"""
    
    def __init__(self):
        """Initialize YOLO model"""
        self.model_path = settings.MODEL_PATH
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        self.iou_threshold = settings.IOU_THRESHOLD
        self.target_class = settings.TARGET_CLASS
        
        # Load YOLO model
        try:
            logger.info(f"Loading YOLO model from {self.model_path}")
            self.model = YOLO(self.model_path)
            logger.info(f"YOLO model loaded successfully")
            logger.info(f"Model classes: {self.model.names}")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            logger.info("Attempting to download default YOLOv8n model...")
            try:
                self.model = YOLO('yolov8n.pt')
                logger.info("Default YOLOv8n model loaded successfully")
            except Exception as e2:
                logger.error(f"Failed to load default model: {e2}")
                raise
    
    def detect(self, frame: np.ndarray) -> List[Detection]:
        """
        Perform detection on a frame
        
        Args:
            frame: Input image frame (numpy array)
            
        Returns:
            List of Detection objects
        """
        try:
            # Run YOLO inference
            results = self.model.predict(
                frame,
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                verbose=False
            )
            
            detections = []
            
            # Process results
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get class name
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    
                    # Filter by target class if specified
                    if self.target_class and class_name.lower() != self.target_class.lower():
                        continue
                    
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0])
                    
                    # Create detection object
                    detection = Detection(
                        class_name=class_name,
                        confidence=confidence,
                        bbox=BoundingBox(
                            x1=int(x1),
                            y1=int(y1),
                            x2=int(x2),
                            y2=int(y2),
                            confidence=confidence
                        )
                    )
                    detections.append(detection)
            
            logger.info(f"Detected {len(detections)} objects")
            return detections
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []
    
    def annotate_frame(self, frame: np.ndarray, detections: List[Detection]) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame
        
        Args:
            frame: Input image frame
            detections: List of detections
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        
        for det in detections:
            bbox = det.bbox
            
            # Draw bounding box
            cv2.rectangle(
                annotated,
                (bbox.x1, bbox.y1),
                (bbox.x2, bbox.y2),
                (0, 255, 0),
                2
            )
            
            # Draw label
            label = f"{det.class_name}: {det.confidence:.2f}"
            (label_w, label_h), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )
            
            # Background for label
            cv2.rectangle(
                annotated,
                (bbox.x1, bbox.y1 - label_h - 10),
                (bbox.x1 + label_w, bbox.y1),
                (0, 255, 0),
                -1
            )
            
            # Label text
            cv2.putText(
                annotated,
                label,
                (bbox.x1, bbox.y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )
        
        return annotated
    
    def calculate_occupancy(self, detections: List[Detection]) -> Tuple[int, int, float]:
        """
        Calculate seat occupancy based on detections
        
        Args:
            detections: List of detections
            
        Returns:
            Tuple of (occupied_seats, available_seats, occupancy_rate)
        """
        total_seats = settings.TOTAL_SEATS
        occupied_seats = len(detections)  # Number of detected persons
        available_seats = max(0, total_seats - occupied_seats)
        occupancy_rate = (occupied_seats / total_seats * 100) if total_seats > 0 else 0.0
        
        return occupied_seats, available_seats, occupancy_rate
