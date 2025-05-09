# Gesture-Based PC Shutdown

This program allows you to shut down your PC by showing your middle finger to the webcam. It uses OpenCV and MediaPipe for hand gesture detection.

## Requirements

- Python 3.7 or higher
- Webcam
- Required Python packages (listed in requirements.txt)

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the program:
```bash
python main.py
```

2. The program will open your webcam feed and start detecting hand gestures.
3. To shut down your PC:
   - Show your middle finger to the camera
   - Hold the gesture for 2 seconds
   - The PC will shut down automatically
4. To quit the program without shutting down, press 'q'

## Safety Features

- The gesture must be held for 2 seconds to prevent accidental shutdowns
- You can quit the program at any time by pressing 'q'
- The program requires clear hand visibility and good lighting conditions

## Note

This program uses the Windows shutdown command. If you're using a different operating system, you may need to modify the shutdown command in the code. 