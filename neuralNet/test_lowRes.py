import json
import pickle
import os
from datetime import datetime
import keras
import HelperFunctions as helpers
import numpy as np

#test_path = "../data/tests/1/"
test_path=""

# load annotation files
path = "../data/labels/training_labels_animals.json"
label_root = ""

with open(os.path.join(label_root, path) , 'r') as f:
    train_labels_animals = json.load(f)
    
path = "../data/labels/test_labels.json"
with open(os.path.join(label_root, path), 'r') as f:
    test_labels = json.load(f)
    
path = "../data/labels/training_labels_no_animals.json"
with open(os.path.join(label_root, path), 'r') as f:
    train_labels_no_animals = json.load(f)


# load testGenL
with open(os.path.join(test_path,"serialized_testGen.pickle"),'rb') as file:
    raw_data = file.read()
testGen = pickle.loads(raw_data)


# load model
# todo look for file name (depends on timestamp)
modelL = keras.models.load_model(os.path.join(test_path,"model-L-20200531-015257"))

# load training history
with open(os.path.join(test_path,"trainHistory-20200531-015257"),'rb') as file:
    raw_data = file.read()
history = pickle.loads(raw_data)


# Use this to visualize results
# It shows the input image (background), the predicted heatmap (white "fog" in foreground)
# and the ground-truth (blue crosses)
# testIdx = random.randint(0,len(testGenL))
# testBatch = testGenL[testIdx]
# gtBatch = testGenL.get_ground_truth(testIdx)
# yHats = modelL.predict (testBatch[0])
# for i in range(0,len(yHats)):
#     helpers.showImageWithHeatmap (testBatch[0][i], yHats[i], gtBatch[i], filename=f"result-L-{i}.png") 


print(f"history keys {history.keys()}")

output_json = []
gt = []
yHats = []
#for i in range(len(testGen)):
for i in range(3):
    temp = {}
    testBatch = testGen[i]
    
    print(testBatch[0].shape)
    print(testBatch[1].shape)
    
    temp['batch'] = i
    temp['images'] = testBatch[0].tolist()
    temp['gt'] = testBatch[1].tolist()
    temp['prediction'] = modelL.predict(testBatch[0]).tolist()

    print(f"prediction shape {np.array(temp['prediction']).shape}")

   # helpers.showImageWithHeatmap(image, hm=None, gt=None, group=1, bodyPart="front", filename=None)
    
    output_json.append(temp)
    
# save output
with open(f"predictions-{str(datetime.now())}.json", 'w') as outfile:
    json.dump(output_json, outfile)
