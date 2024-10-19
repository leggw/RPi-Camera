from gpiozero import Button, LED
from signal import pause
from PIL import Image
import subprocess
import datetime
import glob
import os
import pwd
import grp
from picamzero import Camera


class PiCameraController:
    def __init__(self):
        # Initialize LEDs
        self.green = LED(13)  # Green Led - Pin Number: GPIO 13
        self.blue = LED(19)   # Blue Led - Pin Number: GPIO 19
        self.red = LED(26)    # Red Led - Pin Number: GPIO 26

        # Initialize buttons
        self.btn = Button(5, hold_time=1, bounce_time=0.1)  # HDMI Button - GPIO 5
        self.cptr = Button(6, hold_time=1, bounce_time=0.1)  # Picture/Video Button - GPIO 6

        # Initialize camera and states
        self.camera = Camera()
        self.camera.greyscale = True
        self.is_active_hdmi = False
        self.is_recording = False
        self.was_held = False

        # Set button actions
        self.btn.when_pressed = self.hdmi
        self.cptr.when_held = self.video
        self.cptr.when_released = self.capture

        # Dynamically determine the working directory
        self.media_dir = os.path.join(os.getcwd(), 'media')
        os.makedirs(self.media_dir, exist_ok=True)  # Ensure the media directory exists

        print(f"Ready-to-use. Media will be saved in: {self.media_dir}")
        self.green.on()
        self.blue.off()
        self.red.off()

    def change_file_permissions(self):
        try:
            uid = pwd.getpwnam("www-data").pw_uid
            gid = grp.getgrnam("www-data").gr_gid
            for file in os.listdir(self.media_dir):
                file_path = os.path.join(self.media_dir, file)
                os.chown(file_path, uid, gid)
        except Exception as e:
            print(f"Error changing file permissions: {e}")

    def hdmi(self):
        if not self.is_active_hdmi:
            self.is_active_hdmi = True
            self.blue.on()
            self.green.off()
            print("Started HDMI")
            self.camera = Camera()
            self.camera.start_preview()
        else:
            print("Stopped HDMI")
            self.green.on()
            self.blue.off()
            if self.camera:
                self.camera.stop_preview()
                self.camera = None
            self.is_active_hdmi = False

    def capture(self):
        if not self.was_held:
            if not self.is_recording:
                self.red.on()
                self.green.off()
                datetime_object = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                print("Captured")
                picture_counter = (self.counter(1) + 1)
                img_name = f"im_{picture_counter:04d}_{datetime_object}.jpg"
                img_name_thumb = f"im_{picture_counter:04d}_{datetime_object}.th.jpg"
                img_path = os.path.join(self.media_dir, img_name)
                thumb_path = os.path.join(self.media_dir, img_name_thumb)
                try:
                    self.camera.take_photo(img_path)
                    self.thumbnail_picture(img_path, thumb_path)
                except Exception as e:
                    print(f"Error capturing image: {e}")
                self.red.off()
                self.was_held = False
            else:
                self.video()

    def video(self):
        self.was_held = True
        if not self.is_recording:
            print("Started recording")
            self.is_recording = True
            self.red.blink()
            video_counter = self.counter(2) + 1
            video_path = os.path.join(self.media_dir, 'temp', 'temp.h264')
            os.makedirs(os.path.dirname(video_path), exist_ok=True)  # Ensure the temp directory exists
            try:
                self.camera.start_recording(video_path)
            except Exception as e:
                print(f"Error starting video recording: {e}")
            return video_counter
        else:
            print("Stopped recording")
            try:
                self.camera.stop_recording()
            except Exception as e:
                print(f"Error stopping video recording: {e}")
            self.red.off()
            self.green.on()
            self.blue.on()
            self.is_recording = False
            self.convert()

    def counter(self, what_is_needed):  # Counts amount of video/picture in the media folder.
        mp4_counter = len(glob.glob1(self.media_dir, "*.mp4"))
        jpg_counter = len(glob.glob1(self.media_dir, "*.jpg"))

        if what_is_needed == 1:
            return jpg_counter
        if what_is_needed == 2:
            return mp4_counter
        return 0

    def thumbnail_picture(self, img_path, thumb_path):  # Creates thumbnail for the taken picture.
        try:
            image = Image.open(img_path)
            MAX_SIZE = (100, 100)
            image.thumbnail(MAX_SIZE)
            image.save(thumb_path)
            self.change_file_permissions()
        except Exception as e:
            print(f"Error creating thumbnail: {e}")

    def thumbnail_video(self, video_name, datetime_object, video_counter):  # Creates thumbnail for the recorded video.
        video_input_path = os.path.join(self.media_dir, video_name)
        img_output_path = os.path.join(self.media_dir, f'vi_{video_counter:04d}_{datetime_object}.mp4.v{video_counter:04d}.th.jpg')
        try:
            subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:00.000', '-vframes', '1', img_output_path])
            self.change_file_permissions()
        except Exception as e:
            print(f"Error generating video thumbnail: {e}")

    def convert(self):  # Converts .h264 video format to .mp4.
        datetime_object = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        video_counter = self.counter(2) + 1
        video_name = f"vi_{video_counter:04d}_{datetime_object}.mp4"
        video_path = os.path.join(self.media_dir, video_name)
        command = f"MP4Box -add {os.path.join(self.media_dir, 'temp', 'temp.h264')} {video_path}"
        try:
            subprocess.call([command], shell=True)
            print("Video Converted")
            self.thumbnail_video(video_name, datetime_object, video_counter)
        except Exception as e:
            print(f"Error converting video: {e}")


if __name__ == "__main__":
    camera_controller = PiCameraController()
    pause()