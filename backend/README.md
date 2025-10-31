# LibSpace Backend

FastAPI backend for library seat availability detection system using Raspberry Pi 4, Pi Camera Module, and YOLO object detection.

## Features

- 🎥 Real-time video processing with Pi Camera Module
- 🤖 YOLO-based person detection using Ultralytics
- 📊 RESTful API for seat availability and statistics
- 🔴 Live video streaming with MJPEG
- 📸 Snapshot capture with annotations
- ⚡ FastAPI for high-performance async operations
- 🎯 Configurable detection parameters

## Hardware Requirements

- Raspberry Pi 4 (4GB+ RAM recommended)
- Raspberry Pi Camera Module v2 or v3
- MicroSD card (32GB+ recommended)
- Stable power supply (5V 3A)

## System Setup

### 1. Update Raspberry Pi OS

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install System Dependencies

```bash
# Camera support
sudo apt install -y python3-picamera2 python3-libcamera

# OpenCV dependencies
sudo apt install -y python3-opencv libopencv-dev

# Build tools
sudo apt install -y python3-dev python3-pip python3-venv
sudo apt install -y libatlas-base-dev libhdf5-dev libjpeg-dev libpng-dev
```

### 3. Enable Camera

```bash
sudo raspi-config
# Navigate to: Interface Options -> Camera -> Enable
# Reboot when prompted
```

## Installation

### 1. Clone Repository

```bash
cd /home/anderson/libspace
cd backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** Installing PyTorch and YOLO on Raspberry Pi may take time. For faster installation on Pi, use:

```bash
# Install PyTorch for ARM
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install Ultralytics YOLO
pip install ultralytics
```

### 4. Download YOLO Model

```bash
mkdir -p models
cd models

# Download YOLOv8 nano (smallest, fastest)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# OR download YOLOv8 small (better accuracy)
# wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

### 5. Configure Environment

```bash
cp .env.example .env
nano .env
```

Update the following in `.env`:
- `TOTAL_SEATS`: Total number of seats in your library
- `CAMERA_WIDTH`, `CAMERA_HEIGHT`: Camera resolution
- `DETECTION_INTERVAL`: Time between detections (seconds)
- `CORS_ORIGINS`: Add your Next.js frontend URL
- `CAMERA_ROTATION`: Rotate camera if needed (0, 90, 180, 270)

### 6. Create Required Directories

```bash
mkdir -p data/detections
```

## Running the Backend

### Development Mode

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
```

**Note:** Use only 1 worker on Raspberry Pi due to camera resource constraints.

## API Endpoints

### Base URL
```
http://<raspberry-pi-ip>:8000
```

### Health Check
- `GET /health` - Check API health and service status

### Seats
- `GET /api/v1/seats/availability` - Get current seat availability
- `GET /api/v1/seats/status` - Get brief seat status
- `GET /api/v1/seats/detections` - Get current detections

### Statistics
- `GET /api/v1/statistics/current` - Get comprehensive statistics
- `GET /api/v1/statistics/summary` - Get statistics summary
- `GET /api/v1/statistics/zones` - Get zone-wise statistics

### Camera
- `GET /api/v1/camera/status` - Get camera status
- `GET /api/v1/camera/snapshot` - Get single frame snapshot
- `GET /api/v1/camera/stream` - Get MJPEG video stream
- `GET /api/v1/camera/info` - Get camera configuration

### API Documentation
- Swagger UI: `http://<raspberry-pi-ip>:8000/docs`
- ReDoc: `http://<raspberry-pi-ip>:8000/redoc`

## Testing the API

### Using curl

```bash
# Check health
curl http://localhost:8000/health

# Get seat availability
curl http://localhost:8000/api/v1/seats/availability

# Get snapshot
curl http://localhost:8000/api/v1/camera/snapshot -o snapshot.jpg

# View stream in browser
http://localhost:8000/api/v1/camera/stream
```

### Using Browser
Open `http://<raspberry-pi-ip>:8000/docs` for interactive API documentation.

## Auto-start on Boot (Systemd)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/libspace.service
```

Add:

```ini
[Unit]
Description=LibSpace Backend Service
After=network.target

[Service]
Type=simple
User=anderson
WorkingDirectory=/home/anderson/libspace/backend
Environment="PATH=/home/anderson/libspace/backend/venv/bin"
ExecStart=/home/anderson/libspace/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable libspace.service
sudo systemctl start libspace.service
sudo systemctl status libspace.service
```

## Configuration

### Adjusting Detection Parameters

Edit `app/core/config.py` or `.env`:

- `CONFIDENCE_THRESHOLD`: Detection confidence (0.0-1.0)
- `IOU_THRESHOLD`: Overlap threshold for NMS
- `DETECTION_INTERVAL`: Seconds between detections
- `TARGET_CLASS`: Object class to detect (person, chair, etc.)

### Seat Zones Configuration

Edit `app/core/config.py`:

```python
SEAT_ZONES: List[dict] = [
    {"name": "Zone A", "seats": 20},
    {"name": "Zone B", "seats": 15},
    {"name": "Zone C", "seats": 15},
]
```

## Performance Optimization

### For Raspberry Pi 4

1. **Use lighter YOLO model**: YOLOv8n (nano) is recommended
2. **Lower resolution**: 640x480 or 800x600 for faster processing
3. **Increase detection interval**: 3-5 seconds between detections
4. **Reduce FPS**: 10-15 FPS is sufficient

### Memory optimization

```bash
# Increase swap space if needed
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=2048
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## Troubleshooting

### Camera not working
```bash
# Test camera
rpicam-hello --list-cameras
vcgencmd get_camera

# Check if camera is detected
ls /dev/video*
```

### Import errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

### Slow detection
- Use YOLOv8n instead of larger models
- Increase `DETECTION_INTERVAL`
- Lower camera resolution
- Enable hardware acceleration if available

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   │   ├── camera.py
│   │   ├── seats.py
│   │   └── statistics.py
│   ├── core/         # Configuration
│   │   └── config.py
│   ├── models/       # Data models
│   │   └── schemas.py
│   ├── services/     # Business logic
│   │   ├── camera_service.py
│   │   └── detection_service.py
│   └── main.py       # FastAPI application
├── models/           # YOLO model files
├── data/            # Detection images
├── requirements.txt
├── .env.example
└── README.md
```

## Next Steps

1. **Connect to Next.js Frontend**: Update CORS origins in `.env`
2. **Calibrate Detection**: Adjust thresholds for your library setup
3. **Add Database**: Store historical data (optional)
4. **Implement Zones**: Add actual zone detection logic
5. **Add Notifications**: Alert when occupancy reaches threshold

## Support

For issues specific to:
- Raspberry Pi: Check official Pi forums
- YOLO: Ultralytics documentation
- FastAPI: FastAPI documentation

## License

MIT License
