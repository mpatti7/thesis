import subprocess

def create_options(form):
    options = dict()

    if('delay' in form):
        options['option1'] = dict()
        options['option1']['choice'] = 'delay'
        options['option1']['value'] = form['delay']
    if('speed' in form):
        options['option2'] = dict()
        options['option2']['choice'] = 'speed'
        options['option2']['value'] = form['speed']
    if('cycles' in form):
        options['option3'] = dict()
        options['option3']['choice'] = 'cycles'
        options['option3']['value'] = form['cycles']
    if('2Colors' in form):
        options['option4'] = dict()
        options['option4']['choice'] = '2Colors'
        options['option4']['color1'] = form['favcolor']
        options['option4']['color2'] = form['favColor2']

    return options

def shutdown_pi():
    print(f'Shutting down Pi...')
    subprocess.call('sudo shutdown now', shell=True)

def reboot_pi():
    print(f'Rebooting Pi...')
    subprocess.call('sudo reboot', shell=True)
