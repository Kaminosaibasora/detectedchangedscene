from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import QRect

class ListLayout(QVBoxLayout):

    # TODO : réduire la valeur height

    items        = []
    item_width   = 0
    item_height  = 0
    marge_width  = 0
    marge_height = 0

    def __init__(self, item_w = 100, item_h = 50, parent=None):
        """
        Initialisation 
        Args:
            item_w (int, optional): largeur d'un item. Defaults to 100.
            item_h (int, optional): hauteur d'un item. Defaults to 50.
        """
        super().__init__(parent)
        self.item_width  = item_w
        self.item_height = item_h
    
    def addWidget(self, widget):
        """
        Ajoute un widget à la liste.
        Args:
            widget (QWidget): Widget à ajouter à la liste.
        """
        self.items.append(widget)
        return super().addWidget(widget)

    def setMarge(self, width, height):
        """
        Défini les marges entre les items.
        Args:
            width (int): marge horizontale entre deux items
            height (int): marge verticale entre deux items
        """
        self.marge_width  = width
        self.marge_height = height
    
    def removeBlockFrame(self, widget):
        """
        Retire une suite d'items parmi la liste et met à jour le layout.
        Args:
            widget (QWidget): Bouton correspondant à la frame à supprimer.
        """
        for i in range(len(self.items)) :
            if self.items[i] == widget :
                self.takeAt(i+1) # TODO : retirer ?
                self.takeAt(i)
                self.takeAt(i-1)
                del self.items[i-1:i+2]
                self.update()
                break

    def setGeometry(self, rect):
        """
        Fonction de calcul de placement des items.
        """
        super().setGeometry(rect)
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