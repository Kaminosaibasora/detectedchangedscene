import os
import json

class LoadConfig :

    path_folder_in = ""
    path_folder_out = ""
    path_folder_temp = ""
    __default_path = "./curentconfig.json"

    def __init__(self) -> None:
        if(os.path.exists(self.__default_path)):
            self.load(self.__default_path)
        else :
            self.saveConfig(self.__default_path)
    
    def load(self, path) -> None:
        """
        Chargement des données du fichier de configuration json
        Args:
            path (str): chemin vers le fichier de configuration
        """
        try :
            with open(path, "r") as file :
                data = json.load(file)
                self.path_folder_in     = data["path_folder_in"]
                self.path_folder_out    = data["path_folder_out"]
                self.path_folder_temp   = data["path_folder_temp"]
        except Exception as e :
            print("ERROR", e)

    def saveConfig(self, path, path_in = "", path_out = "", path_temp = "") -> None:
        """
        Sauvegarde la configuration dans un fichier json.
        Args:
            path (_type_): _description_
            path_in (str, optional): _description_. Defaults to "".
            path_out (str, optional): _description_. Defaults to "".
            path_temp (str, optional): _description_. Defaults to "".
        """
        data = {
            "path_folder_in" : path_in,
            "path_folder_out" : path_out,
            "path_folder_temp" : path_temp,
        }
        try : 
            with open(path, "w") as file :
                json.dump(data, file, indent=4)
        except Exception as e :
            print("ERROR", e)
    
    def save(self):
        self.saveConfig(
            self.__default_path, 
            self.path_folder_in, 
            self.path_folder_out, 
            self.path_folder_temp
        )
    
    def set_path_config_file(self, path):
        self.__default_path = path
        try :
            self.load(self.__default_path)
        except Exception as e :
            print("ERROR", e)
            self.saveConfig(self.__default_path, self.path_folder_in, self.path_folder_out, self.path_folder_temp)
    
    def __str__(self) -> str:
        return f"folder in : {self.path_folder_in}\nfolder out : {self.path_folder_out}\nfolder temp : {self.path_folder_temp}"
