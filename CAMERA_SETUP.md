# Pi Camera 3 Video Streaming Server

A Python-based video streaming application for Raspberry Pi 5 with Pi Camera 3 running Ubuntu 24.04.

## Features

- ✨ Real-time MJPEG video streaming to web browser
- 🎬 1280×720 @ 30fps video capture
- 🌐 Web interface with modern UI
- 📱 Responsive design (mobile-friendly)
- ⬇️ Frame capture/download functionality
- 🔄 Stream status monitoring
- 🔌 Easy to use - just run and open browser

## Prerequisites

- Raspberry Pi 5 with Ubuntu 24.04
- Pi Camera 3 connected and enabled
- Python 3.8+
- libcamera installed (included with Ubuntu 24.04 on Pi5)

## Installation

### 1. Install Dependencies

```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip -y

# Install libcamera-dev (if not already installed)
sudo apt install libcamera-dev -y

# Install required Python packages
pip3 install -r requirements.txt
```

### 2. Enable Camera Interface

Ensure your camera is connected to the Pi5 camera ribbon connector.

### 3. Run the Streaming Server

```bash
python3 pi3_camera.py
```

You should see output like:
```
==================================================
Pi Camera 3 Video Streaming Server
==================================================
✓ Camera initialized successfully

⚡ Starting Flask server...
📺 Open http://<your-pi-ip>:5000 in your browser
Press Ctrl+C to stop the server
```

### 4. Access the Stream

Open your web browser and navigate to:
```
http://<your-pi-ip>:5000
```

Replace `<your-pi-ip>` with your Raspberry Pi's IP address. You can find it using:
```bash
hostname -I
```

## Usage

Once the server is running:

1. **View Stream**: The video feed automatically displays in your browser
2. **Refresh Stream**: Click the "🔄 Refresh Stream" button to reconnect
3. **Capture Frame**: Click "⬇️ Download Frame" to save a JPEG screenshot
4. **Monitor Status**: The status bar shows connection status in real-time

## Troubleshooting

### Camera not detected
```bash
# Check camera access
libcamera-hello --list-cameras
```

### Permission errors
```bash
# Add user to video group
sudo usermod -aG video $USER
# Log out and back in, or reboot
```

### Port already in use
Edit `pi3_camera.py` and change the port number in `app.run()`:
```python
app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
```

### Slow streaming
- Reduce resolution in `pi3_camera.py` (change `(1280, 720)` to `(640, 480)`)
- Lower the bitrate in the `MJPEGEncoder(10000000)` call
- Check network connection quality

## Configuration

Edit `pi3_camera.py` to customize:

```python
# Change resolution
main={"size": (640, 480)}  # 480p
# or
main={"size": (1920, 1080)}  # 1080p

# Change framerate
controls={"FrameRate": 15}  # Lower for less bandwidth

# Change encoder bitrate
encoder = MJPEGEncoder(5000000)  # 5Mbps instead of 10Mbps
```

## Performance Notes

- **Network**: Stream works best on local network or low-latency connections
- **Resolution**: 720p @ 30fps requires ~2.5 Mbps bandwidth
- **CPU**: Uses ~30-40% CPU on RPi5 depending on resolution
- **Memory**: ~100-150MB RAM usage

## Security Notes

⚠️ **Important**: This server has no authentication. For public access:

1. Implement password protection (Flask-HTTPAuth)
2. Use HTTPS/SSL certificate
3. Configure firewall rules
4. Consider reverse proxy with authentication

## License

See LICENSE file for details.

## Support

For issues or questions:
1. Check camera connection
2. Verify Ubuntu camera permissions
3. Review system logs: `sudo journalctl -u <service>`
4. Test camera directly: `libcamera-hello`
