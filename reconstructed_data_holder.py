from reconstruction.reconstruct_3d import process_2d_data_to_3d

class ReconstructedDataHolder:
    def __init__(self, calibration_toml_path,joint_data):
        self.calibration_toml_path = calibration_toml_path
        self.joint_data = joint_data
    
    def reconstruct_3d_data(self, start_frame=None, end_frame=None):

        data_3d, repro_error = process_2d_data_to_3d(mediapipe_2d_data=self.joint_data, calibration_toml_path=self.calibration_toml_path, mediapipe_confidence_cutoff_threshold=.7)
        self.data_3d = data_3d

        return self.data_3d
