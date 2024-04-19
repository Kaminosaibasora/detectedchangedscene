import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QMessageBox, QAction, QFileDialog, QPushButton, QLabel, QLineEdit, QStackedWidget, QVBoxLayout
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtGui import QIcon
from view.ListFileWidget import ListFileWidget
from view.VideoPlayerWidget import VideoPlayerWidget

class GUI(QMainWindow):

    video_traitement = None

    def __init__(self, parent=None) -> None:
        super(GUI, self).__init__(parent)
        self.setWindowTitle("Detected Changed Scene")

        # Widget

        self.list_widget        = ListFileWidget()
        self.list_widget        .list_widget.clicked.connect(self.click_choose_path)
        self.label_video_choose = QLabel()
        self.label_video_choose .setText("Vidéo choisie")
        self.video_player       = VideoPlayerWidget()
        self.button_analyse     = QPushButton("Analyse")
        self.button_analyse.clicked.connect(self.launch_analyse)

        self.button_back = QPushButton("BACK")
        self.button_back.clicked.connect(self.back_file_list)
        self.list_frame = QLabel("list frame !!!!") # TODO
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
        self.layout_work_frame.addWidget(self.list_frame,    0, 1, 3, 4)
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

    def click_choose_path(self, line) -> None:
        """
        Sélectionne un fichier lors du clique dans la liste
        Args:
            line (_type_): information inclue dans l'item cliqué
        """
        self.list_widget.linecurrent = line
        self.label_video_choose      .setText(line.data())
        self.list_widget.file_choose = line.data()
        # Charger la vidéo dans le lecteur
        self.video_player.loadMedia(self.list_widget.get_file_path())
        self.video_player.play_pause()
    
    def launch_analyse(self) -> None:
        print("ANALYSE")
        # self.setCentralWidget(self.wid_manage_frame)
        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_index)
    
    def back_file_list(self) -> None:
        print("BACK")
        # self.setCentralWidget(self.wid_selected_file)
        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_index)