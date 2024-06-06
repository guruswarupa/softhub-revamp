# first_time_window.py

import json
import subprocess
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QCheckBox, QWidget , QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import threading

class FirstTimeWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to Softhub")
        self.setFixedSize(1024, 512)
        self.settings = self.load_settings()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # First Screen
        self.first_screen = QWidget()
        self.first_screen_layout = QVBoxLayout()
        self.first_screen.setLayout(self.first_screen_layout)

        app_image = QLabel()
        app_image.setPixmap(QPixmap("images/softhub.png").scaled(1024, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        app_image.setAlignment(Qt.AlignCenter)
        self.first_screen_layout.addWidget(app_image)

        self.stacked_widget.addWidget(self.first_screen)

        # Second Screen
        self.second_screen = QWidget()
        self.second_screen_layout = QVBoxLayout()
        self.second_screen.setLayout(self.second_screen_layout)

        info_label = QLabel("Softhub is a comprehensive software management tool.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Arial", 16))  # Set font size
        self.second_screen_layout.addWidget(info_label)

        self.stacked_widget.addWidget(self.second_screen)

        # Third Screen
        self.third_screen = QWidget()
        self.third_screen_layout = QVBoxLayout()
        self.third_screen.setLayout(self.third_screen_layout)

        package_label = QLabel("Select package managers to install:")
        package_label.setAlignment(Qt.AlignCenter)
        package_label.setFont(QFont("Arial", 16))  # Set font size
        self.third_screen_layout.addWidget(package_label)

        self.package_checkboxes = {
            "winget": QCheckBox("Winget"),
            "chocolatey": QCheckBox("Chocolatey"),
            "scoop": QCheckBox("Scoop")
        }

        for checkbox in self.package_checkboxes.values():
            checkbox.setChecked(self.settings.get("package_managers", {}).get(checkbox.text(), False))
            self.third_screen_layout.addWidget(checkbox)

        self.stacked_widget.addWidget(self.third_screen)

        # Fourth Screen
        self.fourth_screen = QWidget()
        self.fourth_screen_layout = QVBoxLayout()
        self.fourth_screen.setLayout(self.fourth_screen_layout)

        auto_update_label = QLabel("Would you like to enable auto-update?")
        auto_update_label.setAlignment(Qt.AlignCenter)
        auto_update_label.setFont(QFont("Arial", 16))  # Set font size
        self.fourth_screen_layout.addWidget(auto_update_label)

        self.auto_update_checkbox = QCheckBox("Enable auto-update")
        self.auto_update_checkbox.setChecked(self.settings.get("auto_update", False))
        self.fourth_screen_layout.addWidget(self.auto_update_checkbox)

        self.stacked_widget.addWidget(self.fourth_screen)

        # Navigation buttons
        self.navigation_layout = QHBoxLayout()
        layout.addLayout(self.navigation_layout)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.previous_page)
        self.navigation_layout.addWidget(self.back_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.navigation_layout.addWidget(self.next_button)

        self.finish_button = QPushButton("Finish")
        self.finish_button.clicked.connect(self.finish_setup)
        self.navigation_layout.addWidget(self.finish_button)
        self.finish_button.hide()

        self.update_navigation_buttons()

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_settings(self, settings):
        with open("settings.json", "w") as file:
            json.dump(settings, file, indent=4)

    def next_page(self):
        current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_index + 1)
        self.update_navigation_buttons()

    def previous_page(self):
        current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex(current_index - 1)
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        current_index = self.stacked_widget.currentIndex()
        self.back_button.setVisible(current_index > 0)
        self.next_button.setVisible(current_index < self.stacked_widget.count() - 1)
        self.finish_button.setVisible(current_index == self.stacked_widget.count() - 1)

    def finish_setup(self):
        selected_packages = [name for name, checkbox in self.package_checkboxes.items() if checkbox.isChecked()]
        auto_update_enabled = self.auto_update_checkbox.isChecked()
        self.install_packages(selected_packages)
        self.settings["package_managers"] = {checkbox.text(): checkbox.isChecked() for checkbox in self.package_checkboxes.values()}
        self.settings["auto_update"] = auto_update_enabled
        self.save_settings(self.settings)
        self.accept()

    def install_packages(self, packages):
        def install_package(package):
            if package == "winget":
                try:
                    self.run_command("powershell -Command (New-Object Net.WebClient).DownloadFile('https://github.com/microsoft/winget-cli/releases/latest/download/Winget.exe', 'Winget.exe')")
                except subprocess.CalledProcessError as e:
                    print(f"Error downloading Winget: {e}")

        # Create and start a thread for each package installation
        threads = []
        for package in packages:
            thread = threading.Thread(target=install_package, args=(package,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def run_command(self, command):
        subprocess.run(command, shell=True, check=True)


# If you want to test the FirstTimeWindow
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FirstTimeWindow()
    window.show()
    sys.exit(app.exec_())

