import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math
import pyaudio

import wave
import time
import sys

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

def calcSine(notes, SECONDS):
    #SAMPLE_RATE = 24000
    NUM_SAMPLES = math.trunc(SECONDS * SAMPLE_RATE)

    for freq in notes:
        x = np.linspace(0, SECONDS, NUM_SAMPLES, False)
        y =  np.sin(x * freq * 2 * np.pi)
        # Add the attack envelope:
        att_env = np.linspace(0, 1, ATTACK, False)
        ones = np.ones(NUM_SAMPLES - ATTACK - RELEASE)
        rel_env = np.linspace(1, 0, RELEASE, False)
        att_env = np.append(att_env, ones)
        att_env = np.append(att_env, rel_env)

        audio = att_env * y * (2**15 - 1) / np.max(np.abs(y))
        audio = audio.astype(np.int16)
##### SIMPLEAUDIO PLAY #####
        playSine(audio)
##### END SIMPLEAUDIO PLAY #####

    return 0

def playSine(audio):
    # Example of simpleaudio.play_buffer:
    # simpleaudio.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    
    play = sa.play_buffer(audio, 1, 2, 24000)
    play.wait_done();

### TEST ###
calcSine(notes, SECONDS)
### END TEST ###

#def callback(in_data, frame_count, time_info, status):
#    #data = wf.readframes(frame_count)
#    data = calcSine(notes, SECONDS)
#
#    return (data, pyaudio.paContinue)
#
#
###### PYAUDIO #####
## Create an interface to PortAudio
#pa = pyaudio.PyAudio()
#
## Set up the audio output stream.
## 'output = True' indicates that the sound will be played rather than recorded
#stream = pa.open(
#    format = pa.get_format_from_width(2),
#    channels = 1,
#    rate = SAMPLE_RATE,
#    output = True,
#    stream_callback = callback)
#
#stream.start_stream()
#
#while stream.is_active():
#    time.sleep(0.1)
#
## Done, clean up and exit.
#stream.stop_stream()
#stream.close()
#
## close PyAudio (7)
##pa.terminate()
