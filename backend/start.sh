#!/bin/bash
# LibSpace Backend Startup Script

echo "Starting LibSpace Backend..."

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "Please configure .env before running the application"
    exit 1
fi

# Check if models directory exists
if [ ! -d models ]; then
    mkdir -p models
fi

# Check if YOLO model exists
if [ ! -f models/yolov8n.pt ]; then
    echo "YOLO model not found. Downloading YOLOv8n..."
    cd models
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
    cd ..
fi

# Create data directories
mkdir -p data/detections

# Start the server
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
