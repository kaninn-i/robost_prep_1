import sys
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel 
from gui_main import Ui_GUI  # Импорт сгенерированного класса
import cv2
import numpy as np
from ultralytics import YOLO

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_GUI()
    self.ui.setupUi(self)
    self.model = self.load_yolo_model(model_path=r'C:\Users\Илья\Documents\GitHub\robost_prep_1\runs\detect\new_df_objects_detection_v1_5ep\weights\best.pt')
    
    # self.init_buttons()
    # self.init_tables()
    # self.init_cv()
    
  # def init_buttons(self):
    # кнопки
    self.ui.OnButton.clicked.connect(self.OnButton_toggle)
    self.ui.StopButton.clicked.connect(self.StopButton_toggle)
    self.ui.PauseButton.clicked.connect(self.PauseButton_toggle)
    
  # def init_tables(self):
    # pass
  
  # def init_cv(self):
    # --- камеры и прилегающие переменные ---
    self.cap = cv2.VideoCapture(0)  # 0 - индекс камеры по умолчанию
    
    # Создаем QLabel для отображения видео внутри QFrame
    self.video_label1 = QLabel(self.ui.video_frame_1)
    self.video_label2 = QLabel(self.ui.video_frame_2)
    self.video_label3 = QLabel(self.ui.video_frame_3)
    
    # Настраиваем размеры и выравнивание
    for label in [self.video_label1, self.video_label2, self.video_label3]:
      label.setAlignment(Qt.AlignCenter)
      label.setMinimumSize(QSize(251, 171))
      label.setScaledContents(True)
    
    # Таймер для обновления кадров
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_frames)
    self.timer.start(30)  # 30 ms (≈33 FPS)
  
  # ------------------------- кнопки, общий интерфейс 
  def OnButton_toggle(self):
    '''Кнопка On (включения)'''
    print('OnButton is clicked')
    self.ui.lineEdit.changeC("Active" if self.ui.lineEdit.text() == "Stopped" else "Stopped")
    
  def StopButton_toggle(self):
    '''Кнопка Stop (остановки)'''
    print('StopButton is clicked')
    
  def PauseButton_toggle(self):
    '''Кнопка Pause (пауза)'''
    print('PauseButton is clicked')
  
  # ------------------------- камеры -------------------------
  def load_yolo_model(self, model_path):
    '''Загрузка YOLO модели'''
    try:
        model = YOLO(model_path)
        print(f"Модель {model_path} успешно загружена!")
        return model
    except Exception as e:
        print(f"Ошибка загрузки модели: {e}")
        return None
  
  def update_frames(self):
    '''Функция для отображения картинки'''
    # Читаем кадр с камеры
    ret, frame = self.cap.read()
    if not ret:
        return

    # Оригинальное изображение для первого фрейма
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Обработка для второго фрейма (контуры)
    processed_frame = self.detect_contours(frame)
    
    # Обработка для третьего фрейма (YOLO)
    yolo_frame = self.detect_objects(frame.copy()) if self.model else frame
    
    # Обновляем все три фрейма
    self.update_single_frame(self.video_label1, rgb_image)
    self.update_single_frame(self.video_label2, processed_frame)
    self.update_single_frame(self.video_label3, yolo_frame)
    
  def detect_objects(self, frame):
    '''Детекция объектов с помощью YOLO'''
    results = self.model(frame, verbose=False)
    
    # Визуализация результатов
    annotated_frame = results[0].plot()
    
    # Конвертация цветового пространства
    return cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    
  def detect_contours(self, frame):
    '''контуры'''
    # Конвертация в grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Размытие для уменьшения шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Обнаружение краев методом Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Поиск контуров
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Создаем копию оригинального кадра для рисования
    contour_frame = frame.copy()

    # Рисуем контуры зеленым цветом
    cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)

    # Конвертируем обратно в RGB для отображения в Qt
    return cv2.cvtColor(contour_frame, cv2.COLOR_BGR2RGB)
    
  def update_single_frame(self, label, image):
      '''Конвертация и масштабирование изображения'''
      h, w, ch = image.shape
      bytes_per_line = ch * w
      qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
      
      scaled_image = qt_image.scaled(
          label.size(), 
          Qt.AspectRatioMode.KeepAspectRatio,
          Qt.TransformationMode.SmoothTransformation
      )
      
      label.setPixmap(QPixmap.fromImage(scaled_image))


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())