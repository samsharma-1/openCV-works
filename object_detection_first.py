from ultralytics import YOLO
import cv2

# Load YOLOv8 Nano Model
model = YOLO("yolov8n.pt")

# Open Webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    # Detect Objects
    results = model(frame)

    # Draw Results
    annotated_frame = results[0].plot()

    cv2.imshow("Object Detection", annotated_frame)

    # Press ESC to Exit
    if cv2.waitKey(1) == 27:
        break
for result in results:
    for box in result.boxes:

        confidence = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        class_id = int(box.cls[0])
        label = model.names[class_id]

        text = f"{label} {confidence*100:.1f}%"

        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(frame,
                    text,
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2)

cap.release()
cv2.destroyAllWindows()