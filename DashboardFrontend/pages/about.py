from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSizePolicy,
    QScrollArea,
)
from PySide6.QtCore import Qt
import qtawesome as qta

#Simple about page for my application. This doesn't really serve any purpose
#Other than making the application look polished.
class aboutPage(QWidget):

    def __init__(self):
        super().__init__()

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setSpacing(16)

        header = QHBoxLayout()
        header.setSpacing(14)

        logo = QLabel()
        logo_icon = qta.icon("ph.gauge-bold", color="#3B82F6")
        logo.setPixmap(logo_icon.pixmap(36, 36))

        title_block = QVBoxLayout()
        title_block.setSpacing(2)

        app_name = QLabel("SensDash")
        app_name.setStyleSheet("color:#FFFFFF; font-size:22px; font-weight:bold; border:none; background:transparent;")

        version = QLabel("v1.0.0")
        version.setStyleSheet("color:#6B7280; font-size:12px; border:none; background:transparent;")

        title_block.addWidget(app_name)
        title_block.addWidget(version)

        header.addWidget(logo)
        header.addLayout(title_block)
        header.addStretch()

        description_card = self._build_card(
            "ABOUT",
            "SensDash is a custom sensor telemetry dashboard built for personal use, "
            "displaying live engine, drivetrain, and diagnostic data streamed over a "
            "radio telemetry link from a Raspberry Pi reading OBD-II data. This is a "
            "hobby project — built for the fun of building it, not for commercial use."
        )

        vehicle_card = self._build_card(
            "VEHICLE",
            "2009 Jeep Grand Cherokee Laredo\n3.7L V6 \u2014 AWD"
        )

        tech_items = [
            ("Python", "mdi.language-python"),
            ("PySide6 (Qt)", "mdi.widgets"),
            ("pyqtgraph", "mdi.chart-line"),
            ("python-OBD", "mdi.car-cog"),
            ("Radio Telemetry", "mdi.antenna"),
        ]
        tech_card = self._build_icon_list_card("TECH STACK", tech_items)

        outer_layout.addLayout(header)
        outer_layout.addWidget(description_card)
        outer_layout.addWidget(vehicle_card)
        outer_layout.addWidget(tech_card)
        outer_layout.addStretch()

        self.setLayout(outer_layout)

    def _build_card(self, title_text, body_text):
        card = QFrame()
        card.setObjectName("AboutCard")
        card.setStyleSheet("""
            #AboutCard {
                background-color:#14191f;
                border:1px solid #273341;
                border-radius:10px;
            }
        """)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        title = QLabel(title_text)
        title.setStyleSheet("""
            color:#A6B2C2; font-size:12px; font-weight:bold;
            border:none; background:transparent;
        """)

        body = QLabel(body_text)
        body.setWordWrap(True)
        body.setStyleSheet("""
            color:#D1D5DB; font-size:12px; line-height:150%;
            border:none; background:transparent;
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addWidget(body)
        card.setLayout(layout)
        return card

    def _build_icon_list_card(self, title_text, items):
        card = QFrame()
        card.setObjectName("AboutCard")
        card.setStyleSheet("""
            #AboutCard {
                background-color:#14191f;
                border:1px solid #273341;
                border-radius:10px;
            }
        """)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        title = QLabel(title_text)
        title.setStyleSheet("""
            color:#A6B2C2; font-size:12px; font-weight:bold;
            border:none; background:transparent;
        """)

        items_layout = QVBoxLayout()
        items_layout.setSpacing(10)
        items_layout.setContentsMargins(0, 4, 0, 0)

        for label_text, icon_name in items:
            row = QHBoxLayout()
            row.setSpacing(10)

            icon_label = QLabel()
            icon = qta.icon(icon_name, color="#6B7280")
            icon_label.setPixmap(icon.pixmap(16, 16))

            text_label = QLabel(label_text)
            text_label.setStyleSheet("color:#D1D5DB; font-size:12px; border:none; background:transparent;")

            row.addWidget(icon_label)
            row.addWidget(text_label)
            row.addStretch()

            row_widget = QWidget()
            row_widget.setStyleSheet("background:transparent;")
            row_widget.setLayout(row)
            items_layout.addWidget(row_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addLayout(items_layout)
        card.setLayout(layout)
        return card