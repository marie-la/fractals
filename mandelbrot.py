from PIL import Image, ImageDraw
import math, colorsys

dim = (800, 800)
scale = 1.0/(dim[0]/3)
center = (2.2, 1.5)       # Use this for Mandelbrot set
#center = (1.5, 1.5)       # Use this for Julia set
iterate_max = 100
colors_max = 50

img = Image.new("RGB", dim)
d = ImageDraw.Draw(img)

# Calculate a tolerable palette
palette = [0] * colors_max
for i in xrange(colors_max):
    f = 1-abs((float(i)/colors_max-1)**15)
    r, g, b = colorsys.hsv_to_rgb(.66+f/3, 1-f/2, f)
    palette[i] = (int(r*255), int(g*255), int(b*255))

def mandelbrot(c):
    z = 0
    for n in range(iterate_max + 1):
        z = z**3 + c
        if abs(z) > 2:
            return n
    return None

for x in range(dim[0]):
    for y in range(dim[1]):
        c = complex(x * scale - center[0], y * scale - center[1])

        n = mandelbrot(c)

        if n is None:
            v = 1
        else:
            v = n/100.0

        d.point((x,y), fill = palette[int(v * (colors_max-1))])
del d
img.show()
