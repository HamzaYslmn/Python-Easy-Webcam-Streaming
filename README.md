# Python-Easy-Webcam-Streaming

This script provides a simple HTTP MJPEG streaming server using your system's webcam. It is cross-platform and works on both Windows and Linux.

## Features

- Streams live video from your webcam over HTTP (MJPEG format)
- Simple to run, no external dependencies except OpenCV and Python standard library
- Prints status and error messages to the console

## Requirements

- Python 3.x
- OpenCV (`pip install opencv-python`)

## Usage

1. **Install dependencies:**
   ```sh
   pip install opencv-python
   ```

2. **Run the script:**
   ```sh
   python cameratest.py
   ```

3. **View the stream:**
   Open your browser and go to [http://localhost:8000/](http://localhost:8000/)

## How it works

- The script detects your OS and opens the default webcam.
- It starts an HTTP server on port 8000.
- When a client connects, it streams MJPEG video frames from the webcam.
- All status and error messages are printed to the console.

## License

This script is licensed under the GNU Affero General Public License v3.0.  
See [LICENSE](https://github.com/HamzaYslmn/Python-Easy-Webcam-Streaming/blob/main/LICENSE) for details.
