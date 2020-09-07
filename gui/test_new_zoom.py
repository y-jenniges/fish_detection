# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import pandas as pd
import ntpath

from test_graph import Animal
from Models import AnimalGroup, AnimalSpecies, TableModel
from Helpers import get_icon

#IMAGE_DIRECTORY = "../data/maritime_dataset_25/training_data_animals/"
#IMAGE_PREFIX = ""
ANIMAL_LIST = []
# ANIMAL_REMARKS = ["", "Not determined",  "Animal incomplete"]
# IMAGE_REMARKS = []

# class GroupItemModel(QtCore.QAbstractItemModel):
#     def __init__(self, in_nodes):  
#         QtCore.QAbstractItemModel.__init__(self)  
#         self._root = CustomNode(None)  
  
#     def rowCount(self, in_index):  
#         if in_index.isValid():  
#             return in_index.internalPointer().childCount()  
#         return self._root.childCount()  
  
#     def columnCount(self, in_index):  
#         return 1  
    
#     def index(self):
#         pass
    
#     def parent(self):
#         pass
    
#     def data(self):
#         pass



class AnimalSpecificationsWidget(QtWidgets.QWidget):
    """ A widget to provide all information of the current animal. """
    def __init__ (self, models, parent = None):
        super(QtWidgets.QWidget, self).__init__(parent)
        
        self.group = AnimalGroup.UNIDENTIFIED.name.title()
        self.species = AnimalSpecies.UNIDENTIFIED.name.title()
        self.remark = ""
        self.length = 0
        self.models = models
        
        self.init_ui()
        self.init_actions()
        self.init_models()
       
        # setting visuals to initial values and hiding widget
        self.updateVisuals()
        self.hide()
        
        # set tab sequence
        self.setTabOrder(self.comboBox_group, self.comboBox_species)
        self.setTabOrder(self.comboBox_species, self.comboBox_remark)
        self.setTabOrder(self.comboBox_remark, self.spinBox_length)
        

    def init_actions(self):
        # connecting signals and slots
        self.spinBox_length.valueChanged.connect(self.on_length_spinbox_changed)
        self.comboBox_group.currentTextChanged.connect(self.on_group_combobox_changed)
        self.comboBox_species.currentTextChanged.connect(self.on_species_combobox_changed)
        self.comboBox_remark.currentTextChanged.connect(self.on_remark_combobox_changed)
        self.comboBox_remark.lineEdit().editingFinished.connect(self.on_remark_combobox_edited)
                 
    def init_models(self):
        self.comboBox_group.setModel(self.models.model_group)
        self.comboBox_species.setModel(self.models.model_species)
        self.comboBox_remark.setModel(self.models.model_animal_remarks)
        
    def on_remark_combobox_edited(self):
        text = self.comboBox_remark.currentText()
        
        # if the text is not yet in the combobox, add it
        if self.comboBox_remark.findText(text) == -1:
            item = QtGui.QStandardItem(str(text.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.model_remarks.appendRow(item)
            self.focusNextChild()
      
    def on_remark_combobox_changed(self, remark):
        self.parent().animal_painter.setAnimalRemark(str(remark))
        
    def on_species_combobox_changed(self, species):
        if self.comboBox_species.findText(species) != -1 and hasattr(self.parent(), "animal__painter"):
            self.species = species
            self.parent().animal_painter.setAnimalSpecies(species) #setAnimalGroup(group) 
            self.focusNextChild()
        else:
            print("Given species was not in combobox")
            
    def on_group_combobox_changed(self, group):
        if self.comboBox_group.findText(group) != -1 and hasattr(self.parent(), "animal__painter"):
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
        if index != -1:
            self.comboBox_remark.blockSignals(True)
            self.comboBox_remark.setCurrentIndex(index)
            self.comboBox_remark.blockSignals(False)  
        elif self.remark == "nan":
            self.comboBox_remark.blockSignals(True)
            self.comboBox_remark.setCurrentIndex(0)
            self.comboBox_remark.blockSignals(False)            
        elif self.remark != "" and self.remark is not None:
            print("adding new remark entry")
            item = QtGui.QStandardItem(str(self.remark))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.models.model_animal_remarks.appendRow(item)
            #self.model_remarks.appendRow(item)
        
        # set length spinbox
        if self.length: 
            self.spinBox_length.blockSignals(True)
            self.spinBox_length.setValue(self.length) 
            self.spinBox_length.blockSignals(False)
        else: 
            self.spinBox_length.setValue(0)

    
    def init_ui(self):
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
        self.comboBox_group.setIconSize(QtCore.QSize(15, 15))

        # combobox for animal species
        self.comboBox_species = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_species.sizePolicy().hasHeightForWidth())
        self.comboBox_species.setSizePolicy(sizePolicy)
        self.comboBox_species.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_species.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_species.setEditable(True)
        self.comboBox_species.lineEdit().setReadOnly(True)
        self.comboBox_species.lineEdit().setAlignment(QtCore.Qt.AlignRight)
        self.comboBox_species.setObjectName("comboBox_species")
        
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



class ImageArea(QtWidgets.QGraphicsView):
    """
    An implementation of QGraphicsView to enable painting of animals on a 
    photo as well as loading of photos. Moreover, it provides a 
    wheel zoom functionality.
    """
    def __init__(self, models, parent=None):
        super(ImageArea, self).__init__(parent)
        print("init image area")
        self._zoom = 0
        self._scene = QtWidgets.QGraphicsScene()
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._empty = True
        self._scene.addItem(self._photo)     
        self.setScene(self._scene)

        # set properties for graphics view
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        # animal painter to enable adding/removing of animals
        self.animal_painter = AnimalPainter(models, self)      
        
    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
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
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self.setEnableInteraction(True)
            self._empty = False
            #self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
           
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
            self.setEnableInteraction(False)
        self.fitInView() 
        
    def setEnableInteraction(self, isInteractionEnabled):
        self.setEnabled(isInteractionEnabled)
        
    def wheelEvent(self, event):
        if self.hasPhoto():  
            factor = 1
            
            # zoom in if y > 0 (wheel forward), else zoom out (maximum zoom level of 30)
            if event.angleDelta().y() > 0 and self._zoom <= 30:
                factor = 1.15
                self._zoom += 1
            elif event.angleDelta().y() <= 0:
                factor = 0.9
                self._zoom -= 1
            
            # scale the view if zoom is positive, else set it to zero and fit the photo in the view
            if self._zoom > 0:
                self.scale(factor, factor)
                self.parent().setArrowShortcutsActive(False)
            elif self._zoom == 0:
                self.fitInView()
                self.parent().setArrowShortcutsActive(True)
            else:
                self._zoom = 0
                self.parent().setArrowShortcutsActive(True)
            
            #print(f"zoom {self._zoom}")
            #print(f"own width and photo width {self.width(), self._photo.pixmap().rect().width(), self.transform().scale()}")
            #print()
            
    # delegate mouse events to animal painter
    def mousePressEvent(self, event):
        self.animal_painter.mousePressEvent(event)       
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.animal_painter.mouseMoveEvent(event)  
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.animal_painter.mouseReleaseEvent(event)
        super().mouseReleaseEvent(event) 


class AnimalPainter():
    """
    Class providing the logic for adding/removing/moving and jumping between 
    animals. It needs a QGraphicsView that it can paint on and that delegates 
    the mouse events to the AnimalPainter.
    """
    def __init__(self, models, imageArea):

        # dragging offset when moving the markings for head and/or tail
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()
        
        # current animal
        self.cur_animal  = None
        self.widget_animal_specs = AnimalSpecificationsWidget(models, imageArea)
        
        # variables to control what interactions are possible
        self.is_add_mode_active = False
        self.is_remove_mode_active = False
        
        # the QGraphicsView to paint on
        self.imageArea = imageArea
        
        # original size of image
        self.original_img_width = 0
        self.original_img_height = 0
    
    
    def setAnimalRemark(self, remark):
        self.cur_animal.remark = remark
    
    def setAnimalSpecies(self, species):
        self.cur_animal.species = species

    def setAnimalGroup(self, group):
        self.cur_animal.setGroup(group)
        
        # update drawing
        self.cur_animal.head_item_visual.setPixmap(self.cur_animal.pixmap_head)
        self.cur_animal.tail_item_visual.setPixmap(self.cur_animal.pixmap_tail)
        
        # redraw line and boundingbox visuals
        self.imageArea._scene.removeItem(self.cur_animal.line_item_visual)
        self.drawAnimalLine(self.cur_animal)
        
        self.imageArea._scene.removeItem(self.cur_animal.boundingBox_visual)
        self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(self.cur_animal.boundingBox, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
     

    def removeAll(self):
        for animal in ANIMAL_LIST:
            self.removeHeadVisual(animal)
            self.removeTailVisual(animal)
            self.removeLineVisual(animal)
            self.removeBoundingBoxVisual(animal)
            
            animal.is_head_drawn = False
            animal.is_tail_drawn = False
     
    # function to move to specs widget with the bounding bos of the current animal (and prevent it from getting out of the borders of the image)
    def placeSpecsWidget(self):
        if self.cur_animal is not None:
            # reset position of specs widget
            self.widget_animal_specs.move(0,0)
        
            # get position of current bounding box from scene
            pos = self.imageArea.mapFromScene(self.cur_animal.boundingBox_visual.rect().bottomLeft().toPoint())
            
            # move the zoom widget a bit below the button position and center it below the button
            self.widget_animal_specs.move(pos)
        
            # get corners of specs widget in scene coordinates
            top_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topLeft())).toPoint()
            top_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topRight())).toPoint()
            bottom_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomLeft())).toPoint()
            bottom_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomRight())).toPoint()
                        
            # if the lower edge of the specs is not visible, display specs above animal
            if not self.imageArea.rect().contains(bottom_left) and not self.imageArea.rect().contains(bottom_right):
                new_pos = pos + QtCore.QPoint(0,-self.widget_animal_specs.height() - self.cur_animal.boundingBox_visual.rect().height())
                self.widget_animal_specs.move(new_pos)
                
            # if the left edge of the specs is not visible, display specs right of animal
            elif not self.imageArea.rect().contains(bottom_left) and not self.imageArea.rect().contains(top_left):
                new_pos = pos + QtCore.QPoint(self.cur_animal.boundingBox_visual.rect().width(), -self.cur_animal.boundingBox_visual.rect().height())
                self.widget_animal_specs.move(new_pos)   
    
            # # if the top edge of the specs is not visible, display specs below of animal (as usual)
            # elif not self.imageArea.rect().contains(top_left) and not self.imageArea.rect().contains(top_right):
            #     pass
        
            # if the right edge of the specs is not visible, display specs left of animal
            elif not self.imageArea.rect().contains(bottom_right) and not self.imageArea.rect().contains(top_right):
                new_pos = pos + QtCore.QPoint(-self.widget_animal_specs.width(), -self.cur_animal.boundingBox_visual.rect().height())
                self.widget_animal_specs.move(new_pos)
            
     
    def updateBoundingBoxes(self):
        # remove bounding of other animals
        for animal in ANIMAL_LIST:
            self.imageArea._scene.removeItem(animal.boundingBox_visual)
            animal.boundingBox_visual = None

        # draw the current animal bounding box
        if self.cur_animal is not None and self.cur_animal in ANIMAL_LIST:
            self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(self.cur_animal.boundingBox, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
            
            self.widget_animal_specs.setAnimal(self.cur_animal)
            self.placeSpecsWidget()
            self.widget_animal_specs.show()
        else:
            self.widget_animal_specs.hide()
            
    def drawAnimalHead(self, animal):
        """ Draws the head of an animal. """
        if animal != None:
            if animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                animal.head_item_visual = QtWidgets.QGraphicsPixmapItem(animal.pixmap_head)
                animal.head_item_visual.setPos(animal.rect_head.center() - QtCore.QPoint(animal.pixmap_width/4, animal.pixmap_width/4))
                animal.head_item_visual.ItemIsMovable = True
                self.imageArea._scene.addItem(animal.head_item_visual)
                animal.is_head_drawn = True
     
    def drawAnimalLine(self, animal):
        """ Draws the line between head an tail of an animal. """
        animal.line_item_visual = self.imageArea._scene.addLine(animal.line, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
     
    def drawAnimalTailLineBoundingBox(self, animal):
        """ Draws the tail of an animal, the line betwen head and tail and 
        the bounding box around it. """
        
        if animal != None:
            if animal.position_tail != QtCore.QPoint(-1,-1):
                # draw the tail visual
                animal.tail_item_visual = QtWidgets.QGraphicsPixmapItem(animal.pixmap_tail)
                animal.tail_item_visual.setPos(animal.rect_tail.center() - QtCore.QPoint(animal.pixmap_width/4, animal.pixmap_width/4))
                animal.tail_item_visual.ItemIsMovable = True
                self.imageArea._scene.addItem(animal.tail_item_visual)
                
                # draw line and boundingbox visuals
                self.drawAnimalLine(animal)
                animal.boundingBox_visual = self.imageArea._scene.addRect(animal.boundingBox, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
                
                animal.is_tail_drawn = True
                
    def removeHeadVisual(self, animal):
        self.imageArea._scene.removeItem(animal.head_item_visual)
        animal.head_item_visual = None  

    def removeTailVisual(self, animal):
        self.imageArea._scene.removeItem(animal.tail_item_visual)
        animal.tail_item_visual = None  
    
    def removeLineVisual(self, animal):
        self.imageArea._scene.removeItem(animal.line_item_visual)
        animal.line_item_visual = None  

    def removeBoundingBoxVisual(self, animal):
        self.imageArea._scene.removeItem(animal.boundingBox_visual)
        animal.boundingBox_visual = None  
      
    def on_next_animal(self):
        # if no animal ist selected, then select first one
        if self.cur_animal is None and len(ANIMAL_LIST) >0:
            self.cur_animal = ANIMAL_LIST[0]          
            
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in ANIMAL_LIST:
            index = ANIMAL_LIST.index(self.cur_animal)
    
            # only go to next animal if there is another one
            if index < len(ANIMAL_LIST)-1:
                self.cur_animal = ANIMAL_LIST[index+1]
                self.updateBoundingBoxes()
                   
    def on_previous_animal(self):
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in ANIMAL_LIST:
            index = ANIMAL_LIST.index(self.cur_animal)
            
            # only go to previous animal, if there is one
            if index > 0:
                self.cur_animal = ANIMAL_LIST[index-1]
                self.updateBoundingBoxes() 

    def on_remove_animal(self):
        if(self.is_remove_mode_active):
            self.is_remove_mode_active = False
            
        elif self.is_add_mode_active:
            if not self.cur_animal or( self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                self.is_add_mode_active = False
                self.is_remove_mode_active = True
                
            else:
                self.displayErrorMsg("Error", "Please draw head and tail before switching off the Add-mode.", "Error")           
        else:
            self.is_add_mode_active = False
            self.is_remove_mode_active = True          

    def on_add_animal(self): 
        if(self.is_add_mode_active):
            # the add mode can only be deactivated when head and tail are drawn or none of them is drawn
            if self.cur_animal is not None:
                if (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn) or (not self.cur_animal.is_head_drawn and not self.cur_animal.is_tail_drawn):
                    self.is_add_mode_active = False
                else:
                    self.displayErrorMsg("Error", "Please draw head and tail before switching off the Add-mode.", "Error")
        else:
            self.is_remove_mode_active = False
            self.is_add_mode_active = True

    def displayErrorMsg(self, text, information, windowTitle):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(information)
        msg.setWindowTitle(windowTitle)
        msg.exec_()

    def mousePressEvent(self, event):
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        # enable dragging for current animal (when add mode is not active and the current animal is completey drawn)
        if self.cur_animal is not None and not self.is_add_mode_active:
            if(self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                if (2 * QtGui.QVector2D(pos - self.cur_animal.rect_head.center()).length()
                    < self.cur_animal.rect_head.width()):
                    self.drag_position_head = pos - self.cur_animal.position_head
                
                if(self.cur_animal.rect_tail.contains(pos)):
                    self.drag_position_tail = pos - self.cur_animal.position_tail
         
        if(self.is_remove_mode_active):
            # remove mode
            for animal in ANIMAL_LIST:
                if(animal.boundingBox.contains(pos)):
                    # get index of animal in list
                    index = ANIMAL_LIST.index(animal)
                         
                    # if the current animal is to be removed, find a new current animal
                    if(animal == self.cur_animal):
                        # if the index is not the last one, set the next animal as current animal
                        if index != len(ANIMAL_LIST)-1:
                            self.cur_animal = ANIMAL_LIST[index+1]
                        elif index == len(ANIMAL_LIST)-1 and len(ANIMAL_LIST)>1:
                            self.cur_animal = ANIMAL_LIST[index-1]
                        else:
                            self.cur_animal = None
                    
                    # remove animal visuals from scene
                    self.imageArea._scene.removeItem(animal.boundingBox_visual)
                    self.imageArea._scene.removeItem(animal.head_item_visual)
                    self.imageArea._scene.removeItem(animal.tail_item_visual)
                    self.imageArea._scene.removeItem(animal.line_item_visual)
                    
                    # remove animal from list
                    ANIMAL_LIST.remove(animal) 
                    break


        # if user is not removing and not adding animals, switch the current animal to what the user clicks on
        # if the user clicks on no organism, there is no current animal
        elif(not self.is_remove_mode_active and not self.is_add_mode_active):
            is_click_on_animal = False 
            for animal in ANIMAL_LIST:
                if(animal.boundingBox.contains(pos)):
                    self.cur_animal = animal
                    is_click_on_animal = True
                    break
            
            if not is_click_on_animal: self.cur_animal = None
            
                    
        elif(self.is_add_mode_active):
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
                    ANIMAL_LIST.append(self.cur_animal)
                else:
                    # create a new animal
                    self.cur_animal = Animal(position_head = pos)
                    self.cur_animal.setGroup(AnimalGroup.UNIDENTIFIED)
                              
                    # calculate position in original format
                    self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                    
                    # do the actual drawing of the head
                    self.drawAnimalHead(self.cur_animal)
 
            else:                
                # create a new animal
                self.cur_animal = Animal(position_head = pos)
                self.cur_animal.setGroup(AnimalGroup.UNIDENTIFIED)
                
                # calculate position in original format
                self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                
                # do the actual drawing of the head
                self.drawAnimalHead(self.cur_animal)

        self.updateBoundingBoxes()                     

    def mouseMoveEvent(self, event):
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        # if there is a head to draw and if the drag_position is within the widget, move the head
        if not self.drag_position_head.isNull() and self.imageArea.rect().contains(pos):         
            self.cur_animal.setPositionHead(pos - self.drag_position_head)
            # remove head on old position and draw it on the new position
            self.removeHeadVisual(self.cur_animal)
            self.removeLineVisual(self.cur_animal)
            self.drawAnimalHead(self.cur_animal)
            self.drawAnimalLine(self.cur_animal)
            
        # if there is a tail to draw and if the drag_position is within the widget, move the tail
        if not self.drag_position_tail.isNull() and self.imageArea.rect().contains(pos) and self.cur_animal is not None:
            self.cur_animal.setPositionTail(pos - self.drag_position_tail)
            
            # remove tail and line on old position and draw it on the new position
            self.removeTailVisual(self.cur_animal)
            self.removeLineVisual(self.cur_animal)  
            self.removeBoundingBoxVisual(self.cur_animal)
            self.drawAnimalTailLineBoundingBox(self.cur_animal)
         
        self.updateBoundingBoxes()    

    def mouseReleaseEvent(self, event):
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()

    def setOriginalWidthHeight(self, width=None, height=None):
        if width:
            self.original_img_width = width
        if height:
            self.original_img_height = height

    def updateAnimalPosition(self, animal):
        pos_h = QtCore.QPoint(-1, -1)
        pos_t = QtCore.QPoint(-1, -1)

        # transform coordinates of head and tail from original image to scene cooridnates
        pos_h.setX(round(animal.original_pos_head.x()*self.imageArea.width()/self.original_img_width))
        pos_h.setY(round(animal.original_pos_head.y()*self.imageArea.height()/self.original_img_height))
        
        pos_t.setX(round(animal.original_pos_tail.x()*self.imageArea.width()/self.original_img_width))
        pos_t.setY(round(animal.original_pos_tail.y()*self.imageArea.height()/self.original_img_height))
        
        animal.setPositionHead(pos_h)
        animal.setPositionTail(pos_t)

    def drawAnimalsFromList(self, animal_list, image_ending="_L"):
        """ Draws animals from a list on the current image. """
        for i in range(len(animal_list)):  
            # get the head and tail position form the list
            if image_ending=="*_L.jpg":
                original_pos_h = QtCore.QPoint(int(animal_list["LX1"].iloc[i]), int(animal_list["LY1"].iloc[i]))
                original_pos_t = QtCore.QPoint(int(animal_list["LX2"].iloc[i]), int(animal_list["LY2"].iloc[i]))
            elif image_ending == "*_R.jpg":
                original_pos_h = QtCore.QPoint(int(animal_list["RX1"].iloc[i]), int(animal_list["RY1"].iloc[i]))
                original_pos_t = QtCore.QPoint(int(animal_list["RX2"].iloc[i]), int(animal_list["RY2"].iloc[i]))   
            else:
                print("AnimalPainter: Error - no such image ending!")

            # only add an animal if there is a value for the coordinates
            if original_pos_h != QtCore.QPoint(-1, -1) and original_pos_t != QtCore.QPoint(-1, -1):
                # transform coordinates from original image to scene cooridnates
                pos_h = QtCore.QPoint(-1,-1)
                pos_h.setX(round(original_pos_h.x()*self.imageArea.width()/self.original_img_width))
                pos_h.setY(round(original_pos_h.y()*self.imageArea.height()/self.original_img_height))
                
                pos_t = QtCore.QPoint(-1,-1)
                pos_t.setX(round(original_pos_t.x()*self.imageArea.width()/self.original_img_width))
                pos_t.setY(round(original_pos_t.y()*self.imageArea.height()/self.original_img_height))
    
                animal_remark = str(animal_list["object_remarks"].iloc[i])
                if not animal_remark: animal_remark = ""       
        
                # create a new animal
                self.cur_animal = Animal(position_head = pos_h, 
                                          position_tail=pos_t,
                                          group=str(animal_list["group"].iloc[i]),
                                          species=str(animal_list["species"].iloc[i]),
                                          remark=animal_remark)
                
                # set the position in the original image     
                self.cur_animal.original_pos_head = original_pos_h
                self.cur_animal.original_pos_tail = original_pos_t
            
                # do the actual drawing of the head
                self.drawAnimalHead(self.cur_animal)
                self.drawAnimalTailLineBoundingBox(self.cur_animal)
                
                # append animal to list
                ANIMAL_LIST.append(self.cur_animal)   
                
                # update bounding boxes
                self.imageArea.animal_painter.updateBoundingBoxes()      
       
class PhotoViewer(QtWidgets.QWidget):
    """
    A photo viewer that contains a QGraphicsView to display the photos and 
    draw the animals on.
    """    
    newImageLoaded = QtCore.pyqtSignal(str)
    
    def __init__(self, models, imageDirectory, imagePrefix, resFilePath="", imageEnding="*_L.jpg", parent=None):
        super(PhotoViewer, self).__init__(parent)

        # data models
        self.models = models

        # image directory and prefix (needed for retrieving the image_list)
        self.image_directory = imageDirectory
        self.image_prefix = imagePrefix
        self.image_ending = imageEnding
        self.res_file_path = resFilePath

        # list of image pathes and the current image index
        self.cur_image_index = 0
        self.image_list = glob.glob(imageDirectory + imagePrefix + imageEnding)
        #self.res_file = None
        self.loadResFile()

        # initalize gui and actions
        self.init_ui()
        self.init_actions()
        
        # load initial image
        #self.loadImage(self.image_list[self.cur_image_index])
        #self.layout.invalidate()
        #self.layout.activate()
    
    
    def loadResFile(self):
        if ntpath.exists(self.res_file_path):
            res_file = pd.read_excel(self.res_file_path)
            self.models.model_animals.update(res_file)
            #self.image_list = self.res_file["file_id"].unique() + "_L.jpg"
        
            # self.cur_image_index = 0
            # if len(self.image_list) == 0:
            #     self.loadImage(path=None)
            # else:               
            #     self.loadImage(self.image_directory + self.image_list[self.cur_image_index])
        
    def setResFilePath(self, text):
        self.res_file_path = text
        self.loadResFile()
    
    def setImageDir(self, text):
        self.image_directory = text
        self.cur_image_index = 0
        # if len(self.image_list) == 0:
        #     self.loadImage(path=None)
        # else:
        #     self.loadImage(self.image_directory + self.image_list[self.cur_image_index])
        self.updateImageList()
        
    def setImagePrefix(self, text):
        self.image_prefix = text
        self.updateImageList()
        
    def setImageEnding(self, text):
        self.image_ending = text
        self.updateImageList()

    def activateLRMode(self, activateLRMode=False):
        pass

    def updateImageList(self):
        #self.cur_image_index = 0
        self.image_list = glob.glob(self.image_directory + self.image_prefix + self.image_ending)
        
        if not self.image_list:
            self.loadImage(path=None)
        else:
            
            self.loadImage(self.image_list[self.cur_image_index])

    def resizeEvent(self, event):
        super().resizeEvent(event)
        #print("resize in photo viewer")
        if self.cur_image_index < len(self.image_list):
            # reload photo
            path = self.image_list[self.cur_image_index]
            photo = QtGui.QPixmap(path).scaled(QtCore.QSize(self.imageArea.width(), self.imageArea.height()))
            self.imageArea.setPhoto(photo)
            self.updateImageCountVisual()
        
        # remove animals
        self.imageArea.animal_painter.removeAll()
        
        # redraw animals
        for animal in ANIMAL_LIST:
            # update positions
            #print(animal.position_head)
            self.imageArea.animal_painter.updateAnimalPosition(animal)#, self.imageArea.img_width, self.imageArea.img_height)
        
            # redraw animals
            self.imageArea.animal_painter.drawAnimalHead(animal)
            self.imageArea.animal_painter.drawAnimalTailLineBoundingBox(animal)
            
            #print(animal.position_head)
        
        self.imageArea.animal_painter.updateBoundingBoxes()

        # self.imageArea.img_width = self.imageArea.width()
        # self.imageArea.img_height = self.imageArea.height()     
        
        
 

        # # update animal list
        # # ANIMAL_LIST.clear()
        
        # # find current image in result file and draw all animals from it
        # if self.res_file is not None:
        #     cur_file_entries = self.res_file[self.res_file['file_id'] ==  ntpath.basename(path)[:-6]]
        #     self.imageArea.animal_painter.drawAnimalsFromList(cur_file_entries, self.image_ending)
            
        #     self.imageArea.animal_painter.cur_animal = None
        #     self.imageArea.animal_painter.updateBoundingBoxes()

        # print()

    def loadImage(self, path):
        if path:
            image = QtGui.QImage(path)
            photo = QtGui.QPixmap().fromImage(image).scaled(QtCore.QSize(self.imageArea.width(), self.imageArea.height()))
            self.imageArea.animal_painter.setOriginalWidthHeight(width=image.width(), height = image.height())
        else:
            photo = None
        
        self.imageArea.setPhoto(photo)
        self.updateImageCountVisual()
        
        # clear visuals
        self.imageArea.animal_painter.removeAll()
        
        # update animal list
        ANIMAL_LIST.clear()
        
        # find current image in result file and draw all animals from it
        if self.models.model_animals is not None and path is not None:
            cur_file_entries = self.models.model_animals[self.models.model_animals['file_id'] ==  ntpath.basename(path)[:-6]]
            self.imageArea.animal_painter.drawAnimalsFromList(cur_file_entries, self.image_ending)       
            if len(cur_file_entries) > 0: 
                remark = str(cur_file_entries['image_remarks'].iloc[0])
                if remark == "nan": remark = ""
                self.newImageLoaded.emit(remark)
            
        # reset current animal, hide specs widget and update bounding boxes (none should be drawn since cur_animal is None)
        self.imageArea.animal_painter.cur_animal = None
        self.imageArea.animal_painter.widget_animal_specs.hide()
        self.imageArea.animal_painter.updateBoundingBoxes() 
    
    def on_next_image(self):
        # if there is a next image, load it
        if self.cur_image_index < len(self.image_list) - 1:
            # get the new image and load it
            path = self.image_list[self.cur_image_index+1]
            self.cur_image_index = self.cur_image_index + 1        
            self.loadImage(path)
       
    def on_previous_image(self):
        # if there is a previous image, load it
        if self.cur_image_index > 0:
            path = self.image_list[self.cur_image_index-1]
            self.cur_image_index = self.cur_image_index - 1
            self.loadImage(path) 


    def updateImageCountVisual(self):
        num_images = len(self.image_list)
        cur_image = self.cur_image_index
        self.label_imgCount.setText(str(cur_image+1) + "/" + str(num_images))

    def init_actions(self):
        # connect buttons
        self.btn_previous_image.clicked.connect(self.on_previous_image)
        self.btn_next_image.clicked.connect(self.on_next_image)

        # --- define shortcuts ------------------------------------------------------------------------------------------- #  
        self.shortcut_previous_image = QtWidgets.QShortcut(QtGui.QKeySequence("left"), self.btn_previous_image, self.on_previous_image)
        self.shortcut_next_image = QtWidgets.QShortcut(QtGui.QKeySequence("right"), self.btn_next_image, self.on_next_image) 

    # enable or disable arrow key shortcuts
    def setArrowShortcutsActive(self, are_active):
        self.shortcut_previous_image.setEnabled(are_active)
        self.shortcut_next_image.setEnabled(are_active)
              
        
    def init_ui(self):
        # --- left frame ------------------------------------------------------------------------------------------- # 
        # frame
        frame_left = QtWidgets.QFrame(self)
        frame_left.setMinimumSize(QtCore.QSize(60, 0))
        frame_left.setMaximumSize(QtCore.QSize(60, 16777215))
        frame_left.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_left.setObjectName("frame_left")
  
        # layout
        layout_frame_left = QtWidgets.QVBoxLayout(frame_left)
        layout_frame_left.setContentsMargins(5, 5, 5, 0)
        layout_frame_left.setObjectName("layout_frame_left")
        
        # vertical spacers
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
 
        # button for previous image
        self.btn_previous_image = QtWidgets.QPushButton(frame_left)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_previous_image.sizePolicy().hasHeightForWidth())
        self.btn_previous_image.setSizePolicy(sizePolicy)
        self.btn_previous_image.setIcon(get_icon(":/icons/icons/arrow_left_big.png"))
        self.btn_previous_image.setIconSize(QtCore.QSize(20, 40))
        self.btn_previous_image.setCheckable(False)
        self.btn_previous_image.setFlat(False)
        self.btn_previous_image.setObjectName("btn_previous_image")

        # label to display image count
        self.label_imgCount = QtWidgets.QLabel(frame_left)
        self.label_imgCount.setMinimumSize(QtCore.QSize(0, 40))
        self.label_imgCount.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_imgCount.setAlignment(QtCore.Qt.AlignCenter)
        self.label_imgCount.setObjectName("label_imgCount")
        self.label_imgCount.setStyleSheet("font:10pt 'Century Gothic'")
        
        # add widgets to layout
        layout_frame_left.addItem(spacerItem7)
        layout_frame_left.addWidget(self.btn_previous_image)
        layout_frame_left.addItem(spacerItem8)
        layout_frame_left.addWidget(self.label_imgCount)
        
        
        # --- image frame ------------------------------------------------------------------------------------------- # 
        # # frame
        # self.frame_image = QtWidgets.QFrame(self)
        # # frame_image.setMinimumSize(QtCore.QSize(60, 0))
        # # frame_image.setMaximumSize(QtCore.QSize(60, 16777215))
        # self.frame_image.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.frame_image.setObjectName("frame_image")
    
        # # layout
        # self.layout_frame_image = QtWidgets.QGridLayout(self.frame_image)
        # self.layout_frame_image.setContentsMargins(0, 0, 0, 0)
        # self.layout_frame_image.setObjectName("layout_frame_image")



        
        self.imageArea = ImageArea(self.models, self)
        # self.imageAreaR = ImageArea(self)
        
        # self.label_dummy = QtWidgets.QLabel()
        
        # self.layout_frame_image.addWidget(self.imageArea, 0, 0, 1, 1)
        # self.layout_frame_image.addWidget(self.imageAreaR, 1, 0, 1, 1)
        # self.layout_frame_image.addWidget(self.label_dummy, 1, 1, 1, 1)


        
        # --- group and species frame ------------------------------------------------------------------------------------------- # 
        # @todo idea:frame with 2 listwidgets below each other. one for the group, one for species. 
        
        
        # --- right frame ------------------------------------------------------------------------------------------- # 
        # frame
        frame_right = QtWidgets.QFrame(self)
        frame_right.setMinimumSize(QtCore.QSize(60, 0))
        frame_right.setMaximumSize(QtCore.QSize(60, 16777215))
        frame_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_right.setObjectName("frame_right")
        
        # vertical spacers
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        # button for previous image
        self.btn_next_image = QtWidgets.QPushButton(frame_right)      
        self.btn_next_image.setIcon(get_icon(":/icons/icons/arrow_right_big.png"))
        self.btn_next_image.setIconSize(QtCore.QSize(20, 40))
        self.btn_next_image.setObjectName("btn_next_image")
        
        # button for opening image in separate window
        self.btn_openImg = QtWidgets.QPushButton(frame_right)
        self.btn_openImg.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_openImg.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_openImg.setIcon(get_icon(":/icons/icons/open_image.png"))
        self.btn_openImg.setIconSize(QtCore.QSize(30, 30))
        self.btn_openImg.setObjectName("btn_openImg")
        
        # layout
        layout_frame_right = QtWidgets.QVBoxLayout(frame_right)
        layout_frame_right.setContentsMargins(5, 5, 5, 0)
        layout_frame_right.setObjectName("layout_frame_right")
        
        # add widgets to layout
        layout_frame_right.addItem(spacerItem9)
        layout_frame_right.addWidget(self.btn_next_image)
        layout_frame_right.addItem(spacerItem10)
        layout_frame_right.addWidget(self.btn_openImg)
        
        # --- main widget ------------------------------------------------------------------------------------------- #      
        # main layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("layout")
        
        # adding widgets to main layout 
        self.layout.addWidget(frame_left)
        self.layout.addWidget(self.imageArea)
        self.layout.addWidget(frame_right)

        # set main layout
        self.layout = self.layout
        