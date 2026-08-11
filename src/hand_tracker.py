import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """
        Process the BGR frame to detect hand landmarks.
        Returns the raw results object from MediaPipe.
        """
        # Convert to RGB as required by MediaPipe
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        return results

    def extract_landmarks(self, results, width, height):
        """
        Extract normalized landmarks into a list of (x, y) dictionaries.
        """
        landmarks = []
        if results.multi_hand_landmarks:
            hand_lms = results.multi_hand_landmarks[0]
            for lm in hand_lms.landmark:
                # Store normalized coordinates
                landmarks.append({'x': lm.x, 'y': lm.y, 'z': lm.z})
        return landmarks
        
    def close(self):
        self.hands.close()
