
import numpy as np

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
