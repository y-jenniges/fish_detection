import os
from PyQt5 import QtCore, QtGui, QtWidgets
from Helpers import TopFrame, getIcon
from PaintView import PhotoViewer


class PageHome(QtWidgets.QWidget):
    """
    Class to create the home page of the software.
    
    Attributes
    ----------
    factor : float
        Factor for the zoom slider. 
    is_add_animal_active : bool
        Indicates if the add mode is active.
    is_remove_animal_active : bool
        Indicates if the remove mode is active.
    """

    def __init__(self, models, parent=None):        
        super(QtWidgets.QWidget, self).__init__(parent)
        
        # data models
        self.models = models
        
        # variables to indicate if add/remove modes are active
        self.is_add_animal_active = False
        self.is_remove_animal_active = False
        
        # init UI and actions
        self._initUi()
        self._initActions()
        self._initModels()
       
        # slider parameters
        self.slider_max = self.photo_viewer.imageArea.width()*10
        self.slider_min = self.photo_viewer.imageArea.width()
        self.factor = 50*(self.slider_max - self.slider_min)/(self.slider_max)  

    def openZoomWidget(self):
        """ Shows the widget containing the zoom slider. """
        # show the zoom widget if it is not already visible
        if self.widget_zoom.isVisible():
            self.btn_zoom.setIcon(getIcon(":/icons/icons/glass.png")) 
            self.widget_zoom.hide()
            if self.slider_zoom.value() == 0:
                self.photo_viewer.setArrowShortcutsActive(True)
        else:
            self.btn_zoom.setIcon(getIcon(":/icons/icons/glass_darkBlue.png")) 
            self.widget_zoom.show()
            self.placeZoomWidget()
            # arrows are needed for controlling slider and navigating in zoomed-in photo
            self.photo_viewer.setArrowShortcutsActive(False) 
            
    def onZoomValueChanged(self, value):
        """ Zoom into the image according to the level of the zoom slider.  """
        # determine the zoom factor and transform the photo of the photo_viewer
        scale = 1 + value*self.factor/100
        self.photo_viewer.imageArea.setTransform(
            self.photo_viewer.imageArea.transform().fromScale(scale, scale))

        # if thevalue is smaller 1, make the photo fill the photo_viewer image area
        if value < 1:
            self.photo_viewer.imageArea.resetTransform() 
            self.photo_viewer.imageArea.fitInView()
  
    def on_add_clicked(self):
        """ (De-)activate the add mode. """
        if self.is_add_animal_active:          
            self.is_add_animal_active, self.is_remove_animal_active = self.photo_viewer.on_add_animal(False, self.is_remove_animal_active)
        else:
            self.is_add_animal_active, self.is_remove_animal_active = self.photo_viewer.on_add_animal(True, self.is_remove_animal_active)         
        
        self.updateAddRemoveIcons()
            
    def on_remove_clicked(self):
        """ (De-)activate the remove mode. """
        # self.photo_viewer.on_remove_animal()
        # self.updateAddRemoveIcons()
        if self.is_remove_animal_active:          
            self.is_remove_animal_active, self.is_add_animal_active = self.photo_viewer.on_remove_animal(False, self.is_add_animal_active)
        else:
            self.is_remove_animal_active, self.is_add_animal_active = self.photo_viewer.on_remove_animal(True, self.is_add_animal_active)
        
        self.updateAddRemoveIcons()

    def updateAddRemoveIcons(self):
        """ Update the icond of add and remove mode according to their state.  """
        # adapt icon of the add button
        if self.is_add_animal_active:
            self.btn_add.setIcon(getIcon(":/icons/icons/plus_darkBlue.png"))
        else:
            self.btn_add.setIcon(getIcon(":/icons/icons/plus.png"))
            
        # adapt icon of the remove button
        if self.is_remove_animal_active:
            self.btn_delete.setIcon(getIcon(":/icons/icons/bin_open_darkBlue.png"))
        else:
            self.btn_delete.setIcon(getIcon(":/icons/icons/bin_closed.png"))        
 
    def on_filter_clicked(self):
        """ !!! NOT IMPLEMENTED YET !!! 
        
        Opens a widget showinf options for image filters. 
        """
        print("Filters are not implemented yet.")
        # img_path = self.photo_viewer.image_list[self.photo_viewer.cur_image_index]
        # img = img_to_array(load_img(img_path), dtype="uint8")
        # img = helpers.equalizePil(img)
        # h,w,c = img.shape
        # qimage = QtGui.QImage(img, h, w, 3*h, QtGui.QImage.Format_RGB888)
        # self.photo_viewer.imageArea.setPhoto(QtGui.QPixmap.fromImage(qimage))

    def update_species_list(self, list_species):
        """ Append given list of species names to the species data model if
        no entry exists for them yet. """
        for i in range(len(list_species)):
            existing_items = self.models.model_species.findItems(list_species[i]["title"])

            # only append new item if it is not already in the list
            if len(existing_items) == 0:
                item = QtGui.QStandardItem(list_species[i]["title"])           
                item.setTextAlignment(QtCore.Qt.AlignRight)
                # icon = QtGui.QIcon(list_species[i]["imagePath"])
                # item.setIcon(icon)
                self.models.model_species.appendRow(item)

    def showEvent(self, event):
        """" Reload the image when opening the home page. """
        if self.photo_viewer.cur_image_index < len(self.photo_viewer.image_list[0]):
            self.photo_viewer.loadImageFromIndex(self.photo_viewer.cur_image_index)

    def _initUi(self):
        """ Initalize the UI of the home page. """
        # --- top bar  ----------------------------------------------------- #         
        # create the blue top bar
        self.frame_topBar = TopFrame(":/icons/icons/home_w.png", 
                                     "frame_homeBar", self)     
        
        
        # --- control bar  ------------------------------------------------- #         
        # create the cotrol bar containing the menu
        #self.frame_controlBar = MenuFrame("Home", "frame_controlBar_home")  
       
        
        # main frame
        self.frame_controlBar = self._createHomeControlBar()
        self.frame_controlBar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                            QtWidgets.QSizePolicy.Expanding) 
        
        # --- photo viewer  ------------------------------------------------ #        
        self.photo_viewer = PhotoViewer(self.models, imageDirectory="", 
                                        imagePrefix="", outputDir="", 
                                        parent=self)
        self.photo_viewer.setObjectName("photo_viewer")
        
        # --- main widget -------------------------------------------------- #  
        # set main widget properties
        #self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("#btn_leftImg:hover, "
                           "#btn_rightImg:hover{background-color:transparent;}")
        self.setObjectName("page_home")
        
        # main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setObjectName("layout")
        
        # add widgets to main layout
        self.layout.addWidget(self.frame_topBar)
        self.layout.addWidget(self.frame_controlBar)
        self.layout.addWidget(self.photo_viewer)
        
        
        # --- zoom widget  ------------------------------------------------- # 
        # create the zoom slider widget
        self.widget_zoom = QtWidgets.QWidget(self)
        self.widget_zoom.setFixedSize(QtCore.QSize(200, 50))
        self.widget_zoom.setObjectName("widget_zoom")
        self.widget_zoom.setAutoFillBackground(True)
        self.widget_zoom.setStyleSheet(
            "background-color: rgb(200, 200, 200, 200); border: none; border-radius: 3px; ")
        
        self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_zoom.setMaximum(100)
        self.slider_zoom.setMinimum(0)
        self.slider_zoom.setStyleSheet("QSlider{background-color:transparent; } \n"
                                        "QSlider::groove:horizontal {backgroud:white; height: 4px; margin: 1px 0; border:none; border-radius: 3px;} \n"
                                        "QSlider::handle:horizontal {width: 10px; margin: -10px 0; background:  rgb(0, 203, 221); border-radius: 3px; border:none;}"
                                        "QSlider::handle:horizontal:hover{background: rgb(0, 160, 174);} \n"
                                        "QSlider::handle:horizontal:pressed{background:rgb(0,100,108);} \n"  
                                        "QSlider::add-page:horizontal {background: white;} \n"
                                        "QSlider::sub-page:horizontal {background: rgb(0, 160, 174);}")
     
        self.layout_zoom = QtWidgets.QHBoxLayout(self.widget_zoom)
        self.layout_zoom.setContentsMargins(11, 5, 11, 5)
        self.layout_zoom.setSpacing(4)
        self.layout_zoom.setObjectName("layout_zoom")
        self.layout_zoom.addWidget(self.slider_zoom)
        
        self.widget_zoom.hide()  
        self.placeZoomWidget()

    def _createHomeControlBar(self):
        """ Creates the home bar UI containing the image manipulation options. """
        frame_controlBar = QtWidgets.QFrame(self)
        frame_controlBar.setMinimumSize(QtCore.QSize(0, 50))
        frame_controlBar.setMaximumSize(QtCore.QSize(16777215, 50))
        frame_controlBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_controlBar.setLineWidth(0)
        frame_controlBar.setObjectName("frame_controlBar")
        
        # layout 
        self.layout_frame_controlBar = QtWidgets.QHBoxLayout(frame_controlBar)
        self.layout_frame_controlBar.setContentsMargins(11, 5, 11, 5)
        self.layout_frame_controlBar.setSpacing(4)
        self.layout_frame_controlBar.setObjectName("layout_frame_controlBar")
        
        # placeholder menu button to keep symmetry
        self.btn_menu2 = QtWidgets.QPushButton(frame_controlBar)
        self.btn_menu2.setEnabled(False)     
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu2.sizePolicy().hasHeightForWidth())  
        self.btn_menu2.setSizePolicy(sizePolicy)
        self.btn_menu2.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu2.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu2.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu2.setObjectName("btn_menu2")

        # button for switching between left, right and both images
        self.btn_imgSwitch = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_imgSwitch.sizePolicy().hasHeightForWidth())
        self.btn_imgSwitch.setSizePolicy(sizePolicy)
        self.btn_imgSwitch.setMinimumSize(QtCore.QSize(60, 40))
        self.btn_imgSwitch.setMaximumSize(QtCore.QSize(60, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_imgSwitch.setFont(font)
        self.btn_imgSwitch.setObjectName("btn_imgSwitch")
        
        # button for opening a widget displaying filters
        self.btn_filter = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_filter.sizePolicy().hasHeightForWidth())
        self.btn_filter.setSizePolicy(sizePolicy)
        self.btn_filter.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_filter.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_filter.setIcon(getIcon(":/icons/icons/filter.png"))
        self.btn_filter.setIconSize(QtCore.QSize(30, 30))
        self.btn_filter.setObjectName("btn_filter")
        
        # combo box for image remarks
        self.comboBox_imgRemark = QtWidgets.QComboBox(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_imgRemark.sizePolicy().hasHeightForWidth())
        self.comboBox_imgRemark.setSizePolicy(sizePolicy)
        self.comboBox_imgRemark.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_imgRemark.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_imgRemark.setEditable(True)
        self.comboBox_imgRemark.setObjectName("comboBox_imgRemark")
        # self.comboBox_imgRemark.addItem("")
        # self.comboBox_imgRemark.addItem("")
        # self.comboBox_imgRemark.addItem("")
        # self.comboBox_imgRemark.addItem("")
        # self.comboBox_imgRemark.addItem("")
        # self.comboBox_imgRemark.addItem("")
        
        # button for opening a widget for zooming into photo
        self.btn_zoom = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_zoom.sizePolicy().hasHeightForWidth())
        self.btn_zoom.setSizePolicy(sizePolicy)
        self.btn_zoom.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_zoom.setMaximumSize(QtCore.QSize(40, 40))  
        self.btn_zoom.setIcon(getIcon(":/icons/icons/glass.png"))       
        self.btn_zoom.setIconSize(QtCore.QSize(30, 30))
        self.btn_zoom.setObjectName("btn_zoom")
        
        # button for activating the add-animal-mode
        self.btn_add = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_add.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_add.setIcon(getIcon(":/icons/icons/plus.png"))
        self.btn_add.setIconSize(QtCore.QSize(30, 30))
        self.btn_add.setObjectName("btn_add")

        # button for switching to previous animal
        self.btn_previous = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_previous.sizePolicy().hasHeightForWidth())
        self.btn_previous.setSizePolicy(sizePolicy)
        self.btn_previous.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_previous.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_previous.setIcon(getIcon(":/icons/icons/arrow_left_small.png"))
        self.btn_previous.setIconSize(QtCore.QSize(30, 30))
        self.btn_previous.setObjectName("btn_previous")
        
        # playeholder button to keep symmetry 
        self.btn_placeholder = QtWidgets.QPushButton(frame_controlBar)
        self.btn_placeholder.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_placeholder.sizePolicy().hasHeightForWidth())
        self.btn_placeholder.setSizePolicy(sizePolicy)
        self.btn_placeholder.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_placeholder.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_placeholder.setIconSize(QtCore.QSize(30, 30))
        self.btn_placeholder.setObjectName("btn_placeholder")
        
        # button for switching to next animal
        self.btn_next = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_next.sizePolicy().hasHeightForWidth())
        self.btn_next.setSizePolicy(sizePolicy)
        self.btn_next.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_next.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_next.setIcon(getIcon(":/icons/icons/arrow_right_small.png"))
        self.btn_next.setIconSize(QtCore.QSize(30, 30))
        self.btn_next.setObjectName("btn_next")
        
        # button to activate the remove-animals-mode
        self.btn_delete = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy)
        self.btn_delete.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_delete.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_delete.setIcon(getIcon(":/icons/icons/bin_closed.png"))
        self.btn_delete.setIconSize(QtCore.QSize(30, 30))
        self.btn_delete.setObjectName("btn_delete")
        
        # button for undoing the last action
        self.btn_undo = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_undo.sizePolicy().hasHeightForWidth())
        self.btn_undo.setSizePolicy(sizePolicy)
        self.btn_undo.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_undo.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_undo.setIcon(getIcon(":/icons/icons/undo.png"))
        self.btn_undo.setIconSize(QtCore.QSize(30, 30))
        self.btn_undo.setObjectName("btn_undo")
    
        # button for the menu
        self.btn_menu = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu.sizePolicy().hasHeightForWidth())
        self.btn_menu.setSizePolicy(sizePolicy)
        self.btn_menu.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu.setText("")
        self.btn_menu.setIcon(getIcon(":/icons/icons/menu.png"))
        self.btn_menu.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu.setObjectName("btn_menu")      

        # horizontal spacers
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)        
        spacerItem7 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum) 

        # --- create dummies to keep the symmetry in the control bar ------------ #
        # dummy button for switching between left, right and both images
        self.btn_imgSwitch_dummy = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_imgSwitch_dummy.sizePolicy().hasHeightForWidth())
        self.btn_imgSwitch_dummy.setSizePolicy(sizePolicy)
        self.btn_imgSwitch_dummy.setMinimumSize(QtCore.QSize(60, 40))
        self.btn_imgSwitch_dummy.setMaximumSize(QtCore.QSize(60, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_imgSwitch_dummy.setFont(font)
        self.btn_imgSwitch_dummy.setObjectName("btn_imgSwitch_dummy")
        self.btn_imgSwitch_dummy.setEnabled(False)
        
        # dummy button for opening a widget displaying filters
        self.btn_filter_dummy = QtWidgets.QPushButton(frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_filter_dummy.sizePolicy().hasHeightForWidth())
        self.btn_filter_dummy.setSizePolicy(sizePolicy)
        self.btn_filter_dummy.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_filter_dummy.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_filter_dummy.setIconSize(QtCore.QSize(30, 30))
        self.btn_filter_dummy.setObjectName("btn_filter_dummy")
        self.btn_filter_dummy.setEnabled(False)
        
        # dummy combo box for image remarks (necessary to keep symmetry)
        self.comboBox_imgRemark_dummy = QtWidgets.QComboBox(frame_controlBar)
        self.comboBox_imgRemark_dummy.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_imgRemark_dummy.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_imgRemark_dummy.setEditable(False)
        self.comboBox_imgRemark_dummy.setEnabled(False)
        self.comboBox_imgRemark_dummy.setStyleSheet("#comboBox_imgRemark_dummy{background-color:transparent; color:transparent;} #comboBox_imgRemark_dummy:down-arrow{ image:none;}")
        self.comboBox_imgRemark_dummy.setObjectName("comboBox_imgRemark_dummy")

        # --- add widgets to layout of the control bar ---------------------- #
        # add widgets to layout 
        self.layout_frame_controlBar.addWidget(self.btn_menu2)
        self.layout_frame_controlBar.addItem(spacerItem2)
        self.layout_frame_controlBar.addWidget(self.btn_imgSwitch)
        self.layout_frame_controlBar.addWidget(self.btn_filter)
        self.layout_frame_controlBar.addWidget(self.comboBox_imgRemark)
        self.layout_frame_controlBar.addItem(spacerItem11) 
        self.layout_frame_controlBar.addWidget(self.btn_zoom)
        self.layout_frame_controlBar.addItem(spacerItem7)
        self.layout_frame_controlBar.addWidget(self.btn_add)
        self.layout_frame_controlBar.addItem(spacerItem7)
        self.layout_frame_controlBar.addWidget(self.btn_previous)
        self.layout_frame_controlBar.addItem(spacerItem7)
        self.layout_frame_controlBar.addWidget(self.btn_placeholder)
        self.layout_frame_controlBar.addItem(spacerItem7)
        self.layout_frame_controlBar.addWidget(self.btn_next)
        self.layout_frame_controlBar.addItem(spacerItem7)
        self.layout_frame_controlBar.addWidget(self.btn_delete)
        self.layout_frame_controlBar.addItem(spacerItem7)
        self.layout_frame_controlBar.addWidget(self.btn_undo)
        self.layout_frame_controlBar.addItem(spacerItem11)
        self.layout_frame_controlBar.addWidget(self.comboBox_imgRemark_dummy)
        self.layout_frame_controlBar.addWidget(self.btn_filter_dummy)
        self.layout_frame_controlBar.addWidget(self.btn_imgSwitch_dummy)
        self.layout_frame_controlBar.addItem(spacerItem2)
        self.layout_frame_controlBar.addWidget(self.btn_menu)             
        
        return frame_controlBar
        
    def _initActions(self):
        """ Define actions triggered by user interaction with the UI. """
        # connecting signals and slots
        self.btn_add.clicked.connect(self.on_add_clicked)
        self.btn_delete.clicked.connect(self.on_remove_clicked)
        self.btn_next.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_next_animal)
        self.btn_previous.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_previous_animal)
        self.btn_zoom.clicked.connect(self.openZoomWidget)
        self.btn_imgSwitch.clicked.connect(self.switchImageMode)
        self.slider_zoom.valueChanged.connect(self.onZoomValueChanged)
        self.photo_viewer.newImageLoaded.connect(self.onNewImage)
        self.comboBox_imgRemark.currentTextChanged.connect(self.setComboboxImageRemark)
        self.btn_filter.clicked.connect(self.on_filter_clicked)
        
        # --- define shortcuts ------------------------------------------------------------------------------------------- #  
        self.shortcut_previous_animal = QtWidgets.QShortcut(QtGui.QKeySequence("a"), self.btn_previous, self.photo_viewer.imageArea.animal_painter.on_previous_animal)
        self.shortcut_next_animal = QtWidgets.QShortcut(QtGui.QKeySequence("d"), self.btn_next, self.photo_viewer.imageArea.animal_painter.on_next_animal)
        self.shortcut_add_animal = QtWidgets.QShortcut(QtGui.QKeySequence("+"), self.btn_add, self.on_add_clicked)
        self.shortcut_remove_animal = QtWidgets.QShortcut(QtGui.QKeySequence("-"), self.btn_delete, self.on_remove_clicked)
        self.shortcut_img_left = QtWidgets.QShortcut(QtGui.QKeySequence("1"), self.btn_imgSwitch, self.displayLeftImage)
        self.shortcut_img_right = QtWidgets.QShortcut(QtGui.QKeySequence("2"), self.btn_imgSwitch, self.displayRightImage)
        self.shortcut_img_both = QtWidgets.QShortcut(QtGui.QKeySequence("3"), self.btn_imgSwitch, self.displayBothImages)
        
    def _initModels(self):
        """ Add data models to respective UI elements. """
        self.comboBox_imgRemark_dummy.setModel(self.models.model_image_remarks)
        self.comboBox_imgRemark.setModel(self.models.model_image_remarks)

    def setComboboxImageRemark(self, text):
        """ Add a text to the image remark combobx and data model. """
        # if the remark is not in the combobox, add it. Else choose its index
        index = self.comboBox_imgRemark.findText(text) 
        
        if self.comboBox_imgRemark.findText(text) == -1:
            item = QtGui.QStandardItem(str(text))
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            self.models.model_image_remarks.appendRow(item)
            self.comboBox_imgRemark.setCurrentIndex(self.comboBox_imgRemark.count()-1)
        else:
            self.comboBox_imgRemark.setCurrentIndex(index)
        
        # get the current photo ID
        cur_image_path = self.photo_viewer.image_list[0][self.photo_viewer.cur_image_index]
        file_id = os.path.basename(cur_image_path)[:-6]
    
        # adapt the image remark in the data model
        cur_indices = self.models.model_animals.data[
            self.models.model_animals.data['file_id']==file_id].index
        for idx in cur_indices:
            self.models.model_animals.data.loc[idx, 'image_remarks'] = text
    
    def onNewImage(self, remark):
        """ Sets the text in the image remark combobox according to the 
        newly loaded image. """
        # adapt image remark combobox
        self.setComboboxImageRemark(remark)
    
    def switchImageMode(self):
        """ Switches the image mode depending on the current image mode """
        cur_mode = self.btn_imgSwitch.text()
        if cur_mode == "L": 
            self.displayRightImage()
        elif cur_mode == "R":
            self.displayBothImages()
        else:
            self.displayLeftImage()
        
    def displayLeftImage(self):
        """ Display left image. """
        self.btn_imgSwitch.setText("L")
        self.photo_viewer.activateImageMode("L")

    def displayRightImage(self):
        """ Display right image. """
        self.btn_imgSwitch.setText("R")
        self.photo_viewer.activateImageMode("R")
    
    def displayBothImages(self):
        """ Display both images. """
        self.btn_imgSwitch.setText("LR")
        self.photo_viewer.activateImageMode("LR")
     
    def mousePressEvent(self, event):
        """ On mouse press, update visibility of zoom slider widget. """
        super().mousePressEvent(event)          
        # hide the zoom widget if it is open and a click somewhere else is registered
        if self.widget_zoom.isVisible() and not self.widget_zoom.rect().contains(event.pos()):
            self.openZoomWidget()

    def resizeEvent(self, event):
        """ Make sure that zoom slider widget is placed correctly when 
        program is resized. """
        super().resizeEvent(event)
        self.placeZoomWidget()
  
    def placeZoomWidget(self):
        """ Place the zoom widget under the zoom button. """
        # reset position of zoom widget
        self.widget_zoom.move(0,0)
        
        # map the position of the zoom button to the local coordinate system 
        # of the zoom widget
        pos = self.btn_zoom.mapToGlobal(self.btn_zoom.rect().topLeft())
        p = self.widget_zoom.mapFromGlobal(pos)
        
        # move the zoom widget a bit below the button position and center it below the button
        self.widget_zoom.move(p + QtCore.QPoint(-self.widget_zoom.width()/2 + 20, 50))        