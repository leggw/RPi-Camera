# Raspberry Pi Camera Controller

This project is a Python-based application that allows you to control a Raspberry Pi camera using physical buttons connected to the GPIO pins with LEDs for feedback. The application uses the `picamzero` library to capture images and videos, and the `gpiozero` library to handle button and LED control. You can toggle between different modes (image capture and video recording) and control basic camera functionality with HDMI output to preview images.

## Features
- **Capture Images**: Press a button to capture images, which are saved in the `media/` directory.
- **Record Videos**: Press and hold the button to start video recording, and release it to stop the recording. Videos are also saved in the `media/` directory.
- **LED Indicators**: LED indicators show the camera's current state (recording, idle, etc.).
- **Dynamic File Management**: The program saves files with dynamically generated names, ensuring no file overwrites occur.
- **Thumbnail Generation**: Automatically generates thumbnails for captured images and videos.

## Prerequisites

Before running this project, ensure that you have the following installed:

### Hardware
- Raspberry Pi (with Raspberry Pi OS)
- Raspberry Pi Camera Module
- Buttons connected to GPIO pins for controlling the camera
- LEDs connected to GPIO pins for visual feedback

### Software
- Python 3.x
- `picamzero` (Camera control)
- `gpiozero` (GPIO pins control)
- `Pillow` (Image processing for thumbnail generation)
- `ffmpeg` (for video processing)
- `MP4Box` (for video format conversion)

You can install the required Python packages using `pip`:

```bash
pip install gpiozero picamzero Pillow
```
You will also need to install ffmpeg and MP4Box for video processing:

```bash
sudo apt install ffmpeg gpac
```

## Wiring
- GPIO Pin 5: Connected to a button that toggles HDMI preview (simulated in this project).
- GPIO Pin 6: Connected to a button that captures images or starts/stops video recording.
- GPIO Pin 13: Green LED indicating the system is ready.
- GPIO Pin 19: Blue LED indicating HDMI preview is on.
- GPIO Pin 26: Red LED indicating image capture or video recording.
