import cv2

class GrayscaleFilter:
    def __init__(self):
        self.name = "Grayscale"

    def apply(self, frame, intensity):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return cv2.addWeighted(frame, 1.0 - intensity, gray_bgr, intensity, 0)
