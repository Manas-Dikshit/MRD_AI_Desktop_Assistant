import json
import time
import keyboard
import logging
import os
import threading
import sys
from modules.voice import VoiceHandler
from modules.ai_handler import AIHandler
from modules.command_executor import CommandExecutor
from modules.tray_manager import TrayManager
from setup.startup import add_to_startup
from rich.console import Console
from rich.logging import RichHandler

# Setup Logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RichHandler(rich_tracebacks=True),
        logging.FileHandler(os.path.join(log_dir, "mrd_assistant.log"))
    ]
)

console = Console()

class AssistantApp:
    def __init__(self):
        self.running = True
        self.paused = False
        self.config = self.load_config()
        
        if not self.config:
            logging.error("Failed to load config. Exiting.")
            sys.exit(1)

        self.voice = VoiceHandler(self.config)
        self.ai = AIHandler(self.config)
        self.executor = CommandExecutor(self.config)
        self.tray = TrayManager(self.quit_app, self.pause_listening, self.resume_listening)
        
        # Auto-start check
        add_to_startup()

    def load_config(self):
        try:
            config_path = os.path.join("config", "config.json")
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error("config/config.json not found.")
            return {}
        except json.JSONDecodeError:
            logging.error("Error decoding config.json.")
            return {}

    def on_activate(self):
        if self.paused:
            return

        logging.info("Hotkey activated!")
        
        # Play a sound or speak to indicate listening
        wake_response = self.config['assistant'].get('wake_response', "Yes?")
        self.voice.speak(wake_response)
        
        # Listen for command
        user_input = self.voice.listen()
        
        if user_input:
            # Try to execute local command first
            executed, response = self.executor.parse_and_execute(user_input)
            
            if executed:
                self.voice.speak(response)
            else:
                # Fallback to AI
                ai_response = self.ai.get_response(user_input)
                self.voice.speak(ai_response)
        else:
            fallback = self.config['assistant'].get('fallback_response', "I didn't catch that.")
            self.voice.speak(fallback)

    def start_listener(self):
        hotkey = self.config.get("hotkey", "ctrl+shift+m")
        logging.info(f"Registering hotkey: {hotkey}")
        keyboard.add_hotkey(hotkey, self.on_activate)
        
        # Optional: Wake word loop could go here in a separate thread if implemented
        # For now, we rely on hotkey to keep it simple and efficient
        
        while self.running:
            time.sleep(1)

    def pause_listening(self):
        self.paused = True
        logging.info("Assistant paused.")

    def resume_listening(self):
        self.paused = False
        logging.info("Assistant resumed.")

    def quit_app(self):
        self.running = False
        logging.info("Stopping assistant...")
        # Force exit since keyboard listener might be blocking
        os._exit(0)

    def run(self):
        # Start listener in a separate thread
        listener_thread = threading.Thread(target=self.start_listener)
        listener_thread.daemon = True
        listener_thread.start()

        logging.info("MRD Assistant started. Check system tray.")
        
        # Run tray icon in main thread (GUI usually requires main thread)
        self.tray.run()

if __name__ == "__main__":
    app = AssistantApp()
    app.run()
