from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QFrame
)

from pages.utilities.cards import sensorCard

class dashboardPage(QWidget):

    def __init__(self):
        super().__init__()
        
        layout = QGridLayout()

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

        layout.addWidget(rpm_card, 0, 0)
        layout.addWidget(temp_card, 0, 1)
        layout.addWidget(voltage_card, 1, 0)
        layout.addWidget(current_card, 1, 1)

        self.setLayout(layout)
