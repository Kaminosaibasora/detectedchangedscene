from PyQt5.QtWidgets import QPushButton

class QButtonData(QPushButton):
    data = None

    def __init__(self, text, data, parent=None):
        super().__init__(text, parent)
        self.data = data