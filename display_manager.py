from RPLCD.i2c import CharLCD
import shutil

class DisplayManager:
    def __init__(self, clk_pin, dio_pin):
        self.display = CharLCD(i2c_expander='PCF8574', address=0x27)
    
    def update_picture_count(self):
        total, used, free = shutil.disk_usage("/")
        remaining_pictures = int(free / (1.7 * 1024 * 1024))  # Assuming 1.3 MB per picture
        self.display_number(remaining_pictures)
    
    def display_number(self, number):
        self.display.clear()
        digits = str(number)
        self.display.write_string(f"Pics Left: {digits}")