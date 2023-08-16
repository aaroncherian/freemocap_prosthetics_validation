import deeplabcut
from pathlib import Path
import os

config_path = r"C:\Users\aaron\Desktop\JH_DLC_model-Aaron-2023-07-03\config.yaml"

def process_recording_folder(path_to_recording_folder):
    path_to_recording_folder = Path(path_to_recording_folder)

    path_to_video_folder = str(path_to_recording_folder/'synchronized_videos')
    dest_folder = str(path_to_recording_folder/'dlc_data')

    deeplabcut.analyze_videos(config=config_path, gputouse=0, videos=path_to_video_folder, save_as_csv=True, destfolder=dest_folder)

    video_list = sorted(list(Path(path_to_video_folder).glob('*.mp4')))

    for video in video_list:
        deeplabcut.filterpredictions(config=config_path, video=str(video), destfolder=dest_folder, save_as_csv=True)

    deeplabcut.create_labeled_video(config=config_path, videos=path_to_video_folder, destfolder=dest_folder)

def process_session_folder(session_folder):
    # Convert the session folder path to a pathlib Path object
    session_folder_path = Path(session_folder)

    # Loop through all subdirectories (recording folders) in the session folder
    for recording_folder in session_folder_path.iterdir():
        if recording_folder.is_dir():
            # Check if the 'dlc_data' folder exists in the recording folder
            if not (recording_folder / 'dlc_data').exists():
                process_recording_folder(recording_folder)

if __name__ == '__main__':
    process_session_folder(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib')