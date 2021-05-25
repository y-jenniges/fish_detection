#from sklearn.cluster import DBSCAN
#from statistics import median
import numpy as np
import cv2
import pandas as pd
import os
#import matplotlib.pyplot as plt
from PyQt5 import QtCore
from tensorflow.keras.preprocessing.image import load_img, img_to_array # check if t works, otherwise only keras
from skimage.feature import peak_local_max
#from skimage.transform import resize
#from skimage.transform import rescale
from scipy.optimize import linear_sum_assignment


""" Functions and classes necessary for post processing. """


class RectifyMatchWorker(QtCore.QObject):
    """ Object to work in a thread and to be deleted after the rectification 
    and matching calculations finished.
    """
    
    # define custom signals
    finished = QtCore.pyqtSignal() 
    """ Signal emitted when the predicter finished predicting an image list. """
    
    progress = QtCore.pyqtSignal(int)
    """ Signal emitted for every image from an image list that is already predicted. """
    
    def __init__(self, matcher, models, img_list, camera_config):
        super().__init__()
        
        self.matcher = matcher
        self.models = models
        self.image_list = img_list
        self.camera_config = camera_config

    def rectifyMatch(self):
        count = 0
        
        # iterate over left images, rectify and match   
        for i in range(len(self.image_list[0])):
            right_image = self.image_list[1][i]
            left_image = self.image_list[0][i]
            print(right_image)
            print(left_image)
            print()
            
            # only continue if both images exists
            if os.path.isfile(right_image) and os.path.isfile(left_image):
                file_id = os.path.basename(left_image).rstrip(".jpg").rstrip(".png").rstrip("_L").rstrip("_R")
                
                # get animals on current image into necessary format
                cur_entries = self.models.model_animals.data[self.models.model_animals.data["file_id"] == file_id]
                
                animals_left = []
                for i in range(len(cur_entries)):   
                    # only match left animals that do not have a right match yet
                    if cur_entries.iloc[i]["RX1"] is None \
                    or cur_entries.iloc[i]["RX1"] == -1 \
                    or cur_entries.iloc[i]["RX1"] == 0:
                        animal = [0, cur_entries.iloc[i]["LY1"], 
                                  cur_entries.iloc[i]["LX1"], 
                                  cur_entries.iloc[i]["LY2"], 
                                  cur_entries.iloc[i]["LX2"]]
                        animals_left.append(animal)    
                    else:
                        animals_left.append([])  
                
                print("left animals: ")
                print(animals_left)
                print()
                
                # rectify and match images
                merged_objects = self.matcher.rectifyAndMatch(self.matcher, 
                                                 self.camera_config, 
                                                 left_image, 
                                                 right_image, 
                                                 animals_left)
                
                print("merged ojects:")
                print(merged_objects)
                print()
                
                # add right coordinates to data model
                for i in range(len(cur_entries.index)):
                    idx = cur_entries.index[i]
                    
                    # only continue if the animal is matched
                    if merged_objects != [] and merged_objects[i] != []:
                        # the matcher returns rectified coordinates,
                        # they have to be calculated back and just then add them to data model 
                        head = self.matcher.distortPoint([merged_objects[i][6], merged_objects[i][5]], "R")
                        tail = self.matcher.distortPoint([merged_objects[i][8], merged_objects[i][7]], "R")
                        
                        if (np.array(head) < 0).any() or (np.array(tail) < 0).any():
                            head = [-1,-1]
                            tail = [-1,-1]
                            
                        self.models.model_animals.data.loc[idx, "RX1"] = head[1]
                        self.models.model_animals.data.loc[idx, "RY1"] = head[0]
                        self.models.model_animals.data.loc[idx, "RX2"] = tail[1]
                        self.models.model_animals.data.loc[idx, "RY2"] = tail[0] 
                    
            count = count + 1
            self.progress.emit(count)
    
        self.finished.emit()
        

class StereoCorrespondence():
    """ Finder of corresponding objects in stereo image0 and image1
    stereo rectifies the images by given calibrations.
    Get positions of objects in img0, also rectifies them and get the epilines 
    in img1.
    Get region around a position as template and seach for similar region on 
    the other img.
    Seach for a template like region only near the epiline.

    Implemented by Timo Jasper in his Bachelor thesis 'Erkennen und Vermessen 
    von Meereslebewesen auf Stereo-Kamerabildern mit einem neuronalen Netz' 
    (2019). Functions distortPoint and undistortPoint are added for this program.
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
       
    def distortPoint(self, point, lr="L"):
        """Redistort undistorted point. """
        x = np.int64(point[0])
        y = np.int64(point[1])
        
        distorted_x = -1
        distorted_y = -1
        
        if lr == "L":
            distorted_x = self.map_L1[y, x, 0]
            distorted_y = self.map_L1[y, x, 1]
        elif lr == "R":
            distorted_x = self.map_R1[y, x, 0]
            distorted_y = self.map_R1[y, x, 1]            
        
        return [distorted_x, distorted_y]
    
    def undistortPoint(self, point, lr="L"):
        """Undistort a point. """
        # make sure that the point is a numpy array of float
        point = np.array(point).astype(np.float)
        
        rectified = [0,0]
        if lr == "L":
            rectified = cv2.undistortPoints(np.expand_dims([point], 1), self.c_L, self.d_L, R=self.R1, P=self.P1)
        elif lr == "R":
            rectified = cv2.undistortPoints(np.expand_dims([point], 1), self.c_R, self.d_R, R=self.R2, P=self.P2)
        
        return rectified[0][0]
    
    def templateMatching(self, template, img, position, epiline_thresh, template_radius):
        """Template matching near the epiline"""
        
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
        if obj_L == []: return [], []
        
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
    
    def rectifyAndMatch(self, matcher, camera_config, left_image_path, right_image_path, objects_left):   
        """
        Function to rectify images and find corresponding animals on the right image.
    
        Parameters
        ----------
        matcher : StereoCorrespondence
            Object to perform the stereo matching.
        camera_config : loaded json
            Confugration of the camera.
        left_image_path : string
            Path to left image.
        right_image_path : string
            Path to right image.
        objects_left : list<list<int>>
            One entry depicts the group, head and tail positions of one animal
            on the left image.
            
        Returns
        -------
        merged_objects : list<list<int>>
            One entry depicts the group, head and tail positions of one animal
            on the left and right image.
    
        """
        image_L = img_to_array(load_img(left_image_path), dtype="uint8")
        image_R = img_to_array(load_img(right_image_path), dtype="uint8")
        
        merged_objects, img_stereo_debug = \
            self.matchCorrespondences(image_L, image_R, objects_left, [])
            
        return merged_objects
 
# --- neural network helpers ----------------------------------------------- #
def loadImage(fname, factor=32, rescale_range=True):
    """
    Loads an image as a h*w*3 numpy array in [-1, 1] (if rescale_range is True)

    Parameters
    ----------
    fname : string
        Path to image.
    factor : int, optional
        Factor used for padding necessary for the neural network prediction. 
        The default is 32.
    rescale_range : TYPE, optional
        Tells if the image range should be scaled to [-1,1]. The default is True.

    Returns
    -------
    img : np.array
        Loaded image.
    """
    img = img_to_array(load_img(fname), dtype="uint8")
    
    print("PP: img to array")
    
    # if image is still large, downscale it by 25%
    #from PIL import Image, ImageEnhance, ImageOps
    #from skimage.transform import resize
    # when skimage.transform.resize is used, exe (generated by pyinstaller) will crash on other machines
    if img.shape[0] > 2500:
        print("PP: img needs resizing")
        # convert to cv2 format (RGB -> BGR)
        cv_img = img[:, :, ::-1].copy()
        
        # resize image using cv2 function
        dsize=(round(cv_img.shape[1]*0.25), round(cv_img.shape[0]*0.25))
        temp = cv2.resize(cv_img, dsize=dsize, interpolation=cv2.INTER_AREA)#, fx=0.25, fy=0.25)
        
        # convert back to usual format (BGR -> RGB)
        img = temp[:, :, ::-1].copy()
        
        # scikit resize function (in version 0 code)
        #img = resize(img, (img.shape[0]*0.25, img.shape[1]*0.25))

    print("PP: image resized")

    rest_x, rest_y = img.shape[0]%factor, img.shape[1]%factor
    if rest_x != 0:
        img = np.pad(img, ((0,factor-rest_x),(0, 0),(0,0)), 'constant', 
                     constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, factor-rest_y),(0,0)), 'constant', 
                     constant_values=0)
    
    print("PP: padding done")
    
    if rescale_range:
        # image needs to be in [-1,1]
        img = np.asarray(img)
        img = 2.*img/np.max(img) - 1
    return img

def applyNnToImage(model, image):
    """
    Applies a neural network to an image.

    Parameters
    ----------
    model : Keras model
        Neural network model used for the prediction.
    image : np.array
        Image in range in [-1,1] that is to be predicted.

    Returns
    -------
    yHat : list
        Prediction of the neural network.

    """
    # predicted heatmap
    X = np.expand_dims(image, axis=0)
    
    print("PP: X expanded")
    
    yHat = model.predict(X)
    
    print("PP: yHat calculated")
    return yHat

def applyThresholdToHm(image, threshold=50):
    """ Sets all pixels below the given threshold value to zero. """
    img_thr = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO)[1]
    return img_thr

def nonMaxSuppression(image, min_distance=20):
    """ Finds local maxima. """
    coordinates = peak_local_max(image, min_distance=min_distance)
    return coordinates
    
def resizeHm(img, hm):
    """ Resizes a heatmap to the size of a given image. """
    factor = img.shape[0]//hm.shape[0]
    
    hmResized = np.repeat (hm, factor, axis=0) # y
    hmResized = np.repeat (hmResized, factor, axis=1) #x
    hmResized = np.clip (hmResized*2, 0, 1)
    hmResized = hmResized[:, :, np.newaxis]
        
    return hmResized

def findCoordinates(heatmap, threshold=50, radius=20):
    """ Applies a threshold and performs non-maximum supproession to 
    extract coordinates from heatmaps. """
    thr = applyThresholdToHm(heatmap, threshold)
    #plt.imshow(thr)
    #plt.show()
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
    """ Euclidean distance formula weighted by a in x-direction and by b in 
    y-direction. """
    a = 0.54 # put more weight on x-error
    b = 0.46 
    return np.sqrt(a*x*x + b*y*y)


def findHeadTailMatches(heads, tails):
    """ Finds matching heads and tails by optimizing distances using the 
    weighted Euclidean distance measure.
    
    Parameters
    -----------
    heads: list<tuple<int>>
        A list of animal head positions.
    tails: list<tuple<int>>
        A list of animal tail positions.
    """
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
        head_assignment, tail_assignment = linear_sum_assignment(ht_distances)
        matches = np.array([(heads[head_assignment[i]], tails[tail_assignment[i]]) for i in range(len(tail_assignment))])
    return matches 

def scaleMatchCoordinates(matches, input_res, output_res):
    """
    Scales coordinates from an image with input_resolution to an image with 
    output_resolution

    Parameters
    ----------
    matches : list<list<int>>
        One entry depicts the group, head and tail positions of one animal
        on the left and right image.
    input_res : TYPE
        Input resolution.
    output_res : TYPE
        Target resolution.

    Returns
    -------
    ndarray
        List with scaled coordinates.
    """
    xfactor = output_res[0]/input_res[0]
    yfactor = output_res[1]/input_res[1]
    
    scaled_matches = []
    for m in matches:
        m = [[m[0][0]*xfactor, m[0][1]*yfactor], # scale head
             [m[1][0]*xfactor, m[1][1]*yfactor]] # scale tail
        scaled_matches.append(m)
    
    return np.array(scaled_matches)    