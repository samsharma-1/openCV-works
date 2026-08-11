import cv2
import numpy as np

class SepiaFilter:
    def __init__(self):
        self.name = "Sepia"

    def apply(self, frame, intensity):
        # Sepia transformation matrix
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(frame, kernel)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        return cv2.addWeighted(frame, 1.0 - intensity, sepia, intensity, 0)
