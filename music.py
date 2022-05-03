import subprocess
from aubio import source, onset, tempo, pitch
import numpy as np
import os
import lights
import csv

SMOOTH_JAZZ = 'static/songs/smooth_jazz.wav'
DRUM_BEAT = 'static/songs/drum_beat.wav'
JELLYFISH_JAM = 'static/songs/jellyfish_jam.wav'
SONGS_FOLDER_PATH = 'static/songs/'


# Code from: https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py
# Gets the pitch value of an audio file
# Modified to fit my needs
def get_beats(song_path):
    win_s = 1024                # fft size
    hop_s = win_s // 2          # hop size

    samplerate = 0
    s = source(song_path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    onsets = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if o(samples):
            print("%f" % o.get_last_s())
            onsets.append(o.get_last_s())
            if is_beat:
                this_beat = o.get_last_s()
                beats.append(this_beat)
        total_frames += read
        if read < hop_s:
            break
    return beats


# Code from: https://github.com/aubio/aubio/blob/master/python/demos/demo_onset.py
# Gets the timestamps of onsets within an audio file
# Modified to fit my needs
def get_onset_times(file_path):
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size

    samplerate = 0

    s = source(file_path, samplerate, hop_s)
    samplerate = s.samplerate

    o = onset("default", win_s, hop_s, samplerate)

    # list of onsets, in samples
    # onsets = []
    onsets = {}

    # total number of frames read
    total_frames = 0
    i = 0
    while True:
        samples, read = s()
        if o(samples):
            # print("%f" % o.get_last_s())
            # onsets[str(i)] = round(o.get_last_s(), 1)
            onsets[round(o.get_last_s(), 1)] = i
            i += 1
            # onsets.append(o.get_last_s())
            # onsets.append(o.get_last())
        total_frames += read
        if read < hop_s: 
            break
    return onsets


# Code from: https://github.com/aubio/aubio/blob/master/python/demos/demo_pitch.py
# Gets the pitch value of an audio file
# Modified to fit my needs
def get_pitches(file_path):
    downsample = 1
    samplerate = 44100 // downsample
    win_s = 4096 // downsample # fft size
    hop_s = 512  // downsample # hop size

    s = source(file_path, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        this_pitch = pitch_o(samples)[0]
        print(this_pitch)
        pitches += [this_pitch]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < hop_s: 
            break

    print("Average frequency = " + str(np.array(pitches).mean()) + " hz")


# test = get_pitches(DRUM_BEAT)
# print(test)

# test = get_onset_times(JELLYFISH_JAM)
# print(test)
