"""
Adapted from lecture "Anwendungen der Bildverarbeitung" by Udo Frese, 2019
"""
import DataGenerator as dg
import HelperFunctions as helpers
import Globals
import keras
from keras import layers
import time
import json
import os
import pickle
import math
import numpy as np
from tensorflow import random
#from tensorflow import set_random_seed

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
random.set_seed(2)
#set_random_seed(2)

"""group: 
    0 - nothing, 
    1 - fish, 
    2 - crustacea, 
    3- chaetognatha, 
    4 - unidentified_object, 
    5 - jellyfish
bodyPart: 
    'front'
    'back'
    'both'
"""
# constants
BATCH_SIZE = 2
EPOCHS_1 = 10
EPOCHS_2 = 50
USE_CLASSWEIGHTS = False # set to True if class weights are desired

# output directory
out_path = "../data/output/75/"

# load annotation files
label_root = "../data/maritime_dataset_25/labels/"
test_labels, train_labels, train_labels_no_animals, val_labels, class_weights = helpers.loadAndSplitLabels(label_root)

# disable classweights if desired
# disable classweights if desired
if not USE_CLASSWEIGHTS: 
    class_weights = {0: 1, 1:1, 2:1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10:1}

print(f"class weights {class_weights}")

# sample image
data_root = "../data/maritime_dataset_25/"
imageShape = helpers.shapeOfFilename(os.path.join(data_root,"training_data_animals/0.jpg"), downsample_factor=1, image_factor=32)
print(f"Image format {imageShape}.")

# data generators
trainGenL = dg.DataGenerator (dataset=train_labels,
                              no_animal_dataset=train_labels_no_animals,
                              no_animal_ratio=0,
                              prepareEntry=dg.prepareEntryLowResHeatmap,
                              batch_size=BATCH_SIZE)

valGenL = dg.DataGenerator (dataset=val_labels, 
                            prepareEntry=dg.prepareEntryLowResHeatmap,
                            batch_size=BATCH_SIZE)

print("DataGenerators initialized")

# show entries of generators
dg.showEntryOfGenerator (trainGenL, 0, showHeatmaps=False)
dg.showEntryOfGenerator (valGenL, 0, False)


# # Now construct the low-res net and store it into the variable model
# # Loading of MobileNet.V2 will give a warning "`input_shape` is undefined or non-square, or `rows` is not in [96, 128, 160, 192, 224]. Weights for input shape (224, 224) will be loaded as the default."
# # That's correct.
# # Proceed as described in abv-uebung-6.pdf and discuss the architecture.
# # Inspect the architecture with model.summary() to make sure, that the number of trainable weights
# # is compatible to the amount of data we have.
# #
# # For reference you can access the MobileNet.V2 source code at
# # https://github.com/keras-team/keras-applications/blob/master/keras_applications/mobilenet_v2.py

def ourBlock (x, basename, channels=15):
#def ourBlock(x, basename, channels=Globals.channels):
    """Our own block of computation layers used several times in the network. It is similar to
    the block used in MobileNet.V2 but simplified. x is the layer to attach the block to,
    basename the name of this block, which will be extended by layer names. channel is the
    number of channels in the output (internally a multiple of that). The final layer is returned."""
    # First reduce to the defined no of channels to avoid having too many weights
    x = layers.Conv2D (channels, 1, padding='same', name = basename+"_bottleneck_conv")(x)
    x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name=basename+'_bottleneck_BN')(x)
    x = layers.ReLU(6., name=basename+'_bottleneck_relu')(x)

    x = layers.Conv2D (4*channels, 1, padding='same', name = basename+"_conv")(x)
    x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name=basename+'_BN')(x)
    x = layers.ReLU(6., name=basename+'_relu')(x)

    x = layers.DepthwiseConv2D(kernel_size=3, activation=None, use_bias=False, padding='same', name=basename+'-DW')(x)
    x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name=basename+'_DW_BN')(x)
    x = layers.ReLU(6., name=basename+'_DW_relu')(x)
    
    x = layers.Conv2D (channels, 1, padding='same', name = basename+"_project")(x)
    x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name=basename+'_project_BN')(x)
    
    return x

alpha = 1.0
input = keras.layers.Input(shape=imageShape)

backbone = keras.applications.mobilenet_v2.MobileNetV2(alpha=alpha, 
                                                       input_tensor=input, 
                                                       include_top=False, 
                                                       weights='imagenet', 
                                                       pooling=None)

# freeze backbone
for l in backbone.layers:
    l.trainable = False
    
# we attach to the layer with 320 channels because with a 1280 channel input 
# this conv would have too many weights
x = backbone.get_layer("block_16_project_BN").output

# computational block á la MobileNet.V2
x = ourBlock (x, "block_17")

# final heatmap output layer with softmax, because heatmap is within 0..1
out_h = layers.Conv2D(11, 1, padding='same', activation="softmax", name = "heatmap")(x)

# vector output layer
out_v = layers.Conv2D(4, 1, padding='same', activation="linear", name = "vectors")(x)

# define and compile model
modelL = keras.Model(inputs=input, outputs=[out_h, out_v])
modelL.compile(loss={"heatmap": "categorical_crossentropy", "vectors": "mse"}, 
               optimizer=keras.optimizers.Adam(), 
               metrics=["mae", "acc"])

modelL.summary()

# take time of training process
start  = time.time()

# for training mobilenet too 
history_1 = modelL.fit_generator(generator=trainGenL, 
                                 epochs=EPOCHS_1, 
                                 validation_data=valGenL, 
                                 class_weight=class_weights
                                 )

# activate all layers for training
for l in modelL.layers:
    l.trainable = True
    
# compile and fit model again
modelL.compile(loss={"heatmap": "categorical_crossentropy", "vectors": "mse"}, 
               optimizer=keras.optimizers.Adam(), 
               metrics=["mae", "acc"])

history_2 = modelL.fit_generator(generator=trainGenL, 
                                 epochs=EPOCHS_2, 
                                 validation_data=valGenL, 
                                 class_weight=class_weights
                                 )

# print the time used for training
print(f"Training took {time.time() - start}")


# save model, weights and history
modelL.save(f"{out_path}model-L")

modelL.save_weights(f"{out_path}weights-L.h5") # saves weights 

with open(f"{out_path}trainHistory-L1.pickle", 'wb') as file:
    pickle.dump(history_1.history, file)

with open(f"{out_path}trainHistory-L2.pickle", 'wb') as file:
    pickle.dump(history_2.history, file)