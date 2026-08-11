import cv2
import numpy as np

def create_lut(x, y):
    spline = np.interp(np.arange(256), x, y).astype(np.uint8)
    return spline

class WarmFilter:
    def __init__(self):
        self.name = "Warm"
        # Increase red, decrease blue
        x = [0, 64, 128, 192, 255]
        r_y = [0, 74, 148, 212, 255]
        b_y = [0, 54, 108, 172, 255]
        
        self.r_lut = create_lut(x, r_y)
        self.b_lut = create_lut(x, b_y)

    def apply(self, frame, intensity):
        b, g, r = cv2.split(frame)
        
        r_new = cv2.LUT(r, self.r_lut)
        b_new = cv2.LUT(b, self.b_lut)
        
        warm = cv2.merge((b_new, g, r_new))
        return cv2.addWeighted(frame, 1.0 - intensity, warm, intensity, 0)
