import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math

SAMPLE_RATE = 24000

SECONDS = .25
FREQ_MIN = 100
FREQ_MAX = 1000
NUM_NOTES = 100

ATTACK_TIME = .01
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .01
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)

currentNotes = set()

# Create a dataframe from csv
df = pd.read_csv('freq_12tone.csv', delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
twelveTone = [list(row) for row in df.values]

twelveTone = twelveTone[30:54]
notes = [random.choice(twelveTone) for i in range(NUM_NOTES)]

#durations = [2**0, 2**-1, 2**-2, 2**-3, 2**-4, 2**-5]
durations = [2**-1, 2**-2, 2**-3, 2**-4, 2**-5]
seconds = [random.choice(durations) for i in range(NUM_NOTES)]

def calcSine(notes, seconds):
    # If using fixed time value for notes:
    #NUM_SAMPLES = math.trunc(SECONDS * SAMPLE_RATE)
    #seconds = SECONDS

    for freq in notes:
        # .02 to keep us in the + (compensate for attack/release):
        seconds = min(max(.02, random.random()), .25);
        NUM_SAMPLES = math.trunc(seconds * SAMPLE_RATE)

        x = np.linspace(0, seconds, NUM_SAMPLES, False)
        y =  np.sin(x * freq * 2 * np.pi)
        # Add the attack envelope:
        att_env = np.linspace(0, 1, ATTACK, False)
        ones = np.ones(NUM_SAMPLES - ATTACK - RELEASE)
        rel_env = np.linspace(1, 0, RELEASE, False)
        att_env = np.append(att_env, ones)
        att_env = np.append(att_env, rel_env)

        audio = att_env * y * (2**15 - 1) / np.max(np.abs(y))
        audio = audio.astype(np.int16)
        playSine(audio)

    return 0

def playSine(audio):
    # Example of simpleaudio.play_buffer:
    # simpleaudio.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    
    play = sa.play_buffer(audio, 1, 2, 24000)
    play.wait_done();

calcSine(notes, SECONDS)

