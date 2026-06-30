from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QLabel, 
    QVBoxLayout
)

#Setting up Main Window child class pulling from QMainWindow
class MainWindow(QMainWindow):
    
    #Defining initialization of object
    def __init__(self):
        
        #Allows init to pull from MainWindow
        super().__init__()
        
        #Setting Window title and default window size on startup
        self.setWindowTitle("Sensor Dashboard")
        self.resize(800, 500)

        #Setting up taskbar
        menu = self.menuBar()
        home_menu = menu.addMenu("Home")
        settings_menu = menu.addMenu("Settings")

        #Create Individual Widgets 
        self.sensor_label = QLabel("Sensor Value: 0")

        #Setup Layout of Widget Cluster (VBox is a standard layout)
        layout = QVBoxLayout()
        #This actually adds the widgets to the layout
        layout.addWidget(self.sensor_label)

        #Setting up widget cluster (typically have more than one)
        widget = QWidget()
        #Setting Widget cluster Layout
        widget.setLayout(layout)
        #Makes "widget cluster" main body of GUI
        self.setCentralWidget(widget)