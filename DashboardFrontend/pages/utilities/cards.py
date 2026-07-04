from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)

from PySide6.QtGui import(
    QPixmap
)
from PySide6.QtCore import (
    Qt,
    Signal,
)
import qtawesome as qta

class sensorCard(QWidget):

    def __init__(self, title, value, units):
        super().__init__()

        frame = QFrame()
        frame.setObjectName("SensorCard")
        frame.setStyleSheet("""
            #SensorCard {
                background-color: #1A222C;
                border: 1px solid #273341;
                border-radius: 12px;
            }             
        """)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            color: #A6B2C2;
            font-size:14px;                           
        """)
        
        self.value_label = QLabel(str(value))
        self.value_label.setStyleSheet("""
            color:white;
            font-size:38px;
            font-weight:bold;                      
        """)
        
        self.units_label = QLabel(units)
        self.units_label.setStyleSheet("""
            color:#3B82F6;
            font-size:14px;
            font-weight:bold;                               
        """)

        frame_layout = QVBoxLayout()

        frame_layout.addWidget(self.title_label)
        frame_layout.addWidget(self.value_label)
        frame_layout.addWidget(self.units_label)

        frame.setLayout(frame_layout)

        main_layout = QVBoxLayout()

        main_layout.addWidget(frame)

        self.setLayout(main_layout)

class TopBanner(QFrame):

    def __init__(self):
        super().__init__()

        #Main layout for the banner
        layout = QHBoxLayout()
        self.setFixedHeight(45)

        #Setting up banner logo using pixmap
        self.logo = QLabel()
        logo_icon = qta.icon("ph.gauge-bold", color="#FFFFFF")
        logo_pixmap = logo_icon.pixmap(20, 20)
        self.logo.setPixmap(logo_pixmap)

        #Setting up title and wifi connection (need to add functionality to this later)
        self.title = QLabel("Sensor Dashboard")
        self.status = QLabel("● CONNECTED")

        #Setting up usb connection logo (need to add functionality to this later)
        self.connection = QLabel()
        usb_icon = qta.icon("mdi.usb", color="#FFFFFF")
        usb_pixmap = usb_icon.pixmap(20, 20)
        self.connection.setPixmap(usb_pixmap)

        #Setting up network logo
        self.network = QLabel()
        wifi_icon = qta.icon("ph.wifi-high-light", color="#FFFFFF")
        wifi_pixmap = wifi_icon.pixmap(20, 20)
        self.network.setPixmap(wifi_pixmap)

        #Setting up clock (Need to add functionality to this later)
        self.clock = QLabel("5:11 PM")

        #adding widgets to banner layout
        layout.addWidget(self.logo)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addStretch()
        layout.addWidget(self.status)
        layout.addSpacing(15)
        layout.addWidget(self.connection)
        layout.addSpacing(15)
        layout.addWidget(self.network)
        layout.addSpacing(15)
        layout.addWidget(self.clock)

        self.setLayout(layout)

        self.setObjectName("TopBanner")
        self.setStyleSheet("""
        #TopBanner{
            background: #11161D;
            border-bottom: 2px solid #141a1f;           
        }
        """)

        self.title.setStyleSheet("""
            font-size: 15px;
            color: #FFFFFF;
        """)

        self.status.setStyleSheet("""
            color: #009D22;
            font-size: 12px;
        """)

        self.clock.setStyleSheet("""
            font-size: 12px;
            color: #FFFFFF;
        """)

class SideBanner(QFrame):

    dashboard_clicked = Signal()
    livedata_clicked = Signal()
    logs_clicked = Signal()
    settings_clicked = Signal()
    about_clicked = Signal()

    #HTML for the Button
    NORMAL_BUTTON_STYLE = """
        QPushButton {
            background: transparent;
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            text-align: left;
            padding-left: 8px;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #1A222C;
        }
    """

    #HTML for the actively selected button
    ACTIVE_BUTTON_STYLE = """
        QPushButton {
            background-color: rgba(59,130,245,0.5);
            color: white;
            border-left: 2px solid #3B82F6;
            border-radius: 5px;
            color: #FFFFFF;
            text-align: left;
            padding-left: 8px;
            font-size: 14px;
        }
    """
    
    def create_icon(self, icon_name, color="#FFFFFF"):
        return qta.icon(icon_name, color=color)

    def __init__(self):
        super().__init__()

        self.setObjectName("SideBanner")
        self.setFixedWidth(170)
        self.setStyleSheet("""
            #SideBanner {
                background-color: #11161D;
                border-right: 2px solid #141a1f;
            }
        """)

        # Setting up button
        self.dashboard_button = QPushButton("Dashboard")
        self.livedata_button = QPushButton("Live Data")
        self.logs_button = QPushButton("Data Logger")
        self.settings_button = QPushButton("Settings")
        self.about_button = QPushButton("About")
        
        # Setting up array of buttons to reduce code amount
        self.buttons = [
            self.dashboard_button,
            self.livedata_button,
            self.logs_button,
            self.settings_button,
            self.about_button
        ]

        self.dashboard_button.setIcon(
            self.create_icon("fa5s.home")
        )
        self.livedata_button.setIcon(
            self.create_icon("ph.database")
        )
        self.logs_button.setIcon(
            self.create_icon("ri.file-paper-2-fill")
        )
        self.settings_button.setIcon(
            self.create_icon("ri.settings-2-line")
        )
        self.about_button.setIcon(
            self.create_icon("mdi.information-outline")
        )

        #Setting up button sizes and styles
        for button in self.buttons:
            button.setFixedSize(150, 42)
            button.setStyleSheet(self.NORMAL_BUTTON_STYLE)

        # Button Connections
        self.dashboard_button.clicked.connect(
            self.dashboard_clicked.emit
        )

        self.livedata_button.clicked.connect(
            self.livedata_clicked.emit
        )

        self.logs_button.clicked.connect(
            self.logs_clicked.emit
        )

        self.settings_button.clicked.connect(
            self.settings_clicked.emit
        )

        self.about_button.clicked.connect(
            self.about_clicked.emit
        )

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setSpacing(10)
        sidebar_layout.addSpacing(20)

        sidebar_layout.addWidget(
            self.dashboard_button,
            alignment=Qt.AlignHCenter
        )

        sidebar_layout.addWidget(
            self.livedata_button,
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

        sidebar_layout.addWidget(
            self.about_button,
            alignment=Qt.AlignHCenter
        )

        sidebar_layout.addStretch()

        self.setLayout(sidebar_layout)
        
    def set_active_button(self, active_button):

        for button in self.buttons:
            button.setStyleSheet(self.NORMAL_BUTTON_STYLE)
        
        active_button.setStyleSheet(self.ACTIVE_BUTTON_STYLE)