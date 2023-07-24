from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class FileManager:
    def __init__(self, path_to_recording_folder):
        self.path_to_recording_folder = path_to_recording_folder
        self.path_to_3d_dlc_data = self.path_to_recording_folder / 'output_data' / 'dlc_leg_3d.npy'
        self.path_to_3d_freemocap_data = self.path_to_recording_folder / 'output_data'/'raw_data' / 'mediapipe3dData_numFrames_numTrackedPoints_spatialXYZ.npy'


path_to_recording_folder = Path(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_JH_flexion_neutral_trial_1')


import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Initialize file manager
file_manager = FileManager(path_to_recording_folder)

# Load data from npy files
data_dlc = np.load(file_manager.path_to_3d_dlc_data)
data_freemocap = np.load(file_manager.path_to_3d_freemocap_data)

# Select first frame of both datasets
data_dlc_frame1 = data_dlc[1000,:,:] # Assumes data shape is (frames, markers, coordinates)
data_freemocap_frame1 = data_freemocap[1000,:,:] # Assumes data shape is (frames, markers, coordinates)

# Create 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Add data to scatter plot (you may need to adjust the array indices depending on how your data is organized)
ax.scatter(data_dlc_frame1[:,0], data_dlc_frame1[:,1], data_dlc_frame1[:,2], color='b')
ax.scatter(data_freemocap_frame1[:,0], data_freemocap_frame1[:,1], data_freemocap_frame1[:,2], color='r')

mean_x = np.nanmean(data_freemocap[:, :, 0]) # Calculating mean for x across all frames in data_dlc
mean_y = np.nanmean(data_freemocap[:, :, 1]) # Calculating mean for y across all frames in data_dlc
mean_z = np.nanmean(data_freemocap[:, :, 2]) # Calculating mean for z across all frames in data_dlc

ax_range = 900  # Adjust as needed based on your data

# Set equal axes based on mean for entire data
ax.set_xlim([mean_x - ax_range, mean_x + ax_range])
ax.set_ylim([mean_y - ax_range, mean_y + ax_range])
ax.set_zlim([mean_z - ax_range, mean_z + ax_range])


# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Display plot
plt.show()
