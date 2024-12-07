from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def set_volume(target_volume_percent):
    # Get the default audio device
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    # Set the volume level (target_volume_percent should be between 0 and 100)
    current_range = volume.GetVolumeRange()  # Get min, max, and increment levels
    min_volume, max_volume, _ = current_range

    # Map the percentage (e.g., 150%) to the volume range
    target_volume = min_volume + (target_volume_percent / 100.0) * (max_volume - min_volume)

    # Ensure the target volume is within valid bounds
    target_volume = max(min(target_volume, max_volume), min_volume)
    volume.SetMasterVolumeLevel(target_volume, None)

# Example: Set volume to 150%
set_volume(95)