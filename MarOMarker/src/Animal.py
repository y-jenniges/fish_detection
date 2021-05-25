from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from Models import AnimalGroup, AnimalSpecies
import Helpers

class Animal():
    """ 
    Class to represent an animal on an image. 
    
    Attributes
    ----------
    row_index : int
        The index of the row in the result table that this animal 
        represents.
    position_head : QPointF, optional
        The position of the animal head on the displayed image. It will be 
        the center for the head visual, i.e. an 'o'. 
    position_tail : QPointF
        The position of the animal tail on the displayed image. It will be 
        the center for the tail visual, i.e. a 'x'.
    group : string
        The group of the animal. Selectable from the Enum AnimalGroup.
    species : string
        The species of the animal.
    remark : string
        The remark to the animal.
    length: int, optional
        The length of the animal. 
    original_pos_head : QPointF
        The head position on the unscaled original image.
    original_pos_tail : QPointF
        The tail position on the unscaled original image.
    pixmap_width : int
        Width of the square pixmap for the head and tail visuals.         
    pos_visual_head : QPoint
        Position of the head visual.
    pos_visual_tail : QPoint
        Position of the tail visual.
    rect_head : QRect
        Geomatry of the head drawn by the head_item_visual
    rect_tail : QRect
        Geometry of the tail drawn by the tail_item_visual
    line : QLineF
        Geometry of the line drawn by the line_item_visual.        
    is_head_drawn  : bool
        Indicates if the head of the animal is already drawn.
    is_tail_drawn : bool
        Indicates if the tail of the animal is already drawn.
    boundingBox : QRectF
        Box surrdounding the animal and drawn when it becomes active.
    boundingBox_visual:
        Visual of the bounding box that can be drawn in the QGraphicsScene.
    head_item_visual
        Visual of the head that can be drawn in the QGraphicsScene.
    tail_item_visual
        Visual of the tail that can be drawn in the QGraphicsScene.
    line_item_visual 
        Visual of the line that can be drawn in the QGraphicsScene.
    id_visual
        Visual of the ID that can be drawn in the QGraphicsScene.
    manually_corrected: bool
        Indicates if the animal was manually adapted. 
    """

    # the input position refers to the center of the visual
    def __init__(self, models, 
                 row_index, 
                 position_head=QtCore.QPointF(-1,-1), 
                 position_tail=QtCore.QPointF(-1,-1), 
                 group=AnimalGroup.UNIDENTIFIED, 
                 species=AnimalSpecies.UNIDENTIFIED, 
                 remark="", 
                 length=-1):
        """
        Init function.

        Parameters
        ----------
        row_index : int
            The index of the row in the result table that this animal 
            represents.
        position_head : QPoint, optional
            The position of the animal head on the displayed image. It will be 
            the center for the head visual, i.e. an 'o'. The default is 
            QtCore.QPointF(-1,-1).
        position_tail : QPoint, optional
            The position of the animal tail on the displayed image. It will be 
            the center for the tail visual, i.e. a 'x'. The default is 
            QtCore.QPointF(-1,-1).
        group : string, optional
            The group of the animal. Selectable from the Enum AnimalGroup.
            The default is AnimalGroup.UNIDENTIFIED.
        species : string, optional
            The species of the animal.
            The default is AnimalSpecies.UNIDENTIFIED.
        remark : string, optional
            The remark to the animal. The default is "".
        length: int, optional
            The length of the animal. The default is -1.
        """
        # data models
        self._models = models
        
        # row in the table this animal corresponds to
        self.row_index = row_index
        
        # size of the head/tail visuals
        self.pixmap_width = 20
        self._pixmap_head = None
        self._pixmap_tail = None
        
        # store the position on the original (i.e. not resized) image
        self.original_pos_head = QtCore.QPointF(position_head)
        self.original_pos_tail = QtCore.QPointF(position_tail)
        
        # current position of head and tail on the image
        self.position_head = position_head
        self.position_tail = position_tail
        
        # group, species, remark and length of the animal
        self.setGroup(group)
        self.setSpecies(species)
        self.setRemark(remark)
        self.length = length if length > 0 else 0
        #self.height = height if height > 0 else 0
      
        # set the visual for the head, tail and line between them 
        self.pos_visual_head = QtCore.QPoint(int(position_head.x()), int(position_head.y())) - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)
        self.pos_visual_tail = QtCore.QPoint(int(position_tail.x()), int(position_tail.y())) - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)

        self.rect_head = QtCore.QRect(self.pos_visual_head, QtCore.QSize(
            self.pixmap_width, self.pixmap_width))
        self.rect_tail = QtCore.QRect(self.pos_visual_tail, QtCore.QSize(
            self.pixmap_width, self.pixmap_width))       
        self.line = QtCore.QLineF(self.position_head, self.position_tail)  

        # indicate if head/tail is already drawn
        self.is_head_drawn = False
        self.is_tail_drawn = False           
        
        # set the bounding box visual
        self.boundingBox = QtCore.QRectF()
        self.boundingBoxOffset = [50, 50]
        self.calculateBoundingBox()
        
        # the actual items for head, tail, line and boundingbox in the scene
        self.boundingBox_visual = None
        self.head_item_visual = None
        self.tail_item_visual = None
        self.line_item_visual = None
        self.id_visual = None
        
        # indicate if this animal was manually corrected
        self.manually_corrected = False
     
    def createHeadVisual(self):
        """
        Creates a pixmap item (showing a circle), that is drawable on a 
        QGraphicsScene for the animal head and sets its position to the animal 
        head position.

        Returns
        -------
        QGraphicsPixmapItem
            The visual of the animal head (a circle).
        """
        if self.position_head != QtCore.QPointF(-1,-1):
            # create the head visual
            self.head_item_visual = QtWidgets.QGraphicsPixmapItem( \
                self._pixmap_head)
            
            # set position of head visual
            self.head_item_visual.setPos(self.rect_head.center() \
                                         - QtCore.QPointF( \
                                             self.pixmap_width/4, 
                                             self.pixmap_width/4))
            self.head_item_visual.ItemIsMovable = True
        
            self.is_head_drawn = True
        return self.head_item_visual
     
    def createTailVisual(self):
        """
        Creates a pixmap item (showing a cross), that is drawable on a 
        QGraphicsScene for the animal tail and sets its position to the animal 
        tail position.

        Returns
        -------
        QGraphicsPixmapItem
            The visual of the animal tail (a cross).
        """
        if self.position_tail != QtCore.QPointF(-1,-1):
            # create the tail visual
            self.tail_item_visual = QtWidgets.QGraphicsPixmapItem( \
                self._pixmap_tail)
                
            # set position of tail visual
            self.tail_item_visual.setPos(self.rect_tail.center() \
                                         - QtCore.QPointF( \
                                             self.pixmap_width/4, 
                                             self.pixmap_width/4))
            self.tail_item_visual.ItemIsMovable = True
            
            self.is_tail_drawn = True
        return self.tail_item_visual
    
    def setManuallyCorrected(self, corrected=False):
        """
        Sets the manually-corrected parameter of the animal.

        Parameters
        ----------
        corrected : bool, optional
            New value. The default is False.
        """
        self._models.model_animals.data.loc[
            self.row_index, "manually_corrected"] = corrected
                    
    def getColorsAccordingToGroup(self):
        """
        Finds the colour for the animal according to its group and sets the 
        pixmaps for head and tail accordingly.
        """
        self.color = ""
        
        if self.group == AnimalGroup.UNIDENTIFIED \
        or self.group == "Unidentified" \
        or self.group.lower() == "animalgroup.unidentified":
        #or self.group == "AnimalGroup.UNIDENTIFIED":
            self._pixmap_head = QtGui.QPixmap(":/animal_markings/animal_markings/o_gray.png")        
            self._pixmap_tail = QtGui.QPixmap(":/animal_markings/animal_markings/x_gray.png")  
            self.color = QtGui.QColor(217, 217, 217)
              
        elif self.group == AnimalGroup.FISH or self.group == "Fish" \
        or self.group.lower() == "animalgroup.fish":
            self._pixmap_head = QtGui.QPixmap(":/animal_markings/animal_markings/o_blue.png")        
            self._pixmap_tail = QtGui.QPixmap(":/animal_markings/animal_markings/x_blue.png")  
            self.color = QtGui.QColor(0, 112, 192)
            
        elif self.group == AnimalGroup.CRUSTACEA or self.group == "Crustacea" \
        or self.group.lower() == "animalgroup.crustacea":
            self._pixmap_head = QtGui.QPixmap(":/animal_markings/animal_markings/o_red.png")        
            self._pixmap_tail = QtGui.QPixmap(":/animal_markings/animal_markings/x_red.png") 
            self.color = QtGui.QColor(255, 0, 0)
            
        elif self.group == AnimalGroup.CHAETOGNATHA \
        or self.group == "Chaetognatha" \
        or self.group.lower() == "animalgroup.chaetognatha":
            self._pixmap_head = QtGui.QPixmap(":/animal_markings/animal_markings/o_orange.png")        
            self._pixmap_tail = QtGui.QPixmap(":/animal_markings/animal_markings/x_orange.png")  
            self.color = QtGui.QColor(255, 192, 0)
            
        elif self.group == AnimalGroup.JELLYFISH or self.group == "Jellyfish" \
        or self.group.lower() == "animalgroup.jellyfish":
            self._pixmap_head = QtGui.QPixmap(":/animal_markings/animal_markings/o_black.png")        
            self._pixmap_tail = QtGui.QPixmap(":/animal_markings/animal_markings/x_black.png") 
            self.color = QtGui.QColor(0, 0, 0)
            
        else:
            print(f"Animal: Unknown animal group '{self.group, type(self.group)}'! Using unidentified colour.")
            self._pixmap_head = QtGui.QPixmap(":/animal_markings/animal_markings/o_gray.png")        
            self._pixmap_tail = QtGui.QPixmap(":/animal_markings/animal_markings/x_gray.png")  
            self.color = QtGui.QColor(217, 217, 217)
     
        # scale pixmaps
        self._pixmap_head = self._pixmap_head.scaled(QtCore.QSize(
            self.pixmap_width/2, self.pixmap_width/2))     
        self._pixmap_tail = self._pixmap_tail.scaled(QtCore.QSize(
            self.pixmap_width/2, self.pixmap_width/2))     
    
    def setPositionHead(self, pos):
        """
        Sets the head position, moves the displayed rect and adapts the line 
        connecting head and tail accordingly. Also, bounding boxes are updated.

        Parameters
        ----------
        pos : QPoint
            New animal head position.
        """
        self.position_head = pos
        self.rect_head.moveTopLeft(QtCore.QPoint(int(pos.x()), int(pos.y())) - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2))
        self.pos_visual_head = QtCore.QPoint(int(pos.x()), int(pos.y()))  - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)
        
        self.line.setP1(pos)
        self.calculateBoundingBox() 
    
    def setPositionTail(self, pos):
        """
        Sets the tail position, moves the displayed rect and adapts the line 
        connecting head and tail accordingly. Also, bounding boxes are updated.

        Parameters
        ----------
        pos : QPoint
            New animal tail position.
        """
        self.position_tail = pos
        self.rect_tail.moveTopLeft(QtCore.QPoint(int(pos.x()), int(pos.y())) - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2))
        self.pos_visual_tail = QtCore.QPoint(int(pos.x()), int(pos.y())) - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)
        
        self.line.setP2(pos)
        self.calculateBoundingBox()
        
    def setGroup(self, group):
        """
        Sets the animal group, adapts the colours and updates the model entry.

        Parameters
        ----------
        group : string or AnimalGroup
            New animal group.
        """       
        group = str(group)
        if isinstance(group, AnimalGroup):
            g = group.name.title()
        else:
            g = group.title()
            
        self.group = g
        self.getColorsAccordingToGroup()
        
        # adapt group in data model if there is an entry for this animal
        if self.row_index in self._models.model_animals.data.index:
            self._models.model_animals.data.loc[
                self.row_index, 'group'] = g
    
    def setSpecies(self, species):
        """
        Sets the animal species and updates the model entry.

        Parameters
        ----------
        species : string
            New animal species.
        """
        if isinstance(species, AnimalSpecies):
            s = species.name.title()
        elif species.lower() == "nan" or species == "":
            s = "Unidentified"
        else:
            s = species
          
        self.species = s 
        
        # adapt species in data model if there is an entry for this animal
        if self.row_index in self._models.model_animals.data.index:
            self._models.model_animals.data.loc[
                self.row_index, 'species'] = s
    
    def setRemark(self, remark):
        """
        Sets a remark for the animal and updates the model entry.

        Parameters
        ----------
        remark : string
            New animal remark.
        """
        self.remark = str(remark)
        
        # adapt remark in data model if there is an entry for this animal
        if self.row_index in self._models.model_animals.data.index:
            self._models.model_animals.data.loc[
                self.row_index, 'object_remarks'] = str(remark)
    
    def calculateBoundingBox(self):
        """ Calculates the bounding box of the animal. """
        pos_x = min(self.position_tail.x(), self.position_head.x()) \
            - self.boundingBoxOffset[0]/2 
        pos_y = min(self.position_tail.y(), self.position_head.y()) \
            - self.boundingBoxOffset[1]/2 
        size_x = abs(self.position_head.x() - self.position_tail.x()) \
            + self.boundingBoxOffset[0]
        size_y = abs(self.position_head.y() - self.position_tail.y()) \
            + self.boundingBoxOffset[1]
        
        # update the bounding box with the new parameters
        self.boundingBox.setTopLeft(QtCore.QPoint(pos_x, pos_y))
        self.boundingBox.setWidth(size_x)
        self.boundingBox.setHeight(size_y)
        
    def setLength(self, length):
        """
        Sets the length of the animal.

        Parameters
        ----------
        length : float
            Length of the animal.
        """
        self.length = float(length)


class AnimalSpecificationsWidget(QtWidgets.QWidget):
    """ A widget to provide all information about the current animal. 
    
    Attributes
    ----------
    propertyChanged : pyqtSignal
    """
    
    # custom signals
    propertyChanged = QtCore.pyqtSignal(Animal)
    """ Signal emitted when the group, species or remark is changed. """
    
    def __init__ (self, models, parent = None):
        """
        Init function.

        Parameters
        ----------
        models : Models
            Contains all necessary data models, i.e. models for the animal 
            species, group, remark, as well as image remark and the general
            animal data from the result table.
        parent : optional
            The default is None.
        """
        super(QtWidgets.QWidget, self).__init__(parent)
        # init empty animal
        self.animal = None
        
        self.models = models
        
        self._initUi()
        self._initActions()
        self._initModels()
       
        # set an empty animal as default
        self.setAnimal(self.animal)

        # setting visuals to initial values and hiding widget
        self.updateVisuals()
        self.hide()
        
        # set tab sequence
        self.setTabOrder(self.comboBox_group, self.comboBox_species)
        self.setTabOrder(self.comboBox_species, self.comboBox_remark)
        self.setTabOrder(self.comboBox_remark, self.spinBox_length)
        
    def _set_combobox_group_idx(self, idx):
        self.comboBox_group.setCurrentIndex(idx)
        
    def _initModels(self):
        """ Function to set the data models on class widgets. """
        self.comboBox_group.setModel(self.models.model_group)
        self.comboBox_species.setModel(self.models.model_species)
        self.comboBox_remark.setModel(self.models.model_animal_remarks)

    def onRemarkComboboxEdited(self):
        """
        Function called when animal remark is edited. 
        """
        text = self.comboBox_remark.currentText()
        
        # if the text is already present in a similar form, do not add it but only update the combobox index
        for i in range(self.models.model_animal_remarks.rowCount()):
            item = self.models.model_animal_remarks.item(i)
            item.setTextAlignment(QtCore.Qt.AlignRight)
            if item.text().lower() == text.lower():
                text = str(item.text())
  
        # if the text is not yet in the combobox, add it
        if len(self.models.model_animal_remarks.findItems(text)) == 0:
            # add a capitalized, right-aligned entry to model
            item = QtGui.QStandardItem(str(text))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.models.model_animal_remarks.appendRow(item)
            
        # set current combobox index to the new entry and switch focus
        self.comboBox_remark.setCurrentIndex(self.comboBox_remark.findText(str(text)))
        self.focusNextChild()
        
        # update animal object stored in the specs widget
        if self.animal is not None:
            self.animal.setRemark(str(text))
            
            # update the drawn animal
            self.propertyChanged.emit(self.animal)   

        # let animal painter know about change #@todo maybe make animal_painter react to propertyChanged 
        if hasattr(self.parent(), "animal_painter"):
            self.parent().animal_painter.setAnimalRemark(str(text))

    def onSpeciesComboboxChanged(self, species):
        """ Function called when the species combobox is changed. 
        It sets the species of the current animal. 

        Parameters
        ----------
        species : string
            The selected species of the animal. 
            Selectable from the Enum AnimalSpecies.
        """
        if self.animal is not None:
            self.animal.species = species
            self.propertyChanged.emit(self.animal)
            
            # check if model contains the species and adds it otherwise
            if len(self.models.model_species.findItems(species)) > 0 and  \
            hasattr(self.parent(), "animal_painter"):
                self.parent().animal_painter.setAnimalSpecies(species) 
                self.focusNextChild()
            
    def onGroupComboboxChanged(self, group):
        """
        Function called when group combobox entry is changed. It sets the
        group of the current animal.

        Parameters
        ----------
        group : string
            The selected group of the animal. 
            Selectable from the Enum AnimalGroup.
        """
        if self.animal is not None:
            self.animal.group = group
            self.propertyChanged.emit(self.animal)
            
            if len(self.models.model_group.findItems(group)) > -1 \
            and hasattr(self.parent(), "animal_painter"):
                self.parent().animal_painter.setAnimalGroup(group) 
                self.focusNextChild()
     
    def onLengthSpinboxChanged(self, value):
        """
        Called when length combobox is changed. Sets the length of the
        current animal. 

        Parameters
        ----------
        value : float
            New value for animal length.
        """
        if self.animal is not None:
            self.animal.length = value
            self.parent().animal_painter.cur_animal.length = value
            self.focusNextChild()
        
    def setAnimal(self, animal):
        """
        Copies a given animal into the specifications window or resets the 
        specs window and disables it when no animal is provided.

        Parameters
        ----------
        animal : Animal
            Animal to copy.
        """
        self.animal = animal
        
        if animal is not None:
            # enable widget
            self.setEnabled(True)
            
            # set group
            if animal.group in AnimalGroup.__members__.values(): 
                self.animal.group = animal.group.name.title()
            else:
                self.animal.group = animal.group
                
            # set species
            self.animal.species = animal.species
    
            # set remark
            if animal.remark is not None:
                self.animal.remark = str(animal.remark)
            else:
                self.animal.remark = ""
            
            # set length
            self.animal.length = animal.length
            self.updateVisuals()
        
        else:            
            self.updateVisuals()
            self.setEnabled(False)
            
    def updateVisuals(self):
        """ Sets the visuals of the specifications widget to the currently
        set animal. """
        
        if self.animal is None:
            group = AnimalGroup.UNIDENTIFIED.name.title()
            species = AnimalSpecies.UNIDENTIFIED.name.title()
            remark = ""
            length = 0
        else:
            group = self.animal.group
            species = self.animal.species
            remark = self.animal.remark
            length = self.animal.length
        
        # set group combobox
        index = self.comboBox_group.findText(group) 
        if index != -1:
            # blocking signal to avoid calling onGroupComboboxChanged and 
            # thus starting a loop
            self.comboBox_group.blockSignals(True) 
            self.comboBox_group.setCurrentIndex(index)
            self.comboBox_group.blockSignals(False)

        # set species combobox
        index = self.comboBox_species.findText(str(species)) 
        if index != -1:
            self.comboBox_species.blockSignals(True)
            self.comboBox_species.setCurrentIndex(index)
            self.comboBox_species.blockSignals(False)    
        elif species != "" and species is not None:
            # add new species entry
            self.models.addSpecies(str(species), "")
        
        # set remark combobox
        index = self.comboBox_remark.findText(remark) 
        
        # if the remark is already present in a similar form, take its index 
        for i in range(self.models.model_animal_remarks.rowCount()):
            item = self.models.model_animal_remarks.item(i)
            
            if item.text().lower() == remark.lower():
                index = self.comboBox_remark.findText(item.text()) 
                remark = item.text()
            
        if len(self.models.model_animal_remarks.findItems(remark)) != 0 or \
        len(self.models.model_animal_remarks.findItems(remark)):
            self.comboBox_remark.blockSignals(True)
            self.comboBox_remark.setCurrentIndex(index)
            self.comboBox_remark.blockSignals(False)  
        elif remark == "nan":
            self.comboBox_remark.blockSignals(True)
            self.comboBox_remark.setCurrentIndex(0)
            self.comboBox_remark.blockSignals(False)            
        elif remark != "" and remark is not None:
            print("adding new remark entry----------------------")
            item = QtGui.QStandardItem(str(remark))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.models.model_animal_remarks.appendRow(item)
            self.comboBox_remark.setCurrentIndex(self.comboBox_remark.count() - 1)
            
        # set length spinbox
        if length is not None and length != -1: 
            self.spinBox_length.blockSignals(True)
            self.spinBox_length.setValue(length) 
            self.spinBox_length.blockSignals(False)
        else: 
            self.spinBox_length.setValue(0)
        
    def _initActions(self):
        """ Function to connect signals and slots. """
        # connecting signals and slots
        self.spinBox_length.valueChanged.connect(self.onLengthSpinboxChanged)
        self.comboBox_group.currentTextChanged.connect(self.onGroupComboboxChanged)
        self.comboBox_species.currentTextChanged.connect(self.onSpeciesComboboxChanged)
        self.comboBox_remark.currentIndexChanged.connect(self.onRemarkComboboxEdited)
        self.comboBox_remark.lineEdit().editingFinished.connect(self.onRemarkComboboxEdited)

        self.btn_group_fish.clicked.connect(partial(self._set_combobox_group_idx, 0))
        self.btn_group_crustacea.clicked.connect(partial(self._set_combobox_group_idx, 1))
        self.btn_group_chaetognatha.clicked.connect(partial(self._set_combobox_group_idx, 2))
        self.btn_group_jellyfish.clicked.connect(partial(self._set_combobox_group_idx, 3))
        self.btn_group_unidentified.clicked.connect(partial(self._set_combobox_group_idx, 4))
        
    def _initUi(self):
        """ Inits the UI. """
        self.setObjectName("animal_specs_widget")
        self.setStyleSheet("QLabel{font:12pt 'Century Gothic'; color:white;} ")
           
        # main layout
        layout = QtWidgets.QGridLayout(self)
        layout.setObjectName("layout")
        
        # labels
        self.label_group = QtWidgets.QLabel("Group", self)
        self.label_species = QtWidgets.QLabel("Species", self)
        self.label_remark = QtWidgets.QLabel("Remark", self)
        self.label_length = QtWidgets.QLabel("Length", self)
        #self.label_height = QtWidgets.QLabel("Height")
                
        # combobox for animal group
        self.comboBox_group = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_group.sizePolicy().hasHeightForWidth())
        self.comboBox_group.setSizePolicy(sizePolicy)
        self.comboBox_group.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_group.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_group.setEditable(True)
        self.comboBox_group.lineEdit().setReadOnly(True)
        self.comboBox_group.lineEdit().setAlignment(QtCore.Qt.AlignRight)
        self.comboBox_group.setObjectName("comboBox_group")         
        self.comboBox_group.setIconSize(QtCore.QSize(20, 20))
        
        # combobox for animal species
        self.comboBox_species = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_species.sizePolicy().hasHeightForWidth())
        self.comboBox_species.setSizePolicy(sizePolicy)
        self.comboBox_species.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBox_species.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_species.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_species.setEditable(True)
        self.comboBox_species.lineEdit().setReadOnly(True)
        self.comboBox_species.lineEdit().setAlignment(QtCore.Qt.AlignRight)
        self.comboBox_species.setObjectName("comboBox_species")
        
        combo_delegate = Helpers.ComboboxDelegate(None, self.comboBox_species)
        self.comboBox_species.setItemDelegate(combo_delegate)
        
        # combobox for animal remark
        self.comboBox_remark = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_remark.sizePolicy().hasHeightForWidth())
        self.comboBox_remark.setSizePolicy(sizePolicy)
        self.comboBox_remark.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_remark.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_remark.setEditable(True)
        self.comboBox_remark.lineEdit().setAlignment(QtCore.Qt.AlignRight)
        self.comboBox_remark.setObjectName("comboBox_remark")
        
        self.spinBox_length = QtWidgets.QDoubleSpinBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_length.sizePolicy().hasHeightForWidth())
        self.spinBox_length.setSizePolicy(sizePolicy)
        self.spinBox_length.setMinimumSize(QtCore.QSize(200, 40))
        self.spinBox_length.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinBox_length.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_length.setMaximum(99909.99)
        self.spinBox_length.setObjectName("spinBox_length")
        self.spinBox_length.setEnabled(False)
        self.spinBox_length.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_length.setToolTip("Animal length in mm")
        self.spinBox_length.setSuffix(" mm")
        
        # self.spinBox_heigth = QtWidgets.QDoubleSpinBox(self)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.spinBox_heigth.sizePolicy().hasHeightForWidth())
        # self.spinBox_heigth.setSizePolicy(sizePolicy)
        # self.spinBox_heigth.setMinimumSize(QtCore.QSize(200, 40))
        # self.spinBox_heigth.setMaximumSize(QtCore.QSize(16777215, 40))
        # self.spinBox_heigth.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        # self.spinBox_heigth.setMaximum(9999.99)
        # self.spinBox_heigth.setObjectName("spinBox_heigth")
            
        
         # align buttons in a horizontal layout
        button_layout = QtWidgets.QHBoxLayout(self)
        button_layout.setObjectName("button_layout")
        button_layout.setContentsMargins(0, 0, 0, 0)
 
        # frame for group buttons
        self.frame_group_btns = QtWidgets.QFrame(self)
        self.frame_group_btns.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.frame_group_btns.setLayout(button_layout)
        
        # icon size for group buttons
        icon_group_size = QtCore.QSize(30, 30)
        
        # fish button @todo : add abbreviation to buttons icons
        self.btn_group_fish = QtWidgets.QPushButton(self.frame_group_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_group_fish.sizePolicy().hasHeightForWidth())
        self.btn_group_fish.setSizePolicy(sizePolicy)
        self.btn_group_fish.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_group_fish.setIcon(Helpers.getIcon(":/animal_markings/animal_markings/square_blue.png"))# ":/icons/icons/filter.png"))
        self.btn_group_fish.setIconSize(icon_group_size)
        self.btn_group_fish.setObjectName("btn_group_fish")
        self.btn_group_fish.setToolTip("Fish")
        
        # crustacea button
        self.btn_group_crustacea = QtWidgets.QPushButton(self.frame_group_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_group_crustacea.sizePolicy().hasHeightForWidth())
        self.btn_group_crustacea.setSizePolicy(sizePolicy)
        self.btn_group_crustacea.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_group_crustacea.setIcon(Helpers.getIcon(":/animal_markings/animal_markings/square_red.png"))# ":/icons/icons/filter.png"))
        self.btn_group_crustacea.setIconSize(icon_group_size)
        self.btn_group_crustacea.setObjectName("btn_group_crustacea")
        self.btn_group_crustacea.setToolTip("Crustacea")
        
        # chateognatha button
        self.btn_group_chaetognatha = QtWidgets.QPushButton(self.frame_group_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_group_chaetognatha.sizePolicy().hasHeightForWidth())
        self.btn_group_chaetognatha.setSizePolicy(sizePolicy)
        self.btn_group_chaetognatha.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_group_chaetognatha.setIcon(Helpers.getIcon(":/animal_markings/animal_markings/square_orange.png"))# ":/icons/icons/filter.png"))
        self.btn_group_chaetognatha.setIconSize(icon_group_size)
        self.btn_group_chaetognatha.setObjectName("btn_group_chaetognatha")
        self.btn_group_chaetognatha.setToolTip("Chaetognatha")
        
        # jellfish button
        self.btn_group_jellyfish = QtWidgets.QPushButton("J")
        self.btn_group_jellyfish = QtWidgets.QPushButton(self.frame_group_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_group_jellyfish.sizePolicy().hasHeightForWidth())
        self.btn_group_jellyfish.setSizePolicy(sizePolicy)
        self.btn_group_jellyfish.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_group_jellyfish.setIcon(Helpers.getIcon(":/animal_markings/animal_markings/square_black.png"))# ":/icons/icons/filter.png"))
        self.btn_group_jellyfish.setIconSize(icon_group_size)
        self.btn_group_jellyfish.setObjectName("btn_group_jellyfish")
        self.btn_group_jellyfish.setToolTip("Jellyfish")
        
        # unidentified button
        self.btn_group_unidentified = QtWidgets.QPushButton("U") 
        self.btn_group_unidentified = QtWidgets.QPushButton(self.frame_group_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_group_unidentified.sizePolicy().hasHeightForWidth())
        self.btn_group_unidentified.setSizePolicy(sizePolicy)
        self.btn_group_unidentified.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_group_unidentified.setIcon(Helpers.getIcon(":/animal_markings/animal_markings/square_gray.png"))# ":/icons/icons/filter.png"))
        self.btn_group_unidentified.setIconSize(icon_group_size)
        self.btn_group_unidentified.setObjectName("btn_group_unidentified")
        self.btn_group_unidentified.setToolTip("Unidentified")
        
        # add buttons to layout
        button_layout.addWidget(self.btn_group_fish)
        button_layout.addWidget(self.btn_group_crustacea)
        button_layout.addWidget(self.btn_group_chaetognatha)
        button_layout.addWidget(self.btn_group_jellyfish)
        button_layout.addWidget(self.btn_group_unidentified)
        
        # add widgets to layout
        layout.addWidget(self.label_group, 0, 0, 1, 1)
        layout.addWidget(self.frame_group_btns, 0, 1, 1, 1)
        layout.addWidget(self.comboBox_group, 1, 1, 1, 1)
        
        layout.addWidget(self.label_species, 2, 0, 1, 1)
        layout.addWidget(self.comboBox_species, 2, 1, 1, 1)
        
        layout.addWidget(self.label_remark, 3, 0, 1, 1)
        layout.addWidget(self.comboBox_remark, 3, 1, 1, 1)
        
        layout.addWidget(self.label_length, 4, 0, 1, 1)
        layout.addWidget(self.spinBox_length, 4, 1, 1, 1)
           
        # layout.addWidget(self.label_height, 4, 0, 1, 1)
        # layout.addWidget(self.spinBox_heigth, 4, 1, 1, 1)

