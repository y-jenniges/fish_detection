import os
import numpy as np
import pandas as pd
import tensorflow as tf
from PyQt5 import QtCore, QtGui, QtWidgets
from TabWidget import TabWidget
import Helpers
import Losses

class PageSettings(QtWidgets.QWidget):
    """ 
    Class to create the settings page of the software. It contains tabs for
    different types of settings (e.g. camera, user, neural network, species).
    
    Attributes
    ----------
    @todo 
    frame_top_bar : TopFrame
        frame at the top of the window to display user ID and an icon
    frame_control_bar : MenuFrame
        frame below the top bar to display controls of the page and the menu
    label_about_text : string
        text for the about page
        
    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
        
    """
    # create custom signals 
    userIdChanged = QtCore.pyqtSignal(str)
        
    def __init__(self, models, parent=None):
        """
        Init function. It creates the UI and the connections between 
        elements (also to other classes).

        Parameters
        ----------
        models : Models
            Contains all necessary data models, i.e. models for the animal 
            species, group, remark, as well as image remark and the general
            animal data from the result table.
        parent : optional
            The default is None.
        """
        super(QtWidgets.QWidget, self).__init__(parent)

        # data models
        self.models = models
        
        # neural network
        self.nn_model = None

        # init UI and actions on it
        self._initUi()
        self._initActions()
                
    def _initUi(self):  
        """
        Function that initializes the UI components for the settings page.
        """             
        self.setStyleSheet(
            "/*------------------------ line edit -----------------------*/\n"
            "QLineEdit{\n"
            "    background-color:white;\n"
            "    border-radius: 3px;\n"
            "    font: 12pt \"Century Gothic\";\n"
            "    selection-background-color:rgb(0, 203, 221);\n"
            "    selection-color:white;\n"
            "    color:black;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "/*------------------------ tab widget ----------------------*/\n"
            "QTabWidget{\n"
            "    font: 12pt \"Century Gothic\";\n"
            "}\n"
            "\n"
            "QTabWidget::pane { /* The tab widget frame */\n"
            "       border:None;\n"
            "}\n"
            "/* Style the tab using the tab sub-control. Note that\n"
            "    it reads QTabBar _not_ QTabWidget */\n"
            "QTabBar::tab {\n"
            "    font: 12pt \"Century Gothic\";\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
            "                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
            "    border: None;\n"
            "    min-width: 8ex;\n"
            "    min-height: 60ex;\n"
            "    padding: 2px;\n"
            "    padding-bottom:30px;\n"
            "\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected, QTabBar::tab:hover {\n"
            "background-color: rgb(240, 240, 240);\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected {\n"
            "    border-color: #9B9B9B;\n"
            "    border-bottom-color: #C2C7CB; /* same as pane color */\n"
            "}\n"
            "\n"
            "QTabBar::tab:!selected {\n"
            "    margin-top:0px; /* make non-selected tabs look smaller */\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "#frame_camera_options{background-color:rgb(230, 230, 230);border-radius:3px;}\n"
            "#frame_user_options{background-color:rgb(230, 230, 230);border-radius:3px;}\n"
            "#frame_species_options{background-color:rgb(230, 230, 230);border-radius:3px;}\n"
            "#frame_nn_options{background-color:rgb(230, 230, 230);border-radius:3px;}\n"
            "\n"
            "\n"
            "/*-------------------------- labels ------------------------*/\n"
            "QLabel{\n"
            "    color:black;\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "/*-------------------------- buttons ------------------------*/\n"
            "QPushButton{\n"
            "    font: 10pt \"Century Gothic\";\n"
            "}\n"
            "\n"
            "#btn_load, #btn_save, #btn_browse_nn, #btn_add_species, #btn_remove_species{\n"
            "    background-color:rgb(200, 200, 200);\n"
            "}\n"
            "\n"
            "\n"
            "#btn_load:hover, #btn_save:hover, \n"
            "#btn_browse_nn:hover, #btn_add_species:hover, #btn_remove_species:hover{\n"
            "  background-color: rgb(0, 203, 221);\n"
            "}\n"
            "\n"
            "#btn_load:pressed, #btn_save:pressed,\n"
            "#btn_browse_nn:pressed, #btn_add_species:pressed, #btn_remove_species:pressed{\n"
            "background-color: rgb(0, 160, 174);\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "/*--------------------- double spin boxes -------------------*/\n"
            "\n"
            "QDoubleSpinBox {\n"
            "    padding-right: 15px; /* make room for the arrows */\n"
            "    /*border-image: url(:/images/frame.png) 4;*/\n"
            "    border-radius: 3px;\n"
            "    selection-background-color:rgb(0, 203, 221);\n"
            "    font:12pt \"Century Gothic\";\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button {\n"
            "    subcontrol-origin: border;\n"
            "    subcontrol-position: top right; /* position at the top right corner */\n"
            "\n"
            "    width: 16px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */\n"
            "    border-image: url(:/icons/icons/arrow_up.png) 1;\n"
            "    border-width: 1px;\n"
            "    margin:2px;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button:hover {\n"
            "    border-image: url(:/icons/icons/arrow_up_blue.png) 1;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button:pressed {\n"
            "    border-image: url(:/icons/icons/arrow_up_darkblue.png) 1;\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "/*\n"
            "QDoubleSpinBox::up-arrow {\n"
            "    image:url(:/icons/icons/arrow_up.png);\n"
            "    width: 7px;\n"
            "    height: 7px;\n"
            "}\n"
            "QDoubleSpinBox::up-arrow:disabled, QSpinBox::up-arrow:off { /* off state when value is max */\n"
            " /*  image: url(:/images/up_arrow_disabled.png);\n"
            "}\n"
            "QDoubleSpinBox::down-arrow {\n"
            "    image: url(:/icons/icons/arrow_down.png);\n"
            "    width: 7px;\n"
            "    height: 7px;\n"
            "}\n"
            "QDoubleSpinBox::down-arrow:disabled,\n"
            "QDoubleSpinBox::down-arrow:off { /* off state when value in min */\n"
            " /*  image: url(:/icons/icons/arrow_down.png) 1;\n"
            "}\n"
            "*/\n"
            "\n"
            "QDoubleSpinBox::down-button {\n"
            "    subcontrol-origin: border;\n"
            "    subcontrol-position: bottom right; /* position at bottom right corner */\n"
            "\n"
            "    width: 16px;\n"
            "    border-image: url(:/icons/icons/arrow_down.png) 1;\n"
            "    border-width: 1px;\n"
            "    border-top-width: 0;\n"
            "    margin:2px;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::down-button:hover {\n"
            "    border-image: url(:/icons/icons/arrow_down_blue.png) 1;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::down-button:pressed {\n"
            "    border-image:url(:/icons/icons/arrow_down_darkblue.png) 1;\n"
            "}\n")
       
        # --- main page ----------------------------------------------------- #
        self.setObjectName("page_settings")
        
        # main layout
        self.layout_page_settings = QtWidgets.QVBoxLayout(self)
        self.layout_page_settings.setContentsMargins(0, 0, 0, 0)
        self.layout_page_settings.setSpacing(0)
        self.layout_page_settings.setObjectName("layout_page_settings")
        
        # top bar (the blue one on every page)
        self.frame_top_bar = Helpers.TopFrame(":/icons/icons/settings.png", "frame_settings_bar", self)   
        
        # menu bar on about page
        self.frame_control_bar = Helpers.MenuFrame("Settings", "frame_control_bar_settings", self)
  
        # --- main frame for the settings ----------------------------------- #
        self.frame_settings = QtWidgets.QFrame(self)
        self.frame_settings.setStyleSheet("")
        self.frame_settings.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_settings.setObjectName("frame_settings")
        
        # layout for the main settings frame
        self.layout_settings_frame = QtWidgets.QHBoxLayout(self.frame_settings)
        self.layout_settings_frame.setContentsMargins(0, 0, 0, 0)
        self.layout_settings_frame.setSpacing(0)
        self.layout_settings_frame.setObjectName("layout_settings_frame")
                
        # custom tab widget (with horizontal texts on the left side)
        self.tabWidget = TabWidget(self.frame_settings)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        
        # define tabs
        self.tab_camera = self.createTabCamera() # tab for camera settings
        self.tab_neuralNet = self.createTabNeuralNetwork() # tab for neural net
        self.tab_species = self.createTabSpecies() # tab for species    
        self.tab_user = self.createTabUser() # tab for user settings
        
        # add tabs to tab widget
        self.tabWidget.addTab(self.tab_camera, Helpers.getIcon(":/icons/icons/camera.png"), "")
        self.tabWidget.addTab(self.tab_neuralNet, Helpers.getIcon(":/icons/icons/nn.png"), "")
        self.tabWidget.addTab(self.tab_species, Helpers.getIcon(":/icons/icons/fish.png"), "")
        self.tabWidget.addTab(self.tab_user, Helpers.getIcon(":/icons/icons/user_b.png"), "")
        
        # add tab widget to layout of main settings frame
        self.layout_settings_frame.addWidget(self.tabWidget)
        
        
        # --- add widgets to main layout ------------------------------------ #
        self.layout_page_settings.addWidget(self.frame_top_bar)
        self.layout_page_settings.addWidget(self.frame_control_bar)
        self.layout_page_settings.addWidget(self.frame_settings)
    
    def createTabCamera(self):
        # --- main frame (whole tab) ---------------------------------------- #
        tab_camera = QtWidgets.QWidget(self)
        tab_camera.setObjectName("tab_camera")
        
        # main layout
        layout = QtWidgets.QGridLayout(tab_camera)
        layout.setObjectName("layout")
        
        # spacers
        spacerItem34 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
        spacerItem35 = QtWidgets.QSpacerItem(20, 40, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)
        
        
        # --- frame for camera options -------------------------------------- #
        frame_camera_options = QtWidgets.QFrame(tab_camera)
        frame_camera_options.setStyleSheet("")
        frame_camera_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_camera_options.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_camera_options.setObjectName("frame_camera_options")
        
        # layout
        layout_camera_options = QtWidgets.QVBoxLayout(frame_camera_options)
        layout_camera_options.setContentsMargins(11, 11, 11, 11)
        layout_camera_options.setSpacing(7)
        layout_camera_options.setObjectName("layout_camera_options")
        
        # vertical spacer
        spacerItem32 = QtWidgets.QSpacerItem(20, 40, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)
        
        
        # --- frame for camera config file ---------------------------------- #
        frame_config = QtWidgets.QFrame(frame_camera_options)
        frame_config.setMinimumSize(QtCore.QSize(0, 50))
        frame_config.setMaximumSize(QtCore.QSize(16777215, 60))
        frame_config.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_config.setObjectName("frame_config")
        
        # layout
        layout_config = QtWidgets.QHBoxLayout(frame_config)
        layout_config.setContentsMargins(0, 0, 0, 0)
        layout_config.setObjectName("layout_config")
        
        # line edit for config path
        self.lineEdit_config_path = QtWidgets.QLineEdit(frame_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit_config_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_config_path.setSizePolicy(sizePolicy)
        self.lineEdit_config_path.setMinimumSize(QtCore.QSize(400, 40))
        self.lineEdit_config_path.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_config_path.setReadOnly(True)
        self.lineEdit_config_path.setObjectName("lineEdit_config_path")
           
        # button for loading a config file
        self.btn_load = QtWidgets.QPushButton(frame_config)
        self.btn_load.setMinimumSize(QtCore.QSize(125, 40))
        self.btn_load.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_load.setObjectName("btn_load")
        
        # button for saving current camera config
        self.btn_save = QtWidgets.QPushButton(frame_config)
        self.btn_save.setMinimumSize(QtCore.QSize(125, 40))
        self.btn_save.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_save.setObjectName("btn_save")
        
        # add widgets to layout
        layout_config.addWidget(self.lineEdit_config_path)
        layout_config.addWidget(self.btn_load)
        layout_config.addWidget(self.btn_save)
        
        
        # --- frame for offset options -------------------------------------- # 
        frame_offset = QtWidgets.QFrame(frame_camera_options)
        frame_offset.setMinimumSize(QtCore.QSize(0, 30))
        frame_offset.setMaximumSize(QtCore.QSize(16777215, 60))
        frame_offset.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_offset.setObjectName("frame_offset")
        
        # layout
        layout_offset = QtWidgets.QHBoxLayout(frame_offset)
        layout_offset.setContentsMargins(0, 0, 0, 0)
        layout_offset.setObjectName("layout_offset")
        
        # label to display parameter name "offset"
        self.label_offset = QtWidgets.QLabel(frame_offset)
        self.label_offset.setObjectName("label_offset")
        
        # horizontal spacer
        spacerItem29 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
             
        # spin box for the offset
        self.spinBox_offset = QtWidgets.QDoubleSpinBox(frame_offset)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spinBox_offset.sizePolicy().hasHeightForWidth())
        self.spinBox_offset.setSizePolicy(sizePolicy)
        self.spinBox_offset.setMinimumSize(QtCore.QSize(200, 40))
        self.spinBox_offset.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinBox_offset.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_offset.setMaximum(9999.99)
        self.spinBox_offset.setObjectName("spinBox_offset")
        
        # label to display the unit of the offset
        self.label_unit_offset = QtWidgets.QLabel(frame_offset)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_unit_offset.sizePolicy().hasHeightForWidth())
        self.label_unit_offset.setSizePolicy(sizePolicy)
        self.label_unit_offset.setMinimumSize(QtCore.QSize(50, 0))
        self.label_unit_offset.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_unit_offset.setObjectName("label_unit_offset")
             
        # add widgets to layout
        layout_offset.addWidget(self.label_offset)
        layout_offset.addItem(spacerItem29)
        layout_offset.addWidget(self.spinBox_offset)
        layout_offset.addWidget(self.label_unit_offset)
        
        
        # --- frame for camera distance options ----------------------------- #
        frame_distance_cameras = QtWidgets.QFrame(frame_camera_options)
        frame_distance_cameras.setMinimumSize(QtCore.QSize(0, 30))
        frame_distance_cameras.setMaximumSize(QtCore.QSize(16777215, 60))
        frame_distance_cameras.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_distance_cameras.setObjectName("frame_distance_cameras")
        
        # layout
        layout_distance = QtWidgets.QHBoxLayout(frame_distance_cameras)
        layout_distance.setContentsMargins(0, 0, 0, 0)
        layout_distance.setObjectName("layout_distance")
        
        # label to display parameter name "distance between cameras"
        self.label_distance_cameras = QtWidgets.QLabel(frame_distance_cameras)
        self.label_distance_cameras.setObjectName("label_distance_cameras")
              
        # horizontal spacer
        spacerItem30 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
        
        # spin box for the distance between the cameras
        self.spinBox_distance_cameras = QtWidgets.QDoubleSpinBox(frame_distance_cameras)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spinBox_distance_cameras.sizePolicy().hasHeightForWidth())
        self.spinBox_distance_cameras.setSizePolicy(sizePolicy)
        self.spinBox_distance_cameras.setMinimumSize(QtCore.QSize(200, 40))
        self.spinBox_distance_cameras.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinBox_distance_cameras.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_distance_cameras.setMaximum(9999.99)
        self.spinBox_distance_cameras.setObjectName("spinBox_distance_cameras")
        
        # label to display the unit of the distance between the cameras
        self.label_unit_ditance_cameras = QtWidgets.QLabel(frame_distance_cameras)
        self.label_unit_ditance_cameras.setMinimumSize(QtCore.QSize(50, 0))
        self.label_unit_ditance_cameras.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_unit_ditance_cameras.setObjectName("label_unit_ditance_cameras")
        
        # add widgets to layout
        layout_distance.addWidget(self.label_distance_cameras)
        layout_distance.addItem(spacerItem30)
        layout_distance.addWidget(self.spinBox_distance_cameras)
        layout_distance.addWidget(self.label_unit_ditance_cameras)
        
        
        # --- frame for distance chip lense options ------------------------- #
        frame_distance_chip_lense = QtWidgets.QFrame(frame_camera_options)
        frame_distance_chip_lense.setMinimumSize(QtCore.QSize(0, 30))
        frame_distance_chip_lense.setMaximumSize(QtCore.QSize(16777215, 60))
        frame_distance_chip_lense.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_distance_chip_lense.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_distance_chip_lense.setObjectName("frame_distance_chip_lense")
        
        # layout
        layout_distance_cl = QtWidgets.QHBoxLayout(frame_distance_chip_lense)
        layout_distance_cl.setContentsMargins(0, 0, 0, 0)
        layout_distance_cl.setObjectName("layout_distance_cl")
        
        # label to display name of parameter "distance between chip and lense"
        self.label_distance_chip_lense = QtWidgets.QLabel(frame_distance_chip_lense)
        self.label_distance_chip_lense.setObjectName("label_distance_chip_lense")
 
        # horizontal spacer
        spacerItem31 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)

        # spin box for the distance between chip and lense
        self.spinBox_distance_chip_lense = QtWidgets.QDoubleSpinBox(frame_distance_chip_lense)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.spinBox_distance_chip_lense.sizePolicy().hasHeightForWidth())
        self.spinBox_distance_chip_lense.setSizePolicy(sizePolicy)
        self.spinBox_distance_chip_lense.setMinimumSize(QtCore.QSize(200, 40))
        self.spinBox_distance_chip_lense.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinBox_distance_chip_lense.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_distance_chip_lense.setMaximum(99999.99)
        self.spinBox_distance_chip_lense.setObjectName("spinBox_distance_chip_lense")
        
        # label to display the unit of the distance between chip and lense
        self.label_unit_chip_lense = QtWidgets.QLabel(frame_distance_chip_lense)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_unit_chip_lense.sizePolicy().hasHeightForWidth())
        self.label_unit_chip_lense.setSizePolicy(sizePolicy)
        self.label_unit_chip_lense.setMinimumSize(QtCore.QSize(50, 0))
        self.label_unit_chip_lense.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_unit_chip_lense.setObjectName("label_unit_chip_lense")
        
        # add widgets to layout
        layout_distance_cl.addWidget(self.label_distance_chip_lense)
        layout_distance_cl.addItem(spacerItem31)
        layout_distance_cl.addWidget(self.spinBox_distance_chip_lense)
        layout_distance_cl.addWidget(self.label_unit_chip_lense)
        
        
        # --- adding widgets to content (camera options) and main frame ----- #
        layout_camera_options.addWidget(frame_config)
        layout_camera_options.addWidget(frame_offset)
        layout_camera_options.addWidget(frame_distance_cameras)
        layout_camera_options.addWidget(frame_distance_chip_lense)
        layout_camera_options.addItem(spacerItem32)
        
        layout.addWidget(frame_camera_options, 0, 0, 1, 1)
        layout.addItem(spacerItem34, 0, 1, 1, 1)        
        layout.addItem(spacerItem35, 1, 0, 1, 1)   
        
        return tab_camera
        
    def createTabNeuralNetwork(self):
        # --- main frame (whole tab) ---------------------------------------- #
        tab_neuralNet = QtWidgets.QWidget(self)
        tab_neuralNet.setObjectName("tab_neuralNet")
        
        # main layout
        layout = QtWidgets.QGridLayout(tab_neuralNet)
        layout.setObjectName("layout")
        
        # spacers
        spacerItem39 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
        spacerItem40 = QtWidgets.QSpacerItem(20, 40, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)
        
        
        # --- frame for nn options ------------------------------------------ #
        frame_nn_options = QtWidgets.QFrame(tab_neuralNet)
        frame_nn_options.setStyleSheet("")
        frame_nn_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_nn_options.setObjectName("frame_nn_options")
        
        # layout
        layout_nn_options = QtWidgets.QVBoxLayout(frame_nn_options)
        layout_nn_options.setContentsMargins(11, 11, 11, 11)
        layout_nn_options.setSpacing(7)
        layout_nn_options.setObjectName("layout_nn_options")
        
        # vertical spacer
        spacerItem37 = QtWidgets.QSpacerItem(20, 40, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)
        
        
        # --- frame for nn path options ------------------------------------- #
        frame_nn_path_options = QtWidgets.QFrame(frame_nn_options)
        frame_nn_path_options.setMinimumSize(QtCore.QSize(0, 30))
        frame_nn_path_options.setMaximumSize(QtCore.QSize(16777215, 60))
        frame_nn_path_options.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_nn_path_options.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_nn_path_options.setObjectName("frame_nn_path_options")
        
        # layout
        layout_nn_path = QtWidgets.QHBoxLayout(frame_nn_path_options)
        layout_nn_path.setContentsMargins(0, 0, 0, 0)
        layout_nn_path.setObjectName("layout_nn_path")
        
        # label to display name of parameter "neural network path"
        self.label_nn = QtWidgets.QLabel(frame_nn_path_options)
        self.label_nn.setObjectName("label_nn")

        # horizontal spacer
        spacerItem36 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
        
        # line edit for nn path
        self.lineEdit_nn = QtWidgets.QLineEdit(frame_nn_path_options)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_nn.sizePolicy().hasHeightForWidth())
        self.lineEdit_nn.setSizePolicy(sizePolicy)
        self.lineEdit_nn.setMinimumSize(QtCore.QSize(400, 40))
        self.lineEdit_nn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_nn.setMaxLength(32767)
        self.lineEdit_nn.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_nn.setCursorPosition(0)
        self.lineEdit_nn.setReadOnly(True)
        self.lineEdit_nn.setObjectName("lineEdit_nn")
        
        # button for browsing for a nn
        self.btn_browse_nn = QtWidgets.QPushButton(frame_nn_path_options)
        self.btn_browse_nn.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_browse_nn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_browse_nn.setObjectName("btn_browse_nn")
        
        # add widgets to layout
        layout_nn_path.addWidget(self.label_nn)
        layout_nn_path.addItem(spacerItem36)
        layout_nn_path.addWidget(self.lineEdit_nn)        
        layout_nn_path.addWidget(self.btn_browse_nn)
       
        
        # --- adding widgets to content (nn options) and main frame --------- #
        layout_nn_options.addWidget(frame_nn_path_options)
        layout_nn_options.addItem(spacerItem37)
        
        layout.addWidget(frame_nn_options, 0, 0, 1, 1)
        layout.addItem(spacerItem39, 0, 1, 1, 1)
        layout.addItem(spacerItem40, 1, 0, 1, 1)
        
        return tab_neuralNet
           
    def createTabSpecies(self):
        # --- main frame (whole tab) ---------------------------------------- #
        tab_species = QtWidgets.QWidget(self)
        tab_species.setObjectName("tab_species")
        
        # main layout
        layout = QtWidgets.QGridLayout(tab_species)
        layout.setObjectName("layout")
        
        # horizontal spacer
        spacerItem43 = QtWidgets.QSpacerItem(600, 20, 
                                             QtWidgets.QSizePolicy.MinimumExpanding, 
                                             QtWidgets.QSizePolicy.Minimum)     
            
        # --- frame for species options ------------------------------------- #
        frame_species_options = QtWidgets.QFrame(tab_species)
        frame_species_options.setStyleSheet("")
        frame_species_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_species_options.setObjectName("frame_species_options")
        #frame_species_options.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.MinimumExpanding)
        
        # layout of options frame
        layout_species_options = QtWidgets.QVBoxLayout(frame_species_options)
        layout_species_options.setContentsMargins(11, 11, 11, 11)
        layout_species_options.setSpacing(7)
        layout_species_options.setObjectName("layout_species_options")
        
        # list view       
        self.listView_species = QtWidgets.QListView(frame_species_options)   
        self.listView_species.setStyleSheet("QListView{background-color:white; border-radius:3px; border:none;}\n"
                                "QListView::item:hover { background: rgb(0, 203, 221, 50); }\n"
                                "QListView::item:selected { background: rgb(0, 203, 221, 100); color:black;}\n")
        self.listView_species.setModel(self.models.model_species)
        self.listView_species.setWordWrap(True)
        
        self.delegate_species = Helpers.ListViewDelegate(None, self.listView_species)
        self.listView_species.setItemDelegate(self.delegate_species)
        
        # add widgets to main layout
        layout.addWidget(frame_species_options, 0, 0, 1, 1)
        layout.addItem(spacerItem43, 0, 1, 1, 1)  
        
        # --- frame for buttons --------------------------------------------- #
        # frame 
        frame_buttons = QtWidgets.QFrame(frame_species_options)
        frame_buttons.setMinimumSize(QtCore.QSize(0, 30))
        frame_buttons.setMaximumSize(QtCore.QSize(16777215, 60))
        frame_buttons.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_buttons.setObjectName("frame_buttons")

        # layout for buttons frame
        layout_buttons = QtWidgets.QHBoxLayout(frame_buttons)
        layout_buttons.setContentsMargins(0, 0, 0, 0)
        layout_buttons.setObjectName("layout_buttons")
        
        # button to add a list entry
        self.btn_add_species = QtWidgets.QPushButton(frame_buttons)
        self.btn_add_species.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_add_species.setObjectName("btn_add_species")
          
        # button to remove a list entry
        self.btn_remove_species = QtWidgets.QPushButton(frame_buttons)
        self.btn_remove_species.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_remove_species.setObjectName("btn_remove_species")
             
        # add widgets to layout
        layout_buttons.addWidget(self.btn_add_species)
        layout_buttons.addWidget(self.btn_remove_species)
        
        
        # --- content frame ------------------------------------------------- #
        # add widgets to species options frame
        layout_species_options.addWidget(self.listView_species)
        layout_species_options.addWidget(frame_buttons)  
 
        return tab_species

    def createTabUser(self):
        # --- main frame (whole tab) ---------------------------------------- #
        tab_user = QtWidgets.QWidget(self)
        tab_user.setObjectName("tab_user")
        
        # main layout
        gridLayout = QtWidgets.QGridLayout(tab_user)
        gridLayout.setObjectName("gridLayout")
        
        # spacers
        spacerItem48 = QtWidgets.QSpacerItem(609, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
        spacerItem49 = QtWidgets.QSpacerItem(20, 334, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)
        
        # --- frame for user options ---------------------------------------- #
        # frame for the user options
        frame_user_options = QtWidgets.QFrame(tab_user)
        frame_user_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_user_options.setObjectName("frame_user_options")
        
        # layout for the user options frame
        layout_user_options = QtWidgets.QVBoxLayout(frame_user_options)
        layout_user_options.setContentsMargins(11, 11, 11, 11)
        layout_user_options.setSpacing(7)
        layout_user_options.setObjectName("layout_user_options")       
        
        # vertical spacer
        spacerItem46 = QtWidgets.QSpacerItem(20, 40, 
                                             QtWidgets.QSizePolicy.Minimum, 
                                             QtWidgets.QSizePolicy.Expanding)

        
        # --- frame for user id options ------------------------------------- #
        # frame for the options for the user id
        frame_user_id = QtWidgets.QFrame(frame_user_options)
        frame_user_id.setMinimumSize(QtCore.QSize(0, 30))
        frame_user_id.setMaximumSize(QtCore.QSize(16777215, 60))
        frame_user_id.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_user_id.setObjectName("frame_user_id")

        # layout for user id options
        layout_user_id_row = QtWidgets.QHBoxLayout(frame_user_id)
        layout_user_id_row.setContentsMargins(0, 0, 0, 0)
        layout_user_id_row.setObjectName("layout_user_id_row")  
             
        # label to display name of parameter "user id"
        self.label_user_id = QtWidgets.QLabel(frame_user_id)
        self.label_user_id.setObjectName("label_user_id")
        
        # horizontal spacer
        spacerItem45 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
                
        # line edit for the user id
        self.lineEdit_user_id = QtWidgets.QLineEdit(frame_user_id)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit_user_id.sizePolicy().hasHeightForWidth())
        self.lineEdit_user_id.setSizePolicy(sizePolicy)
        self.lineEdit_user_id.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_user_id.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_user_id.setMaxLength(3)
        self.lineEdit_user_id.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_user_id.setCursorPosition(0)
        self.lineEdit_user_id.setReadOnly(False)
        self.lineEdit_user_id.setObjectName("lineEdit_user_id")
        
        # set a validator to ensure that the user ID consists of up to three letters (at least one letter)
        reg_ex = QtCore.QRegExp("[a-zA-Z]{1,3}")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_user_id)
        self.lineEdit_user_id.setValidator(input_validator)
        
        # add widgets to user id options layout
        layout_user_id_row.addWidget(self.label_user_id)
        layout_user_id_row.addItem(spacerItem45)
        layout_user_id_row.addWidget(self.lineEdit_user_id)
        
        
        # --- adding widgets to content (user options) and main frame ------- #
        # add widgets to user options frame        
        layout_user_options.addWidget(frame_user_id)
        layout_user_options.addItem(spacerItem46)
             
        # add widgets to main frame
        gridLayout.addWidget(frame_user_options, 0, 0, 1, 1)       
        gridLayout.addItem(spacerItem48, 0, 1, 1, 1)       
        gridLayout.addItem(spacerItem49, 1, 0, 1, 1)
        
        return tab_user


    def _initActions(self):
        # camera tab      
        self.lineEdit_config_path.textChanged.connect(self.apply_configFile)
        self.btn_load.clicked.connect(self.browse_config)
        self.btn_save.clicked.connect(self.save_config)       
        self.spinBox_offset.valueChanged.connect(self.camera_spinBox_changed)
        self.spinBox_distance_cameras.valueChanged.connect(self.camera_spinBox_changed)
        self.spinBox_distance_chip_lense.valueChanged.connect(self.camera_spinBox_changed)
        
        # neural net tab
        self.btn_browse_nn.clicked.connect(self.browse_for_nn)
        self.lineEdit_nn.textChanged.connect(self.nn_path_changed) #@todo kann man das überhaupt anpassen?
        
        # species tab
        self.btn_add_species.clicked.connect(self.browse_for_species_image)
        self.btn_remove_species.clicked.connect(self.removeSpecies)  
        
        # user tab
        self.lineEdit_user_id.textChanged.connect(self.user_id_changed)
        self.lineEdit_user_id.returnPressed.connect(lambda: self.focusNextChild())
             
                
# --- actions in camera tab ------------------------------------------------- #        
    def camera_spinBox_changed(self):
        # remove file path (it is not valid for the new spinBox values anymore)
        self.lineEdit_config_path.setText("")

    def browse_config(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(filter = "*.csv")
        self.apply_configFile(filename[0])
   
    def apply_configFile(self, path):
        # check if path is valid
        if path != "" and os.path.isfile(path): 
            df = pd.read_csv(path)
        
            # check format of file
            if(self.check_config_format(df)):
                # save old values of spinBoxes
                self.spinBox_offset_oldValue = self.spinBox_offset.value()
                self.spinBox_distance_cameras_oldValue = self.spinBox_distance_cameras.value()
                self.spinBox_distance_chip_lense_oldValue = self.spinBox_distance_chip_lense.value()
                
                # set the respective spinBox values
                self.spinBox_offset.setValue(df["y-offset"][0])
                self.spinBox_distance_cameras.setValue(df["camera-distance"][0])
                self.spinBox_distance_chip_lense.setValue(df["chip-distance"][0])
                
                # display the path to the file in the respective lineEdit
                self.lineEdit_config_path.setText(path)
                
                # set old value for config path
                self.lineEdit_config_path_oldValue = self.lineEdit_config_path.text()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("File Format Error")
                msg.setInformativeText('The given CSV file is not in the required format. Please make sure that it has the following columns with the correct data types:\n   "y-offset" (int64) \n   "camera-distance" (float64) \n   "chip-distance" (int64)')
                msg.setWindowTitle("Error")
                msg.exec_()  
            
        
    def check_config_format(self, df_config):
        # check if the necessary columns are present in the dataframe
        if "y-offset" in df_config.columns \
        and "camera-distance" in df_config.columns \
        and "chip-distance" in df_config.columns:
            return True
        else:
            return False
        
    def save_config(self):
        # create the file dialog
        dialog = QtWidgets.QFileDialog()
        filename = dialog.getSaveFileName(self, 'Save File', filter="*.csv")
        
        # fill the dataframe and write it
        data = {"y-offset": [self.spinBox_offset.value()], "camera-distance": [self.spinBox_distance_cameras.value()], "chip-distance": [self.spinBox_distance_chip_lense.value()]}
        df = pd.DataFrame(data)  
        df.to_csv(filename[0], index=False)

        # update the lineEdit
        self.lineEdit_config_path.setText(filename[0])
        
        
# --- actions in nn tab ----------------------------------------------------- #   
    def nn_path_changed(self, model_path):
        weights = np.array([ 1,  1.04084507,  1.04084507,  1,  1,
        8.90361446,  8.90361446, 13.19642857, 13.19642857, 12.52542373,
       12.52542373])

        print("load model...")
        self.nn_model = self.loadNn(model_path, weights)
        
    def loadNn(self, path, weights=None):
        if os.path.isfile(path):
            try:
                model = tf.keras.models.load_model(path, custom_objects={"loss": Losses.weighted_categorical_crossentropy(weights)})
                return model 
            except:
                # block signal (we do not want to call nn_path_changed) 
                # and set empty text in line edit
                self.lineEdit_nn.blockSignals(True)
                self.lineEdit_nn.setText("")
                self.lineEdit_nn.blockSignals(False)
                
                print("Entered neural network is not valid.")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Loading Error")
                msg.setInformativeText(f"The neural network from {path} is not a valid model.")
                msg.setWindowTitle("Error")
                msg.exec_()  
                return None    
        else:
            return None

        
    def browse_for_nn(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        path = filename[0]
        
        # check if path is valid
        if path != "" and os.path.isfile(path):    
            self.lineEdit_nn.setText(path)
        
# --- actions in species tab ------------------------------------------------ #
    def browse_for_species_image(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(filter = "*.png; *jpg")
        self.addSpecies(filename[0])
          
    def removeSpecies(self):
        row = self.listView_species.currentIndex().row()
        self.models.removeSpecies(row)
        
    def addSpecies(self, image_path, text=None):
        # take text as title or the image name
        if text is None:
            text = os.path.basename(image_path).split('.')[0]

        self.models.addSpecies(text, image_path)

# --- actions in user tab --------------------------------------------------- #  
    def user_id_changed(self):
        self.userIdChanged.emit(self.lineEdit_user_id.text())


# --- functions for saving and restoring options ---------------------------- # 
    def saveCurrentValues(self, settings):       
        settings.setValue("cameraConfigPath", self.lineEdit_config_path.text())       
        settings.setValue("nnPath", self.lineEdit_nn.text()) 
        settings.setValue("userId", self.lineEdit_user_id.text())

    def restoreValues(self, settings):
        self.apply_configFile(settings.value("cameraConfigPath"))
        self.lineEdit_nn.setText(settings.value("nnPath"))
        self.lineEdit_user_id.setText(settings.value("userId"))
        