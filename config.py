# Configuration Parameters

# Camera
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
TARGET_FPS = 30

# Gesture Thresholds
PINCH_THRESHOLD = 0.08       # Normalized distance to activate pinch
GESTURE_COOLDOWN = 0.5       # Seconds between gesture triggers (e.g., next filter)
DEBOUNCE_FRAMES = 5          # Number of consistent frames to confirm a gesture
HORIZONTAL_DEADZONE = 0.02   # Deadzone for horizontal finger movement

# UI Configuration
FONT = 1 # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2
COLOR_TEXT = (255, 255, 255)
COLOR_BG = (0, 0, 0)
COLOR_HIGHLIGHT = (0, 255, 0)

# Landmarks (MediaPipe Hands)
LM_WRIST = 0
LM_THUMB_TIP = 4
LM_INDEX_TIP = 8
LM_MIDDLE_TIP = 12
LM_RING_TIP = 16
LM_PINKY_TIP = 20
