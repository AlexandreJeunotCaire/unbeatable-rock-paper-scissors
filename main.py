#!/usr/bin/env python3

from cv2 import cv2
from collections import deque
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

WINS = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}

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

def show(name):
    return cv2.imread(name)

rock_img = cv2.imread("img/rock.png")
paper_img = cv2.imread("img/paper.png")
scissors_img = cv2.imread("img/scissors.png")

history = deque()

with mp_hands.Hands(
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75) as hands:
    round = True
    last_played = None
    x_offest = 0
    y_offset = 350
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
        if round and results.multi_hand_landmarks:
            right_hand = results.multi_hand_landmarks[0]
            for i, lm in enumerate(right_hand.landmark):
                res.append((i, int(lm.x * image.shape[0]), int(lm.y * image.shape[1])))
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_open = [is_open(res, finger) for finger in tips]

            candidate = ROCK
            if fingers_open[3] or fingers_open[4]:
                candidate = PAPER
            elif fingers_open[1] and fingers_open[2]:
                candidate = SCISSORS

            history.append(candidate)
            if len(history) >= 3:
                res = None
                if history.count(ROCK) == 3:
                    res = ROCK
                elif history.count(PAPER) == 3:
                    res = PAPER
                elif history.count(SCISSORS) == 3:
                    res = SCISSORS
                history.popleft()
                if res is not None:                
                    #img = show(WINS[res])
                    #cv2.imshow("Bot Answer", img)
                    #cv2.rectangle(image, (20,225), (170,425), (0,255,0),cv2.FILLED)
                    #cv2.putText(image, WINS[res], (250,400), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,0), 10)

                    if res == ROCK:
                        last_played = paper_img
                        image[y_offset:y_offset+paper_img.shape[0], x_offest:x_offest+paper_img.shape[1]] = paper_img
                    elif res == PAPER:
                        last_played = scissors_img
                        image[y_offset:y_offset+scissors_img.shape[0], x_offest:x_offest+scissors_img.shape[1]] = scissors_img
                    else:
                        last_played = rock_img
                        image[y_offset:y_offset+rock_img.shape[0], x_offest:x_offest+rock_img.shape[1]] = rock_img
                    round = False



        elif last_played is not None:
            image[y_offset:y_offset+last_played.shape[0], x_offest:x_offest+last_played.shape[1]] = last_played
        
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            round = True
            last_played = None
            #break


cap.release()