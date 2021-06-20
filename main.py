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

rock_img = cv2.imread("img/rock.png")
paper_img = cv2.imread("img/paper.png")
scissors_img = cv2.imread("img/scissors.png")

history = deque()

with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
    
    # Game parameters
    ongoing = True # Is the round ongoing
    time_to_decide = True # 
    last_played = None # What the bot played
    last_played_name = None # Name of the movement the bot made
    true_answer = None # What the player actually did
    true_answer_name = None # Name of the movement the player did

    # Where to place the graphic elements

    x_offest = 500
    x_offest_user = 0
    y_offset = 350
    user_score = 0
    bot_score = 0

    while cap.isOpened():

        # Treating the image in order to recognize the hands
        _, image = cap.read()
   
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        res = []
        if ongoing and results.multi_hand_landmarks: # If the round is not over (and we detected hands)
            height, width, _ = image.shape
            right_hand = results.multi_hand_landmarks[0]

            # Position of all the joints in the hand
            for i, lm in enumerate(right_hand.landmark):
                res.append((i, lm.x * height, lm.y * width))


            fingers_open = [res[4][1] < res[3][1], #true if thumb is open
                            res[8][2] < res[6][2], #true if index is open
                            res[12][2] < res[10][2], #true if middle finger is open
                            res[16][2] < res[14][2], #true if ring finger is open
                            res[20][2] < res[18][2] #true if little finger is open
                            ]

            # Determine what the player most likely played
            candidate = ROCK
            if fingers_open[3] or fingers_open[4]:
                candidate = PAPER
            elif fingers_open[1] and fingers_open[2]:
                candidate = SCISSORS

            history.append(candidate)

            if time_to_decide and len(history) >= 3: # This is to be more accurate in our decision. In particular, people tend to hide their fist behind their head, and it influences the first frames
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

            elif not time_to_decide:
                # We draw the hand
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # We get what the player did with more accuracy
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
            
            # We show the image the AI """"guessed""""" ;p
            if last_played is not None:
                image[y_offset:y_offset+last_played.shape[0], x_offest:x_offest+last_played.shape[1]] = last_played

        
        if last_played is not None:
            image[y_offset:y_offset+last_played.shape[0], x_offest:x_offest+last_played.shape[1]] = last_played

        # Once we determined with accuracy the true movement, we show it too
        if true_answer is not None:
            cv2.putText(image, "Round over", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
            cv2.putText(image, "Press \"[SPACE]\" to continue", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            image[y_offset:y_offset+true_answer.shape[0], x_offest_user:x_offest_user+true_answer.shape[1]] = true_answer


        cv2.putText(image, f"You: {user_score}", (x_offest_user, y_offset - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(image, f"Bot: {bot_score}", (x_offest, y_offset - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Rock paper scissors', image)

        if cv2.waitKey(5) & 0xFF == 32: # 32 = space, 27 = esc if you want to change
            if not ongoing:
                if true_answer_name == WINS[last_played_name]:
                    user_score += 1
                elif last_played_name == WINS[true_answer_name]:
                    bot_score += 1
            
            # reset parameters
            time_to_decide = True
            ongoing = True
            last_played = None
            last_played_name = None
            true_answer = None
            true_answer_name = None
            history = deque()

        if cv2.waitKey(1) & 0xFF == ord("r"):
            user_score = 0
            bot_score = 0

        if cv2.waitKey(5) & 0xFF == 27:
            break


cap.release()