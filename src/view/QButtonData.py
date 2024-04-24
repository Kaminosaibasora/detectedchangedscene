from PyQt5.QtWidgets import QPushButton

class QButtonData(QPushButton):
    data = None

    def __init__(self, text, data, parent=None):
        super().__init__(text, parent)
        self.data = data

    # def getData(self):
    #     print(self.data)
    
    # def delFrame(self, liste_frame):
    #     liste_frame.remove(self.data)
    #     print("DEL", self.data)