import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QPixmap
from view.QButtonData import QButtonData
from view.ListLayout import ListLayout

class FrameManagementWidget(QWidget):

    list_frame = []

    def __init__(self) -> None:
        QWidget.__init__(self)

        self.scroll_area = QScrollArea()
        self.widget_images = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)

        self.layout_images = ListLayout(100, 100)
        self.layout_images.setMarge(10, 10)
        self.widget_images.setLayout(self.layout_images)

        self.setLayout(layout)
    
    def addFrame(self, list_frame, path_temp):
        self.list_frame = list_frame
        list_img = os.listdir(path_temp)
        for i in range(len(list_frame)):
            try : 
                if list_frame[i] - 1 > 0 :
                    image = QLabel()
                    pixmap = QPixmap(path_temp+list_img[list_frame[i]-1])
                    image.setPixmap(pixmap)
                    self.layout_images.addWidget(image)

                    button = QButtonData("❌", list_frame[i])
                    button.setStyleSheet("font-size: 20px; color: red;")
                    button.clicked.connect(lambda: self.del_frame(button.data))
                    self.layout_images.addWidget(button)
                
                image = QLabel()
                pixmap = QPixmap(path_temp+list_img[list_frame[i]])
                image.setPixmap(pixmap)
                self.layout_images.addWidget(image)
            except Exception as e :
                print("ERROR", e)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget_images)
    
    def del_frame(self, nb_frame):
        print("DEL FRAME : ", nb_frame)