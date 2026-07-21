from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QScrollArea
)

from PySide6.QtGui import(
    QPixmap,
    QFont,
    QPainter,
    QPen,
    QColor
)
from PySide6.QtCore import (
    Qt,
    Signal,
    QTimer,
    QTime,
    QRectF
)

from collections import deque

from pages.utilities.fetcher import (
    NetworkCheckWorker,
    ConnectionManager,
)

import qtawesome as qta
import pyqtgraph as pg

pg.setConfigOption('background', '#14191f')
pg.setConfigOption('foreground', '#6B7280')
pg.setConfigOption('antialias', True)

class ArcGauge(QWidget):

    def __init__(self, label, unit="%", min_value=0, max_value=100, color="#3B82F6"):
        super().__init__()
        self.label = label
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.color = QColor(color)
        self.value = min_value
        self.setMinimumSize(110, 110)
    
    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        side = min(self.width(), self.height()) - 20
        x_offset = (self.width() - side) / 2
        y_offset = (self.height() - side) / 2

        rect = QRectF(x_offset, y_offset, side, side)
        start_angle = 225 * 16
        span_angle = -270 * 16

        track_pen = QPen(QColor("#273341"), 8, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(rect, start_angle, span_angle)

        fraction = (self.value - self.min_value) / (self.max_value - self.min_value)
        value_pen = QPen(self.color, 8, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(value_pen)
        painter.drawArc(rect, start_angle, int(span_angle * fraction))

        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value:.0f}{self.unit}")

        painter.end()

class EcuCard(QFrame):

    def __init__(self, connection_manager=None):
        super().__init__()

        self.setObjectName("EcuFrame")
        self.setStyleSheet("""
        #EcuFrame{
            background-color:#14191f;
            border:1px solid #273341;
            border-radius:10px;
        }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        title = QLabel("ECU STATUS")
        title.setStyleSheet("""
            color:#A6B2C2; font-size:12px; font-weight:bold;
            border:none; background:transparent;
        """)

        # --- Faults section, styled and structured exactly like SystemLog ---
        self.faults_layout = QVBoxLayout()
        self.faults_layout.setSpacing(8)
        self.faults_layout.setContentsMargins(0, 0, 0, 0)
        self.faults_layout.addStretch()

        faults_container = QWidget()
        faults_container.setStyleSheet("background:transparent;")
        faults_container.setLayout(self.faults_layout)

        faults_scroll = QScrollArea()
        faults_scroll.setWidget(faults_container)
        faults_scroll.setWidgetResizable(True)
        faults_scroll.setAlignment(Qt.AlignTop)   # forces content to the top, not centered
        faults_scroll.setFrameShape(QFrame.NoFrame)
        faults_scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical { background: transparent; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #273341; border-radius: 4px; min-height: 24px; }
            QScrollBar::handle:vertical:hover { background: #3B4657; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; background: none; border: none; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)

        self._set_no_faults()

        # --- Divider ---
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #273341; border: none;")

        # --- Gauges (compact, secondary) ---
        self.load_gauge = ArcGauge("Engine Load", unit="%", color="#3B82F6")
        self.throttle_gauge = ArcGauge("Throttle Position", unit="%", color="#EAB308")
        self.load_gauge.setFixedSize(80, 80)
        self.throttle_gauge.setFixedSize(80, 80)

        load_label = QLabel("ENGINE LOAD")
        load_label.setAlignment(Qt.AlignCenter)
        load_label.setStyleSheet("color:#6B7280; font-size:9px; border:none; background:transparent;")

        throttle_label = QLabel("THROTTLE POSITION")
        throttle_label.setAlignment(Qt.AlignCenter)
        throttle_label.setStyleSheet("color:#6B7280; font-size:9px; border:none; background:transparent;")

        load_col = QVBoxLayout()
        load_col.setSpacing(4)
        load_col.addWidget(self.load_gauge, alignment=Qt.AlignCenter)
        load_col.addWidget(load_label)

        throttle_col = QVBoxLayout()
        throttle_col.setSpacing(4)
        throttle_col.addWidget(self.throttle_gauge, alignment=Qt.AlignCenter)
        throttle_col.addWidget(throttle_label)

        gauges_layout = QHBoxLayout()
        gauges_layout.addLayout(load_col)
        gauges_layout.addLayout(throttle_col)

        gauges_widget = QWidget()
        gauges_widget.setStyleSheet("background:transparent;")
        gauges_widget.setLayout(gauges_layout)
        gauges_widget.setFixedHeight(110)

        # --- Assemble ---
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)          # tightened from 10 -> 8, matches title-to-content feel
        main_layout.addWidget(title)
        main_layout.addWidget(faults_scroll, 1)
        main_layout.addWidget(divider)
        main_layout.addWidget(gauges_widget)
        self.setLayout(main_layout)

    def _set_no_faults(self):
        self._clear_faults()
        row = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet("color:#3CCF4E; font-size:10px; border:none; background:transparent;")
        text = QLabel("No Active Faults")
        text.setStyleSheet("color:#9CA3AF; font-size:11px; border:none; background:transparent;")
        row.addWidget(dot)
        row.addWidget(text)
        row.addStretch()
        wrapper = QFrame()
        wrapper.setStyleSheet("background:transparent; border:none;")
        wrapper.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # never stretches vertically
        wrapper.setLayout(row)
        self.faults_layout.insertWidget(0, wrapper)

    def _clear_faults(self):
        while self.faults_layout.count() > 1:
            item = self.faults_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_fault(self, code, description):
        self._clear_faults()
        row = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet("color:#EF4444; font-size:10px; border:none; background:transparent;")
        text = QLabel(f"{code}: {description}")
        text.setStyleSheet("color:#D1D5DB; font-size:11px; border:none; background:transparent;")
        row.addWidget(dot)
        row.addWidget(text)
        row.addStretch()
        wrapper = QFrame()
        wrapper.setStyleSheet("background:transparent; border:none;")
        wrapper.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        wrapper.setLayout(row)
        self.faults_layout.insertWidget(0, wrapper)

    def update_engine_load(self, value):
        self.load_gauge.set_value(value)

    def update_throttle_position(self, value):
        self.throttle_gauge.set_value(value)


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

class SecondsAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [f"{int(v)}s" for v in values]

class SensorTrends(QFrame):
    
    SERIES = {
        "rpm": {"label": "Motor Speed (RPM)", "color": "#3B82F6", "axis": "left"},
        "current": {"label": "Motor Current (A)", "color": "#22C55E", "axis": "right"},
        "voltage": {"label": "Battery Voltage (V)", "color": "#EAB308", "axis": "right"},
        "temp": {"label": "Motor Temp (\u00b0F)", "color": "#A855F7", "axis": "right"}
    }
    
    def __init__(self, window_seconds=60, max_points=600):
        super().__init__()

        self.window_seconds = window_seconds
        self.time_data = deque(maxlen=max_points)
        self.data = {key: deque(maxlen=max_points) for key in self.SERIES}

        self.setObjectName("SensorTrendsFrame")
        self.setStyleSheet("""
        #SensorTrendsFrame {
            background-color: #14191f;
            border:1px solid #273341;
            border-radius:10px;
        }              
        """)
        
        
        title = QLabel("SENSOR TRENDS")
        title.setStyleSheet("""
            color:#A6B2C2;
            font-size:12px;
            font-weight:bold;
            border:none;
            background: transparent;
        """)

        self.plot_widget = pg.PlotWidget(
            axisItems = {'bottom': SecondsAxisItem(orientation='bottom')}
        )
        self.plot_widget.setBackground('#14191f')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.15)
        self.plot_widget.setXRange(-self.window_seconds, 0)
        self.plot_widget.setYRange(0, 6000, padding = 0)
        self.plot_widget.getAxis('left').setTickSpacing(major=1000, minor=500)
        self.plot_widget.getAxis('right').setTickSpacing(major=20, minor=10)
        

        tick_font = QFont()
        tick_font.setPointSize(8)

        for axis_name in ('left', 'bottom', 'right'):
            axis = self.plot_widget.getAxis(axis_name)
            axis.setTickFont(tick_font)

        self.plot_widget.getAxis('left').setTextPen(pg.mkPen(self.SERIES["rpm"]["color"]))
        self.plot_widget.getAxis('right').setTextPen(pg.mkPen(self.SERIES["temp"]["color"]))
        
        plot_item = self.plot_widget.getPlotItem()

        axis = self.plot_widget.getAxis('left')
        axis.setStyle(maxTickLevel=1)

        self.right_vb = pg.ViewBox()
        plot_item.showAxis('right')
        plot_item.scene().addItem(self.right_vb)
        plot_item.getAxis('right').linkToView(self.right_vb)
        self.right_vb.setXLink(plot_item.vb)
        self.right_vb.setYRange(0, 120)

        def sync_right_view():
            self.right_vb.setGeometry(plot_item.vb.sceneBoundingRect())
            self.right_vb.linkedViewChanged(plot_item.vb, self.right_vb.XAxis)
        
        plot_item.vb.sigResized.connect(sync_right_view)

        self.curves = {}
        for key, meta in self.SERIES.items():
            pen = pg.mkPen(meta["color"], width = 2)
            if meta["axis"] == "left":
                self.curves[key] = plot_item.plot(pen=pen, name=meta["label"])
            else:
                curve = pg.PlotCurveItem(pen=pen)
                self.right_vb.addItem(curve)
                self.curves[key] = curve

        plot_item.hideButtons()
        plot_item.vb.setMouseEnabled(x=False, y=False)

        self.right_vb.setMouseEnabled(x=False, y=False)
        
        self.plot_widget.getAxis('left').setWidth(45)
        self.plot_widget.getAxis('right').setWidth(45)
        
        legend_row = self._build_legend()

        layout = QVBoxLayout()
        layout.setContentsMargins(12,12,12,12)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addWidget(legend_row)
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def _build_legend(self):
        row = QHBoxLayout()
        row.setSpacing(16)
        row.setContentsMargins(0,0,0,0)
        for meta in self.SERIES.values():
            dot = QLabel("-")
            dot.setStyleSheet(f"color:{meta['color']}; font-weight:bold; border:none; background:transparent;")
            text = QLabel(meta["label"])
            text.setStyleSheet("color:#6B7280; font-size:10px; border:none; background:transparent;")
            pair = QHBoxLayout()
            pair.setSpacing(4)
            pair.addWidget(dot)
            pair.addWidget(text)
            row.addLayout(pair)
        row.addStretch()
        container = QFrame()
        container.setStyleSheet("background:transparent; border:none;")
        container.setLayout(row)
        return container
    
    def add_data_point(self, timestamp, rpm, current, voltage, temp):
        self.time_data.append(timestamp)
        self.data["rpm"].append(rpm)
        self.data["current"].append(current)
        self.data["voltage"].append(voltage)
        self.data["temp"].append(temp)
        self._redraw()
    
    def _redraw(self):
        if not self.time_data:
            return
        latest = self.time_data[-1]
        t = [x - latest for x in self.time_data]
        for key, curve in self.curves.items():
            curve.setData(t, list(self.data[key]))

class SystemLog(QFrame):
    
    LEVEL_COLORS = {
        "info": "#3b82F6",
        "success": "#3CCF4E",
        "error": "#EF4444"
    }

    def __init__(self, connection_manager, sensor_names):
        super().__init__()
        self.conn_mgr = connection_manager
        self.sensor_names = sensor_names

        self.setObjectName("SystemLog")
        self.setObjectName("SystemLogFrame")
        self.setStyleSheet("""
            #SystemLogFrame {
                background-color:#14191f;
                border:1px solid #273341;
                border-radius:10px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        title = QLabel("SYSTEM LOG")
        title.setStyleSheet("""
            color:#A6B2C2; font-size:12px; font-weight:bold;
            border:none; background:transparent;
        """)

        self.entries_layout = QVBoxLayout()
        self.entries_layout.setSpacing(10)
        self.entries_layout.setContentsMargins(0, 0, 0, 0)
        self.entries_layout.addStretch()  # keeps the list pinned to the top as it grows

        entries_container = QWidget()
        entries_container.setStyleSheet("background:transparent;")
        entries_container.setLayout(self.entries_layout)

        scroll = QScrollArea()
        scroll.setWidget(entries_container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #273341;
                border-radius: 4px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3B4657;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        scroll.setFrameShape(QFrame.NoFrame)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)
        main_layout.addWidget(title)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        self.conn_mgr.sensor_status_changed.connect(self._on_sensor_status)
        self.conn_mgr.system_status_changed.connect(self._on_system_status)
        self.conn_mgr.overall_connection_changed.connect(self._on_overall_connection)

        for name in self.sensor_names:
            self.conn_mgr.register_sensor(name)

        self._run_boot_sequence()
    
    def _run_boot_sequence(self):
        self.add_entry("System boot", "info")
        QTimer.singleShot(300, lambda: self.add_entry("Logging started", "info"))

        delay = 600
        for name in self.sensor_names:
            QTimer.singleShot(delay, lambda n=name: self._boot_check_sensor(n))
            delay += 300
        
        QTimer.singleShot(delay+200, lambda: self.add_entry("System connected", "success"))
    
    def _boot_check_sensor(self, name):
        self.conn_mgr.report_sensor_data(name)
        self.add_entry(f"{name}: OK", "success")
    
    def _on_sensor_status(self, name, connected):
        if connected:
            self.add_entry(f"{name} reconnected", "success")
        else:
            self.add_entry(f"{name} disconnected", "error")
    
    def _on_system_status(self, healthy, message):
        self.add_entry(message, "success" if healthy else "error")
    
    def _on_overall_connection(self, connected):
        self.add_entry(
            "System connected" if connected else "System disconnected",
            "success" if connected else "error"
        )

    def add_entry(self, message, level="info"):
        row = QFrame()
        row.setStyleSheet("background:transparent; border:none;")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        timestamp = QLabel(QTime.currentTime().toString("h:mm:ss"))
        timestamp.setStyleSheet("color:#6B7280; font-size:11px; border:none; background:transparent;")
        timestamp.setFixedWidth(55)

        dot = QLabel("●")
        color = self.LEVEL_COLORS.get(level, "#6B7280")
        dot.setStyleSheet(f"color:{color}; font-size:10px; border:none; background:transparent;")

        text = QLabel(message)
        text.setStyleSheet("color:#D1D5DB; font-size:12px; border:none; background:transparent;")

        layout.addWidget(timestamp)
        layout.addWidget(dot)
        layout.addWidget(text)
        layout.addStretch()
        row.setLayout(layout)

        self.entries_layout.insertWidget(0, row)

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
    
    def _check_network(self):
        self._net_worker = NetworkCheckWorker()
        self._net_worker.status_changed.connect(self._update_network_icon)
        self._net_worker.start()
        
    def _update_network_icon(self, connected):
        color = "#3CCF4E" if connected else "#EF4444"
        icon = qta.icon("ph.wifi-high-light" if connected else "ph.wifi-slash-light", color=color)
        self.network.setPixmap(icon.pixmap(20,20))

    def _update_status(self, connected):
        if connected:
            self.status.setText("● CONNECTED")
            self.status.setStyleSheet("color:#009D22; font-size:12px;")
        else:
            self.status.setText("● DISCONNECTED")
            self.status.setStyleSheet("color:#EF4444; font-size:12px;")

    def _update_usb(self, connected):
        color = "#FFFFFF" if connected else "#4B5563"
        icon = qta.icon("mdi.usb", color=color)
        self.connection.setPixmap(icon.pixmap(20,20))
    
    def _update_wifi_manual(self, connected):
        color = "#3CCF4E" if connected else "#4B5563"
        icon = qta.icon("ph.wifi-high-light" if connected else "ph.wifi-slash-light")
        self.network.setPixmap(icon.pixmap(20,20))
 
    def __init__(self, connection_manager):
        super().__init__()

        self.conn_mgr = connection_manager

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
          
        self.network_timer = QTimer(self)
        self.network_timer.timeout.connect(self._check_network)
        self.network_timer.start(5000)

        #Setting up clock (Need to add functionality to this later)
        self.clock = QLabel("5:11 PM")
        self._update_clock()
        
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)

        #Connection
        self.conn_mgr.overall_connection_changed.connect(self._update_status)
        self.conn_mgr.usb_changed.connect(self._update_usb)
        self.conn_mgr.wifi_changed.connect(self._update_wifi_manual)

        self._update_status(self.conn_mgr.overall_connected)
        self._update_usb(self.conn_mgr._usb_connected)

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
    def _update_clock(self):
        self.clock.setText(QTime.currentTime().toString("h:mm AP"))

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
    
    def _update_system_status(self, healthy, message):
        color = "#3CCF4E" if healthy else "#EF4444"
        self.system_card.status.setText(message)
        self.system_card.status.setStyleSheet(f"color:{color}; font-size:10px; font-weight:bold;")

    def __init__(self, connection_manager):
        super().__init__()

        
        self.system_card = StatusCard(
            "System Status",
            "All Systems Normal"
        )

        self.conn_mgr = connection_manager
        self.conn_mgr.system_status_changed.connect(self._update_system_status)

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