import sys
from PyQt5.QtWidgets import QApplication
from splash_screen import SplashScreen
from main_window import MainWindow
from no_internet_window import NoInternetWindow
import json
import os

def main():
    app = QApplication(sys.argv)

    if NoInternetWindow.internet_stat():
        splash = SplashScreen(r"images\softhub load dark.png")
        splash.show()
    else:
        no_internet_window = NoInternetWindow()
        no_internet_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
