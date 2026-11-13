#Basic window start up
import sys
from PySide6.QtWidgets import (
    QApplication, 
)
from PySide6.QtCore import Qt
from main_window import mainWindow

#Quality of life commands to ensure formatting is not altered
app = QApplication(sys.argv)
app.setStyle("Fusion")

try:
    app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
except AttributeError:
    pass

window = mainWindow()
window.show()

app.exec()