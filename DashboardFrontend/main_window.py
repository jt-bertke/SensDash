from PySide6.QtCore import QTimer
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
from pages.utilities.fetcher import(
    ConnectionManager,
    TelemetryManager,
    SimulatedFeed
)


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sensor Dashboard")
        self.resize(1200, 700)
        self.setMinimumSize(1600, 900)

        # --- Shared managers, created once and passed to whatever needs them ---
        self.connection_manager = ConnectionManager()
        self.telemetry_manager = TelemetryManager()

        self.feed = SimulatedFeed(self.telemetry_manager, self.connection_manager)
        self.feed.start()

        # --- Pages ---
        self.dashboard_page = dashboardPage(self.connection_manager, self.telemetry_manager)
        self.liveDataPage = liveDataPage(self.telemetry_manager)
        self.logs_page = logsPage()
        self.settings_page = settingsPage()
        self.aboutPage = aboutPage()

        self.pages = QStackedWidget()
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.liveDataPage)
        self.pages.addWidget(self.logs_page)
        self.pages.addWidget(self.settings_page)
        self.pages.addWidget(self.aboutPage)

        self.Side_Banner = SideBanner(self.connection_manager)

        self.show_dashboard()
        self.Side_Banner.set_active_button(self.Side_Banner.dashboard_button)

        self.Side_Banner.dashboard_clicked.connect(self.show_dashboard)
        self.Side_Banner.livedata_clicked.connect(self.show_livedata)
        self.Side_Banner.logs_clicked.connect(self.show_logs)
        self.Side_Banner.settings_clicked.connect(self.show_settings)
        self.Side_Banner.about_clicked.connect(self.show_about)

        bulk_layout = QHBoxLayout()
        bulk_layout.setContentsMargins(0, 0, 0, 0)
        bulk_layout.setSpacing(0)
        bulk_layout.addWidget(self.Side_Banner)
        bulk_layout.addWidget(self.pages)

        bulk_container = QWidget()
        bulk_container.setLayout(bulk_layout)

        Top_Banner = TopBanner(self.connection_manager)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
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
        self.Side_Banner.set_active_button(self.Side_Banner.dashboard_button)

    def show_livedata(self):
        self.pages.setCurrentWidget(self.liveDataPage)
        self.Side_Banner.set_active_button(self.Side_Banner.livedata_button)

    def show_logs(self):
        self.pages.setCurrentWidget(self.logs_page)
        self.Side_Banner.set_active_button(self.Side_Banner.logs_button)

    def show_settings(self):
        self.pages.setCurrentWidget(self.settings_page)
        self.Side_Banner.set_active_button(self.Side_Banner.settings_button)

    def show_about(self):
        self.pages.setCurrentWidget(self.aboutPage)
        self.Side_Banner.set_active_button(self.Side_Banner.about_button)