from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy
)

from PySide6.QtGui import(
    QPixmap
)
from PySide6.QtCore import (
    Qt,
    Signal,
)
import qtawesome as qta

class EcuCard(QFrame):
    
    def __init__(self):
        super().__init__()

        self.setObjectName("EcuFrame")
        self.setStyleSheet("""
        #EcuFrame{
            background-color:#14191f;
            border:1px solid #273341;
            border-radius:10px;
        }
        """)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

class DriveTrainCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("DriveTrainFrame")
        self.setStyleSheet("""
        #DriveTrainFrame{
            background-color:#14191f;
            border:1px solid #273341;
            border-radius:10px;
        }                
        """)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

class SensorTrends(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("DriveTrainFrame")
        self.setStyleSheet("""
        #DriveTrainFrame{
            background-color:#14191f;
            border:1px solid #273341;
            border-radius:10px;
        }                
        """)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

class SystemLog(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("DriveTrainFrame")
        self.setStyleSheet("""
        #DriveTrainFrame{
            background-color:#14191f;
            border:1px solid #273341;
            border-radius:10px;
        }                
        """)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

class BottomLog(QFrame):
    
    def create_icon(self, icon_title, color="#6B7280", size=25):
        self.label = QLabel()

        self.label.setContentsMargins(0,0,0,0)

        icon = qta.icon(str(icon_title), color=color)
        self.label.setPixmap(icon.pixmap(size, size))

        return self.label
    
    def create_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFixedWidth(1)
        line.setStyleSheet("""
            background-color: #273341;
            border: none;
        """)
        return line
    
    def create_monitor_card(self, value, unit, label, icon):
        #Overall Container of Card
        self.monitor_card = QFrame()

        self.monitor_card.setContentsMargins(0,0,0,0)
        self.monitor_card.setObjectName("MonitorFrame")
        
        self.monitor_card.setStyleSheet("""
        #MonitorFrame{
            background-color:#11161D;
            border-right: 1px solid #273341; 
        }                   
        """)
        
        #Top Text of the Monitor Card
        monitor_card_top_text_layout = QHBoxLayout()
        
        self.value = QLabel(value)
        self.unit = QLabel(unit)
        
        monitor_card_top_text_layout.addWidget(self.value, 1)
        monitor_card_top_text_layout.addWidget(self.unit, 6)

        monitor_card_top_text_layout.setSpacing(3)
        monitor_card_top_text_layout.setContentsMargins(0,0,0,0)

        self.value.setStyleSheet("""
            font-size: 14px;
            color: #6B7280;
            font-weight: bold;
        """)

        self.unit.setStyleSheet("""
            font-size: 10px;
            color: #6B7280;
            font-weight: none;
        """)
        
        self.monitor_card_top_text = QWidget()
        self.monitor_card_top_text.setLayout(monitor_card_top_text_layout)

        #Bottom text of card and overall text of card
        monitor_card_text_layout = QVBoxLayout()
        
        monitor_card_text_layout.setSpacing(0)
        monitor_card_text_layout.setContentsMargins(0,0,0,0)
        
        monitor_card_text_layout.addWidget(self.monitor_card_top_text)
        
        self.label = QLabel(label)
        monitor_card_text_layout.addWidget(self.label)

        self.label.setStyleSheet("""
            font-size: 10px;
            color: #6B7280;
            font-weight: none;
        """)
        
        self.monitor_card_text = QWidget()
        self.monitor_card_text.setLayout(monitor_card_text_layout)

        #Overall Structure of Card
        monitor_card_layout = QHBoxLayout()
        
        monitor_card_layout.setContentsMargins(0,0,0,0)
        monitor_card_layout.setSpacing(6)
        
        monitor_card_layout.addWidget(icon, 1)
        monitor_card_layout.addWidget(self.monitor_card_text, 6)

        self.monitor_card.setLayout(monitor_card_layout)

        return self.monitor_card
   
    def __init__(self):
        super().__init__()

        self.setObjectName("DriveTrainFrame")
        self.setStyleSheet("""
        #DriveTrainFrame{
            background-color:#11161D;
            border:1px solid #273341;
            border-radius:10px;
        }                
        """)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        bottom_log_layout = QHBoxLayout()

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("""
            color: #273341;
        """)

        self.battery_voltage_icon = self.create_icon("fa6s.battery-half")
        self.ambient_temp_icon = self.create_icon("fa5s.thermometer-half")
        self.vehicle_speed_icon = self.create_icon("mdi6.speedometer")
        self.motor_torque_icon = self.create_icon("fa6s.rotate")
        self.drive_state_icon = self.create_icon("mdi.alpha-p-box-outline")

        self.battery_voltage = self.create_monitor_card("12.6", "V", "Battery Voltage", self.battery_voltage_icon)
        self.ambient_temp = self.create_monitor_card("25.3", "°C", "Ambient Temperature", self.ambient_temp_icon)
        self.vehicle_speed = self.create_monitor_card("0.0", "MPH", "Vehicle Speed", self.vehicle_speed_icon)
        self.motor_torque = self.create_monitor_card("0.0", "ft-lbs", "Motor Torque", self.motor_torque_icon)
        self.drive_state = self.create_monitor_card("Park", None, "Drive State", self.drive_state_icon)

        bottom_log_layout.addWidget(self.create_separator(), 1)
        bottom_log_layout.addWidget(self.battery_voltage, 1)
        bottom_log_layout.addWidget(self.create_separator(), 1)
        bottom_log_layout.addWidget(self.ambient_temp, 1)
        bottom_log_layout.addWidget(self.create_separator(),1)
        bottom_log_layout.addWidget(self.vehicle_speed, 1)
        bottom_log_layout.addWidget(self.create_separator(),1)
        bottom_log_layout.addWidget(self.motor_torque, 1)
        bottom_log_layout.addWidget(self.create_separator(),1)
        bottom_log_layout.addWidget(self.drive_state, 1)

        self.setLayout(bottom_log_layout)

class StatusCard(QFrame):

    def __init__(self, title, status):
        super().__init__()

        self.setObjectName("StatusCard")

        self.icon = QLabel()

        icon = qta.icon(
            "fa5s.circle",
            color="#3CCF4E"
        )

        self.icon.setPixmap(icon.pixmap(12,12))

        self.title = QLabel(title)

        self.status = QLabel(status)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setContentsMargins(0,0,0,0)

        text_layout.addWidget(self.title)
        text_layout.addWidget(self.status)

        layout = QHBoxLayout()
        layout.setContentsMargins(12,12,12,12)
        layout.setSpacing(10)

        layout.addWidget(self.icon)
        layout.addLayout(text_layout)

        self.setLayout(layout)

        self.setStyleSheet("""
        #StatusCard{
            background-color:#11161D;
            border:1px solid #273341;
            border-radius:10px;
        }
        QLabel{
            border:none;
        }
        """)
        self.title.setStyleSheet("""
            color:#9CA3AF;
            font-size:8px;
        """)
        self.status.setStyleSheet("""
            color:#3CCF4E;
            font-size:10px;
            font-weight:bold;
        """)

class sensorCard(QFrame):

    def __init__(self, title, value, units):
        super().__init__()

        frame = QFrame()
        frame.setObjectName("SensorCard")
        frame.setStyleSheet("""
            #SensorCard {
                background-color: #14191f;
                border: 1px solid #273341;
                border-radius: 12px;
            }
            QLabel {
                background-color:#14191f;
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

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(12,12,12,12)
        frame_layout.setSpacing(6)

        frame_layout.addWidget(self.title_label)
        frame_layout.addWidget(self.value_label)
        frame_layout.addWidget(self.units_label)

        frame.setLayout(frame_layout)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

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
            background-color: rgba(1,47,99,0.5);
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

        
        self.system_card = StatusCard(
            "System Status",
            "All Systems Normal"
        )

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

        sidebar_layout.addWidget(self.system_card)

        self.version = QLabel("v1.0.0")
        self.version.setStyleSheet("""
            color:#6B7280;
            font-size: 11px;
            border:none;
        """)
        sidebar_layout.addWidget(self.version)

        self.setLayout(sidebar_layout)
        
    def set_active_button(self, active_button):

        for button in self.buttons:
            button.setStyleSheet(self.NORMAL_BUTTON_STYLE)
        
        active_button.setStyleSheet(self.ACTIVE_BUTTON_STYLE)