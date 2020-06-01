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


score = 0
round = 1
guesses = 0
award_points = 5
correct_answer = "amy"

# Getting a random selection from possible_answers to fill multiple choice options
possible_answers = ["amy","bob","cat","dan","elm","fig","gin","ham","ink","jam"]
temp_list = possible_answers.copy()
answers_used = []
correct_answer = ["amy"]
choices = []
COUNT = 1

# Game start

print ("Welcome to CS410P Sound, the game!!\n")

# PLAY THEME MUSIC <-----------

name = input("Please enter your name:\n")
print("Welcome, " + name, "Lets get started...\n")

# PAUSE 1 sec
time.sleep(1)

print("Round " + str(round), "   Score- " + str(score))  
print("\n")


#Play random sound here
print("Playing interval...")
time.sleep(0.5)

#Remove interval playable list OR add to a played list.

def increment():
    global COUNT
    COUNT += 1

def count_reset():
    global COUNT
    COUNT = 1


def fill_choices():
    random_choice = random.choice(possible_answers)
    while COUNT < 5:
        if len(choices) == len(possible_answers):
            break
        if random_choice in answers_used:
            fill_choices()
        else:
            answers_used.append(random_choice)
            choices.append(random_choice)
            #print("Choice " + str(COUNT), " = " + str(choices))
            increment()
            break



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
        print("\n 1) " + str(choices[0]), "\n 2) " + str(choices[1]), "\n 3) " + str(choices[2]), "\n 4) " + str(choices[3]), "\n q) QUIT\n")
        user_selection = input("Enter choice followed by the ENTER key:\n")
        if user_selection == "1":
            print("selection 1") # CHOICE 1
        elif user_selection == "2":
            print("selection 2") # CHOICE 2 
        elif user_selection == "3":
            print("selection 3") # CHOICE 3
        elif user_selection == "4":
            print("selection 4") # CHOICE 4
        elif user_selection == "q":
            print("Thank you for playing, goodbye...") # QUIT
            # PAUSE 1 sec
            time.sleep(1)
            break
        else:
            print("Invalid input, please try again")





