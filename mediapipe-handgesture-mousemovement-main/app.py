import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# Cursor smoothing variables
prev_x, prev_y = 0, 0
smooth_factor = 0.3

# Function to calculate Euclidean distance
def distance(point1, point2):
    return math.hypot(point2.x - point1.x, point2.y - point1.y)

# Function to move cursor smoothly
def move_mouse(hand_landmarks, img_width, img_height):
    global prev_x, prev_y
    
    index_tip = hand_landmarks.landmark[8]
    x = int(index_tip.x * img_width)
    y = int(index_tip.y * img_height)
    
    # Convert to screen space
    screen_x = np.interp(x, [100, img_width - 100], [0, screen_width])
    screen_y = np.interp(y, [100, img_height - 100], [0, screen_height])
    
    # Apply smoothing
    smooth_x = prev_x + (screen_x - prev_x) * smooth_factor
    smooth_y = prev_y + (screen_y - prev_y) * smooth_factor
    prev_x, prev_y = smooth_x, smooth_y
    
    pyautogui.moveTo(smooth_x, smooth_y, duration=0.01)

# Function to handle clicking
def handle_mouse_clicks(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    
    if distance(thumb_tip, index_tip) < 0.02:
        pyautogui.click()
        time.sleep(0.2)

# Function for drag
def handle_mouse_drag(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    
    if distance(thumb_tip, index_tip) < 0.025:
        pyautogui.mouseDown()
    else:
        pyautogui.mouseUp()

# Function for scrolling
def handle_mouse_scroll(hand_landmarks):
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    
    scroll_distance = middle_tip.y - index_tip.y
    
    if scroll_distance > 0.05:
        pyautogui.scroll(5)
    elif scroll_distance < -0.05:
        pyautogui.scroll(-5)

# Webcam feed
cap = cv2.VideoCapture(0)
prev_time = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    height, width, _ = frame.shape

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            move_mouse(hand_landmarks, width, height)
            handle_mouse_clicks(hand_landmarks)
            handle_mouse_drag(hand_landmarks)
            handle_mouse_scroll(hand_landmarks)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
