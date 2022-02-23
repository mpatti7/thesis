from flask import Flask, render_template, request
# import sqlalchemy
# from flask_sqlalchemy import SQLAlchemy
from celery import Celery
# import celery.result
# from celery.result import revoke
# from celery.task.control import revoke
# import celery.result
import lights

#start celery with this: sudo celery -A app.celery worker --loglevel=info

broker_url = 'amqp://localhost'

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
# app.config['result_backend'] = 'db+sqlite:///results.db'
# app.config['result_backend'] = 'amqp://guest@localhost//'
app.config['result_backend'] = 'rpc://results.db'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# CURRENT_TASK_ID = ''
tasks = dict()          #A dictionary to hold looping task ids

blue = (0,0,255)
red = (255,0,0)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basicFunctions/')
def basicFunctions():
    return render_template('basicFunctions.html')

@app.route('/basicFunctions/basicChange', methods = ["POST"])
def basicChange():
    form = request.form.to_dict()       #request the form data
    print(f"form = {form}")
    options = dict()

    if("options" in form):              #if any options were selected, they are added to a separate dictionary
        if(form["options"] == "2Colors"):
            options["option1"] = dict()
            options["option1"]["choice"] = "2Colors"
            options["option1"]["color1"] = form["favcolor"]
            options["option1"]["color2"] = form["favColor2"]
    else:
        options = None
    print(f"options: {options}")

    if('cancel' in form):
        #TODO: Make this not hardcoded, obviously, just don't forget
        tasks['fade_id'].revoke(terminate=True)
        turn_off.delay()
        print(f'killed task')
        return render_template('advancedFunctions.html')

    if("favcolor" in form and "functions" not in form):         #Regular color fill
        color = form["favcolor"]
        # lights.color_fill(color, form["slider"], options)
        result = color_fill.delay(color, form['slider'], options)
        print("color fill")
    elif("btnOff" in form):     #Turn off the lights
        print("turn off")
        turn_off.delay()

    elif(len(form) > 3):
        color = form["favcolor"]
        if("functions" in form):
            if(form["functions"] == "colorWipe"):
                task = color_wipe.delay(color, form['slider'], False, options)
                #TODO: In case any light function throws an exception, use task.traceback to see. Add in try/except with this?
                # print(f'task.ready(): {task.ready()}')
                # lights.color_wipe(color, form["slider"], False, options)
            if(form["functions"] == "rColorWipe"):
                # lights.color_wipe(color, form["slider"], True, options)
                color_wipe.delay(color, form['slider'], True, options)

    return render_template('basicFunctions.html')

@app.route('/advancedFunctions/')
def advancedFunctions():
    return render_template('advancedFunctions.html')

@app.route('/advancedFunctions/advancedChange', methods = ["POST"])
def advancedChange():
    form = request.form.to_dict()       #request the form data
    print(f"form = {form}")
    options = dict()
    color = form['favcolor']
    
    #TODO: Make this not hardcoded, obviously
    id = fade.delay(color)
    print(id.task_id)
    tasks['fade_id'] = id
    print(tasks['fade_id'])
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
def color_fill(color, brightness = 100, options = None):
    return lights.color_fill(color, brightness, options)

@celery.task(name='app.color_wipe')
def color_wipe(color, brightness = 100, reverse = False, options = None):
    return lights.color_wipe(color, brightness, reverse, options)

@celery.task(name='app.turn_off')
def turn_off():
    return lights.turn_off()

@celery.task(name='app.fade')
def fade(color):
    # task_id = fade.request.id
    # global CURRENT_TASK_ID
    # CURRENT_TASK_ID = task_id
    # print(task_id)
    return lights.fade(color)

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
