from flask import Flask, render_template, request
from celery import Celery
import lights
import utils

#start celery with this: sudo celery -A app.celery worker --loglevel=info

broker_url = 'amqp://localhost'

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
# app.config['result_backend'] = 'db+sqlite:///results.db'
# app.config['result_backend'] = 'amqp://guest@localhost//'
app.config['result_backend'] = 'rpc://results.db'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# tasks = dict()          #A dictionary to hold looping task ids
tasks = list()

blue = (0,0,255)
red = (255,0,0)
 
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

    if('cancel' in form):                   #check if any repeating function needs to be canceled before doing anything else
        if(len(tasks) > 0):
            tasks[0].revoke(terminate=True)
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

    #If a function was not selected, then just do a regular color fill
    if("favcolor" in form and "functions" not in form):         #Regular color fill
        color = form["favcolor"]
        task = color_fill.delay(color, options, brightness)
        print("color fill")
    elif("btnOff" in form):     #Turn off the lights
        print("turn off")
        turn_off.delay()

    #If a function was selected, then call it
    elif('functions' in form):
        color = form["favcolor"]
        if(form["functions"] == "colorWipe"):               #Color wipe
            task = color_wipe.delay(color, options, brightness, False)
            tasks.append(task)
            #TODO: In case any light function throws an exception, use task.traceback to see. Add in try/except with this?
            # print(f'task.ready(): {task.ready()}')
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
            task = theaterChase.delay(color, options, brightness, True)
            tasks.append(task)
        if(form['functions'] == 'twinkle'):
            task = twinkle.delay(color, options, brightness, True)
            tasks.append(task)

    return render_template('controls.html')

@app.route('/advancedFunctions/')
def advancedFunctions():
    return render_template('advancedFunctions.html')

@app.route('/advancedFunctions/advancedChange', methods = ["POST"])
def advancedChange():
    return render_template('advancedFunctions.html')

@app.route('/musicSync/')
def musicSync():
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
    # task_id = fade.request.id
    # print(task_id)
    return lights.fade(color, options, brightness, repeat)

@celery.task(name='app.theaterChase')
def theaterChase(color, options, brightness=100, repeat=True):
    return lights.theaterChase(color, options, brightness, repeat)

@celery.task(name='app.twinkle')
def twinkle(color, options, brightness=100, repeat=True):
    return lights.twinkle(color, options, brightness, repeat)


#CELERY TEST
# @app.route('/process/<name>')
# def process(name):
#     reverse.delay(name)
#     return 'I sent an async request'

# @celery.task(name='app.reverse')
# def reverse(string):
#     return string[::-1]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
