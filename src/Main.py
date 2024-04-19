from engine.VideoTraitment import VideoTraitement
from view.GUI import GUI
from PyQt5.QtWidgets import QApplication
import sys

# vt = VideoTraitement("./file_in/test_video.mp4")
# vt.decompose_img(100)
# vt.detected_scene()
# vt.writer_video_scene()

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)

fen = GUI()
fen.show()

app.exec_()