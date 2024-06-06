import sys
from PyQt5.QtWidgets import QApplication
from splash_screen import SplashScreen
from main_window import MainWindow
from no_internet_window import NoInternetWindow
from first_time_window import FirstTimeWindow
import json
import os

def main():
    app = QApplication(sys.argv)
    
    # Check if it's the first time running
    if not os.path.isfile("settings.json"):
        show_first_time_setup()
    else:
        # Check internet connection
        if NoInternetWindow.internet_stat():
            splash = SplashScreen(r"images\softhub load dark.png")
            splash.show()
        else:
            no_internet_window = NoInternetWindow()
            no_internet_window.show()
    
    sys.exit(app.exec_())

def show_first_time_setup():
    app = QApplication(sys.argv)
    first_time_window = FirstTimeWindow()
    if first_time_window.exec_() == FirstTimeWindow.Accepted:
        # Proceed with the application launch
        if NoInternetWindow.internet_stat():
            splash = SplashScreen(r"images\softhub load dark.png")
            splash.show()
        else:
            no_internet_window = NoInternetWindow()
            no_internet_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
