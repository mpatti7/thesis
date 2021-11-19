from flask import Flask, render_template, request
import lights

app = Flask(__name__)

blue = (0,0,255)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basicFunctions/')
def basicFunctions():
    #if color changed dont make new route, call function here and return this page
    return render_template('basicFunctions.html')

@app.route('/colorChange', methods = ["POST"])
def colorChange():
    # turn_off = request.form["btnOff"]
    # print(turn_off)
    color = request.form["favcolor"]
    lights.color_fill(color)
    # function = request.form["options"]
    # print(function)
    # if(function == "colorWipe"):
    #     lights.color_wipe(color)
    return render_template('basicFunctions.html')

@app.route('/functionChange', methods = ["POST"])
def functionChange():
    # color = request.form["favcolor"]
    # print(color)
    function = request.form["options"]
    print(function)
    if(function == "colorWipe"):
        lights.color_wipe(blue)
    if(function == "rColorWipe"):
        lights.color_wipe(blue, True)
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
