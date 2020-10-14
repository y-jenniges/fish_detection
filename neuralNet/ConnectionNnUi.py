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
import HelperFunctions as helpers
#from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

def loadNn(path):
    if os.path.isfile(path):
        return tf.keras.models.load_model(path)
    else:
        return None

def loadImage(fname, factor=32, rescale_range=True):
    "Loads an image as a h*w*3 numpy array in [-1, 1]"

    img = img_to_array(load_img(fname), dtype="uint8")
    
    # if image is still large, downscale it by 25%
    #from PIL import Image, ImageEnhance, ImageOps
    #from skimage.transform import resize
    if img.shape[0] > 2500:
        img = resize(img, (img.shape[0]*0.25, img.shape[1]*0.25))

    rest_x, rest_y = img.shape[0]%factor, img.shape[1]%factor
    if rest_x != 0:
        img = np.pad(img, ((0,factor-rest_x),(0, 0),(0,0)), 'constant', 
                     constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, factor-rest_y),(0,0)), 'constant', 
                     constant_values=0)
       
    if rescale_range:
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
    
    # remove coordinates whose x and y are closer than 10px
    df = pd.DataFrame(coordinates)
    df = df.sort_values(0, ignore_index=True)
    

    final_coords = df.copy() 
    
    for i in range(len(df)):
        for j in range(i, len(df)):
            if abs(df.iloc[i][0] - df.iloc[j][0]) < 10 \
            and abs(df.iloc[i][1] - df.iloc[j][1]) < 10 \
            and i != j and j in final_coords.index:
                print(i,j)
                final_coords.drop(j, inplace=True)  
                
    # drop duplicates
    final_coords = pd.DataFrame(final_coords).drop_duplicates()
    
    # switch x and y
    final_coords = final_coords.reindex(columns=[1,0])
    
    final_coords = final_coords.to_numpy()
    
    return final_coords

def weightedEuclidean(x, y):
    a = 0.54 # put more weight on x-error
    b = 0.46 
    return np.sqrt(a*x*x + b*y*y)


def findHeadTailMatches(heads, tails):
    ht_distances = []
    
    # calculate distance from every head to every tail
    for i in range(len(heads)):
        if len(tails) > 0:
            head = heads[i]
            deltay = abs(np.array(tails)[:,0] - head[0])
            deltax = abs(np.array(tails)[:,1] - head[1])
        
            weighted_delta = weightedEuclidean(deltax, deltay)
            ht_distances.append(weighted_delta)
            
    # calculate matches minimizing the total distance
    ht_distances = np.array(ht_distances)
    _, assignment = linear_sum_assignment(ht_distances)
    
    matches = np.array([(heads[i], tails[assignment[i]]) for i in range(len(heads))])
    return matches 
    #return np.array(assignment)

def exportAnimalsToCsv():
    pass

model_path = "../data/output/36/model-H"
#modelPath = "../data/output/59/model-L"
#modelPath = "../data/output/48/model-L" # trained on all animals, coordiantes dont work

print("load model...")
model = loadNn(model_path)


img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/60.jpg"
#img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/39.jpg"
img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/51.jpg"
#imgPath = "G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images/Rectified_TN_Exif_Remos1_2015.08.02_01.00.49_L.jpg"

print("load image")
image = loadImage(img_path, factor=32)
img = loadImage(img_path, factor=32, rescale_range=False)
    

print("model loaded. predicting...")
prediction = applyNnToImage(model, image)

print("prediction done")

#heads = prediction[0][0,:,:,0]*255
heads = prediction[0,:,:,0]*255
heads = heads.astype('uint8')

# get coordinates
head_coordinates = findCoordinates(heads)

# show prediction heatmap and coordinates
plt.imshow(heads, cmap=plt.cm.gray)
plt.autoscale(False)
plt.plot(head_coordinates[:, 0], head_coordinates[:, 1], 'r.')
plt.show()


# get gt
label_root = "../data/maritime_dataset_25/labels/"
test_labels, train_labels_animals, train_labels_no_animals, val_labels, class_weights = helpers.loadAndSplitLabels(label_root)

fish_heads = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
fish_tails = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
gt = [entry for entry in test_labels if entry["filename"] == img_path][0]
gt_heads = np.array([np.array(animal["position"]) for animal in gt["animals"] if np.array_equal(animal["group"], fish_heads)])
gt_tails = np.array([np.array(animal["position"]) for animal in gt["animals"] if np.array_equal(animal["group"], fish_tails)])


#matches = findHeadTailMatches(head_coordinates, tail_coordinates)
matches = findHeadTailMatches(gt_heads, gt_tails)

# show groundtruth
helpers.showImageWithHeatmap(img, None, gt["animals"], 1, "both")


# plot each match with a different colour
colors = cm.rainbow(np.linspace(0, 1, matches.shape[0]))
plt.imshow(heads, cmap=plt.cm.gray)
plt.imshow(img)
for i in range(matches.shape[0]):
    plt.scatter(matches[i,:,0], matches[i,:,1], color=colors[i])
    plt.plot([matches[i,0,0], matches[i,1,0]], [matches[i,0,1], matches[i,1,1]], color=colors[i])
plt.show()



# import math
# labels = train_labels_animals + val_labels + test_labels

# # calculate how often the matching by findHeadTailMatch was correct
# neg_scores_list = []
# pos_scores_list = []
# problem_entries = []
# for entry in labels:
#     heads = []
#     tails = []
#     for i in range(0, len(entry["animals"]), 2):
#         heads.append(entry["animals"][i]["position"])
#         tails.append(entry["animals"][i+1]["position"])
    
#     if len(heads) > 0 and len(tails) > 0:
#         matches = findHeadTailMatches(heads, tails)
        
#         gt = np.array(range(len(matches)))
        
#         scores = np.equal(matches, gt)
#         pos_score = np.count_nonzero(scores == True)
#         neg_score = np.count_nonzero(scores == False)
        
#         neg_scores_list.append(neg_score)
#         pos_scores_list.append(pos_score)
        
#         if neg_score != 0:
#             problem_entries.append(entry)


# # plot problematic entries
# for entry in problem_entries[:5]:
#     heads = []
#     tails = []
#     image = loadImage(entry["filename"], 32, False)
#     plt.imshow(image)
#     colors = cm.rainbow(np.linspace(0, 1, len(entry["animals"])))
#     for i in range(0, len(entry["animals"]), 2):
#         head = entry["animals"][i]["position"]
#         tail = entry["animals"][i+1]["position"]
#         plt.scatter(head[0], head[1], color=colors[i])
#         plt.scatter(tail[0], tail[1], color=colors[i])
#         plt.plot([head[0], tail[0]], [head[1], tail[1]], color=colors[i])
#     plt.show()
    

# calculate angle between head and tail
# angles = []
# count = 0
# for entry in labels:
#     for i in range(0, len(entry["animals"]), 2):
#         deltay = entry["animals"][i]["position"][1]-entry["animals"][i+1]["position"][1]
#         deltax = entry["animals"][i]["position"][0]-entry["animals"][i+1]["position"][0]
        
#         if deltax == 0:
#             angle = 0
#             print("deltax is 0")
#         else:
#             angle = math.degrees(math.atan(deltay/deltax))
#         angles.append(angle)
        
#     print(count)
#     count += 1
# print(sum(np.abs(angles))/len(np.abs(angles))) 
    
