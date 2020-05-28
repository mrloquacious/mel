import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math

# Rough attempt to introduce rhythm into the random melody generator.
# It's not a pleasing sound, but I'll leave it here for now.
# Also, there's a first attempt at an envelope.

SAMPLE_RATE = 24000

SECONDS = .25
FREQ_MIN = 100
FREQ_MAX = 1000
NUM_NOTES = 100

ATTACK_TIME = .01
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .01
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)

# Read in the .csv of notes/frequencies and choose a range:
df = pd.read_csv('freq_12tone.csv', delimiter=',')
twelveTone = [list(row) for row in df.values]
twelveTone = twelveTone[30:54]
notes = [random.choice(twelveTone) for i in range(NUM_NOTES)]

# Durations to randomly choose from for note lengths:
durations = [2**-1, 2**-2, 2**-3, 2**-4, 2**-5]
seconds = [random.choice(durations) for i in range(NUM_NOTES)]

def calcSine(notes, seconds):
    # If using fixed time value for notes:
    #NUM_SAMPLES = trunc(SECONDS * SAMPLE_RATE)
    #seconds = SECONDS

    for freq in notes:
        # .02 to keep us in the + (compensate for attack/release):
        seconds = min(max(.02, random.random()), .25);
        NUM_SAMPLES = math.trunc(seconds * SAMPLE_RATE)

        # Calculate the sine wave:
        x = np.linspace(0, seconds, NUM_SAMPLES, False)
        y =  np.sin(x * freq * 2 * np.pi)

        # Calulate the envelope:
        att_env = np.linspace(0, 1, ATTACK, False)
        ones = np.ones(NUM_SAMPLES - ATTACK - RELEASE)
        rel_env = np.linspace(1, 0, RELEASE, False)
        env = np.append(att_env, ones)
        env = np.append(env, rel_env)

        # Calculate and play sine wave with envelope:
        audio = env * y * (2**15 - 1) / np.max(np.abs(y))
        audio = audio.astype(np.int16)
        playSine(audio)
    return 0

def playSine(audio):
    play = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
    play.wait_done();

calcSine(notes, SECONDS)

