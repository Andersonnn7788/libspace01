# LibSpace - Library Seat Availability Detection System

Real-time library seat availability monitoring system using Advanced Computer Vision, Raspberry Pi 4, and modern web technologies.

## 🎯 Project Overview

LibSpace is a comprehensive solution for monitoring and displaying real-time seat availability in university libraries. The system uses a Raspberry Pi 4 with a camera module to detect occupied seats using YOLOv8 object detection with intelligent chair-person matching and seat hogging detection, providing a modern Next.js web interface for students to check seat availability before visiting the library.

## 🏗️ Architecture

### Backend (Raspberry Pi 4)
- **Hardware**: Raspberry Pi 4, Pi Camera Module v1
- **Framework**: FastAPI (Python) with async support
- **Computer Vision**: OpenCV + YOLOv8 (Ultralytics)
- **Advanced Features**:
  - 🪑 **Dynamic chair detection** - Automatically detects all chairs/seats in view
  - 👤 **Intelligent person-to-chair matching** - Advanced IoU + spatial proximity algorithm
  - 🎒 **Seat hogging detection** - Detects bags, laptops, books occupying empty seats
  - 🎯 **Priority scoring system** - Distinguishes between person-occupied vs object-hogged seats
  - 📹 **Optimized streaming** - Pre-encoded frames with separate encoding thread
  - 🔄 **Multi-class detection** - Chairs, persons, and 8+ object types
  - 📊 **Real-time statistics** - Occupied, hogged, and available seat counts
  - 🎨 **Color-coded visualization** - Red (occupied), Orange (hogged), Green (available)
  - ⚡ **Performance optimized** - Frame rate control, threaded processing, lock optimization

### Frontend (Next.js Web App)
- **Framework**: Next.js 14+ (React) with TypeScript
- **Styling**: Tailwind CSS
- **Features**:
  - 📊 Real-time seat availability dashboard
  - 📈 Live statistics and occupancy charts
  - 🎥 Live camera feed with annotations
  - 🗺️ Zone-wise occupancy breakdown
  - 🔴 System status monitoring
  - 📱 Responsive design for mobile/desktop
  - 🔄 Auto-refreshing data with SWR
  - 🎨 Modern, clean UI design

## 📁 Project Structure

```
libspace/
├── backend/              # FastAPI backend (Raspberry Pi)
│   ├── app/
│   │   ├── api/         # API endpoints (seats, statistics, camera)
│   │   ├── core/        # Configuration and settings
│   │   ├── models/      # Data models (Seat, Detection, etc.)
│   │   ├── services/    # Business logic
│   │   │   ├── detection_service.py  # YOLO + matching algorithms
│   │   │   └── camera_service.py     # Camera + threading
│   │   ├── dependencies.py           # FastAPI dependencies
│   │   └── main.py                   # FastAPI app
│   ├── models/          # YOLO model files (yolov8n.pt)
│   ├── data/            # Detection snapshots
│   ├── requirements.txt
│   ├── install.sh       # Automated installation
│   ├── start.sh         # Quick start script
│   ├── test_detection.py      # Detection diagnostic tool
│   ├── save_snapshot.py       # Camera snapshot utility
│   └── README.md              # Backend documentation
│
└── frontend/            # Next.js web app
    ├── src/
    │   ├── app/         # Next.js 14 app router
    │   ├── components/  # React components
    │   │   ├── LiveCameraFeed.tsx
    │   │   ├── OccupancyChart.tsx
    │   │   ├── SeatAvailabilityCard.tsx
    │   │   ├── StatisticsCard.tsx
    │   │   ├── SystemStatus.tsx
    │   │   └── ZoneList.tsx
    │   ├── lib/         # API client and utilities
    │   └── types/       # TypeScript types
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

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Configure environment**:
```bash
cp .env.example .env
nano .env
# Update NEXT_PUBLIC_API_URL with your Raspberry Pi IP
```

4. **Run development server**:
```bash
npm run dev
```

5. **Access frontend**:
- Development: http://localhost:3000
- Production build: `npm run build && npm start`

See [frontend/README.md](frontend/README.md) for detailed instructions.

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
- **YOLOv8/YOLOv11**: State-of-the-art object detection
- **Picamera2**: Raspberry Pi camera interface
- **PyTorch**: Deep learning framework
- **Uvicorn**: ASGI server

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization
- **SWR**: Data fetching and caching
- **Axios**: HTTP client

## 📊 Features

### Backend Features ✅
- ✅ **Dynamic chair detection** - Automatically counts all chairs in camera view
- ✅ **Person-to-chair matching** - Advanced IoU + spatial proximity algorithm
- ✅ **Seat hogging detection** - Identifies bags, laptops, books on empty seats
- ✅ **Priority scoring** - Differentiates person-occupied vs object-hogged seats
- ✅ **Multi-class detection** - Chairs, persons, backpacks, laptops, books, etc.
- ✅ **Optimized streaming** - Separate encoding thread for low-latency MJPEG
- ✅ **Performance tuned** - Lock optimization, frame rate control
- ✅ **Diagnostic tools** - Test scripts for camera, detection, and API
- ✅ **RESTful API** - Complete API with auto-documentation
- ✅ **Health monitoring** - Real-time system status

### Frontend Features ✅
- ✅ **Real-time dashboard** - Live seat availability display
- ✅ **Live camera feed** - MJPEG stream with annotations
- ✅ **Occupancy charts** - Visual statistics and trends
- ✅ **Zone breakdown** - Per-zone seat availability
- ✅ **System status** - Camera and detection service monitoring
- ✅ **Auto-refresh** - SWR with configurable intervals
- ✅ **Responsive design** - Mobile and desktop optimized
- ✅ **Color-coded UI** - Green (available), Orange (hogged), Red (occupied)

### Future Enhancements 🔜
- Historical data tracking with database
- Analytics dashboard with trends
- Push notifications for availability changes
- Booking system integration
- Multi-camera support
- Admin dashboard for configuration
- Mobile app (React Native)

## 🔧 Configuration

Key settings in `.env`:

```bash
# Seat Configuration
TOTAL_SEATS=50  # Now dynamically detected, but kept for compatibility
DETECTION_INTERVAL=3.5

# Camera Settings
CAMERA_WIDTH=1280
CAMERA_HEIGHT=720
CAMERA_FPS=15
CAMERA_ROTATION=0

# YOLO Model
MODEL_PATH=models/yolov8n.pt
CONFIDENCE_THRESHOLD=0.5

# Detection Classes
TARGET_CLASSES=["chair", "person"]
DETECT_CHAIRS=true
DETECT_PERSONS=true
DETECT_OBJECTS=true

# Class-Specific Thresholds
CHAIR_CONFIDENCE_THRESHOLD=0.4
PERSON_CONFIDENCE_THRESHOLD=0.5
OBJECT_CONFIDENCE_THRESHOLD=0.3

# Occupancy Detection
OCCUPANCY_IOU_THRESHOLD=0.3

# Object Classes for Hogging Detection
OBJECT_CLASSES=["backpack", "laptop", "book", "handbag", "suitcase", "bottle", "cup", "cell phone"]
```

## 📈 Performance

On Raspberry Pi 4 (4GB):
- **Detection Speed**: ~2-5 FPS with YOLOv8n
- **Camera FPS**: 15 FPS capture
- **Detection Interval**: 3.5 seconds (configurable)
- **API Response Time**: <100ms
- **Streaming**: Optimized MJPEG with pre-encoded frames
- **Multi-threading**: Separate threads for capture, detection, and encoding

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

MIT License

## 🙏 Acknowledgments

- Ultralytics for YOLOv8
- FastAPI team
- Raspberry Pi Foundation
- OpenCV community

## 📧 Support

For questions and support:
- Create an issue on GitHub
- Check documentation in `/backend/README.md`
- Review diagnostic tools: `test_detection.py`, `save_snapshot.py`

---

**Status**: ✅ Production Ready - Both backend and frontend are fully operational!
