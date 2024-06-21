# PyCAM

**PyCAM** is a desktop application that allows you to use your phone as a webcam on your PC. It is built using PySide6 and provides a simple and intuitive interface for streaming video from a URL or a default camera. The application also supports virtual camera functionality, making it compatible with video conferencing tools like Google Meet, Zoom, and Skype.

## Features

### 1. **Get Started Screen**
   - A welcome screen that introduces the application to the user.
   - Provides instructions and a "Continue" button to proceed to the main application.

### 2. **Stream URL Input**
   - An input field for the user to enter the URL of the video stream.
   - Option to leave the input field empty to use the default camera.

### 3. **Start and Stop Buttons**
   - **Start Button**: Begins the video stream from the specified URL or the default camera.
   - **Stop Button**: Stops the video stream and releases the camera resources.

### 4. **Video Display**
   - Displays the live video feed in the application window.
   - Supports scaling and maintaining the aspect ratio of the video feed.

### 5. **Virtual Camera Support**
   - Initializes a virtual camera using `pyvirtualcam` to broadcast the video feed.
   - Makes the video feed available to other applications like Google Meet, Zoom, and Skype.
   - Streams at 30fps or 60fps when possible.

### 6. **Application Icon and Logo**
   - Customizable application icon and logo.
   - Branding the application with the name "PyCAM".

### 7. **User-Friendly Interface**
   - Uses the Roboto font for a modern and clean look.
   - Provides padding and alignment for input fields, buttons, and video display for a better user experience.

### 8. **Error Handling**
   - Prints error messages in case the video stream fails to open or read frames.

## Pakage Used


```bash
pip install opencv-python pyvirtualcam pyside6


## Setup Instructions

<a href="https://github.com/Sarwarhridoy4/PyCam/releases/download/1.0/PyCam.exe" download>
    <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        <img src="https://img.shields.io/badge/Download-Now-brightgreen" alt="Download Now">
    </button>
</a>

