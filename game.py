#Damien Jones, Jesse Emerson
#©2020 PSU CS410P Music and Sound project
#Project is written in python3 and can be compiled and ran using the python3 
#prefix followed by the file name. ex: 
#   python3 file_name.py

import time
import random

# Dummy container for saved sounds, to check compilation
playable = ["snd1.wav", "snd2.wav"] #NOT USED YET<-------------
# List to add sounds once played.
played = [] #NOT USED YET<-------------
#Remove interval playable list OR add to a played list.


SCORE = 0
round = 1
GUESSES = 0
AWARD_POINTS = 5
COUNT = 1

# DEFINE CORRECT ANSWER HERE
correct_answer = "amy"

# Getting a random selection from possible_answers to fill multiple choice options
possible_answers = ["amy","bob","cat","dan","elm","fig","gin","ham","ink","jam"]
answers_used = []
choices = []
choices.append(correct_answer)
possible_answers.remove(correct_answer)

temp_list = possible_answers.copy() #NOT USED <---------------


def increment_COUNT():
    global COUNT
    COUNT += 1

def count_reset():
    global COUNT
    COUNT = 1

def increment_SCORE():
    global SCORE
    SCORE += AWARD_POINTS

def reset_SCORE():
    global SCORE
    SCORE = 0

def increment_GUESSES():
    global GUESSES
    GUESSES += 1

def increment_round():
    global round
    round += 1

def decrement_round():
    global round
    round -= 1


def fill_choices():
    random_choice = random.choice(possible_answers)

    while COUNT < 4:
        #if random_choice == correct_answer:
            #fill_choices()
        #if len(choices) == len(possible_answers):
            #break
        if random_choice in answers_used:
            fill_choices()
        else:
            answers_used.append(random_choice)
            choices.append(random_choice)
            #print("Choice " + str(COUNT), " = " + str(choices))
            increment_COUNT()
            break


# -------------------------->Game start<-------------------------------------#

print ("Welcome to CS410P Sound, the game!!\n")

# PLAY THEME MUSIC <-----------

name = input("Please enter your name:")
print("\n   Welcome, " + name, "Lets get started...\n")

# PAUSE 1 sec
time.sleep(1)

while round < 3:

    
    print("Beginning round " + str(round), "...\n")
    print("   -------------       ---------------")
    print("   |  Round " + str(round), " |       |  Score - " + str(SCORE), " |")  
    print("   -------------       ---------------")
    print("\n")

    time.sleep(1)
    #Play random sound here
    print("Playing interval...\n")
    time.sleep(0.5)


    # REPLAY INTERVAL loop. Will continue to ask until y,n,q is pressed
    replay_interval = None
    while replay_interval not in ("y","n","q"):
        replay_interval = input("Would you like to hear the interval again? (y/n)\n")
        if replay_interval == "y":
            print("Replaying interval...\n")
            time.sleep(1)
        elif replay_interval == "n":
            break
        else: 
            print("Invalid input, please try again...\n")

    # USER CHOICE SELECTION loop.

    user_selection = None

    for a in range(0,4):
        fill_choices()


    while user_selection not in ("1", "2", "3", "4", "q"):
        random.shuffle(choices)
        
        print("\n 1) " + str(choices[0]), "\n 2) " + str(choices[1]), "\n 3) " + str(choices[2]), "\n 4) " + str(choices[3]), "\n q) QUIT\n")
        
        user_selection = input("Enter choice followed by the ENTER key:")
        print("\n")

        if user_selection == "1":
        #print("choices " + str(choices[0]), "  correct answer " + str(correct_answer[0]), "\n")
            if choices[0] == correct_answer:
                print("CORRECT ANSWER, YOU WIN " + str(AWARD_POINTS), " POINTS!")
                increment_SCORE()
            else:
                print("selection 1 is incorrect") # CHOICE 1
                time.sleep(1)

        elif user_selection == "2":
            #print("choices " + str(choices[1]), "  correct answer " + str(correct_answer[0]), "\n")
            if choices[1] == correct_answer:
                print("CORRECT ANSWER, YOU WIN " + str(AWARD_POINTS), " POINTS!")
                increment_SCORE()
            else:
                print("selection 2 is incorrect") # CHOICE 2
                time.sleep(1)

        elif user_selection == "3":
            #print("choices " + str(choices[2]), "  correct answer " + str(correct_answer[0]), "\n")
            if choices[2] == correct_answer:
                print("CORRECT ANSWER, YOU WIN " + str(AWARD_POINTS), " POINTS!")
                increment_SCORE()
            else:
                print("selection 3 is incorrect") # CHOICE 3
                time.sleep(1)

        elif user_selection == "4":
            #print("choices " + str(choices[3]), "  correct answer " + str(correct_answer[0]), "\n")
            if choices[3] == correct_answer:
                print("CORRECT ANSWER, YOU WIN " + str(AWARD_POINTS), " POINTS!")
                increment_SCORE()
            else:
                print("selection 4 is incorrect") # CHOICE 4
                time.sleep(1)

        elif user_selection == "q":
            print("Thank you for playing, goodbye...") # QUIT
            # PAUSE 1 sec
            time.sleep(1)
            break
        else:
            print("Invalid input, please try again")

    print("\n\n")
    increment_round()

decrement_round()
print("Your final score is " + str(SCORE), ", after " + str(round), " rounds!")
if SCORE > 5:
    print("      GREAT JOB!!!!")
elif SCORE > 10:
    print("      EXCELLENT JOB!!!!!!!!")
time.sleep(1)
print("\nThank you for playing, goodbye...\n") # QUIT
# PAUSE 1 sec
time.sleep(1)


