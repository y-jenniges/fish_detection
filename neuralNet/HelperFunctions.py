from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import math
import matplotlib.pyplot as plt
import Globals


# Image helpers --------------------------------------------------------------------#
def loadImage(fname):
    "Loads an image as a h*w*3 numpy array"
    img =  img_to_array(load_img(fname), dtype="uint8")
    
    #print(f"image before {img.shape}")
    rest_x, rest_y = img.shape[0]%32, img.shape[1]%32
    if rest_x != 0:
        img = np.pad(img, ((0,rest_x),(0, 0),(0,0)), 'constant', constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, rest_y),(0,0)), 'constant', constant_values=0)
        
    return img

# Load the first image an d get the shape of that: All images have the same size
def shapeOfFilename(fname):
    "Returns the imageshape of fname (filename)."
    imageShape = loadImage(fname)
    return imageShape.shape

def showImageWithAnnotation(entry):
    "Shows image with filename entry[0] and annotated crosses entry[1] (list of dict with 'x', 'y')"
    image = loadImage(entry['filename'])
    plt.imshow(image)
    x_front = [animal["front"][0] for animal in entry['animals']]
    y_front = [animal["front"][1] for animal in entry['animals']]
    x_back = [animal["back"][0] for animal in entry['animals']]
    y_back = [animal["back"][1] for animal in entry['animals']]
    plt.scatter (x_front, y_front, marker="o", c="w")
    plt.scatter (x_back, y_back, marker="x", c="b")
    plt.show()

def showOverlappingHeatmaps(**heatmaps):
    for h in heatmaps:
        print("hbsd")

# Heatmap helpers ------------------------------------------------------------------#
# Use this to test whether interpolate works
def showInterpolate():
    "Helper function to check that interpolate works"
    x = np.arange(0,4,0.02)
    xInt = [interpolate(myX)[0] for myX in x]
    if not type(xInt[0]) is int:
        raise TypeError(f"First result of interpolate must be int but is {xInt[0]}")
    alpha = [interpolate(myX)[1] for myX in x]
    plt.figure(figsize=(6,2))
    plt.plot (x, xInt, 'r', label='xInt')
    plt.plot (x, alpha, 'b', label='alpha')
    plt.legend()
    plt.show ()

def interpolate (x):
    """Returns an interpolation (xInt, alpha) that distributes a 1 between
    xInt and xInt+1, where xInt<=x<xInt+1 such that alpha goes into
    xInt and (1-alpha) into xInt+1. It does this in a way that is linear
    in x and where for an integer x, xInt=x."""
    xInt = math.floor(x)
    return (xInt, 1-(x-xInt))

def gaussian (sigma, dim):
    """Returns a dim*dim*1 array with a not normalized 
    Gaussian centered at dim//2, dim//2
    with peak value 1 and the given sigma."""
    x,y,z = np.mgrid[0:dim,0:dim,0:1]
    cx=dim//2
    cy=dim//2
    return np.exp(-((x-cx)**2+(y-cy)**2)/(2*sigma**2))