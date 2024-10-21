from gpiozero import Button
from camera_manager import CameraManager
from display_manager import DisplayManager

class MainController:
    def __init__(self):
        self.media_dir = "media"
        
        # Initialize managers
        self.camera_manager = CameraManager(self.media_dir)
        self.display_manager = DisplayManager(clk_pin=21, dio_pin=20)
        
        # Initialize buttons
        self.video_button = Button(5)
        self.capture_button = Button(6, hold_time=1, bounce_time=0.1)

        # Set button actions
        self.video_button.when_pressed = self.start_recording
        self.capture_button.when_pressed = self.capture_photo

        # Update picture count on startup
        self.display_manager.update_picture_count()

    def capture_photo(self):
        self.camera_manager.capture_photo()
        self.display_manager.update_picture_count()

    def start_recording(self):
        video_path = f"{self.media_dir}/temp/temp.h264"
        self.camera_manager.record_video(video_path)
        self.display_manager.update_picture_count()