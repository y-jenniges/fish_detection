"""
Adapted from lecture "Anwendungen der Bildverarbeitung" by Udo Frese, 
University Bremen, 2019
"""
import numpy as np
import matplotlib.pyplot as plt
import HelperFunctions as helpers

# number of animal groups
NUM_GROUPS = 6


class Heatmap():
    """
    This class stores a heatmap and performs the heatmap calculations.
    
    Attributes
    ----------
    imagePath: str
        Path to the image for which the heatmap should be computed
    image: ndarray
        Loaded image
    gt: list of dicts (keys: group, posistion)
        Groundtruth animals on the given image
    group: int
        Animal group (1: fish, 2: crustacea, 3: chaetognatha, 4: unidentified, 5: jellyfish)
    bodyPart: str
        Body parts to display. It is either 'front', 'back' or 'connection'
    gaussian: ndarray
        Gaussian block to add to the heatmap

    
    Methods
    -------
    showImageWithHeatmap(group=None, bodyPart=None, filename=None, exaggerate=1)
        Shows the heatmap superimposed on the image. Recalculates heatmap if 
        different group or bodyPart is desired. 
    downsample(factor=32)
        Downsamples the heatmap by a given factor. 
    """
    
    def __init__(self, entry, group=1, bodyPart="front"): 
        """
        Init function. 

        Parameters
        ----------
        entry : dict (keys: filename, animals)
            Groundtruth entry to create the heatmap for.
        group : int, optional
            Animal group. The default is 1, i.e. fish.
        bodyPart : str, optional
            Bodypart to create the heatmap for. The default is "front".
        """
        assert bodyPart == "front" or bodyPart == "back" or bodyPart == "both" or bodyPart=="connection" 
        assert group in range(NUM_GROUPS)
        
        self.imagePath = entry["filename"]
        self.image = helpers.loadImage(self.imagePath, 32)
        self.gt = entry["animals"]
        self.group = group
        self.bodyPart = bodyPart
            
        # calculate the gaussian function (used to generate the heatmap)
        self.gaussian = helpers.gaussian(8,50)      
         
        # calculate heatmap
        if bodyPart == "both":
            self._calculateHeadTailHeatmap(self.group)
        elif bodyPart == "connection":
            self._annotationToConnectionHm()
        else:
            self._annotationToHeatmap()

    def _annotationToConnectionHm(self):
        """ Converts a list of heads and tails, which are 2D coordinates, 
        into a heatmap which displays the connection between heads and tails.
        """
        # a different gaussian shape (so that the line is not too thick)
        self.gaussian = helpers.gaussian(8,10)
        
        # initialize the heatmap
        hm_y, hm_x = self.image.shape[0], self.image.shape[1]
        self.hm = np.zeros ((hm_y, hm_x, 1), dtype=np.float32)
        
        # arrays for matching the animal group
        group_head = np.zeros(NUM_GROUPS*2 - 1)
        group_tail = np.zeros(NUM_GROUPS*2 - 1)
        group_head[self.group*2-1] = 1
        group_tail[self.group*2] = 1

        # initalize list for heads and tails
        heads = []
        tails = []
        
        # get all heads and tails from the groundtruth
        for animal in self.gt:
            if np.array_equal(animal['group'], group_head):
                heads.append([animal['position'][0], animal['position'][1]])
            if np.array_equal(animal['group'], group_tail):
                tails.append([animal['position'][0], animal['position'][1]])
        
        # iterate over animals        
        for i in range(len(heads)):    
            # calculate slope and intercept of the line connecting head and tail of the animal
            deltaY = heads[i][1] - tails[i][1]
            deltaX = heads[i][0] - tails[i][0]
            
            if deltaX == 0: 
                m = 0
            else:
                m = deltaY/deltaX
                
            b = heads[i][1] - m*heads[i][0]
            
            # calculate the y-values of the line
            xmax = max(int(heads[i][0]), int(tails[i][0]+1))
            xmin = min(int(heads[i][0]), int(tails[i][0]+1))
            
            x = np.array(range(xmin, xmax))
            y = m*x + b

            # for every point on the line, add a gaussian to the heatmap
            for j in range(len(x)-1):
                if 0 <= x[j] < self.hm.shape[1] and 0 <= y[j] < self.hm.shape[0]: 
                    self._addToHeatmap(self.gaussian, x[j]-self.gaussian.shape[1]//2, y[j]-self.gaussian.shape[0]//2)
          
        # clip the heatmap to range [0, 1]
        np.clip (self.hm, 0, 1, out=self.hm)
                       
    def _annotationToHeatmap(self):
        """Converts a list of points (each a dict with 'x' and 'y' component) into 
        a heatmap with original image resolution using self.gaussian. For every 
        head and every tail, the Gaussian gaussian (peak 1) centered at the 
        annotated head/tail point is added."""
        hm_y, hm_x = self.image.shape[0], self.image.shape[1]
        self.hm = np.zeros ((hm_y, hm_x, 1), dtype=np.float32)

        # specify animal group
        group_array = np.zeros(NUM_GROUPS*2 - 1)
        if self.group == 0:
            group_array[0] = 1 
        else:
            if self.bodyPart=='front':
                group_array[self.group*2-1] = 1 
            elif self.bodyPart=='back':
                group_array[self.group*2] = 1 
            elif self.bodyPart=='both':
                print("annotation to high res heatmap: invalid bodyPart")
            
        # iterate over animals in the groundtruth that are of the desired group
        for animal in self.gt:
            if np.array_equal(animal['group'], group_array):
                x = animal['position'][0]
                y = animal['position'][1]
            
                # add block to heatmap
                if 0 <= x < self.hm.shape[1] and 0 <= y < self.hm.shape[0]: 
                    self._addToHeatmap (self.gaussian, x-self.gaussian.shape[1]//2, y-self.gaussian.shape[0]//2)
        
        # make sure that the heatmap is in range [0,1]
        np.clip (self.hm, 0, 1, out=self.hm)

    def _addToHeatmap (self, block, x, y):
        """Adds block to hm[y:y+block.shape[0],x:x+block.shape[1]] and 
         works even if part of block extends outside hm. hm and block
         have both 3 dimensions (w*h*c)."""
      # We have a rectangle hm[hylo:hyhi,hxlo:hxhi] 
      # and a rectangle block[bylo:byhi,bxlo:bxhi] which should be added to the
      # hm-rectangle. Some of the h-indices may be out of bounds in which case
      # both the h-index and the corresponding b-index must be adapted.
        # round x and y such that they are integers (rounded to the pixel grid)
        x = round(x)
        y = round(y)
      
        bsy, bsx,_ = block.shape
        hsy, hsx,_ = self.hm.shape
        # Initially start with considering the full b-block
        hxlo = int(x)
        hylo = int(y)
        hxhi = int(x+bsx)
        hyhi = int(y+bsy)
        bxlo = 0
        bylo = 0
        bxhi = int(bsx)
        byhi = int(bsy)
        if 0<=hxlo and hxhi<=hsx and 0<=hylo and hyhi<=hsy: # fully inside hm
            self.hm[hylo:hyhi,hxlo:hxhi] += block
        else: 
            if hxlo<0: hxlo, bxlo = 0, bxlo-hxlo # clip left side
            if hxhi>hsx: hxhi, bxhi = hsx, bxhi+hsx-hxhi # clip right side
            if hylo<0: hylo, bylo = 0, bylo-hylo # clip top side
            if hyhi>hsy: hyhi, byhi = hsy, byhi+hsy-hyhi # clip bottom side
            if bxlo>=bxhi or bylo>=byhi: return # fully outside hm
            #print(f"hm[{hylo}:{hyhi},{hxlo}:{hxhi}] += block[{bylo}:{byhi},{bxlo}:{bxhi}]")
            self.hm[hylo:hyhi,hxlo:hxhi] += block[bylo:byhi,bxlo:bxhi]
    
    def showImageWithHeatmap (self, group=None, bodyPart=None, filename=None, exaggerate=1):
        """Shows image, the annotation by a heatmap hm [0..1] and the groundTruth gt. 
         The hm.shape must be an integer fraction of the image shape. gt must 
         have be a list of dicts with 'x' and 'y' entries as in the dataset. 
         Both hm and gt can be None in which case they are skipped. 
         If filename is given, the plot is saved."""
         
        if group==None: group=self.group
        if bodyPart==None: bodyPart=self.bodyPart
        
        assert bodyPart == "front" or bodyPart == "back" or bodyPart == "both" or bodyPart=="connection"
        assert group in range(NUM_GROUPS)
        
        # copy image (so the heatmap is not drawn on original)
        img = self.image.copy()
           
        # if a heatmap for another group or bodyPart is wished, calculate it
        if self.group != group or self.bodyPart != bodyPart:
            if bodyPart == 'both':
                self._calculateHeadTailHeatmap(group)
            else:
                self.group = group
                self.bodyPart = bodyPart
                self._annotationToHeatmap()
        
        if self.hm is not None:      
            factor = img.shape[0]//self.hm.shape[0]
    
            assert self.hm.shape[0]*factor==img.shape[0] and self.hm.shape[1]*factor==img.shape[1]
            assert len(self.hm.shape)==3
            
            hmResized = np.repeat (self.hm, factor, axis=0) # y
            hmResized = np.repeat (hmResized, factor, axis=1) #x
            hmResized = np.repeat (hmResized, 3, axis=2) # factor for RGB
            hmResized = np.clip (hmResized*2, 0, 1)
            
            if img.dtype =="uint8":
                img = img//2 + (128*exaggerate*hmResized).astype(np.uint8)
            else:
                img = ((img+1)*64 + 128*exaggerate*hmResized).astype(np.uint8)
        plt.imshow(img)

        # draw groundtruth if given
        if self.gt is not None:    
            
            # specify the one-hot encoding of the desired group
            group_array = np.zeros(NUM_GROUPS*2 - 1)
            if self.bodyPart=='front':
                group_array[self.group*2-1] = 1 
            elif self.bodyPart=='back' or self.bodyPart=='both':
                group_array[self.group*2] = 1 
                
            # draw groundtruth heads and/or tails depending on bodyPart
            if self.bodyPart=='both':     
                group_array_front = np.copy(group_array)
                group_array_front[np.argwhere(group_array==1)-1] = 1
                group_array_front[np.argwhere(group_array==1)] = 0
                
                x_front = [animal['position'][0] for animal in self.gt if np.array_equal(animal['group'], group_array_front)] 
                y_front = [animal['position'][1] for animal in self.gt if np.array_equal(animal['group'], group_array_front)]
                
                x_back = [animal['position'][0] for animal in self.gt if np.array_equal(animal['group'], group_array)]
                y_back = [animal['position'][1] for animal in self.gt if np.array_equal(animal['group'], group_array)]

                plt.scatter(x_front, y_front, s=20, marker='o', c='r')
                plt.scatter(x_back, y_back, s=20, marker='x', c='b')
            else:
                #print("gt is not None")
                x = [animal['position'][0] for animal in self.gt if np.array_equal(animal['group'], group_array) ]
                y = [animal['position'][1] for animal in self.gt if np.array_equal(animal['group'], group_array)]

                # for heads, draw o, for tails an x
                if bodyPart=='front':
                    marker='o'
                    color='r'
                else:
                    marker='x'
                    color='b'

                plt.scatter (x, y, s=20, marker=marker, c=color)
            
        if filename is not None:
            plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()
   
    def _calculateHeadTailHeatmap(self, group=None):
        """
        Calculates a heatmap showing both, heads and tails

        Parameters
        ----------
        group : int, optional
            Group for which to generate the heatmap. If None, the group of the
            Heatmap class instance will be used. 
        """
        if group==None: group=self.group
        
        # init one heatmap for animal head and one for animal tail
        hm_front = []
        hm_back = []
        
        # calculate front heatmap
        self.group = group     
        self.bodyPart = 'front'
        self._annotationToHeatmap()
        hm_front = self.hm 

        # calculate back heatmap
        self.bodyPart = 'back'
        self._annotationToHeatmap()
        hm_back = self.hm 

        # combine both heatmaps by taking the average
        self.bodyPart = 'both'
        self.hm = (hm_front + hm_back)/2

    def downsample (self, factor=32):
      """
      T must be a tensor with at least 3 dimension, where the last three 
      are interpreted as height, width, channels. Downsamples the height and 
      width dimension of T by the given factor. The length in these dimensions 
      must be a multiple of factor.
     
      Parameters
      ----------
        factor : int, optional
            Downsampling factor. If not specified, it is 32
      """
      sh = self.hm.shape
      assert sh[-3]%factor==0
      assert sh[-2]%factor==0
      newSh = sh[:-3] + (sh[-3]//factor, factor) + (sh[-2]//factor, factor) + sh[-1:]
      self.hm = self.hm.reshape(newSh).mean(axis=(-4, -2))
