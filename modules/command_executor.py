import os
import subprocess
import webbrowser
import datetime
import logging
import re

class CommandExecutor:
    def __init__(self, config):
        self.config = config
        self.paths = config.get("paths", {})

    def parse_and_execute(self, text):
        """
        Parses the text for commands and executes them.
        Returns a tuple (executed, response_message).
        If executed is True, the action was handled locally.
        If False, it should be passed to the AI.
        """
        text = text.lower()

        # 1. Open Applications
        if "open" in text or "launch" in text:
            for app_name, app_path in self.paths.items():
                if app_name in text:
                    return self._open_application(app_name, app_path)
            
            # Generic website opening
            if "youtube" in text:
                return self._open_url("https://www.youtube.com", "YouTube")
            if "google" in text:
                return self._open_url("https://www.google.com", "Google")
            if "gmail" in text:
                return self._open_url("https://mail.google.com", "Gmail")
            if "chatgpt" in text:
                return self._open_url("https://chat.openai.com", "ChatGPT")

        # 2. Time and Date
        if "time" in text:
            now = datetime.datetime.now().strftime("%I:%M %p")
            return True, f"The current time is {now}."
        
        if "date" in text:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return True, f"Today is {today}."

        return False, None

    def _open_application(self, name, path):
        try:
            if os.path.exists(path):
                subprocess.Popen(path)
                return True, f"Opening {name}."
            else:
                logging.error(f"Path not found for {name}: {path}")
                return True, f"I couldn't find the executable for {name}. Please check the configuration."
        except Exception as e:
            logging.error(f"Error opening {name}: {e}")
            return True, f"I encountered an error trying to open {name}."

    def _open_url(self, url, name):
        try:
            webbrowser.open(url)
            return True, f"Opening {name}."
        except Exception as e:
            logging.error(f"Error opening URL {url}: {e}")
            return True, f"I couldn't open {name}."
