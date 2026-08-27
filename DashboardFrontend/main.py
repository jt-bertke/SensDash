#Basic window start up
import sys
from PySide6.QtWidgets import (
    QApplication, 
)
from main_window import mainWindow

#Quality of life commands to ensure formatting is not altered
app = QApplication(sys.argv)
app.setStyle("Fusion")

window = mainWindow()
window.show()

app.exec()