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

ATTACK_TIME = .001
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .001
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)

# Create a dataframe from csv
df = pd.read_csv('frequencies_12tone.csv', delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
twelveTone = [list(row) for row in df.values]

notes = list()
notes = [twelveTone[16][1]]

for i in range(0, NUM_NOTES - 1, 3):
    notes.append(notes[i] * 2**(1/3))
    notes.append(notes[i] * 2**(7/12))
    notes.append(notes[i] * 2)
        
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

def calcSine(notes, SECONDS):
    x = np.linspace(0, SECONDS / NUM_NOTES, int(NOTE_LEN), False)
    audio = np.zeros(1)
    for freq in notes:
        y =  np.sin(MAX_AMPLITUDE * x * freq * 2 * np.pi)
        audio2 = (envelope() * y * (2**15 - 1) / np.max(np.abs(y)))
        #audio2 = audio
        audio = np.concatenate((audio, audio2))
        audio = audio.astype(np.int16)
        playSine(audio)
        wavio.write("test.wav", audio, SAMPLE_RATE, sampwidth=2, scale="none")

calcSine(notes, SECONDS)

