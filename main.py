import cv2
import platform
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

def open_camera():
    os_name = platform.system()
    if os_name == "Windows":
        device = 0
        cap = cv2.VideoCapture(device, cv2.CAP_DSHOW)
        print(f"Opening Windows camera device {device} (DirectShow)")
    elif os_name == "Linux":
        device = '/dev/video0'
        cap = cv2.VideoCapture(device)
        print(f"Opening Linux camera device {device} (V4L2)")
    else:
        print(f"Unsupported OS: {os_name}")
        sys.exit(1)
    if not cap.isOpened():
        print("Failed to open camera.")
        sys.exit(1)
    return cap

class VideoStreamHandler(BaseHTTPRequestHandler):
    camera = None

    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return

        print("Client connected for video stream.")
        self.send_response(200)
        self.send_header('Age', '0')
        self.send_header('Cache-Control', 'no-cache, private')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()

        try:
            while True:
                ret, frame = VideoStreamHandler.camera.read()
                if not ret:
                    print("Failed to read frame from camera.")
                    break

                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    print("Failed to encode frame.")
                    continue

                self.wfile.write(b'--frame\r\n')
                self.wfile.write(b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        except OSError as e:
            print(f"[INFO] Client disconnected (OSError): {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")

def run_server(host='0.0.0.0', port=8000):
    VideoStreamHandler.camera = open_camera()
    server = HTTPServer((host, port), VideoStreamHandler)
    print(f"HTTP server started at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        VideoStreamHandler.camera.release()
        print("Released camera.")

def main():
    run_server(host='localhost', port=8000)

if __name__ == "__main__":
    main()
