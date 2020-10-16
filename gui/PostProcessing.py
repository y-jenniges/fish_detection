#!/usr/bin/python

# coding: utf-8

#from sklearn.cluster import DBSCAN
#from statistics import median
import numpy as np
import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
from skimage.feature import peak_local_max
from skimage.transform import resize


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


def rectifyAndMatch(matcher, camera_config, left_image_path, right_image_path, objects_left):    
    image_L = img_to_array(load_img(left_image_path), dtype="uint8")
    image_R = img_to_array(load_img(right_image_path), dtype="uint8")
    
    merged_objects, img_stereo_debug = \
        matcher.matchCorrespondences(image_L, image_R, objects_left, [])
        
    plt.imshow(img_stereo_debug)
    plt.show()
    #undistortPoints with inverted matrices P and R as parameters (to get normal coordinates?)
    return merged_objects

def measureLength(distance_measurer, camera_config, merged_objects):
    #calculate distances by triangulation 
    if len(merged_objects) != 0:
        #Stereo triangulation
        merged_pos = np.empty((len(merged_objects),8), dtype=np.float)
        for i in range(len(merged_objects)):
            merged_pos[i] = np.array(merged_objects[i][1:], dtype=np.float)
            print("found: ", merged_pos[i][:4], " -> ", merged_pos[i][-4:])
        distances = distance_measurer.distances(merged_pos[:,0:2], merged_pos[:,2:4],
                                                merged_pos[:,4:6], merged_pos[:,6:8])
        
    return distances


class StereoCorrespondence():
    """finder of corresponding objects in stereo image0 and image1
    stereo rectifies the images by given calibrations.
    Get positions of objects in img0, also rectifies them and get the epilines 
    in img1.
    Get region around a position as template and seach for similar region on 
    the other img.
    Seach for a template like region only near the epiline.

    Implemented by Timo Jasper in his Bachelor thesis 'Erkennen und Vermessen 
    von Meereslebewesen auf Stereo-Kamerabildern mit einem neuronalen Netz' 
    (2019)
    """
    def __init__(self, c_L, d_L, c_R, d_R, rotation, translation, img_size):
        self.c_L = np.array(c_L)
        self.d_L = np.array(d_L)
        self.c_R = np.array(c_R)
        self.d_R = np.array(d_R)
        self.rotation = np.array(rotation)
        self.translation = np.array(translation)
        
        self.R1 = np.zeros((3, 3))
        self.R2 = np.zeros((3, 3))
        self.P1 = np.zeros((3, 4))
        self.P2 = np.zeros((3, 4))

        # cv2.stereoRectify(self <
        #                   self.P1, self.P2, Q=None,
        #                   flags=cv2.CALIB_ZERO_DISPARITY, alpha=1, newImageSize=(0, 0))
    
        
        cv2.stereoRectify(self.c_L, self.d_L, self.c_R, self.d_R, img_size,
                  self.rotation, self.translation, self.R1, self.R2,
                  self.P1, self.P2, Q=None,
                  flags=cv2.CALIB_ZERO_DISPARITY, alpha=1, newImageSize=(0, 0))
        
        self.map_L1, self.map_L2 = cv2.initUndistortRectifyMap(self.c_L, self.d_L, self.R1, self.P1, img_size, m1type=cv2.CV_32FC2)
        self.map_R1, self.map_R2 = cv2.initUndistortRectifyMap(self.c_R, self.d_R, self.R2, self.P2, img_size, m1type=cv2.CV_32FC2)

        
    def calculateUnrectifiedCoordinates(self, merged_objects):      
        pts_L_H = np.array([[x[1],x[2]] for x in merged_objects])
        pts_L_B = np.array([[x[3],x[4]] for x in merged_objects])
        pts_R_H = np.array([[x[5],x[6]] for x in merged_objects])
        pts_R_B = np.array([[x[7],x[8]] for x in merged_objects])
        
        print(self.P1[:3,:3])
        ptsOut = cv2.undistortPoints(pts_L_H[0], self.P1[:3,:3], None)
        ptsTemp = cv2.convertPointsToHomogeneous(ptsOut);
        rtemp = ttemp = np.array([0,0,0], dtype='float32')
        output = cv2.projectPoints(ptsTemp, rtemp, ttemp, self.c_L, self.d_L, ptsOut);
        print(output)
        #pts_rectified_L_H = cv2.undistortPoints(pts_L_H, self.c_L, self.d_L, R=self.inv_R1, P=self.inv_P1)
        #pts_rectified_L_B = cv2.undistortPoints(pts_L_H, self.c_L, self.d_L, R=self.inv_R1, P=self.inv_P1)
        
        # pts_rectified_R_H = cv2.undistortPoints(pts_R_H, self.c_L, self.d_L, R=self.inv_R2, P=self.inv_P2)
        # pts_rectified_R_B = cv2.undistortPoints(pts_R_B, self.c_L, self.d_L, R=self.inv_R2, P=self.inv_P2)
        
        merged_objects_distorted = []
        
        return merged_objects_distorted
    
    def templateMatching(self, template, img, position, epiline_thresh, template_radius):
        """template matching near the epiline"""
        
        vert_thresh = 5 #vertical search radius
        
        #template inside img?
        if (position[1]-template_radius < 0 or position[1]+template_radius > img.shape[0] or
            position[0]-template_radius < 0 or position[0]+template_radius > img.shape[1]): 
            return None

        #calculate ROI for template search
        min_x = max((int)(position[1]-template_radius-vert_thresh), 0)
        max_x = min((int)(position[1]+template_radius+vert_thresh), img.shape[0])
        min_y = max((int)(position[0]-template_radius-epiline_thresh), 0)
        max_y = min((int)(position[0]+template_radius), img.shape[1])
        search_region = img[min_x:max_x,min_y:max_y,:]
        
        # Apply template Matching
        res = cv2.matchTemplate(search_region,template,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        return np.array([min_x+max_loc[1]+template_radius,min_y+max_loc[0]+template_radius])
    
    
    def sameVec(self, vec0, vec1, min_thresh=5., dynamic_thresh=2.):
        """check if 2 vectors have less than dynamic_thresh*norm(vec0) difference
        param min_thresh is minimum absolute distance threshold for difference of vec0, vec1,
        param dynamic_thresh defines the part of the longer vector thats used as thresh"""
        #print("sameVEC DEBUG: ",vec0, vec1)
        diff_thresh = dynamic_thresh * cv2.norm(vec0, normType=cv2.NORM_L2)
        diff = cv2.norm(np.array(vec0, dtype=float), np.array(vec1, dtype=float), normType=cv2.NORM_L2)
        return diff < max(min_thresh, diff_thresh)
    
        
    def matchCorrespondences(self, img_L, img_R, obj_L, obj_R, template_radius=50, epiline_thresh=2000):
        """match similar obj coordinates, near eplines in the other img and returns merged objects"""
        
        merged_objects = [] #list to collect outputs
        
        #stereo rectify images to get horizontal epilines
        img_L_rectifd = cv2.remap(np.copy(img_L), self.map_L1, self.map_L2, interpolation=cv2.INTER_LINEAR )
        img_R_rectifd = np.zeros(img_L.shape)
        if img_R is not None:
            img_R_rectifd = cv2.remap(np.copy(img_R), self.map_R1, self.map_R2, interpolation=cv2.INTER_LINEAR )
        
        #creates stereorectified overview img for debugging
        img_stereo = np.empty((img_L_rectifd.shape[0], img_L_rectifd.shape[1]*2, img_L_rectifd.shape[2]))
        img_stereo[:,:img_L_rectifd.shape[1],:] = np.copy(img_L_rectifd) 
        img_stereo[:,img_L_rectifd.shape[1]:,:] = np.copy(img_R_rectifd) 
        
        #single left img
        if img_R is None:
            for obj in obj_L:
                merged_objects.append(obj+[0,0,0,0])
            return merged_objects, img_stereo
        
        #no objects given
        if obj_L is None or len(obj_L) == 0:
            return merged_objects, img_stereo
        
        #stereo rectify points for Left Head and Back
        pts_L_H = np.array([[x[1],x[2]] for x in obj_L], dtype=np.float32)
        pts_L_B = np.array([[x[3],x[4]] for x in obj_L], dtype=np.float32)
        pts_R_H = np.array([[x[1],x[2]] for x in obj_R], dtype=np.float32)
        pts_R_H = np.array([[x[3],x[4]] for x in obj_R], dtype=np.float32)
        pts_rectified_L_H = cv2.undistortPoints(np.expand_dims(pts_L_H, 1), self.c_L, self.d_L, R=self.R1, P=self.P1)
        pts_rectified_L_B = cv2.undistortPoints(np.expand_dims(pts_L_B, 1), self.c_L, self.d_L, R=self.R1, P=self.P1)
        
        #iterate over all objects in img_L and find possible right correspondences
        for i in range(len(obj_L)):
            head = pts_rectified_L_H[i,0]
            back = pts_rectified_L_B[i,0]
            
            #create templates from obj positions
            head_template = img_L_rectifd[(int)(head[1]-template_radius):(int)(head[1]+template_radius),
                                          (int)(head[0]-template_radius):(int)(head[0]+template_radius),:]
            back_template = img_L_rectifd[(int)(back[1]-template_radius):(int)(back[1]+template_radius),
                                          (int)(back[0]-template_radius):(int)(back[0]+template_radius),:]
            
            #draw head template recangle on img_stereo
            color = (np.random.choice(255),np.random.choice(255),np.random.choice(255))
            top_left = ((int)(head[0]-template_radius),(int)(head[1]-template_radius))
            bottom_right = ((int)(head[0]+template_radius),(int)(head[1]+template_radius))
            cv2.rectangle(img_stereo, top_left, bottom_right, color, 2)
            #draw back template recangle on img_stereo
            top_left = ((int)(back[0]-template_radius),(int)(back[1]-template_radius))
            bottom_right = ((int)(back[0]+template_radius),(int)(back[1]+template_radius))
            cv2.rectangle(img_stereo, top_left, bottom_right, color, 2)

            #find possible matches on epiline
            head2 = StereoCorrespondence.templateMatching(self,head_template, img_R_rectifd, head, epiline_thresh, template_radius)
            back2 = StereoCorrespondence.templateMatching(self,back_template, img_R_rectifd, back, epiline_thresh, template_radius)
            
            #check if obj and obj2 positions vectors are relative equal
            if head2 is None or back2 is None or not StereoCorrespondence.sameVec(self,(head-back),(head2-back2)):
                #print("found nothing")
                merged_objects.append([obj_L[i][0],head[0],head[1],back[0],back[1]]+[0,0,0,0])
            else:
                #draw head template recangle on img_stereo
                top_left2 = ((int)(head2[1]-template_radius+img_R_rectifd.shape[1]),(int)(head2[0]-template_radius))
                bottom_right2 = ((int)(head2[1]+template_radius+img_R_rectifd.shape[1]),(int)(head2[0]+template_radius))
                cv2.rectangle(img_stereo,top_left2, bottom_right2, color, 3)
                #draw back template recangle on img_stereo
                top_left2 = ((int)(back2[1]-template_radius+img_R_rectifd.shape[1]),(int)(back2[0]-template_radius))
                bottom_right2 = ((int)(back2[1]+template_radius+img_R_rectifd.shape[1]),(int)(back2[0]+template_radius))
                cv2.rectangle(img_stereo,top_left2, bottom_right2, color, 3)
                merged_objects.append([obj_L[i][0],head[0],head[1],back[0],back[1],head2[0],head2[1],back2[0],back2[1]])
                #print("found: ", head[0], head[1], " -> ", top_left2[0], top_left2[1])

        return merged_objects, img_stereo
    
    
    
    
    