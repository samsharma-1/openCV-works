# Product Requirements Document
# Finger-Controlled Instagram + RGB Filter

## 1. Product Vision

Create a touch-free real-time camera application where users manipulate visual effects using hand and finger gestures.

The product combines:

- Computer vision
- Hand landmark detection
- Gesture recognition
- Real-time image processing
- RGB color manipulation

## 2. Problem Statement

Traditional image-filter applications require mouse, keyboard, or touchscreen interaction.

This project replaces those controls with natural hand gestures, allowing the user to interact with the camera output without touching the computer.

## 3. Goals

### Primary Goals

- Detect a user's hand in real time.
- Recognize reliable gestures.
- Switch visual filters using gestures.
- Adjust filter intensity using pinch distance.
- Modify RGB channels using finger movement.
- Provide immediate visual feedback.

### Secondary Goals

- Keep latency low.
- Keep the code modular.
- Make filters easy to extend.
- Run on CPU-only systems.

## 4. Non-Goals

The first version does not need:

- Cloud processing
- User accounts
- Database
- Mobile application
- AI-generated filters
- Online synchronization

## 5. Functional Requirements

### FR-01 Camera

The system shall:

- Open the default webcam.
- Read frames continuously.
- Detect camera failure.
- Allow clean shutdown.

### FR-02 Hand Tracking

The system shall:

- Detect hand landmarks using MediaPipe.
- Track at least one hand.
- Extract fingertip and joint coordinates.

Important landmarks:

```text
0  Wrist
4  Thumb tip
8  Index tip
12 Middle tip
16 Ring tip
20 Pinky tip
```

### FR-03 Gesture Recognition

The system shall classify predefined gestures.

The classifier should use:

- Finger extension state
- Landmark distances
- Landmark angles
- Relative hand geometry

It should not rely exclusively on absolute pixel coordinates.

### FR-04 Filter Selection

The system shall provide a filter manager with a list of available filters.

Example:

```python
filters = [
    "Original",
    "Grayscale",
    "Sepia",
    "Warm",
    "Cool",
    "Vintage",
    "Vivid",
    "Negative",
    "Cinematic"
]
```

### FR-05 Filter Intensity

The system shall convert pinch distance into a normalized intensity value:

```text
0.0 -> 1.0
```

The value should be smoothed before being applied.

### FR-06 RGB Control

The system shall support:

```text
Red   : 0-255
Green : 0-255
Blue  : 0-255
```

The system shall prevent values outside this range.

### FR-07 User Interface

The camera view should display:

- Current filter
- Filter intensity
- RGB values
- Selected RGB channel
- Current gesture
- FPS

### FR-08 Reset

Open palm shall reset:

```text
Filter = Original
Intensity = default
R = default
G = default
B = default
```

## 6. Non-Functional Requirements

### Performance

Target 20–30 FPS on an ordinary laptop.

### Reliability

The system should not change filters because of one noisy frame.

Use temporal smoothing or gesture confirmation.

### Maintainability

Separate:

```text
camera
hand tracking
gesture recognition
filters
RGB processing
UI
main loop
```

### Portability

The project should run on:

- Windows 11
- Linux
- macOS where supported by the Python dependencies

## 7. User Flow

```text
Start application
       |
       v
Open webcam
       |
       v
Detect hand
       |
       v
Recognize gesture
       |
       +---- No valid gesture ----> Keep current state
       |
       v
Update controller state
       |
       v
Apply selected filter
       |
       v
Apply RGB adjustment
       |
       v
Render UI
       |
       v
Repeat
```

## 8. Acceptance Criteria

The first release is successful when:

- Webcam starts correctly.
- Hand landmarks appear correctly.
- Gestures can be detected consistently.
- At least five filters work.
- Filter switching works without keyboard input.
- Pinch controls intensity.
- RGB values can be modified.
- Reset gesture works.
- Application remains responsive for continuous use.
