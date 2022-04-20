import subprocess
# import aubio
from aubio import source, onset, tempo
import numpy
import os
import lights

TEST_WAV = 'static/songs/smooth_jazz.wav'
SONGS_FOLDER_PATH = 'static/songs/'

# def get_commands():
#     print("getting commands")
#     commands = list()
#     return commands


# def run_ffmpeg():
#     print("running ffmpeg")
#     subprocess.Popen(["sudo", "ffmpeg", "-listen", "1", "-i", "http://10.184.128.24:80",  "-c", "copy", "somefile.ogg"])
#     #sudo ffmpeg -listen 1 -i http://10.184.128.24:80 -c copy somefile.ogg

def play_song(song_path):
    with source(song_path) as src:
        test = tempo()
        print(test)
        for frames in src:
            print(frames)

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
            print('onset')
            print("%f" % o.get_last_s())
            onsets.append(o.get_last_s())
            if is_beat:
                print('beat')
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
    onsets = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        if o(samples):
            print("%f" % o.get_last_s())
            onsets.append(o.get_last_s())
            # onsets.append(o.get_last())
        total_frames += read
        if read < hop_s: 
            break
    return onsets

#This gives me a float value representing a beat. this can probably be used to judge the intensity of the lights 
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

def get_song(song_name):
    song_path = ''

    for root, dirs, file in os.walk(SONGS_FOLDER_PATH):
        for f in file:
            if(song_name in f):
                print('found song')
                song_path = os.path.join(root, f)
                return song_path 

# test = get_file_bpm(TEST_WAV)
# test = get_onset_times(TEST_WAV)
# print(test)
# test = play_song(TEST_WAV)
# print(test)