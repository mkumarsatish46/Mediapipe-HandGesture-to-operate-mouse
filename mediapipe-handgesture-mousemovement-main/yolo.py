import streamlit as st
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.85, min_tracking_confidence=0.85)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0
smooth_factor = 0.3 

dragging = False  

def distance(point1, point2):
    return math.hypot(point2.x - point1.x, point2.y - point1.y)

def move_mouse(hand_landmarks, img_width, img_height):
    global prev_x, prev_y
    index_tip = hand_landmarks.landmark[8]
    x, y = int(index_tip.x * img_width), int(index_tip.y * img_height)
    
    screen_x = np.interp(x, [50, img_width - 50], [0, screen_width])
    screen_y = np.interp(y, [50, img_height - 50], [0, screen_height])
    
    smooth_x = prev_x + (screen_x - prev_x) * smooth_factor
    smooth_y = prev_y + (screen_y - prev_y) * smooth_factor
    prev_x, prev_y = smooth_x, smooth_y
    
    pyautogui.moveTo(smooth_x, smooth_y, duration=0.01)

def is_hand_closed(hand_landmarks):
    index_tip, thumb_tip = hand_landmarks.landmark[8], hand_landmarks.landmark[4]
    return distance(index_tip, thumb_tip) < 0.05

def scroll_up(hand_landmarks, is_right_hand):
    if is_right_hand:
        return hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    return False

def scroll_down(hand_landmarks, is_left_hand):
    if is_left_hand:
        return hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    return False

def handle_mouse_actions(hand_landmarks, is_right_hand, is_left_hand):
    global dragging
    if is_hand_closed(hand_landmarks):
        if not dragging:
            pyautogui.mouseDown()
            dragging = True
    else:
        if dragging:
            pyautogui.mouseUp()
            dragging = False

    if scroll_up(hand_landmarks, is_right_hand):
        pyautogui.scroll(10)
    elif scroll_down(hand_landmarks, is_left_hand):
        pyautogui.scroll(-10)

def main():
    st.title("Hand Gesture Mouse Control ✋🖱️")
    run = st.checkbox("Run Webcam")
    FRAME_WINDOW = st.image([])

    cap = None
    if run:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 60)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        while cap.isOpened() and run:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture video")
                break

            frame = cv2.flip(frame, 1)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            height, width, _ = frame.shape

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    handedness = "Right" if hand_landmarks.landmark[0].x > 0.5 else "Left"
                    is_right_hand = handedness == "Right"
                    is_left_hand = handedness == "Left"

                    move_mouse(hand_landmarks, width, height)
                    handle_mouse_actions(hand_landmarks, is_right_hand, is_left_hand)
                    
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS, 
                                           mp_draw.DrawingSpec(color=(0,255,0), thickness=3, circle_radius=6),
                                           mp_draw.DrawingSpec(color=(255,0,0), thickness=2))
                    
                    x_min = min([lm.x for lm in hand_landmarks.landmark]) * width
                    y_min = min([lm.y for lm in hand_landmarks.landmark]) * height
                    x_max = max([lm.x for lm in hand_landmarks.landmark]) * width
                    y_max = max([lm.y for lm in hand_landmarks.landmark]) * height
                    cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 255), 2)

                    cv2.putText(frame, f"{handedness} Hand", (int(x_min), int(y_min)-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            FRAME_WINDOW.image(frame, channels="BGR", use_container_width=True)
    else:
        st.write("Click the checkbox to start.")
    
    if cap:
        cap.release()

if __name__ == '__main__':
    main()