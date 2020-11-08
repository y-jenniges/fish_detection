import json
import os
import pickle
import numpy as np
import keras
from keras.models import Sequential
from keras import layers
#from tensorflow import random # for higher TF versions
from tensorflow import set_random_seed
import HelperFunctions as helpers
import matplotlib.pyplot as plt
import HeatmapClass


# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
#random.set_seed(2)
set_random_seed(2)

# output directory
out_path = "../data/output/1/"

# label directory
label_root = "../data/maritime_dataset_25/labels/"

# load label files
label_path = "training_labels_animals.json"
with open(os.path.join(label_root, label_path) , 'r') as f:
    train_labels = json.load(f)

label_path = "validation_labels.json"
with open(os.path.join(label_root, label_path) , 'r') as f:
    val_labels = json.load(f)

# filter training and validation data for images with fish heads
fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

train_labels = helpers.filter_labels_for_animal_group(train_labels, fish_id)
val_labels = helpers.filter_labels_for_animal_group(val_labels, fish_id)

# sample image
image_example = helpers.loadImage(train_labels[0]['filename'], 32)
plt.imshow(image_example)
plt.show()
print(f"Image shape {image_example.shape}")

# function to generate y
def generateY(entry):
    # load image and make its range [-1,1]
    image = helpers.loadImage(entry['filename'], 32)
    image = 2.*image/np.max(image) - 1

    # create heatmap of fish heads
    hm = HeatmapClass.Heatmap(entry, group=1, bodyPart="front")
    hm.downsample(32)
        
    return np.asarray(image), np.asarray(hm.hm)

# generate x and y train
x_train = []
heatmaps=[]
for entry in train_labels:
    img, hms = generateY(entry)
    x_train.append(img)
    heatmaps.append(hms) 
y_train = np.asarray(heatmaps)

# generate x and y validation
x_val = []
heatmaps=[]
for entry in val_labels:
    img, hms = generateY(entry)
    x_val.append(img)
    heatmaps.append(hms)
y_val = np.asarray(heatmaps)

# make sure that x is a numpy array
x_train = np.asarray(x_train)
x_val = np.asarray(x_val)

# show first data point
helpers.showImageWithHeatmap(x_train[0], y_train[0])

# define model
model = Sequential()
model.add(layers.Conv2D(filters=3, kernel_size=3, activation=None, 
                        use_bias=False, padding='same', 
                        input_shape=image_example.shape))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())
model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())

model.add(layers.MaxPooling2D())

model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())
model.add(layers.Conv2D (filters=8, kernel_size=3, strides=1, padding='same'))
model.add(layers.BatchNormalization(axis=-1, epsilon=1e-3, momentum=0.999))
model.add(layers.ReLU())

model.add(layers.Conv2D (1, 1, padding='same', activation="sigmoid", 
                         name = "heatmap"))

model.compile(loss='binary_crossentropy', 
              optimizer=keras.optimizers.adam(lr=0.001), 
              metrics = ['mae'])

model.summary()

# train model
history = model.fit(x_train, y_train, 
                    epochs=50, 
                    batch_size=4, 
                    verbose=1, 
                    validation_data=(x_val, y_val))

# save model and history
model.save(f"{out_path}model-L")
with open(f"{out_path}trainHistory-L1.pickle", 'wb') as file:
    pickle.dump(history.history, file) 