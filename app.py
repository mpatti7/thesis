from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basicFunctions/')
def basicFunctions():
    return render_template('basicFunctions.html')

# @app.route('/advancedFunctions')
# def advancedFunctions():
#     return render_template('advancedFunctions.html')

# @app.route('/musicSync')
# def musicSync():
#     return render_template('musicSync.html')

# @app.route('/info')
# def info():
#     return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
