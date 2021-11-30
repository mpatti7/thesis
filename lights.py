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
            RGB, so both types are allowed.'''
def color_fill(color):
    print(color)
    if("#" in color):                           #check if this is a hex number or not. if it is, convert it to an RGB value
        c = ImageColor.getcolor(color, "RGB")
        print(c)
        pixels.fill(c)
    else:
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
    c = ImageColor.getcolor(color, "RGB") 
    color_fill(black)

    if(reverse):
        print(f"Reverse Color wipe: {c}")
        for i in range(NUM_LEDS-1, 0, -1):      #technically counting down from 299, not 300 
            pixels[i] = c
    else:
        print(f"Color wipe: {c}")
        for i in range(0, NUM_LEDS):
            pixels[i] = c

def change_brightness(val):
    brightness = val
    print(brightness)

'''Simply turns off the lights.'''
def turn_off():
    print("turning off lights")
    pixels.fill(black)


# while True:
#     try:
#         # pixels.fill(blue)
#         color_fill(blue)
#     except KeyboardInterrupt as error:
#         # pixels.fill(black)
#         color_fill(black)
#         exit()