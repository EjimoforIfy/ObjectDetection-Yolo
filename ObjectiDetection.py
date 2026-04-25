from ultralytics import YOLO
import cv2
import random
import time

# Load YOLO model
model = YOLO("yolov8n.pt")  # or your trained model best.pt

# Open webcam
cap = cv2.VideoCapture(0)

print("Simulation started...")
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ---- SIMULATED ULTRASONIC SENSOR ----
    distance = random.randint(10, 50)  # cm (simulated)
    print(f"\nSimulated Distance: {distance} cm")

    if distance < 30:
        print("Object detected within range")

        # ---- YOLO DETECTION ----
        results = model(frame)
        annotated_frame = results[0].plot()

        detected_classes = []
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            detected_classes.append(label)

        # ---- SIMULATED LOGIC ----
        recyclable_items = ["bottle", "cup", "plastic", "can"]
        trash_items = ["food", "banana", "paper", "cotton wool", "plaster","paper bag","waste"]

        is_recyclable = any(item in recyclable_items for item in detected_classes)
        is_trash = any(item in trash_items for item in detected_classes)

        if is_recyclable:
            print("GREEN LED ON -> Recyclable detected")
            print("RED LED OFF")
            print("Buzzer OFF")

        elif is_trash:
            print("RED LED ON -> Trash detected")
            print("GREEN LED OFF")
            print("BUZZER ON -> Alert!")

        else:
            print("Unknown item")
            print("RED LED ON")
            print("BUZZER ON")

        cv2.imshow("Smart Recycling Simulation", annotated_frame)

    else:
        print("No object nearby")
        print("LEDs OFF | Buzzer OFF")
        cv2.imshow("Smart Recycling Simulation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()
print("Simulation ended.")
