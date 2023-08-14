import deeplabcut
from pathlib import Path
config_path = r"C:\Users\aaron\Desktop\JH_DLC_model-Aaron-2023-07-03\config.yaml"

# deeplabcut.extract_frames(config_path, mode = 'manual', userfeedback=True)

path_to_video_folder = r"D:\2023-06-07_JH\1.0_recordings\treadmill_calib\sesh_2023-06-07_11_55_05_JH_flexion_neg_5_6_trial_1\synchronized_videos"
dest_folder = str(Path(path_to_video_folder)/'dlc_data')

deeplabcut.analyze_videos(config=config_path, gputouse=0, videos = path_to_video_folder, save_as_csv=True, destfolder=dest_folder)