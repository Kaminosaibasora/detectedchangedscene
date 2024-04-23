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
        # frame = self.video_traitement.detected_scene()
        frame = [0, 407, 423, 455, 487, 534, 566, 582, 596, 615, 640, 672, 699, 701, 739, 761, 776, 778, 806, 824, 840, 858, 869, 873, 903, 929, 956, 1033, 1090, 1092, 1093, 1094, 1095, 1103, 1104, 1105, 1107, 1108, 1109, 1115, 1119, 1120, 1122, 1147, 1173, 1199, 1219, 1249, 1261, 1291, 1309, 1344, 1382, 1418, 1443, 1479, 1505, 1525, 1551, 1562, 1571, 1585, 1612, 1631, 1637, 1638, 1640, 1666, 1718, 1750, 1822, 1845, 1866]
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