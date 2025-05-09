import cv2
import mediapipe as mp
import numpy as np
import os
import time

def detect_middle_finger(hand_landmarks):
    """
    Detect if the middle finger is raised while other fingers are down
    """
    # Get finger tip and pip (knuckle) landmarks
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]

    # Get corresponding pip (knuckle) positions
    index_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP]
    middle_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_PIP]

    # Check if middle finger is up and others are down
    middle_up = middle_tip.y < middle_pip.y
    index_down = index_tip.y > index_pip.y
    ring_down = ring_tip.y > ring_pip.y
    pinky_down = pinky_tip.y > pinky_pip.y

    return middle_up and index_down and ring_down and pinky_down

def main():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Variables for gesture detection
    gesture_detected = False
    gesture_start_time = None
    GESTURE_HOLD_TIME = 2.0  # Time in seconds to hold gesture before shutdown

    print("Starting gesture detection...")
    print("Show your middle finger for 2 seconds to shutdown the PC")
    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS
                )

                # Check for middle finger gesture
                if detect_middle_finger(hand_landmarks):
                    if not gesture_detected:
                        gesture_detected = True
                        gesture_start_time = time.time()
                    elif time.time() - gesture_start_time >= GESTURE_HOLD_TIME:
                        # Shutdown the PC
                        cv2.putText(frame, "Shutting down...", (50, 50),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow('Gesture Detection', frame)
                        cv2.waitKey(1000)  # Wait for 1 second to show the message
                        os.system("shutdown /s /t 1")  # Windows shutdown command
                        return
                else:
                    gesture_detected = False
                    gesture_start_time = None

        # Display countdown if gesture is being held
        if gesture_detected:
            remaining_time = GESTURE_HOLD_TIME - (time.time() - gesture_start_time)
            if remaining_time > 0:
                cv2.putText(frame, f"Hold for {remaining_time:.1f}s", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Gesture Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main() 