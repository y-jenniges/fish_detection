import os
import numpy as np
import pandas as pd
import tensorflow as tf
import Helpers
import Losses

GROUP_DICT = {0: "Nothing", 1: "Fish", 2: "Crustacea", 3: "Chaetognatha", 4: "Unidentified", 5: "Jellyfish"}


CLASS_WEIGHTS = np.array([ 1,  1.04084507,  1.04084507,  1,  1,
        8.90361446,  8.90361446, 13.19642857, 13.19642857, 12.52542373,
       12.52542373])

class Predicter():
    def __init__(self, neural_network_path=None, class_weights=None):
        
        self.neural_network = None
        
        if class_weights is not None:
            self.weights = class_weights
        else:
            self.weights = CLASS_WEIGHTS
        
        if neural_network_path is not None:
            self.neural_network = self.loadNeuralNet()
        
    def loadNeuralNet(self, path, weights=None):
        print("load nn in helpers")
        if os.path.isfile(path):
            try:
                # if specified, use given weights
                w = self.weights if weights is None else weights
                
                # load model
                self.neural_network = tf.keras.models.load_model(path, custom_objects={
                        "loss": Losses.weighted_categorical_crossentropy(w)})
                return True
            except:               
                Helpers.displayErrorMsg(
                    "Loading Error", 
                    f"The neural network from {path} is not a valid model.",
                    "Error") 
                return False    
        else:
            Helpers.displayErrorMsg("Path Error", 
                                    f"The neural network path is not valid.",
                                    "Error") 
            return False
        
    def predictImage(self, img_path):
        # create dataframe to store predictions
        df = pd.DataFrame(columns=["group", "LX1", "LY1", "LX2", "LY2"])
        
        # load image
        image = loadImage(img_path, factor=32)
        img = loadImage(img_path, factor=32, rescale_range=False)

        # predict image
        print("model loaded. predicting...")
        prediction = applyNnToImage(model, image)
        print("prediction done")
        
        # iterate over the animal groups
        for i in range(1, prediction.shape[3], 2):
            print(i)
            
            heads = prediction[0,:,:,i]*255
            heads = heads.astype('uint8')
            
            tails = prediction[0,:,:,i+1]*255
            tails = tails.astype('uint8')
        
            # get coordinates
            print("get head coordinates")
            head_coordinates = Helpers.findCoordinates(heads, 110, 5) # thresh for fish:100, jellyfish:10?
            print("get tail coordinates")
            tail_coordinates = Helpers.findCoordinates(tails, 110, 5)
            
            print("find head tail matches")
            # find head-tail matches
            matches = Helpers.findHeadTailMatches(head_coordinates, tail_coordinates)
        
            # scale matches to image resolution
            matches = Helpers.scaleMatchCoordinates(matches, heads.shape, img.shape)
            
            group = GROUP_DICT[np.ceil(i/2)]
            
            #file_id = Rectified_TN_Exif_Remos1_2015.08.02_00.00.49
            
            # show prediction heatmap and coordinates
            plt.imshow(heads, cmap=plt.cm.gray)
            plt.autoscale(False)
            plt.plot(head_coordinates[:, 0], head_coordinates[:, 1], 'r.')
            plt.show()
            
            plt.imshow(tails, cmap=plt.cm.gray)
            plt.autoscale(False)
            plt.plot(tail_coordinates[:, 0], tail_coordinates[:, 1], 'r.')
            plt.show()
        
            # plot each match with a different colour
            colors = cm.rainbow(np.linspace(0, 1, matches.shape[0]))
            plt.imshow(heads, cmap=plt.cm.gray)
            plt.imshow(img)
            for i in range(matches.shape[0]):
                plt.scatter(matches[i,:,0], matches[i,:,1], color=colors[i])
                plt.plot([matches[i,0,0], matches[i,1,0]], [matches[i,0,1], matches[i,1,1]], color=colors[i])
            plt.show()
            
            for m in matches:
                animal = {"group": group, 
                          "LX1": m[0][0], "LY1": m[0][1], # head
                          "LX2": m[1][0], "LY2": m[1][1]} # tail
                df = df.append(animal, ignore_index=True)        
            
        return df
        
        def predictImageList(self, images):
            predictions = []
            for image in images:
                predictions.append(self.predictImage(image))
            
            return predictions
            