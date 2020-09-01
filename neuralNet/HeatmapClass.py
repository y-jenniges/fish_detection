import numpy as np
import matplotlib.pyplot as plt
import HelperFunctions as helpers
import Globals


# todo load image before giving shape to heatmap! (due to padding)

# This class stores a heatmap and performs the calculations
class Heatmap():
    def __init__(self, entry, resolution='low', group = 1, bodyPart = 'front'):
        
        assert bodyPart == "front" or bodyPart == "back" or bodyPart == "both"
        assert group in range(Globals.NUM_GROUPS)
        
        #self.resolution = resolution
        self.imagePath = entry['filename']
        self.image = helpers.loadImage(self.imagePath)
        self.gt = entry['animals']
        self.group = group
        self.bodyPart = bodyPart
              
        # if self.resolution =='low':
        #     self.annotationToHeatmap = self.annotationToLowResHeatmap
        # elif self.resolution == 'high':
        #     self.annotationToHeatmap = self.annotationToHighResHeatmap
        # else:
        #     raise Exception(f"Resolution undefined: Resolution must be either 'low' or 'high'")
         
        self.gaussian = helpers.gaussian(8,50)
         
         
        # calculate heatmap
        if bodyPart == "both":
            self.calculateHeadTailHeatmap(self.group)
        else:
            self.annotationToHeatmap()

    def annotationToHeatmap(self):
        """Converts a list of points (each a dict with 'x' and 'y' component) into 
        a heatmap with original image resolution using myGaussian. For every 
        strawberry, the Gaussian myGaussian (peak 1) centered at the 
        annotated strawberry point is added."""
        hm_y, hm_x = self.image.shape[0], self.image.shape[1]
        self.hm = np.zeros ((hm_y, hm_x, 1), dtype=np.float32)

        group_array = np.zeros(Globals.channels)
        if self.group == 0:
            group_array[0] = 1 
        else:
            if self.bodyPart=='front':
                group_array[self.group*2-1] = 1 
            elif self.bodyPart=='back':
                group_array[self.group*2] = 1 
            elif self.bodyPart=='both':
                print("annotation to high res heatmap: invalid bodyPart")
            
        for animal in self.gt:
            if np.array_equal(animal['group'], group_array):
                x = animal['position'][0]
                y = animal['position'][1]
            
                if 0 <= x < self.hm.shape[1] and 0 <= y < self.hm.shape[0]: 
                    self.addToHeatmap (self.gaussian, x-self.gaussian.shape[1]//2, y-self.gaussian.shape[0]//2)
                
        np.clip (self.hm, 0, 1, out=self.hm)
     
    # def annotationToLowResHeatmap (self):   
    #     self.annotationToHm()
        
    # def annotationToHighResHeatmap (self):   
    #     self.annotationToHm()
        
    # def annotationToLowResHeatmap (self):
    #     """Converts a list of points (each a dict with 'x' and 'y' component) into 
    #      a heatmap with 1/32 of image resolution. A 1 is bilinearly distributed
    #      among the 4 heatmap pixels close to the annotated strawberry. This means,
    #      if the annotated strawberry is in the center of a heatmap pixel, this
    #      pixel gets increased by 1, if it is on the border between two pixel
    #      both get increased by 0.5 ,if it is on the corner between four pixel
    #      each gets increased by 0.25."""
    #     """group: 0 - nothing, 1 - fish, 2 - crustacea, 3- chaetognatha, 4 - unidentified_object, 5 - jellyfish
    #     bodyPart: 'front' or 'back'"""

    #     #print("annotation to low res hm")

    #     hm_y, hm_x = self.image.shape[0]//32, self.image.shape[1]//32
    #     self.hm = np.zeros ((hm_y, hm_x, 1), dtype=np.float32)
         
    #     group_array = np.zeros(Globals.channels)
    #     if self.bodyPart=='front':
    #         group_array[self.group*2-1] = 1 
    #     elif self.bodyPart=='back':
    #         group_array[self.group*2] = 1 
    #     else:
    #         print("annotationToLowResHeatmap: invalid bodyPart")
   
        
    #     for animal in self.gt:
    #         # only receive animals from group that is currently active in class
    #         if np.array_equal(animal['group'], group_array):
    #             #print(animal['group'])
    #             x, y = [animal['position'][0], animal['position'][1]]
    #             #print(x)
    #             hmx, alphaX = helpers.interpolate ((x-16)/32) # increase hmx by alpha, and hmx+1 by 1-alpha
    #             hmy, alphaY = helpers.interpolate ((y-16)/32) # increase hmy by alpha, and hmy+1 by 1-alpha
    

    #             if 0 <= hmx < self.hm.shape[1] and 0 <= hmy < self.hm.shape[0]: 
    #                 self.hm[hmy, hmx, 0] += alphaX*alphaY
    
    #             if 0 <= hmx + 1 < self.hm.shape[1] and 0 <= hmy < self.hm.shape[0]: 
    #                 self.hm[hmy, hmx + 1, 0] += (1-alphaX)*alphaY
    
    #             if 0 <= hmx < self.hm.shape[1] and 0 <= hmy + 1 < self.hm.shape[0]: 
    #                 self.hm[hmy + 1, hmx, 0] += alphaX*(1-alphaY)
    
    #             if 0 <= hmx + 1 < self.hm.shape[1] and 0 <= hmy+ + 1 < self.hm.shape[0]: 
    #                 self.hm[hmy + 1, hmx + 1, 0] += (1-alphaX)*(1-alphaY)
       
    #     np.clip (self.hm, 0, 1, out=self.hm)
        #return self.hm
    
   
    # def annotationToHighResHeatmap (self):
    #     """Converts a list of points (each a dict with 'x' and 'y' component) into 
    #      a heatmap with original image resolution using myGaussian. For every 
    #      strawberry, the Gaussian myGaussian (peak 1) centered at the 
    #      annotated strawberry point is added."""
    #     """group: 0 - nothing, 1 - fish, 2 - crustacea, 3- chaetognatha, 4 - unidentified_object, 5 - jellyfish
    #     bodyPart: 'front' or 'back'"""

    #     self.hm = np.zeros ((self.image.shape[0], self.image.shape[1], 1), dtype=np.float32)
    #     self.gaussian = helpers.gaussian(8,50)

    #     group_array = np.zeros(Globals.channels)
    #     if self.bodyPart=='front':
    #         group_array[self.group*2-1] = 1 
    #     elif self.bodyPart=='back':
    #         group_array[self.group*2] = 1 
    #     elif self.bodyPart=='both':
    #         print("annotation to high res heatmap: invalid bodyPart")
            
    #     for animal in self.gt:
    #         if np.array_equal(animal['group'], group_array):
    #             x = animal['position'][0]
    #             y = animal['position'][1]
    
    #             if 0<=x <self.hm.shape[1] and 0<=y<self.hm.shape[0]: 
    #                 self.addToHeatmap (self.gaussian, x-self.gaussian.shape[1]//2, y-self.gaussian.shape[0]//2)
    
    #     np.clip (self.hm, 0, 1, out=self.hm)    
  

    def addToHeatmap (self, block, x, y):
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
        hxlo = x
        hylo = y
        hxhi = x+bsx
        hyhi = y+bsy
        bxlo = 0
        bylo = 0
        bxhi = bsx
        byhi = bsy
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
    
    
    def showImageWithHeatmap (self, group=None, bodyPart=None, filename=None, exagerate=1):
        """Shows image, the annotation by a heatmap hm [0..1] and the groundTruth gt. 
         The hm.shape must be an integer fraction of the image shape. gt must 
         have be a list of dicts with 'x' and 'y' entries as in the dataset. 
         Both hm and gt can be None in which case they are skipped. 
         If filename is given, the plot is saved."""
         
        if group==None: group=self.group
        if bodyPart==None: bodyPart=self.bodyPart
        
        assert bodyPart == "front" or bodyPart == "back" or bodyPart == "both"
        assert group in range(Globals.NUM_GROUPS)
        
        # copy image (so the heatmap is not drawn on original)
        img = self.image.copy()
           
        # if a heatmap for another group or bodyPart is wished, calculate it
        if self.group != group or self.bodyPart != bodyPart:
            if bodyPart == 'both':
                self.calculateHeadTailHeatmap(group)
            else:
                self.group = group
                self.bodyPart = bodyPart
                self.annotationToHeatmap()
        
        if self.hm is not None:      
            factor = img.shape[0]//self.hm.shape[0]
    
            assert self.hm.shape[0]*factor==img.shape[0] and self.hm.shape[1]*factor==img.shape[1]
            assert len(self.hm.shape)==3
            
            hmResized = np.repeat (self.hm, factor, axis=0) # y
            hmResized = np.repeat (hmResized, factor, axis=1) #x
            hmResized = np.repeat (hmResized, 3, axis=2) # factor for RGB
            hmResized = np.clip (hmResized*2, 0, 1)
            
            # todo adapt abdunkel factor
            if img.dtype =="uint8":
                img = img + (128*exagerate*hmResized).astype(np.uint8)
            else:
                img = ((img+1)*64 + 128*exagerate*hmResized).astype(np.uint8)
        plt.imshow(img)
        
        
        #print(f"body part is {self.bodyPart}")
        if self.gt is not None:    
            
            group_array = np.zeros(Globals.channels)
            if self.bodyPart=='front':
                group_array[self.group*2-1] = 1 
            elif self.bodyPart=='back' or self.bodyPart=='both':
                group_array[self.group*2] = 1 
                
            
            if self.bodyPart=='both':
                
                group_array_front = np.copy(group_array)
                group_array_front[np.argwhere(group_array==1)-1] = 1
                group_array_front[np.argwhere(group_array==1)] = 0
                
                #print(f"group_array {group_array}\ngroup array front {group_array_front}")
                
                x_front = [animal['position'][0] for animal in self.gt if np.array_equal(animal['group'], group_array_front)] 
                y_front = [animal['position'][1] for animal in self.gt if np.array_equal(animal['group'], group_array_front)]
                
                x_back = [animal['position'][0] for animal in self.gt if np.array_equal(animal['group'], group_array)]
                y_back = [animal['position'][1] for animal in self.gt if np.array_equal(animal['group'], group_array)]

                #print(f"x front {x_front}\ny front {y_front}\nx back {x_back}\ny back {y_back}")

                plt.scatter(x_front, y_front, s=20, marker='o', c='r')
                plt.scatter(x_back, y_back, s=20, marker='x', c='b')
                #plt.legend(loc='upper left')
                #plt.show()
             
            else:
                #print("gt is not None")
                x = [animal['position'][0] for animal in self.gt if np.array_equal(animal['group'], group_array) ]
                y = [animal['position'][1] for animal in self.gt if np.array_equal(animal['group'], group_array)]
                
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
   
    
    def calculateHeadTailHeatmap(self, group=None):
        if group==None: group=self.group
        
        # init one heatmap for animal head and one for animal tail
        hm_front = []
        hm_back = []
        
        # calculate front heatmap
        self.group = group     
        self.bodyPart = 'front'
        self.annotationToHeatmap()
        hm_front = self.hm 

        # calculate back heatmap
        self.bodyPart = 'back'
        self.annotationToHeatmap()
        hm_back = self.hm 

        # combine both heatmaps by taking the average
        self.bodyPart = 'both'
        self.hm = (hm_front + hm_back)/2
        
        
    #def calculateAverageHeatmap(self, group):       
 

    def downsample (self, factor=32):
      """T must be a tensor with at least 3 dimension, where the last three are interpreted as height, width, channels.
         Downsamples the height and width dimension of T by the given factor. 
         The length in these dimensions must be a multiple of factor."""
      sh = self.hm.shape
      assert sh[-3]%factor==0
      assert sh[-2]%factor==0
      newSh = sh[:-3] + (sh[-3]//factor, factor) + (sh[-2]//factor, factor) + sh[-1:]
      self.hm = self.hm.reshape(newSh).mean(axis=(-4, -2))
