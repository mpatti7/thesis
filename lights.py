import board
import neopixel
from PIL import ImageColor

NUM_LEDS = 300
pixels = neopixel.NeoPixel(board.D18, NUM_LEDS)

blue = 0,0,255
black = (0,0,0)
# possibly have dictionary that will hold the names of the functions and whenever the user selects a function, use the dictionary to find the right one and call it

def color_fill(color):
    print(color)
    if("#" in color):                           #check if this is a hex number or not. if it is, convert it to an RGB value
        c = ImageColor.getcolor(color, "RGB")
        print(c)
        pixels.fill(c)
    else:
        pixels.fill(color)

def color_wipe(color, reverse = False):
    # c = ImageColor.getcolor(color, "RGB") #uncomment this if passing in a hex value
    color_fill(black)

    if(reverse):
        print(f"Reverse Color wipe: {color}")
        for i in range(NUM_LEDS-1, 0, -1):      #technically counting down from 299, not 300 
            pixels[i] = color
    else:
        print(f"Color wipe: {color}")
        for i in range(0, NUM_LEDS):
            pixels[i] = color

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