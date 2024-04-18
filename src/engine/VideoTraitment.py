import cv2
import os
from PIL import Image
import numpy as np
from scipy import ndimage
from progress.bar import Bar
from engine.VideoEditor import VideoEditor

class VideoTraitement :
    video_path = ""
    temp_path = ""
    folder_out_path = ""
    delta = 500000
    frame_change = [] # TODO : retourner pour obtenir un traitement vidéo ?
    # TODO : ajouter une fonction de destruction qui vide le dossier temp
    # TODO : fonction de lecture vidéo d'une scene ?

    def __init__(self, video_path, temp_path = "./temp/", folder_out_path = "./file_out/") -> None:
        """_summary_
        Initialise les différents chemins.
        Args:
            video_path (_type_): chemin vers la vidéo
            temp_path (str, optional): chemin vers le dossier temporaire. Defaults to "./temp/".
            folder_out_path (str, optional): chemin vers le dossier de sortie. Defaults to "./file_out/".

        Raises:
            Exception: _description_
        """
        if not os.path.exists(video_path):
            print("Le fichier n'existe pas !")
            raise Exception("Le fichier vidéo n'existe pas !")
        self.video_path      = video_path
        self.temp_path       = temp_path
        self.folder_out_path = folder_out_path
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)
        if not os.path.exists(self.folder_out_path):
            os.mkdir(self.folder_out_path)

    def decompose_img(self, size):
        """_summary_
        Décompose la vidéo en images.
        Args:
            size (int): tailler des vignettes de comparaison
        """
        try :
            cap = cv2.VideoCapture(self.video_path)
            print("lecture de la vidéo : " + self.video_path)
            if not cap.isOpened():
                raise Exception("Erreur lors de l'ouverture de la vidéo.")
            frame_count = 0
            bar = Bar('Décomposition des frames', max=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                image_path = f"{self.temp_path}frame_"+self.rename_image(frame_count)+".jpg"
                new_frame = cv2.resize(frame, (size, size))
                cv2.imwrite(image_path, new_frame)
                frame_count += 1
                bar.next()
            bar.finish()
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print("ERROR" + str(e))

    def detected_scene(self):
        """_summary_
        Détecte les changement de scènes et met à jour la variable frame_change
        """
        list_img = os.listdir(self.temp_path)
        self.frame_change = [0]
        base = 0
        image_base = Image.open(self.temp_path + list_img[base])
        flou_base = ndimage.gaussian_filter(np.asarray(image_base), sigma=10)
        cran = 1
        bar = Bar('Détection des scènes', max=len(list_img))
        bar.next()
        while cran < len(list_img) :
            image_compare = Image.open(self.temp_path + list_img[cran])
            flou_compare = ndimage.gaussian_filter(np.asarray(image_compare), sigma=10)
            diff = self.compare_frame(flou_base, flou_compare, np.asarray(image_base).shape)
            if diff > self.delta :
                # print("point de dif entre ", list_img[base], "et", list_img[cran], ":", diff)
                self.frame_change += [cran]
            flou_base = flou_compare
            base = cran
            cran += 1
            bar.next()
        bar.finish()
        print(self.frame_change)
        return self.frame_change

    def compare_frame(self, image_base, image_compare, shape):
        """_summary_
        Compare 2 frames ensembles.
        Args:
            image_base (_type_): _description_
            image_compare (_type_): _description_
            shape (_type_): dimension de la matrice image

        Returns:
            int: valeur de différence
        """
        nb_lignes,nb_colonnes,nb_dim = shape
        dif = 0
        for line in range(nb_lignes):
                for col in range(nb_colonnes):
                    for dim in range(nb_dim):
                        if image_base[line][col][dim] > image_compare[line][col][dim] :
                            dif += image_base[line][col][dim] - image_compare[line][col][dim]
                        else : 
                            dif += image_compare[line][col][dim] - image_base[line][col][dim]
        return dif

    def rename_image(self, num):
        id = str(num)
        while(len(id) < 8):
            id = "0" + id
        return id

    def writer_video_scene(self):
        bar = Bar('Détection des scènes', max=len(self.frame_change)-1)
        for i in range(len(self.frame_change)-1):
            frame_debut = self.frame_change[i]
            frame_fin = self.frame_change[i+1]
            ve = VideoEditor(self.video_path, self.folder_out_path)
            ve.cut_video_scene(frame_debut, frame_fin, "video_test" + str(i))
            bar.next()
        bar.finish()
