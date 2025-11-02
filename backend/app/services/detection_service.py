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
from app.models.schemas import Detection, BoundingBox, Seat

logger = logging.getLogger(__name__)


class DetectionService:
    """YOLO-based detection service for seat occupancy"""
    
    def __init__(self):
        """Initialize YOLO model"""
        self.model_path = settings.MODEL_PATH
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        self.iou_threshold = settings.IOU_THRESHOLD
        self.target_classes = settings.TARGET_CLASSES
        self.detect_chairs = settings.DETECT_CHAIRS
        self.detect_persons = settings.DETECT_PERSONS
        self.detect_objects = settings.DETECT_OBJECTS
        self.object_classes = settings.OBJECT_CLASSES
        self.chair_confidence_threshold = settings.CHAIR_CONFIDENCE_THRESHOLD
        self.person_confidence_threshold = settings.PERSON_CONFIDENCE_THRESHOLD
        self.object_confidence_threshold = settings.OBJECT_CONFIDENCE_THRESHOLD
        self.occupancy_iou_threshold = settings.OCCUPANCY_IOU_THRESHOLD

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
    
    def detect(self, frame: np.ndarray) -> Tuple[List[Detection], List[Detection], List[Detection]]:
        """
        Perform detection on a frame, detecting chairs, persons, and objects

        Args:
            frame: Input image frame (numpy array)

        Returns:
            Tuple of (chair_detections, person_detections, object_detections)
        """
        try:
            # Run YOLO inference with lowest confidence threshold to catch all classes
            min_threshold = min(
                self.chair_confidence_threshold,
                self.person_confidence_threshold,
                self.object_confidence_threshold
            )
            results = self.model.predict(
                frame,
                conf=min_threshold,
                iou=self.iou_threshold,
                verbose=False
            )

            chair_detections = []
            person_detections = []
            object_detections = []

            # Process results
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get class name
                    class_id = int(box.cls[0])
                    class_name = self.model.names[class_id]
                    confidence = float(box.conf[0])

                    # Filter by target classes and apply class-specific confidence thresholds
                    if class_name.lower() == "chair" and self.detect_chairs:
                        if confidence >= self.chair_confidence_threshold:
                            # Get bounding box coordinates
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

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
                            chair_detections.append(detection)

                    elif class_name.lower() == "person" and self.detect_persons:
                        if confidence >= self.person_confidence_threshold:
                            # Get bounding box coordinates
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

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
                            person_detections.append(detection)

                    elif self.detect_objects and class_name.lower() in [obj.lower() for obj in self.object_classes]:
                        if confidence >= self.object_confidence_threshold:
                            # Get bounding box coordinates
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

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
                            object_detections.append(detection)

            logger.info(f"Detected {len(chair_detections)} chairs, {len(person_detections)} persons, and {len(object_detections)} objects")
            return chair_detections, person_detections, object_detections

        except Exception as e:
            logger.error(f"Detection error: {e}")
            return [], [], []

    def calculate_iou(self, bbox1: BoundingBox, bbox2: BoundingBox) -> float:
        """
        Calculate Intersection over Union (IoU) between two bounding boxes

        Args:
            bbox1: First bounding box
            bbox2: Second bounding box

        Returns:
            IoU value (0.0 to 1.0)
        """
        # Calculate intersection area
        x1_inter = max(bbox1.x1, bbox2.x1)
        y1_inter = max(bbox1.y1, bbox2.y1)
        x2_inter = min(bbox1.x2, bbox2.x2)
        y2_inter = min(bbox1.y2, bbox2.y2)

        # Check if there's an intersection
        if x2_inter <= x1_inter or y2_inter <= y1_inter:
            return 0.0

        intersection_area = (x2_inter - x1_inter) * (y2_inter - y1_inter)

        # Calculate union area
        bbox1_area = (bbox1.x2 - bbox1.x1) * (bbox1.y2 - bbox1.y1)
        bbox2_area = (bbox2.x2 - bbox2.x1) * (bbox2.y2 - bbox2.y1)
        union_area = bbox1_area + bbox2_area - intersection_area

        # Calculate IoU
        iou = intersection_area / union_area if union_area > 0 else 0.0
        return iou

    def match_persons_to_chairs(
        self,
        chair_detections: List[Detection],
        person_detections: List[Detection]
    ) -> List[Seat]:
        """
        Match person detections to chair detections based on spatial proximity
        Uses both IoU overlap and vertical/horizontal proximity for better seated detection

        Args:
            chair_detections: List of detected chairs
            person_detections: List of detected persons

        Returns:
            List of Seat objects with occupancy information
        """
        seats = []
        used_persons = set()  # Track which persons have been matched

        for idx, chair in enumerate(chair_detections):
            seat_id = idx + 1
            is_occupied = False
            matched_person = None
            max_score = 0.0

            # Find the person with best match score with this chair
            for person_idx, person in enumerate(person_detections):
                if person_idx in used_persons:
                    continue

                # Calculate IoU for overlap
                iou = self.calculate_iou(chair.bbox, person.bbox)

                # Calculate spatial proximity (if person is above/near the chair)
                # Check if person's bottom is near chair's top (seated position)
                chair_center_x = (chair.bbox.x1 + chair.bbox.x2) / 2
                chair_top_y = chair.bbox.y1
                chair_bottom_y = chair.bbox.y2
                chair_width = chair.bbox.x2 - chair.bbox.x1

                person_center_x = (person.bbox.x1 + person.bbox.x2) / 2
                person_bottom_y = person.bbox.y2
                person_top_y = person.bbox.y1

                # Check horizontal alignment (person's center should be near chair's center)
                horizontal_distance = abs(person_center_x - chair_center_x)
                horizontal_proximity = max(0, 1 - (horizontal_distance / chair_width))

                # Check vertical alignment (person should be above or slightly overlapping chair)
                # If person's bottom is between chair's top and bottom (or slightly below), it's likely seated
                vertical_tolerance = chair.bbox.y2 - chair.bbox.y1  # Chair height as tolerance
                vertical_ok = (person_bottom_y >= chair_top_y - vertical_tolerance * 0.3 and
                              person_top_y <= chair_bottom_y + vertical_tolerance * 0.3)

                # Calculate composite score: Use proximity if vertical alignment is good
                if vertical_ok:
                    # Person is vertically aligned - they might be sitting
                    # Even with low horizontal alignment, give benefit of the doubt
                    proximity_score = max(horizontal_proximity * 0.8, 0.15)  # Minimum score if vertical_ok
                    composite_score = iou * 0.2 + proximity_score
                else:
                    # Fall back to pure IoU
                    composite_score = iou

                # Use very low threshold - if we detect vertical alignment, that's good enough
                min_threshold = 0.10

                if composite_score >= min_threshold and composite_score > max_score:
                    max_score = composite_score
                    matched_person = person
                    is_occupied = True

            # If a person was matched, mark them as used
            if matched_person and matched_person in person_detections:
                person_idx = person_detections.index(matched_person)
                used_persons.add(person_idx)

            # Create seat object
            seat = Seat(
                seat_id=seat_id,
                bbox=chair.bbox,
                is_occupied=is_occupied,
                confidence=chair.confidence,
                person_detection=matched_person if is_occupied else None
            )
            seats.append(seat)

        logger.info(f"Matched {len([s for s in seats if s.is_occupied])} occupied seats out of {len(seats)} total seats")
        return seats

    def match_objects_to_chairs(
        self,
        seats: List[Seat],
        object_detections: List[Detection]
    ) -> List[Seat]:
        """
        Match object detections to chairs to identify hogged seats (objects without persons)
        A seat is marked as hogged if it has objects but no person

        Args:
            seats: List of Seat objects (already matched with persons)
            object_detections: List of detected objects

        Returns:
            Updated list of Seat objects with hogging information
        """
        for seat in seats:
            # Only check for hogging if seat is NOT occupied by a person
            if seat.is_occupied:
                continue

            matched_objects = []

            # Find all objects that overlap with this chair
            for obj in object_detections:
                # Calculate IoU for overlap
                iou = self.calculate_iou(seat.bbox, obj.bbox)

                # Calculate spatial proximity (similar to person matching)
                chair_center_x = (seat.bbox.x1 + seat.bbox.x2) / 2
                chair_center_y = (seat.bbox.y1 + seat.bbox.y2) / 2
                chair_width = seat.bbox.x2 - seat.bbox.x1
                chair_height = seat.bbox.y2 - seat.bbox.y1

                obj_center_x = (obj.bbox.x1 + obj.bbox.x2) / 2
                obj_center_y = (obj.bbox.y1 + obj.bbox.y2) / 2

                # Check if object center is near chair center
                horizontal_distance = abs(obj_center_x - chair_center_x)
                vertical_distance = abs(obj_center_y - chair_center_y)

                horizontal_proximity = max(0, 1 - (horizontal_distance / chair_width))
                vertical_proximity = max(0, 1 - (vertical_distance / chair_height))

                # Calculate composite score
                proximity_score = (horizontal_proximity + vertical_proximity) / 2
                composite_score = iou * 0.3 + proximity_score * 0.7

                # Lower threshold for objects since they might be smaller
                min_threshold = 0.15

                if composite_score >= min_threshold:
                    matched_objects.append(obj)

            # Mark seat as hogged if it has objects but no person
            if matched_objects:
                seat.is_hogged = True
                seat.hogging_objects = matched_objects
            else:
                seat.is_hogged = False
                seat.hogging_objects = None

        hogged_count = len([s for s in seats if s.is_hogged])
        logger.info(f"Detected {hogged_count} hogged seats (objects without persons)")
        return seats

    def annotate_frame(self, frame: np.ndarray, seats: List[Seat]) -> np.ndarray:
        """
        Draw bounding boxes and labels on frame showing chairs and occupancy

        Args:
            frame: Input image frame
            seats: List of Seat objects with occupancy information

        Returns:
            Annotated frame
        """
        annotated = frame.copy()

        for seat in seats:
            bbox = seat.bbox

            # Choose color based on occupancy status
            # Red for person-occupied, Orange for hogged, Green for available
            if seat.is_occupied:
                color = (0, 0, 255)  # Red for occupied
            elif seat.is_hogged:
                color = (0, 165, 255)  # Orange for hogged
            else:
                color = (0, 255, 0)  # Green for available

            # Draw chair bounding box
            cv2.rectangle(
                annotated,
                (bbox.x1, bbox.y1),
                (bbox.x2, bbox.y2),
                color,
                2
            )

            # Draw label for chair
            if seat.is_occupied:
                status = "Occupied"
            elif seat.is_hogged:
                status = "Hogged"
            else:
                status = "Empty"
            label = f"Chair {seat.seat_id}: {status}"
            (label_w, label_h), _ = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                2
            )

            # Background for label
            cv2.rectangle(
                annotated,
                (bbox.x1, bbox.y1 - label_h - 15),
                (bbox.x1 + label_w + 5, bbox.y1),
                color,
                -1
            )

            # Label text
            cv2.putText(
                annotated,
                label,
                (bbox.x1 + 2, bbox.y1 - 7),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            # If occupied, also draw the person bounding box
            if seat.is_occupied and seat.person_detection:
                person_bbox = seat.person_detection.bbox

                # Draw person bounding box in blue
                cv2.rectangle(
                    annotated,
                    (person_bbox.x1, person_bbox.y1),
                    (person_bbox.x2, person_bbox.y2),
                    (255, 0, 0),  # Blue for person
                    2
                )

                # Draw person label
                person_label = f"Person: {seat.person_detection.confidence:.2f}"
                (p_label_w, p_label_h), _ = cv2.getTextSize(
                    person_label,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    2
                )

                # Background for person label
                cv2.rectangle(
                    annotated,
                    (person_bbox.x1, person_bbox.y1 - p_label_h - 12),
                    (person_bbox.x1 + p_label_w + 5, person_bbox.y1),
                    (255, 0, 0),
                    -1
                )

                # Person label text
                cv2.putText(
                    annotated,
                    person_label,
                    (person_bbox.x1 + 2, person_bbox.y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

            # If hogged, draw the hogging objects bounding boxes
            if seat.is_hogged and seat.hogging_objects:
                for obj in seat.hogging_objects:
                    obj_bbox = obj.bbox

                    # Draw object bounding box in purple
                    cv2.rectangle(
                        annotated,
                        (obj_bbox.x1, obj_bbox.y1),
                        (obj_bbox.x2, obj_bbox.y2),
                        (255, 0, 255),  # Purple for objects
                        2
                    )

                    # Draw object label
                    obj_label = f"{obj.class_name}: {obj.confidence:.2f}"
                    (o_label_w, o_label_h), _ = cv2.getTextSize(
                        obj_label,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        2
                    )

                    # Background for object label
                    cv2.rectangle(
                        annotated,
                        (obj_bbox.x1, obj_bbox.y1 - o_label_h - 12),
                        (obj_bbox.x1 + o_label_w + 5, obj_bbox.y1),
                        (255, 0, 255),
                        -1
                    )

                    # Object label text
                    cv2.putText(
                        annotated,
                        obj_label,
                        (obj_bbox.x1 + 2, obj_bbox.y1 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2
                    )

        return annotated
    
    def calculate_occupancy(self, seats: List[Seat]) -> Tuple[int, int, int, float]:
        """
        Calculate seat occupancy based on detected seats, including hogged seats

        Args:
            seats: List of Seat objects with occupancy and hogging information

        Returns:
            Tuple of (occupied_seats, hogged_seats, available_seats, occupancy_rate)
        """
        total_seats = len(seats)  # Dynamically detected seats
        occupied_seats = len([s for s in seats if s.is_occupied])
        hogged_seats = len([s for s in seats if s.is_hogged])
        available_seats = total_seats - occupied_seats - hogged_seats

        # Occupancy rate includes both person-occupied and object-hogged seats
        occupancy_rate = ((occupied_seats + hogged_seats) / total_seats * 100) if total_seats > 0 else 0.0

        logger.info(f"Occupancy: {occupied_seats} occupied, {hogged_seats} hogged, {available_seats} available out of {total_seats} total ({occupancy_rate:.1f}%)")
        return occupied_seats, hogged_seats, available_seats, occupancy_rate
