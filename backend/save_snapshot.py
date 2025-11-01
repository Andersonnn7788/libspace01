#!/usr/bin/env python3
"""
Save a snapshot from the camera to diagnose what it's seeing
"""
import cv2
import numpy as np
from picamera2 import Picamera2
from datetime import datetime

def save_snapshot():
    """Capture and save a snapshot"""
    print("Capturing snapshot from camera...")

    try:
        camera = Picamera2()
        config = camera.create_preview_configuration(
            main={"size": (1280, 720), "format": "RGB888"}
        )
        camera.configure(config)
        camera.start()

        import time
        time.sleep(2)  # Let camera warm up and adjust exposure

        # Capture frame
        frame = camera.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Save snapshot
        filename = f"/home/anderson/libspace/backend/camera_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(filename, frame_bgr)

        # Calculate brightness
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)

        camera.stop()

        print(f"✓ Snapshot saved: {filename}")
        print(f"  - Image size: {frame_bgr.shape[1]}x{frame_bgr.shape[0]}")
        print(f"  - Average brightness: {avg_brightness:.1f}/255")

        if avg_brightness < 30:
            print("  ⚠ Image is very dark - add more lighting!")
        elif avg_brightness > 225:
            print("  ⚠ Image is overexposed - reduce lighting!")
        else:
            print("  ✓ Brightness looks okay")

        return filename

    except Exception as e:
        print(f"✗ Error: {e}")
        return None

if __name__ == "__main__":
    save_snapshot()
