# Finger-Controlled Instagram + RGB Filter

A real-time computer-vision project that uses a webcam, MediaPipe hand tracking, OpenCV, and NumPy to control Instagram-style visual filters and RGB color parameters using finger gestures.

## 1. Project Objective

Build a touch-free visual filter application in which the user's hand becomes the controller.

The system should:

- Capture live webcam frames.
- Detect hand landmarks in real time.
- Recognize predefined finger gestures.
- Select and switch between visual filters.
- Control filter intensity using pinch distance.
- Control red, green, and blue channels using finger movement.
- Display the active filter, selected RGB channel, intensity, and gesture state.
- Reset the image processing state with an open-palm gesture.

## 2. Core Technology

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Camera | OpenCV |
| Hand tracking | MediaPipe |
| Numerical processing | NumPy |
| UI / overlays | OpenCV |
| Input | Webcam |
| Platform | Windows / Linux |

## 3. High-Level Architecture

```text
                 Webcam
                    |
                    v
             OpenCV VideoCapture
                    |
                    v
              Video Frame
                    |
          +---------+---------+
          |                   |
          v                   v
   MediaPipe Hands       Filter Engine
          |                   |
          v                   |
   Hand Landmarks             |
          |                   |
          v                   |
   Gesture Recognizer         |
          |                   |
          +---------+---------+
                    |
                    v
             Filter Controller
                    |
          +---------+---------+
          |                   |
          v                   v
 Instagram Filters       RGB Controller
          |                   |
          +---------+---------+
                    |
                    v
              Final Frame
                    |
                    v
              OpenCV Window
```

## 4. Supported Filter Modes

The initial implementation should contain:

1. Original
2. Grayscale
3. Sepia
4. Warm
5. Cool
6. Vintage
7. Vivid
8. Negative
9. Cinematic

The filter engine should be modular so additional filters can be added without changing gesture recognition.

## 5. Gesture Controls

| Gesture | Function |
|---|---|
| Index finger | Select / interact |
| Two fingers | Next filter |
| Three fingers | RGB control mode |
| Pinch | Adjust filter intensity |
| Index moves left/right | Change selected RGB value |
| Thumb up | Confirm / lock selection |
| Open palm | Reset |

Gesture recognition should use landmark geometry rather than fixed pixel coordinates wherever possible.

## 6. Filter Intensity

The distance between thumb tip and index tip can be normalized and mapped to an intensity value.

```text
Small pinch  -> 0%
Medium pinch -> 50%
Wide pinch   -> 100%
```

The implementation should smooth the measured value to reduce jitter.

## 7. RGB Control

RGB mode contains three channels:

```text
R -> Red
G -> Green
B -> Blue
```

The selected channel can be changed using a gesture or cycling mechanism.

Finger movement controls the selected channel:

```text
Move left  -> decrease
Move right -> increase
```

Each channel is clamped to:

```text
0 <= channel <= 255
```

## 8. Runtime Requirements

Recommended hardware:

- Laptop/desktop with webcam
- Intel Core i5 or equivalent
- 8 GB RAM minimum
- 720p webcam recommended
- Python 3.10 or newer

A dedicated GPU is not required for the initial implementation.

## 9. Software Requirements

Install:

```bash
pip install opencv-python mediapipe numpy
```

Verify:

```bash
python --version
pip show opencv-python mediapipe numpy
```

## 10. Performance Target

Target:

- 720p camera input
- 20–30 FPS on a normal laptop
- Low gesture latency
- Stable hand tracking under normal indoor lighting

For better performance, process the camera frame at a smaller resolution and display the processed result at the required output size.

## 11. Safety / Robustness

The application should handle:

- No hand detected
- Multiple hands
- Temporary landmark loss
- Poor lighting
- Rapid hand movement
- Camera unavailable
- Invalid gesture transitions

When no hand is detected, the current filter should remain active rather than randomly changing.

## 12. Future Extensions

Possible upgrades:

- Face-aware Instagram filters
- Face landmarks
- AR masks
- Background segmentation
- Hand-drawn effects
- Gesture-controlled brightness/contrast
- Recording and screenshot support
- Multiple-hand controls
- Custom filter presets
- GUI using PyQt or Tkinter
- Web deployment using browser-based hand tracking
