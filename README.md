# AUV Vision Pipeline 

A modular, OpenCV-based ROS 2 perception node designed to identify PVC competition gates in murky underwater environments. This stack relies strictly on classic computer vision math—no heavy machine learning models—to maintain high FPS on constrained hardware.

## Key Features

* **Dynamic CLAHE Enhancement:** Integrates an adaptive color-correction filter to cut through underwater noise and normalize RGB channels. Fully toggleable via ROS 2 parameters (`enable_enhancement`).
* **Split-Gate Contour Logic:** Custom mathematical pipeline (`rect_fix.py` & `geometry.py`) that repairs broken bounding boxes. If the camera only sees half the gate, it mathematically infers the 90-degree corners to maintain a stable lock.
* **Pose Estimation:** Calculates real-world forward distance (meters) and lateral offset (pixels) using known gate dimensions and camera focal length, publishing directly to the AUV's PID controllers via `PoseStamped`.
* **Standalone Testing:** Includes `standalone_vision.py` to test the entire OpenCV math chain on local video files without needing to source or launch the full ROS 2 environment.

## Tech Stack
* **Framework:** ROS 2 (Jazzy)
* **Vision:** OpenCV, NumPy
* **Language:** Python 3

## Usage

**Launch the full stack (Vision, Control, and Echo tabs):**
```bash
./start_stack.sh
```
**Launch the stack without CLAHE enhancement Vision, Control, and Echo tabs):**
```bash
./start_stack.sh off
```
