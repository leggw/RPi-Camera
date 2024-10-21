from tm1637 import TM1637
import shutil

class DisplayManager:
    def __init__(self, clk_pin, dio_pin):
        self.display = TM1637(clk=clk_pin, dio=dio_pin)
        self.display.brightness(1)
    
    def update_picture_count(self):
        total, used, free = shutil.disk_usage("/")
        remaining_pictures = int(free / (1.3 * 1024 * 1024))  # Assuming 1.3 MB per picture
        self.display_number(remaining_pictures)
    
    def display_number(self, number):
        digits = [int(d) for d in str(number).zfill(4)]
        self.display.show(digits[:4])