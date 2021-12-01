import board
import neopixel
from PIL import ImageColor

NUM_LEDS = 300
brightness = 50
pixels = neopixel.NeoPixel(board.D18, NUM_LEDS)

blue = 0,0,255
black = (0,0,0)

'''Sets the light strip to a solid color.
    color: the color to set the lights to. fill()
            from the Neopixel library requires RGB
            values, but this function will check first 
            if the color value is hex and convert it to 
            RGB, so both types are allowed.
    brightness: the brightness value to set the lights to.
                Default is 100 (full brightness)'''
def color_fill(color, brightness = 100):
    print(color)
    if("#" in color):                           #check if this is a hex number or not. if it is, convert it to an RGB value
        color = convert_hex_to_rgb(color)
    print(color)
    color = change_brightness(brightness, color)
    print(color)
    pixels.fill(color)

'''Sets the lights to a solid color with a wiping effect.
    color: the color to set the lights to. The fill() method
            from the Neopixel library requires RGB
            values, but this function will check first 
            if the color value is hex and convert it to 
            RGB, so both types are allowed.
    reverse(boolean): default is false. If set to true, colorWipe
            will start from the end of the strip and work backwards.'''
def color_wipe(color, reverse = False):
    c = convert_hex_to_rgb(color) 
    color_fill(black)

    if(reverse):
        print(f"Reverse Color wipe: {c}")
        for i in range(NUM_LEDS-1, 0, -1):      #technically counting down from 299, not 300 
            pixels[i] = c
    else:
        print(f"Color wipe: {c}")
        for i in range(0, NUM_LEDS):
            pixels[i] = c

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
    # color_fill(brightness)

    

'''Simply turns off the lights.'''
def turn_off():
    print("turning off lights")
    pixels.fill(black)

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