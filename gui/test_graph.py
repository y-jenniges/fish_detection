#https://stackoverflow.com/questions/60571837/how-to-move-a-figurecreated-using-paintevent-by-simply-draging-it-in-pyqt5

from PyQt5 import QtCore, QtGui, QtWidgets
from Models import AnimalGroup, AnimalSpecies


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
        





class MeasurementWidget(QtWidgets.QWidget):
    """
    Custom Qt Widget to be used for adding/removing/displaying the heads 
    and tails of animals.
    """

    def __init__(self, parent=None):
        super(MeasurementWidget, self).__init__(parent)
        #self.parent = parent
        
        #self.setLayout(self.horizontalLayout)
        self.setMinimumSize(200,200)
        

        # dragging offset when moving the markings for head and/or tail
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()

        # indicate if head/tail is already created
        self.is_head_drawn = False
        self.is_tail_drawn = False
        
        # current animal
        self.cur_animal  = None
        
        # animal list
        self.animals = []
        
        # variables to control what interactions are possible
        self.is_add_mode_active = False
        self.is_remove_mode_active = False

        # current image
        #self.current_image_pixmap = QtGui.QPixmap("../data/maritime_dataset_25/training_data_animals/0.jpg")
        self.pixmap = QtGui.QPixmap("../data/maritime_dataset_25/training_data_animals/0.jpg")        
        #self.pixmap.scaled(QtCore.QSize(self.width(), self.height()))

        self.setStyleSheet("background: no-repeat")
        # zoom
        self.zoom = 1
        self.scale_offset = [0.0, 0.0]
        self.cur_width = self.width()
        self.cur_height = self.height()
        
        
        self.min_width = self.width()
        self.min_height = self.height()
        self.max_width = self.width()*10
        self.max_height = self.height()*10
        
        

    # @todo it is very slow
    # def get_line_to_draw(self, animal):
    #     # calucalte intersection points of the circle (of animal head) and the line connecting the circle and the cross (for animal tail)
    #     p1 = sympy.geometry.Point2D(animal.line.p1().x(), animal.line.p1().y())
    #     p2 = sympy.geometry.Point2D(animal.line.p2().x(), animal.line.p2().y())
    #     sym_circle = sympy.geometry.Circle(p1, animal.pixmap_width/2)
    #     sym_line = sympy.geometry.Line(p1, p2)
    #     intersection = sympy.geometry.intersection(sym_circle, sym_line)
        
    #     # use the intersection point to draw the line such that it stops at the edge of the circle (and does not intersecti with it)
    #     if intersection[0].x <= p1.x and p2.x <= p1.x:
    #         return QtCore.QLine(animal.line.p2(), QtCore.QPoint(intersection[0].x, intersection[0].y))
    #     else:
    #         return QtCore.QLine(QtCore.QPoint(intersection[1].x, intersection[1].y), animal.line.p2()) 
        
        # alternatively, simply return the original line
        #return animal.line)

    

    def paintEvent(self, event):
        super().paintEvent(event)    
        print("paint")
        # define painter
        painter = QtGui.QPainter(self)
        #painter = QtGui.QPainter(self.parent)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
    
        # draw background      
        pix = self.pixmap.scaled(QtCore.QSize(self.width(), self.height()))
        painter.fillRect(self.rect(), QtGui.QBrush(pix))
    
        # draw all animals in the list
        for animal in self.animals:
            painter.drawPixmap(animal.rect_head, animal.pixmap_head)
            painter.drawPixmap(animal.rect_tail, animal.pixmap_tail)
            
            # draw a line that is not displayed within the circle representing the head
            painter.setPen(QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))  
            painter.drawLine(animal.line)
                   
            painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0,0), 2, QtCore.Qt.SolidLine)) 
            painter.drawRoundedRect(animal.boundingBox, 10, 10)

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
        
        # draw the current animal with it s bounding box
        if self.cur_animal is not None:
            if self.cur_animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                painter.drawPixmap(self.cur_animal.rect_head, self.cur_animal.pixmap_head)
                #self.parent._scene.addPixmap(self.cur_animal.rect_head, self.cur_animal.pixmap_head)
                 
            if self.cur_animal.position_tail != QtCore.QPoint(-1,-1):
                # draw the tail visual
                painter.drawPixmap(self.cur_animal.rect_tail, self.cur_animal.pixmap_tail)
                
                painter.setPen(QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
                painter.drawLine(self.cur_animal.line)#self.get_line_to_draw(self.cur_animal))
                painter.drawRoundedRect(self.cur_animal.boundingBox, 10, 10)
         


    def mousePressEvent(self, event):
        
        if(self.is_head_drawn and self.is_tail_drawn and self.cur_animal is not None):
           if (2 * QtGui.QVector2D(event.pos() - self.cur_animal.rect_head.center()).length()
               < self.cur_animal.rect_head.width()):
               self.drag_position_head = event.pos() - self.cur_animal.position_head
            
           if(self.cur_animal.rect_tail.contains(event.pos())):
               self.drag_position_tail = event.pos() - self.cur_animal.position_tail
         
        if(self.is_remove_mode_active):
            for animal in self.animals:
                if(animal.boundingBox.contains(event.pos())):
            
                    index = self.animals.index(animal)
                         
                    # if the current animal is to be removed, find a new current animal
                    if(animal == self.cur_animal):
                        # if the index is not the last one, set the next animal as current animal
                        if index != len(self.animals)-1:
                            self.cur_animal = self.animals[index+1]
                        elif index == len(self.animals)-1 and len(self.animals)>1:
                            self.cur_animal = self.animals[index-1]
                        else:
                            self.cur_animal = None
                    
                    self.animals.remove(animal) 

        # if user is not removing and not adding animals, switch the current animal to what the user clicks on
        elif(not self.is_remove_mode_active and not self.is_add_mode_active):
             for animal in self.animals:
                if(animal.boundingBox.contains(event.pos())):
                    self.cur_animal = animal
                    break
                    
        elif(self.is_add_mode_active):
            if(self.is_head_drawn and not self.is_tail_drawn):
                # adapt the tail position of the current animal
                self.cur_animal.setPositionTail(event.pos())
                
                 # tail is now defined and will be drawn
                self.is_tail_drawn = True
                
                # add animal to list
                self.animals.append(self.cur_animal)
                
                
            elif(not self.is_head_drawn):
                # create a new animal
                self.cur_animal = Animal(position_head = event.pos())
                self.cur_animal.setGroup(AnimalGroup.FISH)
                
                # head is now defined and will be drawn 
                self.is_head_drawn = True
                
            else:
                # create a new animal
                self.cur_animal = Animal(position_head = event.pos())
                self.cur_animal.setGroup(AnimalGroup.FISH)
                
                # head is now defined and will be drawn 
                self.is_head_drawn = True
                self.is_tail_drawn = False

        self.update()
                      
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # if there is a head to draw and if the drag_position is within the widget, move the head
        if self.cur_animal != None and not self.drag_position_head.isNull() and self.rect().contains(event.pos()):         
            self.cur_animal.setPositionHead(event.pos() - self.drag_position_head)
            
        # if there is a tail to draw and if the drag_position is within the widget, move the tail
        if self.cur_animal != None and not self.drag_position_tail.isNull() and self.rect().contains(event.pos()):
            self.cur_animal.setPositionTail(event.pos() - self.drag_position_tail)
            
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()
        super().mouseReleaseEvent(event)

    def on_next_animal(self):
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in self.animals:
            index = self.animals.index(self.cur_animal)
    
            # only go to next animal if there is another one
            if index < len(self.animals)-1:
                self.cur_animal = self.animals[index+1]
                self.update()
        
    def on_previous_animal(self):
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in self.animals:
            index = self.animals.index(self.cur_animal)
            
            # only go to previous animal, if there is one
            if index > 0:
                self.cur_animal = self.animals[index-1]
                self.update()

    def on_remove_animal(self):
        if(self.is_remove_mode_active):
            self.is_remove_mode_active = False
        else:
            self.is_add_mode_active = False
            self.is_remove_mode_active = True          

    def on_add_animal(self):       
        if(self.is_add_mode_active):
            # the add mode can only be deactivated when head and tail are drawn
            if (self.is_head_drawn and self.is_tail_drawn):
                self.is_add_mode_active = False
            else:
                print("Error: Please draw head and tail before switching of the Add-mode.")
        else:
            self.is_remove_mode_active = False
            self.is_add_mode_active = True

    def setZoom(self, zoom, width, height):
        self.zoom = zoom
        new_size = QtCore.QSize(width+(self.max_width - width)/100.0*zoom, height+(self.max_height - height)/100.0*zoom)
        self.resize(new_size)
        self.update()


# class MyWindow(QtWidgets.QMainWindow):
    
#     def setupUi(self, MainWindow):

#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(1244, 822)
        
#         # create central widget
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.horizontalLayout_15 = QtWidgets.QVBoxLayout(self.centralwidget)
#         self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
#         self.horizontalLayout_15.setObjectName("horizontalLayout_15")



#         # create widgets and gui objects
#         self.measurementWidget = MeasurementWidget()    
#         button_add = QtWidgets.QPushButton('Add')
#         button_remove = QtWidgets.QPushButton('Remove')
#         button_next = QtWidgets.QPushButton('Next')
#         button_previous = QtWidgets.QPushButton('Previous')
        
#         self.scrollArea = QtWidgets.QScrollArea()
#         self.scrollArea.setWidget(self.measurementWidget)
#         self.scrollArea.setVisible(True)
#         self.scrollArea.setWidgetResizable(True)
        
#         self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Horizontal)
#         self.slider_zoom.setMaximum(100)
                 
#         # add objects to layout
#         self.horizontalLayout_15.addWidget(button_add)
#         self.horizontalLayout_15.addWidget(button_remove)
#         self.horizontalLayout_15.addWidget(button_next)
#         self.horizontalLayout_15.addWidget(button_previous)
#         self.horizontalLayout_15.addWidget(self.slider_zoom)
#         self.horizontalLayout_15.addWidget(self.scrollArea)
               
#         MainWindow.setCentralWidget(self.centralwidget)       
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
#         # connect signals and slots      
#         button_add.clicked.connect(self.measurementWidget.on_add_animal)
#         button_remove.clicked.connect(self.measurementWidget.on_remove_animal)
#         button_next.clicked.connect(self.measurementWidget.on_next_animal)
#         button_previous.clicked.connect(self.measurementWidget.on_previous_animal)
#         self.slider_zoom.valueChanged.connect(self.on_slider_zoom)

#     def on_slider_zoom(self):
#         print(f"slider {self.slider_zoom.value()}")
#         self.scrollArea.setWidgetResizable(False)
#         self.measurementWidget.setZoom(self.slider_zoom.value(), self.scrollArea.width(), self.scrollArea.height())
#         self.scrollArea.horizontalScrollBar().setStyleSheet("QScrollBar {height:20px;}");
#         self.scrollArea.verticalScrollBar().setStyleSheet("QScrollBar {width:20px;}");
#         if self.slider_zoom.value() == 0:
#             self.scrollArea.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}");
#             self.scrollArea.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}");
        
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = MyWindow(MainWindow)
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

