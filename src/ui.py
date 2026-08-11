import cv2
import config

class UI:
    def __init__(self):
        self.mp_draw = config.mp_draw if hasattr(config, 'mp_draw') else None # Will be set externally or use cv2

    def draw_landmarks(self, frame, results, mp_hands, mp_draw):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    def draw_info(self, frame, state, fps):
        h, w = frame.shape[:2]
        
        # Create a transparent overlay
        overlay = frame.copy()
        
        # Draw side panel
        cv2.rectangle(overlay, (0, 0), (280, h), (0, 0, 0), -1)
        # Blend overlay
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        
        # Title
        cv2.putText(frame, "InstaGestures", (15, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 200, 200), 2)
        cv2.line(frame, (10, 40), (270, 40), (255, 255, 255), 1)
        
        # Filter info
        cv2.putText(frame, "FILTER", (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, f"{state['filter_name']}", (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        
        # Intensity bar
        cv2.putText(frame, "INTENSITY", (15, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        intensity = state['filter_intensity']
        bar_w = 200
        cv2.rectangle(frame, (15, 155), (15 + bar_w, 165), (100, 100, 100), -1)
        cv2.rectangle(frame, (15, 155), (15 + int(bar_w * intensity), 165), (0, 255, 0), -1)
        
        # RGB Info
        cv2.putText(frame, "RGB TUNING", (15, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        r, g, b = state['rgb']['r'], state['rgb']['g'], state['rgb']['b']
        sel = state['selected_channel']
        
        # Draw R, G, B bars
        def draw_bar(y, label, val, is_sel, color):
            # Highlight selected
            if is_sel:
                cv2.rectangle(frame, (10, y-15), (270, y+15), (50, 50, 50), -1)
            cv2.putText(frame, label, (15, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2 if is_sel else 1)
            cv2.rectangle(frame, (50, y-5), (50 + 200, y+5), (100, 100, 100), -1)
            cv2.rectangle(frame, (50, y-5), (50 + int(val/255*200), y+5), color, -1)
            
        draw_bar(250, "R", r, sel == 'r', (0, 0, 255))
        draw_bar(290, "G", g, sel == 'g', (0, 255, 0))
        draw_bar(330, "B", b, sel == 'b', (255, 0, 0))
        
        # FPS and Gesture on the right side
        cv2.putText(frame, f"FPS: {fps}", (w - 100, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Fancy gesture badge
        g_text = state['gesture']
        if g_text != "NONE":
            cv2.rectangle(frame, (w - 220, 50), (w - 10, 90), (0, 0, 0), -1)
            cv2.putText(frame, f"CMD: {g_text}", (w - 210, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
