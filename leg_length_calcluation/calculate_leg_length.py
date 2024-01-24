from pathlib import Path
from mediapipe_joints import mediapipe_indices
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

path_to_recording_folder = Path(r'D:\2023-06-07_TF01\1.0_recordings\treadmill_calib')

list_of_sessions = ['sesh_2023-06-07_12_38_16_TF01_leg_length_neg_5_trial_1', 'sesh_2023-06-07_12_43_15_TF01_leg_length_neg_25_trial_1', 'sesh_2023-06-07_12_46_54_TF01_leg_length_neutral_trial_1', 'sesh_2023-06-07_12_50_56_TF01_leg_length_pos_25_trial_1', 'sesh_2023-06-07_12_55_21_TF01_leg_length_pos_5_trial_1']
trial_names = ['-12.7mm ', '-6.35mm', '0 inches', '+6.35mm', '+12.7mm']


@dataclass 
class LegJointPositions:
    hip: np.ndarray
    knee: np.ndarray
    ankle: np.ndarray

def calculate_leg_length(leg_joint_positions: LegJointPositions):
    hip = leg_joint_positions.hip
    knee = leg_joint_positions.knee
    ankle = leg_joint_positions.ankle

    # Calculate distances between hip-knee and knee-ankle
    leg_length = np.linalg.norm(knee - hip) + np.linalg.norm(ankle - knee)
    return leg_length


hip_index = mediapipe_indices.index('right_hip')
knee_index = mediapipe_indices.index('right_knee')
ankle_index = mediapipe_indices.index('right_heel')

mean_leg_lengths = []



# Set up figure for subplots
n_sessions = len(list_of_sessions)
fig = plt.figure(figsize=(10, 20))  # Adjust the figure size as needed

mean_leg_lengths = []
std_dev_leg_lengths = []

# Create subplots for line graphs
gs = fig.add_gridspec(n_sessions, 2)
axs_line = [fig.add_subplot(gs[i, 0]) for i in range(n_sessions)]

for i, session in enumerate(list_of_sessions):
    session_path = path_to_recording_folder / session / 'output_data' / 'mediaPipeSkel_3d_body_hands_face.npy'
    body_data = np.load(session_path)
    body_data = body_data[:,:, :]  # Remove the face and hand data

    leg_lengths = []
    for frame_data in body_data:
        joint_positions = LegJointPositions(frame_data[hip_index], frame_data[knee_index], frame_data[ankle_index])
        leg_length = calculate_leg_length(joint_positions)
        leg_lengths.append(leg_length)

    # Plot leg length over time in subplots (column)
    axs_line[i].plot(leg_lengths)
    axs_line[i].set_title(f'{trial_names[i]}')
    axs_line[i].set_xlabel('Frame')
    axs_line[i].set_ylabel('Leg Length (mm)')

    # Calculate and store the mean and standard deviation for the leg length
    mean_leg_length = np.mean(leg_lengths)
    std_dev = np.std(leg_lengths)
    mean_leg_lengths.append(mean_leg_length)
    std_dev_leg_lengths.append(std_dev)

# Bar plot for mean leg lengths with standard deviation
ax_bar = fig.add_subplot(gs[:, 1])
ax_bar.bar(range(n_sessions), mean_leg_lengths, yerr=std_dev_leg_lengths, capsize=5)
ax_bar.set_xticks(range(n_sessions))
ax_bar.set_xticklabels(trial_names, rotation='horizontal')
ax_bar.set_title('Mean Leg Lengths with Std Dev')
ax_bar.set_ylabel('Mean Leg Length')

# Set the y-axis limits to focus on the data range
# Find the maximum mean leg length plus standard deviation
max_mean_length_with_std = max(mean_leg_lengths + np.array(std_dev_leg_lengths))
# Pad the maximum by a small percentage to ensure the top of the error bars are visible
upper_limit = max_mean_length_with_std * 1.05

# Set the lower limit to a bit below the smallest mean leg length, or to 0, whichever is higher
lower_limit = max(min(mean_leg_lengths) - max(std_dev_leg_lengths), 0)

ax_bar.set_ylim(lower_limit, upper_limit)


# Annotate bars with mean value
for j, mean in enumerate(mean_leg_lengths):
    ax_bar.text(j, mean, f'{mean:.2f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()