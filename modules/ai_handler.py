import requests
import logging
import json

class AIHandler:
    def __init__(self, config):
        self.config = config
        self.api_url = config['ai'].get('api_url', "http://localhost:11434/api/generate")
        self.model = config['ai'].get('model', "llama3")

    def get_response(self, user_input):
        """Generates a response from local Ollama instance."""
        try:
            system_prompt = (
                f"You are {self.config['assistant']['name']}, a helpful and intelligent desktop assistant. "
                "Keep your responses concise and suitable for text-to-speech. "
                "Do not include markdown formatting like asterisks or code blocks in your speech."
            )

            payload = {
                "model": self.model,
                "prompt": f"{system_prompt}\n\nUser: {user_input}\nAssistant:",
                "stream": False
            }

            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.ConnectionError:
            logging.error("Could not connect to Ollama. Is it running?")
            return "I cannot connect to my AI brain. Please make sure Ollama is running."
        except Exception as e:
            logging.error(f"AI Error: {e}")
            return "I encountered an error while processing your request."
