import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 300)

def color_fill(rgb):
    print(f"Fill color: {rgb}")
    pixels.fill(rgb)

