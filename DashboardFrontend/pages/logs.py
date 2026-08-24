import csv
from datetime import datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QFileDialog,
    QMessageBox,
    QSizePolicy,
)
import qtawesome as qta


class logsPage(QWidget):
    """
    Simple data logger page: lists recorded sensor sessions and lets the
    user export them to CSV. Session data is currently placeholder/dummy
    data -- swap `self.sessions` population for real records once the
    Pi telemetry pipeline is writing logs.
    """

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #11161D;")

        #Placeholder session data
        # Each session represents one logged drive. `records` holds the
        # actual per-row sensor data that gets written out on export.
        self.sessions = self._generate_dummy_sessions()

        #Header
        title = QLabel("Data Logger")
        title.setStyleSheet("""
            color: #FFFFFF;
            font-size: 20px;
            font-weight: bold;
        """)

        subtitle = QLabel("Review and export recorded sensor sessions")
        subtitle.setStyleSheet("""
            color: #6B7280;
            font-size: 12px;
        """)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(2)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        #Toolbar (export / clear buttons)
        self.export_selected_btn = QPushButton(" Export Selected")
        self.export_selected_btn.setIcon(qta.icon("fa5s.file-export", color="#FFFFFF"))

        self.export_all_btn = QPushButton(" Export All")
        self.export_all_btn.setIcon(qta.icon("fa5s.file-download", color="#FFFFFF"))

        self.clear_btn = QPushButton(" Clear Log")
        self.clear_btn.setIcon(qta.icon("fa5s.trash-alt", color="#FFFFFF"))

        for btn in (self.export_selected_btn, self.export_all_btn, self.clear_btn):
            btn.setFixedHeight(36)
            btn.setCursor(Qt.PointingHandCursor)

        self.export_selected_btn.setStyleSheet(self._button_style(accent=True))
        self.export_all_btn.setStyleSheet(self._button_style(accent=True))
        self.clear_btn.setStyleSheet(self._button_style(accent=False))

        self.export_selected_btn.clicked.connect(self.export_selected)
        self.export_all_btn.clicked.connect(self.export_all)
        self.clear_btn.clicked.connect(self.clear_log)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.export_selected_btn)
        toolbar_layout.addWidget(self.export_all_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.clear_btn)

        #Session table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Session", "Date", "Duration", "Records", "Size"]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for col in range(1, 5):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #14191f;
                border: 1px solid #273341;
                border-radius: 10px;
                color: #E5E7EB;
                gridline-color: #273341;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #1A222C;
                color: #9CA3AF;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #273341;
                font-size: 11px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: rgba(59,130,246,0.25);
                color: #FFFFFF;
            }
        """)

        self._populate_table()

        table_frame = QFrame()
        table_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_frame_layout = QVBoxLayout()
        table_frame_layout.setContentsMargins(0, 0, 0, 0)
        table_frame_layout.addWidget(self.table)
        table_frame.setLayout(table_frame_layout)

        #Status label (bottom)
        self.status_label = QLabel(f"{len(self.sessions)} session(s) logged")
        self.status_label.setStyleSheet("""
            color: #6B7280;
            font-size: 11px;
        """)

        #Page layout
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)
        layout.addLayout(header_layout)
        layout.addLayout(toolbar_layout)
        layout.addWidget(table_frame)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    # Styling helper
    def _button_style(self, accent=True):
        if accent:
            return """
                QPushButton {
                    background-color: #3B82F6;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 8px;
                    padding: 0px 14px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563EB;
                }
            """
        return """
            QPushButton {
                background-color: transparent;
                color: #EF4444;
                border: 1px solid #273341;
                border-radius: 8px;
                padding: 0px 14px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(239,68,68,0.1);
            }
        """

    # Dummy data generation (swap out once real telemetry logging exists)
    def _generate_dummy_sessions(self):
        now = datetime.now()
        return [
            {
                "id": "SESSION-001",
                "date": now - timedelta(days=2, hours=1),
                "duration_sec": 1832,
                "records": [
                    {"time_s": t, "rpm": 2400 + (t % 300), "coolant_temp_f": 195 + (t % 5)}
                    for t in range(0, 1832, 60)
                ],
            },
            {
                "id": "SESSION-002",
                "date": now - timedelta(days=1, hours=4),
                "duration_sec": 942,
                "records": [
                    {"time_s": t, "rpm": 1800 + (t % 200), "coolant_temp_f": 190 + (t % 4)}
                    for t in range(0, 942, 60)
                ],
            },
            {
                "id": "SESSION-003",
                "date": now - timedelta(hours=6),
                "duration_sec": 2710,
                "records": [
                    {"time_s": t, "rpm": 2100 + (t % 400), "coolant_temp_f": 198 + (t % 6)}
                    for t in range(0, 2710, 60)
                ],
            },
        ]

    # Table population
    def _populate_table(self):
        self.table.setRowCount(len(self.sessions))
        for row, session in enumerate(self.sessions):
            duration = str(timedelta(seconds=session["duration_sec"]))
            size_kb = max(1, len(session["records"]) * 3 // 10)

            values = [
                session["id"],
                session["date"].strftime("%Y-%m-%d %H:%M"),
                duration,
                str(len(session["records"])),
                f"{size_kb} KB",
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col != 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    # Export logic
    def _write_sessions_to_csv(self, sessions, filepath):
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["session_id", "session_date", "time_s", "rpm", "coolant_temp_f"])
            for session in sessions:
                for record in session["records"]:
                    writer.writerow([
                        session["id"],
                        session["date"].strftime("%Y-%m-%d %H:%M:%S"),
                        record["time_s"],
                        record["rpm"],
                        record["coolant_temp_f"],
                    ])

    def export_selected(self):
        selected_rows = sorted({idx.row() for idx in self.table.selectedIndexes()})
        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Select one or more sessions to export.")
            return

        sessions_to_export = [self.sessions[r] for r in selected_rows]
        self._prompt_and_export(sessions_to_export, default_name="sensdash_selected_log.csv")

    def export_all(self):
        if not self.sessions:
            QMessageBox.information(self, "No Data", "There are no sessions to export.")
            return
        self._prompt_and_export(self.sessions, default_name="sensdash_full_log.csv")

    def _prompt_and_export(self, sessions, default_name):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log Export",
            default_name,
            "CSV Files (*.csv)"
        )
        if not filepath:
            return

        try:
            self._write_sessions_to_csv(sessions, filepath)
            QMessageBox.information(self, "Export Complete", f"Saved {len(sessions)} session(s) to:\n{filepath}")
        except OSError as e:
            QMessageBox.critical(self, "Export Failed", f"Could not write file:\n{e}")

    # Clear log
    def clear_log(self):
        if not self.sessions:
            return

        confirm = QMessageBox.question(
            self,
            "Clear Log",
            "This will remove all logged sessions from the current view. Continue?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.sessions = []
            self._populate_table()
            self.status_label.setText("0 session(s) logged")

    # Future integration hook
    def add_session(self, session_id, date, records):
        """
        Append a real logged session (e.g. once telemetry data starts
        flowing from ConnectionManager). `records` should be a list of
        dicts matching the keys used in _write_sessions_to_csv.
        """
        duration_sec = records[-1]["time_s"] if records else 0
        self.sessions.append({
            "id": session_id,
            "date": date,
            "duration_sec": duration_sec,
            "records": records,
        })
        self._populate_table()
        self.status_label.setText(f"{len(self.sessions)} session(s) logged")