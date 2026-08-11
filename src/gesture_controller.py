import time
import config
from src.utils import calculate_distance

class GestureController:
    def __init__(self):
        self.last_gesture = "NONE"
        self.gesture_frames = 0
        self.last_action_time = 0
        self.current_command = "NONE"
        self.pinch_distance = 0.0
        self.index_x = 0.0

    def is_finger_extended(self, landmarks, tip_idx, pip_idx):
        """Check if a finger is extended by comparing distance to wrist."""
        wrist = landmarks[0]
        tip = landmarks[tip_idx]
        pip = landmarks[pip_idx]
        
        dist_tip = calculate_distance((wrist['x'], wrist['y']), (tip['x'], tip['y']))
        dist_pip = calculate_distance((wrist['x'], wrist['y']), (pip['x'], pip['y']))
        return dist_tip > dist_pip

    def detect_gesture(self, landmarks):
        if not landmarks:
            return "NONE"

        # Finger states
        thumb_is_up = landmarks[4]['y'] < landmarks[3]['y'] and landmarks[4]['x'] < landmarks[5]['x'] # Simplified
        index_extended = self.is_finger_extended(landmarks, 8, 6)
        middle_extended = self.is_finger_extended(landmarks, 12, 10)
        ring_extended = self.is_finger_extended(landmarks, 16, 14)
        pinky_extended = self.is_finger_extended(landmarks, 20, 18)

        # Calculate pinch distance
        self.pinch_distance = calculate_distance(
            (landmarks[4]['x'], landmarks[4]['y']),
            (landmarks[8]['x'], landmarks[8]['y'])
        )
        
        self.index_x = landmarks[8]['x']

        # Determine gesture based on priority (Open Palm -> Pinch -> Three -> Two -> Index -> None)
        if index_extended and middle_extended and ring_extended and pinky_extended:
            return "OPEN_PALM"
        
        if self.pinch_distance < config.PINCH_THRESHOLD:
            return "PINCH"
            
        if index_extended and middle_extended and ring_extended and not pinky_extended:
            return "THREE_FINGERS"
            
        if index_extended and middle_extended and not ring_extended and not pinky_extended:
            return "TWO_FINGERS"
            
        if index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "INDEX_FINGER"
            
        if thumb_is_up and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "THUMB_UP"

        return "NONE"

    def update(self, landmarks):
        """
        Takes landmarks, applies debouncing, and returns a command string.
        Also updates pinch_distance and index_x for continuous control.
        """
        raw_gesture = self.detect_gesture(landmarks)
        
        if raw_gesture == self.last_gesture:
            self.gesture_frames += 1
        else:
            self.gesture_frames = 0
            self.last_gesture = raw_gesture

        current_time = time.time()
        command = "NONE"

        # Check if gesture is confirmed by holding it for DEBOUNCE_FRAMES
        if self.gesture_frames >= config.DEBOUNCE_FRAMES:
            # Apply cooldown for discrete actions
            if current_time - self.last_action_time > config.GESTURE_COOLDOWN:
                if raw_gesture == "OPEN_PALM":
                    command = "RESET"
                    self.last_action_time = current_time
                elif raw_gesture == "TWO_FINGERS":
                    command = "NEXT_FILTER"
                    self.last_action_time = current_time
                elif raw_gesture == "THREE_FINGERS":
                    command = "RGB_MODE"
                    self.last_action_time = current_time
                elif raw_gesture == "THUMB_UP":
                    command = "CONFIRM"
                    self.last_action_time = current_time

            # Continuous actions don't have cooldown
            if raw_gesture == "PINCH":
                command = "ADJUST_INTENSITY"
            elif raw_gesture == "INDEX_FINGER":
                command = "ADJUST_RGB"
                
        self.current_command = command
        return command
