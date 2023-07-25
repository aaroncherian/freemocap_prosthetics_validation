from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

class FileManager:
    def __init__(self, path_to_recording_folder):
        self.path_to_recording_folder = path_to_recording_folder
        self.path_to_3d_dlc_data = self.path_to_recording_folder / 'output_data' / 'dlc_leg_3d.npy'
        self.path_to_3d_freemocap_data = self.path_to_recording_folder / 'output_data'/'raw_data' / 'mediapipe3dData_numFrames_numTrackedPoints_spatialXYZ.npy'

path_to_recording_folder = Path(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_JH_flexion_neutral_trial_1')

# Initialize file manager
file_manager = FileManager(path_to_recording_folder)

# Load data from npy files
data_dlc = np.load(file_manager.path_to_3d_dlc_data)
data_freemocap = np.load(file_manager.path_to_3d_freemocap_data)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Create space at the bottom for slider

ax3d = fig.add_subplot(111, projection='3d')

# Slider
slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])  # Dimensions [left, bottom, width, height] of the slider
frame_slider = Slider(slider_ax, 'Frame', 0, len(data_dlc)-1, valinit=0, valstep=1)

def update(val):
    frame_num = int(frame_slider.val)
    ax3d.clear()
    
    data_dlc_frame = data_dlc[frame_num,:,:] 
    data_freemocap_frame = data_freemocap[frame_num,:,:]
    
    ax3d.scatter(data_dlc_frame[:,0], data_dlc_frame[:,1], data_dlc_frame[:,2], color='b')
    ax3d.scatter(data_freemocap_frame[:,0], data_freemocap_frame[:,1], data_freemocap_frame[:,2], color='r')
    
    mean_x = np.nanmean(data_freemocap[:, :, 0])
    mean_y = np.nanmean(data_freemocap[:, :, 1])
    mean_z = np.nanmean(data_freemocap[:, :, 2])
    
    ax_range = 900  

    ax3d.set_xlim([mean_x - ax_range, mean_x + ax_range])
    ax3d.set_ylim([mean_y - ax_range, mean_y + ax_range])
    ax3d.set_zlim([mean_z - ax_range, mean_z + ax_range])

    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    
    fig.canvas.draw_idle()

frame_slider.on_changed(update)

# Initial plot
update(0)

plt.show()