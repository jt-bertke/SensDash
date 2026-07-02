from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout
)

class sensorCard(QWidget):

    def __init__(self, title, value, units):
        super().__init__()

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #555;
                border-radius: 10px;
            }             
        """)

        self.title_label = QLabel(title)
        self.value_label = QLabel(str(value))
        self.units_label = QLabel(units)

        frame_layout = QVBoxLayout()

        frame_layout.addWidget(self.title_label)
        frame_layout.addWidget(self.value_label)
        frame_layout.addWidget(self.units_label)

        frame.setLayout(frame_layout)

        main_layout = QVBoxLayout()

        main_layout.addWidget(frame)

        self.setLayout(main_layout)
