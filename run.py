from main_controller import MainController
from signal import pause
import sys

if __name__ == "__main__":
    try:
        controller = MainController()

        controller.display_manager.display.clear()  # Clear any existing content
        controller.display_manager.display.write_string("Now running")

        print("Program running, press Ctrl+C to End")
        pause() # program runs indefinitely
    except KeyboardInterrupt:
        controller.display_manager.display.clear()
        controller.display_manager.display.write_string("Program is stopping")

        print("shutting down")
        sys.exit(0)