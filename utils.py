import subprocess
import csv
import psutil
import lights

def create_options(form):
    options = dict()

    if('functions' in form):
        options['function'] = form['functions']
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

def read_onset_csv(csv_path):
    print(f'Reading in onsets...')
    onsets = {}

    try:
        with open(csv_path, 'r') as infile:
            reader = csv.reader(infile)
            onsets = {float(rows[0]):rows[1] for rows in reader}
    except IOError as error:
        print(f'Error: {error}')

    print('Complete')
    return onsets 

def get_ip_address():
    ip = subprocess.check_output(['hostname', '-I'])
    return str(ip.decode("UTF-8"))

#Returns the pin the lights are wired to
def get_gpio():
    return str(lights.pin)

#Returns CPU temperature in Celsius
def check_cpu_temp():
    temp = subprocess.check_output(['vcgencmd', 'measure_temp'])
    return str(temp.decode('UTF-8')).split('=')[1]
    
#Returns amount of used memory in mega bytes
def check_memory_usage():
    memory = psutil.virtual_memory()
    return str(round(memory.used / 1024.0 / 1024.0, 1)) + 'mb out of ' + str(round(memory.total / 1024.0 / 1024.0, 1)) + 'mb'

def get_light_model():
    return str(lights.model)

def get_num_leds():
    return str(lights.NUM_LEDS)
