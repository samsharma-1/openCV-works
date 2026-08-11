import cv2
import numpy as np

class VintageFilter:
    def __init__(self):
        self.name = "Vintage"

    def apply(self, frame, intensity):
        rows, cols = frame.shape[:2]
        
        # Create a vignette mask
        kernel_x = cv2.getGaussianKernel(cols, cols/2)
        kernel_y = cv2.getGaussianKernel(rows, rows/2)
        kernel = kernel_y * kernel_x.T
        mask = 255 * kernel / np.linalg.norm(kernel)
        mask = cv2.resize(mask, (cols, rows))
        
        # Apply sepia-like color mapping
        vintage = frame.copy()
        
        # Apply mask
        for i in range(3):
            vintage[:, :, i] = vintage[:, :, i] * mask
            
        return cv2.addWeighted(frame, 1.0 - intensity, vintage, intensity, 0)
