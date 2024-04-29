import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QWidget, QScrollArea, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap
from view.QButtonData import QButtonData
from view.ListLayout import ListLayout

class FrameManagementWidget(QWidget):

    list_frame = []

    def __init__(self) -> None:
        QWidget.__init__(self)

        self.scroll_area    = QScrollArea()
        self.widget_images  = QWidget()

        layout  = QVBoxLayout()
        layout  .addWidget(self.scroll_area)

        self.layout_images  = ListLayout(100, 100)
        self.layout_images  .setMarge(10, 10)
        self.widget_images  .setLayout(self.layout_images)

        self.setLayout(layout)
    
    def addFrame(self, list_frame, path_temp):
        """
        Ajoute les différentes frames de description des scènes au layout.
        Args:
            list_frame (list<int>): Liste des différentes frames
            path_temp (str): chemin vers le dossier temporaire contenant les images
        """
        self.list_frame = list_frame
        list_img        = os.listdir(path_temp)
        for i in range(len(list_frame)):
            try : 
                if list_frame[i] - 1 > 0 :
                    image   = QLabel()
                    pixmap  = QPixmap(path_temp+list_img[list_frame[i]-1])
                    image   .setPixmap(pixmap)
                    self.layout_images.addWidget(image)

                    button  = QButtonData("❌", list_frame[i])
                    button  .setStyleSheet("font-size: 20px; color: red;")
                    button  .clicked.connect(self.delFrame)
                    self.layout_images.addWidget(button)
                
                image   = QLabel()
                pixmap  = QPixmap(path_temp+list_img[list_frame[i]])
                image   .setPixmap(pixmap)
                self.layout_images.addWidget(image)
            except Exception as e :
                print("ERROR", e)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget_images)
    
    def delFrame(self, event):
        """
        Supprime une frame qui ne doit pas être découpé et met à jour le layout.
        """
        id_frame = self.sender().data
        self.list_frame.remove(id_frame)
        self.layout_images.removeBlockFrame(self.sender())
        # print(self.list_frame)
    
    def clearFrames(self):
        """
        Retire toutes les frames du composant.
        """
        self.list_frame = []
        self.layout_images.clearFrames()