#!/usr/bin/python

from PIL import Image, ImageDraw
import math, colorsys

dimensions = (1200, 1000)
dim_prev = (200,200)
center = (0.6, .75)       # Use this for Mandelbrot set
#center = (1.5, 1.5)       # Use this for Julia set
iterate_preview = 100
iterate_max = 250
colors_max = 1000

img = Image.new("RGB", dimensions)
prev_img = Image.new("RGB", dim_prev)
d_prev = ImageDraw.Draw(prev_img)

d = ImageDraw.Draw(img)

# Calculate a tolerable palette
palette = [0] * colors_max
for i in xrange(colors_max):
    f = 1-abs((float(i)/colors_max-1)**15)
    r, g, b = colorsys.hsv_to_rgb(.76+f/2.5, 1-f/2, f)
    palette[i] = (int(r*255), int(g*255), int(b*255))

def cpolynomial(z,c):
    return cfour*z**4 + cthree*z**3 + ctwo*z**2 + cone*z + c

cfour = .8
cthree = .1
ctwo = .85
cone = 0

# Calculate the mandelbrot sequence for the point c with start value z
def iterate(c, iter_num, z = 0):
    for n in xrange(iter_num + 1):
        z = cpolynomial(z,c)
        if abs(z) > 2:
            return n
    return None

# Draw our image

def generate_fractal(d, dim, iter_num):
    i = 0
    scale = 0.1/(dim[0]/3)
    for y in xrange(dim[1]):
        for x in xrange(dim[0]):
            c = complex(x * scale - center[0], y * scale - center[1])

            n = iterate(c, iter_num)            # Use this for Mandelbrot set
            #n = iterate_mandelbrot(complex(0.3, 0.6), c)  # Use this for Julia set

            if n is None:
                v = 1
            else:
                v = n/(1.0*iter_num)

            d.point((x, y), fill = palette[int(v * (colors_max-1))])
        if y*1.0/dim[1] > i:
            print str("{0:.2g}".format(y*1.0/dim[1]))+" of pixels done."
            i += .05
    return d

d_prev = generate_fractal(d_prev, dim_prev, iterate_preview)
prev_img.show()
d = generate_fractal(d, dimensions, iterate_max)

del d
del d_prev
img.save("fractal_"+str(cfour)+"_"+str(cthree)+"_"+str(ctwo)+"_"+str(cone)+".png")
img.show()
prev_img.close()
