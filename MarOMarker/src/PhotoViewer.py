from PyQt5 import QtCore, QtGui, QtWidgets
import glob
import pandas as pd
import os
from Helpers import getIcon, displayErrorMsg
from ImageAreas import ImageArea, ImageAreaLR


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

    def on_match_btn(self, activate_match, is_add_active, is_remove_active):
        """
        Delegates query to (de-)activate the match mode to the correct 
        animal painters.

        Parameters
        ----------
        activate_match : bool
            Whether to activate the add mode or deactivate it.
        is_add_active : bool
            Whether the add mode is active or not.
        is_remove_active : bool
            Whether the remove mode is active or not.
            
        Returns
        -------
        is_match_activatable : bool
            Whether it is possible to activate the add mode.
        is_add_active : bool
            Wheter the add mode needs to be active or not.
        is_remove_active : bool
            Whether the remove mode is active or not.
        """
        a, d, g = self.imageAreaLR.imageAreaL.animal_painter.on_match_animal(
            activate_match, is_add_active, is_remove_active)
        
        b, e, h = self.imageAreaLR.imageAreaR.animal_painter.on_match_animal(
            activate_match, is_add_active, is_remove_active)
        
        c, f, i = self.imageArea.animal_painter.on_match_animal(
            activate_match, is_add_active, is_remove_active)
        
        is_match_activatable = a and b and c
        is_add_active = d or e or f
        is_remove_active = g or h or i
        
        self.imageAreaLR.on_match_activated(is_match_activatable)
        
        return is_match_activatable, is_add_active, is_remove_active
    
    def on_add_animal(self, activate_add, is_remove_active, is_match_active):
        """
        Delegates query to (de-)activate the add mode to the correct 
        animal painters.

        Parameters
        ----------
        activate_add : bool
            Whether to activate the add mode or deactivate it.
        is_remove_active : bool
            Whether the remove mode is active or not.
        is_match_active : bool
            Whether the remove mode is active or not.
            
        Returns
        -------
        is_add_activatable : bool
            Whether it is possible to activate the add mode.
        is_remove_active : bool
            Wheter the remove mode needs to be active or not.
        is_match_active : bool
            Whether the remove mode is active or not.
        """
        a, d, g = self.imageAreaLR.imageAreaL.animal_painter.on_add_animal(
            activate_add, is_remove_active, is_match_active)
        
        b, e, h = self.imageAreaLR.imageAreaR.animal_painter.on_add_animal(
            activate_add, is_remove_active, is_match_active)
        
        c, f, i = self.imageArea.animal_painter.on_add_animal(
            activate_add, is_remove_active, is_match_active)
        
        is_add_activatable = a and b and c
        is_remove_active = d or e or f
        is_match_active = g or h or i
        
        self.imageAreaLR.on_match_activated(is_match_active)
        
        return is_add_activatable, is_remove_active, is_match_active

    def on_remove_animal(self, activate_remove, is_add_active, is_match_active):
        """
        Delegates query to (de-)activate the remove mode to the correct 
        animal painters.

        Parameters
        ----------
        activate_remove : bool
            Whether to activate the remove mode or deactivate it.
        is_add_active : bool
            Whether the add mode is active or not.
        is_match_active : bool
            Whether the remove mode is active or not.

        Returns
        -------
        is_remove_activatable : bool
            Whether it is possible to activate the remove mode.
        is_add_active : bool
            Wheter the add mode needs to be active or not.
        is_match_active : bool
            Whether the remove mode is active or not.
        """
        a, d, g = self.imageAreaLR.imageAreaL.animal_painter.on_remove_animal(
            activate_remove, is_add_active, is_match_active)
        
        b, e, h = self.imageAreaLR.imageAreaR.animal_painter.on_remove_animal(
            activate_remove, is_add_active, is_match_active)
        
        c, f, i = self.imageArea.animal_painter.on_remove_animal(
            activate_remove, is_add_active, is_match_active)
        
        is_remove_activatable = a and b and c
        is_add_active = d or e or f
        is_match_active = g or h or i
        
        self.imageAreaLR.on_match_activated(is_match_active)
        
        return is_remove_activatable, is_add_active, is_match_active
          
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
        if len(self.image_list) != 2: return
        if self.cur_image_index >= len(self.image_list[0]) or self.cur_image_index >= len(self.image_list[1]): return
        
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
        # only load image if the list is build and it has an entry at index
        if len(self.image_list) == 2:
            if index < len(self.image_list[0]) and index < len(self.image_list[1]):
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
        
        # clear animal list
        imageArea.animal_painter.animal_list.clear()
        
        # remove 'remove match' buttons from scene
        imageArea.animal_painter.removeAllRemoveMatchBtns()
        
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
      
    def on_wheel_zoom(self, zoom):
        """ When wheel zoom is used on the image, arrow key shortcuts are needed
        for navigating on image and not to switch to next image. The shortcuts
        are handled here. """
        if zoom > 0:
            self.setArrowShortcutsActive(False)
        else:
            self.setArrowShortcutsActive(True)
        
    def _initActions(self):
        """ Initalizes the actions connected to UI elements. """ 
        # connect buttons
        self.btn_previous_image.clicked.connect(self.on_previous_image)
        self.btn_next_image.clicked.connect(self.on_next_image)
        
        self.imageArea.onWheelZoom.connect(self.on_wheel_zoom)
        self.imageAreaLR.imageAreaL.onWheelZoom.connect(self.on_wheel_zoom)
        self.imageAreaLR.imageAreaR.onWheelZoom.connect(self.on_wheel_zoom)
        
        self.imageArea.animal_painter.animalPositionChanged.connect(self.onAnimalDragged)
        self.imageAreaLR.imageAreaL.animal_painter.animalPositionChanged.connect(self.onAnimalDragged)
        self.imageAreaLR.imageAreaR.animal_painter.animalPositionChanged.connect(self.onAnimalDragged)

        # --- define shortcuts ---------------------------------------------- #  
        self.shortcut_previous_image = QtWidgets.QShortcut(
            QtGui.QKeySequence("left"), self.btn_previous_image, 
            self.on_previous_image)
        self.shortcut_next_image = QtWidgets.QShortcut(
            QtGui.QKeySequence("right"), self.btn_next_image, 
            self.on_next_image) 

    def onAnimalDragged(self):
        """ Recalculates the length of an animal when it is dragged and 
        updates all specification widgets accordingly. """
        if hasattr(self.parent().parent().parent(), 'page_data'):
            # recalculate animal length 
            self.parent().parent().parent().page_data.onCalcLength()
            
            # update all specs widgets
            self.imageArea.animal_painter.widget_animal_specs.setAnimal(self.imageArea.animal_painter.cur_animal)
            self.imageAreaLR.imageAreaL.animal_painter.widget_animal_specs.setAnimal(self.imageAreaLR.imageAreaL.animal_painter.cur_animal)
            self.imageAreaLR.imageAreaR.animal_painter.widget_animal_specs.setAnimal(self.imageAreaLR.imageAreaR.animal_painter.cur_animal)
            self.imageAreaLR.updateSpecsWidget() # specs widget on side of LR        

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
        
        
        # scene = QtWidgets.QGraphicsScene(self)
        # gv = QtWidgets.QGraphicsView(scene)
        # gv.setStyleSheet("background-color:green;")
        # gv.setMinimumSize(300,300)
        
        # gv.move(50,50)
        
        
# class LineOverlay(QtWidgets.QWidget):
#     def __init__(self, parent):
#         super(LineOverlay, self).__init__(parent)

#         self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint | QtCore.Qt.ToolTip | QtCore.Qt.WindowStaysOnTopHint);
#         self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True);
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True);
    
#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self)
#         painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(80, 80, 255, 128)))

# class LineOverlayFactoryFilter(QtCore.QObject):
#     def __init__(self, parent=None):
#         super(LineOverlayFactoryFilter, self).__init__(parent)
        
#         #self.overlay = LineOverlay(self.parent())
#         self.overlay = LineOverlay(parent)
        
#     def eventFilter(self, widget, event):
#         if not widget.isWidgetType(): return False
        
#         if event.type() == QtCore.QEvent.MouseButtonPress:
#             #print("mouse button press event")
#             if self.overlay is None: self.overlay = LineOverlay(widget)
#             #self.overlay.setParent(widget)
#             self.overlay.resize(widget.rect().size())
#             self.overlay.move(widget.rect().center())
#             self.overlay.show()
            
#         elif event.type() == QtCore.QEvent.Resize:
#             #print("resize event")
#             if self.overlay is not None and self.overlay.parent() == widget:
#                 self.overlay.resize(widget.size())
#                 self.overlay.move(widget.rect().center())
#                 self.overlay.show()
                
#         return False
 
# import sys

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
    
    
#     window = QtWidgets.QWidget()
#     factory = LineOverlayFactoryFilter(window)
#     layout = QtWidgets.QVBoxLayout(window)


    
    
#     for t in ["foo", "bar", "baz"]:
#         label = QtWidgets.QLabel(t)
#         layout.addWidget(label)
#         label.installEventFilter(factory)
        
#     window.setMinimumSize(300,250)
#     window.show()
    
#     sys.exit(app.exec_())
    
