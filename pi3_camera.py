#!/usr/bin/env python3
"""
Raspberry Pi Camera 3 Video Streaming Server
Streams video from Pi Camera 3 to a web browser via MJPEG
Works with libcamera on Ubuntu 24.04
"""

import io
import threading
import time
from flask import Flask, render_template, Response
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

# Initialize Flask app
app = Flask(__name__, template_folder='.')

# Global camera object
camera = None
camera_lock = threading.Lock()
stream_event = threading.Event()


def init_camera():
    """Initialize the Raspberry Pi Camera 3"""
    global camera
    try:
        camera = Picamera2()
        
        # Configure camera with reasonable defaults
        config = camera.create_video_configuration(
            main={"size": (1280, 720)},  # 720p resolution
            controls={"FrameRate": 30}
        )
        camera.configure(config)
        
        print("✓ Camera initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize camera: {e}")
        return False


class StreamingOutput(io.BytesIO):
    """Buffer for MJPEG streaming"""
    def __init__(self):
        super().__init__()
        self.frame_event = threading.Event()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):  # JPEG start marker
            self.truncate(0)
            self.seek(0)
            self.frame_event.set()
        return super().write(buf)


def generate_frames():
    """Generate MJPEG frames from camera"""
    global camera
    
    if not camera:
        return
    
    output = StreamingOutput()
    encoder = MJPEGEncoder(10000000)  # 10Mbps bitrate
    
    try:
        camera.start_recording(encoder, FileOutput(output))
        
        while True:
            output.frame_event.wait()
            output.frame_event.clear()
            
            current_frame = output.getvalue()
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n'
                b'Content-Length: ' + str(len(current_frame)).encode() + b'\r\n'
                b'\r\n' + current_frame + b'\r\n'
            )
    except Exception as e:
        print(f"Streaming error: {e}")
    finally:
        camera.stop_recording()


@app.route('/')
def index():
    """Main webpage"""
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/camera_info')
def camera_info():
    """Get camera information"""
    try:
        props = camera.camera_properties
        return {
            'model': props.get('Model', 'Unknown'),
            'resolution': '1280x720',
            'framerate': 30
        }
    except:
        return {'error': 'Camera not ready'}


def main():
    """Start the streaming server"""
    print("=" * 50)
    print("Pi Camera 3 Video Streaming Server")
    print("=" * 50)
    
    if not init_camera():
        print("Failed to initialize camera. Check connections and permissions.")
        return
    
    try:
        print("\n⚡ Starting Flask server...")
        print("📺 Open http://<your-pi-ip>:5000 in your browser")
        print("Press Ctrl+C to stop the server\n")
        
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down...")
    finally:
        if camera:
            camera.close()
            print("✓ Camera closed")


if __name__ == '__main__':
    main()
