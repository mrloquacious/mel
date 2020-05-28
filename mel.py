import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math

# Interval is the most relevant branch to the CS410 Course Project.
# Right now it continuously plays an interval (two frequencies played 
# together) and prints the note names. It does this NUM_NOTES times for
# time length of SECONDS each interval. We'll have to modify, depending on
# how the game works, but this will be a good starting place. We could 
# also do a similar thing with chords.

# Global constants:
SAMPLE_RATE = 24000
SECONDS = 2
NUM_NOTES = 20

# Envelope settings:
ATTACK_TIME = .01
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .5
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)

# Import a .csv of notes/frequencies and create 2 lists of NUM_NOTES 
# frequencies:
df = pd.read_csv('frequencies_12tone.csv', delimiter=',')
twelveTone = [list(row) for row in df.values]
twelveTone = twelveTone[48:61]
notes1 = [random.choice(twelveTone) for i in range(NUM_NOTES)]
notes2 = [random.choice(twelveTone) for j in range(NUM_NOTES)]

# An envelope to prevent clicks when changing notes:
def envelope(NUM_SAMPLES):
    NUM_SAMPLES = math.trunc(SECONDS * SAMPLE_RATE)
    att_env = np.linspace(0, 1, ATTACK, False)
    ones = np.ones(NUM_SAMPLES - ATTACK - RELEASE)
    rel_env = np.linspace(1, 0, RELEASE, False)
    env = np.append(att_env, ones)
    env = np.append(env, rel_env)
    return env

# Calculate a single sine wave:
def calcSine(freq, SECONDS, NUM_SAMPLES):
    x = np.linspace(0, SECONDS, NUM_SAMPLES, False)
    y =  np.sin(x * freq * 2 * np.pi)
    return y

# Add 2 sine waves to form an interval:
def sumSines(freq1, freq2, SECONDS):
    NUM_SAMPLES = math.trunc(SECONDS * SAMPLE_RATE)
    y = calcSine(freq1, SECONDS, NUM_SAMPLES) + 
        calcSine(freq2, SECONDS, NUM_SAMPLES)
    audio = envelope(NUM_SAMPLES) * y * (2**15 - 1) / np.max(np.abs(y))
    audio = audio.astype(np.int16)
    return audio

# Play a note or interval or whatever:
def playSine(audio):
    play = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    play.wait_done()

# Cycle through the lists and play intervals:
for n1, n2 in zip(notes1, notes2):
    playSine(sumSines(n1[1], n2[1], SECONDS))
    print(n1[0] + "-" + n2[0])

