from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QScrollArea, QPushButton, QLabel,QFrame,QGridLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import json
from app_widget import AppWidget
from app_detail_window import AppDetailWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Softhub")
        self.setWindowIcon(QIcon(r"images\softhubicon.png"))
        self.set_screen_resolution()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.set_dark_mode()

        # Create horizontal layout for main window
        main_layout = QHBoxLayout(central_widget)

        # Create sidebar widget
        self.sidebar_widget = QListWidget()
        self.populate_sidebar(self.sidebar_widget)
        self.sidebar_widget.setStyleSheet("background-color: #f2f2f2; border-right: 1px solid #ccc;")
        main_layout.addWidget(self.sidebar_widget, 1)  # Set sidebar to take up 20% of the width

        # Create scroll area for main content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create main content widget and set it as the widget for the scroll area
        self.main_content_widget = QWidget()
        self.scroll_area.setWidget(self.main_content_widget)

        main_layout.addWidget(self.scroll_area, 5)  # Main content takes up 80% of the width

        # Add layout to main content widget
        self.main_content_layout = QVBoxLayout(self.main_content_widget)
        
        # Dictionary to hold category frames
        self.category_frames = {}
        
        # Create category frames
        self.create_category_frames()

        # Connect sidebar item click to scroll function
        self.sidebar_widget.itemClicked.connect(self.scroll_to_category)

    def set_dark_mode(self):
        dark_style = """
        QWidget {
            background-color: #2E2E2E;
            color: #FFFFFF; /* Set text color to white */
        }
        QPushButton {
            background-color: #4A4A4A;
            border: none;
            color: #FFFFFF;
            padding: 10px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #5A5A5A;
        }
        QPushButton:pressed {
            background-color: #3A3A3A;
        }
        QListWidget {
            background-color: #1E1E1E;
            color: #FFFFFF; /* Set text color to white */
            border-right: 1px solid #444444;
        }
        QFrame {
            background-color: #2E2E2E;
            color: #FFFFFF; /* Set text color to white */
        }
        QLabel {
            color: #FFFFFF; /* Set text color to white */
        }
        """
        self.setStyleSheet(dark_style)


    def set_screen_resolution(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        self.resize(screen_geometry.width(), screen_geometry.height() - 78)
        self.move(0, 0)

    def populate_sidebar(self, sidebar_widget):
        # Load app information from database file (e.g., JSON)
        with open("app_data.json", "r") as file:
            app_data = json.load(file)

        # Extract unique categories from app data and sort them
        categories = sorted(set(app_info["category"] for app_info in app_data))

        # Add categories to the sidebar
        sidebar_widget.addItems(categories)


    def create_category_frames(self):
        # Load app information from database file (e.g., JSON)
        with open("app_data.json", "r") as file:
            app_data = json.load(file)

        # Extract unique categories from app data
        categories = sorted(set(app_info["category"] for app_info in app_data))

        # Create category frames
        for category in categories:
            category_frame = QFrame()  # Create a frame for the category
            category_frame.setObjectName(category.replace(" ", "_"))  # Set object name for category frame
            category_frame_layout = QVBoxLayout(category_frame)  # Create a layout for the frame
            category_frame_layout.setContentsMargins(10, 10, 10, 10)  # Add margins to provide spacing

            # Create a label for the category
            category_label = QLabel(category)
            category_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Left align category label at the top
            category_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #333;")  # Set font style and color
            category_frame_layout.addWidget(category_label)

            # Add some margin below the category label
            category_frame_layout.addSpacing(10)

            # Filter apps for the current category and sort them
            category_apps = [app_info for app_info in app_data if app_info["category"] == category]
            category_apps = sorted(category_apps, key=lambda x: x["name"])  # Sort apps by name

            # Create a grid layout for the app widgets
            apps_layout = QGridLayout()
            apps_layout.setSpacing(10)  # Add spacing between app widgets

            # Populate apps for the current category
            row = 0
            col = 0
            for app_info in category_apps:
                # Create an app widget with icon and name
                app_icon = app_info.get("icon")
                app_name = app_info.get("name")
                app_widget = QPushButton()
                app_widget.setIcon(QIcon(app_icon))  # Set icon
                app_widget.setIconSize(QSize(64, 64))  # Set icon size
                app_widget.setStyleSheet(
                    "QPushButton { border: 1px solid #ccc; border-radius: 5px; background-color: #fff; padding: 10px; }"
                    "QPushButton::text { margin-left: 25px; }"  # Add spacing between icon and text
                    "QPushButton:hover { background-color: #f0f0f0; }"
                )  # Set style for app widget
                app_widget.setFixedSize(220, 120)  # Set fixed size for app widget
                app_widget.setText(app_name)  # Set app name as text
                app_widget.clicked.connect(lambda _, info=app_info: self.show_app_detail(info))  # Connect the clicked signal to show_app_detail slot
                apps_layout.addWidget(app_widget, row, col)  # Add app widget to the layout
                col += 1
                if col == 5:
                    col = 0
                    row += 1

            # Add the apps layout to the category frame layout
            category_frame_layout.addLayout(apps_layout)

            # Add category frame to the dictionary
            self.category_frames[category] = category_frame

            # Add the category frame to the main content layout
            self.main_content_layout.addWidget(category_frame)


    def scroll_to_category(self, item):
        # Find the category frame associated with the clicked category
        category_name = item.text()
        if category_name in self.category_frames:
            category_frame = self.category_frames[category_name]

            # Calculate the position to scroll to
            scroll_pos = category_frame.geometry().top()

            # Scroll the main content area to make the category frame visible
            self.scroll_area.verticalScrollBar().setValue(scroll_pos)



    def show_app_detail(self, app_info):
        icon_path = app_info.get("icon")
        description = app_info.get("description")
        package_name = app_info.get("package")
        app_name = app_info.get("name")  # Get app name from app_info

        app_detail_window = AppDetailWindow(app_name, icon_path, description, package_name, parent=self)
        app_detail_window.show()


# If you want to test the application
if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())