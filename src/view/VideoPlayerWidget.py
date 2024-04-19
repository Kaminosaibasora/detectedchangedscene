from PyQt5.QtCore import QDir, Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtWidgets import QWidget, QPushButton
import sys
import time

class VideoPlayerWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # lecteur vidéo
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setNotifyInterval(1)
        # widget video
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        # Bouton Play
        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play_pause)
        # LAYOUT
        layout = QGridLayout()
        layout.addWidget(self.videoWidget,      0, 0, 1, 9)
        layout.addWidget(self.playButton,       2, 4)

        self.setLayout(layout)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)

    def loadMedia(self, filepath):
        """Charge la vidéo dans le lecteur

        Args:
            filepath (String): chemin complet vers la vidéo.
        """
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
        # self.playButton.setEnabled(True)
    
    def play_pause(self):
        self.mediaPlayer.setPlaybackRate(1.0)
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.mediaPlayer.play()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))