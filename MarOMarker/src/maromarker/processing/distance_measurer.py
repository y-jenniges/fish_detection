import numpy as np
import cv2

"""
Implemented by Timo Jasper in his Bachelor thesis 'Erkennen und Vermessen 
von Meereslebewesen auf Stereo-Kamerabildern mit einem neuronalen Netz' (2019)
"""
class DistanceMeasurer():
    """ Calculator for distances between points in calibrated stereo-camera images"""
    def __init__(self, c_L, d_L, c_R, d_R, rotation, translation, img_size):
        self.c_L = np.array(c_L)
        self.d_L = np.array(d_L)
        self.c_R = np.array(c_R)
        self.d_R = np.array(d_R)
        self.rotation = np.array(rotation)
        self.translation = np.array(translation)
        
        R1 = np.zeros((3, 3))
        R2 = np.zeros((3, 3))
        self.P1 = np.zeros((3, 4))
        self.P2 = np.zeros((3, 4))

        cv2.stereoRectify(self.c_L, self.d_L, self.c_R, self.d_R, img_size,
                          self.rotation, self.translation, R1, R2,
                          self.P1, self.P2, Q=None,
                          flags=cv2.CALIB_ZERO_DISPARITY, alpha=1, newImageSize=(0, 0))
            
    def distances(self, img_points_L0, img_points_L1, img_points_R0, img_points_R1):
        """ Get points in image space with shape Nx2
        return distances of given points in image space
        if positions in one of the images are 0, return "NaN" as that distance
        """
        distances = []
        
        world_points0 = cv2.triangulatePoints(self.P1, self.P2, np.transpose(img_points_L0), np.transpose(img_points_R0))
        world_points1 = cv2.triangulatePoints(self.P1, self.P2, np.transpose(img_points_L1), np.transpose(img_points_R1))
        #print("world_points: ", world_points0, world_points1)
        
        for i in range(world_points0.shape[1]):
            
            if not (np.any(img_points_L0[i]) or np.any(img_points_L1[i])) or not (np.any(img_points_R0[i]) or np.any(img_points_R1[i])):
                # dont calculate distances for objects in just 1 img
                distances.append("NaN")
            else:
                #convert homogen coordinates to cartesian coordiantes
                p0 = np.array([(world_points0[0,i]/world_points0[3,i]),
                               (world_points0[1,i]/world_points0[3,i]),
                               (world_points0[2,i]/world_points0[3,i])])
                p1 = np.array([world_points1[0,i]/world_points1[3,i],
                               world_points1[1,i]/world_points1[3,i],
                               world_points1[2,i]/world_points1[3,i]])
                #print("p0,p1:",p0, p1)
                distances.append(cv2.norm(p0, p1, normType=cv2.NORM_L2))
            
        return distances
