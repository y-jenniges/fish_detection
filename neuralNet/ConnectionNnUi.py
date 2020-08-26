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
import matplotlib.pyplot as plt

def loadNn(path):
    return keras.models.load_model(path)

def applyNnToImage(model, image_path):
    # image needs to be in [-1,1]
    image = np.asarray(loadImage(image_path))
    image = 2.*image/np.max(image) - 1
    
    # predicted heatmap
    X = np.expand_dims(image, axis=0)
    yHat = model.predict(X)
    return yHat

def loadImage(fname, equalize=False):
    "Loads an image as a h*w*3 numpy array"

    img = img_to_array(load_img(fname), dtype="uint8")

    #print(f"image before {img.shape}")
    rest_x, rest_y = img.shape[0]%32, img.shape[1]%32
    if rest_x != 0:
        img = np.pad(img, ((0,32-rest_x),(0, 0),(0,0)), 'constant', constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, 32-rest_y),(0,0)), 'constant', constant_values=0)
       
    return img


def applyThresholdToHm(image, threshold=130):
    img_thr = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO_INV)[1]
    return img_thr

def nonMaximumSuppression(image, min_distance=20):
    coordinates = peak_local_max(image, min_distance=min_distance)
    return coordinates
    


modelPath = "../data/output/36/model-H"
imgPath = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/60.jpg"
f39 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/39.jpg"

print("load model...")
model = loadNn(modelPath)
print("model loaded. predicting...")
prediction = applyNnToImage(model, imgPath)
print("prediction done")


pred_fish_head = prediction[0, :, :, 0]
#pred_fish_head = pred_fish_head[:, :, np.newaxis]
# convert hm range [0,1] to [0,255]
pred_fish_head = pred_fish_head*255.0
#plt.imshow(pred_fish_head)

image_thr = applyThresholdToHm(pred_fish_head)
coordinates = nonMaximumSuppression(image_thr, 10)

plt.imshow(pred_fish_head, cmap=plt.cm.gray)
plt.autoscale(False)
plt.plot(coordinates[:, 1], coordinates[:, 0], 'r.')

