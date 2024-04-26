from view.GUI import GUI
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)

fen = GUI()
fen.show()

app.exec_()