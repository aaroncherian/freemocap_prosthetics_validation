from pathlib import Path
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QSlider, QWidget, QCheckBox, QPushButton, QGroupBox, QLabel, QLineEdit
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class FileManager:
    def __init__(self, path_to_recording_folder):
        self.path_to_recording_folder = path_to_recording_folder
        self.path_to_3d_dlc_data = self.path_to_recording_folder / 'output_data' / 'dlc_leg_3d.npy'
        self.path_to_3d_freemocap_data = self.path_to_recording_folder / 'output_data'/'raw_data' / 'mediapipe3dData_numFrames_numTrackedPoints_spatialXYZ.npy'

mediapipe_markers = [
    'nose',
    'left_eye_inner',
    'left_eye',
    'left_eye_outer',
    'right_eye_inner',
    'right_eye',
    'right_eye_outer',
    'left_ear',
    'right_ear',
    'mouth_left',
    'mouth_right',
    'left_shoulder',
    'right_shoulder',
    'left_elbow',
    'right_elbow',
    'left_wrist',
    'right_wrist',
    'left_pinky',
    'right_pinky',
    'left_index',
    'right_index',
    'left_thumb',
    'right_thumb',
    'left_hip',
    'right_hip',
    'left_knee',
    'right_knee',
    'left_ankle',
    'right_ankle',
    'left_heel',
    'right_heel',
    'left_foot_index',
    'right_foot_index'
]

dlc_markers = [
'right_hip',
'right_knee',
'right_ankle',
'right_heel',
'right_foot_index',
]


class MainWindow(QMainWindow):
    def __init__(self, data_3d):
        super().__init__()
        self.setWindowTitle('Spliced Data Viewer')

        self.layout = QVBoxLayout()

        plot_widget = ScatterPlot3DWidget(data_3d)
        # plot_widget.set_layout(self.layout)

        self.setCentralWidget(plot_widget)

class ScatterPlot3DWidget(QWidget):
    def __init__(self, data_3d, parent=None):
        super(ScatterPlot3DWidget, self).__init__(parent)
        self.data_3d = data_3d

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Slider Layout
        self.slider_layout = QHBoxLayout()
        self.layout.addLayout(self.slider_layout)

        # Frame label
        self.frame_label = QLabel("Frame 0")
        self.slider_layout.addWidget(self.frame_label)


        # 3D Scatter Plot
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.layout.addWidget(self.canvas)


        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        # self.slider.setMaximum(0)  # Initially set to 0
        self.slider.setMaximum(len(data_3d) - 1)
        # self.slider.setEnabled(False)  # Initially disabled
        self.slider.valueChanged.connect(self.update_plot)
        self.slider_layout.addWidget(self.slider)

        # Axis range
        self.ax_range = 900
        self.mean_x = np.nanmean(data_3d[:, 0:33, 0])
        self.mean_y = np.nanmean(data_3d[:, 0:33, 1])
        self.mean_z = np.nanmean(data_3d[:, 0:33, 2])

    def update_plot(self, value):
        # Clear the current plot
        self.ax.cla()

        # Update frame label
        self.frame_label.setText(f"Frame {value}")

        # Get the data for the selected frame
        frame_data = self.data_3d[value, 0:33, :]

        # Update the scatter plot with the new data
        self.ax.scatter(frame_data[:, 0], frame_data[:, 1], frame_data[:, 2])

        # Set equal axes based on mean for entire reconstructed data
        self.ax.set_xlim([self.mean_x - self.ax_range, self.mean_x + self.ax_range])
        self.ax.set_ylim([self.mean_y - self.ax_range, self.mean_y + self.ax_range])
        self.ax.set_zlim([self.mean_z - self.ax_range, self.mean_z + self.ax_range])

        # Redraw the plot
        self.canvas.draw()

path_to_recording_folder = Path(r'D:\2023-06-07_JH\1.0_recordings\treadmill_calib\sesh_2023-06-07_12_06_15_JH_flexion_neutral_trial_1')

file_manager = FileManager(path_to_recording_folder)

data_dlc = np.load(file_manager.path_to_3d_dlc_data)
data_freemocap = np.load(file_manager.path_to_3d_freemocap_data)

spliced_data = data_freemocap.copy()

for dlc_marker in dlc_markers:
    mediapipe_marker_index = mediapipe_markers.index(dlc_marker)
    spliced_data[:, mediapipe_marker_index, :] = data_dlc[:, dlc_markers.index(dlc_marker), :]
  
app = QApplication([])
win = MainWindow(spliced_data)
win.show()
app.exec()

np.save(path_to_recording_folder / 'output_data' / 'freemocap_spliced.npy', spliced_data)

