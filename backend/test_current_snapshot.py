#!/usr/bin/env python3
"""
Test YOLO detection on the latest snapshot
"""
import sys
import cv2
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.detection_service import DetectionService
from app.core.config import settings

def test_snapshot():
    """Test detection on saved snapshot"""
    print("Testing YOLO on latest snapshot...")

    # Load the image
    img_path = "/home/anderson/libspace/backend/camera_snapshot_20251101_191642.jpg"
    frame = cv2.imread(img_path)

    if frame is None:
        print(f"✗ Could not load image: {img_path}")
        return

    print(f"✓ Image loaded: {frame.shape}")

    # Initialize detection
    detection_service = DetectionService()

    # Test with very low confidence
    print("\nTesting with confidence threshold = 0.1")
    results = detection_service.model.predict(
        frame,
        conf=0.1,
        iou=settings.IOU_THRESHOLD,
        verbose=False
    )

    detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = detection_service.model.names[class_id]
            confidence = float(box.conf[0])
            detections.append((class_name, confidence))

    if detections:
        detections.sort(key=lambda x: x[1], reverse=True)
        print(f"\n✓ Found {len(detections)} objects:")
        for class_name, conf in detections:
            marker = " ⭐" if class_name.lower() in ["chair", "person"] else ""
            print(f"  - {class_name}: {conf:.3f}{marker}")

        # Check if chairs detected
        chairs = [c for c, conf in detections if c.lower() == "chair"]
        if chairs:
            print(f"\n✓ YES! Chairs detected: {len(chairs)}")
        else:
            print("\n✗ NO chairs detected")
            print("Objects that WERE detected:", [c for c, _ in detections[:5]])
    else:
        print("\n✗ NO objects detected at all")
        print("Possible reasons:")
        print("  1. Camera angle is too extreme (too close or unusual angle)")
        print("  2. Objects don't match YOLO's training data")
        print("  3. Image quality issues")

    # Now test with configured thresholds
    print(f"\n\nTesting with configured thresholds:")
    print(f"  - Chair: {settings.CHAIR_CONFIDENCE_THRESHOLD}")
    print(f"  - Person: {settings.PERSON_CONFIDENCE_THRESHOLD}")

    chair_dets, person_dets = detection_service.detect(frame)
    print(f"\nResults:")
    print(f"  - Chairs: {len(chair_dets)}")
    print(f"  - Persons: {len(person_dets)}")

if __name__ == "__main__":
    test_snapshot()
