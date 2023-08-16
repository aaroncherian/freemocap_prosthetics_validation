import os
import shutil

def move_data(session_folder):
    # Get all the subdirectories (recording folders) in the session folder
    recording_folders = [d for d in os.listdir(session_folder) if os.path.isdir(os.path.join(session_folder, d))]
    
    for recording_folder in recording_folders:
        recording_folder_path = os.path.join(session_folder, recording_folder)
        output_data_folder = os.path.join(recording_folder_path, 'output_data')
        
        # Check if the 'output_data' folder exists
        if os.path.exists(output_data_folder):
            original_data_folder = os.path.join(output_data_folder, 'original_data')
            
            # Create the 'original_data' folder if it doesn't exist
            if not os.path.exists(original_data_folder):
                os.makedirs(original_data_folder)
            
            # List all the files/folders in 'output_data'
            items = os.listdir(output_data_folder)
            
            # For each item in 'output_data', if it's neither 'raw_data' nor 'original_data', move it to 'original_data'
            for item in items:
                item_path = os.path.join(output_data_folder, item)
                if item not in ['raw_data', 'original_data'] and os.path.exists(item_path):
                    shutil.move(item_path, os.path.join(original_data_folder, item))

            # Move .blend and .blend1 files from recording folder to original_data folder

            for blend_file_ext in ['.blend', '.blend1']:
                blend_filename = recording_folder + blend_file_ext
                blend_path = os.path.join(recording_folder_path, blend_filename)
                if os.path.exists(blend_path):
                    shutil.move(blend_path, os.path.join(original_data_folder, blend_filename))



if __name__ == '__main__':
    move_data(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib')
