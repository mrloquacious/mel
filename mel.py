import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math
import wavio

""" Effect1 starts with a base frequency (probably a low note) BASE,
which is a number corresponding to a table of 108 frequencies ranging 
from C0 (16.35 Hz) to B8 (7902.13 Hz).
Then, it creates an arpeggio (a major chord) of 3 notes, 1-3-5, repeated 
for NUM_NOTES. 
SECONDS is the time for NUM_NOTES to play. 
Then, it repeats this NUM_NOTES length arpeggio NUM_ARPEG times, 
increasing the base note by a half step each arpeggio. 
This effect is written to a .wav file.

An envelope eliminates the clicks that would occur during note changes, 
and a clamp is intended to eliminate clipping, though this is still a
work in progress.

"""

MAX_AMPLITUDE = 1
SAMPLE_RATE = 12000
SECONDS = .25
NUM_NOTES = 20
NUM_SAMPLES = SAMPLE_RATE * SECONDS
NOTE_LEN = int(NUM_SAMPLES // NUM_NOTES)

BASE = 12
NUM_ARPEG = 8

ATTACK_TIME = .001
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .001
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)

# Create a dataframe from csv
df = pd.read_csv('frequencies_12tone.csv', delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
twelveTone = [list(row) for row in df.values]

# Build a single major arpeggio NUM_NOTES long:
def oneArpeg(start):
    notes = [twelveTone[start][1]]
    for i in range(0, NUM_NOTES - 1, 3):
        notes.append(notes[i] * 2**(1/3))
        notes.append(notes[i] * 2**(7/12))
        notes.append(notes[i] * 2)
    return notes
 
# Build num arpeggios, each arpeggio starting a half step up from the prev:
def manyArpeg(base, num):
    notes = list()
    for i in range(0, num):
        notes.append(oneArpeg(base + i))
    return notes
       
# Envelope to eliminate clicks that occur when changing notes:
def envelope():
    att_env = np.linspace(0, 1, ATTACK, False)
    ones = np.ones(NOTE_LEN - ATTACK - RELEASE)
    rel_env = np.linspace(1, 0, RELEASE, False)
    env = np.append(att_env, ones)
    env = np.append(env, rel_env)
    return env

# Play a single sine wave note:
def playSine(audio):
    play = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    play.wait_done();

# Keep values within 16 bit range:
def clamp(n):
    return min(max(n, -(2**16 - 1)), (2**16 - 1)) 

# Calculate and return a list of lists (ascending arpeggios):
def calcSine(notes):
    x = np.linspace(0, SECONDS / NUM_NOTES, int(NOTE_LEN), False)
    audioAll = np.zeros(0)
    for arpeg in notes:
        for freq in arpeg:
            y =  np.sin(MAX_AMPLITUDE * x * freq * 2 * np.pi)
            audio = (envelope() * y * (2**15 - 1) / np.max(np.abs(y)))
            audioAll = np.concatenate((audioAll, audio))
    audioAll = audioAll.astype(np.int16)

    # Attempt to eliminate audio clipping: TODO
    #audioAllClamped = np.zeros(0)
    #for a in audioAll:
    #    audioAllClamped = np.concatenate((audioAllClamped, clamp(a)))
        
    #playSine(audioAll)
    return audioAll

notes = manyArpeg(BASE, NUM_ARPEG)
audioAll = calcSine(notes)
wavio.write("test.wav", audioAll, SAMPLE_RATE, sampwidth=2, scale="none")

