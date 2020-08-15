#https://stackoverflow.com/questions/60571837/how-to-move-a-figurecreated-using-paintevent-by-simply-draging-it-in-pyqt5
import random
import sys
import enum

from PyQt5 import QtCore, QtGui, QtWidgets

# dict contains all animals on that image
animal_list = []

# map to assign a color to an animal group
animal_color_map = 1

class AnimalGroup(enum.Enum):
    FISH = 1, 
    CRUSTACEA = 2,
    CHAETOGNATHA = 3, 
    JELLYFISH = 4, 
    UNIDENTIFIED = 5

class AnimalSpecies(enum.Enum):
    A = 2,
    B = 3,
    UNIDENTIFIED = 1

class AnimalSpeciesClass:
    def add_species():
        print("add species")
    
    def remove_species():
        print("remove species")



class AnimalVisualRepresentation():
     def __init__(self):
         print("aha")



"""
Class to represent an animal on an image.
"""
class Animal():
# the input position refers to the center of the visual!
    def __init__(self, position_head=QtCore.QPoint(-1,-1), position_tail=QtCore.QPoint(-1,-1), group=AnimalGroup.UNIDENTIFIED, species=AnimalSpecies.UNIDENTIFIED, remark=""):
                
        # size of the head/tail visuals
        self.pixmap_width = 50
        
        self.position_head = position_head
        self.position_tail = position_tail
        self.group = group
        self.species = species
        self.remark = remark
        self.length = None
        self.width = None
      
        # set the visual for the head, tail and line between them
        pos_visual_head = position_head - QtCore.QPoint(self.pixmap_width/2, self.pixmap_width/2)
        pos_visual_tail = position_tail - QtCore.QPoint(self.pixmap_width/2, self.pixmap_width/2)

        self.rect_head = QtCore.QRect(pos_visual_head, QtCore.QSize(self.pixmap_width, self.pixmap_width))
        self.rect_tail = QtCore.QRect(pos_visual_tail, QtCore.QSize(self.pixmap_width, self.pixmap_width))
        self.line = QtCore.QLine(self.position_head, self.position_tail)  

        
        # set the bounding box visual
        self.boundingBox = QtCore.QRect()
        self.boundingBoxOffset = [50, 50]
        self.calculateBoundingBox()

        # set pixmaps for head/tail visuals
        self.get_colors_according_to_group()
     
    def get_colors_according_to_group(self):
        self.color = ""
        
        if self.group == AnimalGroup.UNIDENTIFIED:
            self.pixmap_head = QtGui.QPixmap("animal_markings/o_gray.png")        
            self.pixmap_tail = QtGui.QPixmap("animal_markings/x_gray.png")  
            self.color = QtGui.QColor(217, 217, 217)
              
        elif self.group == AnimalGroup.FISH:
            self.pixmap_head = QtGui.QPixmap("animal_markings/o_blue.png")        
            self.pixmap_tail = QtGui.QPixmap("animal_markings/x_blue.png")  
            self.color = QtGui.QColor(0, 112, 192)
            
        elif self.group == AnimalGroup.CRUSTACEA:
            self.pixmap_head = QtGui.QPixmap("animal_markings/o_red.png")        
            self.pixmap_tail = QtGui.QPixmap("animal_markings/x_red.png") 
            self.color = QtGui.QColor(255, 0, 0)
            
        elif self.group == AnimalGroup.CHAETOGNATHA:
            self.pixmap_head = QtGui.QPixmap("animal_markings/o_orange.png")        
            self.pixmap_tail = QtGui.QPixmap("animal_markings/x_orange.png")  
            self.color = QtGui.QColor(255, 192, 0)
            
        elif self.group == AnimalGroup.JELLYFISH:
            self.pixmap_head = QtGui.QPixmap("animal_markings/o_black.png")        
            self.pixmap_tail = QtGui.QPixmap("animal_markings/x_black.png") 
            self.color = QtGui.QColor(0, 0, 0)
     
    
    def setPositionHead(self, pos):
        self.position_head = pos
        self.rect_head.moveTopLeft(pos - QtCore.QPoint(self.pixmap_width/2, self.pixmap_width/2))
        self.line.setP1(pos)
        self.calculateBoundingBox() 
    
    def setPositionTail(self, pos):
        self.position_tail = pos
        self.rect_tail.moveTopLeft(pos - QtCore.QPoint(self.pixmap_width/2, self.pixmap_width/2))
        self.line.setP2(pos)
        self.calculateBoundingBox()
        
    def setGroup(self, group):
        self.group = group
        self.get_colors_according_to_group()
    
    def calculateBoundingBox(self):
        pos_x = min(self.position_tail.x(), self.position_head.x()) - self.boundingBoxOffset[0]/2 #abs((self.position_head.x() - self.position_tail.x())/2) + min(self.position_head.x(), self.position_tail.x())
        pos_y = min(self.position_tail.y(), self.position_head.y()) - self.boundingBoxOffset[1]/2 #abs((self.position_head.y() - self.position_tail.y())/2) + min(self.position_head.y(), self.position_tail.y())
        size_x = abs(self.position_head.x() - self.position_tail.x()) + self.boundingBoxOffset[0]
        size_y = abs(self.position_head.y() - self.position_tail.y()) + self.boundingBoxOffset[1]
        
        # update the bounding box with the new parameters
        self.boundingBox.setTopLeft(QtCore.QPoint(pos_x, pos_y))
        self.boundingBox.setWidth(size_x)
        self.boundingBox.setHeight(size_y)
        

class MeasurementArea(QtWidgets.QWidget):
    """
    Custom Qt Widget to be used for adding/removing/displaying the heads and tails of animals.
    """

    def __init__(self, parent=None):
        super(MeasurementArea, self).__init__(parent)

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
        self.current_image_pixmap = QtGui.QPixmap("../data/maritime_dataset_25/training_data_animals/0.jpg")
        

    def paintEvent(self, event):
        super().paintEvent(event)    
                
        # define painter
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
    
        # draw background
        pix = self.current_image_pixmap.scaled(QtCore.QSize(self.width(), self.height()))
        painter.fillRect(self.rect(), QtGui.QBrush(pix))
    
        # draw all animals in the list
        for animal in self.animals:
            painter.drawPixmap(animal.rect_head, animal.pixmap_head)
            painter.drawPixmap(animal.rect_tail, animal.pixmap_tail)
            
            # draw a line that is not displayed within the circle representing the head
            painter.setPen(QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))  
            # @todo 
            painter.drawLine(animal.line)
            
            #temp_line = QtCore.QLine(animal.line)
            #temp_line.setP1(QtCore.QPoint(animal.line.x1() + 25, animal.line.y1() - 25))
            #painter.drawLine(temp_line)
            
            
            painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0,0), 2, QtCore.Qt.SolidLine)) 
            painter.drawRoundedRect(animal.boundingBox, 10, 10)
            
         
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
        
        # draw the current animal with it s bounding box
        if self.cur_animal is not None:
            if self.cur_animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                painter.drawPixmap(self.cur_animal.rect_head, self.cur_animal.pixmap_head)
                
            if self.cur_animal.position_tail != QtCore.QPoint(-1,-1):
                # draw the tail visual
                painter.drawPixmap(self.cur_animal.rect_tail, self.cur_animal.pixmap_tail)
                
                painter.setPen(QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
                painter.drawLine(self.cur_animal.line)
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
        if not self.drag_position_head.isNull() and self.rect().contains(event.pos()):         
            self.cur_animal.setPositionHead(event.pos() - self.drag_position_head)
            
        # if there is a tail to draw and if the drag_position is within the widget, move the tail
        if not self.drag_position_tail.isNull() and self.rect().contains(event.pos()):
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



class MyWindow(QtWidgets.QMainWindow):
    
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1244, 822)
        
        # create central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_15 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")

        # create widgets and gui objects
        self.measurementWidget = MeasurementArea(self)    
        button_add = QtWidgets.QPushButton('Add')
        button_remove = QtWidgets.QPushButton('Remove')
        button_next = QtWidgets.QPushButton('Next')
        button_previous = QtWidgets.QPushButton('Previous')
        
        

                 
        # add objects to layout
        self.horizontalLayout_15.addWidget(button_add)
        self.horizontalLayout_15.addWidget(button_remove)
        self.horizontalLayout_15.addWidget(button_next)
        self.horizontalLayout_15.addWidget(button_previous)
        self.horizontalLayout_15.addWidget(self.measurementWidget)
        
       
        MainWindow.setCentralWidget(self.centralwidget)       
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        
        # connect signals and slots      
        button_add.clicked.connect(self.measurementWidget.on_add_animal)
        button_remove.clicked.connect(self.measurementWidget.on_remove_animal)
        button_next.clicked.connect(self.measurementWidget.on_next_animal)
        button_previous.clicked.connect(self.measurementWidget.on_previous_animal)


        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyWindow(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

