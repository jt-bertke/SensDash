import os
import tempfile

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

import qtawesome as qta

BG = "#11161D"
CARD_BG = "#14191f"
BORDER = "#273341"
TEXT = "#FFFFFF"
TEXT_BODY = "#D1D5DB"
TEXT_SECONDARY = "#A6B2C2"
TEXT_MUTED = "#6b7280"
ACCENT = "#3B82F6"
SUCCESS = "#3CCF4E"
WARNING = "#EAB308"
DANGER = "#EF4444"

RADIUS = 10
PAGE_MARGIN = 20

CARD_TITLE_STYLE = (
    f"color:{TEXT_SECONDARY}; font-size:12px; font-weight:bold;"
    "border:none; background:transparent;"
)

_chevron_file = None

def chevron_path():
    global _chevron_file
    if _chevron_file is None:
        path = os.path.join(tempfile.gettempdir(), "sensdash_chevron_down.png")
        qta.icon("fa5s.chevron-down", color=TEXT_MUTED).pixmap(20,20).save(path, "PNG")
        _chevron_file = path.replace("\\", "/")
    return _chevron_file

class PageHeader(QWidget):

    def __init__(self,title, subtitle=None):
        super().__init__()
        self.setStyleSheet("background:transparent;")

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"color:{TEXT}; font-size:20px; font-weight:bold; border:none; background:transparent;"

        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(2)
        layout.addWidget(title_label)

        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet(
                f"color:{TEXT_MUTED}; font-size:12px; border:none; background:transparent;"

            )
            layout.addWidget(subtitle_label)
        self.setLayout(layout)    
    