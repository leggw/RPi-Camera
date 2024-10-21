class HDMIManager:
    def __init__(self, camera_manager):
        self.is_active_hdmi = False
        self.camera_manager = camera_manager

    def toggle_hdmi(self):
        if not self.is_active_hdmi:
            print("Starting HDMI preview")
            self.camera_manager.start_preview()
            self.is_active_hdmi = True
        else:
            print("Stopping HDMI preview")
            self.camera_manager.stop_preview()
            self.is_active_hdmi = False