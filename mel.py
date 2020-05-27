import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math

# The original prototype random melody generator.
# Imports a .csv of note names and frequencies.
# Chooses a random frequency for NUM_NOTES from a range twelveTone and
# plays NUM_NOTES random notes, each of a length SECONDS.

# Global parameters:
SAMPLE_RATE = 24000
SECONDS = 1
NUM_NOTES = 100

# Select a set of NUM_NOTES random frequencies (chosen from the range 
# selected in twelveTone), calculate the sine waves for each, and play 
# each note:
def randMel():
  twelveTone = readCSV()
  twelveTone = twelveTone[30:54]
  notes = [random.choice(twelveTone) for i in range(NUM_NOTES)]
  audio = calcSine(notes)
  playSine(audio)

# Read in the list of 108 notes/frequencies (C0-B8):
def readCSV():
  df = pd.read_csv('freq_12tone.csv', delimiter=',')
  freq = [list(row) for row in df.values]
  return freq

# Calculate the sine wave for the frequency of the note passed in:
def calcSine(notes):
  # Number of samples for each note:
  NUM = SECONDS * SAMPLE_RATE
  x = np.linspace(0, SECONDS, int(NUM), False)
  audio = np.zeros(0)

  # Calculate and return a list of generated sine waves
  for freq in notes:
    y =  np.sin(x * freq * 2 * np.pi)
    sine = (y * (2**15 - 1)) / np.max(np.abs(y))
    audio = np.concatenate((audio, sine))
  audio = audio.astype(np.int16)
  return audio

# Play the sine wave passed in:
def playSine(audio):
  play = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
  play.wait_done();

randMel()

