import cv2
import numpy as np

class CinematicFilter:
    def __init__(self):
        self.name = "Cinematic"

    def apply(self, frame, intensity):
        # Cinematic look: letterbox + teal/orange grading (simplified)
        rows, cols = frame.shape[:2]
        
        # Color grading
        b, g, r = cv2.split(frame)
        # Increase red (warm highlights), increase blue in shadows (not accurate, just simple approximation)
        b = cv2.add(b, 20)
        r = cv2.add(r, 20)
        graded = cv2.merge((b, g, r))
        
        # Letterbox
        bar_height = int(rows * 0.1)
        graded[0:bar_height, :] = 0
        graded[rows-bar_height:rows, :] = 0
        
        return cv2.addWeighted(frame, 1.0 - intensity, graded, intensity, 0)
