from flask import Flask, render_template, request, jsonify
from celery import Celery
# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from onsets import smooth_jazz_onsets
import lights
import utils
import music
import time

#start celery with this: sudo celery -A app.celery worker --loglevel=info

broker_url = 'amqp://localhost'

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_BACKEND_URL'] = "db+sqlite:///results.sqlite"
# app.config['CELERY_BACKEND_URL'] = 'sqla+sqlite:///celerydb.sqlite'
# app.config['result_backend'] = 'db+sqlite:///results.db'
# app.config['result_backend'] = 'amqp://guest@localhost//'
# app.config['result_backend'] = 'rpc://results.db'
# app.config['result_backend'] = "db+sqlite:///results.sqlite"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_BACKEND_URL'])
celery.conf.update(app.config)

tasks = list()      #A list to hold task ids

blue = (0,0,255)
red = (255,0,0)
black = '#000000'

# smooth_jazz_onsets = {}

db = SQLAlchemy(app)

class Results(db.Model):
    # id = db.Column('id', db.Integer, primary_key=True)
    onset = db.Column('onset', db.String(10), primary_key=True)

    def __init__(self, onset):
        self.onset = onset
 
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/controls/')
def controls():
    return render_template('controls.html')

@app.route('/controls/controlsChange', methods = ["POST"])
def controlsChange():
    form = request.form.to_dict()       #request the form data as a dictionary
    print(f"form = {form}")
    options = dict()
    brightness = int()

    #Check if there was another task running already if the user selects another animation and doesn't cancel it first
    if(len(tasks) > 0):
        tasks[0].revoke(terminate=True, signal='SIGKILL')
        turn_off.delay()
        print(f'killed task')
        tasks.pop(0)

    if('cancel' in form):                   #check if any repeating function needs to be canceled before doing anything else
        if(len(tasks) > 0):
            tasks[0].revoke(terminate=True, signal='SIGKILL')
            turn_off.delay()
            print(f'killed task')
            tasks.pop(0)
        return render_template('controls.html')

    #if any options were selected, they are added to a separate dictionary
    options = utils.create_options(form)
    print(f"options: {options}")

    #brightness is the only option that is not part of the options dictionary, it will be used for every function
    if('brightness' in form):
        brightness = float(form['brightness'])
    
    if("btnOff" in form):     #Turn off the lights
        print("turn off")
        turn_off.delay()

    #If a function was not selected, then just do a regular color fill
    if("favcolor" in form and "functions" not in form and "btnOff" not in form):         #Regular color fill
        color = form["favcolor"]
        task = color_fill.delay(color, options, brightness)
        print("color fill")

    #If a function was selected, then call it
    elif('functions' in form):
        color = form["favcolor"]
        if(form["functions"] == "colorWipe"):               #Color wipe
            task = color_wipe.delay(color, options, brightness, False)
            tasks.append(task)
        if(form["functions"] == "rColorWipe"):              #Reverse Color wipe
            task = color_wipe.delay(color, options, brightness, True)
            tasks.append(task)
        if(form['functions'] == 'dotFill'):
            task = dot_fill.delay(color, options, brightness)
            tasks.append(task)
        if(form["functions"] == "fade"):                    #Fade
            task = fade.delay(color, options, brightness)
            tasks.append(task)
        if(form["functions"] == "theaterChase"):            #Theater Chase
            task = theater_chase.delay(color, options, brightness, True)
            tasks.append(task)
        if(form['functions'] == 'twinkle'):
            task = twinkle_disco.delay(color, options, brightness, True)
            tasks.append(task)
        if(form['functions'] == 'disco'):
            task = twinkle_disco.delay(color, options, brightness, True)
            tasks.append(task)

    return render_template('controls.html')

@app.route('/playlists/')
def playlists():
    return render_template('playlists.html')

@app.route('/playlists/playlistsChange', methods = ["POST"])
def playlistsChange():
    form = request.get_json()
    print(f"form = {form}")

    if(len(tasks) > 0):
        tasks[0].revoke(terminate=True, signal='SIGKILL')
        turn_off.delay()
        print(f'killed task')
        tasks.pop(0)

    if('cancel' in form):                   #check if any repeating function needs to be canceled before doing anything else
        if(len(tasks) > 0):
            tasks[0].revoke(terminate=True, signal='SIGKILL')
            turn_off.delay()
            print(f'killed task')
            tasks.pop(0)
        # return render_template('playlists.html')
    else:
        task = play_sequence.delay(form)
        tasks.append(task)
    return render_template('playlists.html')

@app.route('/musicSync/')
def musicSync():   
    return render_template('musicSync.html')

@app.route('/musicSync/musicChange', methods = ["POST"])
def musicChange():
    song = request.get_json()   
    print(f'Song: {song}')
    currentTime = song['currentTime']
    brightness = 100
    color = song['color']
    options = {}

    if(len(tasks) > 0):
        tasks[0].revoke(terminate=True, signal='SIGKILL')
        lights.turn_off()
        print(f'killed task')
        tasks.pop(0)

    if(currentTime in smooth_jazz_onsets):
        print(f'yes')
        color_fill.delay(color, options, brightness)
        time.sleep(.25)
        color_fill.delay(black, options, brightness)
        time.sleep(.25)
    
    return render_template('musicSync.html')

@app.route('/info/')
def info():
    return render_template('info.html')

######################################
########### CELERY TASKS #############
######################################
@celery.task(name='app.color_fill')
def color_fill(color, options, brightness = 100):
    return lights.color_fill(color, options, brightness)

@celery.task(name='app.color_wipe')
def color_wipe(color, options, brightness = 100, reverse = False):
    return lights.color_wipe(color, options, brightness, reverse)

@celery.task(name='app.dot_fill')
def dot_fill(color, options, brightness):
    return lights.dot_fill(color, options, brightness)

@celery.task(name='app.turn_off')
def turn_off():
    return lights.turn_off()

@celery.task(name='app.fade')
def fade(color, options, brightness=100, repeat=True):
    return lights.fade(color, options, brightness, repeat)

@celery.task(name='app.theater_chase')
def theater_chase(color, options, brightness=100, repeat=True):
    return lights.theater_chase(color, options, brightness, repeat)

@celery.task(name='app.twinkle_disco')
def twinkle_disco(color, options, brightness=100, repeat=True):
    return lights.twinkle_disco(color, options, brightness, repeat)

@celery.task(name='app.play_sequence')
def play_sequence(form):
    return lights.play_sequence(form)

@celery.task(name='app.read_csv')
def read_csv():
    # global smooth_jazz_onsets
    # smooth_jazz_onsets = utils.read_onset_csv('static/songs/csv/smooth_jazz_onsets.csv')
    utils.read_onset_csv('static/songs/csv/smooth_jazz_onsets.csv')

@celery.task(name='app.process_song')
def process_song(song):
    song_path = music.get_song(song)
    beats = music.get_beats(song_path)
    # onset_timestamps = music.get_onset_times(song_path)
    # beat_intensity = music.get_file_bpm(song_path)
    # print(len(onset_timestamps))
    # print(len(beat_intensity))

@celery.task(name='app.insert')
def insert_async(data):
    print(f'Inserting data...')
    db.session.add(data)
    db.session.commit()
    return 'Done'

def insert(data):
    print(f'Inserting data...')
    db.session.add(data)
    db.session.commit()
    return 'Done'

if __name__ == '__main__':
    # read_csv.delay()
    # smooth_jazz_onsets = utils.read_onset_csv('static/songs/csv/smooth_jazz_onsets.csv')
    # print(len(smooth_jazz_onsets))
    app.run(debug=True, host='0.0.0.0', port=80)
    # app.run(debug=True)
