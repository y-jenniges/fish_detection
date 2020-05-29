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
   

def calculateAllHeatmapsForImage(entry):
    """Calculate all 12 heatmaps for the given image and save them in a json file"""
    heatmap0f = HeatmapClass.Heatmap(entry, resolution='low', group=0, bodyPart='front').hm.tolist()
    heatmap0b = HeatmapClass.Heatmap(entry, resolution='low', group=0, bodyPart='back').hm.tolist()
    heatmap1f = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='front').hm.tolist()
    heatmap1b = HeatmapClass.Heatmap(entry, resolution='low', group=1, bodyPart='back').hm.tolist()
    heatmap2f = HeatmapClass.Heatmap(entry, resolution='low', group=2, bodyPart='front').hm.tolist()
    heatmap2b = HeatmapClass.Heatmap(entry, resolution='low', group=2, bodyPart='back').hm.tolist()
    heatmap3f = HeatmapClass.Heatmap(entry, resolution='low', group=3, bodyPart='front').hm.tolist()
    heatmap3b = HeatmapClass.Heatmap(entry, resolution='low', group=3, bodyPart='back').hm.tolist()
    heatmap4f = HeatmapClass.Heatmap(entry, resolution='low', group=4, bodyPart='front').hm.tolist()
    heatmap4b = HeatmapClass.Heatmap(entry, resolution='low', group=4, bodyPart='back').hm.tolist()
    heatmap5f = HeatmapClass.Heatmap(entry, resolution='low', group=5, bodyPart='front').hm.tolist()
    heatmap5b = HeatmapClass.Heatmap(entry, resolution='low', group=5, bodyPart='back').hm.tolist()
    
    data = {'hm_0f':heatmap0f, 'hm_0b':heatmap0b, 'hm_1f':heatmap1f, 'hm_1b':heatmap1b, \
            'hm_2f':heatmap2f, 'hm_2b':heatmap2b, 'hm_3f':heatmap3f, 'hm_3b':heatmap3b, \
            'hm_4f':heatmap4f, 'hm_4b':heatmap4b, 'hm_5f':heatmap5f, 'hm_5b':heatmap5b}
    
    with open(hm_path + entry['filename'].split("/")[-1].rsplit(".jpg",1)[0] + '.json','w') as file:
        json.dump(data, file)
    
    print(f"image done: {entry['filename']}")


# label files to work on 
labels_list = [train_labels_animals, test_labels, train_labels_no_animals]
data = labels_list[0]
    
# path to store heatmaps
hm_path = "../data/heatmaps_lowRes/training_animals/"
#hm_path = "../data/heatmaps_highRes/training_animals/"

# iterate over all images
for entry in data:   
    prepared_entry = calculateAllHeatmapsForImage(entry)
    
