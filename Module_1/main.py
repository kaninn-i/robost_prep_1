
import os
print('Path main ------------',os.getcwd())

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from gui_main import Ui_GUI  # Импорт сгенерированного класса

from motion.core import RobotControl


# rc = RobotControl()
# print('----------------', rc.getActualStateOut())


# print(rc.connect())
# rc.__toolOFF()
# rc.engage()

# print('Robot state:', rc.getRobotState())
# print('Robot mode:', rc.getRobotMode())
# rc.moveToPointL(waypoint_list=[12,12,23])
# print(rc.moveToPointL())

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_GUI()
#         self.ui.setupUi(self)  # Критически важная строка!


# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()  # Не забыть показать окно!
# sys.exit(app.exec())


import time

# Создание объекта робота
robot = RobotControl()  # IP и порт по умолчанию

# Подключение к роботу
if not robot.connect():
    print("Ошибка подключения!")
    exit(1)

# Активация двигателей
if not robot.engage():
    print("Не удалось активировать моторы")
    exit(1)

# # Создание точек для движения
# start_point = Waypoint(
#     coordinates=[0.0, 0.0, 0.5, 0.0, 0.0, 0.0],  # x,y,z,rx,ry,rz
#     smoothing_factor=0.2
# )

# target_point = Waypoint(
#     coordinates=[0.4, -0.2, 0.3, 1.57, 0.0, 0.0],
#     smoothing_factor=0.3
# )

try:
    robot.reset()
    # Переход в начальную позицию
    robot.moveToStart()
    
    # Линейное движение к целевой точке
    robot.moveToPointL(
        waypoints=[[180, 180, 0, 0.0, 0.0, 0.0], [200, 150, 0, 0.0, 0.0, 0.0]],
        tool_state=0,  # инструмент выключен
        velocity=1,   # 50% от максимальной скорости
        acceleration=0.3
    )
    
    # Запуск движения
    robot.play()
    
    # Мониторинг состояния
    while robot.getRobotState() != robot.PROGRAM_IS_DONE_S:
        print(f"Текущая позиция: {robot.getToolPosition()}")
        print(f"Температура моторов: {robot.getActualTemperature()}")
        time.sleep(0.5)
        
except Exception as e:
    print(f"Ошибка: {str(e)}")
finally:
    # Остановка и отключение
    robot.stop()
    robot.disengage()
    print("Робот отключен")