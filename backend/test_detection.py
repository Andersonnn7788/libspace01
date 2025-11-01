#!/usr/bin/env python3
"""
Test script to diagnose YOLO detection issues
"""
import sys
import cv2
import numpy as np
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.detection_service import DetectionService
from app.core.config import settings

def test_detection():
    """Test what YOLO detects from camera"""
    print("=" * 60)
    print("YOLO Detection Diagnostic Test")
    print("=" * 60)

    # Initialize detection service
    print("\n1. Initializing DetectionService...")
    detection_service = DetectionService()

    print(f"\n2. Configuration:")
    print(f"   - Chair confidence threshold: {settings.CHAIR_CONFIDENCE_THRESHOLD}")
    print(f"   - Person confidence threshold: {settings.PERSON_CONFIDENCE_THRESHOLD}")
    print(f"   - Occupancy IoU threshold: {settings.OCCUPANCY_IOU_THRESHOLD}")
    print(f"   - Detect chairs: {settings.DETECT_CHAIRS}")
    print(f"   - Detect persons: {settings.DETECT_PERSONS}")

    # Try to capture from camera
    print("\n3. Attempting to capture from camera...")
    try:
        from picamera2 import Picamera2
        camera = Picamera2()
        config = camera.create_preview_configuration(
            main={"size": (settings.CAMERA_WIDTH, settings.CAMERA_HEIGHT), "format": "RGB888"}
        )
        camera.configure(config)
        camera.start()
        print("   ✓ Camera initialized")

        # Capture a frame
        import time
        time.sleep(1)  # Let camera warm up
        frame = camera.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        print("   ✓ Frame captured")

        camera.stop()
    except Exception as e:
        print(f"   ✗ Camera error: {e}")
        print("   Using test image instead...")
        # Create a blank test image
        frame_bgr = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Run detection with VERY low confidence to see everything
    print("\n4. Running YOLO detection with LOW confidence (0.1) to see all objects...")
    results = detection_service.model.predict(
        frame_bgr,
        conf=0.1,  # Very low to see everything
        iou=settings.IOU_THRESHOLD,
        verbose=True
    )

    print("\n5. All detected objects (confidence >= 0.1):")
    all_detections = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = detection_service.model.names[class_id]
            confidence = float(box.conf[0])
            all_detections.append((class_name, confidence))

    if all_detections:
        # Sort by confidence
        all_detections.sort(key=lambda x: x[1], reverse=True)
        for class_name, conf in all_detections:
            marker = ""
            if class_name.lower() == "chair":
                marker = " <- CHAIR!"
            elif class_name.lower() == "person":
                marker = " <- PERSON!"
            print(f"   - {class_name}: {conf:.3f}{marker}")
    else:
        print("   ✗ NO objects detected at all!")
        print("   This means either:")
        print("     1. The camera view is blank/dark")
        print("     2. There are no objects YOLO recognizes in the frame")

    # Test with current thresholds
    print(f"\n6. Running detection with configured thresholds:")
    print(f"   - Chair threshold: {settings.CHAIR_CONFIDENCE_THRESHOLD}")
    print(f"   - Person threshold: {settings.PERSON_CONFIDENCE_THRESHOLD}")

    chair_detections, person_detections = detection_service.detect(frame_bgr)

    print(f"\n7. Results:")
    print(f"   - Chairs detected: {len(chair_detections)}")
    if chair_detections:
        for i, det in enumerate(chair_detections, 1):
            print(f"     {i}. Confidence: {det.confidence:.3f}, BBox: ({det.bbox.x1}, {det.bbox.y1}, {det.bbox.x2}, {det.bbox.y2})")

    print(f"   - Persons detected: {len(person_detections)}")
    if person_detections:
        for i, det in enumerate(person_detections, 1):
            print(f"     {i}. Confidence: {det.confidence:.3f}, BBox: ({det.bbox.x1}, {det.bbox.y1}, {det.bbox.x2}, {det.bbox.y2})")

    # Recommendations
    print("\n8. Recommendations:")
    if not all_detections:
        print("   ⚠ Camera might be pointing at blank wall or dark area")
        print("   → Point camera at an area with chairs and people")
    elif not any(name.lower() == "chair" for name, _ in all_detections):
        print("   ⚠ No chairs detected in frame at any confidence level")
        print("   → Make sure there are actual chairs visible to the camera")
        print("   → Try using 'couch' or 'bench' if those are detected instead")
    else:
        # Find max chair confidence
        chair_confs = [conf for name, conf in all_detections if name.lower() == "chair"]
        if chair_confs:
            max_chair_conf = max(chair_confs)
            print(f"   ℹ Chairs ARE being detected (max confidence: {max_chair_conf:.3f})")
            if max_chair_conf < settings.CHAIR_CONFIDENCE_THRESHOLD:
                print(f"   ⚠ BUT confidence is below threshold ({settings.CHAIR_CONFIDENCE_THRESHOLD})")
                print(f"   → Lower CHAIR_CONFIDENCE_THRESHOLD to {max_chair_conf - 0.05:.2f} in .env")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_detection()
