import json
import os
import numpy as np
import tensorflow as tf
import keras
import HelperFunctions as helpers
import HeatmapClass
import DataGenerator as dg
#from tensorflow import random
from tensorflow import set_random_seed
from keras import backend as K
import Losses

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
#random.set_seed(2)
set_random_seed(2)

BATCH_SIZE = 1

test_path = "../data/output/900/"
model_path = "model-H"


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
model = keras.models.load_model(os.path.join(test_path,model_path), custom_objects={"loss": Losses.weighted_categorical_crossentropy(weights)})


#prepareEntry = dg.prepareEntryLowResHeatmap
prepareEntry=dg.prepareEntryHighResHeatmap

testGen = dg.DataGenerator (dataset=test_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)

tfi = dg.DataGenerator (dataset=fish_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tcr = dg.DataGenerator (dataset=crust_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tch = dg.DataGenerator (dataset=chaeto_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tje = dg.DataGenerator (dataset=jellyfish_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tun = dg.DataGenerator (dataset=unidentified_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)

gens = [testGen, tfi, tcr, tch, tje, tun]

for gen in gens:
    # evaluate on test data
    print("Evaluate on test data")
    results = model.evaluate_generator(gen, verbose=1)
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
