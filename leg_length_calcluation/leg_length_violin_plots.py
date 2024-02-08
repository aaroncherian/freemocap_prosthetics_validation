import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from dataclasses import dataclass
from mediapipe_joints import mediapipe_indices
from qualisys_joint import qualisys_markers

# Dataclass to hold joint positions
@dataclass
class LegJointPositions:
    hip: np.ndarray
    knee: np.ndarray
    ankle: np.ndarray

# Function to calculate leg length
def calculate_leg_length(leg_joint_positions: LegJointPositions):
    hip_knee_length = np.linalg.norm(leg_joint_positions.knee - leg_joint_positions.hip)
    knee_ankle_length = np.linalg.norm(leg_joint_positions.ankle - leg_joint_positions.knee)
    return hip_knee_length + knee_ankle_length

# Indices for hip, knee, and ankle joints
hip_index_mediapipe = mediapipe_indices.index('right_hip')
knee_index_mediapipe = mediapipe_indices.index('right_knee')
ankle_index_mediapipe = mediapipe_indices.index('right_ankle')

hip_index_qualisys = qualisys_markers.index('right_hip')
knee_index_qualisys = qualisys_markers.index('right_knee')
ankle_index_qualisys = qualisys_markers.index('right_ankle')

# Path to recording folder
path_to_recording_folder = Path(r'D:\2023-06-07_TF01\1.0_recordings\treadmill_calib')

# List of sessions and trial names
list_of_sessions = ['sesh_2023-06-07_12_38_16_TF01_leg_length_neg_5_trial_1', 
                    'sesh_2023-06-07_12_43_15_TF01_leg_length_neg_25_trial_1', 
                    'sesh_2023-06-07_12_46_54_TF01_leg_length_neutral_trial_1', 
                    'sesh_2023-06-07_12_50_56_TF01_leg_length_pos_25_trial_1', 
                    'sesh_2023-06-07_12_55_21_TF01_leg_length_pos_5_trial_1']
trial_names = ['-12.7mm', '-6.35mm', '0 inches', '+6.35mm', '+12.7mm']

# Initialize lists to hold the combined data for plotting
combined_data = []
system_labels = []
trial_labels = []

# Load data and calculate leg lengths for both FreeMoCap and Qualisys
for trial_name, session in zip(trial_names, list_of_sessions):
    # Load FreeMoCap data
    freemocap_data_path = path_to_recording_folder / session / 'mediapipe_yolo_dlc_output_data' / 'mediaPipeSkel_3d_body_hands_face.npy'
    freemocap_data = np.load(freemocap_data_path)[:, :, :33]  # Assuming the first 33 columns are body data



    # Calculate leg lengths for FreeMoCap
    freemocap_leg_lengths = []
    for frame_data in freemocap_data:
        joint_positions = LegJointPositions(frame_data[hip_index_mediapipe], 
                                            frame_data[knee_index_mediapipe], 
                                            frame_data[ankle_index_mediapipe])
        leg_length = calculate_leg_length(joint_positions)
        freemocap_leg_lengths.append(leg_length)
    

    
    # Append the data for violin plot
    combined_data.extend(freemocap_leg_lengths)
    system_labels.extend(['FreeMoCap'] * len(freemocap_leg_lengths))
    trial_labels.extend([trial_name] * (len(freemocap_leg_lengths))) 

# Create a DataFrame for seaborn
import pandas as pd
data = pd.DataFrame({'Leg Length': combined_data, 'System': system_labels, 'Trial': trial_labels})

# Plot the split violin plot
plt.figure(figsize=(15, 10))
sns.violinplot(x='Trial', y='Leg Length', hue='System', data=data, split=False, inner='quart', palette='pastel')
plt.title('FreeMoCap Leg Lengths')
plt.legend(loc='upper left')
plt.tight_layout()
# plt.show()


### To plot qualisys

combined_data = []
system_labels = []
trial_labels = []

for trial_name, session in zip(trial_names, list_of_sessions):
    # Load Qualisys data
    qualisys_data_path = path_to_recording_folder / session / 'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy'
    qualisys_data = np.load(qualisys_data_path)

    # Calculate leg lengths for Qualisys
    qualisys_leg_lengths = []
    for frame_data in qualisys_data:
        joint_positions = LegJointPositions(frame_data[hip_index_qualisys], 
                                            frame_data[knee_index_qualisys], 
                                            frame_data[ankle_index_qualisys])
        leg_length = calculate_leg_length(joint_positions)
        qualisys_leg_lengths.append(leg_length)

    # Append the data for violin plot

    combined_data.extend(qualisys_leg_lengths)
    system_labels.extend(['Qualisys'] * len(qualisys_leg_lengths))
    trial_labels.extend([trial_name] * (len(qualisys_leg_lengths)))


import pandas as pd
data = pd.DataFrame({'Leg Length': combined_data, 'System': system_labels, 'Trial': trial_labels})

# Plot the split violin plot
plt.figure(figsize=(15, 10))
sns.violinplot(x='Trial', y='Leg Length', data=data, split=False, inner='quart', color = 'orange')
plt.title('Qualisys Leg Lengths')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show() 
