import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math

import wavio

MAX_AMPLITUDE = 1
SAMPLE_RATE = 12000
SECONDS = .25
NUM_NOTES = 20
NUM_SAMPLES = SAMPLE_RATE * SECONDS
NOTE_LEN = int(NUM_SAMPLES // NUM_NOTES)

# For lists of lists of notes:
BASE = 16
NUM_ARPEG = 12

ATTACK_TIME = .001
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .001
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)

# Create a dataframe from csv
df = pd.read_csv('frequencies_12tone.csv', delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
twelveTone = [list(row) for row in df.values]

def oneArpeg(start):
    notes = [twelveTone[start][1]]
    for i in range(0, NUM_NOTES - 1, 3):
        notes.append(notes[i] * 2**(1/3))
        notes.append(notes[i] * 2**(7/12))
        notes.append(notes[i] * 2)
    return notes
 
def manyArpeg(base, num):
    notes = list()
    for i in range(0, num):
        notes.append(oneArpeg(base + i))
    #print(oneArpeg(notes, base))
    return notes
       
def envelope():
    att_env = np.linspace(0, 1, ATTACK, False)
    ones = np.ones(NOTE_LEN - ATTACK - RELEASE)
    rel_env = np.linspace(1, 0, RELEASE, False)
    env = np.append(att_env, ones)
    env = np.append(env, rel_env)
    return env

def playSine(audio):
    play = sa.play_buffer(audio, 1, 2, 24000)
    play.wait_done();

def clamp(n):
    return min(max(n, -(2**16 - 1)), (2**16 - 1)) 

def calcSine(notes):
    x = np.linspace(0, SECONDS / NUM_NOTES, int(NOTE_LEN), False)
    audioAll = np.zeros(0)
    #for freq in notes[0]:
    for arpeg in notes:
        for freq in arpeg:
            y =  np.sin(MAX_AMPLITUDE * x * freq * 2 * np.pi)
            audio = (envelope() * y * (2**15 - 1) / np.max(np.abs(y)))
            audioAll = np.concatenate((audioAll, audio))
    audioAll = audioAll.astype(np.int16)

    #audioAllClamped = np.zeros(0)
    #for a in audioAll:
    #    audioAllClamped = np.concatenate((audioAllClamped, clamp(a)))
        
    playSine(audioAll)
    wavio.write("test.wav", audioAll, SAMPLE_RATE, sampwidth=2, scale="none")

#notes = oneArpeg(BASE)
#calcSine(notes)

notes = manyArpeg(BASE, NUM_ARPEG)
#print(notes)
calcSine(notes)

