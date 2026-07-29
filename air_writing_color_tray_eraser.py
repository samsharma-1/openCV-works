import cv2
import mediapipe as mp
import numpy as np

# ------------------ MediaPipe ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ------------------ Camera ------------------
cap = cv2.VideoCapture(0)

canvas = None
prev_x, prev_y = 0, 0

# ------------------ Drawing Settings ------------------

colors = [
    ("Red", (0, 0, 255)),
    ("Green", (0, 255, 0)),
    ("Blue", (255, 0, 0)),
    ("Yellow", (0, 255, 255)),
    ("White", (255, 255, 255)),
    ("Black", (0, 0, 0))
]

brush_color = colors[1][1]      # Green default
brush_name = colors[1][0]

brush_thickness = 6
eraser_thickness = 30

eraser = False

toolbar_height = 60

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

    for i, (_, color) in enumerate(colors):

        x1 = 10 + i * 60
        x2 = x1 + 50

        cv2.rectangle(frame, (x1, 10), (x2, 50), color, -1)

    # Eraser Button
    cv2.rectangle(frame, (380, 10), (490, 50), (180, 180, 180), -1)
    cv2.putText(frame, "ERASE", (392, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2)

    # Clear Button
    cv2.rectangle(frame, (510, 10), (620, 50), (60, 60, 60), -1)
    cv2.putText(frame, "CLEAR", (520, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2)

    # ---------------- Hand Detection ----------------

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

        x = int(index.x * w)
        y = int(index.y * h)

        mx = int(middle.x * w)
        my = int(middle.y * h)

        distance = np.sqrt((x - mx) ** 2 + (y - my) ** 2)

        # -------- Toolbar Selection --------

        if y < toolbar_height:

            for i, (name, color) in enumerate(colors):

                left = 10 + i * 60
                right = left + 50

                if left < x < right:

                    brush_color = color
                    brush_name = name
                    eraser = False

            if 380 < x < 490:
                eraser = True

            if 510 < x < 620:
                canvas = np.zeros_like(canvas)

            prev_x, prev_y = 0, 0

        else:

            # Draw only when fingers are apart

            if distance > 40:

                if prev_x == 0 and prev_y == 0:
                    prev_x = x
                    prev_y = y

                if eraser:

                    cv2.line(
                        canvas,
                        (prev_x, prev_y),
                        (x, y),
                        (0, 0, 0),
                        eraser_thickness
                    )

                else:

                    cv2.line(
                        canvas,
                        (prev_x, prev_y),
                        (x, y),
                        brush_color,
                        brush_thickness
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
        (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        brush_color if not eraser else (255, 255, 255),
        2
    )

    cv2.putText(
        output,
        "Spread Index & Middle Finger to Draw",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2
    )

    cv2.imshow("Air Writing", output)

    key = cv2.waitKey(1)

    if key == ord("c"):
        canvas = np.zeros_like(canvas)

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()