import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math

def randMel():

    SECONDS = 1
    FREQ_MIN = 100
    FREQ_MAX = 1000
    NUM_NOTES = 100
    
    #notes = [i for i in np.linspace(FREQ_MIN, FREQ_MAX, NUM_NOTES - 1)] 
    #notes = [random.randint(FREQ_MIN, FREQ_MAX) for i in range(NUM_NOTES)]
    #random.randint(FREQ_MIN, FREQ_MAX)
    
    twelveTone = readCSV()
    twelveTone = twelveTone[30:54]
    notes = [random.choice(twelveTone) for i in range(NUM_NOTES)]
    
    calcSine(notes, SECONDS)

def readCSV():

    # Create a dataframe from csv
    df = pd.read_csv('freq_12tone.csv', delimiter=',')

    # User list comprehension to create a list of lists from Dataframe rows
    freq = [list(row) for row in df.values]

    # Print list of lists i.e. rows
    #print(freq)

    return freq


def calcSine(notes, SECONDS):
    SAMPLE_RATE = 24000
    NUM = math.trunc( SECONDS * SAMPLE_RATE)

    for freq in notes:
        x = np.linspace(0, SECONDS, NUM, False)
        y =  np.sin(x * freq * 2 * np.pi)
        audio = y * (2**15 - 1) / np.max(np.abs(y))
        audio = audio.astype(np.int16)
        playSine(audio)

def playSine(audio):
    # Example of simpleaudio.play_buffer:
    # simpleaudio.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    
    play = sa.play_buffer(audio, 1, 2, 24000)
    play.wait_done();


randMel()

