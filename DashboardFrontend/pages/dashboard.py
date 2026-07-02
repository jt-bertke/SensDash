from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)

class dashboardPage(QWidget):

    def __init__(self):
        super().__init__()
        
        gauge_layout = QVBoxLayout(self)

        rpm_gauge = QFrame()
        rpm_gauge.setFrameShape(QFrame.SyledPanel)

        card_layout = QVBoxLayout(rpm_gauge)

        rpm_label = QLabel("RPM")
        card_layout.addWidget(rpm_label)

        gauge_layout.addWidget(rpm_gauge)
