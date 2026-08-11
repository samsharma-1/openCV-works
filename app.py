import cv2
import time
import sys

from src.camera import Camera
from src.hand_tracker import HandTracker
from src.gesture_controller import GestureController
from src.filter_engine import FilterEngine
from src.rgb_controller import RGBController
from src.ui import UI
import config

def main():
    print("Initializing Application...")
    try:
        camera = Camera()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    tracker = HandTracker()
    gesture_ctrl = GestureController()
    filter_engine = FilterEngine()
    rgb_ctrl = RGBController()
    ui = UI()

    state = {
        "filter_name": filter_engine.get_current_filter_name(),
        "filter_intensity": filter_engine.intensity,
        "rgb": {"r": 255, "g": 255, "b": 255},
        "selected_channel": 'r',
        "gesture": "NONE"
    }

    prev_time = time.time()
    mode = "FILTER" # can be "FILTER" or "RGB"

    print("Application started. Press 'q' to quit.")

    while True:
        frame = camera.read_frame()
        if frame is None:
            break

        # Calculate FPS
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time))
        prev_time = curr_time

        # Process hands
        results = tracker.process_frame(frame)
        h, w, c = frame.shape
        landmarks = tracker.extract_landmarks(results, w, h)

        command = "NONE"
        
        # If hand detected
        if landmarks:
            command = gesture_ctrl.update(landmarks)
            
            # Apply continuous controls based on state
            if mode == "FILTER":
                if gesture_ctrl.current_command == "ADJUST_INTENSITY":
                    # Normalize distance, let's say max distance is 0.2
                    intensity = min(1.0, gesture_ctrl.pinch_distance / 0.2)
                    filter_engine.set_intensity(intensity)
            elif mode == "RGB":
                if gesture_ctrl.current_command == "ADJUST_RGB":
                    rgb_ctrl.update_value(gesture_ctrl.index_x, config.HORIZONTAL_DEADZONE)
                else:
                    rgb_ctrl.active = False
            
            # Apply discrete commands
            if command == "RESET":
                filter_engine.current_index = 0
                filter_engine.set_intensity(1.0)
                rgb_ctrl.reset()
                mode = "FILTER"
            elif command == "NEXT_FILTER" and mode == "FILTER":
                filter_engine.next_filter()
            elif command == "RGB_MODE":
                mode = "RGB" if mode == "FILTER" else "FILTER"
            elif command == "CONFIRM":
                # Maybe switch RGB channel if in RGB mode
                if mode == "RGB":
                    rgb_ctrl.toggle_channel()
        else:
            gesture_ctrl.current_command = "NONE"
            rgb_ctrl.active = False

        # Apply image processing
        processed_frame = filter_engine.apply(frame)
        processed_frame = rgb_ctrl.apply(processed_frame)

        # Update State for UI
        state["filter_name"] = filter_engine.get_current_filter_name()
        state["filter_intensity"] = filter_engine.intensity
        state["rgb"]["r"] = rgb_ctrl.r
        state["rgb"]["g"] = rgb_ctrl.g
        state["rgb"]["b"] = rgb_ctrl.b
        state["selected_channel"] = rgb_ctrl.selected_channel
        state["gesture"] = gesture_ctrl.current_command

        # Draw UI
        ui.draw_landmarks(processed_frame, results, tracker.mp_hands, tracker.mp_draw)
        ui.draw_info(processed_frame, state, fps)

        cv2.imshow("Finger-Controlled Instagram", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    tracker.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
