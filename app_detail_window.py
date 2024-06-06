import subprocess
import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class PackageOperationThread(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, operation, packman, package_name):
        super().__init__()
        self.operation = operation
        self.packman = packman
        self.package_name = package_name

    def run(self):
        if self.operation == "install":
            self.install_package()
        elif self.operation == "uninstall":
            self.uninstall_package()
        elif self.operation == "update":
            self.update_package()
        elif self.operation == "check_installed":
            self.check_installed_status()

    def install_package(self):
        try:
            subprocess.run(["winget", "install", "--id", self.package_name], check=True)
            self.finished.emit(True)
        except subprocess.CalledProcessError:
            self.finished.emit(False)

    def uninstall_package(self):
        try:
            subprocess.run(["winget", "uninstall", "--id", self.package_name], check=True)
            self.finished.emit(True)
        except subprocess.CalledProcessError:
            self.finished.emit(False)

    def update_package(self):
        try:
            subprocess.run(["winget", "upgrade", "--id", self.package_name], check=True)
            self.finished.emit(True)
        except subprocess.CalledProcessError:
            self.finished.emit(False)

    def check_installed_status(self):
        try:
            result = subprocess.run(["winget", "list"], capture_output=True, text=True)
            installed_packages = result.stdout.splitlines()
            is_installed = any(self.package_name in package for package in installed_packages)
            self.finished.emit(is_installed)
        except subprocess.CalledProcessError:
            self.finished.emit(False)

class AppDetailWindow(QDialog):
    def __init__(self, app_name, icon_path, description, package_name, packman, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.description = description
        self.package_name = package_name
        self.app_name = app_name
        self.packman = packman

        self.init_ui()
        self.check_installed_status()  # Check if the app is installed during initialization

    def init_ui(self):
        self.setWindowTitle(self.app_name)
        self.setWindowIcon(QIcon(self.icon_path))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # Remove help button

        layout = QVBoxLayout()

        # Add icon label
        icon_label = QLabel()
        pixmap = QPixmap(self.icon_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Add description label
        desc_label = QLabel(self.description)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Add buttons for install, uninstall, and update
        self.install_button = QPushButton("Install")
        self.uninstall_button = QPushButton("Uninstall")
        self.update_button = QPushButton("Update")

        self.install_button.clicked.connect(self.install_app)
        self.uninstall_button.clicked.connect(self.uninstall_app)
        self.update_button.clicked.connect(self.update_app)

        layout.addWidget(self.install_button)
        layout.addWidget(self.uninstall_button)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def check_installed_status(self):
        self.thread = PackageOperationThread("check_installed", self.packman, self.package_name)
        self.thread.finished.connect(self.on_package_check_finished)
        self.thread.start()

    def on_package_check_finished(self, is_installed):
        if is_installed:
            self.install_button.setText("Installed")
            self.install_button.setEnabled(False)
            self.uninstall_button.setEnabled(True)
            self.update_button.setEnabled(True)
        else:
            self.install_button.setText("Install")
            self.install_button.setEnabled(True)
            self.uninstall_button.setEnabled(False)
            self.update_button.setEnabled(False)

    def install_app(self):
        self.thread = PackageOperationThread("install", self.packman, self.package_name)
        self.thread.finished.connect(self.on_operation_finished)
        self.thread.start()

    def uninstall_app(self):
        self.thread = PackageOperationThread("uninstall", self.packman, self.package_name)
        self.thread.finished.connect(self.on_operation_finished)
        self.thread.start()

    def update_app(self):
        self.thread = PackageOperationThread("update", self.packman, self.package_name)
        self.thread.finished.connect(self.on_operation_finished)
        self.thread.start()

    def on_operation_finished(self, success):
        if success:
            QMessageBox.information(self, "Success", "Operation completed successfully.")
            self.check_installed_status()
        else:
            QMessageBox.critical(self, "Error", "Operation failed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppDetailWindow("Example App", "path/to/icon.png", "This is an example app.", "example-app-id", "winget")
    window.show()
    sys.exit(app.exec_())
