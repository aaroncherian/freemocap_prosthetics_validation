import threshold_2d_data
from pathlib import Path
import numpy as np

from reconstructed_data_holder import ReconstructedDataHolder

class FileManager:
    def __init__(self, path_to_recording_folder):
        self.path_to_recording_folder = path_to_recording_folder
        self.path_to_2d_dlc_data = self.path_to_recording_folder / 'output_data' / 'raw_data' / 'dlc_leg_2d.npy'
        self.path_to_save_3d_data = self.path_to_recording_folder / 'output_data' / 'dlc_leg_3d.npy'
    def load_2d_joint_data(self):
        return np.load(self.path_to_2d_dlc_data)
    def save_3d_joint_data(self, data_3d):
        np.save(self.path_to_save_3d_data, data_3d)

path_to_calibration_toml = Path(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib\sesh_2023-06-07_11_10_50_treadmill_calibration_01\sesh_2023-06-07_11_10_50_treadmill_calibration_01_camera_calibration.toml')
path_to_recording_folder = Path(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_JH_flexion_neutral_trial_1')
file_manager = FileManager(path_to_recording_folder)
dlc_2d_data = file_manager.load_2d_joint_data()

thresholded_dlc_2d_Data = threshold_2d_data.apply_confidence_threshold(array=dlc_2d_data, threshold=0.7)

reconstructed_data_holder = ReconstructedDataHolder(calibration_toml_path=path_to_calibration_toml, joint_data=thresholded_dlc_2d_Data[:,:,:,:2])

dlc_data_3d = reconstructed_data_holder.reconstruct_3d_data()

file_manager.save_3d_joint_data(dlc_data_3d)


f = 2 