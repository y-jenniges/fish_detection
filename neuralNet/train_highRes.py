import DataGenerator as dg
import HelperFunctions as helpers
import Globals
import keras
from keras import layers
import time
import json
import os
import pickle
from tensorflow import random

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
random.set_seed(2)
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
# output directory
out_path = f"../data/output/41/"

# load annotation files
#label_root = "../data/maritime_dataset/labels/"
label_root = "../data/maritime_dataset_25/labels/"
 
label_path = "training_labels_animals.json"
with open(os.path.join(label_root, label_path) , 'r') as f:
    train_labels_animals = json.load(f)
    
label_path = "test_labels.json"
with open(os.path.join(label_root, label_path), 'r') as f:
    test_labels = json.load(f)
    
label_path = "training_labels_no_animals.json"
with open(os.path.join(label_root, label_path), 'r') as f:
    train_labels_no_animals = json.load(f)

# only use images that contain fish
fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
train_labels_animals = helpers.filter_labels_for_animal_group(train_labels_animals, fish_id)
test_labels = helpers.filter_labels_for_animal_group(test_labels, fish_id)

# train_labels_animals = train_labels_animals[:4]
# test_labels = test_labels[:4]


# image path
#data_root = "../data/maritime_dataset/"
data_root = "../data/maritime_dataset_25/"
imageShape = helpers.shapeOfFilename(os.path.join(data_root,"training_data_animals/0.jpg"))
print(f"Image format {imageShape}.")

# data generators
trainGenL = dg.DataGenerator (dataset=train_labels_animals,
                              #hm_folder_path="../data/heatmaps_lowRes/training_animals/",
                              no_animal_dataset=train_labels_no_animals,
                              no_animal_ratio=Globals.no_animal_ratio,
                              prepareEntry=dg.prepareEntryLowResHeatmap,
                              batch_size=Globals.batch_size)

testGenL = dg.DataGenerator (dataset=test_labels, 
                              #hm_folder_path="../data/heatmaps_lowRes/test/" ,
                              prepareEntry=dg.prepareEntryLowResHeatmap,
                              batch_size=Globals.batch_size)


trainGenH = dg.DataGenerator (dataset=train_labels_animals,
                              #hm_folder_path="../data/heatmaps_lowRes/training_animals/",
                              no_animal_dataset=train_labels_no_animals,
                              no_animal_ratio=Globals.no_animal_ratio,
                              prepareEntry=dg.prepareEntryHighResHeatmap,
                              batch_size=Globals.batch_size)

testGenH = dg.DataGenerator (dataset=test_labels, 
                              #hm_folder_path="../data/heatmaps_lowRes/test/" ,
                              prepareEntry=dg.prepareEntryHighResHeatmap,
                              batch_size=Globals.batch_size)

print("DataGenerators initialized")

dg.showEntryOfGenerator (trainGenL, 0, showHeatmaps=False)
dg.showEntryOfGenerator (testGenL, 0, False)

dg.showEntryOfGenerator (trainGenH, 0, showHeatmaps=False)
dg.showEntryOfGenerator (testGenH, 0, False)


# serialize data generators
#serialized_trainGenH = pickle.dumps(trainGenH)
serialized_testGenH = pickle.dumps(testGenH)
serialized_testGenL = pickle.dumps(testGenL)

#filename_train = f'{out_path}serialized_trainGen-H.pickle'
filename_testH = f'{out_path}serialized_testGen-H.pickle'
filename_testL = f'{out_path}serialized_testGen-L.pickle'

# save data generators
# with open(filename_train,'wb') as file:
#     file.write(serialized_trainGenH)
with open(filename_testH,'wb') as file:
    file.write(serialized_testGenH)
with open(filename_testL,'wb') as file:
    file.write(serialized_testGenL)

print("DataGenerators serialized")

# todo: why does this not work??
# load model for low resolution
#modelL = keras.models.load_model(f"{out_path}model-L")

# Now construct the low-res net and store it into the variable model
# Loading of MobileNet.V2 will give a warning "`input_shape` is undefined or non-square, or `rows` is not in [96, 128, 160, 192, 224]. Weights for input shape (224, 224) will be loaded as the default."
# That's correct.
# Proceed as described in abv-uebung-6.pdf and discuss the architecture.
# Inspect the architecture with model.summary() to make sure, that the number of trainable weights
# is compatible to the amount of data we have.
#
# For reference you can access the MobileNet.V2 source code at
# https://github.com/keras-team/keras-applications/blob/master/keras_applications/mobilenet_v2.py

def ourBlock (x, basename, channels=8):
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
#for l in backbone.layers[:-25]:
for l in backbone.layers:
    l.trainable = False
    
# We attach to the layer with 320 channels because with a 1280 channel input this conv would have too many weights
x = backbone.get_layer("block_16_project_BN").output

# Computational block á la MobileNet.V2
x = ourBlock (x, "block_17")
   
# Final output layer with sigmoid, because heatmap is within 0..1
#x = layers.Conv2D (1, 1, padding='same', activation=Globals.activation_outLayer, name = "block_18_conv_output")(x)
x = layers.Conv2D (1, 1, padding='same', activation=Globals.activation_outLayer, name = "heatmap")(x)


# compile model
opt = keras.optimizers.Adam()
modelL = keras.Model(inputs=input, outputs=x)
modelL.compile(loss=Globals.loss, optimizer=opt, metrics=Globals.metrics)
modelL.summary()


# start timer for training
start_L  = time.time()

# for training mobilenet too 
history_L1 = modelL.fit_generator(generator=trainGenL, epochs=10, validation_data=testGenL)

# activate all layers for training
for l in modelL.layers:
    l.trainable = True
    
# compile and fit model again
modelL.compile(loss=Globals.loss, optimizer=opt, metrics=Globals.metrics)
history_L2 = modelL.fit_generator(generator=trainGenL, epochs=Globals.epochs_L, validation_data=testGenL)


end_L = time.time() - start_L


# # upsampling -----------------------------------------------------------------------------------------

# x = modelL.get_layer("block_17_project_BN").output # low-res model before last conv-sigmoid layer
# x = layers.UpSampling2D(interpolation='bilinear', name='block_19_upto16')(x)

# # Concatenate with the layer before the expansion that is followed by conv and downsample
# x = layers.Concatenate(name="block_19_concat")([x,modelL.get_layer("block_12_add").output])
# x = ourBlock (x, 'block_19')

# x = layers.UpSampling2D(interpolation='bilinear', name='block_20_upto8')(x)
# x = layers.Concatenate(name="block_20_concat")([x,modelL.get_layer("block_5_add").output])
# x = ourBlock (x, 'block_20')

# x = layers.UpSampling2D(interpolation='bilinear', name='block_21_upto4')(x)
# x = layers.Concatenate(name="block_21_concat")([x,modelL.get_layer("block_2_add").output])
# x = ourBlock (x, 'block_21')

# x = layers.UpSampling2D(interpolation='bilinear', name='block_22_upto2')(x)
# x = layers.Concatenate(name="block_22_concat")([x,modelL.get_layer("expanded_conv_project_BN").output])
# x = ourBlock (x, 'block_22')

# x = layers.UpSampling2D(interpolation='bilinear', name='block_23_upto1')(x)
# #x = layers.Concatenate(name="block_23_concat")([x, input])
# #x = layers.Conv2D (8, 3, padding='same', name = "block_23_conv")(x)
# #x = layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999, name='block_23_BN')(x)
# #x = layers.ReLU(6., name='block_23_relu')(x)
# x = ourBlock (x, 'block_23', channels=4)

# #x = layers.Conv2D (1, 1, padding='same', activation=Globals.activation_outLayer, name = "block_23_conv_output")(x)
# x = layers.Conv2D (1, 1, padding='same', activation=Globals.activation_outLayer, name = "heatmap")(x)


# modelH = keras.Model(inputs=input, outputs=x)
# modelH.compile(loss=Globals.loss, optimizer=Globals.optimizer, metrics=Globals.metrics)
# modelH.summary()



# # # take time of training process
# # start  = time.time()

# # # train low-res-net
# # #model.load_weights ("strawberry-L.h5"), #load a previous checkpoint
# # #for ctr in range(10):
# start_H = time.time()
# historyH = modelH.fit_generator(generator=trainGenH, epochs=Globals.epochs_H, validation_data=testGenH)
# end_H = time.time() - start_H
# # # print the time used for training
# # print(f"Training took {time.time() - start}")

# print(f"model-L training took {end_L}\nmodel-H training took {end_H}")

# # save model, weights and history
# modelH.save(f"{out_path}model-H")
# #modelH.save_weights(f"{out_path}weights-H.h5") # saves weights (e.g. a checkpoint) locally

modelL.save(f"{out_path}model-L")
#modelL.save_weights(f"{out_path}weights-L.h5") # saves weights (e.g. a checkpoint) locally


# # save the history(todo: is it already contained in modelL.save? and also weights?)
# # history.history is a dict
# with open(f"{out_path}trainHistory-H.pickle", 'wb') as file:
#     pickle.dump(historyH.history, file)
#     #modelL.save_weights(f"fish-L-{ctr}.h5") # saves weights (e.g. a checkpoint) locally
    
with open(f"{out_path}trainHistory-L1.pickle", 'wb') as file:
    pickle.dump(history_L1.history, file)
with open(f"{out_path}trainHistory-L2.pickle", 'wb') as file:
    pickle.dump(history_L2.history, file)