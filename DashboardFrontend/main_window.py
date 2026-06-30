from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
)

from pages.dashboard import dashboardPage
from pages.settings import settingsPage
from pages.logs import logsPage


class mainWindow(QMainWindow):

    #HTML for the Button
    NORMAL_BUTTON_STYLE = """
        QPushButton {
            background: transparent;
            border: none;
            border-radius: 8px;
            text-align: left;
            padding-left: 15px;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #E8E8E8;
        }
    """

    #HTML for the actively selected button
    ACTIVE_BUTTON_STYLE = """
        QPushButton {
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 8px;
            text-align: left;
            padding-left: 15px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0078D7;
        }
    """

    #Defining window initialization
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sensor Dashboard")
        self.resize(1200, 700)

        # Setting up pages and formatting their layout
        self.dashboard_page = dashboardPage()
        self.logs_page = logsPage()
        self.settings_page = settingsPage()
        
        self.pages = QStackedWidget()
        
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.logs_page)
        self.pages.addWidget(self.settings_page)

        # Setting up button
        self.dashboard_button = QPushButton("Dashboard")
        self.logs_button = QPushButton("Logs")
        self.settings_button = QPushButton("Settings")
        
        # Setting up array of buttons to reduce code amount
        self.buttons = [
            self.dashboard_button,
            self.logs_button,
            self.settings_button,
        ]
        
        #Setting up button sizes and styles
        for button in self.buttons:
            button.setFixedSize(140, 42)
            button.setStyleSheet(self.NORMAL_BUTTON_STYLE)

        # Button Connections
        self.dashboard_button.clicked.connect(
            lambda: self.select_page(
                self.dashboard_page,
                self.dashboard_button
            )
        )

        self.logs_button.clicked.connect(
            lambda: self.select_page(
                self.logs_page,
                self.logs_button
            )
        )

        self.settings_button.clicked.connect(
            lambda: self.select_page(
                self.settings_page,
                self.settings_button
            )
        )

        # Sidebar layout and spacing
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setSpacing(10)
        sidebar_layout.addSpacing(20)

        sidebar_layout.addWidget(
            self.dashboard_button,
            alignment=Qt.AlignHCenter
        )

        sidebar_layout.addWidget(
            self.logs_button,
            alignment=Qt.AlignHCenter
        )

        sidebar_layout.addWidget(
            self.settings_button,
            alignment=Qt.AlignHCenter
        )

        sidebar_layout.addStretch()

        sidebar = QWidget()
        sidebar.setFixedWidth(170)
        sidebar.setLayout(sidebar_layout)

        #Side bar styling HTML
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #F7F7F7;
                border-right: 1px solid #D0D0D0;
            }
        """)

        # Main Layout
        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

        # Default page
        self.select_page(
            self.dashboard_page,
            self.dashboard_button
        )
#Function that changes the style of the button if it is selected
    def select_page(self, page, active_button):

        self.pages.setCurrentWidget(page)

        for button in self.buttons:
            button.setStyleSheet(self.NORMAL_BUTTON_STYLE)

        active_button.setStyleSheet(self.ACTIVE_BUTTON_STYLE)