from picamzero import Camera
import os
import datetime

class CameraManager:
    def __init__(self, media_dir):
        self.camera = Camera()
        self.camera.greyscale = False
        self.media_dir = media_dir
        os.makedirs(self.media_dir, exist_ok=True)
        
    def capture_photo(self):
        datetime_object = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        picture_counter = len(os.listdir(self.media_dir)) + 1
        img_name = f"im_{picture_counter:04d}_{datetime_object}.jpg"
        img_path = os.path.join(self.media_dir, img_name)
        print(f"Capturing photo: {img_path}")
        try:
            self.camera.take_photo(img_path)
            return img_path
        except Exception as e:
            print(f"Error capturing image: {e}")
    
    def capture_video(self):
        datetime_object = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_counter = len(os.listdir(self.media_dir)) + 1
        vid_name = f"im_{video_counter:04d}_{datetime_object}.mp4"
        vid_path = os.path.join(self.media_dir, vid_name)
        print(f"Recording video to: {vid_path}")
        try:
            self.camera.record_video(vid_path, duration=10)
        except Exception as e:
            print(f"Error starting video recording: {e}")
        
    # def stop_video(self):
    #     print("Stopping video recording")
    #     try:
    #         self.camera.stop_recording()
    #     except Exception as e:
    #         print(f"Error stopping video recording: {e}")
    
    def start_preview(self):
        self.camera.start_preview()
    
    def stop_preview(self):
        self.camera.stop_preview()