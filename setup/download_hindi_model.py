import os
import requests
import zipfile
import shutil
import logging
from rich.console import Console

console = Console()
logging.basicConfig(level=logging.INFO)

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip"
MODEL_DIR = "model_hi"
ZIP_FILE = "model_hi.zip"

def download_hindi_model():
    if os.path.exists(MODEL_DIR):
        console.print(f"[bold green]Hindi Model directory '{MODEL_DIR}' already exists.[/bold green]")
        return

    console.print(f"[bold yellow]Downloading Hindi Vosk model from {MODEL_URL}...[/bold yellow]")
    try:
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()
        
        with open(ZIP_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        console.print("[bold green]Download complete. Extracting...[/bold green]")
        
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(".")
            
        extracted_folder = "vosk-model-small-hi-0.22"
        if os.path.exists(extracted_folder):
            os.rename(extracted_folder, MODEL_DIR)
            console.print(f"[bold green]Hindi Model extracted and renamed to '{MODEL_DIR}'.[/bold green]")
        else:
            console.print(f"[bold red]Could not find expected folder '{extracted_folder}'.[/bold red]")

        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
            
    except Exception as e:
        console.print(f"[bold red]Failed to download or extract model: {e}[/bold red]")

if __name__ == "__main__":
    download_hindi_model()
