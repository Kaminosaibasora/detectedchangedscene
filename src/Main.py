from engine.VideoTraitment import VideoTraitement

vt = VideoTraitement("./file_in/test_video.mp4")
# vt.decompose_img(100)
vt.detected_scene()

# TODO : interface graphique