import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from PyQt5.QtGui import QPixmap

class FrameManagementWidget(QWidget):

    list_frame = []

    def __init__(self) -> None:
        QWidget.__init__(self)

        self.scroll_area = QScrollArea()
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.widget_images = QWidget()


        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)

        self.layout_images = QVBoxLayout()
        self.widget_images.setLayout(self.layout_images)

        self.setLayout(layout)
    
    def addFrame(self, list_frame, path_temp):
        self.list_frame = list_frame
        list_img = os.listdir(path_temp)
        self.line_layout = QHBoxLayout()
        self.line_widget = QWidget()
        self.line_widget.setLayout(self.line_layout)
        self.line_widget.setStyleSheet("background-color: red;")
        self.line = 0
        for i in range(len(list_frame)):
            if list_frame[i] - 1 > 0 :
                image = QLabel()
                pixmap = QPixmap(path_temp+list_img[list_frame[i]-1])
                image.setPixmap(pixmap)
                self.line_layout.addWidget(image)
                self.new_line()

                button = QPushButton("❌") # TODO : faire un bouton personnalisé
                button.setStyleSheet("font-size: 10px; color: red;")
                button.clicked.connect(lambda: self.del_frame(list_frame[i]))
                self.line_layout.addWidget(button)
                self.new_line()
            
            image = QLabel()
            pixmap = QPixmap(path_temp+list_img[list_frame[i]])
            image.setPixmap(pixmap)
            self.line_layout.addWidget(image)
            self.new_line()

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget_images)
    
    def new_line(self):
        self.line += 1
        if (self.line >= 6):
                self.line = 0
                self.layout_images.addWidget(self.line_widget)
                self.line_layout = QHBoxLayout()
                self.line_widget = QWidget()
                self.line_widget.setStyleSheet("background-color: red;")
                self.line_widget.setLayout(self.line_layout)

    
    def del_frame(self, nb_frame):
        print("DEL FRAME : ", nb_frame)