import winreg
import sys
import os
import logging

def add_to_startup():
    """Adds the current script to Windows startup registry."""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        # Get path to python executable and main script
        python_exe = sys.executable
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))
        
        # Command to run: pythonw.exe (no console) main.py
        # Using pythonw.exe to avoid console window popping up
        pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
        
        command = f'"{pythonw_exe}" "{script_path}"'
        
        winreg.SetValueEx(key, "MRD_Assistant", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        logging.info("Successfully added to startup.")
        return True
    except Exception as e:
        logging.error(f"Failed to add to startup: {e}")
        return False

def remove_from_startup():
    """Removes the script from Windows startup registry."""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, "MRD_Assistant")
        winreg.CloseKey(key)
        logging.info("Successfully removed from startup.")
        return True
    except FileNotFoundError:
        logging.info("Startup key not found, nothing to remove.")
        return True
    except Exception as e:
        logging.error(f"Failed to remove from startup: {e}")
        return False

if __name__ == "__main__":
    # Simple CLI for testing
    if len(sys.argv) > 1:
        if sys.argv[1] == "add":
            add_to_startup()
        elif sys.argv[1] == "remove":
            remove_from_startup()
