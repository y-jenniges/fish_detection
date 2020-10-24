"""
Adapted from lecture "Anwendungen der Bildverarbeitung" by Udo Frese, 
University Bremen, 2019

It offers tools to load the training/validation/test set on the fly, so the 
whole dataset doesn't need to be kept in memory.
"""
import numpy as np
import random
import keras
import HeatmapClass
import HelperFunctions as helpers
# from tensorflow import random 
from tensorflow import set_random_seed

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
#random.set_seed(2)
set_random_seed(2)

OPTION = "vector_fields" 
# "fish_heads"
# "all_animals"
# "body_segmentation"
# "vector_fields" 
# "vector_fields_weighted"

def dummyPrepareEntry (entry, hm_folder):
    """Dummy function to prepare an entry of the dataset. It takes one entry
     and converts it to a input, ground-truth output pair that is given
     to keras. At the moment the image is loaded and the output is just empty."""
    print("dummy prepare entry")
    return (helpers.loadImage(entry['filename']), [])
    
def generateAllHeatmaps(entry, res='low'):
    """ Generates heatmaps, vector fields, segmentation information accroding
    to chosen option and resolution (low is 1/32 and high is 1/2 of the
    original resolution)."""
    hm_1_head = HeatmapClass.Heatmap(entry, resolution=res, group=1, bodyPart="front")
    hm_1_tail = HeatmapClass.Heatmap(entry, resolution=res, group=1, bodyPart="back")
    hm_1_body = HeatmapClass.Heatmap(entry, resolution=res, group=1, bodyPart="connection")
    
    hm_2_head = HeatmapClass.Heatmap(entry, resolution=res, group=2, bodyPart="front")
    hm_2_tail = HeatmapClass.Heatmap(entry, resolution=res, group=2, bodyPart="back")
    hm_2_body = HeatmapClass.Heatmap(entry, resolution=res, group=2, bodyPart="connection")
    
    hm_3_head = HeatmapClass.Heatmap(entry, resolution=res, group=3, bodyPart="front")
    hm_3_tail = HeatmapClass.Heatmap(entry, resolution=res, group=3, bodyPart="back")
    hm_3_body = HeatmapClass.Heatmap(entry, resolution=res, group=3, bodyPart="connection")
    
    hm_4_head = HeatmapClass.Heatmap(entry, resolution=res, group=4, bodyPart="front")
    hm_4_tail = HeatmapClass.Heatmap(entry, resolution=res, group=4, bodyPart="back")
    hm_4_body = HeatmapClass.Heatmap(entry, resolution=res, group=4, bodyPart="connection")
    
    hm_5_head = HeatmapClass.Heatmap(entry, resolution=res, group=5, bodyPart="front")
    hm_5_tail = HeatmapClass.Heatmap(entry, resolution=res, group=5, bodyPart="back")
    hm_5_body = HeatmapClass.Heatmap(entry, resolution=res, group=5, bodyPart="connection")
                  
    # downsampling
    if res=="low": f=32
    else: f=2
    hm_1_head.downsample(f)
    hm_1_tail.downsample(f)
    hm_1_body.downsample(f)
    hm_2_head.downsample(f)
    hm_2_tail.downsample(f)
    hm_2_body.downsample(f)
    hm_3_head.downsample(f)
    hm_3_tail.downsample(f)
    hm_3_body.downsample(f)
    hm_4_head.downsample(f)
    hm_4_tail.downsample(f)
    hm_4_body.downsample(f)
    hm_5_head.downsample(f)
    hm_5_tail.downsample(f)
    hm_5_body.downsample(f)
    
    # head and tail vectors
    head_vectors, tail_vectors = helpers.get_head_tail_vectors(entry, 32, 200, f)
    
    # head and tail heatmaps
    hm_heads = helpers.sumHeatmaps([hm_1_head.hm, hm_2_head.hm, hm_3_head.hm, 
                                    hm_4_head.hm, hm_5_head.hm])
    hm_tails = helpers.sumHeatmaps([hm_1_tail.hm, hm_2_tail.hm, hm_3_tail.hm, 
                                    hm_4_tail.hm, hm_5_tail.hm])
    
    # assemble body heatmap by adding all separate body heatmaps
    hm_body = helpers.sumHeatmaps([hm_1_body.hm, hm_2_body.hm, 
                                   hm_3_body.hm, hm_4_body.hm, hm_5_body.hm])
    
    # nothing heatmap
    #@todo pay attention here!!!!!!!!!!! worth another test round to see if 
    # including hm_body improves sth for vectors (usually it should only be 
    # included in nothing heatmap for segmentation option)
    hm_y, hm_x = hm_1_head.hm.shape[0], hm_1_head.hm.shape[1]
    hm_0 = np.ones((hm_y, hm_x, 1), dtype=np.float32)
    hm_0 -= hm_1_head.hm + hm_1_tail.hm + \
            hm_2_head.hm + hm_2_tail.hm + \
            hm_3_head.hm + hm_3_tail.hm + \
            hm_4_head.hm + hm_4_tail.hm + \
            hm_5_head.hm + hm_5_tail.hm + hm_body 
    hm_0 = np.clip (hm_0, 0, 1, out=hm_0)

    if OPTION == "all_animals":
        return [hm_0, 
            hm_1_head.hm, hm_1_tail.hm, 
            hm_2_head.hm, hm_2_tail.hm,
            hm_3_head.hm, hm_3_tail.hm,
            hm_4_head.hm, hm_4_tail.hm,
            hm_5_head.hm, hm_5_tail.hm]
    elif OPTION == "body_segmentation":
        return [hm_0, 
                hm_1_head.hm, hm_1_tail.hm, 
                hm_2_head.hm, hm_2_tail.hm,
                hm_3_head.hm, hm_3_tail.hm,
                hm_4_head.hm, hm_4_tail.hm,
                hm_5_head.hm, hm_5_tail.hm,
                ], hm_body
    elif OPTION == "vector_fields":
        return [hm_0, 
                hm_1_head.hm, hm_1_tail.hm, 
                hm_2_head.hm, hm_2_tail.hm,
                hm_3_head.hm, hm_3_tail.hm,
                hm_4_head.hm, hm_4_tail.hm,
                hm_5_head.hm, hm_5_tail.hm,
                ], [head_vectors, tail_vectors]
    elif OPTION == "vector_fields_weighted":
        return [hm_0, 
                hm_1_head.hm, hm_1_tail.hm, 
                hm_2_head.hm, hm_2_tail.hm,
                hm_3_head.hm, hm_3_tail.hm,
                hm_4_head.hm, hm_4_tail.hm,
                hm_5_head.hm, hm_5_tail.hm,
                ], [head_vectors, tail_vectors, hm_heads, hm_tails]
    else:
        return

def generateFishHeadHeatmaps(entry, res="low"):
    """ Creates the fish head heatmap in the desired resolution 
    (low is 1/32 and high is 1/2 of original resolution). """
    # generate fish head heatmap
    hm_1_head = HeatmapClass.Heatmap(entry, resolution=res, group=1, bodyPart="front")
    
    # perform downsampling
    if res=="low": 
        f=32
    else: 
        f=2
    hm_1_head.downsample(f)
    
    return hm_1_head.hm


def prepareEntryHeatmap (entry, res="low"):
    """Get's an entry of the dataset (filename, annotation), load filename and
    converts annotation into a heatmap in desired resolution 
    (low:1/32, high:1/2). Returning both as x, y pair to be passed to keras."""

    # load image and make its range [-1,1] (suitable for mobilenet)
    image = helpers.loadImage(entry['filename'], 32)
    image = 2.*image/np.max(image) - 1
    
    # generate y depending on option
    if OPTION == "fish_heads":
        heatmap = generateFishHeadHeatmaps(entry, res=res)
        return np.asarray(image), np.asarray(heatmap)
    
    elif OPTION == "all_animals":
        heatmaps = generateAllHeatmaps(entry, res=res) 
        heatmaps = np.concatenate(heatmaps, axis=2) # concat heatmaps
        return np.asarray(image), np.asarray(heatmaps)
        
    elif OPTION == "body_segmentation":
        heatmaps, hm_body = generateAllHeatmaps(entry, res=res)
         # concatenate heatmaps
        heatmaps = np.concatenate(heatmaps, axis=2)
        
        return np.asarray(image), np.asarray(heatmaps), np.asarray(hm_body)
    
    elif OPTION == "vector_fields" or OPTION == "vector_fields_weighted":
        heatmaps, vectors = generateAllHeatmaps(entry, res=res)

        # concatenate heatmaps, vectors
        heatmaps = np.concatenate(heatmaps, axis=2)
        vectors = np.concatenate(vectors, axis=2)
        
        return np.asarray(image), np.asarray(heatmaps), np.asarray(vectors)
    else:
        print("Error: unknown option in data generator in prepareEntry!")
        return 
  
def prepareEntryLowResHeatmap(entry):
    return prepareEntryHeatmap(entry, "low")

def prepareEntryHighResHeatmap (entry):
    return prepareEntryHeatmap(entry, "high")
    
def showEntryOfGenerator(dataGen, i, showHeatmaps=False):
    """Fetches the first batch and prints dataformat statistics. """    

    X, y = dataGen[i]
    
    # eLo = helpers.entropy(y)
    # eHi = helpers.entropy(np.mean(y, axis=(0,1,2)))
    
    # print(f"X has shape {X.shape}, type {X.dtype} and range [{np.min(X):.3f}..{np.max(X):.3f}]") 
    #print(f"y has shape {y.shape}, type {y.dtype} and range [{np.min(y):.3f}..{np.max(y):.3f}] and entropy [{eLo:.7f}..{eHi:.7f}]")
    

    print(f"X has shape {X.shape}, type {X.dtype} and range [{np.min(X):.3f}..{np.max(X):.3f}]") 
    
    if OPTION == "fish_heads" or OPTION == "all_animals":
        print(f"Y has shape {y.shape}")
    elif OPTION == "vector_fields" or OPTION == "vector_fields_weighted":
        print(f"y['heatmap'] has shape {y['heatmap'].shape}, y ['vectors'] has shape {y['vectors'].shape}")
    elif OPTION == "body_segmentation":
        print(f"y['heatmap'] has shape {y['heatmap'].shape}, y ['segmentation'] has shape {y['segmentation'].shape}")


class DataGenerator(keras.utils.Sequence):
    """Provides a dataset of the erdbeer to keras in a load on demand fashion
    The dataset must have the format dict filename-->list[dict{"x", "y"}].
    To obtain the actual entry, the filename is loaded and converted to
    an image and the labels passed to a given function to convert it into
    a tensor.
    Adapted from https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly"""
    
    def __init__(self, dataset, hm_folder_path=None, no_animal_dataset=[], no_animal_ratio=0, prepareEntry=dummyPrepareEntry, batch_size=4, shuffle=True):
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
        'Denotes the number of batches per epoch'
        number_of_images = np.floor(len(self.dataset) + (len(self.dataset)/self.batch_size)*self.no_animal_size)

        return int(np.floor(number_of_images/self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'   
        batch_animals = self.dataset[index*self.animal_size:(index+1)*self.animal_size] 
        batch_no_animals = self.no_animal_dataset[index*self.no_animal_size:(index+1)*self.no_animal_size]
             
        batch_animals = [self.prepareEntry(e) for e in batch_animals]
        batch_no_animals = [self.prepareEntry(e) for e in batch_no_animals]
            
        batch = batch_animals + batch_no_animals
        
        X = np.array([e[0] for e in batch])
        
        # get y depending on option
        if OPTION == "fish_heads":
            heatmaps = np.array([e[1] for e in batch])
            return X, heatmaps
        
        elif OPTION == "all_animals":
            heatmaps = np.array([e[1] for e in batch])
            return X, heatmaps
            
        elif OPTION == "body_segmentation":
            heatmaps = np.array([e[1] for e in batch])
            hm_body = np.array([e[2] for e in batch])
            return X, {"heatmap": heatmaps, "segmentation": hm_body}
        
        elif OPTION == "vector_fields" or OPTION == "vector_fields_weighted":
            heatmaps = np.array([e[1] for e in batch])
            vectors = np.array([e[2] for e in batch])
            return X, {"heatmap": heatmaps, "vectors": vectors}
        
        else:
            print("Error: unknown option in data generator, get_item!")
            return 
        
    def get_ground_truth (self, index):
        'Generate ground_truth for the batch in the original format (not heatmap).'
        batch_animals = self.dataset[index*self.animal_size:(index+1)*self.animal_size]
        batch_no_animals = self.no_animal_dataset[index*self.no_animal_size:(index+1)*self.no_animal_size]
        batch = batch_animals + batch_no_animals
        
        return [e['animals'] for e in batch]          

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        if self.shuffle:
            random.shuffle(self.dataset)
            random.shuffle(self.no_animal_dataset)