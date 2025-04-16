# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QStatusBar, QTableView, QWidget)

class Ui_GUI(object):
    def setupUi(self, GUI):
        if not GUI.objectName():
            GUI.setObjectName(u"GUI")
        GUI.resize(1000, 807)
        self.centralwidget = QWidget(GUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.OnButton = QPushButton(self.centralwidget)
        self.OnButton.setObjectName(u"OnButton")
        self.OnButton.setGeometry(QRect(10, 10, 88, 27))
        self.PauseButton = QPushButton(self.centralwidget)
        self.PauseButton.setObjectName(u"PauseButton")
        self.PauseButton.setGeometry(QRect(10, 40, 88, 27))
        self.StopButton = QPushButton(self.centralwidget)
        self.StopButton.setObjectName(u"StopButton")
        self.StopButton.setGeometry(QRect(10, 70, 88, 27))
        self.video_frame_1 = QFrame(self.centralwidget)
        self.video_frame_1.setObjectName(u"video_frame_1")
        self.video_frame_1.setGeometry(QRect(730, 40, 251, 171))
        self.video_frame_1.setFrameShape(QFrame.StyledPanel)
        self.video_frame_1.setFrameShadow(QFrame.Raised)
        self.video_frame_2 = QFrame(self.centralwidget)
        self.video_frame_2.setObjectName(u"video_frame_2")
        self.video_frame_2.setGeometry(QRect(730, 220, 251, 171))
        self.video_frame_2.setFrameShape(QFrame.StyledPanel)
        self.video_frame_2.setFrameShadow(QFrame.Raised)
        self.video_frame_3 = QFrame(self.centralwidget)
        self.video_frame_3.setObjectName(u"video_frame_3")
        self.video_frame_3.setGeometry(QRect(730, 400, 251, 171))
        self.video_frame_3.setFrameShape(QFrame.StyledPanel)
        self.video_frame_3.setFrameShadow(QFrame.Raised)
        self.video_label = QLabel(self.centralwidget)
        self.video_label.setObjectName(u"video_label")
        self.video_label.setGeometry(QRect(730, 10, 141, 19))
        self.verticalSlider = QSlider(self.centralwidget)
        self.verticalSlider.setObjectName(u"verticalSlider")
        self.verticalSlider.setGeometry(QRect(30, 220, 16, 160))
        self.verticalSlider.setOrientation(Qt.Vertical)
        self.verticalSlider_2 = QSlider(self.centralwidget)
        self.verticalSlider_2.setObjectName(u"verticalSlider_2")
        self.verticalSlider_2.setGeometry(QRect(80, 220, 16, 160))
        self.verticalSlider_2.setOrientation(Qt.Vertical)
        self.verticalSlider_3 = QSlider(self.centralwidget)
        self.verticalSlider_3.setObjectName(u"verticalSlider_3")
        self.verticalSlider_3.setGeometry(QRect(130, 220, 16, 160))
        self.verticalSlider_3.setOrientation(Qt.Vertical)
        self.verticalSlider_4 = QSlider(self.centralwidget)
        self.verticalSlider_4.setObjectName(u"verticalSlider_4")
        self.verticalSlider_4.setGeometry(QRect(180, 220, 16, 160))
        self.verticalSlider_4.setOrientation(Qt.Vertical)
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(120, 30, 471, 71))
        self.Actual_tool_pose_label = QLabel(self.centralwidget)
        self.Actual_tool_pose_label.setObjectName(u"Actual_tool_pose_label")
        self.Actual_tool_pose_label.setGeometry(QRect(120, 10, 111, 19))
        self.ManualCartButton = QPushButton(self.centralwidget)
        self.ManualCartButton.setObjectName(u"ManualCartButton")
        self.ManualCartButton.setGeometry(QRect(600, 30, 101, 27))
        self.ManualJointButton = QPushButton(self.centralwidget)
        self.ManualJointButton.setObjectName(u"ManualJointButton")
        self.ManualJointButton.setGeometry(QRect(600, 70, 101, 27))
        self.For_manual_label = QLabel(self.centralwidget)
        self.For_manual_label.setObjectName(u"For_manual_label")
        self.For_manual_label.setGeometry(QRect(10, 190, 91, 19))
        self.verticalSlider_5 = QSlider(self.centralwidget)
        self.verticalSlider_5.setObjectName(u"verticalSlider_5")
        self.verticalSlider_5.setGeometry(QRect(230, 220, 16, 160))
        self.verticalSlider_5.setOrientation(Qt.Vertical)
        self.verticalSlider_6 = QSlider(self.centralwidget)
        self.verticalSlider_6.setObjectName(u"verticalSlider_6")
        self.verticalSlider_6.setGeometry(QRect(280, 220, 16, 160))
        self.verticalSlider_6.setOrientation(Qt.Vertical)
        GUI.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(GUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 24))
        GUI.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(GUI)
        self.statusbar.setObjectName(u"statusbar")
        GUI.setStatusBar(self.statusbar)

        self.retranslateUi(GUI)

        QMetaObject.connectSlotsByName(GUI)
    # setupUi

    def retranslateUi(self, GUI):
        GUI.setWindowTitle(QCoreApplication.translate("GUI", u"MainWindow", None))
        self.OnButton.setText(QCoreApplication.translate("GUI", u"On", None))
        self.PauseButton.setText(QCoreApplication.translate("GUI", u"Pause", None))
        self.StopButton.setText(QCoreApplication.translate("GUI", u"Stop", None))
        self.video_label.setText(QCoreApplication.translate("GUI", u"\u0412\u0438\u0434\u0435\u043e \u0441 \u043a\u0430\u043c\u0435\u0440", None))
        self.Actual_tool_pose_label.setText(QCoreApplication.translate("GUI", u"Actual tool pose", None))
        self.ManualCartButton.setText(QCoreApplication.translate("GUI", u"Manual Cart", None))
        self.ManualJointButton.setText(QCoreApplication.translate("GUI", u"Manual Joint", None))
        self.For_manual_label.setText(QCoreApplication.translate("GUI", u"For Manual", None))
    # retranslateUi