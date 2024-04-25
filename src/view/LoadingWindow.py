from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QMovie

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

class ValidateThread(QThread):
    end_work         = pyqtSignal()
    video_traitement = None

    def __init__(self, video_traitement, parent=None) -> None:
        super().__init__(parent)
        self.video_traitement = video_traitement
    
    def run(self):
        self.video_traitement.writer_video_scene()
        self.end_work.emit()

class EcranChargement(QDialog):
    """
    Fenêtre de chargement externe.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Chargement")
        self.setFixedSize(300, 300)

        label = QLabel("Chargement en cours...\nCela peut prendre plusieurs minutes.")
        label_load = QLabel()
        loading = QMovie("./asset/load.gif")
        label_load.setMovie(loading)
        loading.setScaledSize(self.size())
        loading.start()

        layout = QVBoxLayout()
        layout .addWidget(label)
        layout .addWidget(label_load)

        self.setLayout(layout)