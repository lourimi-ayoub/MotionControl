# MotionControl

**MotionControl** is a gesture-based control system that uses a webcam to detect hand gestures and trigger corresponding actions on your computer. It uses **MediaPipe** for hand tracking and **PyAutoGUI** to simulate keypresses for controlling media functions such as volume, play/pause, forward/rewind, and fullscreen.

### Features:

*   Control media playback (play/pause, forward, rewind).
*   Adjust volume (volume up, volume down).
*   Toggle fullscreen mode.
*   Easy-to-use gesture detection for intuitive control.
*   Real-time webcam feedback for accurate interaction.

### Technologies:

*   **Python**: The programming language used for the project.
*   **OpenCV**: Used for capturing webcam frames.
*   **MediaPipe**: Utilized for hand tracking and gesture detection.
*   **PyAutoGUI**: Simulates keyboard input to control media actions.

### Installation:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/MotionControl.git
    cd MotionControl
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    **requirements.txt**:
    ```
    opencv-python
    mediapipe
    pyautogui
    ```

### Usage:

1. Run the script:
    ```bash
    python script.py
    ```

2. The application will start detecting your hand gestures using the webcam:
    *   **Fist**: Press 'ESC'.
    *   **Play/Pause**: Press 'Space'.
    *   **Forward**: Press the right arrow key.
    *   **Rewind**: Press the left arrow key.
    *   **Volume Up**: Increase the volume.
    *   **Volume Down**: Decrease the volume.
    *   **Fullscreen**: Toggle fullscreen mode.

3. To exit the program, press the `Q` key.

### Gesture Recognition:

The system detects the following gestures:
*   **Fist**: All fingers closed. 
*   **Play/Pause**: All fingers open.
*   **Forward**: Only the index finger extended.
*   **Rewind**: Thumb extended.
*   **Volume Up**: Index and middle fingers extended.
*   **Volume Down**: Index, middle, and ring fingers extended.
*   **Fullscreen**: Index, middle, and ring fingers extended with the pinky folded.

### Configuration:

You can customize the following settings in the script:
*   `MAX_NUM_HANDS`: The maximum number of hands to detect (default is 1).
*   `DETECTION_CONFIDENCE`: Confidence threshold for hand detection (default is 0.7).
*   `GESTURE_COOLDOWN`: Delay between actions to prevent repetitive gestures (default is 0.8 seconds).
*   `VOLUME_REPEAT_DELAY`: Delay before repeating volume gestures (default is 1.5 seconds).

### Contributing:

If you find any issues or would like to contribute, feel free to fork the repository and create a pull request.

### License:

This project is licensed under the MIT License.
