from PySide6.QtCore import (
    QThread,
    Signal,
    QObject,
    Signal,
    QTimer
)

import random, socket, time

class NetworkCheckWorker(QThread):
    status_changed = Signal(bool)

    def run(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            self.status_changed.emit(True)
        except OSError:
            self.status_changed.emit(False)

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

        self.link_timer = QTimer(self)
        self.link_timer.timeout.connect(self._check_links)
        self.link_timer.start(3000)
        
        self.health_timer = QTimer(self)
        self.health_timer.timeout.connect(self._check_system_health)
        self.health_timer.start(2000)

        self._sensor_last_seen = {}
        self._sensor_connected = {}

        self.sensor_check_timer = QTimer(self)
        self.sensor_check_timer.timeout.connect(self._check_sensor_staleness)
        self.sensor_check_timer.start(1000)

    def _check_links(self):
        #Simulated
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
    
    def _check_system_health(self):
        #Simulated
        healthy = random.random() > 0.03
        message = "All Systems Normal" if healthy else "Data Pipeline Error"

        if healthy != self._system_healthy:
            self._system_healthy = healthy
            self.system_status_changed.emit(healthy, message)
        
    @property
    def overall_connected(self):
        return self._usb_connected or self._wifi_connected
    
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
