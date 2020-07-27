# Tools to load the training / test set on the fly, so the whole dataset
# doesn't need to be kept in memory.

import numpy as np
import keras
import HelperFunctions as helpers
import Globals
import random
import HeatmapClass
import json
import math
import matplotlib.pyplot as plt
import os

def dummyPrepareEntry (entry, hm_folder):
    """Dummy function to prepare an entry of the dataset. It takes one entry
     and converts it to a input, ground-truth output pair that is given
     to keras. At the moment the image is loaded and the output is just empty."""
    return (helpers.loadImage(entry['filename']), [])

def prepareEntryLowResHeatmap (entry, hm_folder=None):
    """Get's an entry of the dataset (filename, annotation), load filename and
    converts annotation into a low-res heatmap. Returning both as x, y pair.
    to be passed to keras."""

    # use precalculated heatmaps, if their folder is specified
    if hm_folder != None:
        hm_file_path = hm_folder + entry['filename'].split("/")[-1].rsplit(".jpg",1)[0] + '.json'    
        with open(hm_file_path, 'r') as f:
            hm_json = json.load(f)
            hm = np.array(hm_json['hm_1f'])
            # todo adapt the precalculated heatmaps! (i.e. clip them to 0-1)
            np.clip (hm, 0, 1, out=hm)
    else:
        #print("Calculating heatmap...")
        hm = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='front')
        #hm.showImageWithHeatmap()
        hm = helpers.downsample(hm.hm)
        
    
    # load image and make its range [-1,1] (suitable for mobilenet)
    image = helpers.loadImage(entry['filename'])
    image = 2.*image/np.max(image) - 1

    heatmaps=[]
    classification=[]
 
    
    heatmaps = hm
    classification = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    # heatmaps.append(hm)
    # classification.append(np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    #helpers.showImageWithHeatmap(image, hm)



    
    # # idea here: return only necessary heatmaps and classes
    # for animal in entry['animals']:
    #     group = math.ceil(animal['group'].index(1)/2)
    #     #group = str(math.floor(animal['group'].index(1)/2))
    #     bodyPart = 'front' if animal['group'].index(1)%2==0 else 'back'
        
    #     hm = HeatmapClass.Heatmap(entry, resolution='low', group=group, bodyPart=bodyPart)
    #     #hm.showImageWithHeatmap()
    #     hm = helpers.downsample(hm.hm)
        
        
    #     # heatmaps.append(hm)
    #     # classification.append(np.array(animal['group']))
    #     # helpers.showImageWithHeatmap(image, hm)
        
    #     # avoid dulicate heatmaps
    #     if len(heatmaps) == 0:
    #         heatmaps.append(hm)
    #         classification.append(np.array(animal['group']))
    #     else:
    #         isContained = False
    #         for h in heatmaps:
    #             if np.array_equal(h, hm):
    #                 isContained = True
                
    #         if not isContained:   
    #             heatmaps.append(hm)
    #             # heatmaps.append(np.array(hm_json["hm_" + group + bodyPart]))
    #             classification.append(np.array(animal['group']))
    #             helpers.showImageWithHeatmap(image, hm)
                    
    
    
    # # if there is no animal on the image, give an all black heatmap (all zeros) and class 0 (nothing)
    # if len(entry['animals']) == 0:
    #     hm = np.zeros(shape=[np.array(hm_json['hm_0f']).shape[0], np.array(hm_json['hm_0f']).shape[1], 1])
    #     heatmaps.append(hm)
    #     c = np.zeros(Globals.NUM_GROUPS*12)
    #     c[0] = 1
    #     classification.append(c)

    # image, groundtrouth(heatmap), classification is returned
    # maybe only heatmaps that are not empty!!
   
    # idea: for all 12 classes, create one heatmap and a classification array
    # hm_strings = ["hm_0f", "hm_0b", "hm_1f", "hm_1b", "hm_2f", "hm_2b", "hm_3f", "hm_3f", "hm_4f", "hm_4b", "hm_5f", "hm_5b"]


    # # append all heatmaps
    # heatmaps = np.zeros(shape=[Globals.NUM_GROUPS*2, np.array(hm_json['hm_0f']).shape[0], np.array(hm_json['hm_0f']).shape[1], 1])
    # for i in range(len(heatmaps)):
    #     heatmaps[i]= np.array(hm_json[hm_strings[i]], dtype=float)
    
    # # initialize the classification (to start with, all images are classified as nothing (group 0))
    # classification=np.zeros(shape=[Globals.NUM_GROUPS*2, Globals.NUM_GROUPS*2])
    # for i in range(len(classification)):
    #     new_entry = np.zeros(Globals.NUM_GROUPS*2)
    #     new_entry[0]=1
    #     classification[i] = new_entry


    # for animal in entry['animals']:
    #     group = str(math.floor(animal['group'].index(1)/2))
    #     bodyPart = 'f' if animal['group'].index(1)%2==0 else 'b'
         
    #     idx = animal['group'].index(1)
    #     classification[idx] = np.asarray(animal['group'])

    # this return is for one heatmap calculations only
    #return (image, helpers.downsample(np.asarray(hm)))


    # print("datagenerator gives back: ")
    # print(heatmaps)
    # print(classification)
    # print(len(heatmaps))
    # print(len(classification))

    #return np.asarray(image), {"heatmap": heatmaps, "classification": classification}
    

    
    return np.asarray(image), np.asarray(heatmaps), np.asarray(classification)

  
    # return [(image, hms['hm_0f']), (image, hms['hm_0b']), (image, hms['hm_1f']), (image, hms['hm_1b']), \
    #         (image, hms['hm_2f']), (image, hms['hm_2b']), (image, hms['hm_3f']), (image, hms['hm_3b']),\
    #         (image, hms['hm_4f']), (image, hms['hm_4b']), (image, hms['hm_5f']), (image, hms['hm_5b'])]
    # return (image, [heatmap0f, heatmap0b, heatmap1f, heatmap1b, heatmap2f, heatmap2b, 
    #                 heatmap3f, heatmap3b, heatmap4f, heatmap4b, heatmap5f, heatmap5b])
    #return (image, heatmap1f.hm)

def prepareEntryHighResHeatmap (entry, hm_folder=None):
    """Get's an entry of the dataset (filename, annotation), load filename and
    converts annotation into a low-res heatmap. Returning both as x, y pair.
    to be passed to keras."""
    
    # filename = entry['filename']
    # annotation = entry['animals']
    
    # heatmap = HeatmapClass.Heatmap(entry, resolution='high', group=1, bodyPart='front')
        # use precalculated heatmaps, if their folder is specified
    if hm_folder != None:
        hm_file_path = hm_folder + entry['filename'].split("/")[-1].rsplit(".jpg",1)[0] + '.json'    
        with open(hm_file_path, 'r') as f:
            hm_json = json.load(f)
            hm = np.array(hm_json['hm_1f'])
            # todo adapt the precalculated heatmaps! (i.e. clip them to 0-1)
            np.clip (hm, 0, 1, out=hm)
    else:
        #print("Calculating heatmap...")
        hm = HeatmapClass.Heatmap(entry, resolution='high', group=1, bodyPart='front')
        #hm.showImageWithHeatmap()
        hm = hm.hm
    
    # load image and make its range [-1,1] (suitable for mobilenet)
    image = helpers.loadImage(entry['filename'])#/np.array(128,dtype=np.float32)-np.array(1,dtype=np.float32)
    #image = helpers.loadImage(entry['filename'])/np.array(128,dtype=np.float32)-np.array(1,dtype=np.float32)
    #image = 2.*(image - np.min(image))/np.ptp(image)-1
    image = 2.*image/np.max(image) - 1

    heatmaps=[]
    classification=[]
    
    heatmaps = hm
    classification = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    
    # # idea here: return only necessary heatmaps and classes
    # for animal in entry['animals']:
    #     group = math.ceil(animal['group'].index(1)/2)
    #     #group = str(math.floor(animal['group'].index(1)/2))
    #     bodyPart = 'front' if animal['group'].index(1)%2==0 else 'back'
        
    #     hm = HeatmapClass.Heatmap(entry, resolution='low', group=group, bodyPart=bodyPart)
    #     hm.showImageWithHeatmap()
        
    #     heatmaps.append(hm)
    #     # heatmaps.append(np.array(hm_json["hm_" + group + bodyPart]))
    #     classification.append(np.array(animal['group']))
        
    # for animal in entry['animals']:
    #     group = str(math.floor(animal['group'].index(1)/2))
    #     bodyPart = 'f' if animal['group'].index(1)%2==0 else 'b'
        
    #     heatmaps.append(hm_json["hm_" + group + bodyPart])
    #     classification.append(animal['group'])
       

    return np.asarray(image), np.asarray(heatmaps), np.asarray(classification)
    #return (image, np.asarray(hm))
    #return [image, heatmaps, classification]
    
    # return [(image, hms['hm_0f']), (image, hms['hm_0b']), (image, hms['hm_1f']), (image, hms['hm_1b']), \
    #         (image, hms['hm_2f']), (image, hms['hm_2b']), (image, hms['hm_3f']), (image, hms['hm_3b']),\
    #         (image, hms['hm_4f']), (image, hms['hm_4b']), (image, hms['hm_5f']), (image, hms['hm_5b'])]
               
    #return (helpers.loadImage(filename)/np.array(128,dtype=np.float32)-np.array(1,dtype=np.float32), heatmap.hm)


def showEntryOfGenerator(dataGen, i, showHeatmaps=False):
    """Fetches the first batch, prints dataformat statistics and 
    shows the first entry both as image X and annotation y."""    
    X, y = dataGen[i]
    
    # eLo = helpers.entropy(y)
    # eHi = helpers.entropy(np.mean(y, axis=(0,1,2)))
    
    # print(f"X has shape {X.shape}, type {X.dtype} and range [{np.min(X):.3f}..{np.max(X):.3f}]") 
    #print(f"y has shape {y.shape}, type {y.dtype} and range [{np.min(y):.3f}..{np.max(y):.3f}] and entropy [{eLo:.7f}..{eHi:.7f}]")
    
    # print(type(y))
    # print("laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    
    # print(y[0]['classification'].shape)
    # print(y[1]['classification'].shape)
    # print(y[2]['classification'].shape)
    # print(y[3]['classification'].shape)
    #print(y['heatmap'].shape)
    #print(y['classification'].shape)
   #print(f"len of y: {len(y)} and shape of y[0]: {y[0].shape}")
    #print(f"y['heatmap'] has shape {y['heatmap'].shape}, y ['classification'] has shape {y['classification'].shape}")
    #print(f"classification is {y['classification']}")
    print(f"X has shape {X.shape}, type {X.dtype} and range [{np.min(X):.3f}..{np.max(X):.3f}]") 


    # todo how to i know the resolution
    if showHeatmaps:
        # hm_folder_path = "../data/heatmaps_lowRes/"
        # hm_file_path = hm_folder_path + entry['filename'].split("/")[-1].rsplit(".jpg",1)[0] + '.json'    
        # with open(hm_file_path, 'r') as f:
        #     hms = json.load(f)
            
        # show heatmap for 2 batches
        for j in range(2):
            #print(j)
            #print(X[i])
            helpers.showImageWithHeatmap (X[i], y[i][j])

        

class DataGenerator(keras.utils.Sequence):
    """Provides a dataset of the erdbeer to keras in a load on demand fashion
    The dataset must have the format dict filename-->list[dict{"x", "y"}].
    To obtain the actual entry, the filename is loaded and converted to
    an image and the labels passed to a given function to convert it into
    a tensor.
    Adapted from https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly"""
    
    def __init__(self, dataset, hm_folder_path=None, no_animal_dataset=[], no_animal_ratio=0, prepareEntry=dummyPrepareEntry, batch_size=4, shuffle=True):
        #print("DataGenerator: init")
        'Initialization'
        
        self.hm_folder_path = hm_folder_path
        self.dataset = dataset
        self.no_animal_dataset = no_animal_dataset 
        self.no_animal_ratio = no_animal_ratio
        self.prepareEntry = prepareEntry
        self.batch_size = batch_size
        self.shuffle = shuffle
                       
        self.no_animal_size = (int)(batch_size*no_animal_ratio)     
        self.animal_size = batch_size - self.no_animal_size
               
        self.on_epoch_end()
        
    def __len__(self):
        #print("DataGenerator: len")
        'Denotes the number of batches per epoch'
        #return int(np.floor(len(self.dataset) / self.batch_size))
        #print(f"self.animal_size {self.animal_size}\nself.no_animal_size {self.no_animal_size}\nself.batch_size {self.batch_size}\n")_

        number_of_images = np.floor(len(self.dataset) + (len(self.dataset)/self.batch_size)*self.no_animal_size)
        #print(f"number_of_images {number_of_images}")

        return int(np.floor(number_of_images/self.batch_size))
        #return int((np.floor(len(self.dataset)) + np.floor(self.no_animal_ratio*len(self.no_animal_dataset)))/ self.batch_size)
      
    def __getitem__(self, index):
        #print("DataGenerator: getitem")
        'Generate one batch of data'
        
        no_animal_hm_path = os.path.join(self.hm_folder_path, "../training_no_animals/") if self.hm_folder_path != None else None

        
        batch_animals = self.dataset[index*self.animal_size:(index+1)*self.animal_size] 
        batch_no_animals = self.no_animal_dataset[index*self.no_animal_size:(index+1)*self.no_animal_size]
             
        batch_animals = [self.prepareEntry(e, self.hm_folder_path) for e in batch_animals]
        batch_no_animals = [self.prepareEntry(e, no_animal_hm_path) for e in batch_no_animals]
            
        batch = batch_animals + batch_no_animals
        
        X = np.array([e[0] for e in batch])
        heatmaps = np.array([e[1] for e in batch])
        classification = np.array([e[2] for e in batch])
        #y = {'heatmap': np.array([e[1] for e in batch]), 'classification': np.array([e[2] for e in batch])}
        
        #print(f"y[heatmap] shape {np.array(y['heatmap']).shape}")

        #print(f"heatmaps shape {np.asarray(heatmaps).shape}")
        #print(f"heatmaps[0] shape {np.asarray(heatmaps[0]).shape}")

        return X, {"heatmap": heatmaps, "classification": classification}
        #return X, [heatmaps, classification]
        #return X, heatmaps
        
    def get_ground_truth (self, index):
        #print("DataGenerator: get_ground_truth")
        'Generate ground_truth for the batch in the original format (not heatmap).'
        batch_animals = self.dataset[index*self.animal_size:(index+1)*self.animal_size]
        batch_no_animals = self.no_animal_dataset[index*self.no_animal_size:(index+1)*self.no_animal_size]
        batch = batch_animals + batch_no_animals
        
        return [e['animals'] for e in batch]          

    def on_epoch_end(self):
        #print("DataGenerator: on_epoch_end")
        'Updates indexes after each epoch'
        random.shuffle(self.dataset)
        random.shuffle(self.no_animal_dataset)

		
	
