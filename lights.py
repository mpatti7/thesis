import board
import neopixel
from PIL import ImageColor
import time

NUM_LEDS = 300
brightness = 50
pin = board.D18
pixels = neopixel.NeoPixel(pin, NUM_LEDS, auto_write = False)

blue = 0,0,255
black = (0,0,0)

'''Sets the light strip to a solid color.
    color: the color to set the lights to. fill()
            from the Neopixel library requires RGB
            values, but this function will check first 
            if the color value is hex and convert it to 
            RGB, so both types are allowed.
    brightness: the brightness value to set the lights to.
                Default is 100 (full brightness)
    options: Default is None.  A dictionary of options to alter 
            this animation'''
def color_fill(color, options, brightness = 100):
    if('option4' in options):
        color1 = options["option4"]["color1"]
        color2 = options["option4"]["color2"]

        print(f"Double color fill: {color1}, {color2}")

        if("#" in color1):
            color1 = convert_hex_to_rgb(color1)
        if("#" in color2):
            color2 = convert_hex_to_rgb(color2)

        color1 = change_brightness(brightness, color1)
        color2 = change_brightness(brightness, color2)

        for i in range(0, NUM_LEDS, 2):
            pixels[i] = color1
        for j in range(1, NUM_LEDS-1, 2):
            pixels[j] = color2
        pixels.show()
    else:
        print(color)
        if("#" in color):                           #check if this is a hex number or not. if it is, convert it to an RGB value
            color = convert_hex_to_rgb(color)
        print(color)
        color = change_brightness(brightness, color)
        print(color)
        pixels.fill(color)
        pixels.show() 

'''Sets the lights to a solid color with a wiping effect.
    color: the color to set the lights to. The fill() method
            from the Neopixel library requires RGB
            values, but this function will check first 
            if the color value is hex and convert it to 
            RGB, so both types are allowed.
    brightness(int): the brightness value to set the lights to.
                Default is 100 (full brightness)
    reverse(boolean): default is false. If set to true, colorWipe
            will start from the end of the strip and work backwards.
    options(dict): default is None. A dictionary of options to alter 
            this animation
    delay(int): default is 0. The time between when each LED is lit up in seconds.'''
def color_wipe(color, options, brightness = 100, reverse = False):
    pixels.fill(black)
    delay = 0.0

    if('option1' in options):
        delay = float(options['option1']['value']) / 1000.0
        print(f'delay {delay}')
        # delay = delay/1000.0
        
    if('option4' in options):
        print(f"Double color wipe")

        color1 = options["option4"]["color1"]
        color2 = options["option4"]["color2"]

        if("#" in color1):                           
            color1 = convert_hex_to_rgb(color1)
        if("#" in color2):                           
            color2 = convert_hex_to_rgb(color2)
        
        color1 = change_brightness(brightness, color1)
        color2 = change_brightness(brightness, color2)

        if(reverse):
            for i in range(NUM_LEDS-1, -1, -1):
                if(i % 2 != 0):
                    pixels[i] = color1
                if(i % 2 == 0):
                    pixels[i] = color2
                pixels.show()
                time.sleep(delay)
        else:
            for i in range(0, NUM_LEDS):
                if(i % 2 != 0):
                    pixels[i] = color1
                if(i % 2 == 0):
                    pixels[i] = color2
                pixels.show()
                time.sleep(delay)
    else:
        if("#" in color):
            color = convert_hex_to_rgb(color) 
        pixels.show()
        color = change_brightness(brightness, color)

        if(reverse):
            print(f"Reverse Color wipe: {color}")
            for i in range(NUM_LEDS-1, -1, -1):      #technically counting down from 299, not 300 
                pixels[i] = color
                pixels.show()
                time.sleep(delay)
        else:
            print(f"Color wipe: {color}")
            for i in range(0, NUM_LEDS):
                pixels[i] = color
                pixels.show()
                time.sleep(delay)

'''Fades the strip of lights in and out
    color: the color of the lights
    brightness: default is 100. the brightness of the lights
    speed: the rate of which each RGB value increases or decreases by.
            default is 1
    options: default is None. A dictionary of options to alter 
            this animation
    repeat: Default is True. If enabled, this will repeat until it is stopped
            by the user. If disabled, it will only repeat for a specified 
            amount of cycles'''
def fade(color, options, brightness=100, repeat=True):
    turn_off()
    fade_color = list()
    # speed_rate = 1
    cycles = 0

    if('#' in color):
        color = convert_hex_to_rgb(color)
    color = change_brightness(brightness, color)

    if('option3' in options):
        cycles = int(options['option3']['value'])
    if(cycles > 0):
        repeat = False

    #color is a tuple, so the values can't be changed, so it's rgb values are copied into a list where they can be changed
    fade_color.append(color[0])
    fade_color.append(color[1])
    fade_color.append(color[2])

    r_max = color[0]
    g_max = color[1]
    b_max = color[2]

    pixels.fill(fade_color)
    
    #TODO: Add in speed options. May need to add logic if the speed rate won't add or subtract to an even 0 or 255, based on rgb value
    # if(speed == 'default'):
    #     speed_rate = 1
    # print(f'speed: {speed}')
    # if(speed == 'medium'):
    #     speed_rate == 25
    # elif(speed == 'fast'):
    #     speed_rate == 50

    while repeat:
        #Prevent each value from going below 0
        if(fade_color[0] < 0):
            fade_color[0] = 0
        if(fade_color[1] < 0):
            fade_color[1] = 0
        if(fade_color[2] < 0):
            fade_color[2] = 0

        while (fade_color[0] < r_max or fade_color[1] < g_max or fade_color[2] < b_max):
            #Fade up
            if(fade_color[0] < r_max):
                fade_color[0] += 1
            if(fade_color[1] < g_max):
                fade_color[1] += 1
            if(fade_color[2] < b_max):
                fade_color[2] += 1
            print(fade_color)
            pixels.fill(fade_color)
            pixels.show()
        
        while (fade_color[0] != 0 or fade_color[1] != 0 or fade_color[2] != 0):
            #Fade down
            if(fade_color[0] != 0):
                fade_color[0] -= 1
            if(fade_color[1] != 0):
                fade_color[1] -= 1
            if(fade_color[2] != 0):
                fade_color[2] -= 1
            print(fade_color)
            pixels.fill(fade_color)
            pixels.show()   
    
    if(not repeat):
        for i in range(cycles):
            if(fade_color[0] < 0):
                fade_color[0] = 0
            if(fade_color[1] < 0):
                fade_color[1] = 0
            if(fade_color[2] < 0):
                fade_color[2] = 0

            while (fade_color[0] < r_max or fade_color[1] < g_max or fade_color[2] < b_max):
                #Fade up
                if(fade_color[0] < r_max):
                    fade_color[0] += 1
                if(fade_color[1] < g_max):
                    fade_color[1] += 1
                if(fade_color[2] < b_max):
                    fade_color[2] += 1
                print(fade_color)
                pixels.fill(fade_color)
                pixels.show()
            
            while (fade_color[0] != 0 or fade_color[1] != 0 or fade_color[2] != 0):
                #Fade down
                if(fade_color[0] != 0):
                    fade_color[0] -= 1
                if(fade_color[1] != 0):
                    fade_color[1] -= 1
                if(fade_color[2] != 0):
                    fade_color[2] -= 1
                print(fade_color)
                pixels.fill(fade_color)
                pixels.show() 

def theaterChase(color, options, brightness=100, repeat=True):
    print('turn off lights')
    print(f'options: {options}')
    delay = 50
    cycles = 0
    turn_off()

    if('option1' in options):
        delay = float(options['option1']['value'])
    if('option3' in options):
        cycles = int(options['option3']['value'])
    if(cycles > 0):
        repeat = False

    if('#' in color):
        color = convert_hex_to_rgb(color)
    color = change_brightness(brightness, color)

    while repeat:
        for j in range(3):
            for k in range(0, NUM_LEDS, 3):
                pixels[k+j] = color
            pixels.show()
            time.sleep(delay/1000.0)
            for q in range(0, NUM_LEDS, 3):
                pixels[q+j] = black
    
    if(not repeat):
        for i in range(cycles):
            for j in range(3):
                for k in range(0, NUM_LEDS, 3):
                    pixels[k+j] = color
                pixels.show()
                time.sleep(delay/1000.0)
                for q in range(0, NUM_LEDS, 3):
                    pixels[q+j] = black
        turn_off()


'''Adjusts the brightness of the lights. Multiplies the percentage 
    by the RGB values to get a less intense version of the same color.
    val: the percentage from the slider. 
    color: the color chosen for the lights.'''
def change_brightness(val, color):
    if("#" in color):
        color = convert_hex_to_rgb(color)
    val = int(val) / 100
    brightness = (int(color[0] * val), int(color[1] * val), int(color[2] * val))
    print(f"brightness = {brightness}")
    return brightness

'''Simply turns off the lights.'''
def turn_off():
    print("turning off lights")
    pixels.fill(black)
    pixels.show()

'''Converts a hexadecimal value to an RGB value.'''
def convert_hex_to_rgb(hex):
    rgb = ImageColor.getcolor(hex, "RGB")
    return rgb

# while True:
#     try:
#         # pixels.fill(blue)
#         color_fill(blue)
#     except KeyboardInterrupt as error:
#         # pixels.fill(black)
#         color_fill(black)
#         exit()