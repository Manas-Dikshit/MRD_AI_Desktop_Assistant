import os
import requests
import zipfile
import shutil
import logging
from rich.console import Console

console = Console()
logging.basicConfig(level=logging.INFO)

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR = "model"
ZIP_FILE = "model.zip"

def download_model():
    if os.path.exists(MODEL_DIR):
        console.print(f"[bold green]Model directory '{MODEL_DIR}' already exists. Please delete it first if you want to upgrade.[/bold green]")
        return

    console.print(f"[bold yellow]Downloading Vosk model from {MODEL_URL}...[/bold yellow]")
    try:
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()
        
        with open(ZIP_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        console.print("[bold green]Download complete. Extracting...[/bold green]")
        
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(".")
            
        # The zip usually contains a folder named 'vosk-model-small-en-us-0.15'
        extracted_folder = "vosk-model-small-en-us-0.15"
        if os.path.exists(extracted_folder):
            os.rename(extracted_folder, MODEL_DIR)
            console.print(f"[bold green]Model extracted and renamed to '{MODEL_DIR}'.[/bold green]")
        else:
            console.print(f"[bold red]Could not find expected folder '{extracted_folder}'. Please check the extracted files.[/bold red]")

        # Cleanup
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
            
    except Exception as e:
        console.print(f"[bold red]Failed to download or extract model: {e}[/bold red]")

if __name__ == "__main__":
    download_model()
