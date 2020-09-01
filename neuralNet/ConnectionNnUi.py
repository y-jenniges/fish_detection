# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 19:47:52 2020

@author: yjenn
"""
from keras.preprocessing.image import load_img, img_to_array
import keras
import numpy as np
import cv2
from skimage.feature import peak_local_max
from skimage.transform import resize
import matplotlib.pyplot as plt

def loadNn(path):
    return keras.models.load_model(path)

def applyNnToImage(model, image):

    
    # predicted heatmap
    X = np.expand_dims(image, axis=0)
    yHat = model.predict(X)
    return yHat

def loadImage(fname, equalize=False):
    "Loads an image as a h*w*3 numpy array"

    img = img_to_array(load_img(fname), dtype="uint8")
    
    # if image is still large, downscale it by 25%
    #from PIL import Image, ImageEnhance, ImageOps
    #from skimage.transform import resize
    if img.shape[0] > 2500:
        img = resize(img, (img.shape[0]*0.25, img.shape[1]*0.25))

    #print(f"image before {img.shape}")
    rest_x, rest_y = img.shape[0]%32, img.shape[1]%32
    if rest_x != 0:
        img = np.pad(img, ((0,32-rest_x),(0, 0),(0,0)), 'constant', constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, 32-rest_y),(0,0)), 'constant', constant_values=0)
      
    # image needs to be in [-1,1]
    img = np.asarray(img)
    img = 2.*img/np.max(img) - 1
    
    return img


def applyThresholdToHm(image, threshold=130):
    img_thr = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO_INV)[1]
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

modelPath = "../data/output/36/model-H"
#modelPath = "../data/output/48/model-L" # trained on all animals, coordiantes dont work
imgPath = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/60.jpg"
f39 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/39.jpg"
imgPath = "G:/Universität/UniBremen/Semester4/Data/moreTestData/2015_08/Rectified Images/Rectified_TN_Exif_Remos1_2015.08.02_01.00.49_L.jpg"

print("load model...")
model = loadNn(modelPath)
print("load image")
image = loadImage(imgPath)
print("model loaded. predicting...")
prediction = applyNnToImage(model, image)
print("prediction done")



    

#def predictionToCoordinates(prediction):

def saveCoordinatesInFile():
    pass
    

pred_fish_head = prediction[0, :, :]#, 0]
#pred_fish_head = pred_fish_head[:, :, np.newaxis]
# convert hm range [0,1] to [0,255]
pred_fish_head = pred_fish_head*255.0
#plt.imshow(pred_fish_head)

#pred_fish_head = resizeHm(image, pred_fish_head)

image_thr = applyThresholdToHm(pred_fish_head)
coordinates = nonMaxSuppression(image_thr, 10)

plt.imshow(pred_fish_head, cmap=plt.cm.gray)
plt.autoscale(False)
plt.plot(coordinates[:, 1], coordinates[:, 0], 'r.')


# coordinates on non-rectified images
# default for status: not checked
# default for manually corrected: no
columns = ["file_id", "object_remarks", 
           "group", "species", 
           "LX1", "LY1",
           "LX2", "LY2", 
           "LX3", "LY3", 
           "LX4", "LY4", 
           "RX1", "RY1",
           "RX2", "RY2", 
           "RX3", "RY3", 
           "RX4", "RY4", 
           "length", "height", "image_remark",
           "status", "manually_corrected"
            ]

# send an "image written" event to the main thread