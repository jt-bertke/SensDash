from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
)

from pages.dashboard import dashboardPage
from pages.settings import settingsPage
from pages.logs import logsPage
from pages.livedata import liveDataPage
from pages.about import aboutPage
from pages.utilities.cards import (
    TopBanner,
    SideBanner,
)


class mainWindow(QMainWindow):

    #Defining window initialization
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sensor Dashboard")
        self.resize(1600, 800)
        self.setMinimumSize(1600, 800)

        # Setting up pages and formatting their layout
        self.dashboard_page = dashboardPage()
        self.liveDataPage = liveDataPage()
        self.logs_page = logsPage()
        self.settings_page = settingsPage()
        self.aboutPage = aboutPage()
        
        self.pages = QStackedWidget()
        
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.liveDataPage)
        self.pages.addWidget(self.logs_page)
        self.pages.addWidget(self.settings_page)
        self.pages.addWidget(self.aboutPage)

        self.Side_Banner = SideBanner()
        
        self.show_dashboard
        self.Side_Banner.set_active_button(self.Side_Banner.dashboard_button)

        self.Side_Banner.dashboard_clicked.connect(
            self.show_dashboard
        )
        self.Side_Banner.livedata_clicked.connect(
            self.show_livedata
        )
        self.Side_Banner.logs_clicked.connect(
            self.show_logs
        )
        self.Side_Banner.settings_clicked.connect(
            self.show_settings
        )
        self.Side_Banner.about_clicked.connect(
            self.show_about
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
    def show_livedata(self):

        self.pages.setCurrentWidget(self.liveDataPage)
        self.Side_Banner.set_active_button(
            self.Side_Banner.livedata_button
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
    def show_about(self):

        self.pages.setCurrentWidget(self.aboutPage)
        self.Side_Banner.set_active_button(
            self.Side_Banner.about_button
        )