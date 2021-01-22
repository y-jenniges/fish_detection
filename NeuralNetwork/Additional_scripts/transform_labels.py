# transform labels from 6 classes (one hot encoding) to  12 classes (one hot encoding)

import json
import os
import numpy as np
import HeatmapClass
import HelperFunctions as helpers

# load annotation files
#label_root = "../data/maritime_dataset/labels/"
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
   
labels_list = [train_labels_animals, test_labels, train_labels_no_animals]
data = labels_list[2]
    

# new_json = []
for i in range(len(data)):    
    #data[i]['filename'] = data[i]['filename'].replace('_dataset','_dataset_25')
    data[i]['filename'] = data[i]['filename'].replace("_25","",1)
    
    # quarter the resolution of the positions as well
    # for j in range(len(data[i]['animals'])):
    #     data[i]['animals'][j]['position'][0] = data[i]['animals'][j]['position'][0]/4
    #     data[i]['animals'][j]['position'][1] = data[i]['animals'][j]['position'][1]/4
        
#     temp = {}
#     temp['filename'] = data[i]['filename']
#     temp['animals'] = []
    
#     # iterate over animals
#     for j in range(len(data[i]['animals'])):
#         group_idx = data[i]['animals'][j]['group'].index(1)
#         new_idx = 2*group_idx  # index for front class
        
#         temp2 = {}
#         temp3 = {}
#         temp2['group'] = np.zeros(12).tolist()
#         temp3['group'] = np.zeros(12).tolist()
        
        
#         if group_idx == 0:
#             print(f"found a nothing class element! in data({i}), animal number {j}")

#         temp2['group'][new_idx] = 1
#         temp2['position'] = data[i]['animals'][j]['front']
        
#         temp3['group'][new_idx+1] = 1 # back class
#         temp3['position'] = data[i]['animals'][j]['back']
            
#         temp['animals'].append(temp2)
#         temp['animals'].append(temp3)
            
#     new_json.append(temp)    
    
 
    
with open(f"trainin_labels_no_animals.json", 'w') as outfile:
    json.dump(data, outfile)
# with open(f"training_labels_no_animals.json", 'w') as outfile:
#     json.dump(new_json, outfile)
    
    