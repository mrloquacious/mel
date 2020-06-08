import numpy as np
import simpleaudio as sa
import random
import pandas as pd
import math
import wavio
import argparse
import datetime
from data import *

""" 
Effect1 starts with a base frequency (probably a low note) base,
which is a number corresponding to a table of 108 frequencies ranging 
from C0 (16.35 Hz) to B8 (7902.13 Hz).
Then, it creates an arpeggio (a major chord) of 3 notes, 1-3-5, repeated 
for num_notes. 
seconds is the time for num_notes to play. 
Then, it repeats this num_notes length arpeggio num_arpegs times, 
increasing the base note by a half step each arpeggio. 
This effect is written to a .wav file.

An envelope eliminates the clicks that would occur during note changes, 
and a clamp is intended to eliminate clipping, though this is still a
work in progress.
"""

##### GLOBAL CONSTANTS #####
MAX_AMPLITUDE = 1
SAMPLE_RATE = 48000

ATTACK_TIME = .001
ATTACK = int(ATTACK_TIME * SAMPLE_RATE)
RELEASE_TIME = .001
RELEASE = int(RELEASE_TIME * SAMPLE_RATE)
#####

ap = argparse.ArgumentParser()
ap.add_argument(
    "-s", "--seconds",
    help="Number of seconds (or fraction of a second) for each arpeggio.",
    type=float,
    default=.5,
)
ap.add_argument(
    "-b", "--base",
    help="Index of the base frequency for the first apreggio. Default is index 12 is C0 = 32.7Hz.",
    type=int,
    default=12,
)
ap.add_argument(
    "-nn", "--num_notes",
    help="Number of notes per arpeggio.",
    type=int,
    default=21,
)
ap.add_argument(
    "-na", "--num_arpegs",
    help="Number of arpeggios generated.",
    type=int,
    default=4,
)
ap.add_argument(
    "-u", "--up",
    help="Up=True is default. Use 0 for down.",
    type=int,
    default=1,
)
args = ap.parse_args()

seconds = args.seconds
base = args.base
num_notes = len(note_pattern) * 7
num_arpegs = len(arpegs_pattern)
notes_up = args.up
 
num_samples = SAMPLE_RATE * seconds
note_len = int(num_samples // num_notes)

# Create a dataframe from csv
df = pd.read_csv('frequencies_12tone.csv', delimiter=',')
# User list comprehension to create a list of lists from Dataframe rows
twelveTone = [list(row) for row in df.values]

# Build a single major arpeggio num_notes long:
def oneArpeg(seconds, base, num_notes, note_pattern, notes_up):
  base_note = twelveTone[base][1]
  notes = []
  for i in range(0, num_notes, len(note_pattern)):
    for j in range(0, len(note_pattern)):
      if notes_up == True:
        notes.append((base_note * 2**((i + len(note_pattern))/len(note_pattern))) * 2**(note_pattern[j]/12))
        #print(base_note * 2**((i + len(note_pattern))/len(note_pattern)) * 2**(note_pattern[j]/12))
      else:
        notes.append(base_note / 2**(i / len(note_pattern)) / 2**(note_pattern[j]/12))
        #print(base_note / 2**(i / len(note_pattern)) / 2**(note_pattern[j]/12))
  
  return notes

# Build num arpeggios, each arpeggio starting a half step up from the prev:
def manyArpeg(seconds, base, num_notes, note_pattern, num_arpegs, arpegs_pattern, notes_up=True):
  notes = list()
  for i in range(0, num_arpegs):
      notes.append(oneArpeg(seconds, base + arpegs_pattern[i], num_notes, note_pattern, notes_up))
  return notes
     
# Envelope to eliminate clicks that occur when changing notes:
def envelope():
  att_env = np.linspace(0, 1, ATTACK, False)
  ones = np.ones(note_len - ATTACK - RELEASE)
  rel_env = np.linspace(1, 0, RELEASE, False)
  env = np.append(att_env, ones)
  env = np.append(env, rel_env)
  return env

# Play a e sine wave note:
def playAudio(audio):
  play = sa.play_buffer(audio, 1, 2, SAMPLE_RATE)
  play.wait_done();

# Keep values within 16 bit range:
def clamp(n):
  return min(max(n, -(2**16 - 1)), (2**16 - 1)) 

# Calculate and return a list of lists (ascending arpeggios):
def calcSine(notes):
  x = np.linspace(0, seconds / num_notes, int(note_len), False)
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

def generate():
  for i in range(0,13):
    base = i + 12
    notes = manyArpeg(seconds, base, num_notes, note_pattern, num_arpegs, arpegs_pattern, notes_up)
    audioAll = calcSine(notes)
    playAudio(audioAll)
   # wavio.write(str(notes_up) + '_' + str(seconds) + '_' + str(base) + '_' + str(num_notes) + '_' 
   #   + str(note_pattern) + '_' + str(num_arpegs) + '_' + str(arpegs_pattern) + '_' + ".wav", audioAll, 
   #   SAMPLE_RATE, sampwidth=2, scale="none")
    wavio.write(str("base_" + str(base) + ".wav"), audioAll, SAMPLE_RATE, sampwidth=2, scale="none")

def main():
  generate()
 
if __name__ == "__main__":
  main()

