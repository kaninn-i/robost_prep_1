import cv2
import numpy as np

# Инициализация камеры
cap = cv2.VideoCapture(0)

# Создание окна с ползунками
cv2.namedWindow('Settings')
cv2.resizeWindow('Settings', 840, 680)

# Создание трекбаров
cv2.createTrackbar('Color', 'Settings', 0, 5, lambda x: None)  # 0-5 соответствуют цветам
cv2.createTrackbar('S_min', 'Settings', 100, 255, lambda x: None)
cv2.createTrackbar('S_max', 'Settings', 255, 255, lambda x: None)
cv2.createTrackbar('V_min', 'Settings', 100, 255, lambda x: None)
cv2.createTrackbar('V_max', 'Settings', 255, 255, lambda x: None)
cv2.createTrackbar('Blur', 'Settings', 9, 30, lambda x: None)
cv2.createTrackbar('Erode', 'Settings', 1, 5, lambda x: None)
cv2.createTrackbar('Dilate', 'Settings', 2, 5, lambda x: None)
cv2.createTrackbar('Min Area', 'Settings', 500, 5000, lambda x: None)

# Цвета и их HSV-диапазоны (H-диапазоны)
COLOR_RANGES = {
    0: {'name': 'Red',    'h': [(0, 10), (170, 180)]},
    1: {'name': 'Green',  'h': [(35, 85)]},
    2: {'name': 'Blue',   'h': [(90, 120)]},
    3: {'name': 'Yellow', 'h': [(20, 35)]},
    4: {'name': 'Orange', 'h': [(10, 20)]},
    5: {'name': 'Purple', 'h': [(120, 150)]}
}

def get_trackbars():
    return {
        'color': cv2.getTrackbarPos('Color', 'Settings'),
        's_min': cv2.getTrackbarPos('S_min', 'Settings'),
        's_max': cv2.getTrackbarPos('S_max', 'Settings'),
        'v_min': cv2.getTrackbarPos('V_min', 'Settings'),
        'v_max': cv2.getTrackbarPos('V_max', 'Settings'),
        'blur': cv2.getTrackbarPos('Blur', 'Settings') | 1,
        'erode': cv2.getTrackbarPos('Erode', 'Settings'),
        'dilate': cv2.getTrackbarPos('Dilate', 'Settings'),
        'min_area': cv2.getTrackbarPos('Min Area', 'Settings')
    }

while True:
    ret, frame = cap.read()
    if not ret:
        break

    params = get_trackbars()
    color_info = COLOR_RANGES[params['color']]
    
    # Фильтрация шума
    blur_size = params['blur']
    blurred = cv2.GaussianBlur(frame, (blur_size, blur_size), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # Создание маски для выбранного цвета
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for h_range in color_info['h']:
        lower = np.array([h_range[0], params['s_min'], params['v_min']])
        upper = np.array([h_range[1], params['s_max'], params['v_max']])
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))

    # Морфологические операции
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=params['erode'])
    mask = cv2.dilate(mask, kernel, iterations=params['dilate'])

    # Поиск контуров
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = frame.copy()
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < params['min_area']:
            continue
            
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.drawContours(contour_img, [approx], -1, (0, 255, 0), 2)

    # Добавляем текст с названием цвета
    color_text = f"{color_info['name']} (H: {color_info['h']})"
    cv2.putText(frame, color_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Собираем изображения для отображения
    debug_images = [
        ("Original", frame),
        ("HSV Mask", mask),
        ("Processed Mask", cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)),
        ("Contours", contour_img)
    ]

    # Создаем сетку изображений
    grid = []
    for title, img in debug_images:
        resized = cv2.resize(img, (320, 240))
        if len(resized.shape) == 2:
            resized = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
        grid.append(resized)
        
    combined = np.vstack([np.hstack(grid[:2]), np.hstack(grid[2:])])
    
    cv2.imshow('Debug View', combined)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()