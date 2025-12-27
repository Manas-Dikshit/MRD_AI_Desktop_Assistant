import speech_recognition as sr
import pyttsx3
import logging
import os
import json
import time
from vosk import Model, KaldiRecognizer
import pyaudio

class VoiceHandler:
    def __init__(self, config):
        self.config = config
        self.engine = pyttsx3.init()
        self._setup_voice()
        self.vosk_model = None
        self._setup_vosk()

    def _setup_voice(self):
        """Configures the TTS engine based on config."""
        try:
            voices = self.engine.getProperty('voices')
            
            # Log available voices for the user
            logging.info("Available TTS Voices:")
            for idx, voice in enumerate(voices):
                logging.info(f"ID: {idx} - Name: {voice.name}")

            voice_id = self.config['assistant'].get('voice_id', 0)
            if 0 <= voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)
            
            rate = self.config['assistant'].get('speech_rate', 150)
            self.engine.setProperty('rate', rate)
        except Exception as e:
            logging.error(f"Error setting up voice: {e}")

    def _setup_vosk(self):
        """Initializes Vosk model for offline recognition."""
        model_path = self.config.get('voice', {}).get('model_path', 'model')
        if not os.path.exists(model_path):
            logging.warning(f"Vosk model not found at {model_path}. Offline recognition will fail.")
            return
        
        try:
            self.vosk_model = Model(model_path)
            logging.info("Vosk model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load Vosk model: {e}")

    def speak(self, text):
        """Converts text to speech."""
        try:
            logging.info(f"Assistant: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"TTS Error: {e}")

    def listen(self):
        """Listens to the microphone and returns recognized text using Vosk."""
        if not self.vosk_model:
            logging.error("Vosk model not loaded.")
            return None

        rec = KaldiRecognizer(self.vosk_model, 16000)
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
            stream.start_stream()
            
            logging.info("Listening...")
            
            # Listen for up to 5 seconds of silence or until result
            # This is a simplified loop. For production, you'd want better silence detection.
            # Here we just read chunks until we get a final result or timeout logic (omitted for brevity)
            
            start_time = time.time()
            while True:
                # Timeout after 10 seconds if no speech
                if time.time() - start_time > 10:
                    logging.info("Listening timed out.")
                    return None

                data = stream.read(4000, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get('text', '')
                    if text:
                        logging.info(f"User said: {text}")
                        return text
                    # If result is empty, it might be silence, keep listening or break?
                    # For this simple implementation, we return the first result.
                    # return None
        except Exception as e:
            logging.error(f"Listening Error: {e}")
            return None
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            p.terminate()
