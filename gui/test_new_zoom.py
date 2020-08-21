# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
import glob

from test_graph import Animal, AnimalGroup, AnimalSpecies
from Helpers import get_icon

IMAGE_DIRECTORY = "../data/maritime_dataset_25/training_data_animals/"
IMAGE_PREFIX = ""
ANIMAL_LIST = []
ANIMAL_REMARKS = ["", "Not determined",  "Animal incomplete"]
IMAGE_REMARKS = []

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


"""
A widget to provide all information of the current animal
"""
class AnimalSpecificationsWidget(QtWidgets.QWidget):
    def __init__ (self, parent = None):
        super(QtWidgets.QWidget, self).__init__(parent)
        
        self.group = AnimalGroup.UNIDENTIFIED.name.title()
        self.species = AnimalSpecies.A.name.title()
        self.remark = ""
        self.length = 0
        
        self.init_ui()
        
        ANIMAL_REMARKS = ["", "Not determined",  "Animal incomplete"]
        group_icon_list = [":/animal_markings/animal_markings/square_blue.png", 
                           ":/animal_markings/animal_markings/square_red.png", 
                           ":/animal_markings/animal_markings/square_orange.png", 
                           ":/animal_markings/animal_markings/square_black.png", 
                           ":/animal_markings/animal_markings/square_gray.png"]
        
        
        self.model_group = self.comboBox_group.model()#GroupItemModel()#combo.model()
        index = 0
        for group in AnimalGroup:
            icon = QtGui.QIcon(group_icon_list[index])
            
            item = QtGui.QStandardItem(str(group.name.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            item.setIcon(icon)
            self.model_group.appendRow(item)
            index += 1
       # self.comboBox_group.setModel(model)
       
        self.model_species = self.comboBox_species.model()#GroupItemModel()#combo.model()
        for species in AnimalSpecies:
            item = QtGui.QStandardItem(str(species.name.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.model_species.appendRow(item)
       # self.comboBox_group.setModel(model)
       
        self.model_remarks = self.comboBox_remark.model()#GroupItemModel()#combo.model()
        for remark in ANIMAL_REMARKS:
            item = QtGui.QStandardItem(str(remark.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.model_remarks.appendRow(item)
       # self.comboBox_group.setModel(model)
       
        # setting visuals to initial values and hiding widget
        self.updateVisuals()
        self.hide()
        
        # set tab sequence
        self.setTabOrder(self.comboBox_group, self.comboBox_species)
        self.setTabOrder(self.comboBox_species, self.comboBox_remark)
        self.setTabOrder(self.comboBox_remark, self.spinBox_length)
        
        # connecting signals and slots
        self.spinBox_length.valueChanged.connect(self.on_length_spinbox_changed)
        self.comboBox_group.currentTextChanged.connect(self.on_group_combobox_changed)
        self.comboBox_species.currentTextChanged.connect(self.on_species_combobox_changed)
        self.comboBox_remark.currentTextChanged.connect(self.on_remark_combobox_changed)
        self.comboBox_remark.lineEdit().editingFinished.connect(self.on_remark_combobox_edited)
      
    def on_remark_combobox_edited(self):
        text = self.comboBox_remark.currentText()
        
        # if the text is not yet in the combobox, add it
        if self.comboBox_remark.findText(text) == -1:
            item = QtGui.QStandardItem(str(text.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.model_remarks.appendRow(item)
            self.focusNextChild()
      
    def on_remark_combobox_changed(self, remark):
        self.parent().animal_painter.setAnimalRemark(remark)
        
    def on_species_combobox_changed(self, species):
        if self.comboBox_species.findText(species) != -1:
            self.species = species
            self.parent().animal_painter.setAnimalSpecies(species) #setAnimalGroup(group) 
            self.focusNextChild()
        else:
            print("Given species was not in combobox")
            
    def on_group_combobox_changed(self, group):
        if self.comboBox_group.findText(group) != -1:
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
            self.remark = animal.remark
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
        elif self.remark != "" and self.remark is not None:
            print("adding new remark entry")
            item = QtGui.QStandardItem(str(self.remark))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.model_remarks.appendRow(item)
        
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


"""
An implementation of QGraphicsView to enable painting of animals on a photo as well as loading of photos. Moreover, it provides a wheel zoom functionality.
"""
class ImageArea(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(ImageArea, self).__init__(parent)
        
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
        self.animal_painter = AnimalPainter(self)


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
            self._empty = False
            #self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView() 
        
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

"""
Class providing the logic for adding/removing/moving and jumping between animals. It needs a QGraphicsView that it can paint on and that delegates the mouse events to the AnimalPainter.
"""
class AnimalPainter():
    def __init__(self, imageArea):

        # dragging offset when moving the markings for head and/or tail
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()

        # indicate if head/tail is already created
        self.is_head_drawn = False
        self.is_tail_drawn = False
        
        # current animal
        self.cur_animal  = None
        self.widget_animal_specs = AnimalSpecificationsWidget(imageArea)
        
        # variables to control what interactions are possible
        self.is_add_mode_active = False
        self.is_remove_mode_active = False
        
        # the QGraphicsView to paint on
        self.imageArea = imageArea
    
    
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
     
    # function to move to specs widget with the bounding bos of the current animal (and prevent it from getting out of the borders of the image)
    def placeSpecsWidget(self):
        if self.cur_animal is not None:
            # reset position of specs widget
            self.widget_animal_specs.move(0,0)
        
            # get position of current bounding box from scene
            pos = self.imageArea.mapFromScene(self.cur_animal.boundingBox_visual.rect().bottomLeft().toPoint())
            
            # move the zoom widget a bit below the button position and center it below the button
            self.widget_animal_specs.move(pos)
        
            # get corners of specs widget in scne coordinates
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
        if animal != None:
            if self.cur_animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                self.cur_animal.head_item_visual = QtWidgets.QGraphicsPixmapItem(self.cur_animal.pixmap_head)
                self.cur_animal.head_item_visual.setPos(self.cur_animal.rect_head.center() - QtCore.QPoint(self.cur_animal.pixmap_width/4, self.cur_animal.pixmap_width/4))
                self.cur_animal.head_item_visual.ItemIsMovable = True
                self.imageArea._scene.addItem(self.cur_animal.head_item_visual)
     
    def drawAnimalLine(self, animal):
        animal.line_item_visual = self.imageArea._scene.addLine(animal.line, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
     
    def drawAnimalTailLineBoundingBox(self, animal):
        if animal != None:
            if self.cur_animal.position_tail != QtCore.QPoint(-1,-1):
                # draw the tail visual
                self.cur_animal.tail_item_visual = QtWidgets.QGraphicsPixmapItem(self.cur_animal.pixmap_tail)
                self.cur_animal.tail_item_visual.setPos(self.cur_animal.rect_tail.center() - QtCore.QPoint(self.cur_animal.pixmap_width/4, self.cur_animal.pixmap_width/4))
                self.cur_animal.tail_item_visual.ItemIsMovable = True
                self.imageArea._scene.addItem(self.cur_animal.tail_item_visual)
                
                # draw line and boundingbox visuals
                self.drawAnimalLine(self.cur_animal)#cur_animal.line_item_visual = self.imageArea._scene.addLine(self.cur_animal.line, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
                self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(self.cur_animal.boundingBox, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
                
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
            if (self.is_head_drawn and self.is_tail_drawn):
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
            if (self.is_head_drawn and self.is_tail_drawn) or (not self.is_head_drawn and not self.is_tail_drawn):
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
        if(self.is_head_drawn and self.is_tail_drawn and self.cur_animal is not None and not self.is_add_mode_active):
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
            # add mode
            if(self.is_head_drawn and not self.is_tail_drawn):
                # adapt the tail position of the current animal
                self.cur_animal.setPositionTail(pos)
                
                # do the actual drawing
                self.drawAnimalTailLineBoundingBox(self.cur_animal)
                
                # tail is now defined and will be drawn
                self.is_tail_drawn = True
                
                # add animal to list
                ANIMAL_LIST.append(self.cur_animal)
                
 
            else:                
                # create a new animal
                self.cur_animal = Animal(position_head = pos)
                self.cur_animal.setGroup(AnimalGroup.UNIDENTIFIED)
                               
                # do the actual drawing of the head
                self.drawAnimalHead(self.cur_animal)
                
                # head is now drawn
                self.is_head_drawn = True
                self.is_tail_drawn = False
                            
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
        if not self.drag_position_tail.isNull() and self.imageArea.rect().contains(pos):
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


"""
A photo viewer that contains a QGraphicsView to display the photos and draw the animals on.
"""              
class PhotoViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PhotoViewer, self).__init__(parent)

        # list of image pathes and the current image index
        self.cur_image_index = 0
        self.image_list = glob.glob(IMAGE_DIRECTORY + IMAGE_PREFIX + "*.jpg")

        # initalize gui
        self.init_ui()
        
        # initalize actions
        self.init_actions()
        
        # load initial image
        #self.loadImage(self.image_list[self.cur_image_index])


    def resizeEvent(self, event):
        super().resizeEvent(event)
        path = self.image_list[self.cur_image_index]
        photo = QtGui.QPixmap(path).scaled(QtCore.QSize(self.imageArea.width(), self.imageArea.height()))
        self.imageArea.setPhoto(photo)
        self.updateImageCountVisual()
        #self.loadImage(self.image_list[self.cur_image_index])
                
    def loadImage(self, path):
        photo = QtGui.QPixmap(path).scaled(QtCore.QSize(self.imageArea.width(), self.imageArea.height()))
        self.imageArea.setPhoto(photo)
        self.updateImageCountVisual()
        
        # clear visuals
        self.imageArea.animal_painter.removeAll()
        
        # hide animal specs widget
        self.imageArea.animal_painter.widget_animal_specs.hide()
        
        # clear animal list
        ANIMAL_LIST.clear()
  
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
        
        # layout
        layout_frame_left = QtWidgets.QVBoxLayout(frame_left)
        layout_frame_left.setContentsMargins(5, 5, 5, 0)
        layout_frame_left.setObjectName("layout_frame_left")
        
        # add widgets to layout
        layout_frame_left.addItem(spacerItem7)
        layout_frame_left.addWidget(self.btn_previous_image)
        layout_frame_left.addItem(spacerItem8)
        layout_frame_left.addWidget(self.label_imgCount)
        
        
        # --- image frame ------------------------------------------------------------------------------------------- # 
        self.imageArea = ImageArea(self)
        #self.imageArea.setStyleSheet("background-color:red;")
        
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
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setObjectName("layout")
        
        # adding widgets to main layout 
        layout.addWidget(frame_left)
        layout.addWidget(self.imageArea)
        layout.addWidget(frame_right)

        # set main layout
        self.layout = layout
        

        


class MyWindow(QtWidgets.QMainWindow):
    
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1244, 822)
        
        self.photo_viewer = PhotoViewer()
        
        # create central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # create widgets and gui objects 
        button_add = QtWidgets.QPushButton('Add')
        button_remove = QtWidgets.QPushButton('Remove')
        button_next = QtWidgets.QPushButton('Next')
        button_previous = QtWidgets.QPushButton('Previous')
        
        self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_zoom.setMaximum(100)
        self.slider_zoom.setMinimum(0)
                 
        # add objects to layout
        self.horizontalLayout.addWidget(button_add)
        self.horizontalLayout.addWidget(button_remove)
        self.horizontalLayout.addWidget(button_next)
        self.horizontalLayout.addWidget(button_previous)
        self.horizontalLayout.addWidget(self.slider_zoom)
        self.horizontalLayout.addWidget(self.photo_viewer)
  
        MainWindow.setCentralWidget(self.centralwidget)       
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # define gui actions
        self.slider_zoom.valueChanged.connect(self.onValueChanged)
        button_add.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_add_animal)
        button_remove.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_remove_animal)
        button_next.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_next_animal)
        button_previous.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_previous_animal)
       
        self.slider_max = self.photo_viewer.imageArea.width()*10
        self.slider_min = self.photo_viewer.imageArea.width()
        self.factor = 50*(self.slider_max - self.slider_min)/(self.slider_max)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     self.slider_max = self.photo_viewer.imageArea.width()*10
    #     self.slider_min = self.photo_viewer.imageArea.width()
    #     self.factor = 1*(self.slider_max - self.slider_min)/(1*self.slider_max)
            
        
    def onValueChanged(self, value):
        scale = 1 + value*self.factor/100
        self.photo_viewer.imageArea.setTransform(self.photo_viewer.imageArea.transform().fromScale(scale, scale))

        if value < 1:
            self.photo_viewer.imageArea.resetTransform() 
            self.photo_viewer.imageArea.fitInView()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())