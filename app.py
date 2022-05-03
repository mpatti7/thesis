# '''
#     File name: app.py
#     Author: Marissa Patti
#     Python Version: 3.9.2
#     Description: The main Flask application
# '''

from flask import Flask, render_template, request, jsonify
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
import onsets 
import lights
import utils
import music
import time

#start celery with this: sudo celery -A app.celery worker --loglevel=info

broker_url = 'amqp://localhost'

# Flask app configurations
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_BACKEND_URL'] = "db+sqlite:///results.sqlite"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_BACKEND_URL'])
celery.conf.update(app.config)

tasks = list()      #A list to hold celery task ids

blue = (0,0,255)
red = (255,0,0)
black = '#000000'

# Creates the database
db = SQLAlchemy(app)

class Results(db.Model):
    # id = db.Column('id', db.Integer, primary_key=True)
    onset = db.Column('onset', db.String(10), primary_key=True)

    def __init__(self, onset):
        self.onset = onset
 
# The Welcome Screen Route
@app.route('/', methods=['GET', 'POST'])
def index():
    form = request.get_json()
    print(f'form: {form}')

    if(form):
        if(form['choice'] == 'shutdown'):
            utils.shutdown_pi()
        elif(form['choice'] == 'reboot'):
            utils.reboot_pi()

    return render_template('index.html')

# Controls
@app.route('/controls/', methods=['GET', 'POST'])
def controls():
    form = request.get_json()
    print(f'form: {form}')

    if(form):
        if(form['choice'] == 'shutdown'):
            utils.shutdown_pi()
        elif(form['choice'] == 'reboot'):
            utils.reboot_pi()

    return render_template('controls.html')

@app.route('/controls/controlsChange', methods=['GET', 'POST'])
def controlsChange():
    rpiControls = request.get_json()
    print(f'rpiControls: {rpiControls}')

    if(rpiControls):
        if(rpiControls['choice'] == 'shutdown'):
            utils.shutdown_pi()
        elif(rpiControls['choice'] == 'reboot'):
            utils.reboot_pi()

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
        if(form["functions"] == "colorWipe"):               
            task = color_wipe.delay(color, options, brightness, False)
            tasks.append(task)
        elif(form["functions"] == "rColorWipe"):              
            task = color_wipe.delay(color, options, brightness, True)
            tasks.append(task)
        elif(form['functions'] == 'dotFill'):
            task = dot_fill.delay(color, options, brightness)
            tasks.append(task)
        elif(form["functions"] == "fade"):                    
            task = fade.delay(color, options, brightness)
            tasks.append(task)
        elif(form["functions"] == "theaterChase"):            
            task = theater_chase.delay(color, options, brightness, True)
            tasks.append(task)
        elif(form['functions'] == 'twinkle'):
            task = twinkle_disco.delay(color, options, brightness, True)
            tasks.append(task)
        elif(form['functions'] == 'disco'):
            task = twinkle_disco.delay(color, options, brightness, True)
            tasks.append(task)

    return render_template('controls.html')

# Playlists 
@app.route('/playlists/', methods = ["GET", "POST"])
def playlists():
    form = request.get_json()
    print(f'form: {form}')

    if(form):
        if(form['choice'] == 'shutdown'):
            utils.shutdown_pi()
        elif(form['choice'] == 'reboot'):
            utils.reboot_pi()

    return render_template('playlists.html')

@app.route('/playlists/playlistsChange', methods = ["GET", "POST"])
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
    elif('preset' in form):
        if(form['preset'] == 'basic'):
            task = basic_light_show.delay()
            tasks.append(task)
    else:
        task = play_sequence.delay(form)
        tasks.append(task)
    return render_template('playlists.html')

# Music Sync
@app.route('/musicSync/', methods = ["GET", "POST"])
def musicSync():  
    form = request.get_json()
    print(f'form: {form}')

    if(form):
        if(form['choice'] == 'shutdown'):
            utils.shutdown_pi()
        elif(form['choice'] == 'reboot'):
            utils.reboot_pi()

    return render_template('musicSync.html')

@app.route('/musicSync/musicChange', methods = ["GET", "POST"])
def musicChange():
    song = request.get_json()   # Request the song data
    print(f'Song: {song}')
    beats = {}
    if('onsets' in song):
        beats = onsets.get(song['onsets'])

    if(len(tasks) > 0):       # Cancel any tasks already running before starting this next one
        tasks[0].revoke(terminate=True, signal='SIGKILL')
        lights.turn_off()
        print(f'killed task')
        tasks.pop(0)
    if("btnOff" in song):     # Turn off the lights if the off button was clicked
        print("turn off")
        turn_off.delay()
        celery.control.purge()
    else:                     # Otherwise, the song is playing so flash the lights accordingly
        time.sleep(.5)
        if('color' in song):
            light_evens.delay(song['color'], song['brightness'])
        if('currentTime' in song):
            if(song['currentTime'] in beats):
                print(f'yes')
                light_odds.delay(song['color'], song['brightness'])
                time.sleep(.40)
                light_odds.delay(black, song['brightness'])
    
    return render_template('musicSync.html')

# Info
@app.route('/info/', methods = ["GET", "POST"])
def info():
    rpiControls = request.get_json()
    print(f'rpiControls: {rpiControls}')

    if(rpiControls):
        if(rpiControls['choice'] == 'shutdown'):
            utils.shutdown_pi()
        elif(rpiControls['choice'] == 'reboot'):
            utils.reboot_pi()

    # Get system information
    form = {}
    ip = utils.get_ip_address()
    pin = utils.get_gpio()
    temp = utils.get_cpu_temp()
    ram = utils.get_memory_usage()
    model = utils.get_light_model()
    num_leds = utils.get_num_leds()

    if(request.method == 'POST'):       # Request the stuff entered in the text fields on the UI
        form = request.form.to_dict()
        print(f'form: {form}')

    # If the form is not empty, check if anything changed and change it if it did
    if(form):   
        if(form['num_lights'] != num_leds):
            print(f'Changing the amount of LEDs')
        if(form['pin'] != pin):
            print(f'Changing pin number')
        if(form['light_model'] != model):
            print(f'Changing model')

    # Return the HTML template, with the system information to display
    return render_template('info.html', ip=ip, pin=pin, temp=temp, ram=ram, model=model, num_leds=num_leds)

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

@celery.task(name='app.light_evens')
def light_evens(color, brightness=100):
    return lights.light_evens(color, brightness)

@celery.task(name='app.light_odds')
def light_odds(color, brightness=100):
    return lights.light_odds(color, brightness)

@celery.task(name='app.basic_light_show')
def basic_light_show():
    return lights.basic_light_show()

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    # app.run(debug=True)
