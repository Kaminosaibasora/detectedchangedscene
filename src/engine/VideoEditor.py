from moviepy.editor import VideoFileClip

class VideoEditor :
    video_path = ""
    folder_out_path = ""
    clip = None

    def __init__(self, video_path, folder_out_path) -> None:
        self.video_path = video_path
        self.folder_out_path = folder_out_path
        self.clip = VideoFileClip(self.video_path)
    
    def cut_video_scene(self, frame_in, frame_out, video_out_name):
        try :
            clip_coupe = self.clip.subclip(frame_in / self.clip.fps, frame_out / self.clip.fps)
            clip_coupe.write_videofile(self.folder_out_path+video_out_name+".mp4", codec="libx264", audio_codec="aac")
            print("video éditée")
        except Exception as e :
            print("ERROR :", e)