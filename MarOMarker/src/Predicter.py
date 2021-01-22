import os
import numpy as np
import pandas as pd
import tensorflow as tf
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
import Helpers
import PostProcessing as pp
import Losses

GROUP_DICT = {0: "Nothing", 1: "Fish", 2: "Crustacea", 
              3: "Chaetognatha", 4: "Unidentified", 5: "Jellyfish"}

#IMAGE_SHAPE = (4272, 2848)
IMAGE_SHAPE = (2848, 4272)

CLASS_WEIGHTS = np.array([ 1,  1.04084507,  1.04084507,  1,  1,
        8.90361446,  8.90361446, 13.19642857, 13.19642857, 12.52542373,
       12.52542373])

class Predicter():
    """
    Class that handles the complete prediction process. First, animal posisions
    and groups on an image are predicted with a neural network. The 
    generated location heatmaps are then focused into single points. Then,
    heads and tails are matched. 
    
    Attributes
    ----------
    neural_network: keras model
        Neural network used for the predictions.
    class_weights:
        Class weights used by the neural network.
    """
    
    def __init__(self, neural_network_path=None, class_weights=None):
        """
        Init function.

        Parameters
        ----------
        neural_network_path : string, optional
            Path to neural network used for predictions. The default is None.
        class_weights : list<float>, optional
            Class weights for the neural network. The default is None.
        """
        self.neural_network = None
        
        if class_weights is not None:
            self.weights = class_weights
        else:
            self.weights = CLASS_WEIGHTS
        
        if neural_network_path is not None:
            self.loadNeuralNet(neural_network_path)
        
    def loadNeuralNet(self, path, weights=None):
        """
        Loads a neural network from a path with weights for the weighted
        categorical crossentropy loss.

        Parameters
        ----------
        path : string
            Path to neural network.
        weights : list<float>, optional
            Class weights for the network. The default is None.

        Returns
        -------
        bool
            True, if the loading was successfull.
        """
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
                                    f"The neural network path {path} is invalid.",
                                    "Error") 
            return False
        
    def predictImage(self, img_path, file_id, experiment_id="", user_id=""):
        """
        Handles the prediction of an image. From the neural network prediction
        (heatmaps), coordinates are inferred. Then, heads and tails are 
        matched.

        Parameters
        ----------
        img_path : string
            Path to the image to predict.
        file_id : string
            ID of the image. Used as file ID in the returned dataframe.
        experiment_id : string, optional
            ID of experiment. Used as experiment ID in the returned dataframe. 
            The default is "".
        user_id : string, optional
            ID of currently working user. The default is "".

        Returns
        -------
        df : DataFrame
            Prediction information wrapped in a dataframe.
        """
        # create dataframe to store predictions
        df = pd.DataFrame(columns=["file_id", "object_remarks", "group", 
                                   "species", "LX1", "LY1", "LX2", "LY2"])
        
        if self.neural_network is not None:    
            print("predicter: nn not none")
            
            # load image
            image = pp.loadImage(img_path, factor=32)
            print("predicter: image loaded")
            img = pp.loadImage(img_path, factor=32, rescale_range=False)
    
            print("predicter: image and img loaded")
    
            # predict image
            prediction = pp.applyNnToImage(self.neural_network, image)
            
            print("predicter: prediction done")
            
            # iterate over the animal groups
            for i in range(1, prediction.shape[3], 2):
                heads = prediction[0,:,:,i]*255
                heads = heads.astype('uint8')
                
                tails = prediction[0,:,:,i+1]*255
                tails = tails.astype('uint8')
            
                # get coordinates
                head_coordinates = pp.findCoordinates(heads, 110, 5) 
                tail_coordinates = pp.findCoordinates(tails, 110, 5)
                
                print("predicter: coordinates found")
                
                # find head-tail matches
                matches = pp.findHeadTailMatches(head_coordinates, tail_coordinates)

                print("predicter: matches found")
                # # show prediction heatmap and coordinates
                # plt.imshow(heads, cmap=plt.cm.gray)
                # plt.autoscale(False)
                # plt.plot(head_coordinates[:, 0], head_coordinates[:, 1], 'r.')
                # plt.show()
                
                # plt.imshow(tails, cmap=plt.cm.gray)
                # plt.autoscale(False)
                # plt.plot(tail_coordinates[:, 0], tail_coordinates[:, 1], 'r.')
                # plt.show()
            
                # # plot each match with a different colour
                # colors = cm.rainbow(np.linspace(0, 1, matches.shape[0]))
                # plt.imshow(heads, cmap=plt.cm.gray)
                # plt.imshow(img)
                # for i in range(matches.shape[0]):
                #     plt.scatter(matches[i,:,0], matches[i,:,1], color=colors[i])
                #     plt.plot([matches[i,0,0], matches[i,1,0]], [matches[i,0,1], matches[i,1,1]], color=colors[i])
                # plt.show()
                
                # scale matches to image resolution
                matches = pp.scaleMatchCoordinates(matches, heads.shape, IMAGE_SHAPE)
                
                group = GROUP_DICT[np.ceil(i/2)]
                species = "Unidentified"
                
                for m in matches:
                    animal = {"file_id": file_id, 
                              "object_remarks": "", 
                              "group": group, 
                              "species": species,
                              "LX1": m[0][0],
                              "LY1": m[0][1],
                              "LX2": m[1][0],
                              "LY2": m[1][1],
                              "LX3": -1, 
                              "LY3": -1,
                              "LX4": -1,
                              "LY4": -1,
                              "RX1": -1,
                              "RY1": -1,
                              "RX2": -1,
                              "RY2": -1,
                              "RX3": -1, 
                              "RY3": -1,
                              "RX4": -1,
                              "RY4": -1,
                              "length": -1,
                              "height": -1,
                              "image_remarks": "",
                              "status": "not checked",
                              "manually_corrected": "False",
                              "experiment_id": experiment_id,
                              "user_id": user_id}
                    df = df.append(animal, ignore_index=True)          
        else:
            Helpers.displayErrorMsg(
                "Missing Neural Network", 
                "Please specify a neural network on settings page.", 
                "Error")
            
        return df
        
    def predictImageList(self, image_pathes):
        """
        Predicts a list of images.

        Parameters
        ----------
        image_pathes : list<string>
            Pathes to images to predict.

        Returns
        -------
        df : DataFrame
            Prediction information wrapped in a dataframe..
        """
        df = pd.DataFrame(columns=["file_id", "object_remarks", "group", "species", 
                "LX1", "LY1", "LX2", "LY2", "LX3", "LY3", "LX4", "LY4", 
                "RX1", "RY1", "RX2", "RY2", "RX3", "RY3", "RX4", "RY4",
                "length", "height", "image_remarks", "status",
                "manually_corrected", "experiment_id", "user_id"]) 
        for path in image_pathes:
            df.append(self.predictImage(path))
        
        return df
            