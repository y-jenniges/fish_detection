import json
import os
import numpy as np
import tensorflow as tf

import HelperFunctions as helpers
import HeatmapClass
import DataGenerator as dg


test_path = "../data/output/100/"
model_path = "model-L"

# load annotation files
label_root = "../data/maritime_dataset_25/labels/"

path = "test_labels.json"
with open(os.path.join(label_root, path), 'r') as f:
    test_labels = json.load(f)
    
# load model
model = tf.keras.models.load_model(os.path.join(test_path,model_path))


# testGen = dg.DataGenerator (dataset=test_labels, 
#                               #hm_folder_path="../data/heatmaps_lowRes/test/" ,
#                               prepareEntry=dg.prepareEntryLowResHeatmap,
#                               batch_size=4)

# # evaluate on test data
# print("Evaluate on test data")
# results = model.evaluate_generator(testGen)
# print("test loss, test acc:", results)

# minimalistic CNN
def generateY(entry):
    # load image and make its range [-1,1] (suitable for mobilenet)
    image = helpers.loadImage(entry['filename'], 32)
    image = 2.*image/np.max(image) - 1

    heatmaps=[]

    # fish head only
    hm = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart="front")
    hm.downsample(32)
    
    heatmaps = hm.hm
    return np.asarray(image), np.asarray(heatmaps)

x_test = []
y_test = []

print("generating heatmaps...")
heatmaps=[]
for entry in test_labels:
    img, hms = generateY(entry)
    x_test.append(img)
    heatmaps.append(hms)
print("assingning x and y...")
y_test = np.asarray(heatmaps)
x_test = np.asarray(x_test)

print("Evaluate on test data")
results = model.evaluate(x_test, y_test, batch_size=4, verbose=1)
print("test loss, test mae:", results)
