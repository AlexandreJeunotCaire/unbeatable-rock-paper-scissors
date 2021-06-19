#!/usr/bin/env python3

from cv2 import cv2
from collections import deque
import mediapipe as mp
from time import time

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
    ongoing = True
    time_to_decide = True
    last_played = None
    last_played_name = None
    true_answer = None
    true_answer_name = None
    x_offest = 500
    x_offest_user = 0
    y_offset = 350
    user_score = 0
    bot_score = 0
    while cap.isOpened():
        _, image = cap.read()
   
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        res = []
        if ongoing and results.multi_hand_landmarks:
            right_hand = results.multi_hand_landmarks[0]
            for i, lm in enumerate(right_hand.landmark):
                res.append((i, int(lm.x * image.shape[0]), int(lm.y * image.shape[1])))


            fingers_open = [res[4][1] < res[3][1],
                            res[8][2] < res[6][2],
                            res[12][2] < res[10][2],
                            res[16][2] < res[14][2],
                            res[20][2] < res[18][2]
                            ]
            candidate = ROCK
            if fingers_open[3] or fingers_open[4]:
                candidate = PAPER
            elif fingers_open[1] and fingers_open[2]:
                candidate = SCISSORS

            history.append(candidate)

            if time_to_decide and len(history) >= 3:
                res = None
                if history.count(ROCK) == 3:
                    res = ROCK
                elif history.count(PAPER) == 3:
                    res = PAPER
                elif history.count(SCISSORS) == 3:
                    res = SCISSORS
                
                    
                if res is not None:
                    last_played_name = WINS[res]
                    if res == ROCK:
                        last_played = paper_img
                    elif res == PAPER:
                        last_played = scissors_img
                    else:
                        last_played = rock_img
                    time_to_decide = False
            else:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                if len(history) == 5:
                    res = None
                    if history.count(ROCK) == 5:
                        res = ROCK
                    elif history.count(PAPER) == 5:
                        res = PAPER
                    elif history.count(SCISSORS) == 5:
                        res = SCISSORS
                    history.popleft()
                    if res is not None:
                        true_answer_name = res
                        if res == ROCK:
                            true_answer = rock_img
                        elif res == PAPER:
                            true_answer = paper_img
                        else: 
                            true_answer = scissors_img
                        ongoing = False
                    
            if last_played is not None:
                image[y_offset:y_offset+last_played.shape[0], x_offest:x_offest+last_played.shape[1]] = last_played

        
        if last_played is not None:
            image[y_offset:y_offset+last_played.shape[0], x_offest:x_offest+last_played.shape[1]] = last_played

        if true_answer is not None:
            cv2.putText(image, "Round over", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
            cv2.putText(image, "Press \"[SPACE]\" to continue", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            image[y_offset:y_offset+true_answer.shape[0], x_offest_user:x_offest_user+true_answer.shape[1]] = true_answer


        cv2.putText(image, f"You: {user_score}", (x_offest_user, y_offset - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(image, f"Bot: {bot_score}", (x_offest, y_offset - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Rock paper scissors', image)
        if cv2.waitKey(5) & 0xFF == 32:
            if not ongoing:
                if true_answer_name == WINS[last_played_name]:
                    user_score += 1
                elif last_played_name == WINS[true_answer_name]:
                    bot_score += 1
            time_to_decide = True
            ongoing = True
            last_played = None
            last_played_name = None
            true_answer = None_name = None
            history = deque()


cap.release()