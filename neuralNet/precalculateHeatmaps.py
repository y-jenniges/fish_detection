import json
import os
import numpy as np
import HeatmapClass
import HelperFunctions as helpers

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
   
labels_list = [train_labels_animals, test_labels, train_labels_no_animals]
data = labels_list[1]
    
# for every image, calculate heatmap
hm_path = "../data/heatmaps/test_hms.json"

def calculateAllHeatmapsForImage(entry):
    heatmap0f = HeatmapClass.Heatmap(entry, resolution='low', group=0, bodyPart='front').hm
    heatmap0b = HeatmapClass.Heatmap(entry, resolution='low', group=0, bodyPart='back').hm
    heatmap1f = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='front').hm
    heatmap1b = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='back').hm
    heatmap2f = HeatmapClass.Heatmap(entry, resolution='low', group=2, bodyPart='front').hm
    heatmap2b = HeatmapClass.Heatmap(entry, resolution='low', group=2, bodyPart='back').hm
    heatmap3f = HeatmapClass.Heatmap(entry, resolution='low', group=3, bodyPart='front').hm
    heatmap3b = HeatmapClass.Heatmap(entry, resolution='low', group=3, bodyPart='back').hm
    heatmap4f = HeatmapClass.Heatmap(entry, resolution='low', group=4, bodyPart='front').hm
    heatmap4b = HeatmapClass.Heatmap(entry, resolution='low', group=4, bodyPart='back').hm
    heatmap5f = HeatmapClass.Heatmap(entry, resolution='low', group=5, bodyPart='front').hm
    heatmap5b = HeatmapClass.Heatmap(entry, resolution='low', group=5, bodyPart='back').hm
    
        
    image = helpers.loadImage(entry['filename'])/np.array(128,dtype=np.float32)-np.array(1,dtype=np.float32)

    hms = [(image, heatmap0f), (image, heatmap0b), (image, heatmap1f), (image, heatmap1b), \
        (image, heatmap2f), (image, heatmap2b), (image, heatmap3f), (image, heatmap3b),\
        (image, heatmap4f), (image, heatmap4b), (image, heatmap5f), (image, heatmap5b)]
       
    print(f"image done: {entry['filename']}")
    return {'filename':entry['filename'], 'image':image, 'heatmaps':hms}

hms_json = []
# iterate over all images
for entry in data:   
    prepared_entry = calculateAllHeatmapsForImage(entry)
    hms_json.append(prepared_entry)
    
with open(hm_path, 'w') as outfile:
    json.dump(hms_json, outfile)