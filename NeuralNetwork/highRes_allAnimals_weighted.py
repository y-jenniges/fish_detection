"""
Adapted from lecture "Anwendungen der Bildverarbeitung" by Udo Frese, 
University Bremen, 2019
"""
import time
import os
import pickle
import numpy as np
import keras
from keras import layers
#from tensorflow import random
from tensorflow import set_random_seed
import Losses
import DataGenerator as dg
import HelperFunctions as helpers

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
#random.set_seed(2)
set_random_seed(2)

# constants
BATCH_SIZE = 2
EPOCHS_1 = 10
EPOCHS_2 = 100 # 50
EPOCHS_3 = 20

# output directory
out_path = "../data/output/1/"

# load annotation files
label_root = "../data/maritime_dataset_25/labels/"
test_labels, train_labels, train_labels_no_animals, val_labels, class_weights = helpers.loadAndSplitLabels(label_root)
weights = np.array(list(class_weights.values()))

print(f"class weights {weights}")

# sample image
data_root = "../data/maritime_dataset_25/"
imageShape = helpers.shapeOfFilename(os.path.join(data_root,"training_data_animals/0.jpg"), downsample_factor=1, image_factor=32)
print(f"Image format {imageShape}.")

# data generators
trainGenL = dg.DataGenerator (dataset=train_labels,
                              no_animal_dataset=train_labels_no_animals,
                              no_animal_ratio=0,
                              prepareEntry=dg.prepareEntryLowResHeatmap,
                              batch_size=BATCH_SIZE, 
                              )

valGenL = dg.DataGenerator (dataset=val_labels, 
                            prepareEntry=dg.prepareEntryLowResHeatmap,
                            batch_size=BATCH_SIZE, 
                            )

trainGenH = dg.DataGenerator (dataset=train_labels,
                              no_animal_dataset=train_labels_no_animals,
                              no_animal_ratio=0,
                              prepareEntry=dg.prepareEntryHighResHeatmap,
                              batch_size=BATCH_SIZE)

testGenH = dg.DataGenerator (dataset=test_labels, 
                             prepareEntry=dg.prepareEntryHighResHeatmap,
                             batch_size=BATCH_SIZE)

print("DataGenerators initialized")

# show entries of generators
dg.showEntryOfGenerator (trainGenL, 0, showHeatmaps=False)
dg.showEntryOfGenerator (valGenL, 0, False)

dg.showEntryOfGenerator (trainGenH, 0, showHeatmaps=False)
dg.showEntryOfGenerator (testGenH, 0, False)

# # Now construct the low-res net and store it into the variable model
# # Loading of MobileNet.V2 will give a warning "`input_shape` is undefined or non-square, or `rows` is not in [96, 128, 160, 192, 224]. Weights for input shape (224, 224) will be loaded as the default."
# # That's correct.
# # Proceed as described in abv-uebung-6.pdf and discuss the architecture.
# # Inspect the architecture with model.summary() to make sure, that the number of trainable weights
# # is compatible to the amount of data we have.
# #
# # For reference you can access the MobileNet.V2 source code at
# # https://github.com/keras-team/keras-applications/blob/master/keras_applications/mobilenet_v2.py

def ourBlock (x, basename, channels=11):
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

backbone = keras.applications.mobilenet_v2.MobileNetV2(alpha=alpha, input_tensor=input, include_top=False, weights='imagenet', pooling=None)

# freeze backbone
for l in backbone.layers:
    l.trainable = False
    
# we attach to the layer with 320 channels because with a 1280 channel input 
# this conv would have too many weights
x = backbone.get_layer("block_16_project_BN").output

# computational block á la MobileNet.V2
x = ourBlock (x, "block_17")

# final output layer with softmax, because heatmap is within 0..1
x = layers.Conv2D (11, 1, padding='same', activation="softmax", name = "heatmap")(x)

# define and compile model
modelL = keras.Model(inputs=input, outputs=x)
modelL.compile(loss=Losses.weighted_categorical_crossentropy(weights), 
               optimizer=keras.optimizers.Adam(), 
               metrics=["mae", "acc"], 
               )

modelL.summary()

# take time of training process
start_L  = time.time()

# for training mobilenet too 
history_1 = modelL.fit_generator(generator=trainGenL, 
                                 epochs=EPOCHS_1, 
                                 validation_data=valGenL, 
                                 )

# activate all layers for training
for l in modelL.layers:
    l.trainable = True
    
# compile and fit model again
modelL.compile(loss=Losses.weighted_categorical_crossentropy(weights), 
               optimizer=keras.optimizers.Adam(), 
               metrics=["mae", "acc"], 
               )

history_2 = modelL.fit_generator(generator=trainGenL, 
                                 epochs=EPOCHS_2, 
                                 validation_data=valGenL, 
                                 )

end_L = time.time() - start_L

# upsampling -----------------------------------------------------------------------------------------

x = modelL.get_layer("block_17_project_BN").output # low-res model before last conv-sigmoid layer
x = layers.UpSampling2D(interpolation='bilinear', name='block_19_upto16')(x)

# Concatenate with the layer before the expansion that is followed by conv and downsample
x = layers.Concatenate(name="block_19_concat")([x,modelL.get_layer("block_12_add").output])
x = ourBlock (x, 'block_19')

x = layers.UpSampling2D(interpolation='bilinear', name='block_20_upto8')(x)
x = layers.Concatenate(name="block_20_concat")([x,modelL.get_layer("block_5_add").output])
x = ourBlock (x, 'block_20')

x = layers.UpSampling2D(interpolation='bilinear', name='block_21_upto4')(x)
x = layers.Concatenate(name="block_21_concat")([x,modelL.get_layer("block_2_add").output])
x = ourBlock (x, 'block_21')

x = layers.UpSampling2D(interpolation='bilinear', name='block_22_upto2')(x)
x = layers.Concatenate(name="block_22_concat")([x,modelL.get_layer("expanded_conv_project_BN").output])
x = ourBlock (x, 'block_22')

#x = layers.UpSampling2D(interpolation='bilinear', name='block_23_upto1')(x)
# # x = layers.Concatenate(name="block_23_concat")([x, input])
# # x = layers.Conv2D (8, 3, padding='same', name = "block_23_conv")(x)
# # x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name='block_23_BN')(x)
# # x = layers.ReLU(6., name='block_23_relu')(x)
# # x = ourBlock (x, 'block_23', channels=4) # @todo why 4 channels here only?
#x = ourBlock (x, 'block_23', channels=12)


x = layers.Conv2D (11, 1, padding='same', activation="softmax", name = "heatmap")(x)

modelH = keras.Model(inputs=input, outputs=x)
modelH.compile(loss=Losses.weighted_categorical_crossentropy(weights), 
               optimizer=keras.optimizers.Adam(), 
               metrics = ["mae", "acc"])

modelH.summary()

start_H = time.time()
history_H = modelH.fit_generator(generator=trainGenH, 
                                epochs=EPOCHS_3, 
                                validation_data=testGenH)
end_H = time.time() - start_H

# print the time used for training
print(f"model-L training took {end_L}\nmodel-H training took {end_H}")

# save models, weights and histories
modelL.save(f"{out_path}model-L")
modelH.save(f"{out_path}model-H")

modelL.save_weights(f"{out_path}weights-L.h5")
modelH.save_weights(f"{out_path}weights-H.h5")

with open(f"{out_path}trainHistory-L1.pickle", 'wb') as file:
    pickle.dump(history_1.history, file)
    
with open(f"{out_path}trainHistory-L2.pickle", 'wb') as file:
    pickle.dump(history_2.history, file)  

with open(f"{out_path}trainHistory-H.pickle", 'wb') as file:
    pickle.dump(history_H.history, file)  