import board
import neopixel
from PIL import ImageColor

NUM_LEDS = 300
pixels = neopixel.NeoPixel(board.D18, NUM_LEDS)

blue = 0,0,255
black = (0,0,0)
# add color variable...list or tuple? Then get the rgb values from color picker and set this equal to them
# possibly have dictionary that will hold the names of the functions and whenever the user selects a function, use the dictionary to find the right one and call it

def color_fill(color):
    print(ImageColor.getcolor(color, "RGB"))
    pixels.fill(ImageColor.getcolor(color, "RGB"))

def color_wipe(color):
    ImageColor.getcolor(color, "RGB")
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