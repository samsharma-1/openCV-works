# System Architecture

## 1. Directory Structure

```text
finger-filter/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── PRD.md
├── ARCHITECTURE.md
├── GESTURES.md
│
├── src/
│   ├── __init__.py
│   ├── camera.py
│   ├── hand_tracker.py
│   ├── gesture_controller.py
│   ├── filter_engine.py
│   ├── rgb_controller.py
│   ├── ui.py
│   └── utils.py
│
├── filters/
│   ├── __init__.py
│   ├── original.py
│   ├── grayscale.py
│   ├── sepia.py
│   ├── warm.py
│   ├── cool.py
│   ├── vintage.py
│   ├── vivid.py
│   ├── negative.py
│   └── cinematic.py
│
├── tests/
│   ├── test_gestures.py
│   ├── test_filters.py
│   └── test_rgb.py
│
└── assets/
    └── screenshots/
```

## 2. Module Responsibilities

### app.py

Application entry point.

Responsibilities:

- Initialize components.
- Run the main loop.
- Coordinate frame processing.
- Handle shutdown.

### camera.py

Responsibilities:

- Open webcam.
- Read frames.
- Configure resolution/FPS.
- Release camera.

### hand_tracker.py

Responsibilities:

- Initialize MediaPipe.
- Process frames.
- Return hand landmarks.
- Handle tracking confidence.

### gesture_controller.py

Responsibilities:

- Convert landmarks into gestures.
- Apply debounce/smoothing.
- Produce high-level commands.

Example commands:

```text
NEXT_FILTER
PREVIOUS_FILTER
RGB_MODE
ADJUST_INTENSITY
RESET
CONFIRM
```

### filter_engine.py

Responsibilities:

- Maintain active filter.
- Apply filter.
- Apply intensity.
- Expose filter switching.

### rgb_controller.py

Responsibilities:

- Store R/G/B values.
- Modify selected channel.
- Clamp values.
- Apply RGB transformation.

### ui.py

Responsibilities:

- Draw landmarks.
- Draw filter name.
- Draw RGB values.
- Draw intensity.
- Draw FPS.
- Draw gesture status.

## 3. Main Processing Pipeline

For each frame:

```text
Capture frame
    ↓
Flip frame
    ↓
Convert BGR → RGB
    ↓
MediaPipe hand processing
    ↓
Extract landmarks
    ↓
Gesture recognition
    ↓
Update application state
    ↓
Apply filter
    ↓
Apply RGB adjustment
    ↓
Draw UI
    ↓
Display frame
```

## 4. State Model

Recommended state:

```python
state = {
    "filter_index": 0,
    "filter_intensity": 1.0,
    "rgb": {
        "r": 255,
        "g": 255,
        "b": 255
    },
    "selected_channel": "r",
    "gesture": "NONE"
}
```

## 5. Design Principle

Gesture recognition should generate commands.

It should NOT directly modify pixels.

This separation keeps the architecture clean:

```text
Gesture
  ↓
Command
  ↓
Application State
  ↓
Image Processing
```

This makes the system easier to debug and extend.
