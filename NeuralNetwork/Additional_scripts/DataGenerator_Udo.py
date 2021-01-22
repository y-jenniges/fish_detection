#!/usr/bin/python

# coding: utf-8

import numpy as np
import random
import h5py
import cv2
import keras
import os

# Tools to load the training / test set on the fly, so the whole dataset
# doesn't need to be kept in memory.
def dummyPrepareEntry (entry):
    """Dummy function to prepare and entry of the dataset. It takes one entry
     and converts it to a input, ground-truth output pair that is given
     to keras. At the moment the image is loaded and the output is just empty."""
    return (loadImage(entry[0]), [])

class DataGenerator(keras.utils.Sequence):
    """Provides a dataset of the erdbeer to keras in a load on demand fashion
    The dataset must have the format dict filename-->list[dict{"x", "y"}].
    To obtain the actual entry, the filename is loaded and converted to
    an image and the labels passed to a given function to convert it into
    a tensor.
    Adapted from https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly"""
    
    def __init__(self, dataset, prepareEntry=dummyPrepareEntry, batch_size=4, shuffle=True):
        'Initialization'
        self.dataset = dataset
        self.prepareEntry = prepareEntry
        self.batch_size = batch_size
        self.shuffle = shuffle
		
        
    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.dataset) / self.batch_size))
      
    def __getitem__(self, index):
        'Generate one batch of data'
        batch = self.dataset[index*self.batch_size:(index+1)*self.batch_size]
        batch = [self.prepareEntry(e) for e in batch]
        X = np.array([e[0] for e in batch])
        y = np.array([e[1] for e in batch])
        return X, y
        
    def get_ground_truth (self, index):
        'Generate ground_truth for the batch in the original format (not heatmap).'
        batch = self.dataset[index*self.batch_size:(index+1)*self.batch_size]
        return [e[1] for e in batch]          

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        random.shuffle(self.dataset)