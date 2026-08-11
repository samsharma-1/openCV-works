import cv2
import config

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open camera with index {config.CAMERA_INDEX}")

    def read_frame(self):
        """Read and return a frame from the camera. Flips the frame horizontally."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        # Flip horizontally for selfie view
        frame = cv2.flip(frame, 1)
        return frame

    def release(self):
        """Release the camera resource."""
        self.cap.release()
