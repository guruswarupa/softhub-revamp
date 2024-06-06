import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt


class SplashScreen(QSplashScreen):
    def __init__(self, image_path):
        super().__init__(QPixmap(image_path))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(500, 300)
        self.move(400, 200)
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.timeout.connect(self.open_main_window)
        self.timer.start(3000)  # 3000 milliseconds (3 seconds)

    def open_main_window(self):
        main_window = MainWindow()
        main_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(800, 600)  # Set the desired size of the main window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen("splash_image.jpg")  # Replace "splash_image.jpg" with your image file path
    splash.show()
    sys.exit(app.exec_())
