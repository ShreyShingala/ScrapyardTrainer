import cv2
import math 
import numpy as np 
import mediapipe as mp
import random 
import time
import serial as ps


ser = ps.Serial('/dev/tty.usbmodem142401', 115200)  # Ensure this is the correct port for pico
#ser1 = ps.Serial('/dev/tty.usbmodem142301', 9600) # Ensure this is the correct port for the arduino

running = False

randgesture = random.randint(0,2)
gesture_name = ""

start_time = time.time()
display_time = 5

if randgesture == 0: 
    gesture_name = "THUMB'S UP"
elif randgesture == 1: 
    gesture_name = "L"
elif randgesture == 2:  
    gesture_name = "W"

mp_drawing = mp.solutions.drawing_utils 
mp_hands = mp.solutions.hands 
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
frame_width =  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
boxh = int(frame_height/5)
boxw = int(frame_width/5)

def safe():
    print("yes")
    return True 

def check(gesture, finger_x, finger_y):
    if gesture == 0: 
        #Thumb's Up
        if finger_y[0] < finger_y[1] and finger_y[0] < finger_y[2]:
            return safe()
    if gesture == 1: 
        # L
        if finger_y[1] < np.mean([finger_y[2], finger_y[3], finger_y[4]]) <= finger_y[0] and max(finger_x) == finger_x[0]: 
            return safe()
    if gesture == 2: 
        # W 
        if finger_x[1] < finger_x[3] < finger_x[2] < finger_x[4]:
            return safe()
    if gesture == 3: 
        if finger_y[0] > finger_y[1] < finger_y[2] < finger_y[3]:
            return safe()
           
def KILL():
    print("bye bye")
    if not ser.is_open:
        ser.open()
    ser.write(b'e')
    print("bye bye AGAIN") 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.flip(frame, 1)

    cv2.rectangle(frame, (boxw, boxh), (boxw*4, boxh*4), (0, 255, 0), 0)
    crop_img = frame[boxw:boxw*4, boxh:boxw*4]

    image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.putText(frame, "Make a " + gesture_name, (int(frame_width/5), 50), cv2.FONT_HERSHEY_COMPLEX, 1 , (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            finger_x = [thumb_tip.x, index_tip.x, middle_tip.x, ring_tip.x, pinky_tip.x]
            finger_y = [thumb_tip.y, index_tip.y, middle_tip.y, ring_tip.y, pinky_tip.y]
            
            if(check(randgesture, finger_x, finger_y)):
                cap.release()
                cv2.destroyAllWindows()

    cv2.imshow("MAKE A " + gesture_name, frame)
    if time.time() - start_time > display_time:
        print("ada")
        KILL()
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()