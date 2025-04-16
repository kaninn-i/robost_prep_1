import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from gui_main import Ui_GUI  # Импорт сгенерированного класса

def connect():
    pass

def engage():
    pass

def disengage():
    pass

def manualCartMode():
    pass

def manuaJointMode():
    pass

def setJointVelocity():
    pass

def setCartesianVelocity():
    pass

def moveToStart():
    pass

def activateMoveToStart():
    pass

def moveToPointL():
    pass

def moveToPointC():
    pass

def moveToPointJ():
    pass

def play():
    pass

def pause():
    pass

def stop():
    pass

def reset():
    pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GUI()
        self.ui.setupUi(self)  # Критически важная строка!


app = QApplication(sys.argv)
window = MainWindow()
window.show()  # Не забыть показать окно!
sys.exit(app.exec())