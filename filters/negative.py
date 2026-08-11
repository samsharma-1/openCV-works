import cv2

class NegativeFilter:
    def __init__(self):
        self.name = "Negative"

    def apply(self, frame, intensity):
        negative = cv2.bitwise_not(frame)
        return cv2.addWeighted(frame, 1.0 - intensity, negative, intensity, 0)
