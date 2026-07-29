import cv2
import mediapipe as mp
import numpy as np

# ---------------- MediaPipe ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ---------------- Camera ----------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

canvas = None

prev_x, prev_y = 0, 0
smooth_x, smooth_y = 0, 0

alpha = 0.25

# ---------------- Thermal Palette ----------------

gradient_width = 600
gradient_height = 40

thermal_bar = np.zeros(
    (gradient_height, gradient_width, 3),
    dtype=np.uint8
)

for i in range(gradient_width):

    color = cv2.applyColorMap(
        np.array([[i * 255 // gradient_width]], dtype=np.uint8),
        cv2.COLORMAP_INFERNO
    )[0][0]

    thermal_bar[:, i] = color

brush_color = (0, 255, 0)
brush_name = "Thermal"

brush_thickness = 6
eraser_size = 30

eraser = False

toolbar_height = 60

# ---------------------------------------------------

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    # ---------------- Toolbar ----------------

    frame[10:50, 10:610] = thermal_bar

    # Eraser
    cv2.rectangle(frame, (630, 10), (730, 50), (180, 180, 180), -1)
    cv2.putText(frame, "ERASE",
                (642, 38),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2)

    # Clear
    cv2.rectangle(frame, (750, 10), (850, 50), (60, 60, 60), -1)
    cv2.putText(frame, "CLEAR",
                (760, 38),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2)

    # Brush Sizes

    cv2.rectangle(frame, (870, 10), (920, 50), (255,255,255), -1)
    cv2.putText(frame, "S",
                (885,38),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,0),
                2)

    cv2.rectangle(frame, (930,10), (980,50), (220,220,220), -1)
    cv2.putText(frame, "M",
                (945,38),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,0),
                2)

    cv2.rectangle(frame, (990,10), (1040,50), (180,180,180), -1)
    cv2.putText(frame, "L",
                (1005,38),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,0,0),
                2)

    # ---------------- Hand ----------------

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        landmarks = hand.landmark

        index = landmarks[8]
        middle = landmarks[12]

        h, w, _ = frame.shape

        raw_x = int(index.x * w)
        raw_y = int(index.y * h)

        smooth_x = int(alpha * raw_x + (1-alpha) * smooth_x)
        smooth_y = int(alpha * raw_y + (1-alpha) * smooth_y)

        x = smooth_x
        y = smooth_y

        mx = int(middle.x * w)
        my = int(middle.y * h)

        distance = np.sqrt((x-mx)**2 + (y-my)**2)

        # ---------------- Toolbar Selection ----------------

        if y < toolbar_height:

            if 10 < x < 610:

                idx = x - 10

                brush_color = tuple(
                    int(v)
                    for v in thermal_bar[20, idx]
                )

                brush_name = "Thermal"

                eraser = False

            elif 630 < x < 730:

                eraser = True

            elif 750 < x < 850:

                canvas = np.zeros_like(canvas)

            elif 870 < x < 920:

                brush_thickness = 3

            elif 930 < x < 980:

                brush_thickness = 8

            elif 990 < x < 1040:

                brush_thickness = 15

            prev_x = 0
            prev_y = 0

        else:

            if distance > 40:

                if prev_x == 0:
                    prev_x = x
                    prev_y = y

                if eraser:

                    cv2.circle(
                        canvas,
                        (x,y),
                        eraser_size,
                        (0,0,0),
                        -1
                    )

                else:

                    cv2.line(
                        canvas,
                        (prev_x, prev_y),
                        (x, y),
                        brush_color,
                        brush_thickness,
                        cv2.LINE_AA
                    )

                    cv2.circle(
                        canvas,
                        (x,y),
                        brush_thickness//2,
                        brush_color,
                        -1
                    )

                prev_x = x
                prev_y = y

            else:

                prev_x = 0
                prev_y = 0

    # ---------------- Merge ----------------

    output = cv2.add(frame, canvas)

    mode = "ERASER" if eraser else brush_name

    cv2.putText(
        output,
        f"Tool : {mode}",
        (20,90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        brush_color if not eraser else (255,255,255),
        2
    )

    cv2.putText(
        output,
        f"Brush : {brush_thickness}px",
        (20,125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        output,
        "Spread Index & Middle Finger to Draw",
        (20,160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    cv2.imshow("Virtual Thermal Whiteboard", output)

    key = cv2.waitKey(1)

    if key == ord("c"):
        canvas = np.zeros_like(canvas)

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()