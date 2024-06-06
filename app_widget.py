from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDialog, QVBoxLayout, QMessageBox, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

class AppWidget(QWidget):
    clicked = pyqtSignal()  # Define the clicked signal

    def __init__(self, icon_path, name, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.name = name

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add icon label
        icon_label = QLabel()
        pixmap = QPixmap(self.icon_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Add name label
        name_label = QLabel(self.name)
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        # Set layout for the widget
        self.setLayout(layout)

        # Set style sheet for widget and labels
        self.setStyleSheet("""
            QWidget {
                border: 1px solid #ccc;
                padding: 10px;
                margin: 5px;
                max-width: 150px; /* Limit width of widget */
            }
            QLabel {
                margin-left: 10px;
            }
        """)

        # Set cursor to hand pointer
        self.setCursor(Qt.PointingHandCursor)

        # Connect mousePressEvent to emit clicked signal
        self.mousePressEvent = self.emit_clicked

    def emit_clicked(self, event):
        self.clicked.emit()  # Emit the clicked signal when the widget is clicked
