# Gesture-Based PC Shutdown

This program allows you to shut down your PC by showing your middle finger to the webcam. It uses OpenCV and MediaPipe for hand gesture detection.


Install the required packages:
```bash
pip install -r requirements.txt
```

 Run the program:
```bash
python main.py
```

The program will open your webcam feed and start detecting hand gestures.
To shut down your PC:
  - Show your middle finger to the camera
  - Hold the gesture for 2 seconds
  - The PC will shut down automatically
To quit the program without shutting down, press 'q'
