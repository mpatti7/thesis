from flask import Flask, render_template, request
# import sqlalchemy
from celery import Celery
import lights

#start celery with this: sudo celery -A app.celery worker --loglevel=info

broker_url = 'amqp://localhost'

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['result_backend'] = 'db+sqlite:///results.db'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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

    if("favcolor" in form and "functions" not in form):         #Regular color fill
        color = form["favcolor"]
        # lights.color_fill(color, form["slider"], options)
        color_fill.delay(color, form['slider'], options)
        print("color fill")
    elif("btnOff" in form):     #Turn off the lights
        print("turn off")
        # lights.turn_off()
        turn_off.delay()

    elif(len(form) > 3):
        color = form["favcolor"]
        if("functions" in form):
            if(form["functions"] == "colorWipe"):
                color_wipe.delay(color, form['slider'], False, options)
                # lights.color_wipe(color, form["slider"], False, options)
            if(form["functions"] == "rColorWipe"):
                # lights.color_wipe(color, form["slider"], True, options)
                color_wipe.delay(color, form['slider'], True, options)

    return render_template('basicFunctions.html')

@app.route('/advancedFunctions/')
def advancedFunctions():
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
