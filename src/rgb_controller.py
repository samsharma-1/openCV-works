import cv2
import numpy as np

class RGBController:
    def __init__(self):
        self.r = 255
        self.g = 255
        self.b = 255
        self.selected_channel = 'r'
        self.last_x = 0.5
        self.active = False
        
    def reset(self):
        self.r = 255
        self.g = 255
        self.b = 255
        self.selected_channel = 'r'
        self.active = False
        
    def toggle_channel(self):
        if self.selected_channel == 'r':
            self.selected_channel = 'g'
        elif self.selected_channel == 'g':
            self.selected_channel = 'b'
        else:
            self.selected_channel = 'r'

    def update_value(self, index_x, deadzone):
        """Update RGB value based on horizontal finger position."""
        self.active = True
        
        # Map index_x from [0.2, 0.8] to [0, 255]
        val = int((index_x - 0.2) / 0.6 * 255)
        val = max(0, min(255, val))
        
        if self.selected_channel == 'r':
            self.r = val
        elif self.selected_channel == 'g':
            self.g = val
        elif self.selected_channel == 'b':
            self.b = val

    def apply(self, frame):
        """Apply RGB modification to the frame."""
        if self.r == 255 and self.g == 255 and self.b == 255:
            return frame
            
        # Convert to float for multiplication
        float_frame = frame.astype(np.float32)
        
        # OpenCV uses BGR
        float_frame[:, :, 0] *= (self.b / 255.0)
        float_frame[:, :, 1] *= (self.g / 255.0)
        float_frame[:, :, 2] *= (self.r / 255.0)
        
        # Clip and convert back
        return np.clip(float_frame, 0, 255).astype(np.uint8)
