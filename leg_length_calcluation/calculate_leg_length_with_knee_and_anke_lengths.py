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

def calculate_segment_lengths(leg_joint_positions: LegJointPositions):
    hip = leg_joint_positions.hip
    knee = leg_joint_positions.knee
    ankle = leg_joint_positions.ankle

    # Calculate distances between hip-knee and knee-ankle
    hip_knee_length = np.linalg.norm(knee - hip)
    knee_ankle_length = np.linalg.norm(ankle - knee)
    return hip_knee_length, knee_ankle_length


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

# Now we will also store the segment lengths
hip_knee_lengths_sessions = []
knee_ankle_lengths_sessions = []

for i, session in enumerate(list_of_sessions):
    session_path = path_to_recording_folder / session / 'output_data' / 'mediapipe_body_3d_xyz.npy'
    body_data = np.load(session_path)
    # body_data = body_data[0:250,:, :]  # Remove the face and hand data
    leg_lengths = []
    hip_knee_lengths = []
    knee_ankle_lengths = []
    for frame_data in body_data:
        joint_positions = LegJointPositions(frame_data[hip_index], frame_data[knee_index], frame_data[ankle_index])
        
        # Get segment lengths
        hip_knee_length, knee_ankle_length = calculate_segment_lengths(joint_positions)
        hip_knee_lengths.append(hip_knee_length)
        knee_ankle_lengths.append(knee_ankle_length)
        
        # Calculate total leg length and add to list
        leg_length = hip_knee_length + knee_ankle_length
        leg_lengths.append(leg_length)

    # Store the segment lengths for all sessions
    hip_knee_lengths_sessions.append(hip_knee_lengths)
    knee_ankle_lengths_sessions.append(knee_ankle_lengths)

    # Plot total leg length, hip-knee, and knee-ankle lengths over time in subplots (column)
    axs_line[i].plot(leg_lengths, label='Total Leg Length')
    axs_line[i].plot(hip_knee_lengths, label='Hip-Knee Length')
    axs_line[i].plot(knee_ankle_lengths, label='Knee-Ankle Length')
    axs_line[i].set_title(f'{session}')
    axs_line[i].set_xlabel('Frame')
    axs_line[i].set_ylabel('Length')
    axs_line[i].legend()

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



## for qualisys
from qualisys_joint import qualisys_markers

hip_index = qualisys_markers.index('right_hip')
knee_index = qualisys_markers.index('right_knee')
ankle_index = qualisys_markers.index('right_heel')

mean_leg_lengths = []



# Set up figure for subplots
n_sessions = len(list_of_sessions)
fig = plt.figure(figsize=(10, 20))  # Adjust the figure size as needed

mean_leg_lengths = []
std_dev_leg_lengths = []

# Create subplots for line graphs
gs = fig.add_gridspec(n_sessions, 2)
axs_line = [fig.add_subplot(gs[i, 0]) for i in range(n_sessions)]

# Now we will also store the segment lengths
hip_knee_lengths_sessions = []
knee_ankle_lengths_sessions = []

for i, session in enumerate(list_of_sessions):
    session_path = path_to_recording_folder / session / 'qualisys_data' / 'qualisys_joint_centers_3d_xyz.npy'
    body_data = np.load(session_path)
    # body_data = body_data[0:250,:, :]  # Remove the face and hand data
    leg_lengths = []
    hip_knee_lengths = []
    knee_ankle_lengths = []
    for frame_data in body_data:
        joint_positions = LegJointPositions(frame_data[hip_index], frame_data[knee_index], frame_data[ankle_index])
        
        # Get segment lengths
        hip_knee_length, knee_ankle_length = calculate_segment_lengths(joint_positions)
        hip_knee_lengths.append(hip_knee_length)
        knee_ankle_lengths.append(knee_ankle_length)
        
        # Calculate total leg length and add to list
        leg_length = hip_knee_length + knee_ankle_length
        leg_lengths.append(leg_length)

    # Store the segment lengths for all sessions
    hip_knee_lengths_sessions.append(hip_knee_lengths)
    knee_ankle_lengths_sessions.append(knee_ankle_lengths)

    # Plot total leg length, hip-knee, and knee-ankle lengths over time in subplots (column)
    axs_line[i].plot(leg_lengths, label='Total Leg Length')
    axs_line[i].plot(hip_knee_lengths, label='Hip-Knee Length')
    axs_line[i].plot(knee_ankle_lengths, label='Knee-Ankle Length')
    axs_line[i].set_title(f'{session}')
    axs_line[i].set_xlabel('Frame')
    axs_line[i].set_ylabel('Length')
    axs_line[i].legend()

    # Calculate and store the mean and standard deviation for the leg length
    mean_leg_length = np.nanmean(leg_lengths)
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