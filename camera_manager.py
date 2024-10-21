from picamzero import Camera
import os
import datetime

class CameraManager:
    def __init__(self, media_dir):
        self.camera = Camera()
        self.camera.greyscale = True
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
    
    def record_video(self, video_path):
        print(f"Recording video to: {video_path}")
        try:
            self.camera.start_recording(video_path)
        except Exception as e:
            print(f"Error starting video recording: {e}")
        
    def stop_video(self):
        print("Stopping video recording")
        try:
            self.camera.stop_recording()
        except Exception as e:
            print(f"Error stopping video recording: {e}")
    
    def start_preview(self):
        self.camera.start_preview()
    
    def stop_preview(self):
        self.camera.stop_preview()