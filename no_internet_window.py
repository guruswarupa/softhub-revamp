# no_internet_window.py

import sys
from PyQt5.QtWidgets import QDialog, QLabel, QApplication, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

class NoInternetWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        app_width = 1024
        app_height = 512

        screen = QApplication.primaryScreen().geometry()
        screenwidth = screen.width()
        screenheight = screen.height()

        x = (screenwidth / 2) - (app_width / 2)
        y = (screenheight / 2) - (app_height / 2)

        self.setGeometry(int(x), int(y), app_width, app_height)

        layout = QVBoxLayout()

        bg_image1 = QPixmap(r"images/noconnection.png")
        label2 = QLabel()
        label2.setPixmap(bg_image1)
        layout.addWidget(label2)

        self.setLayout(layout)

        self.mousePressEvent = self.mouse_press_event

    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.close()
        elif event.button() == Qt.RightButton:
            self.check_internet_and_act()

    def check_internet_and_act(self):
        if self.internet_stat():
            self.close()
            if self.parent():
                self.parent().show_main()
        else:
            self.show()

    @staticmethod
    def internet_stat(url="https://www.google.com/", timeout=3):
        try:
            r = requests.head(url=url, timeout=timeout)
            return True
        except requests.exceptions.ConnectionError:
            return False
