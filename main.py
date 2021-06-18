#!/usr/bin/env python3

from cv2 import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

tips = {"thumb": 4,
        "index": 8,
        "middle": 12,
        "ring": 16,
        "little": 20}

def is_open(res, finger):
    if tips[finger] == 4:
        return res[tips[finger]][1] < res[tips[finger] - 1][1]
    return res[tips[finger]][2] < res[tips[finger] - 2][2]


with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        res = []
        if results.multi_hand_landmarks:
            right_hand = results.multi_hand_landmarks[0]
            for i, lm in enumerate(right_hand.landmark):
                res.append((i, int(lm.x * image.shape[0]), int(lm.y * image.shape[1])))
            """
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            """

            fingers_open = [is_open(res, finger) for finger in tips]
            if fingers_open[3] or fingers_open[4]:
                print("Paper")
            elif fingers_open[1] and fingers_open[2]:
                if fingers_open[3] or fingers_open[4]:
                    print("Paper")
                else:
                    print("Scissors")
            else:
                print("Rock")

            #print(fingers_open)
        
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break


cap.release()