# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import pandas as pd
import os
from Animal import Animal, AnimalSpecificationsWidget
from Models import AnimalGroup
from Helpers import getIcon, displayErrorMsg

      
class PhotoViewer(QtWidgets.QWidget):
    """
    A photo viewer that contains a QGraphicsView to display the photos and 
    draw the animals on.
    
    Attributes
    -----------
    image_directory : string
        Directory where the images are stored. 
    image_prefix : string
        Images will be displayed only if they start with this prefix.
    image_ending : string
        It is either '\*_L.jpg' or '\*_R.jpg'. Indicates if the left or right 
        image is currently being edited.
    output_dir : string
        Directory where the output file is stored.
    cur_image_index : int
        Index of the current image in image_list.
    image_list : list<string>
        List containing all image pathes that have the given prefix, are of the
        selected date and have the desired image ending.
    newImageLoaded: pyqtSignal
    """    
    
    newImageLoaded = QtCore.pyqtSignal(str)
    """ Signal that is emitted when a new image is loaded. """
    
    def __init__(self, models, imageDirectory, imagePrefix, outputDir="", 
                 imageEnding="*_L.jpg", parent=None):
        """
        Init function.

        Parameters
        ----------
        models : TYPE
            DESCRIPTION.
        imageDirectory : string
            DESCRIPTION.
        imagePrefix : string
            DESCRIPTION.
        outputDir : string, optional
            DESCRIPTION. The default is "".
        imageEnding : string, optional
            DESCRIPTION. The default is "*_L.jpg".
        parent : TYPE, optional
            The parent object. The default is None.
        """
        super(PhotoViewer, self).__init__(parent)

        # data models
        self.models = models

        # image directory and prefix (needed for retrieving the image_list)
        self.image_directory = imageDirectory
        self.image_prefix = imagePrefix
        self.image_ending = imageEnding
        self.output_dir = outputDir

        # list of image pathes and the current image index
        self.cur_image_index = 0
        images_with_prefix = glob.glob(imageDirectory + imagePrefix 
                                       + imageEnding)
        
        self.image_list = []
        if hasattr(self.parent().parent().parent(), 'page_data'):
            date = self.parent().parent().parent().page_data.\
                calendarWidget.selectedDate().toString("yyyy.MM.dd")
            
            self.image_list = [x for x in images_with_prefix if date in x]
            
        # load result file if one already exists
        self.loadResFile()

        # initalize gui and actions
        self._initUi()
        self._initActions()

    def loadResFile(self):
        """ Loads the output file and updates data models with unseen remarks and
        species. """ 
        main_window = self.parent().parent().parent()
        if main_window is not None:
            res_file_name = main_window.getResultFileName()
        
            if res_file_name is not None:
                path = os.path.join(self.output_dir, res_file_name)
                
                if os.path.isfile(path):
                    # load the result file
                    res_file = pd.read_csv(path, sep=",")
                    
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
                    
                    # add species to list in model
                    species = res_file["species"].unique()
                    for spec in species:
                        self.models.addSpecies(spec, "")
                               
    def setOutDir(self, text):
        """ Loads the output file for the new output directoy. """
        self.output_dir = text
        self.loadResFile()
    
    def setImageDir(self, text):
        """ Updates image list according to new image directory. """
        self.image_directory = text
        self.cur_image_index = 0
        self.updateImageList()
        
    def setImagePrefix(self, text):
        """ Updates the image list according to new prefix. """
        self.image_prefix = text
        self.updateImageList()
        
    def setImageEnding(self, text):
        """ Adapt image ending in animal_painter and in self. Must be either
        '\*_L.jpg' or '\*_R.jpg'. """
        assert(text == "*_L.jpg" or text == "*_R.jpg")
        self.image_ending = text
        self.updateImageList()
        self.imageArea.animal_painter.image_ending = text

    def activateLRMode(self, activateLRMode=False):
        """ !!! NOT IMPLEMENTED YET !!! """
        pass

    def updateImageList(self):
        """ Recalculate image list, i.e. filter the image directory for images
        with the correct prefix and date. """
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
        """ Resizes image and animal positions when resize event occurs. """
        super().resizeEvent(event)

        if self.cur_image_index < len(self.image_list):
            # reload photo
            path = self.image_list[self.cur_image_index]
            photo = QtGui.QPixmap(path).scaled(QtCore.QSize(
                self.imageArea.width(), self.imageArea.height()))
            self.imageArea.setPhoto(photo)
            self.updateImageCountVisual()
        
        self.imageArea.animal_painter.redraw()

    def loadImage(self, path):
        """ Loads an image from a path and draws available animals from 
        output file. """
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
        self.imageArea.animal_painter.animal_list.clear()
        
        # find current image in result file and draw all animals from it
        if self.models.model_animals.data is not None and path is not None:
            # find animals on current image
            cur_file_entries = self.models.model_animals.data[
                self.models.model_animals.data['file_id'] == \
                    os.path.basename(path).rstrip(".jpg").rstrip(".png").rstrip("_L").rstrip("_R")]
            
            # draw animals
            self.imageArea.animal_painter.drawAnimalsFromList(
                cur_file_entries, self.image_ending)       
            
            # load current image remark
            if len(cur_file_entries) > 0: 
                remark = str(cur_file_entries['image_remarks'].iloc[0])
                if remark == "nan": remark = ""
                self.newImageLoaded.emit(remark)
            
        # reset current animal, hide specs widget and update bounding boxes 
        # (none should be drawn since cur_animal is None)
        self.imageArea.animal_painter.cur_animal = None
        self.imageArea.animal_painter.widget_animal_specs.hide()
        self.imageArea.animal_painter.updateBoundingBoxes()    
    
    def exportToCsv(self, file_id):
        """ Updates the current CSV table. """
        main_window = self.parent().parent().parent()
        output_dir = main_window.page_data.lineEdit_output_dir.text()
        res_file_name = main_window.getResultFileName()
        self.models.model_animals.exportToCsv(output_dir, res_file_name, file_id)
    
    def on_next_image(self):
        """ Loads the next image and draws animals accordingly. """
        if not self.models.model_animals.isEmpty(): 
            # only go to next image if cur animal is none or complete
            cur_animal = self.imageArea.animal_painter.cur_animal

            if cur_animal is not None and \
            ((cur_animal.is_head_drawn and not cur_animal.is_tail_drawn) or \
             (not cur_animal.is_head_drawn and cur_animal.is_tail_drawn)):
                displayErrorMsg("Error", 
                                "Please draw head and tail before switching the image.", 
                                "Error")  
            # only go to next image if there is one and the add mode is inactive
            elif self.cur_image_index < len(self.image_list) -1:
                cur_file_id = os.path.basename(
                    self.image_list[self.cur_image_index]).rstrip(".jpg"). \
                    rstrip(".png").rstrip("_L").rstrip("_R")
                
                # set current image to status "checked"
                cur_file_indices = self.models.model_animals.data[
                    self.models.model_animals.data['file_id'] ==  cur_file_id].index
                
                for idx in cur_file_indices:
                    self.models.model_animals.data.loc[idx, "status"] = "checked"
                
                # get the new image and load it
                path = self.image_list[self.cur_image_index+1]
                self.cur_image_index = self.cur_image_index + 1    
                self.cur_animal = None
                self.loadImage(path)
                
                # update the previous image in the csv file
                self.exportToCsv(cur_file_id)
    
    def on_previous_image(self):
        """ Loads the previous image and draws animals accordingly. """
        if not self.models.model_animals.isEmpty(): 
            # only go to previous image if cur animal is none or complete
            cur_animal = self.imageArea.animal_painter.cur_animal

            if cur_animal is not None and \
            ((cur_animal.is_head_drawn and not cur_animal.is_tail_drawn) or \
             (not cur_animal.is_head_drawn and cur_animal.is_tail_drawn)):
                displayErrorMsg("Error", 
                                "Please draw head and tail before switching the image.", 
                                "Error")  
            # only go to previous image if there is one and the add mode is inactive
            elif self.cur_image_index > 0:
                # current file_id
                cur_file_id = os.path.basename(
                    self.image_list[self.cur_image_index]).strip(".jpg"). \
                    strip(".png").strip("_L").strip("_R")
                
                # set current image to status "checked"
                cur_file_indices = self.models.model_animals.data[
                    self.models.model_animals.data['file_id'] ==  cur_file_id].index
                
                for idx in cur_file_indices:
                    self.models.model_animals.data.loc[idx, "status"] = "checked"
                    
                # load image
                path = self.image_list[self.cur_image_index-1]
                self.cur_image_index = self.cur_image_index - 1
                self.cur_animal = None
                self.loadImage(path) 
                
                # update the previous image in the csv file
                self.exportToCsv(cur_file_id)

    def updateImageCountVisual(self):
        """ Updates the display of the total number of images and the current 
        image index """
        num_images = len(self.image_list)
        cur_image = self.cur_image_index
        self.label_imgCount.setText(str(cur_image+1) + "/" + str(num_images))

    def _initActions(self):
        """ Initalizes the actions connected to UI elements. """ 
        # connect buttons
        self.btn_previous_image.clicked.connect(self.on_previous_image)
        self.btn_next_image.clicked.connect(self.on_next_image)

        # --- define shortcuts ---------------------------------------------- #  
        self.shortcut_previous_image = QtWidgets.QShortcut(
            QtGui.QKeySequence("left"), self.btn_previous_image, 
            self.on_previous_image)
        self.shortcut_next_image = QtWidgets.QShortcut(
            QtGui.QKeySequence("right"), self.btn_next_image, 
            self.on_next_image) 

    # enable or disable arrow key shortcuts
    def setArrowShortcutsActive(self, are_active):
        """ Function to en-/disable arrow shortcuts for switching between images. """
        self.shortcut_previous_image.setEnabled(are_active)
        self.shortcut_next_image.setEnabled(are_active)
              
        
    def _initUi(self):
        """ Builds the UI. """
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
        # self.btn_openImg = QtWidgets.QPushButton(frame_right)
        # self.btn_openImg.setMinimumSize(QtCore.QSize(40, 40))
        # self.btn_openImg.setMaximumSize(QtCore.QSize(40, 40))
        # self.btn_openImg.setIcon(getIcon(":/icons/icons/open_image.png"))
        # self.btn_openImg.setIconSize(QtCore.QSize(30, 30))
        # self.btn_openImg.setObjectName("btn_openImg")
        
        # layout
        layout_frame_right = QtWidgets.QVBoxLayout(frame_right)
        layout_frame_right.setContentsMargins(5, 5, 5, 0)
        layout_frame_right.setObjectName("layout_frame_right")
        
        # add widgets to layout
        layout_frame_right.addItem(spacerItem9)
        layout_frame_right.addWidget(self.btn_next_image)
        layout_frame_right.addItem(spacerItem10)
        #layout_frame_right.addWidget(self.btn_openImg)
        
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
    """
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

    def _fitInView(self, scale=True):
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
        self._fitInView() 
        
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
            
            # scale the view if zoom is positive, else set it to zero and fit 
            # the photo in the view
            if self._zoom > 0:
                self.scale(factor, factor)
                self.parent().setArrowShortcutsActive(False)
            elif self._zoom == 0:
                self._fitInView()
                self.parent().setArrowShortcutsActive(True)
            else:
                self._zoom = 0
                self.parent().setArrowShortcutsActive(True)
                    
    # delegate mouse events to animal painter
    def mousePressEvent(self, event):
        """ Passes the mouse press event to the animal_painter. """
        self.animal_painter.mousePressEvent(event)       
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ Passes the mouse move event to the animal_painter. """
        self.animal_painter.mouseMoveEvent(event)  
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """ Passes the mouse release event to the animal_painter. """
        self.animal_painter.mouseReleaseEvent(event)
        super().mouseReleaseEvent(event) 


class AnimalPainter():
    """
    Class providing the logic for adding/removing/moving and jumping between 
    animals. It needs a QGraphicsView that it can paint on and that delegates 
    the mouse events to the AnimalPainter.
    
    Dragging implementation taken from
    https://stackoverflow.com/questions/60571837/how-to-move-a-figurecreated-using-paintevent-by-simply-draging-it-in-pyqt5
    (last access: 19.10.2020)
    
    Attributes
    -----------
    animal_list: list<Animal>
        A list of animals on the current image.
    drag_position_head : QPoint
    
    drag_position_tail : QPoint
    
    cur_animal : Animal
        Currently active animal.    
    is_add_mode_active  : bool
        Indicates if the add mode is active.
    is_remove_mode_active: bool
        Indicates if the remove mode is active.
    imageArea : ImageArea
        A canvas to paint the object on and that provides mouse events to 
        the AnimalPainter.
    image_ending : string
        It is either '\*_L.jpg' or '\*_R.jpg'. Indicates if the left or right 
        image is currently being edited.
    original_img_width : int
        Width of the original image. Necessary for rescaling calculations.
    original_img_height : int
        Height of the original image. Necessary for rescaling calculations.
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
        
        # list with all animals on the current image
        self.animal_list = []
        
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
        
        # left or right image
        self.image_ending = "*_L.jpg"
        
        # original size of image (needed for resizing, i.e. recalculating 
        # coordinates)
        self.original_img_width = 0
        self.original_img_height = 0
    
    def setAnimalRemark(self, remark):
        """ Sets the remark of the currently active animal. """
        if self.cur_animal is not None:
            self.cur_animal.setRemark(remark)          
    
    def setAnimalSpecies(self, species):
        """ Sets the species of the currently active animal. """
        if self.cur_animal is not None:
            self.cur_animal.setSpecies(species)
            
    def setAnimalGroup(self, group):
        """ Sets the group of the currently active animal and adapts the 
        visuals accordingly. """
        if self.cur_animal is not None:
            self.cur_animal.setGroup(group) 
            
            # update drawing
            self.cur_animal.head_item_visual.setPixmap(self.cur_animal._pixmap_head)
            self.cur_animal.tail_item_visual.setPixmap(self.cur_animal._pixmap_tail)
            
            # redraw line and boundingbox visuals
            self.imageArea._scene.removeItem(self.cur_animal.line_item_visual)
            self.drawAnimalLine(self.cur_animal)
            
            self.imageArea._scene.removeItem(self.cur_animal.boundingBox_visual)
            self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(
                self.cur_animal.boundingBox, 
                QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
     
    def redraw(self):
        """ Redraws all animals on the current image. """
        # remove animals
        self.removeAll()
        
        # redraw animals
        for animal in self.animal_list:
            # update positions
            self.imageArea.animal_painter.updateAnimalPosition(animal)
            
            # redraw animals
            self.imageArea.animal_painter.drawAnimalHead(animal)
            self.imageArea.animal_painter.drawAnimalTailLineBoundingBox(animal)
                    
        self.imageArea.animal_painter.updateBoundingBoxes()
    
    def removeAll(self):
        """ Removes visuals of all animals. """
        for animal in self.animal_list:
            self.removeHeadVisual(animal)
            self.removeTailVisual(animal)
            self.removeLineVisual(animal)
            self.removeBoundingBoxVisual(animal)
            
            animal.is_head_drawn = False
            animal.is_tail_drawn = False
     
    def placeSpecsWidget(self):
        """ Function to move the specs widget with the bounding box of the 
        current animal (and prevent it from getting out of the borders of 
        the image) """
        if self.cur_animal is not None:
            # reset position of specs widget
            self.widget_animal_specs.move(0,0)
        
            # get position of current bounding box from scene
            pos = self.imageArea.mapFromScene(
                self.cur_animal.boundingBox_visual.rect().bottomLeft().toPoint())
            
            # move the zoom widget a bit below the button position and center it below the button
            self.widget_animal_specs.move(pos)
        
            # get corners of specs widget in scene coordinates
            top_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topLeft())).toPoint()
            top_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topRight())).toPoint()
            bottom_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomLeft())).toPoint()
            bottom_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomRight())).toPoint()
                        
            # if the lower edge of the specs is not visible, display specs above animal
            if not self.imageArea.rect().contains(bottom_left) \
                and not self.imageArea.rect().contains(bottom_right):
                new_pos = pos + QtCore.QPoint(
                    0, -self.widget_animal_specs.height() - self.cur_animal.boundingBox_visual.rect().height())
                self.widget_animal_specs.move(new_pos)
                
            # if the left edge of the specs is not visible, display specs right of animal
            elif not self.imageArea.rect().contains(bottom_left) and not self.imageArea.rect().contains(top_left):
                new_pos = pos + QtCore.QPoint(
                    self.cur_animal.boundingBox_visual.rect().width(), -self.cur_animal.boundingBox_visual.rect().height())
                self.widget_animal_specs.move(new_pos)   
    
            # # if the top edge of the specs is not visible, display specs below of animal (as usual)
            # elif not self.imageArea.rect().contains(top_left) and not self.imageArea.rect().contains(top_right):
            #     pass
        
            # if the right edge of the specs is not visible, display specs left of animal
            elif not self.imageArea.rect().contains(bottom_right) \
                and not self.imageArea.rect().contains(top_right):
                new_pos = pos + QtCore.QPoint(
                    -self.widget_animal_specs.width(), -self.cur_animal.boundingBox_visual.rect().height())
                self.widget_animal_specs.move(new_pos)
                 
    def updateBoundingBoxes(self):
        """ Removes bounding box visuals for all animals and draws only the 
        one of the current animal. """
        # remove bounding of other animals
        for animal in self.animal_list:
            self.imageArea._scene.removeItem(animal.boundingBox_visual)
            animal.boundingBox_visual = None

        # draw the current animal bounding box
        if self.cur_animal is not None and self.cur_animal in self.animal_list:
            self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(
                self.cur_animal.boundingBox, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
            
            self.widget_animal_specs.setAnimal(self.cur_animal)
            self.placeSpecsWidget()
            self.widget_animal_specs.show()
        else:
            self.widget_animal_specs.hide()
            
    def drawAnimalHead(self, animal):
        """ Draws the head of a given animal. """
        if animal != None:
            if animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                self.imageArea._scene.addItem(animal.createHeadVisual())
     
    def drawAnimalLine(self, animal):
        """ Draws the line between head an tail of a given animal. """
        animal.line_item_visual = self.imageArea._scene.addLine(
            animal.line, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
     
    def drawAnimalTailLineBoundingBox(self, animal):
        """ Draws the tail of a given animal, the line betwen head and tail and 
        the bounding box around it. """
        if animal != None:
            if animal.position_tail != QtCore.QPoint(-1,-1):
                # draw the tail visual
                self.imageArea._scene.addItem(animal.createTailVisual())
                
                # draw line and boundingbox visuals
                self.drawAnimalLine(animal)
                animal.boundingBox_visual = self.imageArea._scene.addRect(
                    animal.boundingBox, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))
                
    def removeHeadVisual(self, animal):
        """ Removes the head visual on the image of a given animal. """
        self.imageArea._scene.removeItem(animal.head_item_visual)
        animal.head_item_visual = None  

    def removeTailVisual(self, animal):
        """ Removes the tail visual on the image of a given animal. """
        self.imageArea._scene.removeItem(animal.tail_item_visual)
        animal.tail_item_visual = None  
    
    def removeLineVisual(self, animal):
        """ Removes the line visual on the image of a given animal. """
        self.imageArea._scene.removeItem(animal.line_item_visual)
        animal.line_item_visual = None  

    def removeBoundingBoxVisual(self, animal):
        """ Removes the bounding box visual on the image of a given animal. """
        self.imageArea._scene.removeItem(animal.boundingBox_visual)
        animal.boundingBox_visual = None  
      
    def on_next_animal(self):
        """ Makes the next animal in the animal_list active. """
        # if no animal ist selected, then select first one
        if self.cur_animal is None and len(self.animal_list) >0:
            self.cur_animal = self.animal_list[0]          
            
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in self.animal_list:
            index = self.animal_list.index(self.cur_animal)
    
            # only go to next animal if there is another one
            if index < len(self.animal_list)-1:
                self.cur_animal = self.animal_list[index+1]
                self.updateBoundingBoxes()
            else:
                # else, go to first image
                self.cur_animal = self.animal_list[0]
                self.updateBoundingBoxes()
                   
    def on_previous_animal(self):
        """ Makes the previous animal in the animal_list active. """
        # only switch animals if the current one is in the list (and not None)
        if self.cur_animal in self.animal_list:
            index = self.animal_list.index(self.cur_animal)
            
            # only go to previous animal, if there is one
            if index > 0:
                self.cur_animal = self.animal_list[index-1]
                self.updateBoundingBoxes() 
            else:
                # else, go to last image
                self.cur_animal = self.animal_list[len(self.animal_list)-1]
                self.updateBoundingBoxes()                 

    def on_remove_animal(self):
        """ Handles the activation state of the remove mode. """
        if(self.is_remove_mode_active):
            self.is_remove_mode_active = False           
        elif self.is_add_mode_active:
            # only deactivate add mode is animal is drawn completely
            if not self.cur_animal \
            or (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                self.is_add_mode_active = False
                self.is_remove_mode_active = True    
            else:
                displayErrorMsg("Error", 
                                "Please draw head and tail before switching off the Add-mode.", 
                                "Error")           
        else:
            self.is_add_mode_active = False
            self.is_remove_mode_active = True          

    def on_add_animal(self): 
        """ Handles the activation state of the add mode. """
        if(self.is_add_mode_active):
            # the add mode can only be deactivated when head and tail are drawn 
            # or none of them is drawn
            if self.cur_animal is not None:
                if (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn) \
                    or (not self.cur_animal.is_head_drawn and not self.cur_animal.is_tail_drawn):
                    self.is_add_mode_active = False
                else:
                    displayErrorMsg("Error", 
                                    "Please draw head and tail before switching off the Add-mode.", 
                                    "Error")
            else:
                self.is_add_mode_active = False
        else:
            self.is_remove_mode_active = False
            self.is_add_mode_active = True

    def mousePressEvent(self, event):
        """ Handles the painting options on the image: Enables dragging of
        head/tail visuals, as well as removing/adding animals on click. """
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        # enable dragging for current animal (when add mode is not active and 
        # the current animal is completey drawn)
        if self.cur_animal is not None and not self.is_add_mode_active:
            if(self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                if (2 * QtGui.QVector2D(pos - self.cur_animal.rect_head.center()).length()
                    < self.cur_animal.rect_head.width()):
                    self.drag_position_head = pos - self.cur_animal.position_head
                
                if(self.cur_animal.rect_tail.contains(pos)):
                    self.drag_position_tail = pos - self.cur_animal.position_tail
         
        if(self.is_remove_mode_active):
            # remove mode
            for animal in self.animal_list:
                if(animal.boundingBox.contains(pos)):
                    # get index of animal in list
                    index = self.animal_list.index(animal)
                         
                    # if the current animal is to be removed, find a new current animal
                    if(animal == self.cur_animal):
                        # if the index is not the last one, set the next animal as current animal
                        if index != len(self.animal_list)-1:
                            self.cur_animal = self.animal_list[index+1]
                        elif index == len(self.animal_list)-1 and len(self.animal_list)>1:
                            self.cur_animal = self.animal_list[index-1]
                        else:
                            self.cur_animal = None
                    
                    # remove animal visuals from scene
                    self.imageArea._scene.removeItem(animal.boundingBox_visual)
                    self.imageArea._scene.removeItem(animal.head_item_visual)
                    self.imageArea._scene.removeItem(animal.tail_item_visual)
                    self.imageArea._scene.removeItem(animal.line_item_visual)
                    
                    # remove animal from list and data model if on left image
                    if self.image_ending == "*_L.jpg":
                        pos = self.models.model_animals.data.index.get_loc(animal.row_index)
                        self.models.model_animals.removeRows(pos, 1, QtCore.QModelIndex())
                    elif self.image_ending == "*_R.jpg":
                        # if animal is on right image, just modify entry
                        self.models.model_animals.data.loc[animal.row_index, "RX1"] = -1
                        self.models.model_animals.data.loc[animal.row_index, "RY1"] = -1
                        self.models.model_animals.data.loc[animal.row_index, "RX2"] = -1
                        self.models.model_animals.data.loc[animal.row_index, "RY2"] = -1

                    self.animal_list.remove(animal) 
                    break

        # if user is not removing and not adding animals, switch the current 
        # animal to what the user clicks on
        # if the user clicks on no organism, there is no current animal
        elif(not self.is_remove_mode_active and not self.is_add_mode_active):
            is_click_on_animal = False 
            for animal in self.animal_list:
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
                    self.animal_list.append(self.cur_animal)
                    
                    cur_image_path = self.imageArea.parent().image_list[self.imageArea.parent().cur_image_index]
                    image_remark = self.imageArea.parent().parent().comboBox_imgRemark.currentText()
                    experiment_id = self.imageArea.parent().parent().parent().parent().page_data.lineEdit_exp_id.text()
                    user_id = self.imageArea.parent().parent().parent().parent().page_settings.lineEdit_user_id.text()
                    
                    # if animal is on left image, create new row
                    if self.image_ending == "*_L.jpg":
                        self.models.model_animals.insertRows(
                            self.cur_animal.row_index, 1, 
                            [self.cur_animal], cur_image_path, 
                            image_remark, experiment_id, user_id)
                    elif self.image_ending == "*_R.jpg":
                        # if on right image, adapt current row
                        self.models.model_animals.data.loc[self.cur_animal.row_index, "RX1"] = self.cur_animal.original_pos_head.x()
                        self.models.model_animals.data.loc[self.cur_animal.row_index, "RY1"] = self.cur_animal.original_pos_head.y()
                        self.models.model_animals.data.loc[self.cur_animal.row_index, "RX2"] = self.cur_animal.original_pos_tail.x()
                        self.models.model_animals.data.loc[self.cur_animal.row_index, "RY2"] = self.cur_animal.original_pos_tail.y()
                else:                    
                    # create a new animal
                    self.cur_animal = Animal(self.models, 
                                             row_index=self.models.model_animals.data.index.max()+1,
                                             position_head=pos)
                    self.cur_animal.setGroup(AnimalGroup.UNIDENTIFIED)
                              
                    # calculate position in original format
                    self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                    
                    # do the actual drawing of the head
                    self.drawAnimalHead(self.cur_animal)
 
            else:                
                # create a new animal
                self.cur_animal = Animal(self.models, 
                                         row_index=self.models.model_animals.data.index.max()+1,
                                         position_head=pos)
                self.cur_animal.setGroup(AnimalGroup.UNIDENTIFIED)
                
                # calculate position in original format
                self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                
                # do the actual drawing of the head
                self.drawAnimalHead(self.cur_animal)

        self.updateBoundingBoxes()                     

    def mouseMoveEvent(self, event):
        """ When moving the mouse, adapt head/tail visual position when they
        are dragged. """
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        # if there is a head to draw and if the drag_position is within the widget, move the head
        if not self.drag_position_head.isNull() \
            and self.imageArea.rect().contains(pos) \
            and self.cur_animal is not None:         
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
        if not self.drag_position_tail.isNull() \
            and self.imageArea.rect().contains(pos) \
            and self.cur_animal is not None:
            self.cur_animal.setPositionTail(pos - self.drag_position_tail)
            
            # remove tail and line on old position and draw it on the new position
            self.removeTailVisual(self.cur_animal)
            self.removeLineVisual(self.cur_animal)  
            self.removeBoundingBoxVisual(self.cur_animal)
            self.drawAnimalTailLineBoundingBox(self.cur_animal)

            self.updateOriginalAnimalPosition(self.cur_animal)

            self.updateBoundingBoxes()            
            self.cur_animal.setManuallyCorrected(True)

    def mouseReleaseEvent(self, event):
        """ When releasing the mouse, reset the drag positions. """
        self.drag_position_head = QtCore.QPoint()
        self.drag_position_tail = QtCore.QPoint()

    def setOriginalWidthHeight(self, width=None, height=None):
        """
        Function to set the width and/or height of the original image used for
        coordinate transformations on animals.

        Parameters
        ----------
        width : int, optional
            Width of the original image in pixels. The default is None.
        height : int, optional
            Height of the original image in pixels. The default is None.
        """
        if width:
            self.original_img_width = width
        if height:
            self.original_img_height = height

    def updateAnimalPosition(self, animal):
        """ Recalculates the position of a given animal using its position on 
        the original image and the current size of the displayed image. """
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
        """ Calculates the position of a given animal on the original image by 
        transforming its position on the currently displayed image. """
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
            
            end = "L"
            if self.image_ending == "*_R.jpg": end = "R"
            
            # update data model
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"X1"] = self.cur_animal.original_pos_head.x()
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"Y1"] = self.cur_animal.original_pos_head.y()
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"X2"] = self.cur_animal.original_pos_tail.x()
            self.models.model_animals.data.loc[self.cur_animal.row_index, end+"Y2"] = self.cur_animal.original_pos_tail.y()


    def drawAnimalsFromList(self, animal_list, image_ending="_L"):
        """
        Draws animals from a dataframe on the current image. 

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
        
                length = float(animal_list["length"].iloc[i])
                
                # create a new animal
                self.cur_animal = Animal(self.models,
                                         row_index=animal_list.index[i],
                                         position_head=pos_h, 
                                         position_tail=pos_t,
                                         group=str(animal_list["group"].iloc[i]),
                                         species=str(animal_list["species"].iloc[i]),
                                         remark=animal_remark,
                                         length=length)
                
                # set the position in the original image     
                self.cur_animal.original_pos_head = original_pos_h
                self.cur_animal.original_pos_tail = original_pos_t
            
                # do the actual drawing of the head
                self.drawAnimalHead(self.cur_animal)
                self.drawAnimalTailLineBoundingBox(self.cur_animal)
                
                # append animal to list
                self.animal_list.append(self.cur_animal)   
                
                # update bounding boxes
                self.imageArea.animal_painter.updateBoundingBoxes()      
     
 