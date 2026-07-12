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
    DriveTrainCard,
    SensorTrends,
    SystemLog,
    BottomLog
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

        rpm_card = sensorCard(
            title="Motor Speed",
            value=2500,
            units="RPM"
        )

        temp_card = sensorCard(
            title="Temperature",
            value=68,
            units="F"
        )

        voltage_card = sensorCard(
            title="Voltage",
            value=12.6,
            units="V"
        )

        current_card = sensorCard(
            title="Current",
            value=3.42,
            units="A"
        )

        blank_card1 = sensorCard(
            title="N/A",
            value = 0.00,
            units="N/A"
        )

        blank_card2 = sensorCard(
            title="N/A",
            value = 0.00,
            units="N/A"
        )

        data_cluster.addWidget(rpm_card, 0, 0)
        data_cluster.addWidget(temp_card, 0, 1)
        data_cluster.addWidget(voltage_card, 1, 0)
        data_cluster.addWidget(current_card, 1, 1)
        data_cluster.addWidget(blank_card1, 2,0)
        data_cluster.addWidget(blank_card2, 2,1)


        data_cluster_widget = QWidget()
        data_cluster_widget.setLayout(data_cluster)
        data_cluster_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        Ecu_card = EcuCard()
        Drive_Train = DriveTrainCard()

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
        dash_layout.addWidget(Drive_Train, 0, 1, 1, 1)
        dash_layout.addWidget(data_cluster_widget, 0, 2, 1, 1)
        dash_layout.addWidget(Sensor_Trends, 1, 0, 1, 2)
        dash_layout.addWidget(System_Log, 1, 2, 1, 1)
        dash_layout.addWidget(Bottom_Log, 2, 0, 1, 3)
        
        self.setLayout(dash_layout)
