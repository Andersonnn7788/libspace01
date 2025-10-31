# LibSpace System Architecture & Data Flow

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LibSpace System Architecture                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│                  │         │                  │         │                  │
│  Raspberry Pi 4  │────────▶│  FastAPI Backend │────────▶│  Next.js Frontend│
│  + Pi Camera     │         │                  │         │                  │
│                  │         │                  │         │                  │
└──────────────────┘         └──────────────────┘         └──────────────────┘
        │                             │                             │
        │                             │                             │
        ▼                             ▼                             ▼
  Camera Feed                   REST API                      Web Dashboard
  Detection                    JSON Data                     Live Statistics
  Processing                   Streaming                     Video Display
```

## 📸 Camera Pipeline

```
Camera Module (picamera2)
         │
         ▼
Frame Capture (RGB, 1280x720 @ 15 FPS)
         │
         ▼
Rotation (if configured)
         │
         ▼
RGB → BGR Conversion
         │
         ▼
Store Raw Frame ───────────────┐
         │                     │
         ▼                     ▼
Detection Pipeline        Direct Streaming
```

## 🤖 Detection Pipeline

```
Raw Frame
    │
    ▼
┌────────────────────────────────┐
│    YOLOv8 Object Detection     │
│  (Every DETECTION_INTERVAL)    │
└────────────────────────────────┘
    │
    ▼
Filter by Confidence Threshold
    │
    ▼
Filter by Target Class (person)
    │
    ▼
Create Detection Objects
    │
    ├─── Bounding Boxes
    ├─── Confidence Scores
    └─── Class Labels
    │
    ▼
Calculate Occupancy
    │
    ├─── Occupied Seats = Detection Count
    ├─── Available Seats = Total - Occupied
    └─── Occupancy Rate = (Occupied/Total) × 100
    │
    ▼
Annotate Frame
    │
    ├─── Draw Bounding Boxes
    ├─── Add Labels
    └─── Overlay Statistics
    │
    ▼
Store Annotated Frame
    │
    ▼
Update API Data
```

## 🌐 API Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                    API Request Flow                      │
└─────────────────────────────────────────────────────────┘

Client Request
    │
    ▼
FastAPI Router
    │
    ├─── /health ──────────────────────▶ System Status
    │
    ├─── /api/v1/seats/
    │    ├─── availability ────────────▶ Full Availability Data
    │    ├─── status ──────────────────▶ Brief Status
    │    └─── detections ─────────────▶ Detection List
    │
    ├─── /api/v1/statistics/
    │    ├─── current ────────────────▶ Full Statistics
    │    ├─── summary ────────────────▶ Brief Summary
    │    └─── zones ──────────────────▶ Zone Breakdown
    │
    └─── /api/v1/camera/
         ├─── status ─────────────────▶ Camera Info
         ├─── snapshot ───────────────▶ JPEG Image
         ├─── stream ────────────────▶ MJPEG Stream
         └─── info ──────────────────▶ Config Info
    │
    ▼
JSON Response / Image Stream
```

## 🔄 Service Interaction

```
┌─────────────────────────────────────────────────────────┐
│                   Service Architecture                   │
└─────────────────────────────────────────────────────────┘

main.py (FastAPI App)
    │
    ├─── Startup
    │    ├─── Initialize DetectionService
    │    │    └─── Load YOLO Model
    │    │
    │    └─── Initialize CameraService
    │         ├─── Setup Pi Camera
    │         └─── Start Capture Thread
    │
    ├─── API Routers
    │    ├─── seats.py
    │    ├─── statistics.py
    │    └─── camera.py
    │
    └─── Shutdown
         └─── Stop Camera Service

CameraService (Thread)
    │
    ├─── Continuous Loop
    │    ├─── Capture Frame
    │    ├─── Store Raw Frame
    │    │
    │    └─── Every DETECTION_INTERVAL:
    │         ├─── Call DetectionService
    │         ├─── Calculate Occupancy
    │         ├─── Annotate Frame
    │         └─── Update Availability Data
    │
    └─── Provide Access Methods
         ├─── get_current_frame()
         ├─── get_annotated_frame()
         └─── get_current_availability()

DetectionService
    │
    ├─── detect(frame)
    │    ├─── Run YOLO Inference
    │    ├─── Filter Results
    │    └─── Return Detections
    │
    ├─── annotate_frame(frame, detections)
    │    └─── Draw Boxes & Labels
    │
    └─── calculate_occupancy(detections)
         └─── Return Stats
```

## 📊 Data Models

```
SeatAvailability
├── total_seats: int
├── occupied_seats: int
├── available_seats: int
├── occupancy_rate: float
├── last_updated: datetime
└── detections: List[Detection]
     └── Detection
          ├── class_name: str
          ├── confidence: float
          └── bbox: BoundingBox
               ├── x1, y1, x2, y2: int
               └── confidence: float

Statistics
├── current_availability: SeatAvailability
├── zones: List[ZoneStatistics]
│    └── ZoneStatistics
│         ├── zone_name: str
│         ├── total_seats: int
│         ├── occupied_seats: int
│         ├── available_seats: int
│         └── occupancy_rate: float
└── timestamp: datetime

CameraStatus
├── is_running: bool
├── width: int
├── height: int
├── fps: int
└── last_frame_time: datetime
```

## 🎬 Request/Response Examples

### 1. Get Seat Availability

```
GET /api/v1/seats/availability

Response:
{
  "total_seats": 50,
  "occupied_seats": 23,
  "available_seats": 27,
  "occupancy_rate": 46.0,
  "last_updated": "2025-10-27T10:30:45",
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.87,
      "bbox": {
        "x1": 120, "y1": 150,
        "x2": 280, "y2": 450,
        "confidence": 0.87
      }
    }
  ]
}
```

### 2. Get Statistics

```
GET /api/v1/statistics/current

Response:
{
  "current_availability": { ... },
  "zones": [
    {
      "zone_name": "Zone A",
      "total_seats": 20,
      "occupied_seats": 9,
      "available_seats": 11,
      "occupancy_rate": 45.0
    }
  ],
  "timestamp": "2025-10-27T10:30:45"
}
```

### 3. Camera Stream

```
GET /api/v1/camera/stream

Response: (MJPEG Stream)
Content-Type: multipart/x-mixed-replace; boundary=frame

--frame
Content-Type: image/jpeg

[JPEG DATA]
--frame
Content-Type: image/jpeg

[JPEG DATA]
...
```

## 🔧 Configuration Flow

```
.env File
    │
    ▼
Settings Class (pydantic)
    │
    ├─── PROJECT_NAME
    ├─── CORS_ORIGINS
    │
    ├─── Camera Settings
    │    ├─── CAMERA_WIDTH
    │    ├─── CAMERA_HEIGHT
    │    ├─── CAMERA_FPS
    │    └─── CAMERA_ROTATION
    │
    ├─── Detection Settings
    │    ├─── MODEL_PATH
    │    ├─── CONFIDENCE_THRESHOLD
    │    ├─── DETECTION_INTERVAL
    │    └─── TARGET_CLASS
    │
    └─── Seat Configuration
         ├─── TOTAL_SEATS
         └─── SEAT_ZONES
    │
    ▼
Used by Services
    ├─── CameraService
    ├─── DetectionService
    └─── API Routers
```

## 🚀 Startup Sequence

```
1. Load Configuration
   └─── Read .env file
   └─── Initialize Settings

2. Initialize Detection Service
   └─── Load YOLO model
   └─── Verify model loaded

3. Initialize Camera Service
   └─── Setup picamera2
   └─── Configure resolution/FPS
   └─── Pass detection service reference

4. Start Camera Service
   └─── Start camera
   └─── Launch capture thread
   └─── Begin continuous capture

5. Register API Routers
   └─── Mount endpoints
   └─── Configure CORS

6. Start FastAPI Server
   └─── Uvicorn server
   └─── Listen on 0.0.0.0:8000
   └─── Ready for requests
```

## 🎯 Performance Considerations

```
Raspberry Pi 4 Optimization
    │
    ├─── Camera Capture: 15 FPS
    │    └─── Threaded, non-blocking
    │
    ├─── YOLO Detection: Every 2 seconds
    │    ├─── YOLOv8n (lightest model)
    │    └─── ~2-5 FPS inference speed
    │
    ├─── API Response: <100ms
    │    └─── Async handlers
    │
    └─── Memory Usage: ~1-2GB RAM
         ├─── YOLO model: ~6MB
         ├─── PyTorch overhead: ~500MB
         └─── Frame buffers: ~100MB
```

## 🔐 Security & CORS

```
CORS Middleware
    │
    ├─── Allowed Origins
    │    ├─── http://localhost:3000
    │    ├─── http://localhost:3001
    │    └─── http://<frontend-ip>:3000
    │
    ├─── Allowed Methods: ALL
    ├─── Allowed Headers: ALL
    └─── Allow Credentials: True
```

## 📡 Frontend Integration Points

```
Next.js Frontend
    │
    ├─── REST API Calls
    │    ├─── GET /api/v1/seats/availability
    │    ├─── GET /api/v1/statistics/current
    │    └─── GET /api/v1/statistics/zones
    │
    ├─── Image Display
    │    └─── <img src="/api/v1/camera/snapshot" />
    │
    ├─── Video Stream
    │    └─── <img src="/api/v1/camera/stream" />
    │
    └─── WebSocket (Future)
         └─── Real-time updates
```

## 🎨 System States

```
System States
    │
    ├─── Initializing
    │    ├─── Loading model
    │    ├─── Starting camera
    │    └─── No data available
    │
    ├─── Running
    │    ├─── Camera active
    │    ├─── Detection running
    │    └─── API serving data
    │
    ├─── Error
    │    ├─── Camera failure
    │    ├─── Model not loaded
    │    └─── Service unavailable
    │
    └─── Shutdown
         ├─── Stop camera
         ├─── Release resources
         └─── Clean exit
```

This architecture provides:
✅ Real-time processing
✅ Efficient resource usage
✅ Scalable design
✅ Easy maintenance
✅ Production ready
