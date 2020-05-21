import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math

SAMPLE_RATE = 24000

SECONDS = 2
FREQ_MIN = 100
FREQ_MAX = 1000
NUM_NOTES = 20

ATTACK_TIME = .01
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .5
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)

currentNotes = set()

# Create a dataframe from csv
df = pd.read_csv('freq_12tone.csv', delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
twelveTone = [list(row) for row in df.values]

twelveTone = twelveTone[42:54]
notes1 = [random.choice(twelveTone) for i in range(NUM_NOTES)]
notes2 = [random.choice(twelveTone) for j in range(NUM_NOTES)]

def envelope(NUM_SAMPLES):
    NUM_SAMPLES = math.trunc(SECONDS * SAMPLE_RATE)

    att_env = np.linspace(0, 1, ATTACK, False)
    ones = np.ones(NUM_SAMPLES - ATTACK - RELEASE)
    rel_env = np.linspace(1, 0, RELEASE, False)
    env = np.append(att_env, ones)
    env = np.append(env, rel_env)

    return env

def calcSine(freq, SECONDS, NUM_SAMPLES):

    x = np.linspace(0, SECONDS, NUM_SAMPLES, False)
    y =  np.sin(x * freq * 2 * np.pi)

    return y

def sumSines(freq1, freq2, SECONDS):

    NUM_SAMPLES = math.trunc(SECONDS * SAMPLE_RATE)

    y = calcSine(freq1, SECONDS, NUM_SAMPLES) + calcSine(freq2, SECONDS, NUM_SAMPLES)
    audio = envelope(NUM_SAMPLES) * y * (2**15 - 1) / np.max(np.abs(y))
    audio = audio.astype(np.int16)

    return audio

def playSine(audio):
    # EXAMPLE: simpleaudio.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    
    play = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    play.wait_done()

for n1, n2 in zip(notes1, notes2):
    playSine(sumSines(n1, n2, SECONDS))
    print(n1)
    print(n2)

