import subprocess
# import aubio
from aubio import source, onset, tempo, pitch
import numpy as np
import os
import lights
import csv

SMOOTH_JAZZ = 'static/songs/smooth_jazz.wav'
DRUM_BEAT = 'static/songs/drum_beat.wav'
SONGS_FOLDER_PATH = 'static/songs/'

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
    # print(f'onsets: {onsets}')

    # write the dictionary to a csv  
    # try:
    #     with open('static/songs/csv/smooth_jazz_onsets.csv', 'w') as csv:
    #         for key in onsets.keys():
    #             csv.write("%s,%s\n"%(key, onsets[key]))
    # except IOError as error:
    #     print(f'Error: {error}')
    return onsets

def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            raise ValueError("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            print(f'this_beat: {this_beat}')
            print(type(this_beat))
            beats.append(this_beat)
            print('adding beats')
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break
    return beats

def get_onsets_beats(file_path):
    print(f'Gettings onsets and beats...')

    win_s = 1024                # fft size
    hop_s = win_s // 2          # hop size
    samplerate = 0

    s = source(file_path, samplerate, hop_s)
    samplerate = s.samplerate

    o = onset("default", win_s, hop_s, samplerate)

    # s = source(file_path, samplerate, hop_s)
    # samplerate = s.samplerate
    b = tempo("default", win_s, hop_s, samplerate)

    onsets = {}

    # total number of frames read
    total_frames = 0
    beat_value = 0
    onset_time = 0
    delay = 4. * hop_s

    while True:
        samples, read = s()
        if o(samples):
            # samples, read = s()
            onset_time = o.get_last_s()
        is_beat = b(samples)
        if is_beat:
            this_beat = int(total_frames - delay + is_beat[0] * hop_s)
            print(this_beat)
            print("%f" % (this_beat / float(samplerate)))
            # beat_value = b.get_last_s()
        onsets[round(onset_time, 1)] = round(beat_value, 1)
        total_frames += read
        if read < hop_s: 
            break
    return onsets

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


# test = get_onsets_beats(TEST_WAV)
# print(test)

# test = get_pitches(TEST_WAV)
# print(test)

# test = get_file_bpm(TEST_WAV)
# test = get_onset_times(DRUM_BEAT)
# print(test)
# test = play_song(TEST_WAV)
# print(test)