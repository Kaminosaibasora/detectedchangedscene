from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QStackedWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from view.ListFileWidget import ListFileWidget
from view.VideoPlayerWidget import VideoPlayerWidget
from engine.LoadConfig import LoadConfig
from engine.VideoTraitment import VideoTraitement
from view.LoadingWindow import EcranChargement
from view.LoadingWindow import ChargementThread
from view.LoadingWindow import ValidateThread
from view.FrameManagementWidget import FrameManagementWidget

class GUI(QMainWindow):

    video_traitement = None
    load_config      = None

    def __init__(self, parent=None) -> None:
        super(GUI, self).__init__(parent)
        self.setWindowTitle("Detected Changed Scene")
        self.load_config = LoadConfig()

        # TODO : ajouer un menu de réglage pour le volume, le dossier temp et le dossier file_out et le delta de détection.

        # Widget

        # - - HOME
        self.list_widget        = ListFileWidget()
        self.list_widget        .list_widget.clicked.connect(self.click_choose_path)
        self.label_video_choose = QLabel()
        self.label_video_choose .setText("Vidéo choisie")
        self.video_player       = VideoPlayerWidget()
        self.button_analyse     = QPushButton("Analyse")
        self.button_analyse     .clicked.connect(self.launch_analyse)
        self.button_analyse     .setVisible(False)
        # - - ANALYSE
        self.button_back        = QPushButton()
        self.button_back        .setIcon(QIcon("./asset/back.png"))
        self.button_back        .clicked.connect(self.back_file_list)
        self.button_back        .setIconSize(QSize(80, 80))
        self.button_back        .setFixedSize(100, 100)
        self.list_frame_widget  = FrameManagementWidget()
        self.button_valid       = QPushButton("V\nA\nL\nI\nD\nA\nT\nI\nO\nN")
        self.button_valid       .clicked.connect(self.validate)
        self.button_valid       .setFixedSize(30, 300)
        self.button_valid       .setStyleSheet("QPushButton {"
                                "     font-size: 24px;"
                                "}")

        # LAYOUT

        self.layout = QGridLayout()
        self.layout.addWidget(self.list_widget,        0, 0, 3, 1)
        self.layout.addWidget(self.label_video_choose, 0, 1, 1, 4, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.video_player,       1, 1, 2, 4, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.button_analyse,     3, 1, 1, 4, alignment=Qt.AlignHCenter)

        self.wid_selected_file  = QWidget(self)
        self.wid_selected_file  .setLayout(self.layout)

        self.layout_work_frame  = QGridLayout()
        self.layout_work_frame  .addWidget(self.button_back,       1, 0, 1, 1)
        self.layout_work_frame  .addWidget(self.list_frame_widget, 0, 1, 4, 9)
        self.layout_work_frame  .addWidget(self.button_valid,      1, 10, 1, 1)

        self.wid_manage_frame   = QWidget(self)
        self.wid_manage_frame   .setLayout(self.layout_work_frame)
        self.wid_manage_frame   .setVisible(False)
        
        self.stacked_widget     = QStackedWidget()
        self.stacked_widget     .addWidget(self.wid_selected_file)
        self.stacked_widget     .addWidget(self.wid_manage_frame)

        self.central_layout     = QVBoxLayout()
        self.central_layout     .addWidget(self.stacked_widget)

        self.central_widget     = QWidget()
        self.central_widget     .setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
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
        """
        current_index = self.stacked_widget.currentIndex()
        next_index    = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_index)

        self.video_player.stop()

        # Traitement de la vidéo

        self.video_traitement   = VideoTraitement(self.list_widget.get_file_path())
        self.ecran_chargement   = EcranChargement()
        self.ecran_chargement   .setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ecran_chargement   .show()
        self.thread_chargement  = ChargementThread(self.video_traitement)
        self.thread_chargement  .fin_chargement.connect(self.fin_chargement)
        self.thread_chargement  .start()
        self.button_back.setDisabled(True)
        self.button_valid.setDisabled(True)
    
# ====================================================================================
# --------------------------- ANALYSE PAGE -------------------------------------------
# ====================================================================================
    
    def fin_chargement(self):
        self.ecran_chargement.close()
        print(self.video_traitement.frame_change)
        self.list_frame_widget.addFrame(
            self.video_traitement.frame_change, 
            self.video_traitement.temp_path
        )
        self.button_back.setDisabled(False)
        self.button_valid.setDisabled(False)

    def back_file_list(self) -> None:
        """
        Retour à la page de sélection vidéo
        TODO : vide les fichiers temporaire et supprimer l'instance de travail.
        """
        back_validation = QMessageBox.question(None, 'Retour au choix de vidéo', 
                                 "Êtes-vous sûr de vouloir continuer ?\nCela effacera les images temporaires.", 
                                 QMessageBox.Yes | QMessageBox.No, 
                                 QMessageBox.No)
        if back_validation == QMessageBox.Yes :
            self.video_traitement.deleteTempFiles()
            current_index   = self.stacked_widget.currentIndex()
            next_index      = (current_index + 1) % self.stacked_widget.count()
            self.stacked_widget.setCurrentIndex(next_index)
    
    def validate(self) -> None:
        self.video_traitement.frame_change = self.list_frame_widget.list_frame
        self.ecran_chargement   = EcranChargement()
        self.ecran_chargement   .setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.ecran_chargement   .show()
        validate_thread = ValidateThread(self.video_traitement)
        validate_thread.end_work.connect(self.endWork)
        validate_thread.start()
    
    def endWork(self):
        self.ecran_chargement.close()
        msg_box = QMessageBox()
        msg_box.setText("Votre vidéo a été découpé avec succès.")
        msg_box.setWindowTitle("Validation")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

# ====================================================================================
# ________________________________________ A L L _____________________________________
# ====================================================================================

    def closeEvent(self, event) -> None:
        self.load_config.save()