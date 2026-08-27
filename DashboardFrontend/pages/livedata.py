# livedata.py
import time
from collections import deque

import pyqtgraph as pg
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QComboBox,
    QSizePolicy,
)


METRICS = {
    "rpm":               {"label": "Motor Speed",      "unit": "RPM",    "color": "#3B82F6"},
    "motor_current":     {"label": "Motor Current",    "unit": "A",      "color": "#22C55E"},
    "battery_voltage":   {"label": "Battery Voltage",  "unit": "V",      "color": "#EAB308"},
    "coolant_temp":      {"label": "Coolant Temp",     "unit": "\u00b0F","color": "#A855F7"},
    "oil_pressure":      {"label": "Oil Pressure",     "unit": "psi",    "color": "#F97316"},
    "oil_temp":          {"label": "Oil Temp",         "unit": "\u00b0F","color": "#EC4899"},
    "engine_load":       {"label": "Engine Load",      "unit": "%",      "color": "#14B8A6"},
    "throttle_position": {"label": "Throttle Position","unit": "%",      "color": "#F59E0B"},
    "vehicle_speed":     {"label": "Vehicle Speed",    "unit": "mph",    "color": "#60A5FA"},
    "motor_torque":      {"label": "Motor Torque",     "unit": "ft-lbs", "color": "#F472B6"},
    "ambient_temp":      {"label": "Ambient Temp",     "unit": "\u00b0F","color": "#84CC16"},
}

WINDOW_OPTIONS = {
    "30 Seconds": 30,
    "1 Minute": 60,
    "2 Minutes": 120,
    "5 Minutes": 300,
}

STYLE_OPTIONS = ["Line", "Line + Points"]

PAGE_BACKGROUND = "#0D1117"
CARD_BACKGROUND = "#14191f"
CARD_BORDER = "#273341"

COMBO_STYLE = f"""
    QComboBox {{
        background-color: {PAGE_BACKGROUND};
        color: #D1D5DB;
        border: 1px solid {CARD_BORDER};
        border-radius: 6px;
        padding: 5px 10px;
        font-size: 11px;
    }}
    QComboBox:hover {{
        border: 1px solid #3B4657;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 24px;
        border: none;
        background-color: {PAGE_BACKGROUND};
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
    }}
    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 5px solid #6B7280;
        width: 0px;
        height: 0px;
        margin-right: 8px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {CARD_BACKGROUND};
        color: #D1D5DB;
        border: 1px solid {CARD_BORDER};
        selection-background-color: #1F2937;
        selection-color: #FFFFFF;
        outline: none;
        padding: 4px;
    }}
"""


class liveDataPage(QWidget):
    #Expanded single-metric time-series view, fed by the same JSON packet stream as the dashboard.

    MAX_HISTORY_SECONDS = 600

    def __init__(self, telemetry_manager):
        super().__init__()
        self.telemetry_manager = telemetry_manager
        self.history = {key: deque() for key in METRICS}
        self.current_key = "rpm"

        self.setStyleSheet(f"background-color:{PAGE_BACKGROUND};")

        title = QLabel("LIVE DATA")
        title.setStyleSheet("color:#A6B2C2; font-size:14px; font-weight:bold; background:transparent; border:none;")

        # --- Controls ---
        self.metric_selector = QComboBox()
        for key, meta in METRICS.items():
            self.metric_selector.addItem(meta["label"], userData=key)
        self.metric_selector.setCurrentIndex(0)
        self.metric_selector.currentIndexChanged.connect(self._on_metric_changed)

        self.window_selector = QComboBox()
        self.window_selector.addItems(WINDOW_OPTIONS.keys())
        self.window_selector.setCurrentText("1 Minute")
        self.window_selector.currentTextChanged.connect(self._redraw)

        self.style_selector = QComboBox()
        self.style_selector.addItems(STYLE_OPTIONS)
        self.style_selector.currentTextChanged.connect(self._rebuild_curve)

        for combo in (self.metric_selector, self.window_selector, self.style_selector):
            combo.setStyleSheet(COMBO_STYLE)
            combo.setMinimumWidth(160)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(14)
        controls_layout.addWidget(self._labeled(self.metric_selector, "METRIC"))
        controls_layout.addWidget(self._labeled(self.window_selector, "WINDOW"))
        controls_layout.addWidget(self._labeled(self.style_selector, "STYLE"))
        controls_layout.addStretch()

        #Legend
        self.legend_label = QLabel()
        self.legend_label.setStyleSheet("font-size:12px; font-weight:bold; background:transparent; border:none;")

        #Chart, background matched exactly to the card it sits in
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(CARD_BACKGROUND)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.15)

        plot_item = self.plot_widget.getPlotItem()
        plot_item.hideButtons()
        plot_item.vb.setMouseEnabled(x=False, y=False)
        plot_item.getViewBox().setBorder(None)

        for axis_name in ('left', 'bottom'):
            axis = self.plot_widget.getAxis(axis_name)
            axis.setPen(pg.mkPen(CARD_BORDER))
            axis.setTextPen(pg.mkPen('#6B7280'))
        self.plot_widget.getAxis('left').setWidth(50)

        #Card wrapper, matching EcuCard/SystemLog/etc.
        card = QFrame()
        card.setObjectName("LiveDataCard")
        card.setStyleSheet(f"""
            #LiveDataCard {{
                background-color: {CARD_BACKGROUND};
                border: 1px solid {CARD_BORDER};
                border-radius: 10px;
            }}
        """)
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)
        card_layout.addWidget(self.legend_label)
        card_layout.addWidget(self.plot_widget, 1)
        card.setLayout(card_layout)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)
        main_layout.addWidget(title)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(card, 1)
        self.setLayout(main_layout)

        self.curve = None
        self._rebuild_curve()

        self.telemetry_manager.packet_received.connect(self._on_packet)

    def _labeled(self, widget, label_text):
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        layout = QVBoxLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(label_text)
        label.setStyleSheet("color:#6B7280; font-size:9px; background:transparent; border:none;")
        layout.addWidget(label)
        layout.addWidget(widget)
        wrapper.setLayout(layout)
        return wrapper

    def _on_metric_changed(self, index):
        self.current_key = self.metric_selector.itemData(index)
        self._rebuild_curve()

    def _rebuild_curve(self):
        self.plot_widget.getPlotItem().clear()

        meta = METRICS[self.current_key]
        use_points = self.style_selector.currentText() == "Line + Points"
        pen = pg.mkPen(meta["color"], width=2)

        self.curve = self.plot_widget.getPlotItem().plot(
            pen=pen,
            symbol='o' if use_points else None,
            symbolSize=4,
            symbolBrush=meta["color"],
            symbolPen=None,
        )

        self.legend_label.setText(f"{meta['label']} ({meta['unit']})")
        self.legend_label.setStyleSheet(
            f"color:{meta['color']}; font-size:12px; font-weight:bold; background:transparent; border:none;"
        )
        self._redraw()

    def _on_packet(self, packet):
        now = time.time()
        for key in METRICS:
            if key in packet:
                buf = self.history[key]
                buf.append((now, packet[key]))
                cutoff = now - self.MAX_HISTORY_SECONDS
                while buf and buf[0][0] < cutoff:
                    buf.popleft()
        self._redraw()

    def _redraw(self):
        if self.curve is None:
            return

        window = WINDOW_OPTIONS[self.window_selector.currentText()]
        now = time.time()
        cutoff = now - window

        buf = self.history[self.current_key]
        points = [(t - now, v) for t, v in buf if t >= cutoff]

        if points:
            times = [p[0] for p in points]
            values = [p[1] for p in points]
            self.curve.setData(times, values)
        else:
            self.curve.setData([], [])

        self.plot_widget.setXRange(-window, 0, padding=0)
        self.plot_widget.enableAutoRange(axis='y')