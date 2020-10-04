# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import pandas as pd
import os

from Animal import Animal, AnimalSpecificationsWidget
from Models import AnimalGroup
from Helpers import getIcon


ANIMAL_LIST = []

       
class PhotoViewer(QtWidgets.QWidget):
    """
    A photo viewer that contains a QGraphicsView to display the photos and 
    draw the animals on.
    """    
    newImageLoaded = QtCore.pyqtSignal(str)
    
    def __init__(self, models, imageDirectory, imagePrefix, resFilePath="", 
                 imageEnding="*_L.jpg", parent=None):
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
        images_with_prefix = glob.glob(imageDirectory + imagePrefix 
                                       + imageEnding)
        
        self.image_list = []
        if hasattr(self.parent().parent().parent(), 'page_data'):
            date = self.parent().parent().parent().page_data.\
                calendarWidget.selectedDate().toString("yyyy.MM.dd")
            
            self.image_list = [x for x in images_with_prefix if date in x]
            
        #self.res_file = None
        self.loadResFile()

        # initalize gui and actions
        self._initUi()
        self._initActions()
        
        # load initial image
        if self.cur_image_index < len(self.image_list):
            self.loadImage(self.image_list[self.cur_image_index])

    def loadResFile(self):
        if os.path.isfile(self.res_file_path):
            substring = "_neuralNet_output"
            
            # load the neural network result file or the previsouly saved one
            if substring in self.res_file_path:
                if os.path.isfile(self.res_file_path.replace(substring,"")):
                    self.res_file_path = self.res_file_path.replace(substring,"")  
            else:
                self.res_file_path = self.res_file_path
            
            # load the result file
            res_file = pd.read_csv(self.res_file_path, sep=",")
            
            # set data on animal model
            self.models.model_animals.update(res_file) 
      
            # add image remarks to model
            img_remarks = res_file["image_remarks"].unique()
            for remark in img_remarks:
                self.models.addImageRemark(remark)
            
            # add animal remarks to model
            animal_remarks = res_file["object_remarks"].unique()
            for remark in animal_remarks:
                self.models.addAnimalRemark(remark)               
            
            # add species to list
            species = res_file["species"].unique()
            for spec in species:
                self.models.addSpecies(spec, "")
                               
    def setResFilePath(self, text):
        self.res_file_path = text
        self.loadResFile()
    
    def setImageDir(self, text):
        self.image_directory = text
        self.cur_image_index = 0
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
        images_with_prefix = glob.glob(self.image_directory 
                                       + self.image_prefix + self.image_ending)
        if hasattr(self.parent().parent().parent(), 'page_data'):
            date = self.parent().parent().parent().page_data.\
                calendarWidget.selectedDate().toString("yyyy.MM.dd")
            self.image_list = [x for x in images_with_prefix if date in x]
        
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
            photo = QtGui.QPixmap(path).scaled(QtCore.QSize(
                self.imageArea.width(), self.imageArea.height()))
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
            photo = QtGui.QPixmap().fromImage(image).scaled(QtCore.QSize(
                self.imageArea.width(), self.imageArea.height()))
            self.imageArea.animal_painter.setOriginalWidthHeight(
                width=image.width(), height = image.height())
        else:
            photo = None
        
        self.imageArea.setPhoto(photo)
        self.updateImageCountVisual()
        
        # clear visuals
        self.imageArea.animal_painter.removeAll()
        
        # update animal list
        ANIMAL_LIST.clear()
        
        # find current image in result file and draw all animals from it
        if self.models.model_animals.data is not None and path is not None:
            cur_file_entries = self.models.model_animals.data[
                self.models.model_animals.data['file_id'] == \
                    os.path.basename(path)[:-6]]
            self.imageArea.animal_painter.drawAnimalsFromList(
                cur_file_entries, self.image_ending)       
            if len(cur_file_entries) > 0: 
                remark = str(cur_file_entries['image_remarks'].iloc[0])
                if remark == "nan": remark = ""
                self.newImageLoaded.emit(remark)
            
        # reset current animal, hide specs widget and update bounding boxes (none should be drawn since cur_animal is None)
        self.imageArea.animal_painter.cur_animal = None
        self.imageArea.animal_painter.widget_animal_specs.hide()
        self.imageArea.animal_painter.updateBoundingBoxes() 
    
    
    def exportToCsv(self, file_id):
        res_file_path = self.parent().parent().parent().\
            page_data.lineEdit_res_file.text()
        self.models.model_animals.exportToCsv(res_file_path, file_id)
    
    def on_next_image(self):
        # current file_id
        if self.cur_image_index < len(self.image_list):
            cur_file_id = os.path.basename(self.image_list[self.cur_image_index])[:-6]
            
            # set current image to status "checked"
            cur_file_indices = self.models.model_animals.data[
                self.models.model_animals.data['file_id'] ==  cur_file_id].index
            for idx in cur_file_indices:
                self.models.model_animals.data.loc[idx, "status"] = "checked"
            
            # if there is a next image, load it
            if self.cur_image_index < len(self.image_list) - 1:
                # get the new image and load it
                path = self.image_list[self.cur_image_index+1]
                self.cur_image_index = self.cur_image_index + 1        
                self.loadImage(path)
            
            # update the previous image in the csv file
            self.exportToCsv(cur_file_id)
       
    def on_previous_image(self):
        # current file_id
        cur_file_id = os.path.basename(self.image_list[self.cur_image_index])[:-6]
        
        # set current image to status "checked"
        cur_file_indices = self.models.model_animals.data[
            self.models.model_animals.data['file_id'] ==  cur_file_id].index
        for idx in cur_file_indices:
            self.models.model_animals.data.loc[idx, "status"] = "checked"
            
        # if there is a previous image, load it
        if self.cur_image_index > 0:
            path = self.image_list[self.cur_image_index-1]
            self.cur_image_index = self.cur_image_index - 1
            self.loadImage(path) 
        
        # update the previous image in the csv file
        self.exportToCsv(cur_file_id)


    def updateImageCountVisual(self):
        num_images = len(self.image_list)
        cur_image = self.cur_image_index
        self.label_imgCount.setText(str(cur_image+1) + "/" + str(num_images))

    def _initActions(self):
        # connect buttons
        self.btn_previous_image.clicked.connect(self.on_previous_image)
        self.btn_next_image.clicked.connect(self.on_next_image)

        # --- define shor---------------------------------------------------- #  
        self.shortcut_previous_image = QtWidgets.QShortcut(
            QtGui.QKeySequence("left"), self.btn_previous_image, 
            self.on_previous_image)
        self.shortcut_next_image = QtWidgets.QShortcut(
            QtGui.QKeySequence("right"), self.btn_next_image, 
            self.on_next_image) 

    # enable or disable arrow key shortcuts
    def setArrowShortcutsActive(self, are_active):
        self.shortcut_previous_image.setEnabled(are_active)
        self.shortcut_next_image.setEnabled(are_active)
              
        
    def _initUi(self):
        # --- left frame ---------------------------------------------------- # 
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
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, 
                                            QtWidgets.QSizePolicy.Minimum, 
                                            QtWidgets.QSizePolicy.Expanding)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.
                                            QSizePolicy.Minimum, 
                                            QtWidgets.QSizePolicy.Expanding)
 
        # button for previous image
        self.btn_previous_image = QtWidgets.QPushButton(frame_left)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_previous_image.sizePolicy().hasHeightForWidth())
        self.btn_previous_image.setSizePolicy(sizePolicy)
        self.btn_previous_image.setIcon(getIcon(":/icons/icons/arrow_left_big.png"))
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
        
        
        # --- image area ---------------------------------------------------- # 
        self.imageArea = ImageArea(self.models, self)
        
        # --- right frame --------------------------------------------------- # 
        # frame
        frame_right = QtWidgets.QFrame(self)
        frame_right.setMinimumSize(QtCore.QSize(60, 0))
        frame_right.setMaximumSize(QtCore.QSize(60, 16777215))
        frame_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_right.setObjectName("frame_right")
        
        # vertical spacers
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, 
                                            QtWidgets.QSizePolicy.Minimum, 
                                            QtWidgets.QSizePolicy.Expanding)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)
        
        # button for previous image
        self.btn_next_image = QtWidgets.QPushButton(frame_right)      
        self.btn_next_image.setIcon(getIcon(
            ":/icons/icons/arrow_right_big.png"))
        self.btn_next_image.setIconSize(QtCore.QSize(20, 40))
        self.btn_next_image.setObjectName("btn_next_image")
        
        # button for opening image in separate window
        self.btn_openImg = QtWidgets.QPushButton(frame_right)
        self.btn_openImg.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_openImg.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_openImg.setIcon(getIcon(":/icons/icons/open_image.png"))
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
        
        # --- main widget --------------------------------------------------- #      
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
        

class ImageArea(QtWidgets.QGraphicsView):
    """
    An implementation of QGraphicsView to enable painting of animals on a 
    photo as well as loading of photos. Moreover, it provides a 
    wheel zoom functionality.
    """
    def __init__(self, models, parent=None):
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
        # data models
        self.models = models
        
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
        
        # original size of image (needed for resizing, i.e. recalculating 
        # coordinates)
        self.original_img_width = 0
        self.original_img_height = 0
    
    
    def setAnimalRemark(self, remark):
        if self.cur_animal is not None:
            self.cur_animal.setRemark(remark)
    
    def setAnimalSpecies(self, species):
        if self.cur_animal is not None:
            self.cur_animal.setSpecies(species)

    def setAnimalGroup(self, group):
        if self.cur_animal is not None:
            self.cur_animal.setGroup(group) 
            
            # update drawing
            self.cur_animal.head_item_visual.setPixmap(self.cur_animal._pixmap_head)
            self.cur_animal.tail_item_visual.setPixmap(self.cur_animal._pixmap_tail)
            
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
        """
        Draws the head of an animal.

        Parameters
        ----------
        animal : Animal
            The animal whose head is to be painted.
        """
        if animal != None:
            if animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                # animal.drawHead()
                # animal.head_item_visual = QtWidgets.QGraphicsPixmapItem(animal.pixmap_head)
                # animal.head_item_visual.setPos(animal.rect_head.center() - QtCore.QPoint(animal.pixmap_width/4, animal.pixmap_width/4))
                # animal.head_item_visual.ItemIsMovable = True
                self.imageArea._scene.addItem(animal.createHeadVisual())
                #animal.is_head_drawn = True
     
    def drawAnimalLine(self, animal):
        """
        Draws the line between head an tail of an animal.

        Parameters
        ----------
        animal : Animal
            The animal whose line is to be painted.
        """
        animal.line_item_visual = self.imageArea._scene.addLine(animal.line, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
     
    def drawAnimalTailLineBoundingBox(self, animal):
        """ Draws the tail of an animal, the line betwen head and tail and 
        the bounding box around it. """
        
        if animal != None:
            if animal.position_tail != QtCore.QPoint(-1,-1):
                # draw the tail visual
                # animal.tail_item_visual = QtWidgets.QGraphicsPixmapItem(animal.pixmap_tail)
                # animal.tail_item_visual.setPos(animal.rect_tail.center() - QtCore.QPoint(animal.pixmap_width/4, animal.pixmap_width/4))
                # animal.tail_item_visual.ItemIsMovable = True
                self.imageArea._scene.addItem(animal.createTailVisual())
                
                # draw line and boundingbox visuals
                self.drawAnimalLine(animal)
                animal.boundingBox_visual = self.imageArea._scene.addRect(animal.boundingBox, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
                
                #animal.is_tail_drawn = True
                
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
            else:
                # else, go to first image
                self.cur_animal = ANIMAL_LIST[0]
                self.updateBoundingBoxes()
                   
    def on_previous_animal(self):
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in ANIMAL_LIST:
            index = ANIMAL_LIST.index(self.cur_animal)
            
            # only go to previous animal, if there is one
            if index > 0:
                self.cur_animal = ANIMAL_LIST[index-1]
                self.updateBoundingBoxes() 
            else:
                # else, go to last image
                self.cur_animal = ANIMAL_LIST[len(ANIMAL_LIST)-1]
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
                    
                    # remove animal from list and data model
                    pos = self.models.model_animals.data.index.get_loc(animal.row_index)
                    self.models.model_animals.removeRows(pos, 1, QtCore.QModelIndex())

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
                    
                    cur_image_path = self.imageArea.parent().image_list[self.imageArea.parent().cur_image_index]
                    image_remark = self.imageArea.parent().parent().comboBox_imgRemark.currentText()
                    experiment_id = self.imageArea.parent().parent().parent().parent().page_data.lineEdit_exp_id.text()
                    user_id = self.imageArea.parent().parent().parent().parent().page_settings.lineEdit_user_id.text()
                    self.models.model_animals.insertRows(
                        self.models.model_animals.rowCount(), 1, 
                        [self.cur_animal], cur_image_path, 
                        image_remark, experiment_id, user_id)
                    
                else:
                    # create a new animal
                    self.cur_animal = Animal(self.models, row_index = self.models.model_animals.rowCount(),
                                             position_head = pos)
                    self.cur_animal.setGroup(AnimalGroup.UNIDENTIFIED)
                              
                    # calculate position in original format
                    self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                    
                    # do the actual drawing of the head
                    self.drawAnimalHead(self.cur_animal)
 
            else:                
                # create a new animal
                self.cur_animal = Animal(self.models, row_index = self.models.model_animals.rowCount(),
                                         position_head = pos)
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
            
            self.updateOriginalAnimalPosition(self.cur_animal)
            
            self.updateBoundingBoxes()            
            self.cur_animal.setManuallyCorrected(True)

        # if there is a tail to draw and if the drag_position is within the widget, move the tail
        if not self.drag_position_tail.isNull() and self.imageArea.rect().contains(pos) and self.cur_animal is not None:
            self.cur_animal.setPositionTail(pos - self.drag_position_tail)
            
            # remove tail and line on old position and draw it on the new position
            self.removeTailVisual(self.cur_animal)
            self.removeLineVisual(self.cur_animal)  
            self.removeBoundingBoxVisual(self.cur_animal)
            self.drawAnimalTailLineBoundingBox(self.cur_animal)

            self.updateBoundingBoxes()            
            self.cur_animal.setManuallyCorrected(True)

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
        
    def updateOriginalAnimalPosition(self, animal):
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
            
            # update data model
            self.models.model_animals.data.loc[self.cur_animal.row_index, "LX1"] = self.cur_animal.original_pos_head.x()
            self.models.model_animals.data.loc[self.cur_animal.row_index, "LY1"] = self.cur_animal.original_pos_head.y()
            self.models.model_animals.data.loc[self.cur_animal.row_index, "LX2"] = self.cur_animal.original_pos_tail.x()
            self.models.model_animals.data.loc[self.cur_animal.row_index, "LY2"] = self.cur_animal.original_pos_tail.y()


    def drawAnimalsFromList(self, animal_list, image_ending="_L"):
        """
        Draws animals from a list on the current image. 

        Parameters
        ----------
        animal_list : DataFrame
            The list of animals to draw. Necessary columns: 
            LX1, LY1 (head position on left image), 
            LX2, LY2 (tail position on left image), 
            RX1, RY1 (head position on right image), 
            RX2, RY2 (tail position on right image),
            group, species, object_remarks
        image_ending : string, optional
            Indicates wether to draw animals from left or right image. 
            The default is "_L".
        """
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
                self.cur_animal = Animal(self.models,
                                         row_index=animal_list.index[i],
                                         position_head=pos_h, 
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
     
 