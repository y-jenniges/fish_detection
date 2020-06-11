import DataGenerator as dg
import HelperFunctions as helpers
import Globals
import keras
from keras import layers
import time
import json
import os
import pickle

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
#timestamp = time.strftime("%Y%m%d-%H%M%S")
out_path = f"../data/output/14/"

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


# image path
#data_root = "../data/maritime_dataset/"
data_root = "../data/maritime_dataset_25/"
imageShape = helpers.shapeOfFilename(os.path.join(data_root,"training_data_animals/0.jpg"))
print(f"Image format {imageShape}.")

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

print("DataGenerators initialized")


dg.showEntryOfGenerator (trainGenL, 0, showHeatmaps=False)
dg.showEntryOfGenerator (testGenL, 0, False)


# serialize data generators
serialized_trainGen = pickle.dumps(trainGenL)
serialized_testGen = pickle.dumps(testGenL)

filename_train = f'{out_path}serialized_trainGen-L.pickle'
filename_test = f'{out_path}serialized_testGen-L.pickle'

# save data generators
with open(filename_train,'wb') as file:
    file.write(serialized_trainGen)
with open(filename_test,'wb') as file:
    file.write(serialized_testGen)

print("DataGenerators serialized")




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
input= keras.layers.Input(shape=imageShape)

backbone = keras.applications.mobilenet_v2.MobileNetV2(alpha=alpha, input_tensor=input, include_top=False, weights='imagenet', pooling=None)
for l in backbone.layers:
    l.trainable = False
    
# We attach to the layer with 320 channels because with a 1280 channel input this conv would have too many weights
x = backbone.get_layer("block_16_project_BN").output

# Computational block á la MobileNet.V2
x = ourBlock (x, "block_17")
   
# Final output layer with sigmoid, because heatmap is within 0..1
x = layers.Conv2D (1, 1, padding='same', activation=Globals.activation_outLayer, name = "block_18_conv_output")(x)



# output layers

# output_h = layers.Conv2D (filters=Globals.channels,
#                           kernel_size=1,
#                           padding='same', 
#                           activation='softmax', 
#                           name = "heatmap")(x)

# output_c = layers.Conv2D(filters=Globals.channels, 
#                           kernel_size=[1,1],
#                           strides=1,
#                           padding='same',
#                           dilation_rate=1,
#                           activation='softmax',
#                           name='classification')(x)

# define an optimizer
#opt = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.001, amsgrad=False)
opt = keras.optimizers.Adam()

modelL = keras.Model(inputs=input, outputs=x)
modelL.compile(loss=Globals.loss, optimizer=opt, metrics=Globals.metrics)

# modelL = keras.Model(inputs=input_tensor, outputs=[output_h, output_c])
# modelL.compile(loss=Globals.loss, optimizer=Globals.optimizer, metrics=Globals.metrics)

modelL.summary()

# take time of training process
start  = time.time()

# train low-res-net
#model.load_weights ("strawberry-L.h5"), #load a previous checkpoint
#for ctr in range(10):
history = modelL.fit_generator(generator=trainGenL, epochs=Globals.epochs_L, validation_data=testGenL)

# print the time used for training
print(f"Training took {time.time() - start}")


# save model, weights and history
modelL.save(f"{out_path}model-L")
modelL.save_weights(f"{out_path}weights-L.h5") # saves weights (e.g. a checkpoint) locally
# save the history(todo: is it already contained in modelL.save? and also weights?)
# history.history is a dict
with open(f"{out_path}trainHistory-L.pickle", 'wb') as file:
    pickle.dump(history.history, file)
    #modelL.save_weights(f"fish-L-{ctr}.h5") # saves weights (e.g. a checkpoint) locally
  
    #files.download('fish-L.h5') # download weights from e.g. google-colab to local machine
    
