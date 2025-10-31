# LibSpace Backend - Deployment Checklist

## 📋 Pre-Installation Checklist

### Hardware
- [ ] Raspberry Pi 4 (4GB or 8GB RAM recommended)
- [ ] Raspberry Pi Camera Module v2 or v3
- [ ] MicroSD card (32GB+ recommended)
- [ ] Stable 5V 3A power supply
- [ ] Network connection (Ethernet or WiFi)

### Software
- [ ] Raspberry Pi OS (64-bit recommended)
- [ ] SSH access configured
- [ ] Camera interface enabled

## 🔧 Installation Steps

### 1. System Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Enable camera
sudo raspi-config
# Interface Options → Camera → Enable → Reboot
```
- [ ] System updated
- [ ] Camera enabled
- [ ] System rebooted

### 2. Backend Installation
```bash
cd /home/anderson/libspace/backend
chmod +x install.sh
./install.sh
```
- [ ] Installation script executed
- [ ] Virtual environment created
- [ ] Python packages installed
- [ ] YOLO model downloaded

### 3. Configuration
```bash
nano .env
```
Update the following:
- [ ] `TOTAL_SEATS` - Set to your library's total seats
- [ ] `CAMERA_WIDTH` & `CAMERA_HEIGHT` - Adjust if needed
- [ ] `CAMERA_ROTATION` - Set if camera is rotated
- [ ] `DETECTION_INTERVAL` - Adjust for performance
- [ ] `CORS_ORIGINS` - Add your frontend URL

### 4. Testing
```bash
# Test setup
./test.sh

# Test camera
rpicam-hello

# Start backend
./start.sh
```
- [ ] Setup test passed
- [ ] Camera works
- [ ] Backend starts without errors

### 5. API Verification
Open browser: `http://<pi-ip>:8000/docs`
- [ ] API documentation loads
- [ ] Health check passes (`/health`)
- [ ] Seat availability endpoint works
- [ ] Camera stream displays
- [ ] Snapshot captures image

Test with curl:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/seats/availability
```
- [ ] Health endpoint returns JSON
- [ ] Availability endpoint returns data

## 🚀 Production Setup

### 1. Auto-start Service
```bash
sudo nano /etc/systemd/system/libspace.service
```
Add service configuration (see README.md)
```bash
sudo systemctl daemon-reload
sudo systemctl enable libspace.service
sudo systemctl start libspace.service
```
- [ ] Service file created
- [ ] Service enabled
- [ ] Service started
- [ ] Service status checked

### 2. Security Configuration
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
- [ ] Password changed
- [ ] System updated
- [ ] Firewall configured (optional)

### 3. Network Configuration
Get Pi IP address:
```bash
hostname -I
```
- [ ] Static IP configured (optional)
- [ ] Port forwarding configured (if needed)
- [ ] Firewall rules updated

## 🔍 Verification Checklist

### Camera
- [ ] Camera detected: `rpicam-hello --list-cameras`
- [ ] Camera captures images
- [ ] Camera rotation correct
- [ ] Resolution acceptable

### Detection
- [ ] YOLO model loads successfully
- [ ] Person detection works
- [ ] Confidence threshold appropriate
- [ ] Detection interval suitable
- [ ] Bounding boxes visible

### Performance
- [ ] Detection FPS acceptable (2-5 FPS)
- [ ] Camera FPS stable (15 FPS)
- [ ] API response time <100ms
- [ ] Memory usage <2GB
- [ ] CPU usage reasonable

### API Endpoints
- [ ] `/health` - Returns healthy status
- [ ] `/api/v1/seats/availability` - Returns seat data
- [ ] `/api/v1/seats/status` - Returns brief status
- [ ] `/api/v1/statistics/current` - Returns statistics
- [ ] `/api/v1/statistics/zones` - Returns zone data
- [ ] `/api/v1/camera/status` - Returns camera info
- [ ] `/api/v1/camera/snapshot` - Returns JPEG image
- [ ] `/api/v1/camera/stream` - Streams MJPEG video
- [ ] `/docs` - Shows API documentation

## 🎯 Frontend Integration

### CORS Configuration
- [ ] Frontend URL added to `CORS_ORIGINS`
- [ ] Multiple origins configured if needed
- [ ] CORS allows credentials

### API Testing from Frontend
- [ ] REST API calls work
- [ ] CORS errors resolved
- [ ] Image/stream loads correctly
- [ ] JSON responses parse correctly

## 📊 Monitoring

### System Health
```bash
# Check service status
sudo systemctl status libspace.service

# View logs
sudo journalctl -u libspace.service -f

# Monitor resources
htop
```
- [ ] Service running continuously
- [ ] No errors in logs
- [ ] CPU usage acceptable
- [ ] Memory not growing

### API Health
- [ ] Health endpoint returns healthy
- [ ] Detection running regularly
- [ ] Camera status shows running
- [ ] Timestamps updating

## 🐛 Troubleshooting Checklist

### If Camera Not Working
- [ ] Camera enabled in raspi-config
- [ ] Camera cable properly connected
- [ ] No other processes using camera
- [ ] picamera2 installed correctly
- [ ] Test with: `rpicam-hello`

### If Detection Slow
- [ ] Using YOLOv8n (nano) model
- [ ] Detection interval increased (3-5 sec)
- [ ] Camera resolution lowered (640x480)
- [ ] FPS reduced (10-12)
- [ ] Other apps closed

### If API Not Responding
- [ ] Service running: `systemctl status libspace`
- [ ] Port not blocked: `sudo lsof -i :8000`
- [ ] Firewall allows port 8000
- [ ] Network connectivity OK
- [ ] Check logs: `journalctl -u libspace -f`

### If Import Errors
- [ ] Virtual environment activated
- [ ] Requirements reinstalled
- [ ] System packages installed
- [ ] Python version compatible (3.9+)

## 📝 Documentation Review

Before going live, review:
- [ ] `README.md` - Setup instructions
- [ ] `QUICKSTART.md` - Quick reference
- [ ] `IMPLEMENTATION.md` - Implementation details
- [ ] `ARCHITECTURE.md` - System architecture
- [ ] API documentation at `/docs`

## ✅ Final Checklist

### Backend Ready
- [ ] Installation complete
- [ ] Configuration correct
- [ ] All services running
- [ ] API endpoints working
- [ ] Camera streaming
- [ ] Detection accurate

### Documentation Ready
- [ ] Setup guide available
- [ ] Configuration documented
- [ ] Troubleshooting guide ready
- [ ] API docs accessible

### Integration Ready
- [ ] CORS configured
- [ ] IP address documented
- [ ] API endpoints tested
- [ ] Frontend can connect

### Production Ready
- [ ] Auto-start configured
- [ ] Monitoring set up
- [ ] Backups planned
- [ ] Updates scheduled

## 🎉 Go Live!

Once all items are checked:
1. ✅ Backend is deployed
2. ✅ API is accessible
3. ✅ Detection is working
4. ✅ Ready for frontend integration

## 📞 Support Resources

If you encounter issues:
- Check logs: `sudo journalctl -u libspace.service -f`
- Review troubleshooting: `backend/README.md`
- Test API: `python test_api.py`
- Verify setup: `./test.sh`

## 🔄 Regular Maintenance

Weekly:
- [ ] Check service status
- [ ] Review logs for errors
- [ ] Monitor disk space
- [ ] Test API endpoints

Monthly:
- [ ] Update system packages
- [ ] Review detection accuracy
- [ ] Adjust thresholds if needed
- [ ] Check for YOLO updates

---

**System Status**: ⬜ Not Started | 🟨 In Progress | ✅ Complete | ❌ Issue

Mark items as you complete them to track deployment progress!
