import os
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QFileDialog, QLabel, QVBoxLayout, QWidget, QListWidget, QListWidgetItem

class ListFileWidget(QWidget):

    list_path   = []
    file_choose = ""
    folder_path = ""
    line_curent = None

    def __init__(self) -> None:
        QWidget.__init__(self)
        
        # Widget

        self.label_folder   = QLabel()
        self.button_choose  = QPushButton("Choose")
        self.button_choose  .clicked.connect(self.choose_folder)
        self.list_widget    = QListWidget(self)

        # Layout

        layout  = QVBoxLayout()
        layout  .addWidget(self.label_folder)
        layout  .addWidget(self.button_choose)
        layout  .addWidget(self.list_widget)

        self.setLayout(layout)
        self.setFixedWidth(200)

    def choose_folder(self):
        """
        Ouvre une fenêtre de sélection vers un dossier.
        """
        try :
            valid = False
            self.folder_path = ""
            while not valid :
                try :
                    self.folder_path = QFileDialog.getExistingDirectory(self, "Choose Folder")
                    valid = True
                except Exception as e :
                    print(e)
            self.maj_folder()
        except Exception as e :
            print(e)
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Error :"+e)
            error.setWindowTitle("Erreur de validation")
    
    def maj_folder(self):
        self.list_video_folder(self.folder_path)
        self.maj_list_files()
    
    def list_video_folder(self, path):
        """
        Met à jour le path du folderin de l'objet cut_video et récupère la liste des fichiers.
        """
        self.listpath = self.list_video(path, ["mp4"])
    
    def list_video(self, path = "./../file_in", types_accepted = ["mp4", "mov", "avi"]) -> list:
        """_summary_

        Args:
            path (str, optional): _description_. Defaults to "./../file_in".
            types_accepted (list, optional): _description_. Defaults to ["mp4", "mov", "avi"].

        Returns:
            list: _description_
        """
        if path[-1] == "/" :
            path = path[:-1]
        files = os.listdir(path)
        liste_v = []
        for f in files :
            # TODO : bricoler les types
            if f[-3:] in types_accepted and not os.path.isdir(path+'/'+f):
                liste_v += [f]
        return liste_v
    
    def maj_list_files(self):
        """
        Met à jour les widget de la liste de lien.
        """
        self.list_widget.clear()
        for f in self.listpath :
            self.list_widget.addItem(
                QListWidgetItem(f)
            )

    def clicklist(self, test):
        self.filechoose = test.data()
    
    def updateList(self):
        self.list_widget.removeItemWidget(
            self.list_widget.takeItem(self.list_widget.currentRow())
        )
        self.list_widget.repaint()
        self.linecurrent = None
    
    def get_file_path(self) -> str:
        return self.folder_path + "/" + self.file_choose