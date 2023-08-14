import numpy as np
from pathlib import Path
import pandas as pd

def apply_confidence_threshold(array, threshold):
    """
    Set X,Y values to zero where the corresponding confidence value is below threshold.

    Parameters:
    - array: 4D numpy array with shape (num_cameras, num_frames, num_markers, 3)
      The last dimension should have the structure (x, y, confidence).
    - threshold: Confidence threshold. All X,Y values with a confidence below this threshold will be set to zero.
    """
    confidences = array[:, :, :, 2]  # Get the confidence values
    mask = confidences < threshold  # Create a boolean mask where the confidence values are below threshold
    array[mask, 0:2] = np.nan  # Set the X,Y values to zero where the mask is True
    return array

# Path to your csv folder
path_to_folder_with_csvs = Path(r'C:\Users\aaron\Desktop\JH_DLC_model-Aaron-2023-07-03\videos')
path_to_save = Path(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_JH_flexion_neutral_trial_1\output_data\raw_data')
# Filtered csv list
filtered_csv_list = sorted(list(path_to_folder_with_csvs.glob('*filtered*.csv')))

# Initialize an empty list to hold dataframes
dfs = []



for csv in filtered_csv_list:
    # Read each csv into a dataframe with a multi-index header
    df = pd.read_csv(csv, header=[1, 2])
    
    # Drop the first column (which just has the headers )
    df = df.iloc[:, 1:]
    
    # Check if data shape is as expected
    if df.shape[1] % 3 != 0:
        print(f"Unexpected number of columns in {csv}: {df.shape[1]}")
        continue
    
    try:
        # Convert the df into a 4D numpy array of shape (1, num_frames, num_markers, 3) and append to dfs
        dfs.append(df.values.reshape(1, df.shape[0], df.shape[1]//3, 3))
    except ValueError as e:
        print(f"Reshape failed for {csv} with shape {df.shape}: {e}")


# Concatenate all the arrays along the first axis (camera axis)
final_array = np.concatenate(dfs, axis=0)
final_thresholded_array = apply_confidence_threshold(final_array, 0.6)

f = 2
# Save the final_array as numpy array file
np.save(path_to_save/'dlc_leg_2d.npy', final_array)
np.save(path_to_save/'dlc_leg_2d_thresholded.npy', final_thresholded_array)




