from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from engine.VideoTraitment import VideoTraitement

class ChargementThread(QThread):

    fin_chargement   = pyqtSignal()
    video_traitement = None

    def __init__(self, video_traitment, parent=None) -> None:
        """
        Args:
            video_traitment (VideoTraitement): instance de traitement vidéo.
        """
        super().__init__(parent)
        self.video_traitement = video_traitment

    def run(self):
        """
        Lance la décomposition de la vidéo et la détection de scène.
        """
        self.video_traitement.decompose_img()
        frame = self.video_traitement.detected_scene()
        self.fin_chargement.emit()

class EcranChargement(QDialog):
    """
    Fenêtre de chargement externe.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Chargement")
        self.setFixedSize(200, 100)

        layout      = QVBoxLayout()
        self.label  = QLabel("Chargement en cours...")
        layout.addWidget(self.label)

        self.setLayout(layout)