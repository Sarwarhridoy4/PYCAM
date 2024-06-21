from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, \
    QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap, QFont, QIcon
import cv2
import pyvirtualcam
import sys
import numpy as np
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GetStartedScreen(QWidget):
    def __init__(self, continue_callback):
        super().__init__()

        self.setWindowTitle("Get Started")
        self.setGeometry(100, 100, 800, 600)

        title = QLabel("Welcome to PyCAM", self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Roboto", 18, QFont.Bold))

        instruction = QLabel("Click 'Continue' to proceed...", self)
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setFont(QFont("Roboto", 14))

        continue_button = QPushButton("Continue", self)
        continue_button.clicked.connect(continue_callback)
        continue_button.setFont(QFont("Roboto", 14))

        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(instruction)
        layout.addWidget(continue_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)


class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyCAM")
        self.setGeometry(100, 100, 800, 600)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter the stream URL or leave empty to use default camera")
        self.url_input.setFixedWidth(400)
        self.url_input.setFont(QFont("Roboto", 12))

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_stream)
        self.start_button.setFont(QFont("Roboto", 12))

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_stream)
        self.stop_button.setFont(QFont("Roboto", 12))

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(640, 480)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Stream URL:"))
        input_layout.addWidget(self.url_input)
        input_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.virtual_camera = None

    def start_stream(self):
        url = self.url_input.text().strip()  # Ensure no leading/trailing whitespace
        fps = 30  # Default FPS
        if url:
            try:
                # Use OpenCV's VideoCapture with the correct API for HTTP/HTTPS streams
                self.cap = cv2.VideoCapture()
                if not self.cap.open(url):
                    print(f"Failed to open stream from URL '{url}'.")
                    return

                # Check if capture is opened
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FPS, fps)
                    self.start_button.setEnabled(False)
                    self.stop_button.setEnabled(True)
                    self.timer.start(int(1000 / fps))  # Update interval based on desired FPS
                    print(f"Stream from URL '{url}' opened successfully.")
                else:
                    print(f"Failed to open stream from URL '{url}'.")
            except Exception as e:
                print(f"Error opening stream: {str(e)}")
        else:
            # Use the default camera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Failed to open default camera.")
                return

            # Set desired FPS
            self.cap.set(cv2.CAP_PROP_FPS, fps)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.timer.start(int(1000 / fps))  # Update interval based on desired FPS
            print("Default camera opened successfully.")

        # Initialize virtual camera
        self.virtual_camera = pyvirtualcam.Camera(width=640, height=480, fps=fps)

    def stop_stream(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.image_label.clear()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        if self.virtual_camera:
            self.virtual_camera.close()
            self.virtual_camera = None

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            convert_to_Qt_format = QImage(frame_rgb.data, w, h, QImage.Format_RGB888)

            # Calculate scaled size
            aspect_ratio = w / h if h != 0 else 1.0
            target_width = min(self.image_label.width(), int(self.image_label.height() * aspect_ratio))
            target_height = min(self.image_label.height(), int(self.image_label.width() / aspect_ratio))

            p = QPixmap.fromImage(convert_to_Qt_format).scaled(target_width, target_height, Qt.KeepAspectRatio)
            self.image_label.setPixmap(p)

            if self.virtual_camera:
                # Convert frame to virtual camera format
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                self.virtual_camera.send(frame_bgr)
                self.virtual_camera.sleep_until_next_frame()
        else:
            print("Failed to read frame")


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyCAM")
        self.setGeometry(100, 100, 800, 600)

        # Set window icon
        self.setWindowIcon(QIcon(resource_path("./assets/logo.png")))  # Provide the path to your logo file

        self.get_started_screen = GetStartedScreen(self.show_main_app)
        self.webcam_app = WebcamApp()

        self.setCentralWidget(self.get_started_screen)

    def show_main_app(self):
        self.setCentralWidget(self.webcam_app)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set global font
    app_font = QFont("Roboto", 12)
    app.setFont(app_font)

    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec())
