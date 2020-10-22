import os
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array
from skimage.feature import peak_local_max
from skimage.transform import resize
from scipy.optimize import linear_sum_assignment
import Losses
from sklearn.metrics import confusion_matrix
import HelperFunctions as helpers
import DataGenerator as dg
import keras

from tensorflow import random
#from tensorflow import set_random_seed

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
random.set_seed(2)
#set_random_seed(2)    
    
# dict mapping group ID to its string representation
GROUP_DICT = {0: "Nothing", 1: "Fish", 2: "Crustacea", 
              3: "Chaetognatha", 4: "Unidentified", 5: "Jellyfish"}


def loadNn(path, weights=None):
    if os.path.isfile(path):
        model = keras.models.load_model(
            path, 
            custom_objects={"loss": Losses.weighted_categorical_crossentropy(weights)})
        return model
    
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
    #print(f"image after {img.shape}")
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
        
    return hmResized

def findCoordinates(heatmap, threshold=50, radius=20):
    thr = applyThresholdToHm(heatmap, threshold)
    plt.imshow(thr)
    plt.show()
    coordinates = nonMaxSuppression(thr, radius)
    
    # remove coordinates whose x and y are closer than 10px
    df = pd.DataFrame(coordinates)
    df = df.sort_values(0, ignore_index=True)
    

    final_coords = df.copy() 
    
    for i in range(len(df)):
        for j in range(i, len(df)):
            if abs(df.iloc[i][0] - df.iloc[j][0]) < 10 \
            and abs(df.iloc[i][1] - df.iloc[j][1]) < 10 \
            and i != j and j in final_coords.index:
                #print(i,j)
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
    matches = np.array([])
    if ht_distances.size != 0:
        _, assignment = linear_sum_assignment(ht_distances)
        head_assignment, tail_assignment = linear_sum_assignment(ht_distances)
        
        #matches = np.array([(heads[i], tails[assignment[i]]) for i in range(len(heads))])
        matches = np.array([(heads[head_assignment[i]], tails[tail_assignment[i]]) for i in range(len(tail_assignment))])
    return matches 
    #return np.array(assignment)

def scaleMatchCoordinates(matches, input_res, output_res):
    xfactor = output_res[0]/input_res[0]
    yfactor = output_res[1]/input_res[1]
    
    scaled_matches = []
    for m in matches:
        m = [[m[0][0]*xfactor, m[0][1]*yfactor], # scale head
             [m[1][0]*xfactor, m[1][1]*yfactor]] # scale tail
        scaled_matches.append(m)
    
    return np.array(scaled_matches)

def exportAnimalsToCsv():
    pass

def oneHotToGroup(one_hot):
    if np.array_equal(one_hot, np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "fish_head"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "fish_tail"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "crust_head"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "crust_tail"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "chaeto_head"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])): return "chaeto_tail"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])): return "unid_head"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])): return "unid_tail"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0])): return "jelly_head"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])): return "jelly_tail"
    else:
        print("unknown one hot encoding")
    
def oneHotToGeneralGroup(one_hot):
    if np.array_equal(one_hot, np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "Fish"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "Fish"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "Crustacea"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "Crustacea"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])): return "Chaetognatha"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])): return "Chaetognatha"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])): return "Unidentified"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0])): return "Unidentified"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0])): return "Jellyfish"
    elif np.array_equal(one_hot, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])): return "Jellyfish"
    else:
        print("unknown one hot encoding")
        
model_path = "../data/output/800/model-H"
#model_path = "../data/output/801/model-H"
#model_path = "../data/output/900/model-H"
#model_path = "../data/output/901/model-H"
#modelPath = "../data/output/59/model-L"
#modelPath = "../data/output/48/model-L" # trained on all animals, coordiantes dont work

weights = np.array([ 1.        ,  1.04084507,  1.04084507,  1.        ,  1.        ,
        8.90361446,  8.90361446, 13.19642857, 13.19642857, 12.52542373,
       12.52542373])

print("load model...")
#model = loadNn(model_path, weights)


# get gt
label_root = "../data/maritime_dataset_25/labels/"
test_labels, train_labels_animals, train_labels_no_animals, val_labels, class_weights = helpers.loadAndSplitLabels(label_root)
#gt = [entry for entry in test_labels if entry["filename"] == img_path][0]

# fish_heads = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
# fish_tails = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

# gt_heads = np.array([np.array(animal["position"]) for animal in gt["animals"] if np.array_equal(animal["group"], fish_heads)])
# gt_tails = np.array([np.array(animal["position"]) for animal in gt["animals"] if np.array_equal(animal["group"], fish_tails)])


classes = ["fish_head", "fish_tail", "crust_head", "crust_tail", 
           "chaeto_head", "chaeto_tail", 
           "jelly_head", "jelly_tail", "unid_head", "unid_tail", ]

classes = ["Fish", "Crustacea", "Chaetognatha", "Unidentified", "Jellyfish"]

# evaluate coordinates
eval_df = pd.DataFrame(0, columns=["tp", "tn", "fp", "fn"], 
                       index=classes)

confusion_df = pd.DataFrame(0, columns=["nothing"]+classes, index=["nothing"]+classes)
#img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/60.jpg"
#img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/39.jpg"
#img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/51.jpg"
#img_path = "G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images/Rectified_TN_Exif_Remos1_2015.08.02_01.00.49_L.jpg"
#img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/826.jpg" #jellyfish
#img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/575.jpg" #jellyfish
#img_path = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/309.jpg" #crust

#img_list = ['G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images\\Rectified_TN_Exif_Remos1_2015.08.02_00.00.49_L.jpg', 'G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images\\Rectified_TN_Exif_Remos1_2015.08.02_01.00.49_L.jpg', 'G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images\\Rectified_TN_Exif_Remos1_2015.08.02_05.00.47_L.jpg', 'G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images\\Rectified_TN_Exif_Remos1_2015.08.02_05.30.48_L.jpg', 'G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images\\Rectified_TN_Exif_Remos1_2015.08.02_09.30.48_L.jpg', 'G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images\\Rectified_TN_Exif_Remos1_2015.08.02_22.30.55_L.jpg']
#img_path = img_list[0]

fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fish_labels = helpers.filter_labels_for_animal_group(test_labels, fish_id)

crust_id = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
crust_labels = helpers.filter_labels_for_animal_group(test_labels, crust_id)

chaetognatha_id = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
chaeto_labels = helpers.filter_labels_for_animal_group(test_labels, chaetognatha_id)

unidentified_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]  
unidentified_labels = helpers.filter_labels_for_animal_group(test_labels, unidentified_id)

jellyfish_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
jellyfish_labels = helpers.filter_labels_for_animal_group(test_labels, jellyfish_id)

test_labels = test_labels + train_labels_animals + val_labels
#test_labels = [test_labels[7]]

true_positives = 0
for gt in test_labels:
    image = loadImage(gt["filename"], factor=32)
    
    heads = []
    tails = []
    
    # gt
    for i in range(0, len(gt["animals"]), 2):
        heads.append(gt["animals"][i]["position"])
        tails.append(gt["animals"][i+1]["position"])
    
    # matches
    matches = findHeadTailMatches(np.array(heads), np.array(tails))
    
    for m in matches:
        h = np.array([m[0][0], m[0][1]])
        t = np.array([m[1][0], m[1][1]])
        for i in range(0, len(gt["animals"]), 2):
            if np.array_equal(np.array(gt["animals"][i]["position"]), h):
                if np.array_equal(np.array(gt["animals"][i+1]["position"]), t):
                    true_positives += 1
    print(f"current score {true_positives}")

print(f"final score {true_positives}")
    
    

# for gt in test_labels:
#     print("load image", gt["filename"])
#     image = loadImage(gt["filename"], factor=32)
#     img = loadImage(gt["filename"], factor=32, rescale_range=False)
        
    
#     #print("model loaded. predicting...")
#     #prediction = applyNnToImage(model, image)
#     prediction = np.expand_dims(dg.prepareEntryHeatmap(gt, "high")[1],0)
    
#     #print("prediction done")
    
    
#     # iterate over the groups
#     df = pd.DataFrame(columns=["group", "LX1", "LY1", "LX2", "LY2"])    
#     #df = pd.DataFrame(columns=["group", "x", "y"])   
    
#     for i in range(1, prediction.shape[3], 2):
#         #print(i)
        
#         heads = prediction[0,:,:,i]*255
#         heads = heads.astype('uint8')
        
#         tails = prediction[0,:,:,i+1]*255
#         tails = tails.astype('uint8')
    
#         # get coordinates
#         #print("get head coordinates")
#         head_coordinates = findCoordinates(heads, 110, 5) 
#         #print("get tail coordinates")
#         tail_coordinates = findCoordinates(tails, 110, 5)
        
#         #print("find head tail matches")
#         # find head-tail matches
#         matches = findHeadTailMatches(head_coordinates, tail_coordinates)
    
#         # scale matches to image resolution
#         matches = scaleMatchCoordinates(matches, heads.shape, img.shape)
        
#         group = GROUP_DICT[np.ceil(i/2)]
        
#         # show prediction heatmap and coordinates
#         plt.imshow(heads, cmap=plt.cm.gray)
#         plt.autoscale(False)
#         plt.plot(head_coordinates[:, 0], head_coordinates[:, 1], 'r.')
#         plt.show()
        
#         plt.imshow(tails, cmap=plt.cm.gray)
#         plt.autoscale(False)
#         plt.plot(tail_coordinates[:, 0], tail_coordinates[:, 1], 'r.')
#         plt.show()
    
#         # plot each match with a different colour
#         colors = cm.rainbow(np.linspace(0, 1, matches.shape[0]))
#         plt.imshow(heads, cmap=plt.cm.gray)
#         plt.imshow(img)
#         for i in range(matches.shape[0]):
#             plt.scatter(matches[i,:,0], matches[i,:,1], color=colors[i])
#             plt.plot([matches[i,0,0], matches[i,1,0]], [matches[i,0,1], matches[i,1,1]], color=colors[i])
#         plt.show()
    
    
#         # append predicted animals from the current group
#         for m in matches:
#             animal = {"group": group, 
#                       "LX1": m[0][0], "LY1": m[0][1], # head
#                       "LX2": m[1][0], "LY2": m[1][1]} # tail
#             df = df.append(animal, ignore_index=True)
      
        
#             found = False
            
#             # iterate over gt heads
#             for j in range(0, len(gt["animals"]), 2):
                
#                 # only continue if the group is the same
#                 if oneHotToGeneralGroup(gt["animals"][j]["group"]) == group:
#                     head = np.array([animal["LX1"], animal["LY1"]])
#                     distance_head = np.linalg.norm(np.array(gt["animals"][j]["position"]) - head)
        
#                     if distance_head < 30:
#                         tail = np.array([animal["LX2"], animal["LY2"]])
#                         distance_tail = np.linalg.norm(np.array(gt["animals"][j+1]["position"]) - tail)
                    
#                         if distance_tail < 30:
#                             found = True
#                             eval_df.loc[group, "tp"] += 1
#                             gt["animals"].remove(gt["animals"][j]) # remove head
#                             gt["animals"].remove(gt["animals"][j]) # remove tail
#                             break
                   
#             # add wrong detections
#             if not found:
#                 eval_df.loc[group, "fp"] += 1
            
#     # add unrecognized animals of the group
#     for k in range(0, len(gt["animals"]), 2):
#         g = oneHotToGeneralGroup(gt["animals"][k]["group"])
#         eval_df.loc[group, "fn"] += 1
            
#     print(eval_df)
      
    #     one_hot_h = np.zeros(11)
    #     one_hot_h[i] = 1
        
    #     one_hot_t = np.zeros(11)
    #     one_hot_t[i+1] = 1
        
    #     group_h = oneHotToGroup(one_hot_h)
    #     group_t = oneHotToGroup(one_hot_t)
        
    #     head_coordinates *= 2
    #     tail_coordinates *= 2
        
    #     for h in head_coordinates:
    #         entry = {"group": group_h, "x": h[0], "y": h[1]}
    #         df = df.append(entry, ignore_index=True)
        
    #     for t in tail_coordinates:
    #         entry = {"group": group_t, "x": t[0], "y": t[1]}
    #         df = df.append(entry, ignore_index=True)

    # nothing = [1.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    # fish_h = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # fish_t = [0.0, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # gt_fh = [x["position"] for x in gt["animals"] if x["group"] == fish_h]
    # gt_ft = [x["position"] for x in gt["animals"] if x["group"] == fish_t]
    
    # crust_h = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # crust_t = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # gt_crh = [x["position"] for x in gt["animals"] if x["group"] == crust_h]
    # gt_crt = [x["position"] for x in gt["animals"] if x["group"] == crust_t]
    
    # chaet_h = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # chaet_t = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    # gt_chh = [x["position"] for x in gt["animals"] if x["group"] == chaet_h]
    # gt_cht = [x["position"] for x in gt["animals"] if x["group"] == chaet_t]
    
    # unid_h = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]  
    # unid_t = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]  
    # gt_uh = [x["position"] for x in gt["animals"] if x["group"] == unid_h]
    # gt_ut = [x["position"] for x in gt["animals"] if x["group"] == unid_t]
    
    # jelly_h = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    # jelly_t = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    # gt_jh = [x["position"] for x in gt["animals"] if x["group"] == jelly_h]
    # gt_jt = [x["position"] for x in gt["animals"] if x["group"] == jelly_t]
    
    # gt_all = gt["animals"]
    
    # for i in range(len(df)):
    #     if df.iloc[i]["group"] == "fish_head": 
    #         idx = 0
    #         gt_s = gt_fh
    #     elif  df.iloc[i]["group"] == "fish_tail": 
    #         idx = 1
    #         gt_s = gt_ft
    #     elif df.iloc[i]["group"] == "crust_head": 
    #         idx = 2
    #         gt_s = gt_crh
    #     elif df.iloc[i]["group"] == "crust_tail": 
    #         idx = 3
    #         gt_s = gt_crt
    #     elif df.iloc[i]["group"] == "chaeto_head": 
    #         idx = 4
    #         gt_s = gt_chh
    #     elif df.iloc[i]["group"] == "chaeto_tail": 
    #         idx = 5
    #         gt_s = gt_cht
    #     elif df.iloc[i]["group"] == "unid_head": 
    #         idx = 8
    #         gt_s = gt_uh
    #     elif df.iloc[i]["group"] == "unid_tail": 
    #         idx = 9
    #         gt_s = gt_ut
    #     elif df.iloc[i]["group"] == "jelly_head": 
    #         idx = 6
    #         gt_s = gt_jh
    #     elif df.iloc[i]["group"] == "jelly_tail": 
    #         idx = 7
    #         gt_s = gt_jt
    #     else: 
    #         print("unknown group", df.iloc[i]["group"])
        
    #     data_point = np.array([df.iloc[i]["x"], df.iloc[i]["y"]])
                
    #     found = False
    #     for entry in gt_s:
    #         distance = np.linalg.norm(np.array(entry) - data_point)
    #         if distance < 30:
    #             found = True
    #             eval_df.iloc[idx]["tp"] += 1
    #             gt_s.remove(entry)
    #             break
    #     if not found:
    #         eval_df.iloc[idx]["fp"] += 1
            
    #     # confusion matrix ----------------------------------- #
    #     found = False
    #     for a in gt_all:
    #         distance= np.linalg.norm(np.array(a["position"]) - data_point)
            
    #         if distance < 30:
    #             found = True
    #             gt_group = oneHotToGroup(a["group"])
    #             confusion_df.iloc[idx+1][gt_group] += 1
    #             gt_all.remove(a)
    #             break
                
    #     if not found:
    #         confusion_df.iloc[idx+1]["nothing"] += 1

            
    # eval_df.iloc[0]["fn"] += len(gt_fh) 
    # eval_df.iloc[1]["fn"] += len(gt_ft) 
    
    # eval_df.iloc[2]["fn"] += len(gt_crh) 
    # eval_df.iloc[3]["fn"] += len(gt_crt) 
    
    # eval_df.iloc[4]["fn"] += len(gt_chh) 
    # eval_df.iloc[5]["fn"] += len(gt_cht) 
    
    # eval_df.iloc[6]["fn"] += len(gt_uh) 
    # eval_df.iloc[7]["fn"] += len(gt_ut) 
    
    # eval_df.iloc[8]["fn"] += len(gt_jh) 
    # eval_df.iloc[9]["fn"] += len(gt_jt) 
    
    # print(eval_df)
    # print(confusion_df)


# #matches = findHeadTailMatches(head_coordinates, tail_coordinates)
# matches = findHeadTailMatches(gt_heads, gt_tails)

# # show groundtruth
# helpers.showImageWithHeatmap(img, None, gt["animals"], 1, "both")


# # plot each match with a different colour
# colors = cm.rainbow(np.linspace(0, 1, matches.shape[0]))
# plt.imshow(heads, cmap=plt.cm.gray)
# plt.imshow(img)
# for i in range(matches.shape[0]):
#     plt.scatter(matches[i,:,0], matches[i,:,1], color=colors[i])
#     plt.plot([matches[i,0,0], matches[i,1,0]], [matches[i,0,1], matches[i,1,1]], color=colors[i])
# plt.show()



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
    



# barWidth = 0.2

# bars1 = [393, 556, 405]
# bars2 = [430, 729, 368]
# bars3 = [248, 376, 550]
# bars4 = [395, 448, 403]

# r1 = np.arange(len(bars1))
# r2 = [x + barWidth for x in r1]
# r3 = [x + barWidth for x in r2]
# r4 = [x + barWidth for x in r3]

# # Make the plot
# plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label='No weights, 50')
# plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label='No weights, 100')
# plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='Weights, 50')
# plt.bar(r4, bars4, color='#2d7f5f', width=barWidth, edgecolor='white', label='Weights, 100') 

# # Add xticks on the middle of the group bars
# plt.xlabel('group', fontweight='bold')
# plt.xticks([r + barWidth for r in range(len(bars1))], ['True positives', 'False positives', 'False negatives'])
 
# # Create legend & Show graphic
# plt.legend()
# plt.show()

# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# columns = ["Background", "Fish head", "Fish tail", "Crustacea head", "Crustacea tail", "Chaetognatha head", "Chaetognatha tail", "Jellyfish head", "Jellyfish tail", "Unidentified head", "Unidentified tail"]
# data_801 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [155, 108, 9, 2, 0, 0, 0, 0, 0, 0, 0], [199, 10, 103, 0, 3, 1, 0, 0, 0, 0, 0], [179, 4, 2, 109, 16, 3, 1, 1, 0, 1, 0], [167, 0, 0, 3, 88, 0, 2, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
# data_901 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [55, 94, 20, 1, 0, 1, 0, 0, 0, 0, 0], [63, 17, 87, 0, 1, 1, 0, 0, 1, 0, 0], [114, 1, 0, 108, 4, 1, 0, 0, 0, 3, 0], [78, 0, 0, 0, 85, 0, 1, 0, 0, 0, 3], [14, 1, 1, 0, 0, 3, 0, 1, 1, 0, 0], [18, 0, 1, 0, 0, 0, 3, 0, 1, 0, 0], [5, 1, 1, 0, 0, 0, 0, 3, 1, 0, 0], [4, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [17, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0], [18, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0]]

# df_801 = pd.DataFrame(data=data_801, columns=columns, index=columns)
# df_901 = pd.DataFrame(data=data_901, columns=columns, index=columns)

# def plot_confusion_matrix(df_confusion, title='Confusion matrix', cmap=plt.cm.gray_r):
#     plt.matshow(df_confusion, cmap=plt.cm.Blues) # imshow
#     #plt.title(title)
#     plt.colorbar()
#     tick_marks = np.arange(len(df_confusion.columns))
#     plt.xticks(tick_marks, df_confusion.columns, rotation=90)
#     plt.yticks(tick_marks, df_confusion.index)
#     #plt.tight_layout()
#     plt.ylabel(df_confusion.index.name)
#     plt.xlabel(df_confusion.columns.name)

# plot_confusion_matrix(df_801)
# plot_confusion_matrix(df_901)