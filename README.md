# Light Pi

Light Pi is a Flask based web application powered by a Raspberry Pi to remotely control LED lights with a GUI.

## Supplies
- https://www.amazon.com/ALITOVE-WS2812B-Programmable-Addressable-Waterproof/dp/B018XAELE4/ref=sr_1_6?crid=39PLUTUT9CLSH&dchild=1&keywords=alitove+ws2812b&qid=1632438856&sprefix=alitove%2Caps%2C166&sr=8-6
- 15 amp Power supply
- 74AHCT125 level converter chip

## Hardware Setup/Wiring
- https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring 
    - Using the level converter chip 
1. Pi GPIO18 to 74AHCT125 pin 1A
2. 74AHCT125 pin 1Y to NeoPixel DIN
3. Power supply ground to 74AHCT125 ground
4. Power supply ground to 74AHCT125 pin 1OE
5. Power supply ground to Pi GND
6. Power supply ground to NeoPixel GND
7. Power supply 5V to 74AHCT125 VCC
8. Power supply 5V to NeoPixel 5V

## Software Installations
1. Install Flask
```bash
sudo pip3 install flask
```
2. Install Celery
```bash
sudo pip3 install celery
```
3. Install RabbitMQ
```bash
sudo apt-get install rabbitmq-server
sudo pip3 install rabbitmq
```
4. Install Adafruit Neopixels 
    - https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage 
```bash
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
sudo python3 -m pip install --force-reinstall adafruit-blinka
```
## Software Setup
1. https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/
    - Follow "Preparation and Installation" up to step 5
2. Clone test repo and run a test
```bash
git clone https://github.com/rpi-ws281x/rpi-ws281x-python.git
```
3. There should be a folder called rpi-WS281x-python somewhere on the pi
```bash
cd rpi-ws281x-python/examples
sudo python3 strandtest.py
```
- Note: the number of leds in this file is only 16. You can edit the file and change LED_COUNT to the amount of lights you have
- If the LEDs behave normally with this test script, then the setup is complete. If not, follow the "Troubleshooting" section 
of this website: https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html  

4. Clone Light Pi
```bash
git clone https://github.com/mpatti7/thesis.git
```

## Run The Project
1. Open 2 terminals
2. For both terminals: 
```bash
cd thesis/  
```
3. In one terminal:
```bash
sudo python3 app.py 
```
4. In the other terminal:
```bash
sudo celery -A app.celery worker --loglevel=info 
```
5. In your browser, navigate to the IP address of your Pi

<!-- ## How To Use -->
