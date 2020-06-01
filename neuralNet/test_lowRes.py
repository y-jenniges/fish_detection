import json
import pickle
import os
from datetime import datetime
import keras
import HelperFunctions as helpers
import numpy as np
import matplotlib.pyplot as plt
import time
import HeatmapClass

#timestamp = time.strftime("%Y%m%d-%H%M%S")  

out_path = "../data/output/"

test_path = "../data/tests/2/"
#test_path=""
out_path = test_path + "output/"
model_path = "model-L-20200601-035023"
hist_path = "trainHistory-20200601-035023.pickle"
testGen_path = "serialized_testGen.pickle"


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
with open(os.path.join(test_path, testGen_path),'rb') as file:
    raw_data = file.read()
testGen = pickle.loads(raw_data)


# load model
# todo look for file name (depends on timestamp)
modelL = keras.models.load_model(os.path.join(test_path,model_path))

# load training history
with open(os.path.join(test_path, hist_path),'rb') as file:
    raw_data = file.read()
history = pickle.loads(raw_data)

print("Loading done")

# predicting one specific image

entry = test_labels[60]
#helpers.showImageWithAnnotation(entry)
image = np.asarray(helpers.loadImage(entry['filename']))
hm = HeatmapClass.Heatmap(entry)

X = np.expand_dims(image, axis=0)
y = np.asarray(hm.hm)
yHat = modelL.predict(X)
print(f"yhat shape {yHat.shape})")
helpers.showImageWithHeatmap(image, yHat[0, :, :, :], filename="a.jpg")

with open("60.json", "w") as f:
    json.dump(yHat.tolist(), f)


# show heatmap only
# with open("../data/tests/2/39.json","r") as f:
#     data=json.load(f)
# plt.savefig("39_hm.jpg")
# plt.imshow(np.array(data)[0,:,:,:], cmap="gray")


print(f"history keys {history.keys()}")


# output_json = []
# gt = []
# yHats = []
# #for i in range(len(testGen)):
# for i in range(10):
#     temp = {}
#     testBatch = testGen[i]
    
# #     print(testBatch[0].shape)
# #     print(testBatch[1].shape)
        
#     temp['batch'] = i
#     temp['images'] = testBatch[0].tolist()
#     temp['gt'] = testBatch[1].tolist()
#     temp['prediction'] = modelL.predict(testBatch[0]).tolist()

#     #todo adapt gt in DataGenerator!
#     for j in range(4):
#         t = {}
#         t['image'] = temp['images'][j]
#         t['gt'] = temp['gt'][j]
#         t['prediction'] = temp['prediction'][j]
#         # save output
#         helpers.showImageWithHeatmap(np.array(t['image']), hm=np.array(t['prediction']), gt=None, group=1, bodyPart="front", filename=f"{out_path}batch{i}-image{j}.jpg")
#         with open(f"{out_path}predictions-batch{i}-image{j}.json", 'w') as outfile:
#             json.dump(t, outfile)



# evaluation --------------------------------------------------------#
# print("load predictions")
# # p = "../data/tests/1/predictions-batch0-image0-20200531-111730.json"
# # p = "../data/tests/1/predictions-batch0-image1-20200531-111822.json"
# # p = "../data/tests/1/predictions-batch0-image2-20200531-111914.json"
# # p = "../data/tests/1/predictions-batch0-image3-20200531-112006.json"

# p = out_path + "predictions-batch0-image0.json"
# with open(p, 'r') as f:
#     out = json.load(f)

# pred =  np.asarray(out['prediction'])

# print(f"Is there any non-zero entry in gt, i.e. any animal on image? {np.any(np.array(out['gt']))}")
# print(f"Prediction: {np.min(pred), np.max(pred)}")
# helpers.showImageWithHeatmap(np.asarray(out['image']), pred)
# helpers.showImageWithHeatmap(np.asarray(out['image']), np.asarray(out['gt']))

print(f"MAE: {history['mae']}")
print(f"Loss: {history['loss']}")

# plot mae history
# plt.plot(history['mae'])
# plt.plot(history['val_mae'])
# plt.title('model mean absolute error')
# plt.ylabel('mae')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper right')
# #plt.savefig(out_path+"mae")
# plt.show()

# # plot loss history
# plt.plot(history['loss'])
# plt.plot(history['val_loss'])
# plt.title('model loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(['train', 'test'], loc='upper right')
# #plt.savefig(out_path+"loss")
# plt.show()
