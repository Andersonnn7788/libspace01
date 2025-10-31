#!/bin/bash
# Quick test script to verify backend setup

echo "LibSpace Backend Test Script"
echo "=============================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run install.sh first."
    exit 1
else
    echo "✅ Virtual environment found"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Copy from .env.example"
    exit 1
else
    echo "✅ .env file found"
fi

# Check if YOLO model exists
if [ ! -f "models/yolov8n.pt" ]; then
    echo "❌ YOLO model not found in models/"
    echo "   Download with: cd models && wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
    exit 1
else
    echo "✅ YOLO model found"
fi

# Test camera
echo ""
echo "Testing camera..."
if command -v rpicam-hello &> /dev/null; then
    rpicam-hello --list-cameras 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ Camera detected"
    else
        echo "⚠️  Camera not detected or not enabled"
        echo "   Enable camera: sudo raspi-config -> Interface Options -> Camera"
    fi
else
    echo "⚠️  rpicam-hello not found (normal if not on Raspberry Pi)"
fi

# Test Python imports
echo ""
echo "Testing Python dependencies..."
source venv/bin/activate

python3 -c "import fastapi; print('✅ FastAPI installed')" 2>/dev/null || echo "❌ FastAPI not installed"
python3 -c "import cv2; print('✅ OpenCV installed')" 2>/dev/null || echo "❌ OpenCV not installed"
python3 -c "import ultralytics; print('✅ Ultralytics installed')" 2>/dev/null || echo "❌ Ultralytics not installed"
python3 -c "import torch; print('✅ PyTorch installed')" 2>/dev/null || echo "❌ PyTorch not installed"

# Check if on Raspberry Pi
if grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    python3 -c "from picamera2 import Picamera2; print('✅ Picamera2 installed')" 2>/dev/null || echo "❌ Picamera2 not installed"
fi

echo ""
echo "=============================="
echo "Test complete!"
echo ""
echo "If all checks passed, start the backend with:"
echo "  ./start.sh"
echo ""
