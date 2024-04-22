import sys
import time
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QPushButton
from engine.VideoTraitment import VideoTraitement

class ChargementThread(QThread):

    fin_chargement = pyqtSignal()
    video_traitement = None

    def __init__(self, video_traitment, parent=None) -> None:
        super().__init__(parent)
        self.video_traitement = video_traitment

    def run(self):
        # self.video_traitement.decompose_img()
        frame = self.video_traitement.detected_scene()
        self.fin_chargement.emit()

class EcranChargement(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chargement")
        self.setFixedSize(200, 100)

        layout = QVBoxLayout()
        self.label = QLabel("Chargement en cours...")
        layout.addWidget(self.label)

        self.setLayout(layout)