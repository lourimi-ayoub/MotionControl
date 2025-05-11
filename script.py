import cv2
import mediapipe as mp
import pyautogui
import time

# ==== Settings ==== 
DEBUG = True
MAX_NUM_HANDS = 1
DETECTION_CONFIDENCE = 0.7
HISTORY_LENGTH = 5
GESTURE_COOLDOWN = 0.8  # seconds
VOLUME_REPEAT_DELAY = 1.5  # seconds (for volume gestures)

# ==== MediaPipe Setup ==== 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=MAX_NUM_HANDS, min_detection_confidence=DETECTION_CONFIDENCE)
mp_draw = mp.solutions.drawing_utils

# ==== Gesture Definitions ==== 
GESTURE_ACTIONS = {
    "fist": "esc",
    "play/pause": "space",
    "forward": "right",
    "rewind": "left",
    "volume_up": "volumeup",
    "volume_down": "volumedown",
    "fullscreen": "f"
}

# ==== Gesture Detection and Action ==== 
def detect_gesture(landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x else 0)
    # Other fingers
    for i in range(1, 5):
        fingers.append(1 if landmarks[tips_ids[i]].y < landmarks[tips_ids[i] - 2].y else 0)

    if fingers == [0, 0, 0, 0, 0]:
        return "fist"
    elif fingers == [1, 1, 1, 1, 1]:
        return "play/pause"
    elif fingers == [0, 1, 0, 0, 0]:
        return "forward"
    elif fingers == [1, 0, 0, 0, 0]:
        return "rewind"
    elif fingers == [0, 1, 1, 0, 0]:
        return "volume_up"
    elif fingers == [0, 1, 1, 1, 1]:
        return "volume_down"
    elif fingers == [1, 1, 1, 0, 0]:
        return "fullscreen"
    return "unknown"

def perform_action(gesture):
    key = GESTURE_ACTIONS.get(gesture)
    if key:
        pyautogui.press(key)
        print(f"Performed: {gesture} → '{key}'")
    else:
        print(f"No action mapped for gesture: {gesture}")

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    gesture_history = []
    prev_gesture = None
    last_action_time = 0
    last_volume_up_time = 0
    last_volume_down_time = 0

    volume_repeat_state = {
        "volume_up": False,
        "volume_down": False
    }

    print("MotionControl started. Press 'Q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        current_gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                current_gesture = detect_gesture(hand_landmarks.landmark)

                gesture_history.append(current_gesture)
                if len(gesture_history) > HISTORY_LENGTH:
                    gesture_history.pop(0)

                if gesture_history.count(current_gesture) >= 4:
                    if current_gesture != prev_gesture and (time.time() - last_action_time) > GESTURE_COOLDOWN:
                        perform_action(current_gesture)
                        prev_gesture = current_gesture
                        last_action_time = time.time()

                    # Volume Up and Down Repeat Check
                    if current_gesture == "volume_up" and not volume_repeat_state["volume_up"]:
                        volume_repeat_state["volume_up"] = True
                        last_volume_up_time = time.time()
                        perform_action(current_gesture)
                    elif current_gesture == "volume_down" and not volume_repeat_state["volume_down"]:
                        volume_repeat_state["volume_down"] = True
                        last_volume_down_time = time.time()
                        perform_action(current_gesture)

                    # Wait and Check for Repeat Action
                    if volume_repeat_state["volume_up"] and (time.time() - last_volume_up_time) > VOLUME_REPEAT_DELAY:
                        volume_repeat_state["volume_up"] = False

                    if volume_repeat_state["volume_down"] and (time.time() - last_volume_down_time) > VOLUME_REPEAT_DELAY:
                        volume_repeat_state["volume_down"] = False

        if DEBUG:
            cv2.putText(frame, f'Gesture: {current_gesture}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("MotionControl", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Exited MotionControl.")

if __name__ == "__main__":
    main()
