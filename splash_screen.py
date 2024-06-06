from PyQt5.QtWidgets import QSplashScreen, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
from main_window import MainWindow

class SplashScreen(QSplashScreen):
    def __init__(self, image_path):
        super().__init__(QPixmap(image_path))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(1024, 512)
        self.center_splash_window()
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.timeout.connect(self.open_main_window)
        self.timer.start(3000)

    def open_main_window(self):
        self.timer.stop()
        self.main_window = MainWindow()  # Keep a reference to the main window
        self.main_window.show()

    def center_splash_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        center_point = screen_geometry.center()
        top_left_point = center_point - self.rect().center()
        self.move(top_left_point)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    splash = SplashScreen(r"images\softhub load dark.png")
    splash.show()
    sys.exit(app.exec_())
