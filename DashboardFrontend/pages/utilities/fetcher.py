#The fetcher file holds some logic of the future data stream. It is
# mostly dummy data but will be setup to handle the data from the Pi.
# Some classes are not being used anymore, but I haven't removed them
# just in case I want to use them in the future.

from PySide6.QtCore import (
    QThread,
    Signal,
    QObject,
    Signal,
    QTimer
)

import random, time

class ConnectionManager(QObject):
    usb_changed = Signal(bool)
    wifi_changed = Signal(bool)
    overall_connection_changed = Signal(bool)    
    system_status_changed = Signal(bool, str)     
    sensor_status_changed = Signal(str, bool)   

    SENSOR_STALE_THRESHOLD = 3.0 

    def __init__(self):
        super().__init__()
        self._usb_connected = True
        self._wifi_connected = True
        self._system_healthy = True
        self._sensor_last_seen = {}
        self._sensor_connected = {}

        self.link_timer = QTimer(self)
        self.link_timer.timeout.connect(self._check_links)
        self.link_timer.start(3000)

        self.health_timer = QTimer(self)
        self.health_timer.timeout.connect(self._check_system_health)
        self.health_timer.start(2000)

        self.sensor_check_timer = QTimer(self)
        self.sensor_check_timer.timeout.connect(self._check_sensor_staleness)
        self.sensor_check_timer.start(1000)

    def _check_links(self):
        new_usb = random.random() > 0.05
        new_wifi = random.random() > 0.05

        if new_usb != self._usb_connected:
            self._usb_connected = new_usb
            self.usb_changed.emit(new_usb)
            self._emit_overall()

        if new_wifi != self._wifi_connected:
            self._wifi_connected = new_wifi
            self.wifi_changed.emit(new_wifi)
            self._emit_overall()

    def _emit_overall(self):
        connected = self._usb_connected or self._wifi_connected
        self.overall_connection_changed.emit(connected)

    @property
    def overall_connected(self):
        return self._usb_connected or self._wifi_connected

    def _check_system_health(self):
        healthy = random.random() > 0.03
        message = "All Systems Normal" if healthy else "Data Pipeline Error"

        if healthy != self._system_healthy:
            self._system_healthy = healthy
            self.system_status_changed.emit(healthy, message)

    # --- Per-sensor connectivity ---
    def register_sensor(self, name):
        if name not in self._sensor_connected:
            self._sensor_connected[name] = False
            self._sensor_last_seen[name] = 0

    def report_sensor_data(self, name):
        self._sensor_last_seen[name] = time.time()
        if not self._sensor_connected.get(name, False):
            self._sensor_connected[name] = True
            self.sensor_status_changed.emit(name, True)

    def _check_sensor_staleness(self):
        now = time.time()
        for name, last_seen in self._sensor_last_seen.items():
            connected = (now - last_seen) < self.SENSOR_STALE_THRESHOLD
            if connected != self._sensor_connected.get(name, False):
                self._sensor_connected[name] = connected
                self.sensor_status_changed.emit(name, connected)

class TelemetryManager(QObject):
    packet_received = Signal(dict)

    def ingest(self, packet):
        self.packet_received.emit(packet)

class SimulatedFeed(QObject):
    
    def __init__(self, telemetry_manager, connection_manager, interval_ms=500):
        super().__init__()
        self.telemetry_manager = telemetry_manager
        self.connection_manager = connection_manager
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.interval_ms = interval_ms

    def start(self):
        self.timer.start(self.interval_ms)
    
    def stop(self):
        self.timer.stop()
    
    def _tick(self):
        packet = {
            "rpm": random.uniform(700, 4000),
            "motor_current": random.uniform(20, 40),
            "battery_voltage": random.uniform(12.0, 14.4),
            "coolant_temp": random.uniform(180, 220),
            "oil_pressure": random.uniform(25, 60),
            "oil_temp": random.uniform(190, 240),
            "engine_load": random.uniform(10, 80),
            "throttle_position": random.uniform(0, 100),
            "heading": random.uniform(0, 360),
            "instant_mpg": random.uniform(15, 28),
            "avg_mpg": 19.8,
            "trip_a": 293.0,
            "trip_b": 1042.3,
            "tire_fl": random.uniform(30, 36),
            "tire_fr": random.uniform(30, 36),
            "tire_rl": random.uniform(30, 36),
            "tire_rr": random.uniform(30, 36),
            "vehicle_speed": random.uniform(0, 70),
            "motor_torque": random.uniform(100, 260),
            "drive_state": "D",
            "ambient_temp": random.uniform(60, 90),
            "faults": [],
        }
        self.telemetry_manager.ingest(packet)

        for sensor_name in ("RPM", "Motor Current", "Battery Voltage", "Coolant Temp",
                             "Oil Pressure", "Oil Temp", "Compass/Heading", "Gas Mileage"):
            self.connection_manager.report_sensor_data(sensor_name)
