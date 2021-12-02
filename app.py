from flask import Flask, render_template, request
import lights

app = Flask(__name__)

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
    form = request.form.to_dict()
    print(f"form = {form}")

    # if(len(form) == 1 and "favcolor" in form):
    if(len(form) == 3 and "favcolor" in form and "functions" not in form):
        color = form["favcolor"]
        lights.color_fill(color, form["slider"])
        print("color fill")
    elif("btnOff" in form):
        print("turn off")
        lights.turn_off()
    elif(len(form) > 3):
        color = form["favcolor"]
        if("functions" in form):
            if(form["functions"] == "colorWipe"):
                lights.color_wipe(color, form["slider"])
            if(form["functions"] == "rColorWipe"):
                lights.color_wipe(color, form["slider"], True)
        if("options" in form):
            if(form["options"] == "2Colors"):
                lights.two_colors(form["favcolor"], form["favColor2"])

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
