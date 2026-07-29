import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

canvas = None

prev_x, prev_y = 0, 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        landmarks = hand.landmark

        # Index fingertip
        index_tip = landmarks[8]

        # Middle fingertip
        middle_tip = landmarks[12]

        h, w, _ = frame.shape

        x = int(index_tip.x * w)
        y = int(index_tip.y * h)

        mx = int(middle_tip.x * w)
        my = int(middle_tip.y * h)

        # Distance between index and middle fingers
        distance = np.sqrt((x - mx) ** 2 + (y - my) ** 2)

        # Draw only when fingers are apart
        if distance > 40:

            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y

            cv2.line(
                canvas,
                (prev_x, prev_y),
                (x, y),
                (0, 255, 0),
                6
            )

            prev_x, prev_y = x, y

        else:
            prev_x, prev_y = 0, 0

    output = cv2.add(frame, canvas)

    cv2.putText(
        output,
        "Spread Index & Middle Finger to Draw",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2,
    )

    cv2.imshow("Air Writing", output)

    key = cv2.waitKey(1)

    if key == ord("c"):
        canvas = np.zeros_like(frame)

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()