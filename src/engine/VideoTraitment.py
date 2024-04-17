import cv2
import os
from PIL import Image
import numpy as np
from scipy import ndimage

class VideoTraitement :
    video_path = ""
    temp_path = ""
    folder_out_path = ""

    def __init__(self, video_path, temp_path = "./temp/", folder_out_path = "./file_out/") -> None:
        self.video_path      = video_path
        self.temp_path       = temp_path
        self.folder_out_path = folder_out_path
        # TODO vérifier l'existance des dossiers et les créer si nécessaire
        # TODO : vérifier l'existance de la vidéo
        if not os.path.exists(video_path):
            print("Le fichier n'existe pas !")

    def decompose_img(self, size):
        """_summary_
        décompose la vidéo en image
        Args:
            size (int): tailler des vignettes de comparaison
        """
        try :
            print("START")
            cap = cv2.VideoCapture(self.video_path)
            print("lecture de la vidéo : " + self.video_path)
            if not cap.isOpened():
                print("Erreur lors de l'ouverture de la vidéo.")
                exit()
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                image_path = f"{self.temp_path}frame_"+self.rename_image(frame_count)+".jpg"
                new_frame = cv2.resize(frame, (size, size))
                cv2.imwrite(image_path, new_frame)
                # print(f"Frame {frame_count} enregistrée")
                frame_count += 1
            cap.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print("ERROR" + str(e))

    def compare_frame(self):
        list_img = os.listdir(self.temp_path)
        frame_change = [0]
        # print(list_img)
        base = 0
        image_base = Image.open(self.temp_path + list_img[base])
        flou_base = ndimage.gaussian_filter(np.asarray(image_base), sigma=10)
        cran = 1
        while cran < len(list_img) :
            image_compare = Image.open(self.temp_path + list_img[cran])
            flou_compare = ndimage.gaussian_filter(np.asarray(image_compare), sigma=10)
            nb_lignes,nb_colonnes,nb_dim = np.asarray(image_base).shape
            diff = 0
            for line in range(nb_lignes):
                for col in range(nb_colonnes):
                    # print("compare :", flou_base[line][col], flou_compare[line][col])
                    for dim in range(nb_dim):
                        dif = 0
                        if flou_base[line][col][dim] > flou_compare[line][col][dim] :
                            dif = flou_base[line][col][dim] - flou_compare[line][col][dim]
                        else : 
                            dif = flou_compare[line][col][dim] - flou_base[line][col][dim]
                        # if dif != 0 :
                        #     print(dif, ":", dim, ":", flou_base[line][col], flou_compare[line][col])
                        diff += dif
            if diff > 500000 :
                print("point de dif entre ", list_img[base], "et", list_img[cran], ":", diff)
                print("NOUVELLE SCENE !")
                frame_change += [cran]
            flou_base = flou_compare
            base = cran
            cran += 1
        print(frame_change)

    def rename_image(self, num):
        id = str(num)
        while(len(id) < 8):
            id = "0" + id
        return id
