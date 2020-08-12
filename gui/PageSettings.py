from PyQt5 import QtCore, QtGui, QtWidgets

from TabWidget import TabWidget
from Helpers import TopFrame, MenuFrame, get_icon

import time
"""
Class to create the settings page of the software.
"""
class PageSettings(QtWidgets.QWidget):

    def __init__(self, parent=None):
        start_time = time.time()
        super(QtWidgets.QWidget, self).__init__(parent)
                
        self.setStyleSheet("/*-------------------------- line edit ------------------------*/\n"
"QLineEdit{\n"
"    background-color:white;\n"
"    border-radius: 3px;\n"
"    font: 12pt \"Century Gothic\";\n"
"    selection-background-color:rgb(0, 203, 221);\n"
"    selection-color:white;\n"
"    color:black;\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"\n"
"\n"
"/*-------------------------- tab widget ------------------------*/\n"
"QTabWidget{\n"
"    font: 12pt \"Century Gothic\";\n"
"}\n"
"\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"       border:None;\n"
"}\n"
"\n"
"\n"
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
"#btn_apply_camera, #btn_apply_user, #btn_apply_species, #btn_apply_nn{\n"
"    background-color:rgb(150, 150, 150);\n"
"}\n"
"\n"
"#btn_load, #btn_save, #btn_browse_nn{\n"
"    background-color:rgb(200, 200, 200);\n"
"}\n"
"\n"
"\n"
"#btn_apply_camera:hover , \n"
"#btn_apply_user:hover, \n"
"#btn_apply_species:hover, \n"
"#btn_apply_nn:hover,\n"
"#btn_load:hover, #btn_save:hover, \n"
"#btn_browse_nn:hover{\n"
"  background-color: rgb(0, 203, 221);\n"
"}\n"
"\n"
"#btn_apply_camera:pressed , \n"
"#btn_apply_user:pressed, \n"
"#btn_apply_species:pressed, \n"
"#btn_apply_nn:pressed,\n"
"#btn_load:pressed, #btn_save:pressed,\n"
"#btn_browse_nn:pressed{\n"
"background-color: rgb(0, 160, 174);\n"
"}\n"
"\n"
"\n"
"\n"
"/*-------------------------- double spin boxes ------------------------*/\n"
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
"}\n"
"")
        self.setObjectName("page_settings")
        
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        
        # top bar (the blue one on every page)
        self.frame_topBar = TopFrame(":/icons/icons/settings.png", "frame_settingsBar")
        self.verticalLayout_4.addWidget(self.frame_topBar)
        
        # menu bar on about page
        self.frame_controlBar = MenuFrame("Settings", "frame_controlBar_settings")
        self.verticalLayout_4.addWidget(self.frame_controlBar)
    
        # main frame for the settings
        self.frame_settings = QtWidgets.QFrame(self)
        self.frame_settings.setStyleSheet("")
        self.frame_settings.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_settings.setObjectName("frame_settings")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_settings)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
                
        # custom tab widget (with horizontal texts on the left side)
        self.tabWidget = TabWidget(self.frame_settings)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        
        # tab for camera settings
        self.tab_camera = QtWidgets.QWidget()
        self.tab_camera.setObjectName("tab_camera")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_camera)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_camera_options = QtWidgets.QFrame(self.tab_camera)
        self.frame_camera_options.setStyleSheet("")
        self.frame_camera_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_camera_options.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_camera_options.setObjectName("frame_camera_options")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_camera_options)
        self.verticalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_6.setSpacing(7)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_config = QtWidgets.QFrame(self.frame_camera_options)
        self.frame_config.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_config.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_config.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_config.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_config.setObjectName("frame_config")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_config)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.lineEdit_config_path = QtWidgets.QLineEdit(self.frame_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_config_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_config_path.setSizePolicy(sizePolicy)
        self.lineEdit_config_path.setMinimumSize(QtCore.QSize(400, 40))
        self.lineEdit_config_path.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_config_path.setInputMask("")
        self.lineEdit_config_path.setText("")
        self.lineEdit_config_path.setReadOnly(True)
        self.lineEdit_config_path.setObjectName("lineEdit_config_path")
        
        self.horizontalLayout_11.addWidget(self.lineEdit_config_path)
        
        self.btn_load = QtWidgets.QPushButton(self.frame_config)
        self.btn_load.setMinimumSize(QtCore.QSize(125, 40))
        self.btn_load.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_load.setObjectName("btn_load")
        self.horizontalLayout_11.addWidget(self.btn_load)
        
        self.btn_save = QtWidgets.QPushButton(self.frame_config)
        self.btn_save.setMinimumSize(QtCore.QSize(125, 40))
        self.btn_save.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_11.addWidget(self.btn_save)
        
        self.verticalLayout_6.addWidget(self.frame_config)
        
        self.frame_offset = QtWidgets.QFrame(self.frame_camera_options)
        self.frame_offset.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_offset.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_offset.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_offset.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_offset.setObjectName("frame_offset")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_offset)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_offset = QtWidgets.QLabel(self.frame_offset)
        self.label_offset.setObjectName("label_offset")
        self.horizontalLayout_12.addWidget(self.label_offset)
        spacerItem29 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem29)
        
        self.spinBox_offset = QtWidgets.QDoubleSpinBox(self.frame_offset)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_offset.sizePolicy().hasHeightForWidth())
        self.spinBox_offset.setSizePolicy(sizePolicy)
        self.spinBox_offset.setMinimumSize(QtCore.QSize(200, 40))
        self.spinBox_offset.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinBox_offset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_offset.setPrefix("")
        self.spinBox_offset.setMaximum(9999.99)
        self.spinBox_offset.setObjectName("spinBox_offset")
        self.horizontalLayout_12.addWidget(self.spinBox_offset)
        
        self.label_unit_offset = QtWidgets.QLabel(self.frame_offset)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_unit_offset.sizePolicy().hasHeightForWidth())
        self.label_unit_offset.setSizePolicy(sizePolicy)
        self.label_unit_offset.setMinimumSize(QtCore.QSize(50, 0))
        self.label_unit_offset.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_unit_offset.setObjectName("label_unit_offset")
        self.horizontalLayout_12.addWidget(self.label_unit_offset)
        self.verticalLayout_6.addWidget(self.frame_offset)
        self.frame_distance_cameras = QtWidgets.QFrame(self.frame_camera_options)
        self.frame_distance_cameras.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_distance_cameras.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_distance_cameras.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_distance_cameras.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_distance_cameras.setObjectName("frame_distance_cameras")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_distance_cameras)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_distance_cameras = QtWidgets.QLabel(self.frame_distance_cameras)
        self.label_distance_cameras.setObjectName("label_distance_cameras")
        self.horizontalLayout_13.addWidget(self.label_distance_cameras)
        spacerItem30 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem30)
        self.spinBox_distance_cameras = QtWidgets.QDoubleSpinBox(self.frame_distance_cameras)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_distance_cameras.sizePolicy().hasHeightForWidth())
        self.spinBox_distance_cameras.setSizePolicy(sizePolicy)
        self.spinBox_distance_cameras.setMinimumSize(QtCore.QSize(200, 40))
        self.spinBox_distance_cameras.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinBox_distance_cameras.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_distance_cameras.setPrefix("")
        self.spinBox_distance_cameras.setMaximum(9999.99)
        self.spinBox_distance_cameras.setObjectName("spinBox_distance_cameras")
        self.horizontalLayout_13.addWidget(self.spinBox_distance_cameras)
        self.label_unit_ditance_cameras = QtWidgets.QLabel(self.frame_distance_cameras)
        self.label_unit_ditance_cameras.setMinimumSize(QtCore.QSize(50, 0))
        self.label_unit_ditance_cameras.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_unit_ditance_cameras.setObjectName("label_unit_ditance_cameras")
        self.horizontalLayout_13.addWidget(self.label_unit_ditance_cameras)
        self.verticalLayout_6.addWidget(self.frame_distance_cameras)
        self.frame_distance_chip_lense = QtWidgets.QFrame(self.frame_camera_options)
        self.frame_distance_chip_lense.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_distance_chip_lense.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_distance_chip_lense.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_distance_chip_lense.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_distance_chip_lense.setObjectName("frame_distance_chip_lense")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_distance_chip_lense)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_distance_chip_lense = QtWidgets.QLabel(self.frame_distance_chip_lense)
        self.label_distance_chip_lense.setObjectName("label_distance_chip_lense")
        self.horizontalLayout_14.addWidget(self.label_distance_chip_lense)
        spacerItem31 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem31)
        self.spinBox_distance_chip_lense = QtWidgets.QDoubleSpinBox(self.frame_distance_chip_lense)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_distance_chip_lense.sizePolicy().hasHeightForWidth())
        self.spinBox_distance_chip_lense.setSizePolicy(sizePolicy)
        self.spinBox_distance_chip_lense.setMinimumSize(QtCore.QSize(200, 40))
        self.spinBox_distance_chip_lense.setMaximumSize(QtCore.QSize(16777215, 40))
        self.spinBox_distance_chip_lense.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_distance_chip_lense.setPrefix("")
        self.spinBox_distance_chip_lense.setMaximum(99999.99)
        self.spinBox_distance_chip_lense.setObjectName("spinBox_distance_chip_lense")
        self.horizontalLayout_14.addWidget(self.spinBox_distance_chip_lense)
        self.label_unit_chip_lense = QtWidgets.QLabel(self.frame_distance_chip_lense)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_unit_chip_lense.sizePolicy().hasHeightForWidth())
        self.label_unit_chip_lense.setSizePolicy(sizePolicy)
        self.label_unit_chip_lense.setMinimumSize(QtCore.QSize(50, 0))
        self.label_unit_chip_lense.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_unit_chip_lense.setObjectName("label_unit_chip_lense")
        self.horizontalLayout_14.addWidget(self.label_unit_chip_lense)
        self.verticalLayout_6.addWidget(self.frame_distance_chip_lense)
        spacerItem32 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem32)
        self.frame_apply = QtWidgets.QFrame(self.frame_camera_options)
        self.frame_apply.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_apply.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_apply.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_apply.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_apply.setObjectName("frame_apply")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_apply)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem33 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem33)
        
        self.btn_apply_camera = QtWidgets.QPushButton(self.frame_apply)
        self.btn_apply_camera.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_apply_camera.setStyleSheet("font:bold;")
        self.btn_apply_camera.setObjectName("btn_apply_camera")
        self.btn_apply_camera.setEnabled(False)
        self.horizontalLayout_16.addWidget(self.btn_apply_camera)
        
        self.verticalLayout_6.addWidget(self.frame_apply)
        self.gridLayout_3.addWidget(self.frame_camera_options, 0, 0, 1, 1)
        spacerItem34 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem34, 0, 1, 1, 1)
        spacerItem35 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem35, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_camera, get_icon(":/icons/icons/camera.png"), "")
        
        # tab for neural net
        self.tab_neuralNet = QtWidgets.QWidget()
        self.tab_neuralNet.setObjectName("tab_neuralNet")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_neuralNet)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_nn_options = QtWidgets.QFrame(self.tab_neuralNet)
        self.frame_nn_options.setStyleSheet("")
        self.frame_nn_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_nn_options.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_nn_options.setObjectName("frame_nn_options")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.frame_nn_options)
        self.verticalLayout_17.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_17.setSpacing(7)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.frame_nn_info = QtWidgets.QFrame(self.frame_nn_options)
        self.frame_nn_info.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_nn_info.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_nn_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_nn_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_nn_info.setObjectName("frame_nn_info")
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout(self.frame_nn_info)
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.label_nn = QtWidgets.QLabel(self.frame_nn_info)
        self.label_nn.setObjectName("label_nn")
        self.horizontalLayout_36.addWidget(self.label_nn)
        spacerItem36 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_36.addItem(spacerItem36)
        
        self.lineEdit_nn = QtWidgets.QLineEdit(self.frame_nn_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_nn.sizePolicy().hasHeightForWidth())
        self.lineEdit_nn.setSizePolicy(sizePolicy)
        self.lineEdit_nn.setMinimumSize(QtCore.QSize(400, 40))
        self.lineEdit_nn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_nn.setStyleSheet("")
        self.lineEdit_nn.setInputMask("")
        self.lineEdit_nn.setText("")
        self.lineEdit_nn.setMaxLength(32767)
        self.lineEdit_nn.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_nn.setCursorPosition(0)
        self.lineEdit_nn.setReadOnly(True)
        self.lineEdit_nn.setObjectName("lineEdit_nn")
        self.horizontalLayout_36.addWidget(self.lineEdit_nn)
        
        self.btn_browse_nn = QtWidgets.QPushButton(self.frame_nn_info)
        self.btn_browse_nn.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_browse_nn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_browse_nn.setObjectName("btn_browse_nn")
        self.horizontalLayout_36.addWidget(self.btn_browse_nn)
        
        self.verticalLayout_17.addWidget(self.frame_nn_info)
        spacerItem37 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_17.addItem(spacerItem37)
        self.frame_apply_nn = QtWidgets.QFrame(self.frame_nn_options)
        self.frame_apply_nn.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_apply_nn.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_apply_nn.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_apply_nn.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_apply_nn.setObjectName("frame_apply_nn")
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout(self.frame_apply_nn)
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        spacerItem38 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_37.addItem(spacerItem38)
        
        self.btn_apply_nn = QtWidgets.QPushButton(self.frame_apply_nn)
        self.btn_apply_nn.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_apply_nn.setStyleSheet("font:bold;")
        self.btn_apply_nn.setObjectName("btn_apply_nn")
        self.btn_apply_nn.setEnabled(False)
        self.horizontalLayout_37.addWidget(self.btn_apply_nn)
        
        self.verticalLayout_17.addWidget(self.frame_apply_nn)
        self.gridLayout_4.addWidget(self.frame_nn_options, 0, 0, 1, 1)
        spacerItem39 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem39, 0, 1, 1, 1)
        spacerItem40 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem40, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_neuralNet, get_icon(":/icons/icons/nn.png"), "")
        
        # tab for species
        self.tab_species = QtWidgets.QWidget()
        self.tab_species.setObjectName("tab_species")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_species)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.frame_species_options = QtWidgets.QFrame(self.tab_species)
        self.frame_species_options.setStyleSheet("")
        self.frame_species_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_species_options.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_species_options.setObjectName("frame_species_options")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_species_options)
        self.verticalLayout_10.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_10.setSpacing(7)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.listView = QtWidgets.QListView(self.frame_species_options)
        self.listView.setStyleSheet("background-color:white;\n"
"border-radius:3px;")
        self.listView.setObjectName("listView")
        self.verticalLayout_10.addWidget(self.listView)
        spacerItem41 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem41)
        self.frame_apply_species = QtWidgets.QFrame(self.frame_species_options)
        self.frame_apply_species.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_apply_species.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_apply_species.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_apply_species.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_apply_species.setObjectName("frame_apply_species")
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout(self.frame_apply_species)
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        spacerItem42 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_35.addItem(spacerItem42)
        
        self.btn_apply_species = QtWidgets.QPushButton(self.frame_apply_species)
        self.btn_apply_species.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_apply_species.setStyleSheet("font:bold;")
        self.btn_apply_species.setObjectName("btn_apply_species")
        self.btn_apply_species.setEnabled(False)
        self.horizontalLayout_35.addWidget(self.btn_apply_species)
        
        self.verticalLayout_10.addWidget(self.frame_apply_species)
        self.gridLayout_6.addWidget(self.frame_species_options, 0, 0, 1, 1)
        spacerItem43 = QtWidgets.QSpacerItem(609, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem43, 0, 1, 1, 1)
        spacerItem44 = QtWidgets.QSpacerItem(20, 334, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem44, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_species, get_icon(":/icons/icons/fish.png"), "")
        
        # tab for user settings
        self.tab_user = QtWidgets.QWidget()
        self.tab_user.setObjectName("tab_user")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_user)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_user_options = QtWidgets.QFrame(self.tab_user)
        self.frame_user_options.setStyleSheet("")
        self.frame_user_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_user_options.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_user_options.setObjectName("frame_user_options")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_user_options)
        self.verticalLayout_9.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_9.setSpacing(7)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_distance_chip_lense_4 = QtWidgets.QFrame(self.frame_user_options)
        self.frame_distance_chip_lense_4.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_distance_chip_lense_4.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_distance_chip_lense_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_distance_chip_lense_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_distance_chip_lense_4.setObjectName("frame_distance_chip_lense_4")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout(self.frame_distance_chip_lense_4)
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_distance_chip_lense_4 = QtWidgets.QLabel(self.frame_distance_chip_lense_4)
        self.label_distance_chip_lense_4.setObjectName("label_distance_chip_lense_4")
        self.horizontalLayout_32.addWidget(self.label_distance_chip_lense_4)
        spacerItem45 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_32.addItem(spacerItem45)
        
        self.lineEdit_user_id = QtWidgets.QLineEdit(self.frame_distance_chip_lense_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_user_id.sizePolicy().hasHeightForWidth())
        self.lineEdit_user_id.setSizePolicy(sizePolicy)
        self.lineEdit_user_id.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_user_id.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_user_id.setStyleSheet("")
        self.lineEdit_user_id.setInputMask("")
        self.lineEdit_user_id.setText("")
        self.lineEdit_user_id.setMaxLength(3)
        self.lineEdit_user_id.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_user_id.setCursorPosition(0)
        self.lineEdit_user_id.setReadOnly(False)
        self.lineEdit_user_id.setObjectName("lineEdit_user_id")
        
        # set a validator to ensure that the user ID consists of up to three letters (at least one)
        reg_ex = QtCore.QRegExp("[a-zA-Z]{1,3}")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_user_id)
        self.lineEdit_user_id.setValidator(input_validator)
        
        self.horizontalLayout_32.addWidget(self.lineEdit_user_id)
        
        self.verticalLayout_9.addWidget(self.frame_distance_chip_lense_4)
        spacerItem46 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem46)
        self.frame_apply_user = QtWidgets.QFrame(self.frame_user_options)
        self.frame_apply_user.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_apply_user.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_apply_user.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_apply_user.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_apply_user.setObjectName("frame_apply_user")
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.frame_apply_user)
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        spacerItem47 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_33.addItem(spacerItem47)
        
        self.btn_apply_user = QtWidgets.QPushButton(self.frame_apply_user)
        self.btn_apply_user.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_apply_user.setStyleSheet("font:bold;")
        self.btn_apply_user.setObjectName("btn_apply_user")
        self.btn_apply_user.setEnabled(False)
        self.horizontalLayout_33.addWidget(self.btn_apply_user)
        
        self.verticalLayout_9.addWidget(self.frame_apply_user)
        self.gridLayout.addWidget(self.frame_user_options, 0, 0, 1, 1)
        spacerItem48 = QtWidgets.QSpacerItem(609, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem48, 0, 1, 1, 1)
        spacerItem49 = QtWidgets.QSpacerItem(20, 334, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem49, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_user, get_icon(":/icons/icons/user_b.png"), "")

        
        self.horizontalLayout_10.addWidget(self.tabWidget)
        self.verticalLayout_4.addWidget(self.frame_settings)


        #print(f"page settings init: {time.time() - start_time}")






        
    # def apply_settings_decision(self, answer):
    #     if answer.text() == "&Yes": 
    #         # apply the new values
    #         self.apply_all_settings()
    #     else:
    #         # restore all not applied values
    #         self.restore_old_settings()
    
    # def apply_all_settings(self):
    #     self.camera_apply_btn_pressed()
    #     self.nn_apply_btn_pressed()
    #     self.user_apply_btn_pressed()
    #     self.species_apply_btn_pressed()
    
    # def restore_old_settings(self):
    #     print(self.lineEdit_config_path_oldValue)
        
    #     if self.btn_apply_camera.isEnabled() == True:   
    #         self.spinBox_offset.setValue(self.spinBox_offset_oldValue)
    #         self.spinBox_distance_cameras.setValue(self.spinBox_distance_cameras_oldValue)
    #         self.spinBox_distance_chip_lense.setValue(self.spinBox_distance_chip_lense_oldValue)
    #         self.lineEdit_config_path.setText(self.lineEdit_config_path_oldValue)   
    #         self.btn_apply_camera.setEnabled(False)
        
    #     if self.btn_apply_nn.isEnabled() == True:
    #         self.lineEdit_nn.setText(self.lineEdit_nn_oldValue)
    #         self.btn_apply_nn.setEnabled(False)
            
    #     if self.btn_apply_species.isEnabled() == True:
    #         print("not implemented yet")
    #         self.btn_apply_species.setEnabled(False)
        
    #     if self.btn_apply_user.isEnabled() == True:
    #          self.lineEdit_user_id.setText(self.lineEdit_user_id_oldValue)
    #          self.btn_apply_user.setEnabled(False)
             
    # # -------------------- species settings -------------------------------- # 
    # def species_apply_btn_pressed(self):
    #     print("not implemented yet")
        
    # def species_changed(self):
    #     self.btn_apply_species.setEnabled(True)
        
    # # -------------------- user settings -------------------------------- #     
    # def user_apply_btn_pressed(self):
    #      # disable apply btn
    #     self.btn_apply_user.setEnabled(False)

    #     # save the new value
    #     self.lineEdit_user_id_oldValue = self.lineEdit_user_id.text()    
        
    #     # update the userId in the top bar of the software (on every page)
    #     self.label_user_id.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_data.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_settings.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_handbook.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_about.setText(self.lineEdit_user_id_oldValue)
        
    #     # also update the dummy userIds to preserve the symmetry of the bar
    #     self.label_user_id_2.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_data_2.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_settings_2.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_handbook_2.setText(self.lineEdit_user_id_oldValue)
    #     self.label_user_id_about_2.setText(self.lineEdit_user_id_oldValue)
        
    
    # def user_id_changed(self):
    #     self.btn_apply_user.setEnabled(True)
        
    # def direct_to_user_settings(self):
    #     self.action_to_settings_page()
    #     self.tabWidget.setCurrentIndex(3)
    
    # # -------------------- nn settings -------------------------------- # 
    # def nn_apply_btn_pressed(self):
    #     # disable apply btn
    #     self.btn_apply_nn.setEnabled(False)

    #     # save the new value
    #     self.lineEdit_nn_oldValue = self.lineEdit_nn.text()
    
    # def nn_path_changed(self):
    #     self.btn_apply_nn.setEnabled(True)
        
    # def browse_for_nn(self):
    #     filename = QtWidgets.QFileDialog.getOpenFileName()
    #     self.lineEdit_nn.setText(filename[0])
    #     # @todo!! make use of NN
    
    # # -------------------- camera settings -------------------------------- # 
    # def camera_apply_btn_pressed(self):
    #     # disable apply btn
    #     self.btn_apply_camera.setEnabled(False)
        
    #     # save the new values of the spinBoxes and the file path
    #     self.lineEdit_config_path_oldValue = self.lineEdit_config_path.text()
    #     self.spinBox_offset_oldValue = self.spinBox_offset.value()
    #     self.spinBox_distance_cameras_oldValue = self.spinBox_distance_cameras.value()
    #     self.spinBox_distance_chip_lense_oldValue = self.spinBox_distance_chip_lense.value()
        

    # def camera_spinBox_changed(self):
    #     # enable apply button
    #     self.btn_apply_camera.setEnabled(True)
        
    #     # remove file path (it is not valid for the new spinBox values anymore)
    #     self.lineEdit_config_path.setText("")
        
    
    # def check_all_settings(self):
    #     # check if there are not applied settings
    #     if self.btn_apply_camera.isEnabled() == True or \
    #         self.btn_apply_nn.isEnabled() == True or \
    #         self.btn_apply_species.isEnabled() == True or \
    #         self.btn_apply_user.isEnabled() == True:
 
    #         # if not all changes to the settings were applied, ask the user what to do
    #         msg = QtWidgets.QMessageBox()
    #         msg.setIcon(QtWidgets.QMessageBox.Question)
    #         msg.setText("Do you want to apply the changes to the settings?")
    #         msg.setWindowTitle("Settings changed")
    #         msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    #         msg.buttonClicked.connect(self.apply_settings_decision)
    #         msg.exec_()


    
    # def load_config(self):
    #     filename = QtWidgets.QFileDialog.getOpenFileName(filter = "*.csv")
    #     df = pd.read_csv(filename[0])
        
    #     # check format of file
    #     if(self.check_config_format(df)):
    #         # save old values of spinBoxes
    #         self.spinBox_offset_oldValue = self.spinBox_offset.value()
    #         self.spinBox_distance_cameras_oldValue = self.spinBox_distance_cameras.value()
    #         self.spinBox_distance_chip_lense_oldValue = self.spinBox_distance_chip_lense.value()
            
    #         # set the respective spinBox values
    #         self.spinBox_offset.setValue(df["y-offset"][0])
    #         self.spinBox_distance_cameras.setValue(df["camera-distance"][0])
    #         self.spinBox_distance_chip_lense.setValue(df["chip-distance"][0])
            
    #         # display the path to the file in the respective lineEdit
    #         self.lineEdit_config_path.setText(filename[0])
            
    #         # set old value for config path
    #         self.lineEdit_config_path_oldValue = self.lineEdit_config_path.text()
    #     else:
    #         msg = QtWidgets.QMessageBox()
    #         msg.setIcon(QtWidgets.QMessageBox.Critical)
    #         msg.setText("File Format Error")
    #         msg.setInformativeText('The given CSV file is not in the required format. Please make sure that it has the following columns with the correct data types:\n   "y-offset" (int64) \n   "camera-distance" (float64) \n   "chip-distance" (int64)')
    #         msg.setWindowTitle("Error")
    #         msg.exec_()
      
    # def check_config_format(self, df_config):
    #     type_dict = dict(df_config.dtypes)

    #     # check if the necessary columns are present in the dataframe
    #     if "y-offset" in df_config.columns and "camera-distance" in df_config.columns and "chip-distance" in df_config.columns:
    #         return True
    #     else:
    #         return False
        
        
        
    # def save_config(self):
    #     # create the file dialog
    #     dialog = QtWidgets.QFileDialog()
    #     filename = dialog.getSaveFileName(self, 'Save File', filter="*.csv")
        
    #     # fill the dataframe and write it
    #     data = {"y-offset": [self.spinBox_offset.value()], "camera-distance": [self.spinBox_distance_cameras.value()], "chip-distance": [self.spinBox_distance_chip_lense.value()]}
    #     df = pd.DataFrame(data)  
    #     df.to_csv(filename[0], index=False)

    #     # update the lineEdit
    #     self.lineEdit_config_path.setText(filename[0])