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
import DataGenerator as dg
import Globals


test_path = "../data/output/55/"
out_path = test_path #+ "output/"

res = "-L"

model_path = "model" + res
testGen_path = "serialized_testGen" + res+ ".pickle"


# load annotation files
label_root = "../data/maritime_dataset_25/labels/"

path = "training_labels_animals.json"
with open(os.path.join(label_root, path) , 'r') as f:
    train_labels_animals = json.load(f)
    
path = "test_labels.json"
with open(os.path.join(label_root, path), 'r') as f:
    test_labels = json.load(f)
    
path = "training_labels_no_animals.json"
with open(os.path.join(label_root, path), 'r') as f:
    train_labels_no_animals = json.load(f)

hist_path = "trainHistory" + res + ".pickle"
a = "trainHistory-L1.pickle"
b = "trainHistory-L2.pickle"
c = "trainHistory-H.pickle"

# load testGen
# with open(os.path.join(test_path, testGen_path),'rb') as file:
#     raw_data = file.read()
# testGen = pickle.loads(raw_data)

# testGen = dg.DataGenerator (dataset=test_labels, 
#                               #hm_folder_path="../data/heatmaps_lowRes/test/" ,
#                               prepareEntry=dg.prepareEntryLowResHeatmap,
#                               batch_size=Globals.batch_size)


# load model
# todo look for file name (depends on timestamp)
modelL = keras.models.load_model(os.path.join(test_path,model_path))

# load training history
with open(os.path.join(test_path, a),'rb') as file:
    raw_data = file.read()
history = pickle.loads(raw_data)



print("Loading done")

############ predicting one specific image
f0 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/0.jpg"
f22 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/22.jpg"
f39 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/39.jpg"
f51 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/51.jpg"
f60 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/60.jpg"

f309 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/309.jpg" #crust
f867 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/867.jpg" #chaeto
f883 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/883.jpg" #chaeto
f913 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/913.jpg" #chaeto
f575 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/575.jpg" #jellyfish
f193 = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/193.jpg" #unidentified

#tests = {"f0":0, "f22":22, "f39":39, "f51":51, "f60":60}
tests = {"193":f193,"575":f575, "913":f913,"883":f883,"867":f867, "309":f309, "0":f0, "22":f22, "39":f39, "51":f51, "60":f60}
tests = {"60":f60}
tests = {"309":f309}
tests = {"867":f867}
tests = {"913":f913}
tests = {"575":f575}
tests = {"193":f193}
tests = {"51":f51}

for k, v in tests.items():
    entry = [entry for entry in test_labels if entry['filename'] == v][0]
    #entry = test_labels[i]
    image = np.asarray(helpers.loadImage(entry['filename']))
    image = 2.*image/np.max(image) - 1
    
    # groundtruth heatmap
    hm = HeatmapClass.Heatmap(entry)
    y = np.asarray(hm.hm)
    
    # predicted heatmap
    X = np.expand_dims(image, axis=0)
    yHat = modelL.predict(X)
    
    print(v)
    print(f"yhat shape {yHat[0].shape})")
    print(f"yhat shape {yHat[1].shape})")
   # print(f"yhat has range {np.min(yHat), np.max(yHat)}")
    print(k)
    print()
    
    # with open(out_path + str(i) + ".json", "w") as f:
    #    json.dump(yHat.tolist(), f)
    
    
    
    #helpers.showImageWithAnnotation(entry)
    animal="fish"
    print(animal)
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 1], gt=entry['animals'], exaggerate=1, group=1, bodyPart="front", filename=f"{out_path}test{k}{res}_{animal}_front_exag1.jpg")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 2], gt=entry['animals'], exaggerate=1, group=1, bodyPart="back", filename=f"{out_path}test{k}{res}_{animal}_back_exag1.jpg")
    
    animal="crustacea"
    print("crustacea")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 3], gt=entry['animals'], exaggerate=1, group=2, bodyPart="front", filename=f"{out_path}test{k}{res}_{animal}_front_exag1.jpg")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 4], gt=entry['animals'], exaggerate=1, group=2, bodyPart="back", filename=f"{out_path}test{k}{res}_{animal}_back_exag1.jpg")
    
    animal="chaetognatha"
    print("chaetognatha")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 5], gt=entry['animals'], exaggerate=1, group=3, bodyPart="front", filename=f"{out_path}test{k}{res}_{animal}_front_exag1.jpg")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 6], gt=entry['animals'], exaggerate=1, group=3, bodyPart="back", filename=f"{out_path}test{k}{res}_{animal}_back_exag1.jpg")
    
    animal="unidentified"
    print("unidentified")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 7], gt=entry['animals'], exaggerate=1, group=4, bodyPart="front", filename=f"{out_path}test{k}{res}_{animal}_front_exag1.jpg")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 8], gt=entry['animals'], exaggerate=1, group=4, bodyPart="back", filename=f"{out_path}test{k}{res}_{animal}_back_exag1.jpg")
    
    animal="jellyfish"
    print("jellyfish")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 9], gt=entry['animals'], exaggerate=1, group=5, bodyPart="front", filename=f"{out_path}test{k}{res}_{animal}_front_exag1.jpg")
    helpers.showImageWithHeatmap(image, yHat[0][0, :, :, 10], gt=entry['animals'], exaggerate=1, group=5, bodyPart="back", filename=f"{out_path}test{k}{res}_{animal}_back_exag1.jpg")
    
    #helpers.showImageWithHeatmap(image, yHat[0, :, :, :], gt=entry['animals'], exaggerate=10)#, filename=f"{out_path}test{k}{res}_exag10.jpg")
    # helpers.showImageWithHeatmap(image, yHat[0, :, :, :], gt=entry['animals'], exaggerate=100, filename=f"{out_path}test{k}{res}_exag100.jpg")
   # helpers.showImageWithHeatmap(image, yHat[0, :, :, :], gt=entry['animals'], exaggerate=1)
    #print(helpers.entropy(yHat))

# show heatmap only
# with open(out_path+str(i)+".json","r") as f:
#     data=json.load(f)
# data = np.array(data)[0,:,:,:]
# plt.imsave(out_path + str(i) +'_hm.png', data[:,:,0], cmap='gray')
# plt.imshow(data[:,:,0], cmap="gray")
# #image = np.ones(shape=image.shape)*255 # black image
# helpers.showImageWithHeatmap(image, data, filename=out_path+str(i)+"_image_hm.jpg")


# print(f"({np.min(data), np.max(data)})")

# print(f"history keys {history.keys()}")


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

key = "mae"

print(f"key: {history[key]}")
print(f"Loss: {history['loss']}")


# plot mae history
plt.plot(history[key])
plt.plot(history[f'val_{key}'])
plt.title(f'model{res} {key}')
plt.ylabel(key)
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.savefig(out_path+f"{key}{res}2.png")
plt.show()

# plot loss history
plt.plot(history['loss'])
plt.plot(history['val_loss'])
plt.title(f'model{res} loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.savefig(out_path+f"loss{res}2.png")
plt.show()
