from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
)

from PySide6.QtGui import(
    QPixmap
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
        layout.setContentsMargins(20,8,20,12)

        #Setting up banner logo using pixmap
        self.logo = QLabel()
        logo_icon = qta.icon("ph.gauge-bold", color="#FFFFFF")
        logo_pixmap = logo_icon.pixmap(32, 32)
        self.logo.setPixmap(logo_pixmap)

        #Setting up title and wifi connection (need to add functionality to this later)
        self.title = QLabel("Sensor Dashboard")
        self.status = QLabel("● Connected")

        #Setting up usb connection logo (need to add functionality to this later)
        self.connection = QLabel()
        usb_icon = qta.icon("mdi.usb", color="#FFFFFF")
        usb_pixmap = usb_icon.pixmap(25, 25)
        self.connection.setPixmap(usb_pixmap)

        #Setting up network logo
        self.network = QLabel()
        wifi_icon = qta.icon("ph.wifi-high-light", color="#FFFFFF")
        wifi_pixmap = wifi_icon.pixmap(25, 25)
        self.network.setPixmap(wifi_pixmap)

        #Setting up clock (Need to add functionality to this later)
        self.clock = QLabel("5:11 PM")

        #adding widgets to banner layout
        layout.addWidget(self.logo)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addStretch()
        layout.addWidget(self.status)
        layout.addSpacing(10)
        layout.addWidget(self.connection)
        layout.addSpacing(10)
        layout.addWidget(self.network)
        layout.addSpacing(10)
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
            font-size: 20px;
            color: #FFFFFF;
        """)

        self.status.setStyleSheet("""
            color: #FFFFFF;
            font-size: 15px;
            font-weight: bold;
        """)

        self.clock.setStyleSheet("""
            color: #FFFFFF;
            font-weight: bold;
        """)

        self.setFixedHeight(60)


