import pandas as pd
import numpy as np
import keras
import tensorflow as tf
import HelperFunctions as helpers
from sklearn.metrics import confusion_matrix
import DataGenerator as dg
import Losses 

from tensorflow import random
#from tensorflow import set_random_seed

# fix random seeds of numpy and tensorflow for reproducability
np.random.seed(0)
random.set_seed(2)
#set_random_seed(2)

BATCH_SIZE = 1
model_path = "../data/output/800/model-H"

# get gt
label_root = "../data/maritime_dataset_25/labels/"
test_labels, train_labels_animals, train_labels_no_animals, val_labels, class_weights = helpers.loadAndSplitLabels(label_root)
weights = np.array(list(class_weights.values()))
test_labels = test_labels[:2]

fish_id = [0.0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
fish_labels = helpers.filter_labels_for_animal_group(test_labels, fish_id)

crust_id = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
crust_labels = helpers.filter_labels_for_animal_group(test_labels, crust_id)

chaetognatha_id = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
chaeto_labels = helpers.filter_labels_for_animal_group(test_labels, chaetognatha_id)

unidentified_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]  
unidentified_labels = helpers.filter_labels_for_animal_group(test_labels, unidentified_id)

jellyfish_id = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
jellyfish_labels = helpers.filter_labels_for_animal_group(test_labels, jellyfish_id)


# load model
model = keras.models.load_model(model_path, custom_objects={"loss": Losses.weighted_categorical_crossentropy(weights)})
print("model loaded")

prepareEntry=dg.prepareEntryHighResHeatmap

testGen = dg.DataGenerator (dataset=test_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)

tfi = dg.DataGenerator(dataset=fish_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tcr = dg.DataGenerator(dataset=crust_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tch = dg.DataGenerator(dataset=chaeto_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tje = dg.DataGenerator(dataset=jellyfish_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)
tun = dg.DataGenerator(dataset=unidentified_labels, prepareEntry=prepareEntry, batch_size=BATCH_SIZE, shuffle=False)

gens = [testGen]#, tfi, tcr, tch, tje, tun]


# evaluate coordinates
eval_df = pd.DataFrame(0, columns=["tp", "tn", "fp", "fn"], 
                       index=["fish_head", "fish_tail", "crust_head", "crust_tail", 
                              "chaeto_head", "chaeto_tail", "unid_head", "unid_tail", 
                              "jelly_head", "jelly_tail"])




for t in gens:
    asum = 0
    rsum = 0
    psum = 0
    fpsum = 0
    fnsum = 0
    tpsum = 0
    tnsum = 0
    for i in range(len(t)):
        print(i)
        x = t[i][0]
        y_true = t[i][1]
        y_pred = model.predict(x)
        
        # fish head
        y_true = t[i][1][0,:,:,1]
        y_pred = y_pred[0,:,:,1]
        
        # fish tail
        y_true = t[i][1][0,:,:,2]
        y_pred = y_pred[0,:,:,2]
        
        #image = x[0,:,:,:]
        #helpers.showImageWithHeatmap(image, y_pred[0,:,:,1], None, 1, "front")
        #helpers.showImageWithHeatmap(image, y_pred[0,:,:,5], None, 3, "front")
        #helpers.showImageWithHeatmap(image, y_pred, None, 5, "front")
        acc = tf.keras.metrics.Accuracy()
        acc.update_state(y_true, y_pred)
        
        recall = tf.keras.metrics.Recall()
        recall.update_state(y_true, y_pred)
        #print("recall", recall.result().numpy())
        
        precision = tf.keras.metrics.Precision()
        precision.update_state(y_true, y_pred)
        #print("precision", precision.result().numpy())
        
        fp = tf.keras.metrics.FalsePositives()
        fp.update_state(y_true, y_pred)
        #print("false positives", fp.result().numpy())
        
        fn = tf.keras.metrics.FalseNegatives()
        fn.update_state(y_true, y_pred)
        #print("false negatives", fn.result().numpy())
        
        tp = tf.keras.metrics.TruePositives()
        tp.update_state(y_true, y_pred)
        #print("true positives", tp.result().numpy())
        
        tn = tf.keras.metrics.TrueNegatives()
        tn.update_state(y_true, y_pred)
        #print("true negatives", tn.result().numpy())
        
        asum += acc.result().numpy()
        rsum += recall.result().numpy()
        psum += precision.result().numpy()
        fpsum += fp.result().numpy()
        fnsum += fn.result().numpy()
        tpsum += tp.result().numpy()
        tnsum += tn.result().numpy()
        

        
        
    print("avg acc: ", asum/len(t))
    print("avg recall: ", rsum/len(t))
    print("avg precision: ", psum/len(t))
    print("avg fp: ", fpsum/len(t))
    print("avg fn: ", fnsum/len(t))
    print("avg tp: ", tpsum/len(t))   
    print("avg tn: ", tnsum/len(t))
