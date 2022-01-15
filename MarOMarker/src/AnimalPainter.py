from PyQt5 import QtCore, QtGui, QtWidgets
import math
import numpy as np
from functools import partial
from Animal import Animal, AnimalSpecificationsWidget
from Models import AnimalGroup, AnimalSpecies
from Helpers import getIcon, displayErrorMsg
import PhotoViewer
import ImageAreas 
    

class AnimalPainter(QtCore.QObject):
    """
    Class providing the logic for adding/removing/moving and jumping between 
    animals. It needs a QGraphicsView that it can paint on and that delegates 
    the mouse events to the AnimalPainter.
    
    Dragging implementation taken from
    https://stackoverflow.com/questions/60571837/how-to-move-a-figurecreated-using-paintevent-by-simply-draging-it-in-pyqt5
    (last access: 19.10.2020)
    
    Attributes
    -----------
    animal_list: list<Animal>
        A list of animals on the current image.
    drag_position_head : QPoint
    
    drag_position_tail : QPoint
    
    cur_animal : Animal
        Currently active animal.    
    imageArea : ImageArea
        A canvas to paint the object on and that provides mouse events to 
        the AnimalPainter.
    image_ending : string
        It is either '\*_L.jpg' or '\*_R.jpg'. Indicates if the left or right 
        image is currently being edited.
    original_img_width : int
        Width of the original image. Necessary for rescaling calculations.
    original_img_height : int
        Height of the original image. Necessary for rescaling calculations.
    propertyChanged : pyqtSignal
    animalSelectionChanged : pyqtSignal
    removeMatchBtnClicked : pyqtSignal
    animalPositionChanged : pyqtSignal
    """
    # define custom signals
    propertyChanged = QtCore.pyqtSignal(Animal)
    """ Signal emitted when the group, remark or species of an animal is changed. """
    
    animalSelectionChanged = QtCore.pyqtSignal()
    """ Signal emitted when animal selection changed. """
    
    removeMatchBtnClicked = QtCore.pyqtSignal(Animal)
    """ Signal emitted when a remove animal match button was clicked. """
    
    animalPositionChanged = QtCore.pyqtSignal()
    """ Signal emitted when a the position of an animal is changed by dragging. """
    
    def __init__(self, models, imageArea, parent=None):
        """
        Init function.

        Parameters
        ----------
        models : Models
            Contains all necessary data models, i.e. models for the animal 
            species, group, remark, as well as image remark and the general
            animal data from the result table.
        imageArea : ImageArea
            A QGraphicsView providing a photo to paint on and that passes the
            mouse events to AnimalPainter.
        """
        super(AnimalPainter, self).__init__(parent)
        
        # data models
        self.models = models
        
        # list with all animals on the current image
        self.animal_list = []
        
        # list of buttons and their corresponding animal to remove a match
        self.btns_remove_match = []
        
        # dragging offset when moving the markings for head and/or tail
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()
        
        # current animal
        self.cur_animal  = None
        self.widget_animal_specs = AnimalSpecificationsWidget(models, imageArea)
        
        # the QGraphicsView to paint on
        self.imageArea = imageArea
        
        # left or right image
        self.image_ending = "*_L.jpg"
        
        # original size of image (needed for resizing, i.e. recalculating 
        # coordinates)
        self.original_img_width = 0
        self.original_img_height = 0
        
        # function to update the bounding boxes
        self.updateBoundingBoxes = self.updateBoundingBoxesNormal
        
        # remember the group and species of the most recently adapted animal
        self._previous_group = "Unidentified"
        self._previous_species = AnimalSpecies.UNIDENTIFIED
        
        # variable to indicate if organism markings are visible
        self.are_markings_visible = True
        
        # setup shortcuts
        self.shortcut_deselect_animal = QtWidgets.QShortcut(
            QtGui.QKeySequence("Escape"), self.imageArea, self.deselectAnimal) 
        
    def makeAllMarkingsVisible(self, make_visible):
        """ Makes markings of all animals (in-)visible. This includes head, tail, line, bounding box and ID markings. """
        for animal in self.animal_list:
            if animal.boundingBox_visual: animal.boundingBox_visual.setVisible(make_visible)
            if animal.head_item_visual: animal.head_item_visual.setVisible(make_visible)
            if animal.tail_item_visual: animal.tail_item_visual.setVisible(make_visible)
            if animal.line_item_visual: animal.line_item_visual.setVisible(make_visible)
            if animal.id_visual: animal.id_visual.setVisible(make_visible)
            
        self.are_markings_visible = make_visible
    
    def setAnimalRemark(self, remark):
        """ Sets the remark of the currently active animal. """
        if self.cur_animal is not None:
            self.cur_animal.setRemark(remark)   
            
            self.propertyChanged.emit(self.cur_animal)  
    
    def setAnimalSpecies(self, species):
        """ Sets the species of the currently active animal. """
        if self.cur_animal is not None:
            self.cur_animal.setSpecies(species)
            self._previous_species = species
            
            self.propertyChanged.emit(self.cur_animal)  
            
    def setAnimalGroup(self, group):
        """ Sets the group of the currently active animal and adapts the 
        visuals accordingly. """
        if self.cur_animal is not None:
            self.cur_animal.setGroup(group) 
            
            # use this group for animals that are added after this animal
            self._previous_group = group
            
            # update drawing
            self.cur_animal.head_item_visual.setPixmap(self.cur_animal._pixmap_head)
            self.cur_animal.tail_item_visual.setPixmap(self.cur_animal._pixmap_tail)
            
            # redraw line and boundingbox visuals
            # if self.cur_animal.line_item_visual is not None:
            #     self.imageArea._scene.removeItem(self.cur_animal.line_item_visual)
            self.removeLineVisual(self.cur_animal)
            self.drawAnimalLine(self.cur_animal)
            
            # if self.cur_animal.boundingBox_visual is not None:
            #     self.imageArea._scene.removeItem(self.cur_animal.boundingBox_visual)
            self.removeBoundingBoxVisual(self.cur_animal)
            self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(
                self.cur_animal.boundingBox, 
                QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
            
            # redraw ID and 'remove match' button if match mode is active and the animal has a match
            # if isinstance(self.imageArea.parent().parent(), ImageAreas.ImageAreaLR):
            #     matchL = self.imageArea.parent().parent().findAnimalMatch(self.cur_animal, "L")
            #     matchR = self.imageArea.parent().parent().findAnimalMatch(self.cur_animal, "R")
            #     if matchL is None and matchR is None: return
                
            if hasattr(self.imageArea.parent().parent().parent().parent().parent(), "is_match_animal_active"):
                if self.imageArea.parent().parent().parent().parent().parent().is_match_animal_active:
                    if self.cur_animal.id_visual is not None:
                        self.imageArea._scene.removeItem(self.cur_animal.id_visual)
                    self.drawAnimalIdRemoveBtn(self.cur_animal)
            
            self.propertyChanged.emit(self.cur_animal)   
     
    def redraw(self):
        """ Redraws all animals on the current image. """
        # remove animals
        self.removeAll()
        
        # redraw animals
        for animal in self.animal_list:
            # update positions
            self.updateAnimalPosition(animal)
            
            # redraw animals
            self.drawAnimalHead(animal)
            self.drawAnimalTailLineBoundingBox(animal)
                    
        self.updateBoundingBoxes() 
    
    def removeAll(self, remove_from_list=False):
        """ Removes visuals of all animals and its storage in the list if 
        desired. """
        for animal in self.animal_list:
            self.removeAnimal(animal, remove_from_list)
          
    def removeAnimal(self, animal, remove_from_list=False):
        """ Removes given animal visually and from list. """
        self.removeHeadVisual(animal)
        self.removeTailVisual(animal)
        self.removeLineVisual(animal)
        self.removeBoundingBoxVisual(animal)
        self.removeIdVisual(animal)
        
        animal.is_head_drawn = False
        animal.is_tail_drawn = False
        
        if remove_from_list:
            self.animal_list.remove(animal)
     
    def placeSpecsWidget(self):
        """ Function to move the specs widget with the bounding box of the 
        current animal (and prevent it from getting out of the borders of 
        the image) """
        if self.cur_animal is not None:
            if self.cur_animal.boundingBox_visual is not None:
                # reset position of specs widget
                self.widget_animal_specs.move(0,0)

                # get position of current bounding box from scene
                pos = self.imageArea.mapFromScene(
                    self.cur_animal.boundingBox_visual.rect().bottomLeft().toPoint())
                
                # move the specs to the bottom left corner of the animal bounding box
                self.widget_animal_specs.move(pos)
                
                # specs widget in viewport coords
                specs_vp = self.imageArea.mapFromScene(QtCore.QRectF(self.widget_animal_specs.rect()))
                specs_width = (specs_vp.value(1) - specs_vp.value(0)).x() #self.widget_animal_specs.width()
                specs_height = (specs_vp.value(2) - specs_vp.value(1)).y() #self.widget_animal_specs.height()
                    
                # bounding box in viewport coordinates
                bb_vp = self.imageArea.mapFromScene(self.cur_animal.boundingBox_visual.rect())
                bb_width = (bb_vp.value(1) - bb_vp.value(0)).x() #self.cur_animal.boundingBox_visual.rect().width()
                bb_height = (bb_vp.value(2) - bb_vp.value(1)).y() #self.cur_animal.boundingBox_visual.rect().height()
                
                # 8 possible placements of specs that are checked one after the other
                # 1. specs below animal
                top_left = pos + QtCore.QPoint(0, 0)
                result, visibility_areas = self.checkVisibility(top_left, None)
                if result: return
                
                # 2. specs left of animal
                top_left = pos + QtCore.QPoint(-specs_width, -bb_height)
                result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
                if result: return
                
                # 3. specs above animal
                top_left = pos + QtCore.QPoint(0, -bb_height - specs_height)
                result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
                if result: return
                
                # 4. specs right of animal
                top_left = pos + QtCore.QPoint(bb_width, -bb_height)
                result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
                if result: return
    
                # 5. specs on top left corner
                top_left = pos + QtCore.QPoint(-specs_width, -bb_height - specs_height)
                result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
                if result: return
                           
                # 6. specs on top right corner
                top_left = pos + QtCore.QPoint(bb_width, -bb_height - specs_height)
                result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
                if result: return
                
                # 7. specs on bottom left corner
                top_left = pos + QtCore.QPoint(-specs_width, 0)
                result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
                if result: return
                
                # 8. specs on bottom right corner
                top_left = pos + QtCore.QPoint(bb_width, 0)
                result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
                if result: return
                
                # if none of the methods was chosen, check which yields most
                # visibility (i.e. maximum visible area) of the specs widget
                max_area_index = visibility_areas[:,0].argmax()
                top_left = visibility_areas[max_area_index, 1]
                self.widget_animal_specs.move(top_left)
               
    def checkVisibility(self, top_left, visibility_areas=None):
        """
        Checks which corners of the specs widget, i.e. a QRect specified by it's 
        top left corner position) are visible and how much area of the specs is 
        visible in the current image area.

        Parameters
        ----------
        top_left : QPoint
            Top left corner position of the animal specification widget.
        visibility_areas : np.array<int, QPoint>, optional
            List of top left corners specifying the specs widget, as well as the
            corresponding visible area. If given, the new position and area will 
            be stacked on this array. The default is None. 

        Returns
        -------
        bool
            Whether all 4 corners of the specs widget are visible.
        visibility_areas : np.array<int, QPoint>
            The area of the specs widget that is visible in the image area and 
            the top left corner of the specs widget specifying its position.
        """
        # determine which area of the specs is visible
        rect = QtCore.QRect(top_left, QtCore.QSize(self.widget_animal_specs.width(), self.widget_animal_specs.height()))
        intersection_rect = rect.intersected(self.imageArea.rect())
        area = intersection_rect.width()*intersection_rect.height()
        visibility_area = np.array([area, top_left])     
        
        # stack visibility areas if some are given
        if visibility_areas is None: 
            visibility_areas = visibility_area
        else:
            visibility_areas = np.vstack((visibility_areas, visibility_area))
        
        # check which and how many corners are visible for the given top left corner
        if self.checkVisibleCorners(top_left)[0] == 4: 
            self.widget_animal_specs.move(top_left)
            return True, visibility_areas
        
        return False, visibility_areas
            
    def checkVisibleCorners(self, top_left=None):
        """
        Checks which corners of the specs widget (specified by it's top left 
        corner) are visible on the image area.

        Parameters
        ----------
        top_left : QPoint, optional
            Top left corner position of the specs widget. If not given, its
            current position is assumed. The default is None.

        Returns
        -------
        count : int
            Number of visible corners.
        tl : bool
            Whether the top left corner is visible.
        tr : bool
            Whether the top right corner is visible.
        bl : bool
            Whether the bottom left corner is visible.
        br : bool
            Whether the bottom right corner is visible.
        """
        
        # if top left corner is not specified, get the coordinates from the 
        # specs widget in the scene
        if not top_left:
            # get corners of specs widget in scene coordinates
            top_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topLeft())).toPoint()
            top_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topRight())).toPoint()
            bottom_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomLeft())).toPoint()
            bottom_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomRight())).toPoint()
        else:
            # calculate positions of the corners given the top left one
            bottom_left = top_left + QtCore.QPoint(0, self.widget_animal_specs.height())
            top_right = top_left + QtCore.QPoint(self.widget_animal_specs.width(), self.widget_animal_specs.height())
            bottom_right = top_left + QtCore.QPoint(self.widget_animal_specs.width(), 0)
       
        # init return variables
        count = 0
        tl = False
        tr = False
        bl = False
        br = False
        
        # check which corners are visible
        if self.imageArea.rect().contains(top_left): 
            count = count +1
            tl = True
        if self.imageArea.rect().contains(top_right): 
            count = count +1
            tr = True
        if self.imageArea.rect().contains(bottom_left): 
            count = count +1
            bl = True
        if self.imageArea.rect().contains(bottom_right): 
            count = count +1
            br = True
        
        return count, tl, tr, bl, br
                 
    def updateBoundingBoxesNormal(self):
        """ Removes bounding box visuals for all animals and draws only the 
        one of the current animal. """
        # remove bounding of other animals
        for animal in self.animal_list:
            self.removeBoundingBoxVisual(animal)
            
            # set colour to full opacity
            animal.color.setAlpha(255)
            
            # remove ID
            self.removeIdVisual(animal)

        # draw the current animal bounding box
        if self.cur_animal is not None and self.cur_animal in self.animal_list:
            self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(
                self.cur_animal.boundingBox, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
            
            self.widget_animal_specs.setAnimal(self.cur_animal)
            self.placeSpecsWidget()
            self.widget_animal_specs.show()
        else:
            self.widget_animal_specs.hide()
    
    def updateBoundingBoxesMatchMode(self):
        """ Draws boundingg boxes as needed in the match mode (i.e. draws a 
        (more transparent) bounding box and an ID for every animal that has a 
        match). """
        
        # hide specs widget in the scene
        self.widget_animal_specs.hide()
    
        for animal in self.animal_list:
            # remove old bounding box from scene   
            self.removeBoundingBoxVisual(animal)

            # remove ID
            self.removeIdVisual(animal)
            
            # remove remove-match-btn visual
            self.removeRemoveBtnVisual(animal)
                           
            # only drawbounding boxes of animals that are annotated on both images
            if self.models.model_animals.data.loc[animal.row_index, "RX1"] != -1 \
            and self.models.model_animals.data.loc[animal.row_index, "LX1"] != -1:
                # current animal (that has a match)
                if animal == self.cur_animal:
                    # set colour to full opacity
                    animal.color.setAlpha(255)
                    
                    # draw the new bounding box
                    animal.boundingBox_visual = self.imageArea._scene.addRect(
                        animal.boundingBox, QtGui.QPen(animal.color, 5, QtCore.Qt.SolidLine))
                else:
                    # for all other animals with match, set a more transparent color
                    animal.color.setAlpha(70)
                         
                    # add new bounding box to scene
                    animal.boundingBox_visual = self.imageArea._scene.addRect(
                        animal.boundingBox, QtGui.QPen(animal.color, 5, QtCore.Qt.SolidLine))
                
                # only draw IDs for animals with a match
                self.drawAnimalIdRemoveBtn(animal) 
            
            # draw bounding box of current animal (without match) a bit thinner
            # than animals that have a match
            elif animal == self.cur_animal:
                # set colour to full opacity
                animal.color.setAlpha(255)
                
                # draw the new bounding box
                animal.boundingBox_visual = self.imageArea._scene.addRect(
                    animal.boundingBox, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))

    def drawAnimalIdRemoveBtn(self, animal):
        """ Draws the ID the of a given animal and a button to remove its
        match if the match mode is active. """
        if animal != None:
            self.drawAnimalId(animal)
            self.drawRemoveMatchBtn(animal)
        
    def drawRemoveMatchBtn(self, animal):
        """ Draws the button to remove a match on a given animal. """
        if animal is None:
            return
        elif animal.boundingBox_visual is None: 
            return
        
        # if button is already drawn, remove it before drawing a new button
        self.removeRemoveBtnVisual(animal)
        # for btn, ani in self.btns_remove_match:
        #     if animal == ani:
        #         if btn is not None:
        #             self.imageArea._scene.removeItem(btn)
        #             self.btns_remove_match.remove([btn, ani])
        
        # get animal color as string
        c = animal.color
        color = "(" + str(c.red()) + "," + str(c.green()) + "," + str(c.blue()) + ", 70)"
       
        # define button
        btn = QtWidgets.QPushButton(self.parent())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btn.sizePolicy().hasHeightForWidth())
        btn.setSizePolicy(sizePolicy)
        btn.setMinimumSize(QtCore.QSize(20, 20))
        btn.setMaximumSize(QtCore.QSize(20, 20))
        btn.setIcon(getIcon(":/icons/icons/x_white.png"))
        btn.setIconSize(QtCore.QSize(15, 15))
        btn.setObjectName("btn")
        btn.setStyleSheet("QPushButton{\n"
                        "    background-color:rgb"+ color +";\n"
                        "    outline:none;\n"
                        "    border: none; \n"
                        "    border-width: 0px;\n"
                        "    border-radius: 0px;\n"
                        "}\n"
                        "QPushButton:hover {\n"
                        "    background-color: rgb(0, 203, 221);\n"
                        "}\n"
                        "QPushButton:pressed {\n"
                        "    background-color: rgb(0, 160, 174);\n"
                        "}\n")

        # get top left corner of bounding box and move button there
        top_right = animal.boundingBox_visual.rect().topRight()   
        btn.move((top_right - QtCore.QPoint(20-2.5, 20+2.5)).toPoint())
        
        # add btn to scene and to list
        proxy = self.imageArea._scene.addWidget(btn)
        self.btns_remove_match.append([proxy, animal])
        
        # init action
        btn.clicked.connect(partial(self.remove_match, proxy))
     
    def removeAllRemoveMatchBtns(self):
        # remove old buttons from scene
        for btn, ani in self.btns_remove_match:
            if btn is not None:
                self.imageArea._scene.removeItem(btn)
            
        # clear list
        self.btns_remove_match = []
        
    def remove_match(self, button_proxy):
        """ Called when a remove match button is clicked. """
        #self.removeMatchBtnClicked.emit(animal)
        #print(f"remove match for btn {button_proxy}")
        animal = None
        for btn_proxy, ani in self.btns_remove_match:
            if button_proxy == btn_proxy:
                animal = ani
        if animal:
            img_spec = self.image_ending.lstrip("*_").rstrip(".jpg")        
            self.imageArea.parent().parent().on_remove_match_btn(img_spec, animal) 

    def drawAnimalId(self, animal):
        """ Draws the ID of a given animal. """
        # the animal ID is its row index in the data table
        animal_id = animal.row_index
        
        # get top left corner of bounding box
        top_left = animal.boundingBox_visual.rect().topLeft()
        
        # draw ID
        font = QtGui.QFont("Century Gothic", 12, QtGui.QFont.Bold) 
        
        # create text visual
        animal.id_visual = self.imageArea._scene.addSimpleText(str(animal_id), font)
        
        # draw the ID in the animal's colour (full opacity)
        animal.color.setAlpha(255)
        animal.id_visual.setBrush(animal.color)
        
        # draw a black outline around the ID for better visibility
        animal.id_visual.setPen(QtCore.Qt.black)
        
        # move the ID visual to the top left position of the bounding box
        animal.id_visual.setPos(top_left - QtCore.QPoint(0, 2*font.pointSize()))
        
    def drawAnimalHead(self, animal):
        """ Draws the head of a given animal. """
        if animal != None:
            if animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                self.imageArea._scene.addItem(animal.createHeadVisual())
     
    def drawAnimalLine(self, animal):
        """ Draws the line between head an tail of a given animal. """
        # set colour to full opacity
        animal.color.setAlpha(255)
        
        # draw line
        animal.line_item_visual = self.imageArea._scene.addLine(
            animal.line, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
     
    def drawAnimalTailLineBoundingBox(self, animal):
        """ Draws the tail of a given animal, the line betwen head and tail and 
        the bounding box around it. """
        if animal != None:
            if animal.position_tail != QtCore.QPoint(-1,-1):
                # draw the tail visual
                self.imageArea._scene.addItem(animal.createTailVisual())
                
                # draw line and boundingbox visuals
                self.drawAnimalLine(animal)
                animal.boundingBox_visual = self.imageArea._scene.addRect(
                    animal.boundingBox, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
                
    def removeHeadVisual(self, animal):
        """ Removes the head visual on the image of a given animal. """
        if animal.head_item_visual is not None:
            self.imageArea._scene.removeItem(animal.head_item_visual)
        animal.head_item_visual = None  

    def removeTailVisual(self, animal):
        """ Removes the tail visual on the image of a given animal. """
        if animal.tail_item_visual is not None:
            self.imageArea._scene.removeItem(animal.tail_item_visual)
        animal.tail_item_visual = None  
    
    def removeLineVisual(self, animal):
        """ Removes the line visual on the image of a given animal. """
        if animal.line_item_visual is not None:
            self.imageArea._scene.removeItem(animal.line_item_visual)
        animal.line_item_visual = None  

    def removeBoundingBoxVisual(self, animal):
        """ Removes the bounding box visual on the image of a given animal. """
        if animal.boundingBox_visual is not None:
            self.imageArea._scene.removeItem(animal.boundingBox_visual)
        animal.boundingBox_visual = None  
      
    def removeIdVisual(self, animal):
        """ Removes the ID visual on the image of a given animal. """
        if animal.id_visual is not None:
            self.imageArea._scene.removeItem(animal.id_visual)
        animal.id_visual = None
        
    def removeRemoveBtnVisual(self, animal):
        """ Removes the remove-match-button of a given animal. """
        # if button is already drawn, remove it before drawing a new button
        for btn, ani in self.btns_remove_match:
            if animal == ani:
                if btn is not None:
                    self.imageArea._scene.removeItem(btn)
                    self.btns_remove_match.remove([btn, ani])        
                
    def on_next_animal(self):
        """ Makes the next animal in the animal_list active. """
        # if no animal ist selected, then select first one
        if self.cur_animal is None and len(self.animal_list) > 0:
            self.cur_animal = self.animal_list[0]          
                    
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in self.animal_list:
            index = self.animal_list.index(self.cur_animal)
    
            # only go to next animal if there is another one
            if index < len(self.animal_list)-1:
                self.cur_animal = self.animal_list[index+1]
            else:
                # else, go to first animal
                self.cur_animal = self.animal_list[0]
                
            self.updateBoundingBoxes()
                   
    def on_previous_animal(self):
        """ Makes the previous animal in the animal_list active. """
        # if no animal is selected, then select last one
        if self.cur_animal is None and len(self.animal_list) > 0:
            self.cur_animal = self.animal_list[-1] 
            
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in self.animal_list:
            index = self.animal_list.index(self.cur_animal)
            
            # only go to previous animal, if there is one
            if index > 0:
                self.cur_animal = self.animal_list[index-1]
            else:
                # else, go to last animal
                self.cur_animal = self.animal_list[len(self.animal_list)-1]
            
            self.updateBoundingBoxes()   

    def on_match_animal(self, activate_match, is_add_active, is_remove_active):
        """ Handles the activation state of the match mode. 

        Parameters
        ----------
        activate_match : bool
            Whether to activate the remove mode or deactivate it.
        is_add_active : bool
            Whether the add mode is active or not.
        is_remove_active : bool
            Whether the remove mode is active or not.

        Returns
        -------
        is_match_activatable : bool
            Whether it is possible to activate the match mode.
        is_add_active : bool
            Wheter the add mode needs to be active or not.
        is_remove_active : bool
            Whether the remove mode needs to be active or not.
        """ 
        if not activate_match:
            return False, is_add_active, is_remove_active  
        elif is_add_active:
            # only deactivate add mode is animal is drawn completely
            if not self.cur_animal \
            or (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                return True, False, False
            else:
                displayErrorMsg("Error", 
                                "Please draw head and tail before switching off the Add-mode.", 
                                "Error")     
                return False, True, False
        else:
            return True, False, False    
        
    def on_remove_animal(self, activate_remove, is_add_active, is_match_active):
        """ Handles the activation state of the remove mode. 

        Parameters
        ----------
        activate_remove : bool
            Whether to activate the remove mode or deactivate it.
        is_add_active : bool
            Whether the add mode is active or not.
        is_match_active : bool
            Whether the remove mode is active or not.

        Returns
        -------
        is_remove_activatable : bool
            Whether it is possible to activate the remove mode.
        is_add_active : bool
            Wheter the add mode needs to be active or not.
        is_match_active : bool
            Whether the remove mode is active or not.
        """ 
        if not activate_remove:
            return False, is_add_active, is_match_active  
        elif is_add_active:
            # only deactivate add mode is animal is drawn completely
            if not self.cur_animal \
            or (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                return True, False, False
            else:
                displayErrorMsg("Error", 
                                "Please draw head and tail before switching off the Add-mode.", 
                                "Error")    
                return False, True, False
        else:
            return True, False, False    

    def on_add_animal(self, activate_add, is_remove_active, is_match_active): 
        """ Handles the activation state of the add mode. 
        
        Parameters
        ----------
        activate_add : bool
            Whether to activate the add mode or deactivate it.
        is_remove_active : bool
            Whether the remove mode is active or not.
        is_match_active : bool
            Whether the remove mode is active or not.

        Returns
        -------
        is_add_activatable : bool
            Whether it is possible to activate the add mode.
        is_remove_active : bool
            Whether the remove mode needs to be active or not.
        is_match_active : bool
            Whether the match mode needs to be active or not.
        """
        # if add mode is to be turned off
        if not activate_add:
            # the add mode can only be deactivated when head and tail are drawn 
            # or none of them is drawn (i.e. cur_animal is None)
            if self.cur_animal is not None:
                if (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn) \
                    or (not self.cur_animal.is_head_drawn and not self.cur_animal.is_tail_drawn):
                        return False, is_remove_active, is_match_active
                else:
                    displayErrorMsg("Error", 
                                    "Please draw head and tail before switching off the Add-mode.", 
                                    "Error")
                    return True, False, False
            else:
                return False, is_remove_active, is_match_active
        else:
            # turn on add mode
            return True, False, False
            
    def deselectAnimal(self):
        """ Deselects the current animal. """
        self.cur_animal = None
        self.updateBoundingBoxes()  
        
    def redrawAnimal(self, animal):
        """ Redraws the given animal. """
        # remove visuals of the animal
        self.removeAnimal(animal, False)
        
        # redraw visuals of animal
        self.drawAnimalHead(animal)
        self.drawAnimalTailLineBoundingBox(animal)
        
    def mousePressEvent(self, event):
        """ Handles the painting options on the image: Enables dragging of
        head/tail visuals, as well as removing/adding animals on click. """
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        # find photo viewer parent
        if isinstance(self.imageArea.parent().parent(), PhotoViewer.PhotoViewer):
            parent = self.imageArea.parent().parent()
        elif isinstance(self.imageArea.parent().parent().parent().parent(), PhotoViewer.PhotoViewer):
            parent = self.imageArea.parent().parent().parent().parent()
        else:
            print("AnimalPainter: Could not find PhotoViewer parent.")
            return
        
        # check if user can draw an animal (not possible, when user drew an animal head on other image)
        is_animal_addable = parent.imageAreaLR.isAnimalAddable(self.image_ending)
        
        # get states of add and remove modes from home page
        is_add_mode_active = parent.parent().is_add_animal_active
        is_remove_mode_active = parent.parent().is_remove_animal_active
        
        # enable dragging for current animal (when add mode is not active and 
        # the current animal is completey drawn)
        if self.cur_animal is not None and not is_add_mode_active:
            if(self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                if (2 * QtGui.QVector2D(pos - self.cur_animal.rect_head.center()).length()
                    < self.cur_animal.rect_head.width()):
                    self.drag_position_head = pos - self.cur_animal.position_head
                
                if(self.cur_animal.rect_tail.contains(pos)):
                    self.drag_position_tail = pos - self.cur_animal.position_tail
         
        if(is_remove_mode_active):
            # remove mode
            for animal in self.animal_list:
                if(animal.boundingBox.contains(pos)):
                    # get index of animal in list
                    index = self.animal_list.index(animal)
                         
                    # if the current animal is to be removed
                    if(animal == self.cur_animal):
                        # if the index is not the last one, set the next animal as current animal
                        if index != len(self.animal_list)-1:
                            self.cur_animal = self.animal_list[index+1]
                        elif index == len(self.animal_list)-1 and len(self.animal_list)>1:
                            self.cur_animal = self.animal_list[index-1]
                        else:
                            self.cur_animal = None
                            
                    # remove animal visuals from scene and from animal list
                    self.removeAnimal(animal, True)
                                        
                    # if the animal has left and right coordinates, only 
                    # delete coordinates of the current image (left OR right)
                    if self.models.model_animals.data.loc[animal.row_index, "RX1"] != -1 and \
                        self.models.model_animals.data.loc[animal.row_index, "LX1"] != -1:
   
                        if self.image_ending == "*_L.jpg":
                            self.models.model_animals.data.loc[animal.row_index, "LX1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "LY1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "LX2"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "LY2"] = -1 
                            if isinstance(self.imageArea.parent().parent(), ImageAreas.ImageAreaLR):
                                match = self.imageArea.parent().parent().findAnimalMatch(animal, "L")
                            
                        elif self.image_ending == "*_R.jpg":
                            self.models.model_animals.data.loc[animal.row_index, "RX1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "RY1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "RX2"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "RY2"] = -1
                            if isinstance(self.imageArea.parent().parent(), ImageAreas.ImageAreaLR):
                                match = self.imageArea.parent().parent().findAnimalMatch(animal, "R")
                        
                        # reset length of matching animal
                        if isinstance(self.imageArea.parent().parent(), ImageAreas.ImageAreaLR):
                            match.setLength(0)
                            # update the visuals of the matching animal too
                            self.imageArea.parent().parent().redrawSelection()
                            
                        self.models.model_animals.data.loc[animal.row_index, "length"] = -1 
                           
                    else:  
                        # if animal has only left OR right coordinates, remove
                        # complete data row
                        pos = self.models.model_animals.data.index.get_loc(animal.row_index)
                        self.models.model_animals.removeRows(pos, 1, QtCore.QModelIndex())                        
                    break

        # if user is not removing and not adding animals, switch the current 
        # animal to what the user clicks on
        # if the user clicks on no organism, there is no current animal
        elif(not is_remove_mode_active and not is_add_mode_active):
            is_click_on_animal = False 
            for animal in self.animal_list:
                if(animal.boundingBox.contains(pos)):
                    self.cur_animal = animal
                    is_click_on_animal = True
                    break
            
            if not is_click_on_animal: self.cur_animal = None
            
            self.animalSelectionChanged.emit()
                            
        elif(is_add_mode_active):
            if not is_animal_addable: 
                text = "Error: Animal not addable."
                information = "Please complete the animal on the other image before adding an animal here."
                title = "Animal not addable"
                displayErrorMsg(text, information, title)
                return 
            
            # calculate click position in original format
            original_x = round(pos.x()*self.original_img_width/self.imageArea.width())
            original_y = round(pos.y()*self.original_img_height/self.imageArea.height())
            
            # add mode
            if self.cur_animal:
                if(self.cur_animal.is_head_drawn and not self.cur_animal.is_tail_drawn):
                    # adapt the tail position of the current animal
                    self.cur_animal.setPositionTail(pos)
                    self.cur_animal.original_pos_tail = QtCore.QPoint(original_x, original_y)
                    
                    # do the actual drawing
                    self.drawAnimalTailLineBoundingBox(self.cur_animal)
                    
                    # add animal to list
                    self.animal_list.append(self.cur_animal)
                    
                    cur_image_path = parent.image_list[0][parent.cur_image_index]
                    image_remark = parent.parent().comboBox_imgRemark.currentText()
                    experiment_id = parent.parent().parent().parent().page_data.lineEdit_exp_id.text()
                    user_id = parent.parent().parent().parent().page_settings.lineEdit_user_id.text()
                    
                    # add new data row and use coordinates of the animal as left
                    # or right image coordinates (depending on image_spec)
                    if self.image_ending == "*_R.jpg":
                        image_spec = "R"
                    else: 
                        image_spec = "L"
                    
                    self.models.model_animals.insertRows(
                    int(self.cur_animal.row_index), int(1), 
                    [self.cur_animal], cur_image_path, 
                    image_remark, experiment_id, user_id, [image_spec])
                    
                    # reactivate esc shortcut after tail is drawn
                    #parent.setEscShortcutActive(True)
                    self.shortcut_deselect_animal.setEnabled(True)
                                       
                else:                    
                    # create a new animal
                    idx = self.models.model_animals.data.index.max()
                    if math.isnan(idx): idx = 0
                
                    self.cur_animal = Animal(self.models, 
                                             row_index=idx+1,
                                             position_head=pos)
                    
                    self.cur_animal.setGroup(self._previous_group)
                    self.cur_animal.setSpecies(self._previous_species)
                              
                    # calculate position in original format
                    self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                    
                    # do the actual drawing of the head
                    self.drawAnimalHead(self.cur_animal)
                    
                    # deactivate esc shortcut to prevent creation of incomplete animals
                    self.shortcut_deselect_animal.setEnabled(False)
                    
                     # since a new animal is selected, emit signal
                    self.animalSelectionChanged.emit() 
            else:                
                # create a new animal
                idx = self.models.model_animals.data.index.max()
                if math.isnan(idx): idx = 0
                
                self.cur_animal = Animal(self.models, 
                                         row_index=idx+1,
                                         position_head=pos)
                
                self.cur_animal.setGroup(self._previous_group)
                self.cur_animal.setSpecies(self._previous_species)
                
                # calculate position in original format
                self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                
                # do the actual drawing of the head
                self.drawAnimalHead(self.cur_animal)
                
                # since a new animal is selected, emit signal
                self.animalSelectionChanged.emit() 

        self.updateBoundingBoxes()                

    def mouseMoveEvent(self, event):
        """ When moving the mouse, adapt head/tail visual position when they
        are dragged. """
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        # if there is a head to draw and if the drag_position is within the widget, move the head
        if not self.drag_position_head.isNull() \
            and self.imageArea.rect().contains(pos) \
            and self.cur_animal is not None:         
            self.cur_animal.setPositionHead(pos - self.drag_position_head)
            # remove head on old position and draw it on the new position
            self.removeHeadVisual(self.cur_animal)
            self.removeLineVisual(self.cur_animal)
            self.drawAnimalHead(self.cur_animal)
            self.drawAnimalLine(self.cur_animal)
            
            self.updateOriginalAnimalPosition(self.cur_animal)
            
            self.updateBoundingBoxes()            
            self.cur_animal.setManuallyCorrected(True)
            
            self.animalPositionChanged.emit()

        # if there is a tail to draw and if the drag_position is within the widget, move the tail
        if not self.drag_position_tail.isNull() \
            and self.imageArea.rect().contains(pos) \
            and self.cur_animal is not None:
            self.cur_animal.setPositionTail(pos - self.drag_position_tail)
            
            # remove tail and line on old position and draw it on the new position
            self.removeTailVisual(self.cur_animal)
            self.removeLineVisual(self.cur_animal)  
            self.removeBoundingBoxVisual(self.cur_animal)
            self.drawAnimalTailLineBoundingBox(self.cur_animal)

            self.updateOriginalAnimalPosition(self.cur_animal)

            self.updateBoundingBoxes()            
            self.cur_animal.setManuallyCorrected(True)
            
            self.animalPositionChanged.emit()

    def mouseReleaseEvent(self, event):
        """ When releasing the mouse, reset the drag positions. """
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()

    def setOriginalWidthHeight(self, width=None, height=None):
        """
        Function to set the width and/or height of the original image used for
        coordinate transformations on animals.

        Parameters
        ----------
        width : int, optional
            Width of the original image in pixels. The default is None.
        height : int, optional
            Height of the original image in pixels. The default is None.
        """
        if width:
            self.original_img_width = width
        if height:
            self.original_img_height = height

    def updateAnimalPosition(self, animal):
        """ Recalculates the position of a given animal using its position on 
        the original image and the current size of the displayed image. """
        pos_h = QtCore.QPoint(-1, -1)
        pos_t = QtCore.QPoint(-1, -1)

        # transform coordinates of head and tail from original image to scene cooridnates
        pos_h.setX(round(animal.original_pos_head.x()*self.imageArea.width()/self.original_img_width))
        pos_h.setY(round(animal.original_pos_head.y()*self.imageArea.height()/self.original_img_height))
        
        pos_t.setX(round(animal.original_pos_tail.x()*self.imageArea.width()/self.original_img_width))
        pos_t.setY(round(animal.original_pos_tail.y()*self.imageArea.height()/self.original_img_height))
        
        animal.setPositionHead(pos_h)
        animal.setPositionTail(pos_t)
        
    def updateOriginalAnimalPosition(self, animal):
        """ Calculates the position of a given animal on the original image by 
        transforming its position on the currently displayed image. """
        if animal is not None:
            pos_oh = QtCore.QPoint(-1, -1)
            pos_ot = QtCore.QPoint(-1, -1)
    
            # transform coordinates of head and tail from current image to original image coordinates
            pos_oh.setX(round(animal.position_head.x()*self.original_img_width/self.imageArea.width()))
            pos_oh.setY(round(animal.position_head.y()*self.original_img_height/self.imageArea.height()))
            
            pos_ot.setX(round(animal.position_tail.x()*self.original_img_width/self.imageArea.width()))
            pos_ot.setY(round(animal.position_tail.y()*self.original_img_height/self.imageArea.height()))
            
            animal.original_pos_head = pos_oh
            animal.original_pos_tail = pos_ot
            
            end = "L"
            if self.image_ending == "*_R.jpg": end = "R"
            
            # update data model
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"X1"] = self.cur_animal.original_pos_head.x()
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"Y1"] = self.cur_animal.original_pos_head.y()
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"X2"] = self.cur_animal.original_pos_tail.x()
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"Y2"] = self.cur_animal.original_pos_tail.y()

    def drawAnimalsFromList(self, animal_list):
        """
        Draws animals from a dataframe on the current image. 

        Parameters
        ----------
        animal_list : DataFrame
            The list of animals to draw. Necessary columns: 
            LX1, LY1 (head position on left image), 
            LX2, LY2 (tail position on left image), 
            RX1, RY1 (head position on right image), 
            RX2, RY2 (tail position on right image),
            group, species, object_remarks
        """                
        for i in range(len(animal_list)):  
            # get the head and tail position form the list
            if self.image_ending=="*_L.jpg":
                original_pos_h = QtCore.QPointF(float(animal_list["LX1"].iloc[i]), float(animal_list["LY1"].iloc[i]))
                original_pos_t = QtCore.QPointF(float(animal_list["LX2"].iloc[i]), float(animal_list["LY2"].iloc[i]))
            elif self.image_ending == "*_R.jpg":
                original_pos_h = QtCore.QPointF(float(animal_list["RX1"].iloc[i]), float(animal_list["RY1"].iloc[i]))
                original_pos_t = QtCore.QPointF(float(animal_list["RX2"].iloc[i]), float(animal_list["RY2"].iloc[i]))   
            else:
                print("AnimalPainter: Error - no such image ending!")

            # only add an animal if there is a value for the coordinates
            if original_pos_h != QtCore.QPointF(-1, -1) and original_pos_t != QtCore.QPointF(-1, -1):
                # transform coordinates from original image to scene cooridnates
                pos_h = QtCore.QPointF(-1,-1)
                pos_h.setX(round(original_pos_h.x()*self.imageArea.width()/self.original_img_width))
                pos_h.setY(round(original_pos_h.y()*self.imageArea.height()/self.original_img_height))
                
                pos_t = QtCore.QPointF(-1,-1)
                pos_t.setX(round(original_pos_t.x()*self.imageArea.width()/self.original_img_width))
                pos_t.setY(round(original_pos_t.y()*self.imageArea.height()/self.original_img_height))
    
                animal_remark = str(animal_list["object_remarks"].iloc[i])
                if not animal_remark: animal_remark = ""       
        
                length = float(animal_list["length"].iloc[i])
                
                # create a new animal 
                animal = Animal(self.models,
                         row_index=animal_list.index[i],
                         position_head=pos_h, 
                         position_tail=pos_t,
                         group=str(animal_list["group"].iloc[i]),
                         species=str(animal_list["species"].iloc[i]),
                         remark=animal_remark,
                         length=length)
                
                # set the position in the original image     
                animal.original_pos_head = original_pos_h
                animal.original_pos_tail = original_pos_t
            
                # do the actual drawing of the head
                self.drawAnimalHead(animal)
                self.drawAnimalTailLineBoundingBox(animal)
                
                # append animal to list
                self.animal_list.append(animal)  
                
                # update bounding boxes
                self.updateBoundingBoxes()      
     
 