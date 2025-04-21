from core import RobotControl  # импортируй свой файл с классом, если он в другом месте — укажи путь
from robot_control.motion_program import Waypoint
from time import sleep
from math import radians
# IP = '192.168.88.105' 
# IP = 'manipulator.local' 
IP = '192.168.2.55'
# 1. Инициализация робота и подключение
robot = RobotControl(ip = IP)
# a, b = robot.connect()
# if not a:
if not robot.connect():
    print("❌ Не удалось подключиться к роботу")
    exit()
robot.connect()
# 2. Включаем ручной режим и активируем привод
# print(b.getPar)ameterTree())
robot.engage()
robot.manualJointMode()
sleep(1)
robot.setJointVelocity([0.1, 0.0, 0.0, 0.0, 0.0, 0.0])
# a =robot.getToolPosition()
# robot._RobotControl__robot.semiAutoMode()

# 3. Сохраняем текущую позицию как стартовую
# robot.start_position = robot._RobotControl__robot.getActualJointPosition()
# print("✅ Стартовая позиция сохранена")

# 4. Создаём цель — список из одного или нескольких Waypoint
# ⚠️ Эти значения должны быть допустимыми углами сочленений для твоего робота
target_position = Waypoint([radians(0), radians(-45), radians(90), radians(0), radians(90), radians(0)])
robot.moveToPointJ([target_position])  # moveJ = суставное движение
robot.play()

# 5. Ждём окончания движения
sleep(3)

# 6. Возвращаемся на стартовую позицию
robot.moveToStart()
robot.play()

sleep(3)

# 7. Выключаем привод
robot.disengage()
print("🚀 Сценарий завершён")