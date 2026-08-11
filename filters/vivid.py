import cv2
import numpy as np

class VividFilter:
    def __init__(self):
        self.name = "Vivid"

    def apply(self, frame, intensity):
        # Increase saturation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] *= 1.5  # Increase saturation by 50%
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        vivid = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        return cv2.addWeighted(frame, 1.0 - intensity, vivid, intensity, 0)
