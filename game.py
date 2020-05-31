#Damien Jones, Jesse Emerson
#©2020 PSU CS410P Music and Sound project
#Project is written in python3 and can be compiled and ran using the pythinn3 
#prefix followed by the file name. ex: 
#   python3 file_name.py

import time
import random



score = 0
round = 1
guesses = 0
award_points = 5

# Dummy container for saved sounds, to check compilation
playable = ["snd1.wav", "snd2.wav"] #NOT USED YET<-------------
# List to add sounds once played.
played = [] #NOT USED YET<-------------


# Game start
print ("Welcome to CS410P Sound, the game!!\n")
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
while user_selection not in ("1", "2", "3", "4", "q"):
        user_selection = input("Enter choice followed by the ENTER key:\n\n 1) ans1\n 2) ans2\n 3) ans3\n 4) ans4\n q) quit\nYour selection: ")
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





