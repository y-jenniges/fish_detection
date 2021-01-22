#!/usr/bin/python

# coding: utf-8

import numpy as np
import random
import h5py
import cv2
import keras
import os

class DataGenerator(keras.utils.Sequence):
    """ generates batches from disjunct random data with animals
    and ratio (%) without animals on it

    use data_type as "train", "validation", "test" to specify the generated type of data
    """
    def __init__(self, no_animal_ratio, batch_size, path, dataType = "train"):
        """Initialization"""
        self.batch_size = batch_size
        self.no_animal_ratio = no_animal_ratio
        self.data_type = dataType
        self.indices_val = []
        self.indices_test = []
        self.indices_animals = []
        self.indices_no_animals = []
        self.path = path
        self.animal_size = (int)(batch_size-(batch_size*no_animal_ratio))
        self.no_animal_size = batch_size - self.animal_size
        self.on_epoch_end()

    def __len__(self):
        """Denotes the number of batches per epoch"""
        if self.data_type == "validation":
            validation_images_size = len(os.listdir(self.path+"validation_data/"))
            return (int)(validation_images_size / self.batch_size)-1
        if self.data_type == "test":
            test_images_size = len(os.listdir(self.path+"test_data/"))
            return (int)(test_images_size / self.batch_size)-1
        training_animal_size = len(os.listdir(self.path+"training_data_animals/")) 
        return (int)(training_animal_size / self.animal_size)-1

    def __getitem__(self, idx):
        """Generate one batch of data"""
        if self.data_type == "validation":
            with h5py.File(self.path+"validation_labels.h5", "r") as f:
                batch_labels = np.empty((self.batch_size, 15, 15, 10),dtype=np.float32)
                batch_data = np.empty((self.batch_size,480,480,3),dtype=np.uint8)
                b_i = 0 # index of batch for adding images
                for i in self.indices_val[idx*self.batch_size : (idx+1)*self.batch_size]:
                    batch_labels[b_i] = np.array(f["validation_labels"][i])
                    batch_data[b_i] = np.array(cv2.imread(self.path+"validation_data/"+str(i)+".jpg"))
                    b_i += 1
            return batch_data, {'classification': batch_labels[:,:,:,:6], 'localization': batch_labels[:,:,:,-4:]}
        elif self.data_type == "test":
            with h5py.File(self.path+"test_labels.h5", "r") as f:
                batch_labels = np.empty((self.batch_size, 15, 15, 10),dtype=np.float32)
                batch_data = np.empty((self.batch_size,480,480,3),dtype=np.uint8)
                b_i = 0 # index of batch for adding images
                for i in self.indices_test[idx*self.batch_size : (idx+1)*self.batch_size]:
                    batch_labels[b_i] = np.array(f["test_labels"][i])
                    batch_data[b_i] = np.array(cv2.imread(self.path+"test_data/"+str(i)+".jpg"))
                    b_i += 1
            return batch_data, {'classification': batch_labels[:,:,:,:6], 'localization': batch_labels[:,:,:,-4:]}
        elif self.data_type == "train":
            batch_labels = np.empty((self.batch_size, 15, 15, 10),dtype=np.float32)
            batch_data = np.empty((self.batch_size,480,480,3),dtype=np.uint8)
            b_i = 0 # index of batch for adding samples
            with h5py.File(self.path+"training_labels_animals.h5", "r") as f:
                for i in self.indices_animals[idx*self.animal_size : (idx+1)*self.animal_size]:
                    #data augmentation
                    if random.choice([True, False]):
                        batch_labels[b_i] = np.flip(f["training_labels_animals"][i],1)
                        batch_data[b_i] = np.flip(cv2.imread(self.path+"training_data_animals/"+str(i)+".jpg"),1)
                    else:
                        batch_labels[b_i] = np.array(f["training_labels_animals"][i])
                        batch_data[b_i] = np.array(cv2.imread(self.path+"training_data_animals/"+str(i)+".jpg"))
                    b_i += 1
            with h5py.File(self.path+"training_labels_no_animals.h5", "r") as f:
                for i in self.indices_no_animals[idx*self.no_animal_size : (idx+1)*self.no_animal_size]:
                    batch_labels[b_i] = np.array(f["training_labels_no_animals"][i])
                    batch_data[b_i] = np.array(cv2.imread(self.path+"training_data_no_animals/"+str(i)+".jpg"))
                    b_i += 1
            return batch_data, {'classification': batch_labels[:,:,:,:6], 'localization': batch_labels[:,:,:,-4:]}
    
    def on_epoch_end(self):
        if self.data_type == "validation":
            with h5py.File(self.path+"validation_labels.h5", "r") as f:
                self.indices_val = [i for i in range(f.get("validation_labels").shape[0])]
        elif self.data_type == "test":
            with h5py.File(self.path+"test_labels.h5", "r") as f:
                self.indices_test = [i for i in range(f.get("test_labels").shape[0])]
        elif self.data_type == "train":
            with h5py.File(self.path+"training_labels_animals.h5", "r") as f:
                self.indices_animals = [i for i in range(f.get("training_labels_animals").shape[0])]
            random.shuffle(self.indices_animals)
            with h5py.File(self.path+"training_labels_no_animals.h5", "r") as f:
                self.indices_no_animals = [i for i in range(f.get("training_labels_no_animals").shape[0])]
            random.shuffle(self.indices_no_animals)
        else:
            print("invalid data_type")
            return None
