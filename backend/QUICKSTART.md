# LibSpace Backend - Quick Reference

## 🚀 Quick Commands

### Installation
```bash
cd backend
chmod +x install.sh
./install.sh
```

### Configuration
```bash
nano .env
# Update: TOTAL_SEATS, CAMERA_WIDTH, CAMERA_HEIGHT, CORS_ORIGINS
```

### Run Backend
```bash
./start.sh
```

### Test Setup
```bash
./test.sh
```

### Manual Start
```bash
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

Base URL: `http://<raspberry-pi-ip>:8000`

### Main Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |
| `/api/v1/seats/availability` | GET | Seat availability |
| `/api/v1/seats/status` | GET | Brief status |
| `/api/v1/statistics/current` | GET | Full statistics |
| `/api/v1/statistics/zones` | GET | Zone statistics |
| `/api/v1/camera/stream` | GET | Video stream |
| `/api/v1/camera/snapshot` | GET | Single snapshot |
| `/api/v1/camera/status` | GET | Camera status |

## 🧪 Testing

### Test Camera
```bash
rpicam-hello --list-cameras
rpicam-still -o test.jpg
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Seat availability
curl http://localhost:8000/api/v1/seats/availability

# Get snapshot
curl http://localhost:8000/api/v1/camera/snapshot -o snapshot.jpg
```

### View in Browser
```
http://<raspberry-pi-ip>:8000/docs
http://<raspberry-pi-ip>:8000/api/v1/camera/stream
```

## ⚙️ Configuration Options

### Camera Settings (.env)
```bash
CAMERA_WIDTH=1280          # 640, 800, 1280, 1920
CAMERA_HEIGHT=720          # 480, 600, 720, 1080
CAMERA_FPS=15              # 10, 15, 20, 30
CAMERA_ROTATION=0          # 0, 90, 180, 270
```

### Detection Settings (.env)
```bash
DETECTION_INTERVAL=2.0     # Seconds between detections
CONFIDENCE_THRESHOLD=0.5   # 0.0-1.0 (higher = stricter)
TARGET_CLASS=person        # person, chair, etc.
```

### Seat Configuration (.env)
```bash
TOTAL_SEATS=50            # Total seats in library
```

## 🔧 Troubleshooting

### Camera Not Working
```bash
# Enable camera
sudo raspi-config
# Interface Options -> Camera -> Enable

# Reboot
sudo reboot

# Test camera
rpicam-hello
```

### Slow Performance
```bash
# Use lighter model
MODEL_PATH=models/yolov8n.pt

# Lower resolution
CAMERA_WIDTH=640
CAMERA_HEIGHT=480

# Increase interval
DETECTION_INTERVAL=3.0
```

### Import Errors
```bash
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

### Port Already in Use
```bash
# Kill process on port 8000
sudo lsof -ti:8000 | xargs sudo kill -9

# Or use different port
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

## 📊 Performance Tips

### Raspberry Pi 4 Optimization
1. **Use YOLOv8n** (nano) model - fastest
2. **Lower resolution**: 640x480 or 800x600
3. **Increase interval**: 3-5 seconds
4. **Reduce FPS**: 10-15 is enough
5. **Close other apps**: Free up memory

### Expected Performance
- Detection: 2-5 FPS with YOLOv8n
- Camera: 15 FPS capture
- Memory: ~1-2GB RAM usage

## 🔄 Auto-start on Boot

```bash
sudo nano /etc/systemd/system/libspace.service
```

Add:
```ini
[Unit]
Description=LibSpace Backend
After=network.target

[Service]
Type=simple
User=anderson
WorkingDirectory=/home/anderson/libspace/backend
Environment="PATH=/home/anderson/libspace/backend/venv/bin"
ExecStart=/home/anderson/libspace/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable libspace.service
sudo systemctl start libspace.service
sudo systemctl status libspace.service
```

## 📝 Logs

### View Logs
```bash
# Real-time logs
tail -f /var/log/syslog | grep libspace

# Systemd logs
sudo journalctl -u libspace.service -f
```

## 🔐 Security

### Basic Security
```bash
# Change default password
passwd

# Update system
sudo apt update && sudo apt upgrade

# Configure firewall (optional)
sudo apt install ufw
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 8000/tcp  # API
sudo ufw enable
```

## 📦 YOLO Models

### Available Models
- **yolov8n.pt**: Nano (fastest, 3.2M params)
- **yolov8s.pt**: Small (11.2M params)
- **yolov8m.pt**: Medium (25.9M params)

### Download Models
```bash
cd models
# Nano (recommended for Pi)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# Small (better accuracy)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

## 🌐 Network Access

### Find Pi IP Address
```bash
hostname -I
```

### Access from Network
```
http://<pi-ip-address>:8000
```

### Update CORS for Frontend
```bash
nano .env
# Add: CORS_ORIGINS=http://<frontend-ip>:3000
```

## 📚 Useful Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- Ultralytics YOLOv8: https://docs.ultralytics.com
- Raspberry Pi Camera: https://www.raspberrypi.com/documentation/computers/camera_software.html
- OpenCV Python: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
