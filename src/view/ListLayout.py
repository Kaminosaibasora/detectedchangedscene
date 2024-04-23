import sys
from PyQt5.QtWidgets import QLayout, QLayoutItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QRect, QSize, Qt

class ListLayout(QVBoxLayout):

    # TODO : réduire la valeur height

    items = []
    item_width = 0
    item_height = 0
    marge_width = 0
    marge_height = 0

    def __init__(self, item_w = 100, item_h = 50, parent=None):
        super().__init__(parent)
        self.item_width = item_w
        self.item_height = item_h
    
    def addWidget(self, widget) -> None:
        self.items.append(widget)
        return super().addWidget(widget)

    def setMarge(self, width, height):
        self.marge_width = width
        self.marge_height = height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        # print("OK")
        if not self.items:
            return
        actual_width = 0
        actual_height = 0
        for i, item in enumerate(self.items):
            # print(item, actual_width, actual_height)
            item.setGeometry(QRect(actual_width, actual_height, self.item_width, self.item_height))
            actual_width += self.item_width
            actual_width += self.marge_width
            if (actual_width + self.item_width) >= rect.width():
                actual_height += self.item_height
                actual_height += self.marge_height
                actual_width = 0