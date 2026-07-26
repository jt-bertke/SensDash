import sys
from PySide6.QtWidgets import (
    QApplication, 
)
from main_window import mainWindow

app = QApplication(sys.argv)
app.setStyle("Fusion")

window = mainWindow()
window.show()

app.exec()