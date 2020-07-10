from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import math
import matplotlib.pyplot as plt
import Globals
import cv2
from PIL import Image, ImageEnhance, ImageOps

# Label file helpers ---------------------------------------------------------------#
def filter_labels_for_animal_group(label_list, animal_id=[0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
    filtered_list = []

    for entry in label_list:
        for animal in entry['animals']:
            if animal_id == animal['group']:
                filtered_list.append(entry)
                break
    return filtered_list


# image helpers --------------------------------------------------------------------#
def loadImage(fname, equalize=True):
    "Loads an image as a h*w*3 numpy array"
    
    # load image in PIL format (either first equalized or not)
    img = np.asarray(Image.fromarray(equalizeImage(fname))) if equalize else img_to_array(load_img(fname), dtype="uint8")
    
    #print(f"image before {img.shape}")
    rest_x, rest_y = img.shape[0]%32, img.shape[1]%32
    if rest_x != 0:
        img = np.pad(img, ((0,32-rest_x),(0, 0),(0,0)), 'constant', constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, 32-rest_y),(0,0)), 'constant', constant_values=0)
       
    return img

# Load the first image an d get the shape of that: All images have the same size
def shapeOfFilename(fname):
    "Returns the imageshape of fname (filename)."
    imageShape = loadImage(fname)
    return imageShape.shape

# todo head and tail are switched!!
# def showImageWithAnnotation(entry):
#     "Shows image with filename entry[0] and annotated crosses entry[1] (list of dict with 'x', 'y')"
#     image = loadImage(entry['filename'])
#     plt.imshow(image)
#     x_front = [animal["position"][0] for animal in entry['animals'] if animal['group'].index(1)%2==0]   # the even group entries encode the front of an animal
#     y_front = [animal["position"][1] for animal in entry['animals'] if animal['group'].index(1)%2==0]   
    
#     x_back = [animal["position"][0] for animal in entry['animals'] if animal['group'].index(1)%2!=0]    # the odd group entries encode the back of an animal
#     y_back = [animal["position"][1] for animal in entry['animals'] if animal['group'].index(1)%2!=0]
#     plt.scatter (x_front, y_front, marker="o", c="w")
#     plt.scatter (x_back, y_back, marker="x", c="b")
#     plt.show()

def entropy(x):
    '''Returns the average entropy of the probability distributions in x. The last axis of x
    is assumed to represent the different events with their probabilities. Over this axis the
    entropy is computed, all other axes create just a multitude of such distributions and over
    these axes the average is taken. If the last axis has dimension 1 this is assumed to be
    a binary crossentropy.'''
    tmp = x
    if tmp.shape[-1]==1: # If only one channel we view it as distribution on a binary values
        tmp = np.concatenate((tmp, 1-tmp),axis=-1)
    xlogx = -tmp*np.log(np.maximum(tmp, np.finfo(tmp.dtype).eps))
    return np.average(np.sum(xlogx,axis=-1))




# def showImageWithHeatmap (image, hm=None, gt=None, filename=None):
#     """Shows image, the annotation by a heatmap hm [0..1] and the groundTruth gt. 
#      The hm.shape must be an integer fraction of the image shape. gt must 
#      have be a list of dicts with 'x' and 'y' entries as in the dataset. 
#      Both hm and gt can be None in which case they are skipped. 
#      If filename is given, the plot is saved."""
#     if hm is not None:
#         factor = image.shape[0]//hm.shape[0]
#         assert hm.shape[0]*factor==image.shape[0] and hm.shape[1]*factor==image.shape[1]
#         assert len(hm.shape)==3
#         hmResized = np.repeat (hm, factor, axis=0) # y
#         hmResized = np.repeat (hmResized, factor, axis=1) #x
#         hmResized = np.repeat (hmResized, 3, axis=2) # factor for RGB
#         hmResized = np.clip (hmResized*2, 0, 1)
        
#         #print(f"hm resized {hmResized.shape}\nimage {image.shape}\nfactor {factor}")
#         if image.dtype =="uint8":
#             image = image//2 + (128*hmResized).astype(np.uint8)
#         else:
#             image = ((image+1)*64 + 128*hmResized).astype(np.uint8)
#     plt.imshow(image)
#     if gt is not None:
#         print("gt is not none")
#         x = [label["x"] for label in gt]
#         y = [label["y"] for label in gt]
#         plt.scatter (x, y, marker="x", c="b")
#     if filename is not None:
#         plt.savefig(filename, dpi=150, bbox_inches='tight')
#     plt.show()

def equalizeImage(img_path):
    image = cv2.imread(img_path)

    # convert image from RGB to HSV
    img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    
    # Histogram equalisation on the V-channel
    #img_hsv[:, :, 2] = cv2.equalizeHist(img_hsv[:, :, 2])
    
    # contrast limited adaptive histogram equalization (clahe)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(20,20))
    img_hsv[:, :, 2] = clahe.apply(img_hsv[:, :, 2])
        
    # convert image back from HSV to RGB
    image = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
        
    # flip BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    return image

def adaptBrigthness(image, factor=1):
    # convert to PIL format
    img = Image.fromarray(image)
    
    # adapt brigthness
    enhancer = ImageEnhance.Brightness(img)
    im_output = enhancer.enhance(factor)
    
    # convert back to np.array
    return np.asarray(im_output)

# factor < 1 -> decrease contrast
# facotr > 1 -> increase contrast
def adaptContrast(image, factor=1, auto=False):
    # convert to PIL format
    img = Image.fromarray(image)
    
    # adapt contrast
    if auto:
        im_output = ImageOps.autocontrast(img)
    else:
        enhancer = ImageEnhance.Contrast(img)
        im_output = enhancer.enhance(factor)
    
    # convert back to np.array
    return np.asarray(im_output)

def equalizePil(image):
    # convert to PIL format
    img = Image.fromarray(image)
    
    # equalize
    im_output = ImageOps.equalize(img)
    
    # convert back to np.array
    return np.asarray(im_output)


# heatmap helpers ------------------------------------------------------------------#
# use this to test whether interpolate works
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

def downsample (T, factor=32):
  """T must be a tensor with at least 3 dimension, where the last three are interpreted as height, width, channels.
     Downsamples the height and width dimension of T by the given factor. 
     The length in these dimensions must be a multiple of factor."""
  sh = T.shape
  assert sh[-3]%factor==0
  assert sh[-2]%factor==0
  newSh = sh[:-3] + (sh[-3]//factor, factor) + (sh[-2]//factor, factor) + sh[-1:]
  return T.reshape(newSh).mean(axis=(-4, -2))

# nned to calcualte heatmap anyway, so this funtcion is not very useful
def showImageWithHeatmap (image, hm=None, gt=None, group=1, bodyPart="front", filename=None, exaggerate=1):
    """Shows image, the annotation by a heatmap hm [0..1] and the groundTruth gt. 
      The hm.shape must be an integer fraction of the image shape. gt must 
      have be a list of dicts with 'x' and 'y' entries as in the dataset. 
      Both hm and gt can be None in which case they are skipped. 
      If filename is given, the plot is saved."""
    assert bodyPart == "front" or bodyPart == "back" or bodyPart == "both"
    assert group in range(Globals.NUM_GROUPS)
    
    # copy image (so the heatmap is not drawn on original)
    img = image.copy()
       
    if hm is not None:
 
        factor = img.shape[0]//hm.shape[0]

        assert hm.shape[0]*factor==img.shape[0] and hm.shape[1]*factor==img.shape[1]
        assert len(hm.shape)==3
        
        hmResized = np.repeat (hm, factor, axis=0) # y
        hmResized = np.repeat (hmResized, factor, axis=1) #x
        hmResized = np.repeat (hmResized, 3, axis=2) # factor for RGB
        hmResized = np.clip (hmResized*2, 0, 1)
        
        if img.dtype =="uint8":
            img = img//2 + (128*exaggerate*hmResized).astype(np.uint8)
        else:
            img = ((img+1)*64 + 128*exaggerate*hmResized).astype(np.uint8)
    plt.imshow(img)
    
    if gt is not None:               
        if bodyPart=='both':
            group_array_front = np.zeros(Globals.channels())
            group_array_front[group*2] = 1
            group_array_back = np.zeros(Globals.channels)
            group_array_back[group*2+1] = 1
            
            x_front = [animal['position'][0] for animal in gt if np.array_equal(animal['group'], group_array_front)] 
            y_front = [animal['position'][1] for animal in gt if np.array_equal(animal['group'], group_array_front)]
            
            x_back = [animal['position'][0] for animal in gt if np.array_equal(animal['group'], group_array_back)]
            y_back = [animal['position'][1] for animal in gt if np.array_equal(animal['group'], group_array_back)]
         

            plt.scatter(x_front, y_front, marker='o', c='b',)
            plt.scatter(x_back, y_back, marker='x', c='b',)
            #plt.legend(loc='upper left')
            #plt.show()
         
        else:
            group_array = np.zeros(Globals.channels)
            if bodyPart=='front':
                group_array[group*2-1] = 1 
            elif bodyPart=='back':
                group_array[group*2] = 1 
                
            x = [animal['position'][0] for animal in gt if np.array_equal(animal['group'], group_array) ]
            y = [animal['position'][1] for animal in gt if np.array_equal(animal['group'], group_array)]
            
            marker = "o" if bodyPart == "front" else "x"
            plt.scatter (x, y, marker=marker, c="b")
        
    if filename is not None:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()


def showOverlappingHeatmaps(**heatmaps):
    if heatmaps != None:
        
        final_hm = np.zeros(shape=heatmaps[0].shape)    
        final_hm = sum(heatmaps)/len(heatmaps)
          
        return final_hm