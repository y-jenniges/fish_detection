# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:06:25 2020

@author: yjenn
"""

import json
import os
import pickle
import HelperFunctions as helpers
import math
import matplotlib.pyplot as plt
import HeatmapClass
import Globals
import numpy as np
import keras
from keras.models import Sequential
#from keras.layers import Dense, Dropout
from keras import layers
from tensorflow import random

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
random.set_seed(2)


# output directory
out_path = "../data/output/47/"

label_root = "../data/maritime_dataset_25/labels/"

label_path = "training_labels_animals.json"
with open(os.path.join(label_root, label_path) , 'r') as f:
    labels = json.load(f)
  
labels = labels[:2]
 


num_classes = 2   
fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
crust_id = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#jellyfish_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    

test_ratio = 0.05


# splitting data into test and train for every organism
# FISH
fish = helpers.filter_labels_for_animal_group(labels, fish_id)
fish_test_length = math.ceil(test_ratio*len(fish))
test_fish = fish[:fish_test_length]
train_fish = fish[fish_test_length:]

# CRUSTACEA
crust = helpers.filter_labels_for_animal_group(labels, crust_id)
crust_test_length = math.ceil(test_ratio*len(crust))
test_crust = crust[:crust_test_length]
train_crust = crust[crust_test_length:]

# JELLYFISH
# jellyfish = helpers.filter_labels_for_animal_group(labels, jellyfish_id)
# jellyfish_test_length = math.ceil(test_ratio*len(jellyfish))
# test_jellyfish = jellyfish[:jellyfish_test_length]
# train_jellyfish = jellyfish[jellyfish_test_length:]

# sample image
image_example = helpers.loadImage(fish[0]['filename'])
plt.imshow(image_example)
plt.show()

# create final test and train data
test_labels = test_fish #+ test_crust
train_labels = train_fish #+ train_crust

def generateY(entry):

    # hm = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='front')
    # #hm.showImageWithHeatmap()
    # hm = hm.hm
    
    # load image and make its range [-1,1] (suitable for mobilenet)
    image = helpers.loadImage(entry['filename'])
    image = 2.*image/np.max(image) - 1

    heatmaps=[]
    classifications=[]
    
      
    # idea here: fish head only
    hm = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart="front")
    hm.downsample()
    
    heatmaps = hm.hm
    
        
    return np.asarray(image), np.asarray(heatmaps), np.asarray(classifications)


x_train = []
x_test = []

heatmaps=[]
classifications = []
for entry in train_labels:
    img, hms, cs = generateY(entry)
    x_train.append(img)
    heatmaps.append(hms)
    classifications.append(cs)


y_train = np.asarray(heatmaps)
#y_train = {"heatmap": heatmaps, "classification":classifications}

heatmaps=[]
classifications = []
for entry in test_labels:
    img, hms, cs = generateY(entry)
    x_test.append(img)
    heatmaps.append(hms)
    classifications.append(cs)

y_test = np.asarray(heatmaps)
#y_test = {"heatmap": heatmaps, "classification":classifications}

x_train = np.asarray(x_train)
x_test = np.asarray(x_test)








# overfitting one batch
helpers.showImageWithHeatmap(x_train[0], y_train[0])

model = Sequential()
model.add(layers.Conv2D(filters=3, kernel_size=3, activation=None, use_bias=False, padding='same', input_shape=image_example.shape))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))
model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))
model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU(6.))

model.add(layers.Conv2D (1, 1, padding='same', activation="sigmoid", name = "heatmap"))


model.compile(loss='binary_crossentropy', 
              optimizer=keras.optimizers.adam(lr=0.001), 
              metrics = ['mae'])

model.summary()

history = model.fit(x_train, y_train, 
                    epochs=1, 
                    batch_size=4, 
                    verbose=1, 
                    validation_data=(x_test, y_test))



model.save(f"{out_path}model-L")
with open(f"{out_path}trainHistory-L1.pickle", 'wb') as file:
    pickle.dump(history.history, file) 