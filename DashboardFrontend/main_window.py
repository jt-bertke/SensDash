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
from pages.utilities.cards import (
    TopBanner,
    SideBanner,
)


class mainWindow(QMainWindow):

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

        self.Side_Banner = SideBanner()
        self.show_dashboard
        self.Side_Banner.set_active_button(self.Side_Banner.dashboard_button)
        self.Side_Banner.dashboard_clicked.connect(
            self.show_dashboard
        )
        self.Side_Banner.logs_clicked.connect(
            self.show_logs
        )
        self.Side_Banner.settings_clicked.connect(
            self.show_settings
        )

        # Main Layout
        bulk_layout = QHBoxLayout()

        bulk_layout.setContentsMargins(0, 0, 0, 0)
        bulk_layout.setSpacing(0)

        bulk_layout.addWidget(self.Side_Banner)
        bulk_layout.addWidget(self.pages)

        bulk_container = QWidget()
        bulk_container.setLayout(bulk_layout)

        #Setting up top banner
        Top_Banner = TopBanner()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_layout.addWidget(Top_Banner)
        main_layout.addWidget(bulk_container)

        container = QWidget()
        container.setStyleSheet("""
            background-color: #11161D;
            border-right: red;
        """)
        container.setLayout(main_layout)

        self.setCentralWidget(container)
    
    def show_dashboard(self):

        self.pages.setCurrentWidget(self.dashboard_page)
        self.Side_Banner.set_active_button(
            self.Side_Banner.dashboard_button
        )
    def show_logs(self):

        self.pages.setCurrentWidget(self.logs_page)
        self.Side_Banner.set_active_button(
            self.Side_Banner.logs_button
        )
    def show_settings(self):
        
        self.pages.setCurrentWidget(self.settings_page)
        self.Side_Banner.set_active_button(
            self.Side_Banner.settings_button
        )