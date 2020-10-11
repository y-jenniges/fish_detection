import json
import os
import numpy as np
import tensorflow as tf
import keras
import HelperFunctions as helpers
import HeatmapClass
import DataGenerator as dg
from tensorflow import random
#from tensorflow import set_random_seed
from keras import backend as K

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
random.set_seed(2)
#set_random_seed(2)

BATCH_SIZE = 1

test_path = "../data/output/700/"
model_path = "model-L"


def weighted_categorical_crossentropy(weights):
    """
    A weighted version of keras.objectives.categorical_crossentropy
    
    Variables:
        weights: numpy array of shape (C,) where C is the number of classes
    
    Usage:
        weights = np.array([0.5,2,10]) # Class one at 0.5, class 2 twice the normal weights, class 3 10x.
        loss = weighted_categorical_crossentropy(weights)
        model.compile(loss=loss,optimizer='adam')
    Taken from:
        https://gist.github.com/wassname/ce364fddfc8a025bfab4348cf5de852d
    """
    
    weights = K.variable(weights)
        
    def loss(y_true, y_pred):
        # scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
        # clip to prevent NaN's and Inf's
        y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
        # calc
        loss = y_true * K.log(y_pred) * weights
        loss = -K.sum(loss, -1)
        return loss
    
    return loss

# load annotation files
label_root = "../data/maritime_dataset_25/labels/"

path = "test_labels.json"
with open(os.path.join(label_root, path), 'r') as f:
    test_labels = json.load(f)
    
test, train, train_no, val, cv = helpers.loadAndSplitLabels(label_root)
weights = np.array(list(cv.values()))

fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fish_labels = helpers.filter_labels_for_animal_group(test_labels, fish_id)

crust_id = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
crust_labels = helpers.filter_labels_for_animal_group(test_labels, crust_id)

chaetognatha_id = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
chaeto_labels = helpers.filter_labels_for_animal_group(test_labels, chaetognatha_id)

unidentified_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]  
unidentified_labels = helpers.filter_labels_for_animal_group(test_labels, unidentified_id)

jellyfish_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
jellyfish_labels = helpers.filter_labels_for_animal_group(test_labels, jellyfish_id)

#test_labels[:4]
    
# load model
#model = keras.models.load_model(os.path.join(test_path,model_path))
model = keras.models.load_model(os.path.join(test_path,model_path), custom_objects={"loss": weighted_categorical_crossentropy(weights)})



testGen = dg.DataGenerator (dataset=test_labels, 
                            prepareEntry=dg.prepareEntryLowResHeatmap,
                            batch_size=BATCH_SIZE,
                            shuffle=False)

# evaluate on test data
print("Evaluate on test data")
results = model.evaluate_generator(testGen, verbose=1)#)#, len(test_labels)//BATCH_SIZE)
print("test loss, test acc:", results)

# # minimalistic CNN
# def generateY(entry):
#     # load image and make its range [-1,1] (suitable for mobilenet)
#     image = helpers.loadImage(entry['filename'], 32)
#     image = 2.*image/np.max(image) - 1

#     heatmaps=[]

#     # fish head only
#     hm = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart="front")
#     hm.downsample(32)
    
#     heatmaps = hm.hm
#     return np.asarray(image), np.asarray(heatmaps)

# x_test = []
# y_test = []

# print("generating heatmaps...")
# heatmaps=[]
# for entry in test_labels:
#     img, hms = generateY(entry)
#     x_test.append(img)
#     heatmaps.append(hms)
# print("assingning x and y...")
# y_test = np.asarray(heatmaps)
# x_test = np.asarray(x_test)

# print("Evaluate on test data")
# results = model.evaluate(x_test, y_test, batch_size=BATCH_SIZE, verbose=1)
# print("test loss, test mae:", results)
