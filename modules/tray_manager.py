import pystray
from PIL import Image, ImageDraw
import threading
import sys
import os

class TrayManager:
    def __init__(self, on_quit_callback, on_pause_callback, on_resume_callback):
        self.on_quit = on_quit_callback
        self.on_pause = on_pause_callback
        self.on_resume = on_resume_callback
        self.icon = None
        self.paused = False

    def _create_image(self):
        # Generate an icon image
        width = 64
        height = 64
        color1 = "blue"
        color2 = "white"

        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (width // 2, 0, width, height // 2),
            fill=color2)
        dc.rectangle(
            (0, height // 2, width // 2, height),
            fill=color2)

        return image

    def _on_clicked(self, icon, item):
        if str(item) == "Quit":
            self.on_quit()
            icon.stop()
        elif str(item) == "Pause Listening":
            self.paused = True
            self.on_pause()
            self._update_menu()
        elif str(item) == "Resume Listening":
            self.paused = False
            self.on_resume()
            self._update_menu()

    def _update_menu(self):
        if self.icon:
            self.icon.menu = pystray.Menu(
                pystray.MenuItem("Resume Listening" if self.paused else "Pause Listening", self._on_clicked),
                pystray.MenuItem("Quit", self._on_clicked)
            )

    def run(self):
        image = self._create_image()
        self.icon = pystray.Icon("MRD Assistant", image, "MRD Assistant", menu=pystray.Menu(
            pystray.MenuItem("Pause Listening", self._on_clicked),
            pystray.MenuItem("Quit", self._on_clicked)
        ))
        self.icon.run()

    def stop(self):
        if self.icon:
            self.icon.stop()
