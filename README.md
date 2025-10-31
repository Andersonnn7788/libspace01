# LibSpace - Library Seat Availability Detection System

Real-time library seat availability monitoring system using Computer Vision, Raspberry Pi 4, and modern web technologies.

## 🎯 Project Overview

LibSpace is a comprehensive solution for monitoring and displaying real-time seat availability in university libraries. The system uses a Raspberry Pi 4 with a camera module to detect occupied seats using YOLO object detection, and provides a modern web interface for students to check seat availability before visiting the library.

## 🏗️ Architecture

### Backend (Raspberry Pi 4)
- **Hardware**: Raspberry Pi 4, Pi Camera Module v2/v3
- **Framework**: FastAPI (Python)
- **Computer Vision**: OpenCV + YOLOv8 (Ultralytics)
- **Features**:
  - Real-time person detection
  - Live video streaming (MJPEG)
  - RESTful API for seat data
  - Automatic seat occupancy calculation
  - Zone-based statistics

### Frontend (Next.js Web App)
- **Framework**: Next.js 14+ (React)
- **Features**:
  - Real-time seat availability display
  - Live statistics and charts
  - Zone-wise occupancy view
  - Live camera feed
  - Responsive design for mobile/desktop

## 📁 Project Structure

```
libspace/
├── backend/              # FastAPI backend (Raspberry Pi)
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Configuration
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI app
│   ├── models/          # YOLO model files
│   ├── requirements.txt
│   ├── install.sh       # Installation script
│   └── README.md
│
└── frontend/            # Next.js web app (coming soon)
    ├── src/
    ├── public/
    └── package.json
```

## 🚀 Quick Start

### Backend Setup (Raspberry Pi 4)

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Run installation script**:
```bash
chmod +x install.sh
./install.sh
```

3. **Configure settings**:
```bash
nano .env
# Update TOTAL_SEATS, CAMERA settings, etc.
```

4. **Start the backend**:
```bash
./start.sh
```

5. **Access API**:
- API: http://your-pi-ip:8000
- Docs: http://your-pi-ip:8000/docs

See [backend/README.md](backend/README.md) for detailed instructions.

### Frontend Setup (Next.js)

Coming soon! The Next.js frontend will be added in the next phase.

## 🔌 API Endpoints

### Seat Availability
- `GET /api/v1/seats/availability` - Current seat availability
- `GET /api/v1/seats/status` - Brief status summary

### Statistics
- `GET /api/v1/statistics/current` - Comprehensive statistics
- `GET /api/v1/statistics/zones` - Zone-wise statistics

### Camera
- `GET /api/v1/camera/stream` - Live video stream
- `GET /api/v1/camera/snapshot` - Single frame capture
- `GET /api/v1/camera/status` - Camera status

### Health
- `GET /health` - System health check

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async web framework
- **OpenCV**: Computer vision and image processing
- **YOLOv8**: State-of-the-art object detection
- **Picamera2**: Raspberry Pi camera interface
- **PyTorch**: Deep learning framework
- **Uvicorn**: ASGI server

### Frontend (Planned)
- **Next.js 14**: React framework with SSR
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Chart.js**: Data visualization
- **SWR**: Data fetching and caching

## 📊 Features

### Current Features ✅
- Real-time person detection using YOLOv8
- Live MJPEG video streaming
- RESTful API for seat data
- Configurable detection parameters
- Zone-based seat organization
- Automatic occupancy calculation
- Snapshot capture with annotations
- Health monitoring and status checks

### Planned Features 🔜
- Next.js web dashboard
- Historical data tracking
- Database integration (PostgreSQL/SQLite)
- Push notifications
- Booking system integration
- Multi-camera support
- Advanced analytics
- Admin dashboard

## 🔧 Configuration

Key settings in `.env`:

```bash
# Seat Configuration
TOTAL_SEATS=50
DETECTION_INTERVAL=2.0

# Camera Settings
CAMERA_WIDTH=1280
CAMERA_HEIGHT=720
CAMERA_FPS=15
CAMERA_ROTATION=0

# YOLO Model
MODEL_PATH=models/yolov8n.pt
CONFIDENCE_THRESHOLD=0.5
TARGET_CLASS=person
```

## 📈 Performance

On Raspberry Pi 4 (4GB):
- **Detection Speed**: ~2-5 FPS with YOLOv8n
- **Camera FPS**: 15 FPS capture
- **Detection Interval**: 2 seconds (configurable)
- **API Response Time**: <100ms

## 🐛 Troubleshooting

### Camera Issues
```bash
# Test camera
rpicamera-hello --list-cameras

# Enable camera interface
sudo raspi-config
# Interface Options -> Camera -> Enable
```

### Performance Issues
- Use YOLOv8n (nano) model for faster inference
- Lower camera resolution (640x480)
- Increase detection interval (3-5 seconds)
- Reduce FPS to 10-12

### Import Errors
```bash
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

## 📝 Development Roadmap

- [x] Phase 1: Backend API with YOLO detection
- [ ] Phase 2: Next.js frontend dashboard
- [ ] Phase 3: Database integration
- [ ] Phase 4: Historical analytics
- [ ] Phase 5: Multi-camera support
- [ ] Phase 6: Mobile app (React Native)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT License

## 👥 Authors

- Anderson - Initial development

## 🙏 Acknowledgments

- Ultralytics for YOLOv8
- FastAPI team
- Raspberry Pi Foundation
- OpenCV community

## 📧 Support

For questions and support:
- Create an issue on GitHub
- Check documentation in `/backend/README.md`

---

**Note**: This is an active development project. The Next.js frontend will be added soon!
