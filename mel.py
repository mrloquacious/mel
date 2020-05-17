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

SECONDS = 1
FREQ_MIN = 100
FREQ_MAX = 1000
NUM_NOTES = 100

currentNotes = set()

#notes = [i for i in np.linspace(FREQ_MIN, FREQ_MAX, NUM_NOTES - 1)] 
notes = [random.randint(FREQ_MIN, FREQ_MAX) for i in range(NUM_NOTES)]
#random.randint(FREQ_MIN, FREQ_MAX)

# Create a dataframe from csv
twelveTone = pd.read_csv('freq_12tone.csv', delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
freq = [list(row) for row in twelveTone.values]


freq = freq[30:54]
notes = [random.choice(freq) for i in range(NUM_NOTES)]


# Print list of lists i.e. rows
#print(freq)

#return freq

def calcFreq():
    return 440 * 2**((key - 69) / 12)

def calcSine(notes, SECONDS):
    #SAMPLE_RATE = 24000
    NUM = math.trunc( SECONDS * SAMPLE_RATE)

    for freq in notes:
        x = np.linspace(0, SECONDS, NUM, False)
        y =  np.sin(x * freq * 2 * np.pi)
        audio = y * (2**15 - 1) / np.max(np.abs(y))
        audio = audio.astype(np.int16)
        #playSine(audio)
    return audio


def playSine(audio):
    # Example of simpleaudio.play_buffer:
    # simpleaudio.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    
    play = sa.play_buffer(audio, 1, 2, 24000)
    play.wait_done();

def callback(in_data, frame_count, time_info, status):
    #data = wf.readframes(frame_count)
    data = calcSine(notes, SECONDS)

    return (data, pyaudio.paContinue)

#randMel()


# Create an interface to PortAudio
pa = pyaudio.PyAudio()

# Set up the audio output stream.
# 'output = True' indicates that the sound will be played rather than recorded
stream = pa.open(
    format = pa.get_format_from_width(2),
    channels = 1,
    rate = SAMPLE_RATE,
    output = True,
    stream_callback = callback)


# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)


# Done, clean up and exit.
stream.stop_stream()
stream.close()

# close PyAudio (7)
#pa.terminate()
