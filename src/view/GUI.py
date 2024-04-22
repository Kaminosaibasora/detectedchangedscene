import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox, QAction, QFileDialog, QPushButton, QLabel, QLineEdit, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QIcon
from view.ListFileWidget import ListFileWidget
from view.VideoPlayerWidget import VideoPlayerWidget
from engine.LoadConfig import LoadConfig
from engine.VideoTraitment import VideoTraitement
from view.LoadingWindow import EcranChargement
from view.LoadingWindow import ChargementThread
from view.FrameManagementWidget import FrameManagementWidget

class GUI(QMainWindow):

    video_traitement = None
    load_config = None

    def __init__(self, parent=None) -> None:
        super(GUI, self).__init__(parent)
        self.setWindowTitle("Detected Changed Scene")
        self.load_config = LoadConfig()

        # Widget

        # - - HOME
        self.list_widget        = ListFileWidget()
        self.list_widget        .list_widget.clicked.connect(self.click_choose_path)
        self.label_video_choose = QLabel()
        self.label_video_choose .setText("Vidéo choisie")
        self.video_player       = VideoPlayerWidget()
        self.button_analyse     = QPushButton("Analyse")
        self.button_analyse.clicked.connect(self.launch_analyse)
        self.button_analyse.setVisible(False)
        # - - ANALYSE
        self.button_back = QPushButton("BACK")
        self.button_back.clicked.connect(self.back_file_list)
        self.list_frame_widget = FrameManagementWidget()
        self.button_valid = QPushButton("VALIDATION")

        # LAYOUT

        self.layout = QGridLayout()
        self.layout.addWidget(self.list_widget,        0, 0, 3, 1)
        self.layout.addWidget(self.label_video_choose, 0, 1, 1, 4, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.video_player,       1, 1, 2, 4, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.button_analyse,     3, 1, 1, 4, alignment=Qt.AlignHCenter)

        self.wid_selected_file = QWidget(self)
        self.wid_selected_file .setLayout(self.layout)

        self.layout_work_frame = QGridLayout()
        self.layout_work_frame.addWidget(self.button_back,   1, 0, 1, 1)
        self.layout_work_frame.addWidget(self.list_frame_widget,    0, 1, 3, 4)
        self.layout_work_frame.addWidget(self.button_valid,  1, 5, 3, 1)

        self.wid_manage_frame = QWidget(self)
        self.wid_manage_frame .setLayout(self.layout_work_frame)
        self.wid_manage_frame.setVisible(False)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.wid_selected_file)
        self.stacked_widget.addWidget(self.wid_manage_frame)

        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.stacked_widget)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        # self.setCentralWidget(self.wid_selected_file)
        self.resize(1200, 720)

        # CHARGEMENT DES DONNEES
        if (self.load_config.path_folder_in != "") :
            self.list_widget.folder_path = self.load_config.path_folder_in
            self.list_widget.maj_folder()

    def click_choose_path(self, line) -> None:
        """
        Sélectionne un fichier lors du clique dans la liste
        Args:
            line (_type_): information inclue dans l'item cliqué
        """
        self.list_widget.linecurrent = line
        self.label_video_choose      .setText(line.data())
        self.list_widget.file_choose = line.data()
        self.button_analyse.setVisible(True)
        # Charger la vidéo dans le lecteur
        self.video_player.loadMedia(self.list_widget.get_file_path())
        self.video_player.play_pause()
        # confirmer la configuration
        self.load_config.path_folder_in = self.list_widget.folder_path
    
    def launch_analyse(self) -> None:
        """
        Passe sur la page d'analyse des frame et lance l'analyse
        TODO : écran de chargement d'analyse + thread pour éviter le blocage du programme
        """
        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_index)

        # Traitement de la vidéo

        self.video_traitement = VideoTraitement(self.list_widget.get_file_path())
        self.ecran_chargement = EcranChargement()
        self.ecran_chargement.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ecran_chargement.show()
        self.thread_chargement = ChargementThread(self.video_traitement)
        self.thread_chargement.fin_chargement.connect(self.fin_chargement)
        self.thread_chargement.start()
    
# ====================================================================================
# --------------------------- ANALYSE PAGE -------------------------------------------
# ====================================================================================
    
    def fin_chargement(self):
        self.ecran_chargement.close()
        # print(self.video_traitement.frame_change)
        self.list_frame_widget.addFrame(
            self.video_traitement.frame_change, 
            self.video_traitement.temp_path
        )

    def back_file_list(self) -> None:
        """
        Retour à la page de sélection vidéo
        TODO : vide les fichiers temporaire et supprimer l'instance de travail.
        """
        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_index)

# ====================================================================================
# ________________________________________ A L L _____________________________________
# ====================================================================================

    def closeEvent(self, event) -> None:
        self.load_config.save()