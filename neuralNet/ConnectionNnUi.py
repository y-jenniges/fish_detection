import os
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
from skimage.feature import peak_local_max
from skimage.transform import resize
import matplotlib.cm as cm

def loadNn(path):
    if os.path.isfile(path):
        return tf.keras.models.load_model(path)
    else:
        return None

def loadImage(fname, factor=64):
    "Loads an image as a h*w*3 numpy array in [-1, 1]"

    img = img_to_array(load_img(fname), dtype="uint8")
    
    # if image is still large, downscale it by 25%
    #from PIL import Image, ImageEnhance, ImageOps
    #from skimage.transform import resize
    if img.shape[0] > 2500:
        img = resize(img, (img.shape[0]*0.25, img.shape[1]*0.25))

    print(f"image before {img.shape}")
    rest_x, rest_y = img.shape[0]%factor, img.shape[1]%factor
    if rest_x != 0:
        img = np.pad(img, ((0,factor-rest_x),(0, 0),(0,0)), 'constant', 
                     constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, factor-rest_y),(0,0)), 'constant', 
                     constant_values=0)
       
    # image needs to be in [-1,1]
    img = np.asarray(img)
    img = 2.*img/np.max(img) - 1
    print(f"image after {img.shape}")
    return img

def applyNnToImage(model, image):
    # predicted heatmap
    X = np.expand_dims(image, axis=0)
    yHat = model.predict(X)
    return yHat

def applyThresholdToHm(image, threshold=50):
    img_thr = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO)[1]
    return img_thr

def nonMaxSuppression(image, min_distance=20):
    coordinates = peak_local_max(image, min_distance=min_distance)
    return coordinates
    
def resizeHm(img, hm):
    factor = img.shape[0]//hm.shape[0]
    
    hmResized = np.repeat (hm, factor, axis=0) # y
    hmResized = np.repeat (hmResized, factor, axis=1) #x
    hmResized = np.clip (hmResized*2, 0, 1)
    hmResized = hmResized[:, :, np.newaxis]
        
    # print(f"hmresized shape {hmResized.shape}")
    # if img.dtype =="uint8":
    #     img = img//2 + (128*exaggerate*hmResized).astype(np.uint8)
    # else:
    #     img = ((img+1)*64 + 128*exaggerate*hmResized).astype(np.uint8)
    #plt.imshow(hmResized)

def findCoordinates(heatmap):
    thr = applyThresholdToHm(heatmap, 50)
    coordinates = nonMaxSuppression(thr, 20)
    
    # remove coordinates whose x and y are closer than 5px
    df = pd.DataFrame(coordinates)
    df = df.sort_values(0, ignore_index=True)
    
    final_coords = []
    final_coords.append(df.iloc[0])  
    for i in range(1, len(df)):
        if abs(df.iloc[i][0] - df.iloc[i-1][0]) > 5 \
        or abs(df.iloc[i][1] - df.iloc[i-1][1]) > 5:
             final_coords.append(df.iloc[i])  
             
    final_coords = pd.DataFrame(final_coords).to_numpy()
    
    return final_coords

def matchHeadsAndTails():
    pass

def exportAnimalsToCsv():
    pass

model_path = "../data/output/36/model-H"
#modelPath = "../data/output/59/model-L"
#modelPath = "../data/output/48/model-L" # trained on all animals, coordiantes dont work

print("load model...")
model = loadNn(model_path)


img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/60.jpg"
img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/39.jpg"
img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/51.jpg"
#imgPath = "G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images/Rectified_TN_Exif_Remos1_2015.08.02_01.00.49_L.jpg"

print("load image")
image = loadImage(img_path, factor=32)

print("model loaded. predicting...")
prediction = applyNnToImage(model, image)

print("prediction done")

#heads = prediction[0][0,:,:,0]*255
heads = prediction[0,:,:,0]*255
heads = heads.astype('uint8')

# get coordinates
coordinates = findCoordinates(heads)

# show prediction heatmap and coordinates
plt.imshow(heads, cmap=plt.cm.gray)
plt.autoscale(False)
plt.plot(coordinates[:, 1], coordinates[:, 0], 'r.')
plt.show()

# print("load model for connections...")
# image_c = loadImage(img_path, factor=64)
# model_c = loadNn("../data/output/59/model-L")
# prediction_c = applyNnToImage(model_c, image_c)

# # load head and tail vector fields and amplify them
# head_vector_field = prediction_c[1][0, :, :, :2]
# tail_vector_field = prediction_c[1][0, :, :, 2:]

def findTail(head, tails):
    # tails needs to be numpy array
    
    # calculate y distances 
    deltay = abs(np.array(tails)[:,0] - head[0])
    deltax = abs(np.array(tails)[:,1] - head[1])
    
    weighted_delta = weightedDistanceSquared(deltay, deltax)
    
    min_index = np.argmin(weighted_delta)

    return np.array(tails[min_index])
    
def weightedDistanceSquared(x, y):
    a = 1
    b = 2 #more distance in y direction is double as bad as in x-driection
    return a*x*x + b*y*y

# get gt
import HelperFunctions as helpers
import itertools

#helpers.show_image_with_vectors(image_c, head_vector_field, 10000)

label_root = "../data/maritime_dataset_25/labels/"
test_labels, train_labels_animals, train_labels_no_animals, val_labels, class_weights = helpers.loadAndSplitLabels(label_root)

fish_heads = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
fish_tails = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
gt = [entry for entry in test_labels if entry["filename"] == img_path][0]
gt_heads = np.array([np.array(animal["position"]) for animal in gt["animals"] if np.array_equal(animal["group"], fish_heads)])
gt_tails = np.array([np.array(animal["position"]) for animal in gt["animals"] if np.array_equal(animal["group"], fish_tails)])



matches = []
tails = gt_tails.copy()
for head in coordinates:
    if len(tails) > 0:
        head_point = np.array([head[1], head[0]])
        tail = findTail(head_point, tails)
        #tails = np.array([x for x in tails if not np.array_equal(x, tail)])
        print(tails)
        matches.append([head_point, tail])
    
matches = np.array(matches)

# # plot all matches
# plt.imshow(heads, cmap=plt.cm.gray)
# #plt.autoscale(False)
# plt.scatter(matches[:,:,0], matches[:,:,1])
# plt.show()


# show groundtruth
helpers.showImageWithHeatmap(image, None, gt["animals"], 1, "both")


# plot each match with a different colour
colors = cm.rainbow(np.linspace(0, 1, matches.shape[0]))
plt.imshow(heads, cmap=plt.cm.gray)
for i in range(matches.shape[0]):
    plt.scatter(matches[i,:,0], matches[i,:,1], color=colors[i])
plt.show()

# #@todo only go untip 400 px in original format? recursion
# def find_similar_neighbours(vector_pos, vector_orient, neighbour_indices, tail_projections, vector_field):   
#     #max deviation of 30% from original orientation
#     max_deviation = 15
    
    
#     # check if there is a tail somewhere @todo or head (depends on iteration)
#     print(f"vector position {vector_pos}")
#     if vector_pos.tolist() in tail_projections.tolist():
#         print(f"Found a matching tail at position (on vector field grid): {vector_pos}")
#         return vector_pos
#     else:
#         if neighbour_indices is not None and len(neighbour_indices) > 0:
#             new_vec_pos = np.array(neighbour_indices[0], dtype=np.int64)
#             new_vec_ori = np.array(vector_field[new_vec_pos[0], new_vec_pos[1], :])
#             print(f"new_vec_pos and ori {new_vec_pos, new_vec_ori}")
                        
#             # determine neighbour range
#             x_start = new_vec_pos[0]-1 if new_vec_pos[0]-1 >= 0 else 0
#             x_end = new_vec_pos[0]+2 if new_vec_pos[0]+2 <=  vector_field.shape[0] else vector_field.shape[0]
            
#             y_start = new_vec_pos[1]-1 if new_vec_pos[1]-1 >= 0 else 0
#             y_end = new_vec_pos[1]+2 if new_vec_pos[1]+2 <=  vector_field.shape[1] else vector_field.shape[1]
            
#             x = range(x_start, x_end)
#             y = range(y_start, y_end)
#             new_neighbours = []
#             for i in x:
#                 for j in y:
#                     if i != new_vec_pos[0] or j != new_vec_pos[1]:
#                         new_neighbours.append([i,j])
            
#             print(new_neighbours)
#             # do not check neighbours that have already been checked
#             new_neighbours = [x for x in new_neighbours if x not in neighbour_indices]
#             #new_neighbours = new_neighbours[new_neighbours != neighbour_indices][0]
            
#             print("new neighbours")
#             print(new_neighbours)
            
#             deviation = new_vec_ori*max_deviation
            
#             # filter the new neighbours for only those with similar orientation
#             final_neighbours = []
#             for n in new_neighbours:
#                 orientation = np.array(vector_field[n[0], n[1], :])
                
#                 lower_thresh_x = new_vec_ori[0] - deviation[0] if new_vec_ori[0] > 0 else new_vec_ori[0] + deviation[0]
#                 upper_thresh_x = new_vec_ori[0] + deviation[0] if new_vec_ori[0] > 0 else new_vec_ori[0] - deviation[0]
#                 lower_thresh_y = new_vec_ori[1] - deviation[1] if new_vec_ori[1] > 0 else new_vec_ori[1] + deviation[1]
#                 upper_thresh_y = new_vec_ori[1] + deviation[1] if new_vec_ori[1] > 0 else new_vec_ori[1] - deviation[1]
                
#                 if lower_thresh_x <= orientation[0] <= upper_thresh_x \
#                 and lower_thresh_y <= orientation[1] <= upper_thresh_y:
#                     final_neighbours.append(n)
                    
#             print("final neighbours")
#             print(final_neighbours)
            
#             tail_pos_projection = find_similar_neighbours(new_vec_pos, 
#                                                           new_vec_ori, 
#                                                           final_neighbours, 
#                                                           tail_projections, 
#                                                           vector_field)
        
#             return tail_pos_projection
#         return None
    
# # get shorter list (we are only looking for complete animals)
# if len(heads) <= len(tails):
#     factor = head_vector_field.shape[1]/image.shape[1]
#     tail_projections = np.around(np.array(tails)*factor).astype(np.int64)
    
#     for i in range(len(heads)):
#         # find position and orientation of nearest vector      
#         head_projection= np.around(np.array(heads[i])*factor).astype(np.int64) # on smaller grid image
        
#         nearest_vec_pos = head_projection.copy().astype(np.int64)
#         nearest_vec_ori = head_vector_field[head_projection[0], head_projection[1], :]
        
#         #grid = head_vector_field[:,:,1]
#         x = range(nearest_vec_pos[0]-1, nearest_vec_pos[0]+2)
#         y = range(nearest_vec_pos[1]-1, nearest_vec_pos[1]+2)
#         neighbours = []
#         for i in x:
#             for j in y:
#                 if i != nearest_vec_pos[0] or j != nearest_vec_pos[1]:
#                     neighbours.append([i,j])
                
#         print(neighbours)
    
#         # find similar vectors (in position and orientation)
#         # tail_pos_projection = find_similar_neighbours(nearest_vec_pos, 
#         #                                               nearest_vec_ori, 
#         #                                               neighbours, tail_projections, 
#         #                                               head_vector_field)
        
#         # find tail position in original coordinates
        
# else:
#     for i in range(len(tails)):
#         pass

# import numpy as np
# import scipy
# import scipy.ndimage as ndimage
# import scipy.ndimage.filters as filters
# import matplotlib.pyplot as plt

# #fname = '/tmp/slice0000.png'
# neighborhood_size = 5
# threshold = 1500

# #data = scipy.misc.imread(fname)
# data = image

# data_max = filters.maximum_filter(data, neighborhood_size)
# maxima = (data == data_max)
# data_min = filters.minimum_filter(data, neighborhood_size)
# diff = ((data_max - data_min) > threshold)
# maxima[diff == 0] = 0

# labeled, num_objects = ndimage.label(maxima)
# slices = ndimage.find_objects(labeled)
# x, y = [], []
# for dy,dx in slices:
#     x_center = (dx.start + dx.stop - 1)/2
#     x.append(x_center)
#     y_center = (dy.start + dy.stop - 1)/2    
#     y.append(y_center)

# plt.imshow(data)
# #plt.savefig('/tmp/data.png', bbox_inches = 'tight')

# plt.autoscale(False)
# plt.plot(x,y, 'ro')
# #plt.savefig('/tmp/result.png', bbox_inches = 'tight')




# pred_fish_head = prediction[0, :, :]#, 0]
# #pred_fish_head = pred_fish_head[:, :, np.newaxis]
# # convert hm range [0,1] to [0,255]
# pred_fish_head = pred_fish_head*255.0
# #plt.imshow(pred_fish_head)

# #pred_fish_head = resizeHm(image, pred_fish_head)

# image_thr = applyThresholdToHm(pred_fish_head)
# coordinates = nonMaxSuppression(image_thr, 10)

# plt.imshow(pred_fish_head, cmap=plt.cm.gray)
# plt.autoscale(False)
# plt.plot(coordinates[:, 1], coordinates[:, 0], 'r.')


# # coordinates on non-rectified images
# # default for status: not checked
# # default for manually corrected: no
# columns = ["file_id", "object_remarks", 
#            "group", "species", 
#            "LX1", "LY1",
#            "LX2", "LY2", 
#            "LX3", "LY3", 
#            "LX4", "LY4", 
#            "RX1", "RY1",
#            "RX2", "RY2", 
#            "RX3", "RY3", 
#            "RX4", "RY4", 
#            "length", "height", "image_remark",
#            "status", "manually_corrected"
#             ]

# # send an "image written" event to the main thread