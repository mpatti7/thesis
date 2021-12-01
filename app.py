from flask import Flask, render_template, request
import lights

app = Flask(__name__)
 
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
    if("favcolor" in form and "options" not in form):
        color = form["favcolor"]
        lights.color_fill(color, form["slider"])
        print("color fill")
    elif("btnOff" in form):
        print("turn off")
        lights.turn_off()
    elif(len(form) > 2 and "options" in form):
        color = form["favcolor"]
        if(form["options"] == "colorWipe"):
            lights.color_wipe(color)
        if(form["options"] == "rColorWipe"):
            lights.color_wipe(color, True)
    # if("slider" in form):
    #     color = request.form["favcolor"]
    #     lights.change_brightness(form["slider"], color)

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
