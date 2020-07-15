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



# output directory
out_path = "../data/output/30/"

label_root = "../data/maritime_dataset_25/labels/"

label_path = "training_labels_animals.json"
with open(os.path.join(label_root, label_path) , 'r') as f:
    labels = json.load(f)
  
labels = labels[:5]
    
fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
jellyfish_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    

test_ratio = 0.05

# splitting data into test and train for every organism
# FISH
fish = helpers.filter_labels_for_animal_group(labels, fish_id)
fish_test_length = math.ceil(test_ratio*len(fish))
test_fish = fish[:fish_test_length]
train_fish = fish[fish_test_length:]

# JELLYFISH
jellyfish = helpers.filter_labels_for_animal_group(labels, jellyfish_id)
jellyfish_test_length = math.ceil(test_ratio*len(jellyfish))
test_jellyfish = jellyfish[:jellyfish_test_length]
train_jellyfish = jellyfish[jellyfish_test_length:]

# sample image
img = helpers.loadImage(fish[0]['filename'])
plt.imshow(img)
plt.show()

# create final test and train data
test_labels = test_fish + test_jellyfish
train_labels = train_fish + train_jellyfish

def generateY(entry):

    hm = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='front')
    #hm.showImageWithHeatmap()
    hm = hm.hm
    
    # load image and make its range [-1,1] (suitable for mobilenet)
    image = helpers.loadImage(entry['filename'])
    image = 2.*image/np.max(image) - 1

    heatmaps=[]
    classifications=[]
    
    
    # idea here: generate all heatmaps
    for i in list(range(Globals.NUM_GROUPS)):
        
        if i == 0:
            hm = HeatmapClass.Heatmap(entry, resolution='low', group=i, bodyPart="front")
            hm.downsample()
            
            c = np.zeros(Globals.NUM_GROUPS*2-1)
            c[0] = 1
            
            heatmaps.append(hm)
            classifications.append(c)
        else:
            # generate head heatmap
            hm_f = HeatmapClass.Heatmap(entry, resolution='low', group=i, bodyPart="front")
            hm_f.downsample()
            
            # generate tail heatmap
            hm_b = HeatmapClass.Heatmap(entry, resolution='low', group=i, bodyPart="back")
            hm_b.downsample()
            
            # append heatmaps
            heatmaps.append(hm_f)
            heatmaps.append(hm_b)
            
            # create classifications
            c_f = np.zeros(Globals.NUM_GROUPS*2-1)
            c_b = np.zeros(Globals.NUM_GROUPS*2-1)
            c_f[i*2-1] = 1
            c_b[i*2] = 1
            
            # append classifications
            classifications.append(c_f)
            classifications.append(c_b)
        
    # # idea here: return only necessary heatmaps and classes
    # coveredGroups = []    
    # for animal in entry['animals']:
    #     group = math.ceil(animal['group'].index(1)/2)
    #     #group = str(math.floor(animal['group'].index(1)/2))
    #     bodyPart = 'front' if animal['group'].index(1)%2==0 else 'back'
        
    #     if (group, bodyPart) not in coveredGroups:
    #         # calculate heatmap      
    #         hm = HeatmapClass.Heatmap(entry, resolution='low', group=group, bodyPart=bodyPart)
    #         hm.downsample()
    #         #hm = helpers.downsample(hm.hm)
    
    #         # append heatmap
    #         hm.showImageWithHeatmap()
    #         heatmaps.append(hm)
        
    #         # append classification
    #         # heatmaps.append(np.array(hm_json["hm_" + group + bodyPart]))
    #         classifications.append(np.array(animal['group']))
            
    #         # add to this group to the covered ones
    #         coveredGroups.append((group, bodyPart))
        
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


y_train = heatmaps
#y_train = {"heatmap": heatmaps, "classification":classifications}

heatmaps=[]
classifications = []
for entry in test_labels:
    img, hms, cs = generateY(entry)
    x_test.append(img)
    heatmaps.append(hms)
    classifications.append(cs)

y_test = heatmaps
#y_test = {"heatmap": heatmaps, "classification":classifications}





num_classes = 11
input= keras.layers.Input(shape=img.shape)

# https://medium.com/@vijayabhaskar96/multi-label-image-classification-tutorial-with-keras-imagedatagenerator-cd541f8eaf24
model = Sequential()
model.add(layers.Conv2D(32, (3, 3), padding='same', input_shape=img.shape))
model.add(layers.Activation('relu'))
model.add(layers.Conv2D(32, (3, 3)))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Dropout(0.25))

model.add(layers.Conv2D(64, (3, 3), padding='same'))
model.add(layers.Activation('relu'))
model.add(layers.Conv2D(64, (3, 3)))
model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Dropout(0.25))

model.add(layers.Flatten())
model.add(layers.Dense(512))
model.add(layers.Activation('relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(num_classes, activation='sigmoid'))
model.compile(keras.optimizers.rmsprop(lr=0.0001, decay=1e-6),
              loss="binary_crossentropy",
              metrics=["accuracy"])


#inputA = layers.Input(shape=img.shape)
#inputB = layers.Input(shape=(num_classes,))

# x = layers.Conv2D (num_classes, 1, padding='same', name = "aha_bottleneck_conv", input_shape=img.shape)(input)
# x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name='aha_bottleneck_BN')(x)
# x = layers.ReLU(6., name='aha_bottleneck_relu')(x)

# x = layers.Conv2D (4*num_classes, 1, padding='same', name = "conv")(x)
# x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name='BN')(x)
# x = layers.ReLU(6., name= 'relu')(x)

# x = layers.DepthwiseConv2D(kernel_size=3, activation=None, use_bias=False, padding='same', name='aha-DW')(x)
# x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name='aha_DW_BN')(x)
# x = layers.ReLU(6., name='aha_DW_relu')(x)

# x = layers.Conv2D (num_classes, 1, padding='same', name = "aha_project")(x)
# x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name='aha_project_BN')(x)


# x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')#, input_shape=img.shape)
# x = layers.MaxPooling2D((2, 2))
# x = layers.Conv2D(64, (3, 3), activation='relu')
# x = layers.MaxPooling2D((2, 2))
# x = layers.Conv2D(64, (3, 3), activation='relu')



# x = layers.Conv2D (channels, 1, padding='same', name = basename+"_bottleneck_conv")(x)
# x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name=basename+'_bottleneck_BN')(x)
# x = layers.ReLU(6., name=basename+'_bottleneck_relu')(x)

# output_h = layers.Conv2D (filters=1,
#                           kernel_size=1,
#                           padding='same', 
#                           activation='sigmoid', 
#                           name = "heatmap")(x)

# output_c = layers.Conv2D(filters=num_classes, 
#                           kernel_size=[1,1],
#                           strides=1,
#                           padding='same',
#                           dilation_rate=1,
#                           activation='softmax',
#                           name='classification')(x)


# model = keras.Model(inputs=input, outputs=[output_h, output_c])

# model.compile(loss={'heatmap': 'mse', 'classification': 'categorical_crossentropy'}, 
#               optimizer=keras.optimizers.adam(lr=0.001), 
#               metrics = {'heatmap':['mae'], 'classification':['acc']})
history = model.fit(x_train, y_train, 
                    epochs=1, 
                    batch_size=1, 
                    verbose=1, 
                    validation_data=(x_test, y_test))
#                    validation_split=0.2)

# # Test the model after training
# test_results = model.evaluate(X_testing, Targets_testing, verbose=1)
# print(f'Test results - Loss: {test_results[0]} - Accuracy: {test_results[1]*100}%')


model.save(f"{out_path}model-L")
with open(f"{out_path}trainHistory-L.pickle", 'wb') as file:
    pickle.dump(history.history, file) 