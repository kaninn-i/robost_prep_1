# import cv2
# from ultralytics import YOLO

# model = YOLO('yolov8n.pt') 
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret: break
    
#     # Предобработка через OpenCV
#     resized = cv2.resize(frame, (640, 640))
#     blurred = cv2.GaussianBlur(resized, (5,5), 0)
    
#     # Детекция через YOLO
#     results = model(blurred)
    
#     # Постобработка и визуализация
#     for box in results[0].boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         cls_id = int(box.cls[0])
#         conf = float(box.conf[0])
        
#         # Отрисовка через OpenCV
#         cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
#         cv2.putText(frame, 
#                    f"{model.names[cls_id]} {conf:.2f}",
#                    (x1, y1-10), 
#                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    
#     cv2.imshow('YOLO + OpenCV', frame)
#     if cv2.waitKey(1) == 27: break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n-seg.pt')

def detect_shape(contour):
    peri = cv2.arcLength(contour, True)
    epsilon = 0.04 * peri
    approx = cv2.approxPolyDP(contour, epsilon, True)
    return len(approx)

def get_dominant_color(roi):
    pixels = np.float32(roi.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, _, centers = cv2.kmeans(pixels, 2, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    return centers[0].astype(int)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break
    
    results = model(frame)[0]
    
    if results.masks is not None:
        for mask, box in zip(results.masks.xy, results.boxes):
            # Конвертация контура в правильный формат
            contour = np.array(mask, dtype=np.int32).reshape((-1, 1, 2))
            
            shape = "unknown"
            try:
                sides = detect_shape(contour)
                if sides == 3:
                    shape = "triangle"
                elif sides == 4:
                    shape = "rectangle"
                else:
                    shape = "circle"
            except:
                continue
            
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            roi = frame[y1:y2, x1:x2]
            
            if roi.size > 0:
                color = get_dominant_color(roi)
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                cv2.putText(frame, f"{shape} {color}", (x1, y1-20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow('Smart Sorting', frame)
    if cv2.waitKey(1) == 27: 
        break

cap.release()
cv2.destroyAllWindows()