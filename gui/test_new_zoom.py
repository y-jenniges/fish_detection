# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
import glob

from test_graph import Animal, AnimalGroup, AnimalSpecies
from Helpers import get_icon

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
        for animal in ANIMAL_LIST:
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
        elif self.is_add_mode_active:
            if (self.is_head_drawn and self.is_tail_drawn):
                self.is_add_mode_active = False
                self.is_remove_mode_active = True
            else:
                print("Error: Please draw head and tail before switching off the Add-mode.")            
        else:
            self.is_add_mode_active = False
            self.is_remove_mode_active = True          

    def on_add_animal(self): 
        if(self.is_add_mode_active):
            # the add mode can only be deactivated when head and tail are drawn
            if (self.is_head_drawn and self.is_tail_drawn):
                self.is_add_mode_active = False
            else:
                print("Error: Please draw head and tail before switching off the Add-mode.")
        else:
            self.is_remove_mode_active = False
            self.is_add_mode_active = True

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
                
                # do the actual drawing
                self.drawAnimalTailLineBoundingBox(self.cur_animal)
                
                # tail is now defined and will be drawn
                self.is_tail_drawn = True
                
                # add animal to list
                ANIMAL_LIST.append(self.cur_animal)
 
            else:                
                # create a new animal
                self.cur_animal = Animal(position_head = pos)
                self.cur_animal.setGroup(AnimalGroup.FISH)
                               
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
    def __init__(self):
        super(PhotoViewer, self).__init__()

        # list of image pathes and the current image index
        self.cur_image_index = 0
        self.image_list = glob.glob(IMAGE_DIRECTORY + IMAGE_PREFIX + "*.jpg")

        # initalize gui
        self.init_ui()
        
        # initalize actions
        self.init_actions()
        

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.loadImage(self.image_list[self.cur_image_index])
                
    def loadImage(self, path):
        photo = QtGui.QPixmap(path).scaled(QtCore.QSize(self.imageArea.width(), self.imageArea.height()))
        self.imageArea.setPhoto(photo)
        self.updateImageCountVisual()
        
        # clear visuals
        self.imageArea.animal_painter.removeAll()
        
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
        QtWidgets.QShortcut(QtGui.QKeySequence("left"), self.btn_previous_image, self.on_previous_image)
        QtWidgets.QShortcut(QtGui.QKeySequence("right"), self.btn_next_image, self.on_next_image)
        

        
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
        self.imageArea = ImageArea()
        
        
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