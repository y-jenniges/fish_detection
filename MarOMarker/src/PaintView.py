# panning and zoomin 
# https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import pandas as pd
import os
import math
import numpy as np
from functools import partial
from Animal import Animal, AnimalSpecificationsWidget
from Models import AnimalGroup, AnimalSpecies
from Helpers import getIcon, displayErrorMsg, MismatchDialog

      
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
    output_dir : string
        Directory where the output file is stored.
    cur_image_index : int
        Index of the current image in image_list.
    image_list : [list<string>, list<string>]
        List containing all image pathes that have the given prefix, are of the
        selected date. First entry contains all left image pathes and second
        entry all right image pathes.
    newImageLoaded: pyqtSignal
    """    
    
    newImageLoaded = QtCore.pyqtSignal(str)
    """ Signal that is emitted when a new image is loaded. """
    
    def __init__(self, models, imageDirectory, imagePrefix, outputDir="", 
                parent=None):
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
        parent : TYPE, optional
            The parent object. The default is None.
        """
        super(PhotoViewer, self).__init__(parent)

        # data models
        self.models = models

        # image directory and prefix (needed for retrieving the image_list)
        self.image_directory = imageDirectory
        self.image_prefix = imagePrefix
        self.output_dir = outputDir

        # list of image pathes and the current image index (load per default L image)
        self.cur_image_index = 0
        l_images_with_prefix = glob.glob(imageDirectory + imagePrefix + "*_L.jpg")
        r_images_with_prefix = glob.glob(imageDirectory + imagePrefix + "*_R.jpg")
        
        self.image_list = []
        if hasattr(self.parent().parent().parent(), 'page_data'):
            date = self.parent().parent().parent().page_data.\
                calendarWidget.selectedDate().toString("yyyy.MM.dd")
            
            self.image_list.append([x for x in l_images_with_prefix if date in x])
            self.image_list.append([x for x in r_images_with_prefix if date in x])
            
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
        
    def setImageEnding(self, text, imageArea=None):
        """ Adapt image ending in animal_painter and in self. Must be either
        '\*_L.jpg' or '\*_R.jpg'. """
        assert(text == "*_L.jpg" or text == "*_R.jpg")

        if imageArea:
            imageArea.animal_painter.image_ending = text
        else:
            self.imageArea.animal_painter.image_ending = text
            
        self.updateImageList()

    def on_add_animal(self, activate_add, is_remove_active):
        """
        Delegates query to (de-)activate the add mode to the correct 
        animal painters.

        Parameters
        ----------
        activate_add : bool
            Whether to activate the add mode or deactivate it.
        is_remove_active : bool
            Whether the remove mode is active or not.

        Returns
        -------
        is_add_activatable : bool
            Whether it is possible to activate the add mode.
        is_remove_active : bool
            Wheter the remove mode needs to be active or not.
        """
        a, d = self.imageAreaLR.imageAreaL.animal_painter.on_add_animal(
            activate_add, is_remove_active)
        b, e = self.imageAreaLR.imageAreaR.animal_painter.on_add_animal(
            activate_add, is_remove_active)
        c, f = self.imageArea.animal_painter.on_add_animal(
            activate_add, is_remove_active)
        
        is_add_activatable = a and b and c
        is_remove_active = d and e and f
        return is_add_activatable, is_remove_active

    def on_remove_animal(self, activate_remove, is_add_active):
        """
        Delegates query to (de-)activate the remove mode to the correct 
        animal painters.

        Parameters
        ----------
        activate_remove : bool
            Whether to activate the remove mode or deactivate it.
        is_add_active : bool
            Whether the add mode is active or not.

        Returns
        -------
        is_remove_activatable : bool
            Whether it is possible to activate the remove mode.
        is_add_active : bool
            Wheter the add mode needs to be active or not.
        """
        a, d = self.imageAreaLR.imageAreaL.animal_painter.on_remove_animal(
            activate_remove, is_add_active)
        b, e = self.imageAreaLR.imageAreaR.animal_painter.on_remove_animal(
            activate_remove, is_add_active)
        c, f = self.imageArea.animal_painter.on_remove_animal(
            activate_remove, is_add_active)
        
        is_remove_activatable = a and b and c
        is_add_active = d and e and f
        return is_remove_activatable, is_add_active
          
    def on_next_animal(self):
        """ Delegates the query to make the next animal active to the correct 
        animal painter by checking for the active image area. """
        if self.stackedWidget_imagearea.currentIndex() == 0:
            self.imageArea.animal_painter.on_next_animal()
        elif self.stackedWidget_imagearea.currentIndex() == 1:
            self.imageAreaLR.on_next_animal()
            
    def on_previous_animal(self):
        """ Delegates the query to make the previous animal active to the correct 
        animal painter by checking for the active image area. """
        if self.stackedWidget_imagearea.currentIndex() == 0:
            self.imageArea.animal_painter.on_previous_animal()
        elif self.stackedWidget_imagearea.currentIndex() == 1:
            self.imageAreaLR.on_previous_animal()  
    
    def activateImageMode(self, mode):
        """
        Showing either the left, right or both images in the GUI depending on
        the mode.

        Parameters
        ----------
        mode : string
            Can be either 'L', 'R' or 'LR'.
        """
        if mode == "L":
            self.stackedWidget_imagearea.setCurrentIndex(0)
            self.setImageEnding("*_L.jpg")
        elif mode == "R":
            self.stackedWidget_imagearea.setCurrentIndex(0)
            self.setImageEnding("*_R.jpg")
        elif mode == "LR":
            self.stackedWidget_imagearea.setCurrentIndex(1)
            self.setImageEnding("*_L.jpg")
        else:
            print("PhotoViewer: Unknown image mode.")

    def updateImageList(self):
        """ Recalculate image list, i.e. filter the image directory for images
        with the correct prefix and date. """
        l_images_with_prefix = glob.glob(self.image_directory 
                             + self.image_prefix + "*_L.jpg")
        r_images_with_prefix = glob.glob(self.image_directory 
                             + self.image_prefix + "*_R.jpg")
        
        if hasattr(self.parent().parent().parent(), 'page_data'):
            date = self.parent().parent().parent().page_data.\
                calendarWidget.selectedDate().toString("yyyy.MM.dd")
            # clear and refill image list
            self.image_list = [] 
            self.image_list.append([x for x in l_images_with_prefix if date in x])
            self.image_list.append([x for x in r_images_with_prefix if date in x])
        
        if not self.image_list:
            self.loadImageFromPath(path=None)
        else:
            self.loadImageFromIndex(self.cur_image_index)

    def resizeEvent(self, event):
        """ Resizes image and animal positions when resize event occurs. """
        super().resizeEvent(event)

        pathL = self.image_list[0][self.cur_image_index]
        pathR = self.image_list[1][self.cur_image_index]
        
        # if LR view is active, both image areas needs to be scaled
        if self.stackedWidget_imagearea.currentIndex() == 1:
            self._resizeView(pathL, self.imageAreaLR.imageAreaL)
            self._resizeView(pathR, self.imageAreaLR.imageAreaR)
        else:
            if self.imageArea.animal_painter.image_ending == "*_L.jpg":
                self._resizeView(pathL, self.imageArea)
            else:
                self._resizeView(pathR, self.imageArea)
                
    def _resizeView(self, path, imageArea):
        if self.cur_image_index < len(self.image_list[0]):
            # reload photo
            photo = QtGui.QPixmap(path).scaled(QtCore.QSize(
                imageArea.width(), imageArea.height()))
            imageArea.setPhoto(photo)
            
            self.updateImageCountVisual()
        
        imageArea.animal_painter.redraw()
        
    def loadImageFromIndex(self, index):
        """ Loads image at index in the image list into all views 
        (i.e. L, R and LR). """
        pathL = self.image_list[0][index]
        pathR = self.image_list[1][index]
        
        if self.stackedWidget_imagearea.currentIndex() == 0:
            if self.imageArea.animal_painter.image_ending == "*_L.jpg":
                self.loadSingleImage(pathL, self.imageArea)
            else:
                self.loadSingleImage(pathR, self.imageArea)
        elif self.stackedWidget_imagearea.currentIndex() == 1:
            self.loadSingleImage(pathL, self.imageAreaLR.imageAreaL)
            self.loadSingleImage(pathR, self.imageAreaLR.imageAreaR)
        
    def loadImageFromPath(self, path, imageArea=None):
        # if LR view is active, update both image views, else only the current one
        if self.stackedWidget_imagearea.currentIndex() == 1:
            # check if the path is for L or R image
            if path.endswith("_L.jpg"):
                pathL = path
                pathR = path.replace("_L.jpg", "_R.jpg")
            else:
                pathL = path.replace("_R.jpg", "_L.jpg")
                pathR = path
            
            self.loadSingleImage(pathL, self.imageAreaLR.imageAreaL)
            self.loadSingleImage(pathR, self.imageAreaLR.imageAreaR)
        else:
            self.loadSingleImage(path)        

    def loadSingleImage(self, path, imageArea=None):
        """ Loads an image from a path to the given imageArea and draws 
        available animals from output file. """
        
        if not imageArea:
            imageArea = self.imageArea
        
        if path:
            image = QtGui.QImage(path)
            photo = QtGui.QPixmap().fromImage(image).scaled(QtCore.QSize(
                imageArea.width(), imageArea.height()))
            imageArea.animal_painter.setOriginalWidthHeight(
                width=image.width(), height = image.height())
        else:
            photo = None
        
        imageArea.setPhoto(photo)
        self.updateImageCountVisual()
        
        # clear visuals
        imageArea.animal_painter.removeAll()
        
        # update animal list
        imageArea.animal_painter.animal_list.clear()
        
        # find current image in result file and draw all animals from it
        if self.models.model_animals.data is not None and path is not None:
            # find animals on current image
            cur_file_entries = self.models.model_animals.data[
                self.models.model_animals.data['file_id'] == \
                    os.path.basename(path).rstrip(".jpg").rstrip(".png").rstrip("_L").rstrip("_R")]
            
            # draw animals
            imageArea.animal_painter.drawAnimalsFromList(cur_file_entries)
            
            # load current image remark
            if len(cur_file_entries) > 0: 
                remark = str(cur_file_entries['image_remarks'].iloc[0])
                if remark == "nan": remark = ""
                self.newImageLoaded.emit(remark)
            
        # reset current animal, hide specs widget and update bounding boxes 
        # (none should be drawn since cur_animal is None)
        imageArea.animal_painter.cur_animal = None
        imageArea.animal_painter.widget_animal_specs.hide()
        imageArea.animal_painter.updateBoundingBoxes()    
    
    def exportToCsv(self, file_id):
        """ Updates the current CSV table. """
        main_window = self.parent().parent().parent()
        output_dir = main_window.page_data.lineEdit_output_dir.text()
        res_file_name = main_window.getResultFileName()
        self.models.model_animals.exportToCsv(output_dir, res_file_name, file_id)
        
    def on_next_image(self, imageArea=None):
        """ Loads the next image and draws animals accordingly. """
        if self.stackedWidget_imagearea.currentIndex() == 0:
            self.switchImage(self.cur_image_index+1, self.imageArea)
        elif self.stackedWidget_imagearea.currentIndex() == 1:
            self.switchImage(self.cur_image_index+1, self.imageAreaLR.imageAreaL)
            self.switchImage(self.cur_image_index, self.imageAreaLR.imageAreaR)

    def on_previous_image(self, imageArea=None):
        """ Loads the previous image and draws animals accordingly. """
        if self.stackedWidget_imagearea.currentIndex() == 0:
            self.switchImage(self.cur_image_index-1, self.imageArea)
        elif self.stackedWidget_imagearea.currentIndex() == 1:
            self.switchImage(self.cur_image_index-1, self.imageAreaLR.imageAreaL)
            self.switchImage(self.cur_image_index, self.imageAreaLR.imageAreaR)
            
    def switchImage(self, newIndex, imageArea=None):
        if not imageArea:
            imageArea = self.imageArea
            
        if not self.models.model_animals.isEmpty(): 
            # only go to another image if cur animal is none or complete
            cur_animal = imageArea.animal_painter.cur_animal

            if cur_animal is not None and \
            ((cur_animal.is_head_drawn and not cur_animal.is_tail_drawn) or \
             (not cur_animal.is_head_drawn and cur_animal.is_tail_drawn)):
                displayErrorMsg("Error", 
                                "Please draw head and tail before switching the image.", 
                                "Error")  
            # only go to new image if the given index is valid
            elif newIndex in range(len(self.image_list[0])):
                # current file_id
                cur_file_id = os.path.basename(
                    self.image_list[0][newIndex]).strip(".jpg"). \
                    strip(".png").strip("_L").strip("_R")
                
                # set current image to status "checked"
                cur_file_indices = self.models.model_animals.data[
                    self.models.model_animals.data['file_id'] ==  cur_file_id].index
                
                for idx in cur_file_indices:
                    self.models.model_animals.data.loc[idx, "status"] = "checked"
                    
                # get the new image and load it
                self.cur_image_index = newIndex
                self.cur_animal = None
                self.loadImageFromIndex(newIndex) 
                
                # update the previous image in the csv file
                self.exportToCsv(cur_file_id)        

    def updateImageCountVisual(self):
        """ Updates the display of the total number of images and the current 
        image index """
        if self.image_list:
            num_images = len(self.image_list[0])
            cur_image = self.cur_image_index
            self.label_imgCount.setText(str(cur_image+1) + "/" + str(num_images))

    def isAddModeActive(self):
        """
        Check if add mode is active in one of the image areas.

        Returns
        -------
        bool
            If the add mode is active or not.
        """
        # check if single image dsipaly is active or both (i.e. L/R or LR view)
        if self.stackedWidget_imagearea.currentIndex() == 0:
            # if L (or R) is active, check its imageArea
            if self.imageArea.animal_painter.is_add_mode_active:
                return True
        else:
            # if LR mode is active, check if add mode is active for one of the
            # image areas
            if self.imageAreaLR.imageAreaL.animal_painter.is_add_mode_active:
                return True
            elif self.imageAreaLR.imageAreaR.animal_painter.is_add_mode_active:
                return True       
        return False
            
    def isRemoveModeActive(self):
        """
        Check if remove mode is active in one of the image areas.

        Returns
        -------
        bool
            If the remove mode is active or not.
        """
        # check if single image dsipaly is active or both (i.e. L/R or LR view)
        if self.stackedWidget_imagearea.currentIndex() == 0:
            if self.imageArea.animal_painter.is_remove_mode_active:
                return True
        else:
            if self.imageAreaLR.imageAreaL.animal_painter.is_remove_mode_active:
                return True
            elif self.imageAreaLR.imageAreaR.animal_painter.is_remove_mode_active:
                return True
        return False
        
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
        self.frame_left = QtWidgets.QFrame(self)
        self.frame_left.setMinimumSize(QtCore.QSize(60, 0))
        self.frame_left.setMaximumSize(QtCore.QSize(60, 16777215))
        self.frame_left.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_left.setObjectName("frame_left")
  
        # layout
        layout_frame_left = QtWidgets.QVBoxLayout(self.frame_left)
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
        self.btn_previous_image = QtWidgets.QPushButton(self.frame_left)
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
        self.label_imgCount = QtWidgets.QLabel(self.frame_left)
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
        
        
        # --- stacked widget to display L, R or LR image(s) ----------------- # 
        self.stackedWidget_imagearea = QtWidgets.QStackedWidget(self)
        self.stackedWidget_imagearea.setLineWidth(0)
        self.stackedWidget_imagearea.setObjectName("stackedWidget")
        
        # image area to display left image OR right image
        self.imageArea = ImageArea(self.models, self)
        self.stackedWidget_imagearea.addWidget(self.imageArea)   
        
        # image area to display left and right images
        self.imageAreaLR = ImageAreaLR(self.models, self)
        self.stackedWidget_imagearea.addWidget(self.imageAreaLR)
             
        # initially display the view with only one image
        self.stackedWidget_imagearea.setCurrentIndex(0)


        # --- right frame --------------------------------------------------- # 
        # frame
        self.frame_right = QtWidgets.QFrame(self)
        self.frame_right.setMinimumSize(QtCore.QSize(60, 0))
        self.frame_right.setMaximumSize(QtCore.QSize(60, 16777215))
        self.frame_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_right.setObjectName("frame_right")
        
        # vertical spacers
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, 
                                            QtWidgets.QSizePolicy.Minimum, 
                                            QtWidgets.QSizePolicy.Expanding)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)
        
        # button for previous image
        self.btn_next_image = QtWidgets.QPushButton(self.frame_right)      
        self.btn_next_image.setIcon(getIcon(
            ":/icons/icons/arrow_right_big.png"))
        self.btn_next_image.setIconSize(QtCore.QSize(20, 40))
        self.btn_next_image.setObjectName("btn_next_image")
        
        # button for opening image in separate window
        # self.btn_openImg = QtWidgets.QPushButton(self.frame_right)
        # self.btn_openImg.setMinimumSize(QtCore.QSize(40, 40))
        # self.btn_openImg.setMaximumSize(QtCore.QSize(40, 40))
        # self.btn_openImg.setIcon(getIcon(":/icons/icons/open_image.png"))
        # self.btn_openImg.setIconSize(QtCore.QSize(30, 30))
        # self.btn_openImg.setObjectName("btn_openImg")
        
        # layout
        layout_frame_right = QtWidgets.QVBoxLayout(self.frame_right)
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
        self.layout.addWidget(self.frame_left)
        self.layout.addWidget(self.stackedWidget_imagearea)
        self.layout.addWidget(self.frame_right)

        # set main layout
        self.layout = self.layout
       
        
class ImageAreaLR(QtWidgets.QWidget):
    """
    A QWidget that handles the LR view, i.e. displays left and right images.
    
    Attributes
    ----------
    _models: Models
        Underlying data models containing the animal information.
    """
    def __init__(self, models, parent=None):
        super(ImageAreaLR, self).__init__(parent)
        
        self._models = models
        
        self._initUi()
        self._initActions()
        
        # if the left or  right image was lastly active (needed for iterating
        # through animals)
        self.last_active = "*_L.jpg"
        
        # the currently selected animal that needs to be matched and on which 
        # image it is
        self.animal_to_match = [None, "L"]
        
        if parent:
            self.parent().setImageEnding("*_L.jpg", self.imageAreaL)
            self.parent().setImageEnding("*_R.jpg", self.imageAreaR)
    
    def on_next_animal(self):
        """ Delegates the query to make next animal active to the lastly active
        image area (L or R). Also adapts the selection to have a matching pair 
        in both image areas active. """
        if self.last_active == "*_L.jpg":
            imageArea = self.imageAreaL
        elif self.last_active == "*_R.jpg":
            imageArea = self.imageAreaR
        
        # switch to next animal
        imageArea.animal_painter.on_next_animal()
        
        # update visuals on both image areas (so that both animals of a match
        # are selected
        self.redrawSelection()
    
    def on_previous_animal(self):
        """ Delegates the query to make next animal active to the lastly active
        image area (L or R). Also adapts the selection to have a matching pair 
        in both image areas active. """
        if self.last_active == "*_L.jpg":
            imageArea = self.imageAreaL
        elif self.last_active == "*_R.jpg":
            imageArea = self.imageAreaR
        
        # switch to next animal
        imageArea.animal_painter.on_previous_animal()
        
        # update visuals on both image areas (so that both animals of a match
        # are selected
        self.redrawSelection()
    
    def redrawSelection(self):   
        """ Finds the current animal (on the lastly active image area) and
        updates the bounding boxes of it and of its match on the right image. """
        if self.last_active == "*_L.jpg":
            imageArea = self.imageAreaL
            otherImageArea = self.imageAreaR
            image = "L"
        elif self.last_active == "*_R.jpg":
            imageArea = self.imageAreaR
            otherImageArea = self.imageAreaL
            image = "R"
            
        # find matching animal
        cur_animal = imageArea.animal_painter.cur_animal
        matching_animal = self.findAnimalMatch(cur_animal, image)
        
        # select matching animal and update bounding boxes
        otherImageArea.animal_painter.cur_animal = matching_animal
        otherImageArea.animal_painter.updateBoundingBoxes()  
        
        # update specs widget @todo
        self.updateSpecsWidget()
        
    def updateSpecsWidget(self):
        """ Updates the specs widget (on the side) with the currently active
        animal (either on left or right image). """
        # check if L or R view has an acitve current animal and update the specs widget
        if self.imageAreaL.animal_painter.cur_animal is not None:
            self.widget_animal_specs.setAnimal(self.imageAreaL.animal_painter.cur_animal)
        elif self.imageAreaR.animal_painter.cur_animal is not None:
            self.widget_animal_specs.setAnimal(self.imageAreaR.animal_painter.cur_animal)
        else:
            self.widget_animal_specs.setAnimal(None)
    
    def findAnimalMatch(self, animal, image="L"):
        """ Determines which animal object belongs to the given animal by 
        checking the data table and comparing head and tail coordinates.

        Parameters
        ----------
        animal : Animal
            Animal to find the match of.
        image : string
            Depicts whether the given animal is on the left ro right image.

        Returns
        -------
        matching_animal : Animal
            The matching animal. If none exists yet, None is returned.
        """
        if not animal: return
        
        if image == "R":
            coord = "L"
            imageArea = self.imageAreaL
        else:
            coord = "R"
            imageArea = self.imageAreaR
            
        # check if animal is in data model    
        if animal.row_index in self._models.model_animals.data.index:
            
            # check if animal has a match on right (left) image
            if self._models.model_animals.data.loc[animal.row_index, coord+'X1'] != -1:
                
                # get right (left) animal coordinates from data model
                position_head = QtCore.QPoint(
                    self._models.model_animals.data.loc[animal.row_index, coord+'X1'], 
                    self._models.model_animals.data.loc[animal.row_index, coord+'Y1'])
                position_tail = QtCore.QPoint(
                    self._models.model_animals.data.loc[animal.row_index, coord+'X2'], 
                    self._models.model_animals.data.loc[animal.row_index, coord+'Y2'])
                
                # check if any animal instance exists that has the same R (L) coordinates
                for matching_animal in imageArea.animal_painter.animal_list:
                    if matching_animal.original_pos_head == position_head  \
                    and matching_animal.original_pos_tail == position_tail:
                            return matching_animal
        return None
        
        
    def redrawLeftAnimal(self, animal):
        """ Given the right animal, redraw its matching left animal. """
        self.redrawAnimalMatch(animal, "R")
        
    def redrawRightAnimal(self, animal):
        """ Given the left animal, redraw its matching right animal. """
        self.redrawAnimalMatch(animal, "L")

    def redrawAnimalMatch(self, animal, image="L"):
        """
        Redraws the animal that is matched to the given animal (if existant). 

        Parameters
        ----------
        animal : Animal
            The animal whose counterpart is to be redrawn.
        image : string, optional
            Describes on which image the animal is located, i.e. on the right 
            ('R') or the left ('L') image. 
        """
        if image == "R":
            imageArea = self.imageAreaL
        else:
            imageArea = self.imageAreaR

        # find matching animal
        matching_animal = self.findAnimalMatch(animal, image)
        print(matching_animal)
        
        # if there is a matching animal, redraw it on the image area
        if matching_animal:
            print(matching_animal.group)
            # update properties of matching animal
            matching_animal.setGroup(animal.group)
            matching_animal.setSpecies(animal.species)
            matching_animal.setRemark(animal.remark)
            
            # remove matching animal visuals
            imageArea.animal_painter.removeAnimal(matching_animal, False)
            
            # redraw the visuals
            imageArea.animal_painter.drawAnimalHead(matching_animal)
            imageArea.animal_painter.drawAnimalTailLineBoundingBox(matching_animal)      
            imageArea.animal_painter.updateBoundingBoxes()     

        self.updateSpecsWidget()     
            
    def on_match_activated(self, is_active):
        #@todo
        print(f"match was clicked, photo viewer will go to match mode {is_active}")
        
        if is_active:
        # redraw the animals (make more transparent, add IDs to bounding boxes)
            self.imageAreaL.animal_painter.updateBoundingBoxes = self.imageAreaL.animal_painter.updateBoundingBoxesMatchMode
            self.imageAreaR.animal_painter.updateBoundingBoxes = self.imageAreaR.animal_painter.updateBoundingBoxesMatchMode
        else:
            self.imageAreaL.animal_painter.updateBoundingBoxes = self.imageAreaL.animal_painter.updateBoundingBoxesNormal
            self.imageAreaR.animal_painter.updateBoundingBoxes = self.imageAreaR.animal_painter.updateBoundingBoxesNormal
        
        # draw bounding boxes and IDs of all animals that have a match
        self.imageAreaL.animal_painter.updateBoundingBoxes()
        self.imageAreaR.animal_painter.updateBoundingBoxes() 
        
        # update specs widget  @todo needed here?
        self.updateSpecsWidget()
        
        # change behaviour of animal painters for mouse clicks (disable add/remove?)
        
    def _initUi(self):
        """ Defines and draws the UI elements. """
        # -- frame for the two images displayed below each other ------------ #
        layout_imageFrame = QtWidgets.QVBoxLayout(self)
        layout_imageFrame.setContentsMargins(0, 0, 0, 0)
        layout_imageFrame.setSpacing(0)
        layout_imageFrame.setObjectName("layout_imageFrame")
        
        self.imageAreaL = ImageArea(self._models, self)
        self.imageAreaR = ImageArea(self._models, self)
        
        spacer = QtWidgets.QSpacerItem(5, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)  
        
        layout_imageFrame.addWidget(self.imageAreaL)
        layout_imageFrame.addItem(spacer)
        layout_imageFrame.addWidget(self.imageAreaR)
        
        frame_image = QtWidgets.QFrame(self)
        frame_image.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_image.setLayout(layout_imageFrame)

        
        # -- frame for more options ----------------------------------------- #
        # layout for frame that should contain the specifications widget
        layout_specs = QtWidgets.QGridLayout(self)
        layout_specs.setObjectName("layout_specs")
        layout_specs.setAlignment(QtCore.Qt.AlignCenter)
        
        # frame to contain the specs widget
        frame_specs = QtWidgets.QFrame(self)
        frame_specs.setStyleSheet("QFrame{background-color:rgb(200, 200, 200);  border-radius: 3px; border: none;} ")
        frame_specs.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_specs.setLayout(layout_specs)
            
        # specification widget
        self.widget_animal_specs = AnimalSpecificationsWidget(self._models, self.imageAreaL)
        self.widget_animal_specs.setStyleSheet("QLabel{font:12pt 'Century Gothic'; color:black;} QComboBox QAbstractItemView {background-color:white;border:None;selection-background-color: rgb(0, 203, 221);}")
        self.widget_animal_specs.show()
        
        # add specs widget to specs layout
        layout_specs.addWidget(self.widget_animal_specs) 
        
        # layout for the options frame
        layout_options = QtWidgets.QVBoxLayout(self)
        layout_options.setContentsMargins(7, 7, 7, 7)
        layout_options.setSpacing(0)
        layout_options.setObjectName("layout_options")
        
        # spacer
        spacer1 = QtWidgets.QSpacerItem(5, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)  
        
        # add widgets to options frame
        layout_options.addWidget(frame_specs)
        layout_options.addItem(spacer1)
        
        # put options layout into a frame
        frame_options = QtWidgets.QFrame(self)
        frame_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_options.setLayout(layout_options)
        
        # main layout
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("layout")
        
        # adding widgets to main layout 
        self.layout.addWidget(frame_image)
        self.layout.addWidget(frame_options)
        
        # set main layout
        self.setLayout(self.layout)
    
    def updateDrawnAnimal(self, animal):
        """ Given the animal stored in the specs widget (on the side), this 
        function updates the corresponding animal on left and right image. """
        print("update drawn animal")
        if self.imageAreaL.animal_painter.cur_animal is not None:
            painter = self.imageAreaL.animal_painter
            image = "L"
        elif self.imageAreaR.animal_painter.cur_animal is not None:
            painter = self.imageAreaR.animal_painter
            image = "R"
        else:
            return
        
        # update properties of current animal
        painter.cur_animal.setGroup(animal.group)
        painter.cur_animal.setSpecies(animal.species)
        painter.cur_animal.setRemark(animal.remark)
        
        # remove animal visuals
        painter.removeAnimal(painter.cur_animal, False)
        
        # redraw the visuals
        painter.drawAnimalHead(painter.cur_animal)
        painter.drawAnimalTailLineBoundingBox(painter.cur_animal)      
        painter.updateBoundingBoxes() 
        
        # redraw matching animal
        self.redrawAnimalMatch(painter.cur_animal, image)
    
    def handleMatching(self, image="L"):#@todo
        # image: on which image the selection occrued
        
        # find parent home page
        if hasattr(self.parent().parent().parent(), "is_match_animal_active"):
            parent = self.parent().parent().parent()
        else:
            return
        
        # check if the match mode is active
        if parent.is_match_animal_active:
            # check on which image area the selected animal is located
            if image == "L":
                imageArea = self.imageAreaL
            else:
                imageArea = self.imageAreaR
             
            # determine selected animal
            animal = imageArea.animal_painter.cur_animal
            
            # check if there has already been one animal selected and waits for its match
            if self.animal_to_match[0] is None:           
                # set animal to match
                self.animal_to_match = [animal, image]
                print("set animal to match")

            else:
                # an animal waits for its match
                # if the new selection occured on the same image as the 
                # waiting match, the new selection will be waiting for a match now
                if image == self.animal_to_match[1]:
                    self.animal_to_match = [animal, image]
                    self.imageAreaL.animal_painter.updateBoundingBoxes()
                    self.imageAreaR.animal_painter.updateBoundingBoxes()
                    print("switch animal to match")
                    return
                
                # match the active and the lastly selected animal
                if animal is not None:
                    if image == "L":
                        match_successfull = self.matchAnimals(animal, self.animal_to_match[0])
                    elif image == "R":
                        match_successfull = self.matchAnimals(self.animal_to_match[0], animal) 
                    
                    #if match_successfull:
                    # set the animal waiting to be matched to None #@todo do i need this?
                    self.animal_to_match[0] = None
                    
                    if not match_successfull:
                        self.imageAreaL.animal_painter.cur_animal = None
                        self.imageAreaR.animal_painter.cur_animal = None
                
                # update the visuals, i.e. IDs, bounding boxes on both images
                self.redrawSelection()
     
    def handleDifferentGroup(self, animal_L, animal_R):
        text = "You are about to match two animals that have a different group. \nWhich group do you want to keep?"
        dlg = MismatchDialog("Groups do not match", text, animal_L.group, animal_R.group, None, self)
        answer = dlg.exec_()
        
        if answer == -1:
            print("handling differnt group: return false")
            return False
        elif answer == 0:
            animal_R.setGroup(animal_L.group)
            self.imageAreaR.animal_painter.redrawAnimal(animal_R)
        elif answer == 1:
            animal_L.setGroup(animal_R.group)
            self.imageAreaL.animal_painter.redrawAnimal(animal_L)
            
        return True
        
    def handleDifferentSpecies(self, animal_L, animal_R):
        text = "You are about to match two animals that have a different species. \nWhich species do you want to keep?"
        dlg = MismatchDialog("Species do not match", text, animal_L.species, animal_R.species, None, self)
        answer = dlg.exec_()
        
        if answer == -1:
            return False
        elif answer == 0:
            animal_R.setSpecies(animal_L.species)
        elif answer == 1:
            animal_L.setSpecies(animal_R.species)
    
        return True
    
    def handleDifferentRemark(self, animal_L, animal_R):
        text = "You are about to match two animals that have different remarks. \nWhich remark do you want to keep?"
        dlg = MismatchDialog("Remarks do not match", text, animal_L.remark, animal_R.remark, "Merge remarks", self)
        answer = dlg.exec_()
        
        if answer == -1:
            return False
        elif answer == 0:
            animal_R.setRemark(animal_L.remark)
        elif answer == 1:
            animal_L.setRemark(animal_R.remark)
        elif answer == 2:
            animal_R.setRemark(animal_L.remark + ", " + animal_R.remark)
            animal_L.setRemark(animal_L.remark + ", " + animal_R.remark)
            
        return True
    
    # def handleDifferentLength(self, animal_L, animal_R):
    #     pass
    
    def matchAnimals(self, animal_L, animal_R):
        print("match called")
        # if group, species, remark, length, other props are different, then what?
        if str(animal_L.group) != str(animal_R.group):
            print(f"animals do not have the same group {animal_L.group, animal_R.group}")
            if not self.handleDifferentGroup(animal_L, animal_R): return False
                   
        if str(animal_L.species) != str(animal_R.species):
            print(f"animals do not have the same species {animal_L.species, animal_R.species}")
            if not self.handleDifferentSpecies(animal_L, animal_R): return False
            
        if str(animal_L.remark) != str(animal_R.remark):
            print(f"animals do not have the same remark {animal_L.remark, animal_R.remark}")
            if not self.handleDifferentRemark(animal_L, animal_R): return False
            
        # if str(animal_L.length) != str(animal_R.length): # länge muss sowieso neu berechnet werden bei einer match änderung
        #     print(f"animals do not have the same length {animal_L.length, animal_R.length}")
        #     if not self.handleDifferentLength(animal_L, animal_R): return False

        # remove old matches - there are 4 cases (for this we need to adapt the data model and the animal instances)
        # left animal has no right coordinates, right animal has no left coordinates
        if self._models.model_animals.data.loc[animal_L.row_index, "RX1"] == -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] == -1:
            self.match(animal_L, animal_R)
        
        # left animal has right coordinates, right animal doesnt have left coordinates
        elif self._models.model_animals.data.loc[animal_L.row_index, "RX1"] != -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] == -1:
            # find old animal that represents curent right coordinates  
            cur_right_animal = self.findAnimalMatch(animal_L, "L")
            
            # create separate data row for olf right animal
            self.createSeparateDataRow(cur_right_animal, image="R")
            
            # replace right animal
            self.match(animal_L, animal_R)
            
        # left animal has no right coordinates, right animal has left coordinates
        elif self._models.model_animals.data.loc[animal_L.row_index, "RX1"] == -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] != -1:           
            # find old animal that represents curent left coordinates  
            cur_left_animal = self.findAnimalMatch(animal_R, "R")
            
            # create separate data row for old right animal
            self.createSeparateDataRow(cur_left_animal, image="L")
            
            # replace right animal
            self.match(animal_L, animal_R)
    
        
        # left animal has right coordinates, right animal has left coordinates
        elif self._models.model_animals.data.loc[animal_R.row_index, "RX1"] != -1 \
        and self._models.model_animals.data.loc[animal_R.row_index, "LX1"] != -1:
            # find old animal that represents curent right coordinates  
            cur_right_animal = self.findAnimalMatch(animal_L, "L")
            cur_left_animal = self.findAnimalMatch(animal_R, "R")
            
             # create separate data rows for old left and right animal
            self.createSeparateDataRow(cur_right_animal, image="R")
            self.createSeparateDataRow(cur_left_animal, image="L")
            
            # replace animals
            self.match(animal_L, animal_R)
        
        # recalculate length of animals (this changes when different animals are matched)
        self.parent().parent().parent().parent().parent().page_data.onCalcLength()
        
        return True
    
    def createSeparateDataRow(self, animal, image="L"):  
        """
        Adds a row at the end of the data table for the given animal.

        Parameters
        ----------
        animal : Annimal
            The animal to create a data row for.
        image : string
            Either "L" or "R", depending on which image the animal is located. 
            The default is "L".
        """
        # get experiment settings
        image_path = self._models.model_animals.data.loc[animal.row_index, "file_id"] + "_R.jpg"  
        image_remark = self._models.model_animals.data.loc[animal.row_index, "image_remarks"]
        experiment_id = self._models.model_animals.data.loc[animal.row_index, "experiment_id"]
        user_id = self._models.model_animals.data.loc[animal.row_index, "user_id"]
        
        # add a data row for the animal
        animal.row_index = self._models.model_animals.data.index.max() + 1
        
        self._models.model_animals.insertRows(animal.row_index, int(1), 
                                              [animal], image_path, image_remark, 
                                              experiment_id, user_id, image)
            
    def match(self, animal_L, animal_R):
        """
        Adapting match information in the data table and updating the indeces
        of the given animals.

        Parameters
        ----------
        animal_L : Animal
            Animal on left image.
        animal_R : Animal
            Animal on right image.
        """

        if animal_L is not None:
            animal = animal_L
            match = animal_R
            image = "R" # adapt right coordinates
        elif animal_R is not None:
            animal = animal_R
            match = animal_L
            image = "L" # adapt left coordinates
        else:
            return
             
        # in case no match is given, set the coordinates to adapt to default (-1)
        if match is None:
            self._models.model_animals.data.loc[animal.row_index, image+"X1"] = -1
            self._models.model_animals.data.loc[animal.row_index, image+"Y1"] = -1
            self._models.model_animals.data.loc[animal.row_index, image+"X2"] = -1
            self._models.model_animals.data.loc[animal.row_index, image+"Y2"] = -1
        else:
            # merge the new animal coordinates to the original animal
            self._models.model_animals.data.loc[animal.row_index, image+"X1"] = self._models.model_animals.data.loc[match.row_index, image+"X1"]
            self._models.model_animals.data.loc[animal.row_index, image+"Y1"] = self._models.model_animals.data.loc[match.row_index, image+"Y1"]
            self._models.model_animals.data.loc[animal.row_index, image+"X2"] = self._models.model_animals.data.loc[match.row_index, image+"X2"]
            self._models.model_animals.data.loc[animal.row_index, image+"Y2"] = self._models.model_animals.data.loc[match.row_index, image+"Y2"]
    
            # remove new animal entry from data model
            pos = self._models.model_animals.data.index.get_loc(match.row_index)
            self._models.model_animals.removeRows(pos, 1, QtCore.QModelIndex())        
                  
            # update row index of new right animal 
            match.row_index = animal.row_index
        
    def _initActions(self):
        """ Defines the actions possible on the ImageAreaLR. """
        self.imageAreaL.animal_painter.propertyChanged.connect(self.redrawRightAnimal)
        self.imageAreaR.animal_painter.propertyChanged.connect(self.redrawLeftAnimal)
        
        self.imageAreaL.animal_painter.animalSelectionChanged.connect(self.redrawSelection)
        self.imageAreaR.animal_painter.animalSelectionChanged.connect(self.redrawSelection)
        
        self.widget_animal_specs.propertyChanged.connect(self.updateDrawnAnimal)
        
        self.imageAreaL.animal_painter.animalSelectionChanged.connect(partial(self.handleMatching, "L"))
        self.imageAreaR.animal_painter.animalSelectionChanged.connect(partial(self.handleMatching, "R"))
        

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
        
            # find the photo viewer in the parent tree
            parent = None
            if isinstance(self.parent().parent().parent().parent(), PhotoViewer):
                parent = self.parent().parent().parent().parent()
            elif isinstance(self.parent().parent(), PhotoViewer):
                parent = self.parent().parent()
            else:
                print("ImageArea: Could not find PhotoViewer as parent and \
                      could therefore not (de-) activate arrow shortcuts.")
                print(self.parent())
                return
            
            # scale the view if zoom is positive, else set it to zero and fit 
            # the photo in the view
            if self._zoom > 0:
                self.scale(factor, factor)
                parent.setArrowShortcutsActive(False)
            elif self._zoom == 0:
                self._fitInView()
                parent.setArrowShortcutsActive(True)
            else:
                self._zoom = 0
                parent.setArrowShortcutsActive(True)
                    
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
                
    def enterEvent(self, event):
        """ Defines behaviour when cursor enters image area. """
        self.animal_painter.shortcut_deselect_animal.setEnabled(True)

        # tell imageAreaLR that this imageArea is active
        if isinstance(self.parent().parent(), ImageAreaLR): 
            self.parent().parent().last_active = self.animal_painter.image_ending
        
    def leaveEvent(self, event):
        """ Defines behaviour when cursor leaves image area. """
        self.animal_painter.shortcut_deselect_animal.setEnabled(False)


class AnimalPainter(QtCore.QObject):
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
    propertyChanged : pyqtSignal
    animalSelectionChanged : pyqtSignal
    """
    # define custom signals
    propertyChanged = QtCore.pyqtSignal(Animal)
    """ Signal emitted when the group or species of an animal is changed. """
    
    animalSelectionChanged = QtCore.pyqtSignal()
    """ Signal emitted when animal selection changed. """
    
    def __init__(self, models, imageArea, parent=None):
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
        super(AnimalPainter, self).__init__(parent)
        
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
        
        # the QGraphicsView to paint on
        self.imageArea = imageArea
        
        # left or right image
        self.image_ending = "*_L.jpg"
        
        # original size of image (needed for resizing, i.e. recalculating 
        # coordinates)
        self.original_img_width = 0
        self.original_img_height = 0
        
        # function to update the bounding boxes
        self.updateBoundingBoxes = self.updateBoundingBoxesNormal
        
        # remember the group and species of the most recently adapted animal
        self._previous_group = AnimalGroup.UNIDENTIFIED
        self._previous_species = AnimalSpecies.UNIDENTIFIED
        
        # setup shortcuts
        self.shortcut_deselect_animal = QtWidgets.QShortcut(
            QtGui.QKeySequence("Escape"), self.imageArea, self.deselectAnimal) 
    
    def setAnimalRemark(self, remark):
        """ Sets the remark of the currently active animal. """
        if self.cur_animal is not None:
            self.cur_animal.setRemark(remark)   
            
            self.propertyChanged.emit(self.cur_animal)  
    
    def setAnimalSpecies(self, species):
        """ Sets the species of the currently active animal. """
        if self.cur_animal is not None:
            self.cur_animal.setSpecies(species)
            self._previous_species = species
            
            self.propertyChanged.emit(self.cur_animal)  
            
    def setAnimalGroup(self, group):
        """ Sets the group of the currently active animal and adapts the 
        visuals accordingly. """
        if self.cur_animal is not None:
            self.cur_animal.setGroup(group) 
            
            # use this group for animals that are added after this animal
            self._previous_group = group
            
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
            
            # redraw ID
            self.imageArea._scene.removeItem(self.cur_animal.id_visual)
            self.drawAnimalId(self.cur_animal)
            
            self.propertyChanged.emit(self.cur_animal)   
     
    def redraw(self):
        """ Redraws all animals on the current image. """
        # remove animals
        self.removeAll()
        
        # redraw animals
        for animal in self.animal_list:
            # update positions
            self.updateAnimalPosition(animal)
            
            # redraw animals
            self.drawAnimalHead(animal)
            self.drawAnimalTailLineBoundingBox(animal)
                    
        self.updateBoundingBoxes() 
    
    def removeAll(self, remove_from_list=False):
        """ Removes visuals of all animals and its storage in the list if 
        desired. """
        for animal in self.animal_list:
            self.removeAnimal(animal, remove_from_list)
          
    def removeAnimal(self, animal, remove_from_list=False):
        """ Removes given animal visually and from list. """
        self.removeHeadVisual(animal)
        self.removeTailVisual(animal)
        self.removeLineVisual(animal)
        self.removeBoundingBoxVisual(animal)
        self.removeIdVisual(animal)
        
        animal.is_head_drawn = False
        animal.is_tail_drawn = False
        
        if remove_from_list:
            self.animal_list.remove(animal)
     
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
            
            # move the specs to the bottom left corner of the animal bounding box
            self.widget_animal_specs.move(pos)
            
            # 8 possible placements of specs that are checked one after the other
            # 1. specs below animal
            top_left = pos + QtCore.QPoint(0, 0)
            result, visibility_areas = self.checkVisibility(top_left, None)
            if result: return
            
            # 2. specs left of animal
            top_left = pos + QtCore.QPoint(-self.widget_animal_specs.width(), -self.cur_animal.boundingBox_visual.rect().height())
            result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
            if result: return
            
            # 3. specs above animal
            top_left = pos + QtCore.QPoint(0, -self.cur_animal.boundingBox_visual.rect().height()-self.widget_animal_specs.height())
            result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
            if result: return
            
            # 4. specs right of animal
            top_left = pos + QtCore.QPoint(self.cur_animal.boundingBox_visual.rect().width(), -self.cur_animal.boundingBox_visual.rect().height())
            result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
            if result: return

            # 5. specs on top left corner
            top_left = pos + QtCore.QPoint(-self.widget_animal_specs.width(), -self.cur_animal.boundingBox_visual.rect().height()-self.widget_animal_specs.height())
            result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
            if result: return
                       
            # 6. specs on top right corner
            top_left = pos + QtCore.QPoint(self.cur_animal.boundingBox_visual.rect().width(), -self.cur_animal.boundingBox_visual.rect().height()-self.widget_animal_specs.height())
            result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
            if result: return
            
            # 7. specs on bottom left corner
            top_left = pos + QtCore.QPoint(-self.widget_animal_specs.width(), 0)
            result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
            if result: return
            
            # 8. specs on bottom right corner
            top_left = pos + QtCore.QPoint(self.cur_animal.boundingBox_visual.rect().width(), 0)
            result, visibility_areas = self.checkVisibility(top_left, visibility_areas)
            if result: return
            
            # if none of the methods was chosen, check which yields most
            # visibility (i.e. maximum visible area) of the specs widget
            max_area_index = visibility_areas[:,0].argmax()
            top_left = visibility_areas[max_area_index, 1]
            self.widget_animal_specs.move(top_left)
               
    def checkVisibility(self, top_left, visibility_areas=None):
        """
        Checks which corners of the specs widget, i.e. a QRect specified by it's 
        top left corner position) are visible and how much area of the specs is 
        visible in the current image area.

        Parameters
        ----------
        top_left : QPoint
            Top left corner position of the animal specification widget.
        visibility_areas : np.array<int, QPoint>, optional
            List of top left corners specifying the specs widget, as well as the
            corresponding visible area. If given, the new position and area will 
            be stacked on this array. The default is None. 

        Returns
        -------
        bool
            Whether all 4 corners of the specs widget are visible.
        visibility_areas : np.array<int, QPoint>
            The area of the specs widget that is visible in the image area and 
            the top left corner of the specs widget specifying its position.
        """
        # determine which area of the specs is visible
        rect = QtCore.QRect(top_left, QtCore.QSize(self.widget_animal_specs.width(), self.widget_animal_specs.height()))
        intersection_rect = rect.intersected(self.imageArea.rect())
        area = intersection_rect.width()*intersection_rect.height()
        visibility_area = np.array([area, top_left])     
        
        # stack visibility areas if some are given
        if visibility_areas is None: 
            visibility_areas = visibility_area
        else:
            visibility_areas = np.vstack((visibility_areas, visibility_area))
        
        # check which and how many corners are visible for the given top left corner
        if self.checkVisibleCorners(top_left)[0] == 4: 
            self.widget_animal_specs.move(top_left)
            return True, visibility_areas
        
        return False, visibility_areas
            
    def checkVisibleCorners(self, top_left=None):
        """
        Checks which corners of the specs widget (specified by it's top left 
        corner) are visible on the image area.

        Parameters
        ----------
        top_left : QPoint, optional
            Top left corner position of the specs widget. If not given, its
            current position is assumed. The default is None.

        Returns
        -------
        count : int
            Number of visible corners.
        tl : bool
            Whether the top left corner is visible.
        tr : bool
            Whether the top right corner is visible.
        bl : bool
            Whether the bottom left corner is visible.
        br : bool
            Whether the bottom right corner is visible.
        """
        
        # if top left corner is not specified, get the coordinates from the 
        # specs widget in the scene
        if not top_left:
            # get corners of specs widget in scene coordinates
            top_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topLeft())).toPoint()
            top_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().topRight())).toPoint()
            bottom_left = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomLeft())).toPoint()
            bottom_right = self.imageArea.mapToScene(self.widget_animal_specs.mapToParent(self.widget_animal_specs.rect().bottomRight())).toPoint()
        else:
            # calculate positions of the corners given the top left one
            bottom_left = top_left + QtCore.QPoint(0, self.widget_animal_specs.height())
            top_right = top_left + QtCore.QPoint(self.widget_animal_specs.width(), self.widget_animal_specs.height())
            bottom_right = top_left + QtCore.QPoint(self.widget_animal_specs.width(), 0)
       
        # init return variables
        count = 0
        tl = False
        tr = False
        bl = False
        br = False
        
        # check which corners are visible
        if self.imageArea.rect().contains(top_left): 
            count = count +1
            tl = True
        if self.imageArea.rect().contains(top_right): 
            count = count +1
            tr = True
        if self.imageArea.rect().contains(bottom_left): 
            count = count +1
            bl = True
        if self.imageArea.rect().contains(bottom_right): 
            count = count +1
            br = True
        
        return count, tl, tr, bl, br
                 
    def updateBoundingBoxesNormal(self):
        """ Removes bounding box visuals for all animals and draws only the 
        one of the current animal. """
        # remove bounding of other animals
        for animal in self.animal_list:
            self.imageArea._scene.removeItem(animal.boundingBox_visual)
            animal.boundingBox_visual = None
            
            # set colour to full opacity
            animal.color.setAlpha(255)
            
            # remove ID
            self.imageArea._scene.removeItem(animal.id_visual)
            animal.id_visual = None

        # draw the current animal bounding box
        if self.cur_animal is not None and self.cur_animal in self.animal_list:
            self.cur_animal.boundingBox_visual = self.imageArea._scene.addRect(
                self.cur_animal.boundingBox, QtGui.QPen(self.cur_animal.color, 2, QtCore.Qt.SolidLine))
            
            self.widget_animal_specs.setAnimal(self.cur_animal)
            self.placeSpecsWidget()
            self.widget_animal_specs.show()
        else:
            self.widget_animal_specs.hide()
    
    def updateBoundingBoxesMatchMode(self):
        """ Draws boundingg boxes as needed in the match mode (i.e. draws a 
        (more transparent) bounding box and an ID for every animal that has a 
        match). """
        
        # hide specs widget
        self.widget_animal_specs.hide()
    
        for animal in self.animal_list:
            # remove old bounding box from scene
            self.imageArea._scene.removeItem(animal.boundingBox_visual)
            animal.boundingBox_visual = None
            
            # remove ID
            self.imageArea._scene.removeItem(animal.id_visual)
            animal.id_visual = None
                           
            # only drawbounding boxes of animals that are annotated on both images
            if self.models.model_animals.data.loc[animal.row_index, "RX1"] != -1 \
            and self.models.model_animals.data.loc[animal.row_index, "LX1"] != -1:
                # current animal (that has a match)
                if animal == self.cur_animal:
                    # set colour to full opacity
                    animal.color.setAlpha(255)
                    
                    # draw the new bounding box
                    animal.boundingBox_visual = self.imageArea._scene.addRect(
                        animal.boundingBox, QtGui.QPen(animal.color, 5, QtCore.Qt.SolidLine))
                else:
                    # for all other animals with match, set a more transparent color
                    animal.color.setAlpha(70)
                         
                    # add new bounding box to scene
                    animal.boundingBox_visual = self.imageArea._scene.addRect(
                        animal.boundingBox, QtGui.QPen(animal.color, 5, QtCore.Qt.SolidLine))
                
                # only draw IDs for animals with a match
                self.drawAnimalId(animal) # @todo
            
            # draw bounding box of current animal (without match) a bit thinner
            # than animals that have a match
            elif animal == self.cur_animal:
                # set colour to full opacity
                    animal.color.setAlpha(255)
                    
                    # draw the new bounding box
                    animal.boundingBox_visual = self.imageArea._scene.addRect(
                        animal.boundingBox, QtGui.QPen(animal.color, 2, QtCore.Qt.SolidLine))

    def drawAnimalId(self, animal):
        """ Draws the IDs of a given animal if the match mode is active. """
        # find page home (as parent of photoviewer)
        if isinstance(self.imageArea.parent().parent().parent().parent(), PhotoViewer):
            parent = self.imageArea.parent().parent().parent().parent().parent()
        elif isinstance(self.imageArea.parent().parent().parent().parent().parent().parent(), PhotoViewer):
            parent = self.imageArea.parent().parent().parent().parent().parent().parent().parent()
        else:
            print("AnimalPainter: Could not find PageHome parent.")
            return
        
        # only draw IDs if match mode is active
        if parent.is_match_animal_active:
            if animal != None:
                # the animal ID is its row index in the data table
                animal_id = animal.row_index
                
                # get top left corner of bounding box
                top_left = animal.boundingBox_visual.rect().topLeft()
                
                # draw ID
                font = QtGui.QFont("Century Gothic", 12, QtGui.QFont.Bold) 
                
                # create text visual
                animal.id_visual = self.imageArea._scene.addSimpleText(str(animal_id), font)
                
                # draw the ID in the animal's colour (full opacity)
                animal.color.setAlpha(255)
                animal.id_visual.setBrush(animal.color)
                
                # draw a black outline around the ID for better visibility
                animal.id_visual.setPen(QtCore.Qt.black)
                
                # move the ID visual to the top left position of the bounding box
                animal.id_visual.setPos(top_left - QtCore.QPoint(0, 2*font.pointSize()))

    def drawAnimalHead(self, animal):
        """ Draws the head of a given animal. """
        if animal != None:
            if animal.position_head != QtCore.QPoint(-1,-1):
                # draw the head visual
                self.imageArea._scene.addItem(animal.createHeadVisual())
     
    def drawAnimalLine(self, animal):
        """ Draws the line between head an tail of a given animal. """
        # set colour to full opacity
        animal.color.setAlpha(255)
        
        # draw line
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
      
    def removeIdVisual(self, animal):
        """ Removes the ID visual on the image of a given animal. """
        self.imageArea._scene.removeItem(animal.id_visual)
        animal.id_visual = None
        
    def on_next_animal(self):
        """ Makes the next animal in the animal_list active. """
        # if no animal ist selected, then select first one
        if self.cur_animal is None and len(self.animal_list) > 0:
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
        # if no animal is selected, then select last one
        if self.cur_animal is None and len(self.animal_list) > 0:
            self.cur_animal = self.animal_list[-1] 
            
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

    def on_remove_animal(self, activate_remove, is_add_active):
        """ Handles the activation state of the remove mode. 

        Parameters
        ----------
        activate_remove : bool
            Whether to activate the remove mode or deactivate it.
        is_add_active : bool
            Whether the add mode is active or not.

        Returns
        -------
        is_remove_activatable : bool
            Whether it is possible to activate the remove mode.
        is_add_active : bool
            Wheter the add mode needs to be active or not.
        """ 
        if not activate_remove:
            return False, is_add_active       
        elif is_add_active:
            # only deactivate add mode is animal is drawn completely
            if not self.cur_animal \
            or (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                return True, False   
            else:
                displayErrorMsg("Error", 
                                "Please draw head and tail before switching off the Add-mode.", 
                                "Error")           
        else:
            return True, False       

    def on_add_animal(self, activate_add, is_remove_active): 
        """ Handles the activation state of the add mode. 
        
        Parameters
        ----------
        activate_add : bool
            Whether to activate the add mode or deactivate it.
        is_remove_active : bool
            Whether the remove mode is active or not.

        Returns
        -------
        is_add_activatable : bool
            Whether it is possible to activate the add mode.
        is_remove_active : bool
            Wheter the remove mode needs to be active or not.
        """
        # if add mode is to be turned off
        if not activate_add:
            # the add mode can only be deactivated when head and tail are drawn 
            # or none of them is drawn
            if self.cur_animal is not None:
                if (self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn) \
                    or (not self.cur_animal.is_head_drawn and not self.cur_animal.is_tail_drawn):
                        return False, is_remove_active
                else:
                    displayErrorMsg("Error", 
                                    "Please draw head and tail before switching off the Add-mode.", 
                                    "Error")
            else:
                return False, is_remove_active
        else:
            return True, False
            
    def deselectAnimal(self):
        """ Deselects the current animal. """
        self.cur_animal = None
        self.updateBoundingBoxes()  
        
    def redrawAnimal(self, animal):
        """ Redraws the given animal. """
        # remove visuals of the animal
        self.removeAnimal(animal, False)
        
        # redraw visuals of animal
        self.drawAnimalHead(animal)
        self.drawAnimalTailLineBoundingBox(animal)
        
    def mousePressEvent(self, event):
        """ Handles the painting options on the image: Enables dragging of
        head/tail visuals, as well as removing/adding animals on click. """
        # convert event position to scene corrdinates
        pos = self.imageArea.mapToScene(event.pos()).toPoint()
        
        # find photo viewer parent
        if isinstance(self.imageArea.parent().parent(), PhotoViewer):
            parent = self.imageArea.parent().parent()
        elif isinstance(self.imageArea.parent().parent().parent().parent(), PhotoViewer):
            parent = self.imageArea.parent().parent().parent().parent()
        else:
            print("AnimalPainter: Could not find PhotoViewer parent.")
            return
        
        # get states of add and remove modes from home page
        is_add_mode_active = parent.parent().is_add_animal_active
        is_remove_mode_active = parent.parent().is_remove_animal_active
        is_match_animal_active = parent.parent().is_match_animal_active
        
        # enable dragging for current animal (when add mode is not active and 
        # the current animal is completey drawn)
        if self.cur_animal is not None and not is_add_mode_active:
            if(self.cur_animal.is_head_drawn and self.cur_animal.is_tail_drawn):
                if (2 * QtGui.QVector2D(pos - self.cur_animal.rect_head.center()).length()
                    < self.cur_animal.rect_head.width()):
                    self.drag_position_head = pos - self.cur_animal.position_head
                
                if(self.cur_animal.rect_tail.contains(pos)):
                    self.drag_position_tail = pos - self.cur_animal.position_tail
         
        if(is_remove_mode_active):
            # remove mode
            for animal in self.animal_list:
                if(animal.boundingBox.contains(pos)):
                    # get index of animal in list
                    index = self.animal_list.index(animal)
                         
                    # if the current animal is to be removed
                    if(animal == self.cur_animal):
                        # if the index is not the last one, set the next animal as current animal
                        if index != len(self.animal_list)-1:
                            self.cur_animal = self.animal_list[index+1]
                        elif index == len(self.animal_list)-1 and len(self.animal_list)>1:
                            self.cur_animal = self.animal_list[index-1]
                        else:
                            self.cur_animal = None
                            
                    # remove animal visuals from scene and from animal list
                    self.removeAnimal(animal, True)
                                        
                    # if the animal has left and right coordinates, only 
                    # delete coordinates of the current image (left OR right)
                    if self.models.model_animals.data.loc[animal.row_index, "RX1"] != -1 and \
                        self.models.model_animals.data.loc[animal.row_index, "LX1"] != -1:
   
                        if self.image_ending == "*_L.jpg":
                            self.models.model_animals.data.loc[animal.row_index, "LX1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "LY1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "LX2"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "LY2"] = -1     
                            
                        elif self.image_ending == "*_R.jpg":
                            self.models.model_animals.data.loc[animal.row_index, "RX1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "RY1"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "RX2"] = -1
                            self.models.model_animals.data.loc[animal.row_index, "RY2"] = -1
                        
                        # if the match mode is active, we need to update the ID and bounding box of the matching animal too
                        if is_match_animal_active:
                            self.imageArea.parent().parent().redrawSelection()
                    else:  
                        # if animal has only left OR right coordinates, remove
                        # complete data row
                        pos = self.models.model_animals.data.index.get_loc(animal.row_index)
                        self.models.model_animals.removeRows(pos, 1, QtCore.QModelIndex())                        
                    break

        # if user is not removing and not adding animals, switch the current 
        # animal to what the user clicks on
        # if the user clicks on no organism, there is no current animal
        elif(not is_remove_mode_active and not is_add_mode_active):
            is_click_on_animal = False 
            for animal in self.animal_list:
                if(animal.boundingBox.contains(pos)):
                    self.cur_animal = animal
                    is_click_on_animal = True
                    break
            
            if not is_click_on_animal: self.cur_animal = None
            
            self.animalSelectionChanged.emit()
                            
        elif(is_add_mode_active):
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
                    
                    cur_image_path = parent.image_list[0][parent.cur_image_index]
                    image_remark = parent.parent().comboBox_imgRemark.currentText()
                    experiment_id = parent.parent().parent().parent().page_data.lineEdit_exp_id.text()
                    user_id = parent.parent().parent().parent().page_settings.lineEdit_user_id.text()
                    
                    # add new data row and use coordinates of the animal as left
                    # or right image coordinates (depending on image_spec)
                    if self.image_ending == "*_R.jpg":
                        image_spec = "R"
                    else: 
                        image_spec = "L"
                    
                    self.models.model_animals.insertRows(
                    int(self.cur_animal.row_index), int(1), 
                    [self.cur_animal], cur_image_path, 
                    image_remark, experiment_id, user_id, [image_spec])
                    
                    # reactivate esc shortcut after tail is drawn
                    #parent.setEscShortcutActive(True)
                    self.shortcut_deselect_animal.setEnabled(True)
                                       
                else:                    
                    # create a new animal
                    idx = self.models.model_animals.data.index.max()
                    if math.isnan(idx): idx = 0
                
                    self.cur_animal = Animal(self.models, 
                                             row_index=idx+1,
                                             position_head=pos)
                    
                    self.cur_animal.setGroup(self._previous_group)
                    self.cur_animal.setSpecies(self._previous_species)
                              
                    # calculate position in original format
                    self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                    
                    # do the actual drawing of the head
                    self.drawAnimalHead(self.cur_animal)
                    
                    # deactivate esc shortcut to prevent creation of incomplete animals
                    #parent.setEscShortcutActive(False) 
                    self.shortcut_deselect_animal.setEnabled(False)
                    
                     # since a new animal is selected, emit signal
                    self.animalSelectionChanged.emit() 
            else:                
                # create a new animal
                idx = self.models.model_animals.data.index.max()
                if math.isnan(idx): idx = 0
                
                self.cur_animal = Animal(self.models, 
                                         row_index=idx+1,
                                         position_head=pos)
                
                self.cur_animal.setGroup(self._previous_group)
                self.cur_animal.setSpecies(self._previous_species)
                
                # calculate position in original format
                self.cur_animal.original_pos_head = QtCore.QPoint(original_x, original_y)
                
                # do the actual drawing of the head
                self.drawAnimalHead(self.cur_animal)
                
                # since a new animal is selected, emit signal
                self.animalSelectionChanged.emit() 

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


    def drawAnimalsFromList(self, animal_list):
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
        """                
        for i in range(len(animal_list)):  
            # get the head and tail position form the list
            if self.image_ending=="*_L.jpg":
                original_pos_h = QtCore.QPoint(int(animal_list["LX1"].iloc[i]), int(animal_list["LY1"].iloc[i]))
                original_pos_t = QtCore.QPoint(int(animal_list["LX2"].iloc[i]), int(animal_list["LY2"].iloc[i]))
            elif self.image_ending == "*_R.jpg":
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
                animal = Animal(self.models,
                         row_index=animal_list.index[i],
                         position_head=pos_h, 
                         position_tail=pos_t,
                         group=str(animal_list["group"].iloc[i]),
                         species=str(animal_list["species"].iloc[i]),
                         remark=animal_remark,
                         length=length)
                
                # set the position in the original image     
                animal.original_pos_head = original_pos_h
                animal.original_pos_tail = original_pos_t
            
                # do the actual drawing of the head
                self.drawAnimalHead(animal)
                self.drawAnimalTailLineBoundingBox(animal)
                
                # append animal to list
                self.animal_list.append(animal)  
                
                # update bounding boxes
                self.updateBoundingBoxes()      
     
 