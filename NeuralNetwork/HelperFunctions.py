from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import math
import matplotlib.pyplot as plt
import Globals
import cv2
import os
import json
from PIL import Image, ImageEnhance, ImageOps
"""
Module contains helper functions for label and image loading, visualization
options for heatmaps and vector fields. Also relevant functions for heatmap
and vector field calculations are present.
Some functions are taken from lecture "Anwendungen der Bildverarbeitung" 
by Udo Frese, University Bremen, 2019
"""

# Label file helpers ---------------------------------------------------------#
def filter_labels_for_animal_group(label_list, 
                                   animal_id=[0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
    """
    Filters the labels for entries that contain the given animal group 
    (in one-hot encoding).

    Parameters
    ----------
    label_list : list of dicts (keys: filename, animals)
        List of labels to filter.
    animal_id : list of int, optional
        One-hot encoded animal group. The default is 
        [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], i.e. fish heads.

    Returns
    -------
    filtered_list : list of dicts (keys: filename, animals)
        Filtered label list.
    """
    filtered_list = []

    for entry in label_list:
        for animal in entry['animals']:
            if animal_id == animal['group']:
                filtered_list.append(entry)
                break
    return filtered_list

def loadAndSplitLabels(label_root="../data/maritime_dataset_25/labels/"):
    """
    Loads labels and generates class weights. 

    Parameters
    ----------
    label_root : str, optional
        Path to label file folder. The default is "../data/maritime_dataset_25/labels/".

    Returns
    -------
    all_test_labels : list of dicts (keys: filename, animals)
        List of test labels.
    train_labels_animals : list of dicts (keys: filename, animals)
        Loaded training labels with animals.
    train_labels_no_animals : list of dicts (keys: filename, animals)
        Loaded training labels without animals.
    validation_labels : list of dicts (keys: filename, animals)
        Loaded validation labels.
    class_weights : dict (one key per class)
        Weights for every class.
    """
    label_path = "training_labels_animals.json"
    with open(os.path.join(label_root, label_path) , 'r') as f:
        train_labels_animals = json.load(f)
        
    label_path = "test_labels.json"
    with open(os.path.join(label_root, label_path), 'r') as f:
        all_test_labels = json.load(f)
        
    label_path = "training_labels_no_animals.json"
    with open(os.path.join(label_root, label_path), 'r') as f:
        train_labels_no_animals = json.load(f)
        
    label_path = "validation_labels.json"
    with open(os.path.join(label_root, label_path), 'r') as f:
        validation_labels = json.load(f)
    
    # filter train labels for each group
    fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    train_fish_labels = filter_labels_for_animal_group(train_labels_animals, fish_id)

    crust_id =          [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    train_crust_labels = filter_labels_for_animal_group(train_labels_animals, crust_id)
  
    chaetognatha_id =   [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    train_chaeto_labels = filter_labels_for_animal_group(train_labels_animals, chaetognatha_id)
   
    unidentified_id =   [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]  
    train_unidentified_labels = filter_labels_for_animal_group(train_labels_animals, unidentified_id)

    jellyfish_id =      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    train_jellyfish_labels = filter_labels_for_animal_group(train_labels_animals, jellyfish_id)
    
    # calculating class weight accroding to the number of available data (num images)
    max_class_length = max(len(train_fish_labels), len(train_crust_labels), len(train_chaeto_labels), len(train_unidentified_labels), len(train_jellyfish_labels))  
    weight_fish =  max_class_length/len(train_fish_labels)
    weight_crust = max_class_length/len(train_crust_labels)
    weight_chaeto = max_class_length/len(train_chaeto_labels)
    weight_unid = max_class_length/len(train_unidentified_labels)
    weight_jelly = max_class_length/len(train_jellyfish_labels)
    class_weights = {0: 1, 1:weight_fish, 2:weight_fish, 
                      3: weight_crust, 4: weight_crust, 
                      5: weight_chaeto, 6: weight_chaeto, 
                      7: weight_unid, 8: weight_unid, 
                      9: weight_jelly, 10:weight_jelly}
     
    return all_test_labels, train_labels_animals, train_labels_no_animals, validation_labels, class_weights

# image helpers --------------------------------------------------------------------#
def loadImage(fname, factor=64, pad=True):
    """Loads an image as a h*w*3 numpy array"""
    # load image in PIL format (either first equalized or not)
    img = img_to_array(load_img(fname), dtype="uint8")

    if pad:
        #print(f"image before {img.shape}")
        rest_x, rest_y = img.shape[0]%factor, img.shape[1]%factor
        if rest_x != 0:
            img = np.pad(img, ((0,factor-rest_x),(0, 0),(0,0)), 'constant', constant_values=0)
        if rest_y != 0:        
            img = np.pad(img, ((0,0),(0, factor-rest_y),(0,0)), 'constant', constant_values=0)
    else:
        img = img_to_array(load_img(fname), dtype="uint8")
        
    return img

# Load the first image an d get the shape of that: All images have the same size
def shapeOfFilename(fname, downsample_factor=2, image_factor=32):
    """Returns the imageshape of fname (filename) downsampled by 
    downsample_factor. and padded using image_factor. """
    imageShape = downsample(loadImage(fname, image_factor),downsample_factor)
    return imageShape.shape

def entropy(x):
    """Returns the average entropy of the probability distributions in x. The last axis of x
    is assumed to represent the different events with their probabilities. Over this axis the
    entropy is computed, all other axes create just a multitude of such distributions and over
    these axes the average is taken. If the last axis has dimension 1 this is assumed to be
    a binary crossentropy."""
    tmp = x
    if tmp.shape[-1]==1: # If only one channel we view it as distribution on a binary values
        tmp = np.concatenate((tmp, 1-tmp),axis=-1)
    xlogx = -tmp*np.log(np.maximum(tmp, np.finfo(tmp.dtype).eps))
    return np.average(np.sum(xlogx,axis=-1))

# heatmap helpers ------------------------------------------------------------#
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
  """T must be a tensor with at least 3 dimension, where the last three are 
  interpreted as height, width, channels. Downsamples the height and width 
  dimension of T by the given factor. The length in these dimensions must be 
  a multiple of factor."""
  sh = T.shape
  assert sh[-3]%factor==0
  assert sh[-2]%factor==0
  newSh = sh[:-3] + (sh[-3]//factor, factor) + (sh[-2]//factor, factor) + sh[-1:]
  return T.reshape(newSh).mean(axis=(-4, -2))

def show_image_with_non_zero_vectors(image, vectors, vector_scale=200, filename=None, gt=None):
    # get directions of vectors 
    u = vectors[:,:,1]
    v = vectors[:,:,0]
    
    # get indices and values of non-zero entries in given vector field
    ui = np.nonzero(u)
    vi = np.nonzero(v)
    uz = u[ui]
    vz = v[vi]

    factor = 1
    if image is not None: 
        factor = image.shape[1]/vectors.shape[1]
        plt.imshow(image)

    plt.axis("off")
    
    if vz.shape == uz.shape:
        # display non-zero vectors
        for i in range(len(ui)):
            plt.quiver(ui[1]*factor, ui[0]*factor, 
                        vz*vector_scale, uz*vector_scale, 
                        color=["w"], width=1/250, 
                        angles='xy', scale_units='xy', scale=1)   
    else:
        print("vz and uz not equal shape")
        
    if gt is not None:
        for i in range(0, len(gt), 2):
            plt.scatter(gt[i]["position"][0], gt[i]["position"][1], s=20, marker='o', c='r')
            plt.scatter(gt[i+1]["position"][0], gt[i+1]["position"][1], s=20, marker='x', c='b')
    
    if filename is not None:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
    
    plt.show()
    
def show_image_with_all_vectors(image, vectors, vector_scale=200, image_factor=32, filename=None):
    # get directions of vectors 
    u = vectors[:,:,1]
    v = vectors[:,:,0]

    plt.imshow(image)
    vector_scale = vector_scale*image_factor
    #image_factor = 1
    # display all vectors
    #factor = image.shape[0]/vectors.shape[0] # factor to scale position of vectors
    
    for i in range(u.shape[0]):
        for j in range(u.shape[1]):
            plt.quiver(round(j*image_factor), round(i*image_factor), 
                        v[i, j]*vector_scale, u[i, j]*vector_scale, 
                        color=["r"], width=1/250, 
                        angles='xy', scale_units='xy', scale=1)   
        
    if filename is not None:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        
    plt.show()    
 
def show_image_with_vectors(image, vectors, vector_scale=200):
    plt.imshow(image)
    for i in range(vectors.shape[0]):
        for j in range(vectors.shape[1]):
            plt.quiver(j, i, 
                        vectors[i, j,0]*vector_scale, vectors[i, j,1]*vector_scale, 
                        color=["r"], width=1/250, 
                        angles='xy', scale_units='xy', scale=1)   
            
    plt.show()

def get_head_tail_vectors(entry, image_factor=32, vector_scale=200.0, downsample_factor=1):
    # factor: image scale
    # scale_factor:veector scale
    image = downsample(loadImage(entry["filename"], image_factor), downsample_factor)
    img_y, img_x = image.shape[0], image.shape[1]
    #print(image.shape)
    
    head_vectors = np.zeros((img_y, img_x, 2), dtype=np.float32)
    tail_vectors = np.zeros((img_y, img_x, 2), dtype=np.float32)
    
    # iterate over all animal heads
    for i in range(0, len(entry["animals"]), 2):
        # head coordinates
        x_head = round(entry["animals"][i]["position"][0]/downsample_factor)
        y_head = round(entry["animals"][i]["position"][1]/downsample_factor)
        
        # tail coordinates
        x_tail = round(entry["animals"][i+1]["position"][0]/downsample_factor)
        y_tail = round(entry["animals"][i+1]["position"][1]/downsample_factor)
        
        # vector pointing from head to tail
        head_dx = (x_tail - x_head)/vector_scale
        head_dy = (y_tail - y_head)/vector_scale

        # vector pointing from tail to head
        tail_dx = -1*head_dx
        tail_dy = -1*head_dy

        # add head and tail vector to vector field
        head_vectors[y_head, x_head] = np.array([head_dx, head_dy])
        tail_vectors[y_tail, x_tail] = np.array([tail_dx, tail_dy])
        
    return head_vectors, tail_vectors

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

        print(f"img, hm shape {image.shape, hm.shape}")

        assert hm.shape[0]*factor==img.shape[0] and hm.shape[1]*factor==img.shape[1]
        assert len(hm.shape)==3 or len(hm.shape) ==2
        
        if len(hm.shape) == 3:
            hmResized = np.repeat (hm, factor, axis=0) # y
            hmResized = np.repeat (hmResized, factor, axis=1) #x
            hmResized = np.repeat (hmResized, 3, axis=2) # factor for RGB
            hmResized = np.clip (hmResized*2, 0, 1)
        elif len(hm.shape) == 2:
            hmResized = np.repeat (hm, factor, axis=0) # y
            hmResized = np.repeat (hmResized, factor, axis=1) #x
            hmResized = np.clip (hmResized*2, 0, 1)
            hmResized = hmResized[:, :, np.newaxis]
        
        print(f"hmresized shape {hmResized.shape}")
        if img.dtype =="uint8":
            img = img//2 + (128*exaggerate*hmResized).astype(np.uint8)
        else:
            img = ((img+1)*64 + 128*exaggerate*hmResized).astype(np.uint8)
    plt.imshow(img)
    plt.axis("off")
    
    # draw groundtruth if it is available
    if gt is not None:            
        group_array = np.zeros(Globals.channels)
        if bodyPart=='front':
            group_array[group*2-1] = 1 
        elif bodyPart=='back' or bodyPart=='both':
            group_array[group*2] = 1     
        
        if bodyPart=='both':
            group_array_front = np.copy(group_array)
            group_array_front[np.argwhere(group_array==1)-1] = 1
            group_array_front[np.argwhere(group_array==1)] = 0

            x_front = [animal['position'][0] for animal in gt if np.array_equal(animal['group'], group_array_front)] 
            y_front = [animal['position'][1] for animal in gt if np.array_equal(animal['group'], group_array_front)]
            
            x_back = [animal['position'][0] for animal in gt if np.array_equal(animal['group'], group_array)]
            y_back = [animal['position'][1] for animal in gt if np.array_equal(animal['group'], group_array)]

            plt.scatter(x_front, y_front, s=20, marker='o', c='r')
            plt.scatter(x_back, y_back, s=20, marker='x', c='b')         
        else:
            x = [animal['position'][0] for animal in gt if np.array_equal(animal['group'], group_array) ]
            y = [animal['position'][1] for animal in gt if np.array_equal(animal['group'], group_array)]
            
            if bodyPart=='front':
                marker='o'
                color='r'
            else:
                marker='x'
                color='b'

            plt.scatter (x, y, s=20, marker=marker, c=color)

    if filename is not None:
        plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()

def sumHeatmaps(heatmaps):
    """ Sums a list of heatmaps up and clips it to range [0,1]. """
    if heatmaps != None:   
        final_hm = sum(heatmaps)
        final_hm = np.clip(final_hm, 0, 1)

        return final_hm
    else:
        return None
