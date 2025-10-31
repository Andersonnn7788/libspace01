#!/bin/bash
# LibSpace Backend Installation Script for Raspberry Pi 4

set -e

echo "=================================="
echo "LibSpace Backend Installation"
echo "=================================="
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
    echo "Warning: This script is designed for Raspberry Pi"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install system dependencies
echo ""
echo "Step 2: Installing system dependencies..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-picamera2 \
    python3-libcamera \
    python3-opencv \
    libopencv-dev \
    libopenblas-dev \
    libhdf5-dev \
    libjpeg-dev \
    libpng-dev \
    cmake \
    build-essential

# Create virtual environment
echo ""
echo "Step 3: Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo ""
echo "Step 4: Upgrading pip..."
pip install --upgrade pip wheel setuptools

# Install Python dependencies
echo ""
echo "Step 5: Installing Python packages (this may take 15-30 minutes)..."
echo "Installing core packages..."
pip install fastapi uvicorn pydantic pydantic-settings python-multipart python-dotenv aiofiles

echo "Installing NumPy and Pillow..."
pip install numpy pillow

echo "Installing OpenCV..."
pip install opencv-python opencv-contrib-python

echo "Installing PyTorch (ARM version)..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

echo "Installing Ultralytics YOLO..."
pip install ultralytics

echo "Installing picamera2..."
pip install picamera2

# Create directories
echo ""
echo "Step 6: Creating project directories..."
mkdir -p models
mkdir -p data/detections
mkdir -p config

# Copy environment file
echo ""
echo "Step 7: Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your settings."
fi

# Download YOLO model
echo ""
echo "Step 8: Downloading YOLO model..."
if [ ! -f models/yolov8n.pt ]; then
    cd models
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
    cd ..
    echo "YOLO model downloaded successfully"
else
    echo "YOLO model already exists"
fi

# Make start script executable
chmod +x start.sh

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Update TOTAL_SEATS and other settings"
echo "3. Run the backend: ./start.sh"
echo ""
echo "To test camera:"
echo "  rpicam-hello"
echo ""
echo "To start backend:"
echo "  ./start.sh"
echo ""
echo "API will be available at: http://$(hostname -I | awk '{print $1}'):8000"
echo "API docs: http://$(hostname -I | awk '{print $1}'):8000/docs"
echo ""
