#https://stackoverflow.com/questions/60571837/how-to-move-a-figurecreated-using-paintevent-by-simply-draging-it-in-pyqt5

from PyQt5 import QtCore, QtGui, QtWidgets
from Models import AnimalGroup, AnimalSpecies
import Helpers

class Animal():
    """ 
    Class to represent an animal on an image. 
    
    Attributes
    ----------
    group: string
        group of the animal
    species: string
        species of the animal
    remark: string
        remark to the animal
    length: float
        length of the animal 
    row_index : int
        row index of the represented animal in the data table
    pixmap_width: int
        width (=height) of the pixmaps for animal head and tail
    original_pos_head: QPoint
        position of the animal head on the original resolution image
    original_pos_tail: QPoint
        position of the animal tail on the original resolution image
    position_head: QPoint
        position of the animal head on the currently displayed size of the 
        image
    position_tail: QPoint
        position of the animal tail on the currently displayed size of the 
        image
    is_head_drawn: bool
        states if the head of the animal is drawn on the canvas
    is_tail_drawn: bool
        states if the tail of the animal is drawn on the canvas
    boundingBoxOffset: [int, int]
        distance between head/tail points and bounding box
        
    Methods
    -------
    createHeadVisual():
    createTailVisual():
    setManuallyCorrected(corrected=False):
        if the user has adapted the animal, this variable has to be set to 
        True (for statistical evaluation purposes of the neural network)
    getColorsAccordingToGroup():
        finds the color for the animal according to its group 
    setPositionHead
    setPositionTail
    setGroup
    setSpecies
    setRemark
    calculateBoundingBox
    """
    
    
    # the input position refers to the center of the visual!
    def __init__(self, models, row_index, position_head=QtCore.QPoint(-1,-1), 
                 position_tail=QtCore.QPoint(-1,-1), 
                 group=AnimalGroup.UNIDENTIFIED, 
                 species=AnimalSpecies.UNIDENTIFIED, remark=""):
        """
        Init function.

        Parameters
        ----------
        row_index : int
            The index of the row in the result table that this animal 
            represents.
        position_head : QPoint, optional
            The position of the animal head. It will be the center for the 
            head visual, i.e. an 'o'. The default is QtCore.QPoint(-1,-1).
        position_tail : QPoint, optional
            The position of the animal tail. It will be the center for the 
            tail visual, i.e. a 'x'. The default is QtCore.QPoint(-1,-1).
        group : string, optional
            The group of the animal. Selectable from the Enum AnimalGroup.
            The default is AnimalGroup.UNIDENTIFIED.
        species : string, optional
            The species of the animal. Selectable from the Enum AnimalSpecies.
            The default is AnimalSpecies.UNIDENTIFIED.
        remark : string, optional
            The remark to the animal. The default is "".
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
        self.original_pos_head = QtCore.QPoint(position_head)
        self.original_pos_tail = QtCore.QPoint(position_tail)
        
        # current position of head and tail on the image
        self.position_head = position_head
        self.position_tail = position_tail
        
        # group, species, remark and length of the animal
        self.group = group
        self.species = species
        self.remark = remark
        self.length = None
        #self.height = None
      
        # set the visual for the head, tail and line between them @todo pblic or private?
        self.pos_visual_head = position_head - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)
        self.pos_visual_tail = position_tail - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)

        self.rect_head = QtCore.QRect(self.pos_visual_head, QtCore.QSize(
            self.pixmap_width, self.pixmap_width))
        self.rect_tail = QtCore.QRect(self.pos_visual_tail, QtCore.QSize(
            self.pixmap_width, self.pixmap_width))       
        self.line = QtCore.QLineF(self.position_head, self.position_tail)  

        # indicate if head/tail is already drawn
        self.is_head_drawn = False
        self.is_tail_drawn = False           

        # set pixmaps for head/tail visuals
        self.getColorsAccordingToGroup()
        
        # set the bounding box visual
        self.boundingBox = QtCore.QRectF()
        self.boundingBoxOffset = [50, 50]
        self.calculateBoundingBox()
        
        # the actual items for head, tail, line and boundingbox in the scene
        self.boundingBox_visual = None
        self.head_item_visual = None
        self.tail_item_visual = None
        self.line_item_visual = None
        
        # indicate if this animal was manually corrected
        self.manually_corrected = False
     
     
    def createHeadVisual(self):
        if self.position_head != QtCore.QPoint(-1,-1):
            # create the head visual
            self.head_item_visual = QtWidgets.QGraphicsPixmapItem( \
                self._pixmap_head)
            self.head_item_visual.setPos(self.rect_head.center() \
                                         - QtCore.QPoint( \
                                             self.pixmap_width/4, 
                                             self.pixmap_width/4))
            self.head_item_visual.ItemIsMovable = True
        
            self.is_head_drawn = True
        return self.head_item_visual
     
    def createTailVisual(self):
        if self.position_tail != QtCore.QPoint(-1,-1):
            # create the tail visual
            self.tail_item_visual = QtWidgets.QGraphicsPixmapItem( \
                self._pixmap_tail)
            self.tail_item_visual.setPos(self.rect_tail.center() \
                                         - QtCore.QPoint( \
                                             self.pixmap_width/4, 
                                             self.pixmap_width/4))
            self.tail_item_visual.ItemIsMovable = True
            
            self.is_tail_drawn = True
        return self.tail_item_visual
    
    def setManuallyCorrected(self, corrected=False):
        self._models.model_animals.data.loc[
            self.row_index, "manually_corrected"] = corrected
                    
    def getColorsAccordingToGroup(self):
        """
        Function that finds the colour for the animal according to its group 
        and finds the pixmaps for head and tail accordingly.
        """
        self.color = ""
        
        if self.group == AnimalGroup.UNIDENTIFIED \
        or self.group == "Unidentified":
            self._pixmap_head = QtGui.QPixmap("animal_markings/o_gray.png")        
            self._pixmap_tail = QtGui.QPixmap("animal_markings/x_gray.png")  
            self.color = QtGui.QColor(217, 217, 217)
              
        elif self.group == AnimalGroup.FISH or self.group == "Fish":
            self._pixmap_head = QtGui.QPixmap("animal_markings/o_blue.png")        
            self._pixmap_tail = QtGui.QPixmap("animal_markings/x_blue.png")  
            self.color = QtGui.QColor(0, 112, 192)
            
        elif self.group == AnimalGroup.CRUSTACEA or self.group == "Crustacea":
            self._pixmap_head = QtGui.QPixmap("animal_markings/o_red.png")        
            self._pixmap_tail = QtGui.QPixmap("animal_markings/x_red.png") 
            self.color = QtGui.QColor(255, 0, 0)
            
        elif self.group == AnimalGroup.CHAETOGNATHA \
        or self.group == "Chaetognatha":
            self._pixmap_head = QtGui.QPixmap("animal_markings/o_orange.png")        
            self._pixmap_tail = QtGui.QPixmap("animal_markings/x_orange.png")  
            self.color = QtGui.QColor(255, 192, 0)
            
        elif self.group == AnimalGroup.JELLYFISH or self.group == "Jellyfish":
            self._pixmap_head = QtGui.QPixmap("animal_markings/o_black.png")        
            self._pixmap_tail = QtGui.QPixmap("animal_markings/x_black.png") 
            self.color = QtGui.QColor(0, 0, 0)
     
        # scale pixmaps
        self._pixmap_head = self._pixmap_head.scaled(QtCore.QSize(
            self.pixmap_width/2, self.pixmap_width/2))     
        self._pixmap_tail = self._pixmap_tail.scaled(QtCore.QSize(
            self.pixmap_width/2, self.pixmap_width/2))
        
    
    def setPositionHead(self, pos):
        self.position_head = pos
        self.rect_head.moveTopLeft(pos - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2))
        self.pos_visual_head = pos - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)
        
        self.line.setP1(pos)
        self.calculateBoundingBox() 
    
    def setPositionTail(self, pos):
        self.position_tail = pos
        self.rect_tail.moveTopLeft(pos - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2))
        self.pos_visual_tail = pos - QtCore.QPoint(
            self.pixmap_width/2, self.pixmap_width/2)
        
        self.line.setP2(pos)
        self.calculateBoundingBox()
        
    def setGroup(self, group):
        self.group = group
        self.getColorsAccordingToGroup()
        
        # adapt group in data model if there is an entry for this animal
        if self.row_index in self._models.model_animals.data.index:
            self._models.model_animals.data.loc[
                self.row_index, 'group'] = group
    
    def setSpecies(self, species):
        self.species = species
        
        # adapt species in data model if there is an entry for this animal
        if self.row_index in self._models.model_animals.data.index:
            self._models.model_animals.data.loc[
                self.row_index, 'species'] = species
    
    def setRemark(self, remark):
        self.remark = remark
        
        # adapt species in data model if there is an entry for this animal
        if self.row_index in self._models.model_animals.data.index:
            self._models.model_animals.data.loc[
                self.row_index, 'object_remarks'] = remark
    
    def calculateBoundingBox(self):
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


class AnimalSpecificationsWidget(QtWidgets.QWidget):
    """ A widget to provide all information about the current animal. """
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
        
        self.group = AnimalGroup.UNIDENTIFIED.name.title()
        self.species = AnimalSpecies.UNIDENTIFIED.name.title()
        self.remark = ""
        self.length = 0
        self.models = models
        
        self._initUi()
        self._initActions()
        self._initModels()
       
        # setting visuals to initial values and hiding widget
        self.updateVisuals()
        self.hide()
        
        # set tab sequence
        self.setTabOrder(self.comboBox_group, self.comboBox_species)
        self.setTabOrder(self.comboBox_species, self.comboBox_remark)
        self.setTabOrder(self.comboBox_remark, self.spinBox_length)
        
    def _initActions(self):
        """ Function to connect signals and slots. """
        # connecting signals and slots
        self.spinBox_length.valueChanged.connect(self.on_length_spinbox_changed)
        self.comboBox_group.currentTextChanged.connect(self.on_group_combobox_changed)
        self.comboBox_species.currentTextChanged.connect(self.on_species_combobox_changed)
        self.comboBox_remark.currentTextChanged.connect(self.on_remark_combobox_changed)
        self.comboBox_remark.lineEdit().editingFinished.connect(self.on_remark_combobox_edited)
        self.comboBox_remark.lineEdit().returnPressed.connect(self.on_remark_combobox_return_pressed)
        
    def _initModels(self):
        """ Function to set the data models on class widgets. """
        self.comboBox_group.setModel(self.models.model_group)
        self.comboBox_species.setModel(self.models.model_species)
        self.comboBox_remark.setModel(self.models.model_animal_remarks)
        
    def on_remark_combobox_return_pressed(self):
        """ Function dealing with the return event on the editable combobox 
        for animal remarks. This ensures that the newly typed entry is 
        capitalized and right-aligned. """
        text = self.comboBox_remark.currentText()
        index = self.comboBox_remark.findText(text)
        
        if index != -1:
            # remove item from animal remarks model
            items = self.models.model_animal_remarks.findItems(text)
            for item in items:
                self.models.model_animal_remarks.removeRow(item.row())
            
            # add a capitalized, right-aligned entry in model
            item = QtGui.QStandardItem(str(text.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.models.model_animal_remarks.appendRow(item)
            
            # set current combobox image to the new entry and switch focus
            self.comboBox_remark.setCurrentIndex(index)
            self.focusNextChild()

    # @todo would editfinsihed not be enough?   
    def on_remark_combobox_edited(self):
        """
        Function called when animal remark is edited. 
        """
        text = self.comboBox_remark.currentText()
        print(f"editing finsihed {text}")
        
        # if the text is not yet in the combobox, add it
        if len(self.models.model_animal_remarks.findItems(text)) == 0:
            print("on remark combobox edited adding to model")
        #if self.comboBox_remark.findText(text) == -1:
            item = QtGui.QStandardItem(str(text.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.models.model_animal_remarks.appendRow(item)
            self.focusNextChild()
     
    # @todo why to i need this?
    def on_remark_combobox_changed(self, remark):
        """ Function handling when the animal remark combobox gets changed, 
        i.e. the editing is not finished yet. """
        self.parent().animal_painter.setAnimalRemark(str(remark))
        
    def on_species_combobox_changed(self, species):
        """ Function called when the species combobox is changed. 
        It sets the species of the current animal. 

        Parameters
        ----------
        species : string
            The selected species of the animal. 
            Selectable from the Enum AnimalSpecies.
        """
        
        # check if model contains the species and adds it otherwise
        if len(self.models.model_species.findItems(species)) > 0 and hasattr(self.parent(), "animal_painter"):
        #if self.comboBox_species.findText(species) != -1 and hasattr(self.parent(), "animal__painter"):
            self.species = species
            self.parent().animal_painter.setAnimalSpecies(species) #setAnimalGroup(group) 
            self.focusNextChild()
        else:
            print("Given species was not in combobox")
            #@todo add species to model
            
    def on_group_combobox_changed(self, group):
        """
        Function called when group combobox entry is changed. It sets the
        group of the current animal.

        Parameters
        ----------
        group : string
            The selected group of the animal. 
            Selectable from the Enum AnimalGroup.
        """
        if len(self.models.model_group.findItems(group)) > -1 and hasattr(self.parent(), "animal_painter"):
        #if self.comboBox_group.findText(group) != -1 and hasattr(self.parent(), "animal_painter"):
            self.group = group
            self.parent().animal_painter.setAnimalGroup(group) #setAnimalGroup(group) 
            self.focusNextChild()
        else:
            print("Given group was not in combobox")
     
    def on_length_spinbox_changed(self, value):
        self.length = value
        self.parent().animal_painter.cur_animal.length = value#setAnimalLength(value)
        self.focusNextChild()
        
    def setAnimal(self, animal):
        # set group
        if animal.group in AnimalGroup.__members__.values(): 
            self.group = animal.group.name.title()
        else:
            self.group = animal.group
            
        # set species
        if animal.species in AnimalSpecies.__members__.values(): 
            self.species = animal.species.name.title()
        else:
            self.species = animal.species

        if animal.remark is not None:
            self.remark = str(animal.remark)
        else:
            self.remark = ""
            
        self.length = animal.length
        self.updateVisuals()
    
    def updateVisuals(self):
        # set group combobox
        index = self.comboBox_group.findText(self.group) 
        if index != -1:
            self.comboBox_group.blockSignals(True) # blocking signal to avoid calling on_group_combobox_changed and thus starting a loop
            self.comboBox_group.setCurrentIndex(index)
            self.comboBox_group.blockSignals(False)

        # set species combobox
        index = self.comboBox_species.findText(self.species) 
        if index != -1:
            self.comboBox_species.blockSignals(True)
            self.comboBox_species.setCurrentIndex(index)
            self.comboBox_species.blockSignals(False)       
        
        # set remark combobox
        index = self.comboBox_remark.findText(self.remark) 
        if len(self.models.model_animal_remarks.findItems(self.remark)) != 0 or \
        len(self.models.model_animal_remarks.findItems(self.remark.title())):
            self.comboBox_remark.blockSignals(True)
            self.comboBox_remark.setCurrentIndex(index)
            self.comboBox_remark.blockSignals(False)  
        elif self.remark == "nan":
            self.comboBox_remark.blockSignals(True)
            self.comboBox_remark.setCurrentIndex(0)
            self.comboBox_remark.blockSignals(False)            
        elif self.remark != "" and self.remark is not None:
            print("adding new remark entry----------------------")
            item = QtGui.QStandardItem(str(self.remark).title())
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.models.model_animal_remarks.appendRow(item)
            self.comboBox_remark.setCurrentIndex(self.comboBox_remark.count() - 1)
            #self.model_remarks.appendRow(item)
            
  
        
        # set length spinbox
        if self.length: 
            self.spinBox_length.blockSignals(True)
            self.spinBox_length.setValue(self.length) 
            self.spinBox_length.blockSignals(False)
        else: 
            self.spinBox_length.setValue(0)

    
    def _initUi(self):
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
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
        
            
        # add widgets to layout
        layout.addWidget(self.label_group, 0, 0, 1, 1)
        layout.addWidget(self.comboBox_group, 0, 1, 1, 1)
        
        layout.addWidget(self.label_species, 1, 0, 1, 1)
        layout.addWidget(self.comboBox_species, 1, 1, 1, 1)
        
        layout.addWidget(self.label_remark, 2, 0, 1, 1)
        layout.addWidget(self.comboBox_remark, 2, 1, 1, 1)
        
        layout.addWidget(self.label_length, 3, 0, 1, 1)
        layout.addWidget(self.spinBox_length, 3, 1, 1, 1)
           
        # layout.addWidget(self.label_height, 4, 0, 1, 1)
        # layout.addWidget(self.spinBox_heigth, 4, 1, 1, 1)

