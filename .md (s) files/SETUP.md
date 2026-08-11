# Setup Guide

## 1. Install Python

Use Python 3.10 or newer.

Check:

```bash
python --version
```

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run

```bash
python app.py
```

## 5. Camera Troubleshooting

If the default camera does not open, try another camera index:

```python
cv2.VideoCapture(1)
```

or:

```python
cv2.VideoCapture(2)
```

## 6. Performance Optimization

If FPS is low:

- Reduce camera resolution.
- Process at 640x480.
- Lower MediaPipe model complexity.
- Reduce filter computation.
- Avoid unnecessary frame copies.
- Use NumPy vectorized operations.

## 7. Windows Notes

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again.

## 8. Recommended Development Order

Build in this order:

1. Webcam capture.
2. MediaPipe hand tracking.
3. Finger-state detection.
4. Gesture debouncing.
5. Filter engine.
6. Filter switching.
7. Pinch intensity.
8. RGB controller.
9. UI overlay.
10. Performance optimization.
11. Testing.
