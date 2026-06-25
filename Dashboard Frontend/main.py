import sys
import math
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QHBoxLayout, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen


# -------------------------
# RPM GAUGE (QPainter)
# -------------------------
class RPMGauge(QWidget):
    def __init__(self):
        super().__init__()
        self.rpm = 0
        self.max_rpm = 8000
        self.setMinimumSize(250, 250)

    def set_rpm(self, rpm):
        self.rpm = rpm
        self.update()  # triggers repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(20, 20, -20, -20)

        # background circle
        bg_pen = QPen(QColor("#333"))
        bg_pen.setWidth(12)
        painter.setPen(bg_pen)
        painter.drawEllipse(rect)

        # RPM arc
        angle_span = int(360 * (self.rpm / self.max_rpm))

        arc_pen = QPen(QColor("#00e5ff"))
        arc_pen.setWidth(12)
        painter.setPen(arc_pen)
        painter.drawArc(rect, 90 * 16, -angle_span * 16)

        # center text
        painter.setPen(QColor("white"))
        painter.drawText(rect, Qt.AlignCenter, f"{self.rpm} RPM")


# -------------------------
# MAIN DASHBOARD
# -------------------------
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Car Dashboard")
        self.setStyleSheet("background-color: #0f0f0f; color: white;")

        # ---------------- TOP BAR ----------------
        self.speed_label = QLabel("Speed: 0 mph")
        self.gear_label = QLabel("Gear: D")
        self.time_label = QLabel("21:45")

        top_bar = QHBoxLayout()
        top_bar.addWidget(self.speed_label)
        top_bar.addStretch()
        top_bar.addWidget(self.gear_label)
        top_bar.addStretch()
        top_bar.addWidget(self.time_label)

        # ---------------- RPM GAUGE ----------------
        self.rpm_gauge = RPMGauge()

        # ---------------- FUEL BAR ----------------
        self.fuel = QProgressBar()
        self.fuel.setRange(0, 100)
        self.fuel.setValue(70)
        self.fuel.setTextVisible(True)
        self.fuel.setStyleSheet("""
            QProgressBar {
                background-color: #222;
                border-radius: 8px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #00c853;
                border-radius: 8px;
            }
        """)

        fuel_card = QFrame()
        fuel_layout = QVBoxLayout()
        fuel_layout.addWidget(QLabel("Fuel"))
        fuel_layout.addWidget(self.fuel)
        fuel_card.setLayout(fuel_layout)
        fuel_card.setStyleSheet("background-color: #1c1c1c; border-radius: 10px; padding: 10px;")

        # ---------------- RIGHT PANEL ----------------
        self.temp_label = QLabel("Engine Temp: 90°C")
        self.voltage_label = QLabel("Voltage: 12.4V")

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.temp_label)
        right_panel.addWidget(self.voltage_label)

        right_frame = QFrame()
        right_frame.setLayout(right_panel)
        right_frame.setStyleSheet("background-color: #1c1c1c; border-radius: 10px; padding: 10px;")

        # ---------------- MAIN LAYOUT ----------------
        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.rpm_gauge)
        middle_layout.addWidget(right_frame)
        middle_layout.addWidget(fuel_card)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(top_bar)
        main_layout.addLayout(middle_layout)

        # ---------------- SIMULATED DATA LOOP ----------------
        self.speed = 0
        self.rpm = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)  # 10 Hz update

    def update_data(self):
        # fake driving simulation
        self.speed = (self.speed + random.randint(0, 3)) % 120
        self.rpm = int(self.speed * 60 + random.randint(-200, 200))

        fuel_value = max(0, self.fuel.value() - 0.01)

        # update UI
        self.speed_label.setText(f"Speed: {self.speed} mph")
        self.rpm_gauge.set_rpm(self.rpm)
        self.fuel.setValue(int(fuel_value))


# -------------------------
# RUN APP
# -------------------------
app = QApplication(sys.argv)

window = Dashboard()
window.resize(900, 500)
window.show()

sys.exit(app.exec())