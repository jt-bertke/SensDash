from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy
)

import time

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

    def __init__(self, connection_manager, telemetry_manager):
        super().__init__()
        self.connection_manager = connection_manager
        self.telemetry_manager = telemetry_manager
        self._known_fault_codes = set()

        # --- 3x2 sensor grid ---
        data_cluster = QGridLayout()
        data_cluster.setContentsMargins(0, 0, 0, 0)
        data_cluster.setSpacing(3)
        for row in range(3):
            data_cluster.setRowStretch(row, 1)
        for col in range(2):
            data_cluster.setColumnStretch(col, 1)

        self.compass_card = CompassCard()

        self.oil_card = DualStatCard(
            "OIL PRESSURE / TEMP",
            "Pressure", "--", "psi",
            "Temp", "--", "°F",
        )

        self.mileage_card = DualStatCard(
            "GAS MILEAGE",
            "Instant", "--", "mpg",
            "Average", "--", "mpg",
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
            units="°F"
        )

        data_cluster.addWidget(self.compass_card, 0, 0)
        data_cluster.addWidget(self.oil_card, 0, 1)
        data_cluster.addWidget(self.mileage_card, 1, 0)
        data_cluster.addWidget(self.trip_card, 1, 1)
        data_cluster.addWidget(self.placeholder_card, 2, 0)
        data_cluster.addWidget(self.motor_temp_card, 2, 1)

        data_cluster_widget = QWidget()
        data_cluster_widget.setLayout(data_cluster)
        data_cluster_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.Ecu_card = EcuCard()
        self.Tire_Pressure = TirePressureCard()
        self.Sensor_Trends = SensorTrends()
        self.System_Log = SystemLog(connection_manager, [
            "RPM", "Motor Current", "Battery Voltage", "Coolant Temp",
            "Oil Pressure", "Oil Temp", "Compass/Heading", "Gas Mileage",
        ])
        self.Bottom_Log = BottomLog()

        dash_layout = QGridLayout()
        dash_layout.setSpacing(12)
        dash_layout.setColumnStretch(0, 1)
        dash_layout.setColumnStretch(1, 1)
        dash_layout.setColumnStretch(2, 1)
        dash_layout.setRowStretch(0, 5)
        dash_layout.setRowStretch(1, 3)
        dash_layout.setRowStretch(2, 1)

        dash_layout.addWidget(self.Ecu_card, 0, 0, 1, 1)
        dash_layout.addWidget(self.Tire_Pressure, 0, 1, 1, 1)
        dash_layout.addWidget(data_cluster_widget, 0, 2, 1, 1)
        dash_layout.addWidget(self.Sensor_Trends, 1, 0, 1, 2)
        dash_layout.addWidget(self.System_Log, 1, 2, 1, 1)
        dash_layout.addWidget(self.Bottom_Log, 2, 0, 1, 3)

        self.setLayout(dash_layout)

        self.telemetry_manager.packet_received.connect(self._on_packet)

    def _on_packet(self, packet):
        if "rpm" in packet:
            self.motor_temp_card 

        if "rpm" in packet:
            self.connection_manager.report_sensor_data("RPM")
        if "motor_current" in packet:
            self.connection_manager.report_sensor_data("Motor Current")
        if "battery_voltage" in packet:
            self.Bottom_Log.update_value("battery_voltage", f"{packet['battery_voltage']:.1f}")
            self.connection_manager.report_sensor_data("Battery Voltage")
        if "coolant_temp" in packet:
            self.motor_temp_card.update_value(f"{packet['coolant_temp']:.0f}")
            self.connection_manager.report_sensor_data("Coolant Temp")
        if "oil_pressure" in packet:
            self.oil_card.update_value1(f"{packet['oil_pressure']:.0f}")
            self.connection_manager.report_sensor_data("Oil Pressure")
        if "oil_temp" in packet:
            self.oil_card.update_value2(f"{packet['oil_temp']:.0f}")
            self.connection_manager.report_sensor_data("Oil Temp")
        if "engine_load" in packet:
            self.Ecu_card.update_engine_load(packet["engine_load"])
        if "throttle_position" in packet:
            self.Ecu_card.update_throttle_position(packet["throttle_position"])
        if "heading" in packet:
            self.compass_card.update_heading(packet["heading"])
            self.connection_manager.report_sensor_data("Compass/Heading")
        if "instant_mpg" in packet:
            self.mileage_card.update_value1(f"{packet['instant_mpg']:.1f}")
        if "avg_mpg" in packet:
            self.mileage_card.update_value2(f"{packet['avg_mpg']:.1f}")
            self.connection_manager.report_sensor_data("Gas Mileage")
        if "trip_a" in packet:
            self.trip_card.update_value1(f"{packet['trip_a']:.1f}")
        if "trip_b" in packet:
            self.trip_card.update_value2(f"{packet['trip_b']:.1f}")

        for key, pos in (("tire_fl", "fl"), ("tire_fr", "fr"), ("tire_rl", "rl"), ("tire_rr", "rr")):
            if key in packet:
                self.Tire_Pressure.update_tire(pos, packet[key])

        if "vehicle_speed" in packet:
            self.Bottom_Log.update_value("vehicle_speed", f"{packet['vehicle_speed']:.1f}")
        if "motor_torque" in packet:
            self.Bottom_Log.update_value("motor_torque", f"{packet['motor_torque']:.1f}")
        if "drive_state" in packet:
            self.Bottom_Log.update_value("drive_state", packet["drive_state"])
        if "ambient_temp" in packet:
            self.Bottom_Log.update_value("ambient_temp", f"{packet['ambient_temp']:.1f}")

        if all(k in packet for k in ("rpm", "motor_current", "battery_voltage", "coolant_temp")):
            self.Sensor_Trends.add_data_point(
                time.time(),
                rpm=packet["rpm"],
                current=packet["motor_current"],
                voltage=packet["battery_voltage"],
                temp=packet["coolant_temp"],
            )

        if "faults" in packet:
            current_codes = {f["code"] for f in packet["faults"]}
            for fault in packet["faults"]:
                if fault["code"] not in self._known_fault_codes:
                    self.Ecu_card.add_fault(fault["code"], fault["description"])
            if not current_codes and self._known_fault_codes:
                self.Ecu_card._set_no_faults()
            self._known_fault_codes = current_codes
