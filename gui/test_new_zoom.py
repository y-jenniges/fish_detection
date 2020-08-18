# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
import glob

from test_graph import Animal, AnimalGroup, AnimalSpecies


IMAGE_DIRECTORY = "../data/maritime_dataset_25/training_data_animals/"
IMAGE_PREFIX = ""
ANIMAL_LIST = []


"""
An implementation of QGraphicsView to enable painting of animals on a photo as well as loading of photos. Moreover, it provides a wheel zoom functionality.
"""
class ImageArea(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(ImageArea, self).__init__(parent)
        
        self._zoom = 0
        self._scene = QtWidgets.QGraphicsScene()
        self._photo = QtWidgets.QGraphicsPixmapItem()

        self._scene.addItem(self._photo)     
        self.setScene(self._scene)

        # set properties for graphics view
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
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
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)               
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
            # zoom in if y > 0, else zoom out
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            
            # scale the view if zoom is positive, else set it to zero and fit the photo in the view
            if 20 > self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            elif self._zoom >= 20:
                # just zoom in to a factor of 20
                pass
            else:
                self._zoom = 0

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
        
        # variables to control what interactions are possible
        self.is_add_mode_active = False
        self.is_remove_mode_active = False
        
        # the QGraphicsView to paint on
        self.imageArea = imageArea
 
    def removeAll(self):
        print("remove all")
        for animal in ANIMAL_LIST:
            print("remove another one")
            self.removeHeadVisual(animal)
            self.removeTailVisual(animal)
            self.removeLineVisual(animal)
            self.removeBoundingBoxVisual(animal)
            
 
    def updateBoundingBoxes(self):
        # remove bounding of other animals
        for animal in ANIMAL_LIST:
            self.imageArea._scene.removeItem(animal.boundingBox_visual)
            animal.boundingBox_visual = None

        # draw the current animal bounding box
        if self.cur_animal is not None and self.cur_animal in ANIMAL_LIST:
            self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(self.cur_animal.boundingBox, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
                
    def drawAnimalHead(self, animal):
        if animal != None:
            if self.cur_animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                self.cur_animal.head_item_visual = QtWidgets.QGraphicsPixmapItem(self.cur_animal.pixmap_head)
                self.cur_animal.head_item_visual.setPos(self.cur_animal.rect_head.center() - QtCore.QPoint(self.cur_animal.pixmap_width/4, self.cur_animal.pixmap_width/4))
                self.cur_animal.head_item_visual.ItemIsMovable = True
                self.imageArea._scene.addItem(self.cur_animal.head_item_visual)
     
    def drawAnimalLine(self, animal):
        self.cur_animal.line_item_visual = self.imageArea._scene.addLine(self.cur_animal.line, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
     
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

    def mousePressEvent(self, event):
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        if(self.is_head_drawn and self.is_tail_drawn and self.cur_animal is not None):
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
        elif(not self.is_remove_mode_active and not self.is_add_mode_active):
             for animal in ANIMAL_LIST:
                if(animal.boundingBox.contains(pos)):
                    self.cur_animal = animal
                    break
                    
        elif(self.is_add_mode_active):
            # add mode
            if(self.is_head_drawn and not self.is_tail_drawn):
                # adapt the tail position of the current animal
                self.cur_animal.setPositionTail(pos)
                
                 # tail is now defined and will be drawn
                self.is_tail_drawn = True
                
                # do the actual drawing
                self.drawAnimalTailLineBoundingBox(self.cur_animal)
                
                # add animal to list
                ANIMAL_LIST.append(self.cur_animal)
 
            else:                
                # create a new animal
                self.cur_animal = Animal(position_head = pos)
                self.cur_animal.setGroup(AnimalGroup.FISH)
                
                # head is now defined and will be drawn 
                self.is_head_drawn = True
                self.is_tail_drawn = False
                
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
    def __init__(self):
        super(PhotoViewer, self).__init__()

        self.cur_image_index = 0
        self.setStyleSheet("ImageArea{background-color:black}")

        # gui elements
        self.imageArea = ImageArea()
        self.btn_next_image = QtWidgets.QPushButton("next image")
        self.btn_previous_image = QtWidgets.QPushButton("previous image")
        
        # create a layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setObjectName("layout")
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        # add gui elements to layout
        self.layout.addWidget(self.imageArea)
        self.layout.addWidget(self.btn_next_image)
        self.layout.addWidget(self.btn_previous_image)
        
        # initalize actions
        self.btn_next_image.clicked.connect(self.on_next_image)
        self.btn_previous_image.clicked.connect(self.on_previous_image)
        

    def resizeEvent(self, event):
        super().resizeEvent(event)
        image_list = glob.glob(IMAGE_DIRECTORY + IMAGE_PREFIX + "*.jpg")
        self.loadImage(image_list[self.cur_image_index])
                
    def loadImage(self, path):
        photo = QtGui.QPixmap(path).scaled(QtCore.QSize(self.imageArea.width(), self.imageArea.height()))
        self.imageArea.setPhoto(photo)
  
    def on_next_image(self):
        image_list = glob.glob(IMAGE_DIRECTORY + IMAGE_PREFIX + "*.jpg")
        path = image_list[self.cur_image_index+1]
        self.cur_image_index = self.cur_image_index + 1        
        self.loadImage(path)
        self.updateImageCount()   
        
        # clear visuals
        self.imageArea.animal_painter.removeAll()
        
        # clear animal list
        ANIMAL_LIST.clear()
        print(ANIMAL_LIST)
       
    def on_previous_image(self):
        image_list = glob.glob(IMAGE_DIRECTORY + IMAGE_PREFIX + "*.jpg")
        path = image_list[self.cur_image_index-1]
        self.cur_image_index = self.cur_image_index - 1
        self.loadImage(path)   
        self.updateImageCount()  
        
    def updateImageCount(self):
        #print(f"new image count : {self.cur_image_index}" )
        pass





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