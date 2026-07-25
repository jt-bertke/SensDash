from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout
)

from PySide6.QtCore import (
    QTimer,
)

import time
import random

from pages.utilities.cards import (
    sensorCard,
    EcuCard,
    TirePressureCard,
    SensorTrends,
    SystemLog,
    BottomLog,
    DualStatCard,
    CompassCard,
    PlaceholderCard
)

class dashboardPage(QWidget):

    def __init__(self, connection_manager):
        super().__init__()
        
        data_cluster = QGridLayout()

        data_cluster.setContentsMargins(0,0,0,0)
        data_cluster.setSpacing(3)
        for row in range(3):
            data_cluster.setRowStretch(row, 1)
        for col in range(2):
            data_cluster.setColumnStretch(col, 1)

        self.compass_card = CompassCard()
        
        self.oil_card = DualStatCard(
            "OIL PRESSURE / TEMP",
            "Pressure", "--", "psi",
            "Temp", "--", "F",
        )

        self.mileage_card = DualStatCard(
            "GAS MILEAGE",
            "Instant", "--", "mpg",
            "Average", "--", "mpg"
        )

        self.trip_card = DualStatCard(
            "TRIP A / B",
            "Trip A", "--", "mi",
            "Trip B", "--", "mi",
        )

        self.placeholder_card = PlaceholderCard()

        self.motor_temp_card = sensorCard(
            title="Coolant Temp",
            value="--",
            units="F"
        )

        self._grid_test_timer = QTimer(self)
        self._grid_test_timer.timeout.connect(lambda: (
            self.compass_card.update_heading(random.uniform(0, 360)),
            self.oil_card.update_value1(f"{random.uniform(30, 60):.0f}"),
            self.oil_card.update_value2(f"{random.uniform(180, 230):.0f}"),
            self.mileage_card.update_value1(f"{random.uniform(15, 25):.1f}"),
            self.mileage_card.update_value2(f"{random.uniform(18, 22):.1f}"),
            self.motor_temp_card.value_label.setText(f"{random.uniform(180, 220):.0f}"),
        ))
        self._grid_test_timer.start(1000)

        data_cluster.addWidget(self.compass_card, 0, 0)
        data_cluster.addWidget(self.placeholder_card, 0, 1)
        data_cluster.addWidget(self.mileage_card, 1, 0)
        data_cluster.addWidget(self.trip_card, 1, 1)
        data_cluster.addWidget(self.oil_card, 2,0)
        data_cluster.addWidget(self.motor_temp_card, 2,1)


        data_cluster_widget = QWidget()
        data_cluster_widget.setLayout(data_cluster)
        data_cluster_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        Ecu_card = EcuCard()
        self._ecu_test_timer = QTimer()
        self._ecu_test_timer.timeout.connect(lambda: (
            Ecu_card.update_engine_load(random.uniform(10, 80)),
            Ecu_card.update_throttle_position(random.uniform(0, 100))
        ))
        self._ecu_test_timer.start(500)
        Ecu_card.add_fault("P0301", "Cylinder 1 Misfire Detected")
        
        Tire_Pressure = TirePressureCard()
        Tire_Pressure.update_tire("fl", 34)
        Tire_Pressure.update_tire("fr", 35)
        Tire_Pressure.update_tire("rl", 33)
        Tire_Pressure.update_tire("rr", 35)

        Sensor_Trends = SensorTrends()
        self._test_timer = QTimer()
        self._test_timer.timeout.connect(lambda: Sensor_Trends.add_data_point(
            time.time(),
            rpm=3000 + random.uniform(-500, 500),
            current=30 + random.uniform(-5, 5),
            voltage=45 + random.uniform(-2, 2),
            temp=70 +random.uniform(-3, 3),
        ))
        self._test_timer.start(500)

        System_Log = SystemLog(connection_manager, [
            "ECU / OBD-II Link", "Coolant Temp", "Oil Pressure",
            "Oil Temp", "TPMS", "Compass / GPS",
        ])

        Bottom_Log = BottomLog()

        dash_layout = QGridLayout()

        dash_layout.setSpacing(12)

        dash_layout.setColumnStretch(0, 1)
        dash_layout.setColumnStretch(1, 1)
        dash_layout.setColumnStretch(2, 1)

        dash_layout.setRowStretch(0, 5)
        dash_layout.setRowStretch(1, 3)
        dash_layout.setRowStretch(2, 1)

        dash_layout.addWidget(Ecu_card, 0, 0, 1, 1)
        dash_layout.addWidget(Tire_Pressure, 0, 1, 1, 1)
        dash_layout.addWidget(data_cluster_widget, 0, 2, 1, 1)
        dash_layout.addWidget(Sensor_Trends, 1, 0, 1, 2)
        dash_layout.addWidget(System_Log, 1, 2, 1, 1)
        dash_layout.addWidget(Bottom_Log, 2, 0, 1, 3)
        
        self.setLayout(dash_layout)
