# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from Animal import AnimalSpecificationsWidget
from AnimalPainter import AnimalPainter
from Helpers import MismatchDialog
import PhotoViewer


class ImageArea(QtWidgets.QGraphicsView):
    """
    An implementation of QGraphicsView to enable painting of animals on a 
    photo as well as loading of photos. Moreover, it provides a 
    wheel zoom functionality.
    
    Attributes
    ----------
    _zoom : int
        Zoom level.
    _scene : QGraphicsScene
        The Scene for the QGraphicsView.
    _image : QGraphicsPixmapItem
        The image to display.
    _empty : bool
        Indicates if an image is currently displayed.
    animal_painter : AnimalPainter
        The painter to delegate the mouse events to.
    rightMouseButtonClicked: pyqtSignal
    """
    
    # custom signals
    rightMouseButtonClicked = QtCore.pyqtSignal(QtCore.QPoint)
    """ Signal emitted when the right mouse button is pressed. """
    
    def __init__(self, models, parent=None):
        super(ImageArea, self).__init__(parent)
        
        self._zoom = 0
        self._scene = QtWidgets.QGraphicsScene()
        self._image = QtWidgets.QGraphicsPixmapItem()
        self._empty = True
        self._scene.addItem(self._image)     
        self.setScene(self._scene)

        # set properties for graphics view
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        # animal painter to enable adding/removing of animals
        self.animal_painter = AnimalPainter(models, self)      
        
    def hasPhoto(self):
        """ Returns if there is a photo loaded or not. """
        return not self._empty

    def fitInView(self, scale=True):
        """ Responsible for proper image scaling. """
        rect = QtCore.QRectF(self._image.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                # viewrect = self.viewport().rect()
                # scenerect = self.transform().mapRect(rect)
                # factor = min(viewrect.width() / scenerect.width(),
                #               viewrect.height() / scenerect.height())
                # self.scale(factor, factor)   
            self._zoom = 0

    def setPhoto(self, pixmap=None):     
        """ Sets the current image corectly scaled to the screen. """ 
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self.setEnableInteraction(True)
            self._empty = False
            #self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._image.setPixmap(pixmap)
           
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._image.setPixmap(QtGui.QPixmap())
            self.setEnableInteraction(False)
        self.fitInView() 
        
    def setEnableInteraction(self, isInteractionEnabled):
        """ Enables/Disables if the image is manipulable. """
        self.setEnabled(isInteractionEnabled)
        
    def wheelEvent(self, event):
        """ Catches the mouse wheel event and zooms into the image accordingly. """
        if self.hasPhoto():  
            factor = 1
            
            # zoom in if y > 0 (wheel forward), else zoom out 
            # (maximum zoom level of 30)
            if event.angleDelta().y() > 0 and self._zoom <= 30:
                factor = 1.15
                self._zoom += 1
            elif event.angleDelta().y() <= 0:
                factor = 0.9
                self._zoom -= 1
        
            # find the photo viewer in the parent tree
            parent = None
            if isinstance(self.parent().parent().parent().parent(), PhotoViewer):
                parent = self.parent().parent().parent().parent()
            elif isinstance(self.parent().parent(), PhotoViewer):
                parent = self.parent().parent()
            else:
                print("ImageArea: Could not find PhotoViewer as parent and \
                      could therefore not (de-) activate arrow shortcuts.")
                print(self.parent())
                return
            
            # scale the view if zoom is positive, else set it to zero and fit 
            # the photo in the view
            if self._zoom > 0:
                self.scale(factor, factor)
                parent.setArrowShortcutsActive(False)
            elif self._zoom == 0:
                self.fitInView()
                parent.setArrowShortcutsActive(True)
            else:
                self._zoom = 0
                parent.setArrowShortcutsActive(True)
                    
    # delegate mouse events to animal painter
    def mousePressEvent(self, event):
        """ Passes the mouse press event to the animal_painter. """
        if event.button() == QtCore.Qt.LeftButton:
            self.animal_painter.mousePressEvent(event)  
        elif event.button() == QtCore.Qt.RightButton:
            self.rightMouseButtonClicked.emit(event.pos())
        super().mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        """ Passes the mouse move event to the animal_painter. """
        self.animal_painter.mouseMoveEvent(event)  
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """ Passes the mouse release event to the animal_painter. """
        self.animal_painter.mouseReleaseEvent(event)
        super().mouseReleaseEvent(event) 
                
    def enterEvent(self, event):
        """ Defines behaviour when cursor enters image area. """
        self.animal_painter.shortcut_deselect_animal.setEnabled(True)

        # tell imageAreaLR that this imageArea is active
        if isinstance(self.parent().parent(), ImageAreaLR): 
            self.parent().parent().last_active = self.animal_painter.image_ending
        
    def leaveEvent(self, event):
        """ Defines behaviour when cursor leaves image area. """
        self.animal_painter.shortcut_deselect_animal.setEnabled(False)



class ImageAreaLR(QtWidgets.QWidget):
    """
    A QWidget that handles the LR view, i.e. displays left and right images.
    
    Attributes
    ----------
    _models: Models
        Underlying data models containing the animal information.
    """
    def __init__(self, models, parent=None):
        super(ImageAreaLR, self).__init__(parent)
        
        self._models = models
        
        self._initUi()
        self._initActions()
        
        # if the left or  right image was lastly active (needed for iterating
        # through animals)
        self.last_active = "*_L.jpg"
        
        # indicates if match mode is active 
        self.is_match_mode_active = False
        
        # the currently selected animal that needs to be matched and on which 
        # image it is
        self.animal_to_match = [None, "L"]
        
        if parent:
            self.parent().setImageEnding("*_L.jpg", self.imageAreaL)
            self.parent().setImageEnding("*_R.jpg", self.imageAreaR)
    
    def on_right_mouse_click(self, image, click_position):
        """
        Initiates the process of removing a match when the right mouse 
        button is clicked and the match mode is active.

        Parameters
        ----------
        image : string
            Either 'L' or 'R'. Depicts on which image the click occured.
        click_position : QPoint
            Position where the click occured.

        Returns
        -------
        None.

        """
        if self.is_match_mode_active:
            if image == "L": 
                imageArea = self.imageAreaL
            else:
                imageArea = self.imageAreaR

            for animal in imageArea.animal_painter.animal_list:
                if animal.boundingBox.contains(click_position):
                    # find the match of the current animal
                    match = self.findAnimalMatch(animal, image)
                    
                    if match is not None:
                        # remove the match
                        if image == "L":
                            self.on_remove_match(animal, match)
                        elif image == "R":
                            self.on_remove_match(match, animal)

    def on_remove_match(self, animal_L, animal_R):
        """ Creates a separate data row for the right animal and removes the 
        right coordinates from the left animal. """
        # create data row for the right animal and update index
        self.createSeparateDataRow(animal_R, "R")   
        
        # remove right coordinates from left animal 
        self.match(animal_L, None)
        
        # reset current animals
        self.imageAreaL.animal_painter.cur_animal = None
        self.imageAreaR.animal_painter.cur_animal = None
        
        # redraw animals
        self.imageAreaL.animal_painter.updateBoundingBoxes()
        self.imageAreaR.animal_painter.updateBoundingBoxes()
        
        # remove cancel button, redraw cancel button when group changes
        for btn, ani in self.imageAreaL.animal_painter.btns_remove_match:
            if animal_L == ani:
                self.imageAreaL._scene.removeItem(btn)
                self.imageAreaL.animal_painter.btns_remove_match.remove([btn, ani])
                
        for btn, ani in self.imageAreaR.animal_painter.btns_remove_match:
            if animal_R == ani:
                self.imageAreaR._scene.removeItem(btn)
                self.imageAreaR.animal_painter.btns_remove_match.remove([btn, ani])
        
    def on_next_animal(self):
        """ Delegates the query to make next animal active to the lastly active
        image area (L or R). Also adapts the selection to have a matching pair 
        in both image areas active. """
        if self.last_active == "*_L.jpg":
            imageArea = self.imageAreaL
        elif self.last_active == "*_R.jpg":
            imageArea = self.imageAreaR
        
        # switch to next animal
        imageArea.animal_painter.on_next_animal()
        
        # update visuals on both image areas (so that both animals of a match
        # are selected
        self.redrawSelection()
    
    def on_previous_animal(self):
        """ Delegates the query to make next animal active to the lastly active
        image area (L or R). Also adapts the selection to have a matching pair 
        in both image areas active. """
        if self.last_active == "*_L.jpg":
            imageArea = self.imageAreaL
        elif self.last_active == "*_R.jpg":
            imageArea = self.imageAreaR
        
        # switch to next animal
        imageArea.animal_painter.on_previous_animal()
        
        # update visuals on both image areas (so that both animals of a match
        # are selected
        self.redrawSelection()
    
    def redrawSelection(self):   
        """ Finds the current animal (on the lastly active image area) and
        updates the bounding boxes of it and of its match on the right image. """
        if self.last_active == "*_L.jpg":
            imageArea = self.imageAreaL
            otherImageArea = self.imageAreaR
            image = "L"
        elif self.last_active == "*_R.jpg":
            imageArea = self.imageAreaR
            otherImageArea = self.imageAreaL
            image = "R"
            
        # find matching animal
        cur_animal = imageArea.animal_painter.cur_animal
        matching_animal = self.findAnimalMatch(cur_animal, image)
        imageArea.animal_painter.updateBoundingBoxes()  
        imageArea.animal_painter.placeSpecsWidget()
        
        # select matching animal and update bounding boxes
        otherImageArea.animal_painter.cur_animal = matching_animal
        otherImageArea.animal_painter.updateBoundingBoxes()  
        otherImageArea.animal_painter.placeSpecsWidget()  
        
        # update specs widget content
        self.updateSpecsWidget()
        
    def updateSpecsWidget(self):
        """ Updates the specs widget (on the side) with the currently active
        animal (either on left or right image). """
        # check if L or R view has an acitve current animal and update the specs widget
        if self.imageAreaL.animal_painter.cur_animal is not None:
            self.widget_animal_specs.setAnimal(self.imageAreaL.animal_painter.cur_animal)
        elif self.imageAreaR.animal_painter.cur_animal is not None:
            self.widget_animal_specs.setAnimal(self.imageAreaR.animal_painter.cur_animal)
        else:
            self.widget_animal_specs.setAnimal(None)
    
    def findAnimalMatch(self, animal, image="L"):
        """ Determines which animal object belongs to the given animal by 
        checking the data table and comparing head and tail coordinates.

        Parameters
        ----------
        animal : Animal
            Animal to find the match of.
        image : string
            Depicts whether the given animal is on the left ro right image.

        Returns
        -------
        matching_animal : Animal
            The matching animal. If none exists yet, None is returned.
        """
        if not animal: return
        
        if image == "R":
            coord = "L"
            imageArea = self.imageAreaL
        else:
            coord = "R"
            imageArea = self.imageAreaR
            
        # check if animal is in data model    
        if animal.row_index in self._models.model_animals.data.index:
            
            # check if animal has a match on right (left) image
            if self._models.model_animals.data.loc[animal.row_index, coord+'X1'] != -1:
                
                # get right (left) animal coordinates from data model
                position_head = QtCore.QPoint(
                    self._models.model_animals.data.loc[animal.row_index, coord+'X1'], 
                    self._models.model_animals.data.loc[animal.row_index, coord+'Y1'])
                position_tail = QtCore.QPoint(
                    self._models.model_animals.data.loc[animal.row_index, coord+'X2'], 
                    self._models.model_animals.data.loc[animal.row_index, coord+'Y2'])
                
                # check if any animal instance exists that has the same R (L) coordinates
                for matching_animal in imageArea.animal_painter.animal_list:
                    if matching_animal.original_pos_head == position_head  \
                    and matching_animal.original_pos_tail == position_tail:
                            return matching_animal
        return None
        
        
    def redrawLeftAnimal(self, animal):
        """ Given the right animal, redraw its matching left animal. """
        self.redrawAnimalMatch(animal, "R")
        
    def redrawRightAnimal(self, animal):
        """ Given the left animal, redraw its matching right animal. """
        self.redrawAnimalMatch(animal, "L")

    def redrawAnimalMatch(self, animal, image="L"):
        """
        Redraws the animal that is matched to the given animal (if existant). 

        Parameters
        ----------
        animal : Animal
            The animal whose counterpart is to be redrawn.
        image : string, optional
            Describes on which image the animal is located, i.e. on the right 
            ('R') or the left ('L') image. 
        """
        if image == "R":
            imageArea = self.imageAreaL
        else:
            imageArea = self.imageAreaR

        # find matching animal
        matching_animal = self.findAnimalMatch(animal, image)
        print(matching_animal)
        
        # if there is a matching animal, redraw it on the image area
        if matching_animal:
            print(matching_animal.group)
            # update properties of matching animal
            matching_animal.setGroup(animal.group)
            matching_animal.setSpecies(animal.species)
            matching_animal.setRemark(animal.remark)
            
            # remove matching animal visuals
            imageArea.animal_painter.removeAnimal(matching_animal, False)
            
            # redraw the visuals
            imageArea.animal_painter.drawAnimalHead(matching_animal)
            imageArea.animal_painter.drawAnimalTailLineBoundingBox(matching_animal)      
            imageArea.animal_painter.updateBoundingBoxes()     

        self.updateSpecsWidget()     
            
    def on_match_activated(self, is_active):
        """
        Changes bounding box style when match mode is activated.

        Parameters
        ----------
        is_active : bool
            State of the match mode.
        """   
        if is_active:
            # redraw the animals (make more transparent, add IDs to bounding boxes)
            self.imageAreaL.animal_painter.updateBoundingBoxes = self.imageAreaL.animal_painter.updateBoundingBoxesMatchMode
            self.imageAreaR.animal_painter.updateBoundingBoxes = self.imageAreaR.animal_painter.updateBoundingBoxesMatchMode
            
            # reset current animals
            self.imageAreaL.animal_painter.cur_animal = None
            self.imageAreaR.animal_painter.cur_animal = None
            
            self.is_match_mode_active = True
        else:
            self.imageAreaL.animal_painter.updateBoundingBoxes = self.imageAreaL.animal_painter.updateBoundingBoxesNormal
            self.imageAreaR.animal_painter.updateBoundingBoxes = self.imageAreaR.animal_painter.updateBoundingBoxesNormal
            
            # remove 'remove match' buttons
            self.imageAreaL.animal_painter.removeAllRemoveMatchBtns()
            self.imageAreaR.animal_painter.removeAllRemoveMatchBtns()
            
            self.is_match_mode_active = False
        
        # draw bounding boxes and IDs of all animals that have a match
        self.imageAreaL.animal_painter.updateBoundingBoxes()
        self.imageAreaR.animal_painter.updateBoundingBoxes() 
        
        # update specs widget  #@todo needed here?
        self.updateSpecsWidget()
        
    def _initUi(self):
        """ Defines and draws the UI elements. """
        # -- frame for the two images displayed below each other ------------ #
        layout_imageFrame = QtWidgets.QVBoxLayout(self)
        layout_imageFrame.setContentsMargins(0, 0, 0, 0)
        layout_imageFrame.setSpacing(0)
        layout_imageFrame.setObjectName("layout_imageFrame")
        
        self.imageAreaL = ImageArea(self._models, self)
        self.imageAreaR = ImageArea(self._models, self)
        
        spacer = QtWidgets.QSpacerItem(5, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)  
        
        layout_imageFrame.addWidget(self.imageAreaL)
        layout_imageFrame.addItem(spacer)
        layout_imageFrame.addWidget(self.imageAreaR)
        
        frame_image = QtWidgets.QFrame(self)
        frame_image.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_image.setLayout(layout_imageFrame)

        
        # -- frame for more options ----------------------------------------- #
        # layout for frame that should contain the specifications widget
        layout_specs = QtWidgets.QGridLayout(self)
        layout_specs.setObjectName("layout_specs")
        layout_specs.setAlignment(QtCore.Qt.AlignCenter)
        
        # frame to contain the specs widget
        frame_specs = QtWidgets.QFrame(self)
        frame_specs.setStyleSheet("QFrame{background-color:rgb(200, 200, 200);  border-radius: 3px; border: none;} ")
        frame_specs.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_specs.setLayout(layout_specs)
            
        # specification widget
        self.widget_animal_specs = AnimalSpecificationsWidget(self._models, self.imageAreaL)
        self.widget_animal_specs.setStyleSheet("QLabel{font:12pt 'Century Gothic'; color:black;} QComboBox QAbstractItemView {background-color:white;border:None;selection-background-color: rgb(0, 203, 221);}")
        self.widget_animal_specs.show()
        
        # add specs widget to specs layout
        layout_specs.addWidget(self.widget_animal_specs) 
        
        # layout for the options frame
        layout_options = QtWidgets.QVBoxLayout(self)
        layout_options.setContentsMargins(7, 7, 7, 7)
        layout_options.setSpacing(0)
        layout_options.setObjectName("layout_options")
        
        # spacer
        spacer1 = QtWidgets.QSpacerItem(5, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)  
        
        # add widgets to options frame
        layout_options.addWidget(frame_specs)
        layout_options.addItem(spacer1)
        
        # put options layout into a frame
        frame_options = QtWidgets.QFrame(self)
        frame_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_options.setLayout(layout_options)
        
        # main layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("layout")
        
        # adding widgets to main layout 
        self.layout.addWidget(frame_image)
        self.layout.addWidget(frame_options)
        
        # set main layout
        self.setLayout(self.layout)
    
    def updateDrawnAnimal(self, animal):
        """ Given the animal stored in the specs widget (on the side), this 
        function updates the corresponding animal on left and right image. """
        if self.imageAreaL.animal_painter.cur_animal is not None:
            painter = self.imageAreaL.animal_painter
            image = "L"
        elif self.imageAreaR.animal_painter.cur_animal is not None:
            painter = self.imageAreaR.animal_painter
            image = "R"
        else:
            return
        
        # update properties of current animal
        painter.cur_animal.setGroup(animal.group)
        painter.cur_animal.setSpecies(animal.species)
        painter.cur_animal.setRemark(animal.remark)
        
        # remove animal visuals
        painter.removeAnimal(painter.cur_animal, False)
        
        # redraw the visuals
        painter.drawAnimalHead(painter.cur_animal)
        painter.drawAnimalTailLineBoundingBox(painter.cur_animal)      
        painter.updateBoundingBoxes() 
        
        # redraw matching animal
        self.redrawAnimalMatch(painter.cur_animal, image)
    
    def handleMatching(self, image="L"):
        """ When the match mode is active, this function enables a different
        clicking strategy, i.e. 1st click selects animal, 2nd click matches
        the animal. 
        
        Parameters
        ----------
        image : string
            Either 'L' or 'R'. Depicts on which image the selection occured.
        """
        # find parent home page
        if hasattr(self.parent().parent().parent(), "is_match_animal_active"):
            parent = self.parent().parent().parent()
        else:
            return
        
        # check if the match mode is active
        if parent.is_match_animal_active:
            # check on which image area the selected animal is located
            if image == "L":
                imageArea = self.imageAreaL
            else:
                imageArea = self.imageAreaR
             
            # determine selected animal
            animal = imageArea.animal_painter.cur_animal
            
            # check if there has already been one animal selected and waits for its match
            if self.animal_to_match[0] is None:           
                # set animal to match
                self.animal_to_match = [animal, image]

            else:
                # an animal waits for its match
                # if the new selection occured on the same image as the 
                # waiting match, the new selection will be waiting for a match now
                if image == self.animal_to_match[1]:
                    self.animal_to_match = [animal, image]
                    self.imageAreaL.animal_painter.updateBoundingBoxes()
                    self.imageAreaR.animal_painter.updateBoundingBoxes()
                    return
                
                # match the active and the lastly selected animal
                if animal is not None:
                    if image == "L":
                        match_successfull = self.matchAnimals(animal, self.animal_to_match[0])
                    elif image == "R":
                        match_successfull = self.matchAnimals(self.animal_to_match[0], animal) 
                    
                    # set the animal waiting to be matched to None 
                    self.animal_to_match[0] = None
                    
                    if not match_successfull:
                        self.imageAreaL.animal_painter.cur_animal = None
                        self.imageAreaR.animal_painter.cur_animal = None
                
                # update the visuals, i.e. IDs, bounding boxes on both images
                self.redrawSelection()
     
    def handleDifferentGroup(self, animal_L, animal_R):
        text = "You are about to match two animals that have a different group. \nWhich group do you want to keep?"
        dlg = MismatchDialog("Groups do not match", text, animal_L.group, animal_R.group, None, self)
        answer = dlg.exec_()
        
        if answer == -1:
            print("handling differnt group: return false")
            return False
        elif answer == 0:
            animal_R.setGroup(animal_L.group)
            self.imageAreaR.animal_painter.redrawAnimal(animal_R)
        elif answer == 1:
            animal_L.setGroup(animal_R.group)
            self.imageAreaL.animal_painter.redrawAnimal(animal_L)
            
        return True
        
    def handleDifferentSpecies(self, animal_L, animal_R):
        text = "You are about to match two animals that have a different species. \nWhich species do you want to keep?"
        dlg = MismatchDialog("Species do not match", text, animal_L.species, animal_R.species, None, self)
        answer = dlg.exec_()
        
        if answer == -1:
            return False
        elif answer == 0:
            animal_R.setSpecies(animal_L.species)
        elif answer == 1:
            animal_L.setSpecies(animal_R.species)
    
        return True
    
    def handleDifferentRemark(self, animal_L, animal_R):
        text = "You are about to match two animals that have different remarks. \nWhich remark do you want to keep?"
        dlg = MismatchDialog("Remarks do not match", text, animal_L.remark, animal_R.remark, "Merge remarks", self)
        answer = dlg.exec_()
        
        if answer == -1:
            return False
        elif answer == 0:
            animal_R.setRemark(animal_L.remark)
        elif answer == 1:
            animal_L.setRemark(animal_R.remark)
        elif answer == 2:
            animal_R.setRemark(animal_L.remark + ", " + animal_R.remark)
            animal_L.setRemark(animal_L.remark + ", " + animal_R.remark)
            
        return True
        
    def matchAnimals(self, animal_L, animal_R):
        # if group, species, remark, length, other props are different, then what?
        if str(animal_L.group) != str(animal_R.group):
            print(f"animals do not have the same group {animal_L.group, animal_R.group}")
            if not self.handleDifferentGroup(animal_L, animal_R): return False
                   
        if str(animal_L.species) != str(animal_R.species):
            print(f"animals do not have the same species {animal_L.species, animal_R.species}")
            if not self.handleDifferentSpecies(animal_L, animal_R): return False
            
        if str(animal_L.remark) != str(animal_R.remark):
            print(f"animals do not have the same remark {animal_L.remark, animal_R.remark}")
            if not self.handleDifferentRemark(animal_L, animal_R): return False
        
        # remove old matches - there are 4 cases (for this we need to adapt the data model and the animal instances)
        # left animal has no right coordinates, right animal has no left coordinates
        if self._models.model_animals.data.loc[animal_L.row_index, "RX1"] == -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] == -1:
            self.match(animal_L, animal_R)
        
        # left animal has right coordinates, right animal doesnt have left coordinates
        elif self._models.model_animals.data.loc[animal_L.row_index, "RX1"] != -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] == -1:
            # find old animal that represents curent right coordinates  
            cur_right_animal = self.findAnimalMatch(animal_L, "L")
            
            # create separate data row for olf right animal
            self.createSeparateDataRow(cur_right_animal, image="R")
            
            # replace right animal
            self.match(animal_L, animal_R)
            
        # left animal has no right coordinates, right animal has left coordinates
        elif self._models.model_animals.data.loc[animal_L.row_index, "RX1"] == -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] != -1:           
            # find old animal that represents curent left coordinates  
            cur_left_animal = self.findAnimalMatch(animal_R, "R")
            
            # create separate data row for old right animal
            self.createSeparateDataRow(cur_left_animal, image="L")
            
            # replace right animal
            self.match(animal_L, animal_R)
        
        # left animal has right coordinates, right animal has left coordinates
        elif self._models.model_animals.data.loc[animal_R.row_index, "RX1"] != -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] != -1:
            # find old animal that represents curent right coordinates  
            cur_right_animal = self.findAnimalMatch(animal_L, "L")
            cur_left_animal = self.findAnimalMatch(animal_R, "R")
            
             # create separate data rows for old left and right animal
            self.createSeparateDataRow(cur_right_animal, image="R")
            self.createSeparateDataRow(cur_left_animal, image="L")
            
            # replace animals
            self.match(animal_L, animal_R)
        
        # recalculate length of animals (this changes when different animals are matched)
        self.parent().parent().parent().parent().parent().page_data.onCalcLength()
        
        return True
    
    def createSeparateDataRow(self, animal, image="L"):  
        """
        Adds a row at the end of the data table for the given animal.

        Parameters
        ----------
        animal : Annimal
            The animal to create a data row for.
        image : string
            Either "L" or "R", depending on which image the animal is located. 
            The default is "L".
        """
        # get experiment settings
        image_path = self._models.model_animals.data.loc[animal.row_index, "file_id"] + "_R.jpg"  
        image_remark = self._models.model_animals.data.loc[animal.row_index, "image_remarks"]
        experiment_id = self._models.model_animals.data.loc[animal.row_index, "experiment_id"]
        user_id = self._models.model_animals.data.loc[animal.row_index, "user_id"]
        
        # add a data row for the animal
        animal.row_index = self._models.model_animals.data.index.max() + 1
        
        self._models.model_animals.insertRows(animal.row_index, int(1), 
                                              [animal], image_path, image_remark, 
                                              experiment_id, user_id, image)
        
        imageArea = self.imageAreaL if image=="L" else self.imageAreaR
        
        # remove the button to remove a match 
        for btn, ani in imageArea.animal_painter.btns_remove_match:
            if animal == ani:
                imageArea._scene.removeItem(btn)
                imageArea.animal_painter.btns_remove_match.remove([btn, ani])
                
    def match(self, animal_L, animal_R):
        """
        Adapting match information in the data table and updating the indeces
        of the given animals.

        Parameters
        ----------
        animal_L : Animal
            Animal on left image.
        animal_R : Animal
            Animal on right image.
        """

        if animal_L is not None:
            animal = animal_L
            match = animal_R
            image = "R" # adapt right coordinates
        elif animal_R is not None:
            animal = animal_R
            match = animal_L
            image = "L" # adapt left coordinates
        else:
            return
             
        # in case no match is given, set the coordinates to adapt to default (-1)
        if match is None:
            self._models.model_animals.data.loc[animal.row_index, image+"X1"] = -1
            self._models.model_animals.data.loc[animal.row_index, image+"Y1"] = -1
            self._models.model_animals.data.loc[animal.row_index, image+"X2"] = -1
            self._models.model_animals.data.loc[animal.row_index, image+"Y2"] = -1
        else:
            # merge the new animal coordinates to the original animal
            self._models.model_animals.data.loc[animal.row_index, image+"X1"] = self._models.model_animals.data.loc[match.row_index, image+"X1"]
            self._models.model_animals.data.loc[animal.row_index, image+"Y1"] = self._models.model_animals.data.loc[match.row_index, image+"Y1"]
            self._models.model_animals.data.loc[animal.row_index, image+"X2"] = self._models.model_animals.data.loc[match.row_index, image+"X2"]
            self._models.model_animals.data.loc[animal.row_index, image+"Y2"] = self._models.model_animals.data.loc[match.row_index, image+"Y2"]
    
            # remove new animal entry from data model
            pos = self._models.model_animals.data.index.get_loc(match.row_index)
            self._models.model_animals.removeRows(pos, 1, QtCore.QModelIndex())        
                  
            # update row index of new right animal 
            match.row_index = animal.row_index
        
    def _initActions(self):
        """ Defines the actions possible on the ImageAreaLR. """
        self.imageAreaL.animal_painter.propertyChanged.connect(self.redrawRightAnimal)
        self.imageAreaR.animal_painter.propertyChanged.connect(self.redrawLeftAnimal)
        
        self.imageAreaL.animal_painter.animalSelectionChanged.connect(self.redrawSelection)
        self.imageAreaR.animal_painter.animalSelectionChanged.connect(self.redrawSelection)
        
        self.widget_animal_specs.propertyChanged.connect(self.updateDrawnAnimal)
        
        self.imageAreaL.animal_painter.animalSelectionChanged.connect(partial(self.handleMatching, "L"))
        self.imageAreaR.animal_painter.animalSelectionChanged.connect(partial(self.handleMatching, "R"))
        
        self.imageAreaL.rightMouseButtonClicked.connect(partial(self.on_right_mouse_click, "L"))
        self.imageAreaR.rightMouseButtonClicked.connect(partial(self.on_right_mouse_click, "R"))
        
        self.imageAreaL.animal_painter.removeMatchBtnClicked.connect(partial(self.on_remove_match_btn, "L"))
        self.imageAreaR.animal_painter.removeMatchBtnClicked.connect(partial(self.on_remove_match_btn, "R"))
   
        
    def on_remove_match_btn(self, image, animal):
        print("on_remove_match_btn")
        match = self.findAnimalMatch(animal, image)
        #@todo when removing one animal match by btn, the matching cross is not deleted
        if image == "L":
            self.on_remove_match(animal, match)
        elif image == "R":
            self.on_remove_match(match, animal)
