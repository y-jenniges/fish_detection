# Tools to load the training / test set on the fly, so the whole dataset
# doesn't need to be kept in memory.

import numpy as np
import keras
import HelperFunctions as helpers
import random
import HeatmapClass

def dummyPrepareEntry (entry):
    """Dummy function to prepare an entry of the dataset. It takes one entry
     and converts it to a input, ground-truth output pair that is given
     to keras. At the moment the image is loaded and the output is just empty."""
    return (helpers.loadImage(entry['filename']), [])

def prepareEntryLowResHeatmap (entry):
    """Get's an entry of the dataset (filename, annotation), load filename and
    converts annotation into a low-res heatmap. Returning both as x, y pair.
    to be passed to keras."""
    
    filename = entry['filename']
    annotation = entry['animals']
    
    # todo das hier sind alle heatmaps für ein Bild, wie gebe ich das dem netz?
    heatmap1f = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='front')
    heatmap1b = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='back')
    heatmap2f = HeatmapClass.Heatmap(entry, resolution='low', group=2, bodyPart='front')
    heatmap2b = HeatmapClass.Heatmap(entry, resolution='low', group=2, bodyPart='back')
    heatmap3f = HeatmapClass.Heatmap(entry, resolution='low', group=3, bodyPart='front')
    heatmap3b = HeatmapClass.Heatmap(entry, resolution='low', group=3, bodyPart='back')
    heatmap4f = HeatmapClass.Heatmap(entry, resolution='low', group=4, bodyPart='front')
    heatmap4b = HeatmapClass.Heatmap(entry, resolution='low', group=4, bodyPart='back')
    heatmap5f = HeatmapClass.Heatmap(entry, resolution='low', group=5, bodyPart='front')
    heatmap5b = HeatmapClass.Heatmap(entry, resolution='low', group=5, bodyPart='back')
    heatmap6f = HeatmapClass.Heatmap(entry, resolution='low', group=6, bodyPart='front')
    heatmap6b = HeatmapClass.Heatmap(entry, resolution='low', group=6, bodyPart='back')
    
    image = helpers.loadImage(filename)/np.array(128,dtype=np.float32)-np.array(1,dtype=np.float32)
    
    # return [(image, heatmap1f), (image, heatmap1b), (image, heatmap2f), (image, heatmap2b), (image, heatmap3f), (image, heatmap3b), 
    #         (image, heatmap4f), (image, heatmap4b), (image, heatmap5f), (image, heatmap5b), (image, heatmap6f), (image, heatmap6b)]
    return (image, [heatmap1f, heatmap1b, heatmap2f, heatmap2b, heatmap3f, heatmap3b, heatmap4f, heatmap4b, heatmap5f, heatmap5b, heatmap6f, heatmap6b])
    #return (image, heatmap1f.hm)

def prepareEntryHighResHeatmap (entry):
    """Get's an entry of the dataset (filename, annotation), load filename and
    converts annotation into a low-res heatmap. Returning both as x, y pair.
    to be passed to keras."""
    
    filename = entry['filename']
    annotation = entry['animals']
    
    heatmap = HeatmapClass.Heatmap(entry, resolution='high', group=1, bodyPart='front')
    
    return (helpers.loadImage(filename)/np.array(128,dtype=np.float32)-np.array(1,dtype=np.float32), heatmap.hm)


def showEntryOfGenerator(dataGen,i):
    """Fetches the first batch, prints dataformat statistics and 
    shows the first entry both as image X and annotation y."""    
    X, y = dataGen[i]
    print(f"X has shape{X.shape}, type {X.dtype} and range [{np.min(X)}..{np.max(X)}]")
    print(f"y has shape{y.shape}, type {y.dtype} and range [{np.min(y)}..{np.max(y)}]")
    
    # if heatmap != None:
    #     heatmap.showImageWithHeatmap (X[i], y[i]) 



class DataGenerator(keras.utils.Sequence):
    """Provides a dataset of the erdbeer to keras in a load on demand fashion
    The dataset must have the format dict filename-->list[dict{"x", "y"}].
    To obtain the actual entry, the filename is loaded and converted to
    an image and the labels passed to a given function to convert it into
    a tensor.
    Adapted from https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly"""
    
    def __init__(self, dataset, no_animal_dataset=[], no_animal_ratio=0, prepareEntry=dummyPrepareEntry, batch_size=4, shuffle=True):
        'Initialization'
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
        'Denotes the number of batches per epoch'
        #return int(np.floor(len(self.dataset) / self.batch_size))
        print(f"self.animal_size {self.animal_size}\nself.no_animal_size {self.no_animal_size}\nself.batch_size {self.batch_size}")
        return int((np.floor(len(self.dataset)) + np.floor(len(self.no_animal_dataset)))/ self.batch_size)
      
    def __getitem__(self, index):
        'Generate one batch of data'
        batch_animals = self.dataset[index*self.animal_size:(index+1)*self.animal_size] 
        batch_no_animals = self.no_animal_dataset[index*self.no_animal_size:(index+1)*self.no_animal_size]
        
        batch_animals = [self.prepareEntry(e) for e in batch_animals]
        batch_no_animals = [self.prepareEntry(e) for e in batch_no_animals]
        
        batch = batch_animals + batch_no_animals

        X = np.array([e[0] for e in batch])
        y = np.array([e[1] for e in batch])
             
        return X, y
        
    def get_ground_truth (self, index):
        'Generate ground_truth for the batch in the original format (not heatmap).'
        batch_animals = self.dataset[index*self.animal_size:(index+1)*self.animal_size]
        batch_no_animals = self.no_animal_dataset[index*self.no_animal_size:(index+1)*self.no_animal_size]
        batch = batch_animals + batch_no_animals
        
        return [e['animals'] for e in batch]          

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        random.shuffle(self.dataset)
        random.shuffle(self.no_animal_dataset)

		
	