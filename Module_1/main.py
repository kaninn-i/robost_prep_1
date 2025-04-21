
import os, math
print('Path main ------------',os.getcwd())
from time import sleep
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from gui_main import Ui_GUI  # Импорт сгенерированного класса

from motion.core import RobotControl
from motion.robot_control.motion_program import Waypoint


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

# print(robot.getToolPosition())

# print(robot.getRobotMode())
# robot.manualCartMode()
# print(robot.getRobotMode())

# # Создание точек для движения
# start_point = Waypoint(
#     coordinates=[0.0, 0.0, 0.5, 0.0, 0.0, 0.0],  # x,y,z,rx,ry,rz
#     smoothing_factor=0.2
# )

# target_point = Waypoint(
#     coordinates=[0.4, -0.2, 0.3, 1.57, 0.0, 0.0],
#     smoothing_factor=0.3
# )

# try:
robot.reset()
degrees = [math.degrees(el) for el in robot.getToolPosition()]
print(degrees)

# Переход в начальную позицию
# robot.moveToStart()
# robot.activateMoveToStart()

# # Линейное движение к целевой точке
# robot.manualCartMode()
# sleep(1)
robot.moveToStart()
# sleep(1)
robot.moveToPointL(
    # waypoint_list=[[180, 180, 0, 0.0, 0.0, 0.0], [200, 200, 0, 0.0, 0.0, 0.0]],
    # waypoint_list=Waypoint([200, 200, 0, 0.0, 0.0, 0.0]),
    waypoint_list=[[200, 200, 0, 0.0, 0.0, 0.0]],
    tool=0,  # инструмент выключен
    velocity=0.5,   # 50% от максимальной скорости
    acceleration=0.3
)

# # Запуск движения
robot.play()
    
#     # Мониторинг состояния
#     while robot.getRobotState() != robot.PROGRAM_IS_DONE_S:
#         print(f"Текущая позиция: {robot.getToolPosition()}")
#         print(f"Температура моторов: {robot.getActualTemperature()}")
#         time.sleep(0.5)
        
# except Exception as e:
#     print(f"Ошибка: {str(e)}")
# finally:
#     # Остановка и отключение
#     robot.stop()
#     robot.disengage()
#     print("Робот отключен")