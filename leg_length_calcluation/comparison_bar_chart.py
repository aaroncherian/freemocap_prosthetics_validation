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
ankle_index_mediapipe = mediapipe_indices.index('right_heel')

hip_index_qualisys = qualisys_markers.index('right_hip')
knee_index_qualisys = qualisys_markers.index('right_knee')
ankle_index_qualisys = qualisys_markers.index('right_heel')

# Path to recording folder
path_to_recording_folder = Path(r'D:\2023-06-07_TF01\1.0_recordings\treadmill_calib')

# List of sessions and trial names
list_of_sessions = ['sesh_2023-06-07_12_38_16_TF01_leg_length_neg_5_trial_1', 
                    'sesh_2023-06-07_12_43_15_TF01_leg_length_neg_25_trial_1', 
                    'sesh_2023-06-07_12_46_54_TF01_leg_length_neutral_trial_1', 
                    'sesh_2023-06-07_12_50_56_TF01_leg_length_pos_25_trial_1', 
                    'sesh_2023-06-07_12_55_21_TF01_leg_length_pos_5_trial_1']
trial_names = ['-12.7mm', '-6.35mm', '0mm', '+6.35mm', '+12.7mm']

delta_names = ['-12.7mm', '-6.35mm', '+6.35mm', '+12.7mm']

# Initialize lists to hold the combined data for plotting
combined_data = []
system_labels = []
trial_labels = []

# Load data and calculate leg lengths for both FreeMoCap and Qualisys
# for trial_name, session in zip(trial_names, list_of_sessions):
#     # Load FreeMoCap data
#     freemocap_data_path = path_to_recording_folder / session / 'output_data' / 'mediaPipeSkel_3d_body_hands_face.npy'
#     freemocap_data = np.load(freemocap_data_path)[:, :, :33]  # Assuming the first 33 columns are body data

#     # Load Qualisys data
#     qualisys_data_path = path_to_recording_folder / session / 'qualisys_data'/ 'qualisys_joint_centers_3d_xyz.npy'
#     qualisys_data = np.load(qualisys_data_path)

#     # Calculate leg lengths for FreeMoCap
#     freemocap_leg_lengths = []
#     for frame_data in freemocap_data:
#         joint_positions = LegJointPositions(frame_data[hip_index_mediapipe], 
#                                             frame_data[knee_index_mediapipe], 
#                                             frame_data[ankle_index_mediapipe])
#         leg_length = calculate_leg_length(joint_positions)
#         freemocap_leg_lengths.append(leg_length)
    
#     # Calculate leg lengths for Qualisys
#     qualisys_leg_lengths = []
#     for frame_data in qualisys_data:
#         joint_positions = LegJointPositions(frame_data[hip_index_qualisys], 
#                                             frame_data[knee_index_qualisys], 
#                                             frame_data[ankle_index_qualisys])
#         leg_length = calculate_leg_length(joint_positions)
#         qualisys_leg_lengths.append(leg_length)

# Expected delta values (converted from mm to the same unit as your data, assuming it is in mm)
expected_deltas = np.array([-12.7, -6.35, 6.35, 12.7])  # Convert these values if necessary

# Neutral index (the index of '0 inches' in your trial_names)
neutral_index = trial_names.index('0mm')

# Initialize lists to hold delta values for each system
qualisys_deltas = []
freemocap_deltas = []

# Load neutral lengths for both systems
neutral_freemocap_data_path = path_to_recording_folder / list_of_sessions[neutral_index] / 'output_data' / 'mediaPipeSkel_3d_body_hands_face.npy'
neutral_freemocap_data = np.load(neutral_freemocap_data_path)[:, :, :33]
neutral_freemocap_leg_length = np.mean([calculate_leg_length(LegJointPositions(frame[hip_index_mediapipe], frame[knee_index_mediapipe], frame[ankle_index_mediapipe])) for frame in neutral_freemocap_data])

neutral_qualisys_data_path = path_to_recording_folder / list_of_sessions[neutral_index] / 'qualisys_data' / 'qualisys_joint_centers_3d_xyz.npy'
neutral_qualisys_data = np.load(neutral_qualisys_data_path)
neutral_qualisys_leg_length = np.mean([calculate_leg_length(LegJointPositions(frame[hip_index_qualisys], frame[knee_index_qualisys], frame[ankle_index_qualisys])) for frame in neutral_qualisys_data])

# Calculate deltas for both systems
for i, session in enumerate(list_of_sessions):
    # Skip the neutral session
    if i == neutral_index:
        continue

    # FreeMoCap data
    freemocap_data_path = path_to_recording_folder / session / 'output_data' / 'mediaPipeSkel_3d_body_hands_face.npy'
    freemocap_data = np.load(freemocap_data_path)[:, :, :33]
    mean_freemocap_leg_length = np.nanmean([calculate_leg_length(LegJointPositions(frame[hip_index_mediapipe], frame[knee_index_mediapipe], frame[ankle_index_mediapipe])) for frame in freemocap_data])
    freemocap_deltas.append(mean_freemocap_leg_length - neutral_freemocap_leg_length)

    # Qualisys data
    qualisys_data_path = path_to_recording_folder / session / 'qualisys_data' / 'qualisys_joint_centers_3d_xyz.npy'
    qualisys_data = np.load(qualisys_data_path)
    mean_qualisys_leg_length = np.nanmean([calculate_leg_length(LegJointPositions(frame[hip_index_qualisys], frame[knee_index_qualisys], frame[ankle_index_qualisys])) for frame in qualisys_data])
    qualisys_deltas.append(mean_qualisys_leg_length - neutral_qualisys_leg_length)

# Plot the deltas
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.25
index = np.arange(len(expected_deltas))

bar1 = ax.bar(index, expected_deltas, bar_width, label='Expected', color = 'black')
bar2 = ax.bar(index + bar_width, qualisys_deltas, bar_width, label='Qualisys', color = 'C1')
bar3 = ax.bar(index + 2 * bar_width, freemocap_deltas, bar_width, label='FreeMoCap', color = 'C0')

ax.set_xlabel('Trial')
ax.set_ylabel('Delta Leg Length (mm)')
ax.set_title('Delta in Leg Length Compared to Neutral')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(delta_names)
ax.legend()

plt.tight_layout()
plt.show()