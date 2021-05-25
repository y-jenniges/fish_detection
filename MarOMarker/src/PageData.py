import os
import json
import glob
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui
from Animal import Animal
from Helpers import TopFrame, MenuFrame, displayErrorMsg, ProgressBar
import PostProcessing as pp
from Predicter import Predicter, PredictionWorker
from DistanceMeasurer import DistanceMeasurer


IMAGE_SIZE = (4272, 2848)
#IMAGE_SIZE = (2848, 4272)

class PageData(QtWidgets.QWidget): 
    """ Class to create the data page of the software.
    
    Attributes
    ----------
    predicter : Predicter
        Applies the neural network and performs post processing to generate
        animal information.
    config_path : string
        Path to the camera configuration file. TODO: replace this configuration 
        by the configuration loadable on settings page. 
    matcher : StereoCorrespondence
        For the animals on the left image, it finds corresponding animals 
        on the right image. 
    distance_measurer : DistanceMeasurer
        Calculates the length of animals.  
    imageDirChanged : pyqtSignal
    outputDirectoryChanged : pyqtSignal
    imagePrefixChanged : pyqtSignal
    experimentIdChanged : pyqtSignal
    """
    # define custom signals
    imageDirChanged = QtCore.pyqtSignal(str)
    """ Signal emitted when the image directory is changed. """
    
    outputDirectoryChanged = QtCore.pyqtSignal(str)
    """ Signal emitted when the output directory is changed. """
    
    imagePrefixChanged = QtCore.pyqtSignal(str)
    """ Signal emitted when the image prefix is changed. """
    
    experimentIdChanged = QtCore.pyqtSignal(str)
    """ Signal emitted when the experiment ID is changed. """
    
    def __init__(self, models, parent=None):     
        super(QtWidgets.QWidget, self).__init__(parent)
        # data models
        self.models = models
        
        # init UI, actions
        self._initUi()
        self._initActions()
        
        # create object to predict images
        self.predicter = Predicter()
        
        # camera configuration @todo needs to be set to file used in settings and adaptable by the parameters that are set there
        config_path = "config.json" # default camera config
        self.onCameraConfigChanged(config_path)
        
        self.onCalenderSelectionChanged()
     
    def onCameraConfigChanged(self, config_path):
        """ Loads a new camera configuration from a json file path. """
        print("loadi loadi loadi cami config")
        # read camera config
        self.camera_config = {}
        with open(config_path, 'r') as f:
            self.camera_config = json.load(f)
        
        # instantiate a matcher to find matching animals on left and right image
        self.matcher = pp.StereoCorrespondence(self.camera_config['mtx_L'], 
                                              self.camera_config['dist_L'],
                                              self.camera_config['mtx_R'], 
                                              self.camera_config['dist_R'],
                                              self.camera_config['R'], 
                                              self.camera_config['T'], IMAGE_SIZE)
        
        # instantiate a distance-measurer to determine length of animals
        self.distance_measurer = DistanceMeasurer(self.camera_config['mtx_L'], 
                                                 self.camera_config['dist_L'],
                                                 self.camera_config['mtx_R'], 
                                                 self.camera_config['dist_R'],
                                                 self.camera_config['R'], 
                                                 self.camera_config['T'], IMAGE_SIZE)       
        
        # recalculate length of animals
        self.onCalcLength()
        
    def onImageDirEditChanged(self, text=None, updateVisuals=True):
        """ Function to handle when the user changes the img_dir line edit """
        if text is None: text = self.lineEdit_img_dir.text()

        if not os.path.isdir(text): # check if directory exists
            self.lineEdit_img_dir.setText("")
            print("The entered img dir is not a valid path.") 
            
        # check for output file, if it exists, otherwise create one
        self.onOutDirChanged()
            
        self.updateNumImages()
        self.imageDirChanged.emit(self.lineEdit_img_dir.text())
     
    def onOutDirChanged(self):
        """ Function to handle when the user changes the output dir line edit.
        It makes sure that a result file exists and creates one otherwise. """
        # current output directory
        out_dir = self.lineEdit_output_dir.text()
        
        if not os.path.isdir(out_dir): # check if directory exists
            self.lineEdit_output_dir.setText("")
            print("The entered output dir is not a valid path.") 
        else:
            # if result file does not exist yet, create one
            main_window = self.parent().parent()
            if main_window is not None:
                res_file = main_window.getResultFileName()
                path = os.path.join(out_dir, res_file)
                
                if not os.path.isfile(path):
                    print(f"creating out file {path}")
                    self.models.model_animals.exportToCsv(out_dir, res_file)
                else:
                    print(f"load out file {path}")
                    self.models.model_animals.loadFile(path)
        
        self.outputDirectoryChanged.emit(self.lineEdit_output_dir.text())
        
    def onPrefixEditChanged(self):
        """ Function to handle when the user changes the image prefix line edit """
        self.imagePrefixChanged.emit(self.lineEdit_img_prefix.text())
        self.updateNumImages()    
    
    def onExpIdEditChanged(self):
        """ Function to handle when the user changes the experiment id line edit """
        self.experimentIdChanged.emit(self.lineEdit_exp_id.text())
        
    def updateNumImages(self):
        """ Function to check how many images are in the current 
        image directory with the current prefix for the current date and 
        updates the display of this count """
        date = self.calendarWidget.selectedDate().toString("yyyy.MM.dd")
        images_with_prefix = glob.glob(self.lineEdit_img_dir.text() \
                                       + self.lineEdit_img_prefix.text() + "*")
        images_with_date = [x for x in images_with_prefix if date in x]
        num_images = str(len(images_with_date))
        
        self.label_num_imgs_text.setText(num_images)   
        
    def onBrowseOutDir(self):
        """ Function that opens a dialog for the user to select an output
        directory. """
        
        filename = QtWidgets.QFileDialog.getExistingDirectory(
            self, self.tr("Select Output Directory"), "", 
            QtWidgets.QFileDialog.ShowDirsOnly)
        
        print(f"PageData: onBrowseOutDir {filename}")
        
        if len(filename) > 0: 
            if os.path.isdir(filename):
                self.lineEdit_output_dir.setText(filename + "/")
                self.onImageDirEditChanged(filename + "/")
                
        self.onOutDirChanged()
      
    def onBrowseImageDir(self):
        """ Function that opens a dialog for the user to select a directory 
        where the images are """
        filename = QtWidgets.QFileDialog.getExistingDirectory(
            self, self.tr("Open Image Directory"), "", 
            QtWidgets.QFileDialog.ShowDirsOnly)
        
        if len(filename) > 0: 
            if os.path.isdir(filename):
                self.lineEdit_img_dir.setText(filename + "/")
                self.onImageDirEditChanged(filename + "/")

    def updateImageDir(self):
        """ Function to update the image directory according to the input 
        from the calender widget """
        try:
            img_root_dir = self.parent().parent().page_settings.lineEdit_root_dir.text()
            date = self.calendarWidget.selectedDate().toString("yyyy_MM")
            directory = img_root_dir + "/" + date + "/" 
            print(img_root_dir)
            print(directory)
            # enable frame to manipulate data properties
            self.frame_data_information.setEnabled(True) 
            
            # if directory does not exist, clear the image directory
            if not os.path.isdir(directory):
                self.lineEdit_img_dir.setText("")
            else:
                self.lineEdit_img_dir.setText(directory)
                self.onImageDirEditChanged(directory)
            
            # update the number of images
            self.updateNumImages() 
    
            # adapt experiment id  
            new_exp_id = "Spitzbergen " \
                + str(self.calendarWidget.selectedDate().year())     
            self.lineEdit_exp_id.setText(new_exp_id) 
            self.onExpIdEditChanged()
        except:
            print("PageData: Cannot update image directory yet.")
        
    def onCalenderSelectionChanged(self):
        """ Function to handle a change of the calender widget selection. """
        # set the date label
        self.label_date.setText(self.calendarWidget.selectedDate() \
                                .toString("dd.MM.yyyy")) 
        
        # adapt image directory
        self.updateImageDir()       
 
    def _createFrameData(self):
        """ Creates the data page UI. """
        # data frame
        frame_data = QtWidgets.QFrame(self)
        frame_data.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        frame_data.setAccessibleName("")
        frame_data.setStyleSheet(
            "QLabel{ \n"
            "    color:black; \n"
            "    background-color:transparent;\n"
            "}\n"
            "\n"
            "QLabel:disabled{\n"
            "    color: rgb(150, 150 ,150);\n"
            "}\n"
            "\n"
            "#frame_data_selection, #frame_data_information{\n"
            "    background-color:rgb(230, 230, 230);  \n"
            "    border-radius:3px;\n"
            "}\n"
            "\n"
            "/*------------------------- frames --------------------------*/\n"
            "#frame_data_options{background-color:rgb(230,230,230); border:none; border-radius:3px;}"
            "#frame_nn_activation, #frame_pred_check, #frame_rectify_match, "
            "#frame_check_match, #frame_length_measurement{"
            "   background-color: rgb(230, 230, 230); "
            "   border:none; "
            "   border-radius:3px;}"
            "\n"
            "/*------------------------ line edit ------------------------*/\n"
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
            "QLineEdit:disabled{\n"
            "    color: rgb(200, 200, 200);\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "/*-------------------------- buttons ------------------------*/\n"
            "QPushButton{\n"
            "    font: 10pt \"Century Gothic\";\n"
            "    border:none; border-radius:3px;\n"
            "    padding:10;"
            "}\n"
            "\n"
            "#btn_out_dir, #btn_img_dir, #btn_nn_activation, #btn_pred_check,"
            "#btn_rectify_match, #btn_check_match, #btn_length_measurement{\n"
            "    background-color: rgb(200, 200, 200);\n"
            "}"
            "\n"
            "#btn_out_dir:hover, #btn_img_dir:hover, #btn_nn_activation:hover,"
            "#btn_pred_check:hover, #btn_rectify_match:hover, "
            "#btn_check_match:hover, #btn_length_measurement:hover{\n"
            "  background-color: rgb(0, 203, 221);\n"
            "}\n"
            "\n"
            "#btn_out_dir:pressed, #btn_img_dir:pressed, "
            "#btn_nn_activation:pressed, #btn_pred_check:pressed,"
            "#btn_rectify_match:pressed, #btn_check_match:pressed, "
            "#btn_length_measurement:pressed{\n"
            "    background-color: rgb(0, 160, 174);\n"
            "}")
                
        frame_data.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_data.setObjectName("frame_data")
        
        # layout for main data frame
        self.layout_frame_data = QtWidgets.QGridLayout(frame_data)
        self.layout_frame_data.setObjectName("layout_frame_data")
        self.layout_frame_data.setAlignment(QtCore.Qt.AlignCenter)
        
        # scroll area containing the steps of the data pipeline
        self.scrollArea = self._createScrollArea(frame_data)  

        # add widgets to layout
        self.layout_frame_data.addWidget(self.scrollArea, 0, 0, 1, 1)

        return frame_data    
    
    def _createFrameDataOptions(self, parent):
        """ Created frame that contains all elements to adapt the 
        data selection; parent: scroll area"""
        # frame for data options
        frame_data_options = QtWidgets.QFrame(parent)
        frame_data_options.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_data_options.setObjectName("frame_data_options")
   
        # layout for data options
        self.layout_frame_data_options = QtWidgets.QHBoxLayout(frame_data_options)
        self.layout_frame_data_options.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_data_options.setSpacing(0)
        self.layout_frame_data_options.setObjectName("layout_frame_data_options")
        
        # spacers   
        spacerItem20 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, 
                                             QtWidgets.QSizePolicy.Minimum)
        
        # frame to offer data selection functionalities
        self.frame_data_selection = self._createFrameDataSelection(frame_data_options)
  
        # frame to display information derived from data selection
        self.frame_data_information = self._createFrameDataInformation(frame_data_options)
   
        # add widgets to layout
        self.layout_frame_data_options.addWidget(self.frame_data_selection)
        self.layout_frame_data_options.addItem(spacerItem20)
        self.layout_frame_data_options.addWidget(self.frame_data_information)
        
        return frame_data_options     
    
    def _createFrameProcessArrow(self, parent):
        """ Creates a frame containing a centralized arrow. """
        frame = QtWidgets.QFrame(parent)
        frame.setObjectName(u"frame")
        frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        layout = QtWidgets.QHBoxLayout(frame)
        layout.setSpacing(0)
        layout.setObjectName(u"layout")
        layout.setContentsMargins(0, 0, 0, 0)
        
        hspacer = QtWidgets.QSpacerItem(165, 20, 
                                        QtWidgets.QSizePolicy.Expanding, 
                                        QtWidgets.QSizePolicy.Minimum)
        
        label_arrow = QtWidgets.QLabel(frame)
        label_arrow.setObjectName(u"label_arrow")
        label_arrow.setMaximumSize(QtCore.QSize(40, 70))
        label_arrow.setPixmap(QtGui.QPixmap(":/icons/icons/process_arrow_down.png"))
        label_arrow.setScaledContents(True)
        label_arrow.setAlignment(QtCore.Qt.AlignCenter)

        layout.addItem(hspacer)
        layout.addWidget(label_arrow)
        layout.addItem(hspacer)
        
        return frame
    
    def _createFrameBtnLabelNumber(self, parent, frame_name, btn_name, 
                                   label_text_name, label_nr_name, add_progressBar=False):
        """ Creates a frame with a button, a label and a number. """
        frame = QtWidgets.QFrame(parent)
        frame.setObjectName(frame_name)
        frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        layout = QtWidgets.QHBoxLayout(frame)
        layout.setSpacing(7)
        layout.setObjectName(u"layout")
        layout.setContentsMargins(11, 11, 11, 11)
        
        # button
        btn = QtWidgets.QPushButton(frame)
        btn.setObjectName(btn_name)
        sizePolicy4 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                            QtWidgets.QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(btn.sizePolicy().hasHeightForWidth())
        btn.setSizePolicy(sizePolicy4)
        btn.setMinimumSize(QtCore.QSize(500, 40))

        # label
        label_text = QtWidgets.QLabel(frame)
        label_text.setObjectName(label_text_name)
        
        # label for number
        label_number = QtWidgets.QLabel(frame)
        label_number.setObjectName(label_nr_name)
        
        # add widgets to layout
        layout.addWidget(btn)
        layout.addWidget(label_text)
        layout.addWidget(label_number)
        
        if add_progressBar:
            progress = ProgressBar(parent)
            progress.setMinimumWidth(100)
            layout.addWidget(progress)
            return frame, btn, label_text, label_number, progress
        
        return frame, btn, label_text, label_number
    
    def _createScrollArea(self, frame_data):
        """ Creates scroll area containing the content of the data page. """
        scrollArea = QtWidgets.QScrollArea(frame_data)
        scrollArea.setObjectName(u"scrollArea_data_options")
        scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollArea.setWidgetResizable(True)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1659, 1171))

        self.gridLayout_scrollArea = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_scrollArea.setObjectName(u"gridLayout_scrollArea")
        self.gridLayout_scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        
        # data selection row
        self.label_data_selection = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.frame_data_options = self._createFrameDataOptions(self.scrollAreaWidgetContents)
        frame_process_arrow1 = self._createFrameProcessArrow(self.scrollAreaWidgetContents)

        # neural network activation row
        self.label_nn_activation = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.frame_nn_activation, self.btn_nn_activation, \
        self.label_nn_activation_text, self.label_nn_activation_number, \
        self.progressBar_nn \
        = self._createFrameBtnLabelNumber(self.scrollAreaWidgetContents, 
                                         "frame_nn_activation",
                                          "btn_nn_activation", 
                                          "label_nn_activation", 
                                          "label_nn_activation_number", 
                                          True)
        frame_process_arrow2 = self._createFrameProcessArrow(self.scrollAreaWidgetContents)
        
        # prediction check row
        self.label_prediction_check = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.frame_pred_check, self.btn_pred_check, \
        self.label_pred_check_text, self.label_pred_check_number \
        = self._createFrameBtnLabelNumber(self.scrollAreaWidgetContents, 
                                         "frame_pred_check",
                                          "btn_pred_check", 
                                          "label_pred_check", 
                                          "label_pred_check_number")
        frame_process_arrow3 = self._createFrameProcessArrow(self.scrollAreaWidgetContents)
        
        # rectify and match row
        self.label_rectify_match = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.frame_rectify_match, self.btn_rectify_match, \
        self.label_rectify_match_text, self.label_rectify_match_number, \
        self.progressBar_rectify_match \
        = self._createFrameBtnLabelNumber(self.scrollAreaWidgetContents, 
                                         "frame_rectify_match",
                                          "btn_rectify_match", 
                                          "label_rectify_match", 
                                          "label_rectify_match_number", 
                                          True)
        frame_process_arrow4 = self._createFrameProcessArrow(self.scrollAreaWidgetContents)
        
        # check matching row
        self.label_check_match = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.frame_check_match, self.btn_check_match, \
        self.label_check_match_text, self.label_check_match_number \
        = self._createFrameBtnLabelNumber(self.scrollAreaWidgetContents, 
                                         "frame_check_match", 
                                          "btn_check_match", 
                                          "label_check_match", 
                                          "label_check_match_number")
        frame_process_arrow5 = self._createFrameProcessArrow(self.scrollAreaWidgetContents)
        
        # length measurement row
        self.label_length_measurement = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.frame_length_measurement, self.btn_length_measurement, \
        self.label_length_measurement_text, self.label_length_measurement_number \
        = self._createFrameBtnLabelNumber(self.scrollAreaWidgetContents, 
                                         "frame_length_measurement",
                                          "btn_length_measurement", 
                                          "label_length_measurement", 
                                          "label_length_measurement_number")
        
        # add widgets to layout
        self.gridLayout_scrollArea.addWidget(self.label_data_selection, 0, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.gridLayout_scrollArea.addWidget(self.frame_data_options, 0, 1, 1, 1)
        self.gridLayout_scrollArea.addWidget(frame_process_arrow1, 1, 0, 1, 1)

        self.gridLayout_scrollArea.addWidget(self.label_nn_activation, 2, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.gridLayout_scrollArea.addWidget(self.frame_nn_activation, 2, 1, 1, 1)
        self.gridLayout_scrollArea.addWidget(frame_process_arrow2, 3, 0, 1, 1)
        
        self.gridLayout_scrollArea.addWidget(self.label_prediction_check, 4, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.gridLayout_scrollArea.addWidget(self.frame_pred_check, 4, 1, 1, 1)
        self.gridLayout_scrollArea.addWidget(frame_process_arrow3, 5, 0, 1, 1)
        
        self.gridLayout_scrollArea.addWidget(self.label_rectify_match, 6, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.gridLayout_scrollArea.addWidget(self.frame_rectify_match, 6, 1, 1, 1)
        self.gridLayout_scrollArea.addWidget(frame_process_arrow4, 7, 0, 1, 1)
        
        self.gridLayout_scrollArea.addWidget(self.label_check_match, 8, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.gridLayout_scrollArea.addWidget(self.frame_check_match, 8, 1, 1, 1)
        self.gridLayout_scrollArea.addWidget(frame_process_arrow5, 9, 0, 1, 1)
        
        self.gridLayout_scrollArea.addWidget(self.label_length_measurement, 10, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.gridLayout_scrollArea.addWidget(self.frame_length_measurement, 10, 1, 1, 1)
        
        self.gridLayout_scrollArea.setColumnStretch(1, 5)
        scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        return scrollArea
    
    def _createFrameDataOptions_2(self, frame_data):
        """ Created frame that contains all elements to adapt the 
        data selection """
        # frame for data options
        frame_data_options = QtWidgets.QFrame(frame_data)
        frame_data_options.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_data_options.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_data_options.setObjectName("frame_data_options")
        
        # layout for data options
        self.layout_frame_data_options = QtWidgets.QHBoxLayout(frame_data_options)
        self.layout_frame_data_options.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_data_options.setSpacing(0)
        self.layout_frame_data_options.setObjectName("layout_frame_data_options")
        
        # spacers
        spacerItem17 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)      
        spacerItem20 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        spacerItem22 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        
        # frame to offer data selection functionalities
        self.frame_data_selection = self._createFrameDataSelection(frame_data_options)
  
        # frame to display information derived from data selection
        self.frame_data_information = self._createFrameDataInformation(frame_data_options)
   
        # add widgets to layout
        self.layout_frame_data_options.addItem(spacerItem17)
        self.layout_frame_data_options.addWidget(self.frame_data_selection)
        self.layout_frame_data_options.addItem(spacerItem20)
        self.layout_frame_data_options.addWidget(self.frame_data_information)
        self.layout_frame_data_options.addItem(spacerItem22)
        
        return frame_data_options
    
    def _createFrameDataSelection(self, frame_data_options):   
        """ Creates frame with the main data selection options (calendar and 
        data filter combobox) """
        # data selection frame
        frame_data_selection = QtWidgets.QFrame(frame_data_options)
        frame_data_selection.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_data_selection.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_data_selection.setObjectName("frame_data_selection")
        
        # layout 
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(frame_data_selection)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        
        # calender widget to select a date from 
        self.calendarWidget = QtWidgets.QCalendarWidget(frame_data_selection)
        self.calendarWidget.setStyleSheet(
            "QCalenderWidget{\n"
            "border-radius: 10px;\n"
            "}\n"
            "\n"
            "/* buttons in navigation bar*/\n"
            "QCalendarWidget QToolButton {\n"
            "      color: white;\n"
            "      font: 12pt \"Century Gothic\";\n"
            "      background-color: transparent;    \n"
            "  }\n"
            "\n"
            "/* set icon to go to next month*/\n"
            "QCalendarWidget QToolButton#qt_calendar_nextmonth{\n"
            "    qproperty-icon:url(:/icons/icons/arrow_right_small.png);\n"
            "}\n"
            "\n"
            "/* set icon to go to previous month*/\n"
            "QCalendarWidget QToolButton#qt_calendar_prevmonth{\n"
            "    qproperty-icon:url(:/icons/icons/arrow_left_small.png);\n"
            "}\n"
            "\n"
            "\n"
            "/* menu to select a month */\n"
            "QCalendarWidget QMenu {\n"
            "      color: white;\n"
            "      font: 10pt \"Century Gothic\";\n"
            "      background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
            "                   stop:0 rgb(150, 150, 150), stop:1 rgb(200, 200, 200));\n"
            "      border-radius: 3px;\n"
            "}\n"
            "\n"
            "QCalendarWidget QMenu::item:selected {\n"
            "    background-color: rgb(0, 203, 221);\n"
            "}\n"
            "\n"
            "\n"
            "/* header row */\n"
            "QCalendarWidget QWidget { alternate-background-color: rgb(200, 200, 200); }\n"
            "\n"
            "   \n"
            "/* normal days */\n"
            "QCalendarWidget QAbstractItemView:enabled{\n"
            "      font:10pt \"Century Gothic\";  \n"
            "      color: rgb(100, 100, 100);  \n"
            "      background-color: white; \n"
            "      selection-background-color: rgb(0, 203, 221);\n"
            "      selection-color: white;\n"
            "}\n"
            "   \n"
            "  \n"
            "/* navigation bar */\n"
            "QCalendarWidget QWidget#qt_calendar_navigationbar{ \n"
            "    background-color:rgb(150, 150, 150);\n"
            "}\n"
            "\n"
            "/* days in other months */\n"
            "QCalendarWidget QAbstractItemView:disabled { \n"
            "    color:rgb(180,180,180);\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "/*--- spin box to select a year -----------------------------*/\n"
            "\n"
            "QCalendarWidget QSpinBox {\n"
            "    padding-right: 15px; /* make room for the arrows */\n"
            "    /*border-image: url(:/images/frame.png) 4;*/\n"
            "    border-radius: 3px;\n"
            "    selection-background-color:rgb(0, 203, 221);\n"
            "    font:12pt \"Century Gothic\";\n"
            "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, "
            "                stop:0 rgb(150, 150, 150), stop:1 rgb(200, 200, 200));\n"
            "}\n"
            "\n"
            "QCalendarWidget QSpinBox::up-button {\n"
            "    subcontrol-origin: border;\n"
            "    subcontrol-position: top right; /* position at the top right corner */\n"
            "\n"
            "    width: 16px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */\n"
            "    border-image: url(:/icons/icons/arrow_up.png) 1;\n"
            "    border-width: 1px;\n"
            "    margin:2px;\n"
            "}\n"
            "\n"
            "QCalendarWidget QSpinBox::up-button:hover {\n"
            "    border-image: url(:/icons/icons/arrow_up_blue.png) 1;\n"
            "}\n"
            "\n"
            "QCalendarWidget QSpinBox::up-button:pressed {\n"
            "    border-image: url(:/icons/icons/arrow_up_darkblue.png) 1;\n"
            "}\n"
            "\n"
            "QCalendarWidget QSpinBox::down-button {\n"
            "    subcontrol-origin: border;\n"
            "    subcontrol-position: bottom right;\n"
            "\n"
            "    width: 16px;\n"
            "    border-image: url(:/icons/icons/arrow_down.png) 1;\n"
            "    border-width: 1px;\n"
            "    border-top-width: 0;\n"
            "    margin:2px;\n"
            "}\n"
            "\n"
            "QCalendarWidget QSpinBox::down-button:hover {\n"
            "    border-image: url(:/icons/icons/arrow_down_blue.png) 1;\n"
            "}\n"
            "\n"
            "QCalendarWidget QSpinBox::down-button:pressed {\n"
            "    border-image:url(:/icons/icons/arrow_down_darkblue.png) 1;\n"
            "}\n"
            "")
        
        # adapt calendar widget settings
        self.calendarWidget.setLocale(QtCore.QLocale(
            QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setHorizontalHeaderFormat(
            QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(
            QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName("calendarWidget")        

        # --- frame to display the current date ----------------------------- #
        self.frame_date = QtWidgets.QFrame(frame_data_selection)
        self.frame_date.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_date.setMaximumSize(QtCore.QSize(16777214, 40))
        self.frame_date.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_date.setObjectName("frame_date")
        
        # layout for date frame
        self.layout_frame_date = QtWidgets.QHBoxLayout(self.frame_date)
        self.layout_frame_date.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_date.setObjectName("layout_frame_date")
        
        # label displaying "date"
        self.label_date_text = QtWidgets.QLabel(self.frame_date)
        #self.label_date_text.setStyleSheet("")
        self.label_date_text.setObjectName("label_date_text")
        
        # spacer
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
        
        # label displaying the date selected in the calendar
        self.label_date = QtWidgets.QLabel(self.frame_date)
        self.label_date.setObjectName("label_date")
        
        # add widgets to layout
        self.layout_frame_date.addWidget(self.label_date_text)
        self.layout_frame_date.addItem(spacerItem18)
        self.layout_frame_date.addWidget(self.label_date)
        
        
        # --- frame to display data filter options ----------------------------- #
        self.frame_img_filter = QtWidgets.QFrame(frame_data_selection)
        self.frame_img_filter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_img_filter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_img_filter.setObjectName("frame_img_filter")
        
        # layout
        self.layout_data_filter = QtWidgets.QHBoxLayout(self.frame_img_filter)
        self.layout_data_filter.setContentsMargins(0, 0, 0, 0)
        self.layout_data_filter.setObjectName("layout_data_filter")
        
        # label to display the text "data filter"
        self.label_image_filter = QtWidgets.QLabel(self.frame_img_filter)
        #self.label_image_filter.setStyleSheet("")
        self.label_image_filter.setObjectName("label_image_filter")
                
        # spacer
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, 
                                             QtWidgets.QSizePolicy.Expanding, 
                                             QtWidgets.QSizePolicy.Minimum)
        
        # combo box to select a data filter
        self.comboBox_image_filter = QtWidgets.QComboBox(self.frame_img_filter)
        self.comboBox_image_filter.setMinimumSize(QtCore.QSize(250, 40))
        self.comboBox_image_filter.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_image_filter.setObjectName("comboBox_image_filter")
        self.comboBox_image_filter.addItem("")
        self.comboBox_image_filter.addItem("")
        self.comboBox_image_filter.addItem("")
        self.comboBox_image_filter.setEnabled(False)
        
        # add widgets to data filter frame
        self.layout_data_filter.addWidget(self.label_image_filter)
        self.layout_data_filter.addItem(spacerItem19)
        self.layout_data_filter.addWidget(self.comboBox_image_filter)
        
        
        # --- add widgets to data selection frame -------------------------- #
        self.verticalLayout_7.addWidget(self.calendarWidget)
        self.verticalLayout_7.addWidget(self.frame_date)        
        self.verticalLayout_7.addWidget(self.frame_img_filter)
        
        return frame_data_selection
        
    def _createFrameDataInformation(self, frame_data_options):
        """ Creates frame that shows image directory, result file path, 
        image prefix and experiment ID """
        # frame for data information
        frame_data_information = QtWidgets.QFrame(frame_data_options)
        frame_data_information.setEnabled(False)
        frame_data_information.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_data_information.setObjectName("frame_data_information")
        
        # layout
        self.gridLayout_5 = QtWidgets.QGridLayout(frame_data_information)
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        # line edit for the result file path
        self.lineEdit_output_dir = QtWidgets.QLineEdit(frame_data_information)
        self.lineEdit_output_dir.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_output_dir.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_output_dir.setObjectName("lineEdit_output_dir")
        
        # label to display text "number of images"
        self.label_num_imgs = QtWidgets.QLabel(frame_data_information)
        self.label_num_imgs.setObjectName("label_num_imgs")
        self.label_num_imgs.setMinimumSize(QtCore.QSize(0, 40))
        self.label_num_imgs.setMaximumSize(QtCore.QSize(16777215, 40))
        
        # line edit for the image directory path
        self.lineEdit_img_dir = QtWidgets.QLineEdit(frame_data_information)
        self.lineEdit_img_dir.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_img_dir.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_img_dir.setObjectName("lineEdit_img_dir")
                
        # button to browse for image directories
        self.btn_img_dir = QtWidgets.QPushButton(frame_data_information)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btn_img_dir.sizePolicy().hasHeightForWidth())
        self.btn_img_dir.setSizePolicy(sizePolicy)
        self.btn_img_dir.setMinimumSize(QtCore.QSize(90, 40))
        self.btn_img_dir.setMaximumSize(QtCore.QSize(90, 40))
        self.btn_img_dir.setObjectName("btn_img_dir")
        
        # label to display text "experiment id"
        self.label_exp_id = QtWidgets.QLabel(frame_data_information)
        self.label_exp_id.setObjectName("label_exp_id")

        # label to display text "image directory"
        self.label_img_dir = QtWidgets.QLabel(frame_data_information)
        self.label_img_dir.setObjectName("label_img_dir")

        # line edit to set the image prefix
        self.lineEdit_img_prefix = QtWidgets.QLineEdit(frame_data_information)
        self.lineEdit_img_prefix.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_img_prefix.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_img_prefix.setObjectName("lineEdit_img_prefix")
        
        # label to display the text "result file"
        self.label_out_dir = QtWidgets.QLabel(frame_data_information)
        self.label_out_dir.setObjectName("label_out_dir")
        
        # label to display the number of images in the current directory
        self.label_num_imgs_text = QtWidgets.QLabel(frame_data_information)
        self.label_num_imgs_text.setStyleSheet("padding-left: 10px;")
        self.label_num_imgs_text.setAlignment(
            QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_num_imgs_text.setObjectName("label_num_imgs_text")
                
        # button to browse files for a result file
        self.btn_out_dir = QtWidgets.QPushButton(frame_data_information)
        self.btn_out_dir.setMinimumSize(QtCore.QSize(90, 40))
        self.btn_out_dir.setMaximumSize(QtCore.QSize(90, 40))
        self.btn_out_dir.setObjectName("btn_out_dir")
        
        # line edit for the experiment id
        self.lineEdit_exp_id = QtWidgets.QLineEdit(frame_data_information)
        self.lineEdit_exp_id.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_exp_id.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_exp_id.setObjectName("lineEdit_exp_id")
        
        # label to display text "image prefix"
        self.label_img_prefix = QtWidgets.QLabel(frame_data_information)
        self.label_img_prefix.setObjectName("label_img_prefix")
        
        # --- add widgets to data information frame ------------------------ #
        self.gridLayout_5.addWidget(self.lineEdit_output_dir, 2, 1, 1, 1)
        self.gridLayout_5.addWidget(self.label_num_imgs, 5, 0, 1, 1)
        self.gridLayout_5.addWidget(self.lineEdit_img_dir, 1, 1, 1, 1)
        self.gridLayout_5.addWidget(self.btn_img_dir, 1, 2, 1, 1)
        self.gridLayout_5.addWidget(self.label_exp_id, 4, 0, 1, 1)
        self.gridLayout_5.addWidget(self.label_img_dir, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.lineEdit_img_prefix, 3, 1, 1, 1)
        self.gridLayout_5.addWidget(self.label_out_dir, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.label_num_imgs_text, 5, 1, 1, 1)
        self.gridLayout_5.addWidget(self.btn_out_dir, 2, 2, 1, 1)
        self.gridLayout_5.addWidget(self.lineEdit_exp_id, 4, 1, 1, 1)
        self.gridLayout_5.addWidget(self.label_img_prefix, 3, 0, 1, 1)
        
        return frame_data_information
    
    def onNnFinished(self):
        """ Called when the predictions are done. Enables the data page and 
        updates data table. """
        self.setEnabled(True)
        
        # get prediction parameters
        df = self.predicter.df
        
        print(df)
        
        # insert data into data model
        row = len(self.models.model_animals.data)
        count = len(df)

        #for path in image_pathes:
        # insert data into model
        self.models.model_animals.insertDfRows(row=row, 
                                               count=count, 
                                               df=df)

        print("PageData: New data inserted into model")

    def onNnProgress(self, i):
        """ Called to report on the prediction progress. Updates the label
        displaying the number of predicted images and the progress bar. """
        # update label displaying number of predicted images
        self.label_nn_activation_number.setText(str(i))
        
        # update progress bar
        img_list = self.parent().parent().page_home.photo_viewer.image_list
        num_images = len(img_list[0])
        self.progressBar_nn.setValue(i/num_images*100)
    
    def areInputOutputDirsValid(self): 
        """ Checks if there is a valid image input directory and output directory. """
        # check if there is a valid input image directory
        if not os.path.isdir(self.lineEdit_img_dir.text()):
            text = "Error: Invalid image directory"
            information = "Please specify a valid image directory beside the calendar on the data page."
            windowTitle = "Invalid image directory"
            displayErrorMsg(text, information, windowTitle)
            return False
        
        # check if there is a valid output directory
        if not os.path.isdir(self.lineEdit_output_dir.text()):
            text = "Error: Missing output directory"
            information = "Please specify the output directory beside the calendar on the data page."
            windowTitle = "Missing output directory"
            displayErrorMsg(text, information, windowTitle)
            return False
        
        return True
        
    def onNnActivated(self):
        """
        Handles the activation of the "run neural network" button.
        It gets the current image list from the photo viewer that it applies 
        the neural network to (in a separate thread). It appends the new data 
        to the data model.
        """       
        # check for input and output directories
        if not self.areInputOutputDirsValid(): return
        
        # check if there is a neural netowk
        if self.predicter.neural_network is None:
            displayErrorMsg(
                "Missing Neural Network", 
                "Please specify a neural network on settings page.", 
                "Error")
            return
        
        if self.predicter is not None:
            # reset progress bar and label
            self.progressBar_nn.setValue(0)
            self.label_nn_activation_number.setText(str(0))
            
            # get image path list from photo viewer
            img_list = self.parent().parent().page_home.photo_viewer.image_list.copy()
            
            # determine file IDs
            file_ids = []
            for path in img_list[0]:
                file_ids.append(os.path.basename(path).rstrip(".jpg").rstrip(".png").rstrip("_L"))
                
            # get experiment and user ID
            exp_id = self.lineEdit_exp_id.text()
            user_id = self.frame_topBar.label_user_id.text()
            
            # create a QThread and worker object
            self.thread = QtCore.QThread()
            self.worker = PredictionWorker(self.predicter, img_list[0], file_ids, exp_id, user_id)
            
            # move worker to the thread
            self.worker.moveToThread(self.thread)
            
            # connect signals and slots from thread to worker and vice versa
            self.thread.started.connect(self.worker.predictImageList)
            self.thread.finished.connect(self.thread.deleteLater)
            
            self.worker.finished.connect(self.onNnFinished)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)    
            self.worker.progress.connect(self.onNnProgress)
        
            # start prediction       
            self.setEnabled(False)
            self.thread.start()
  
    def onCheckPredictions(self):
        """ Handles the click on 'Check predictions on home screen' button by
        navigating to the home screen. """ 
        # navigate to home screen
        self.parent().parent().directToHomePage()
        self.parent().parent().page_home.displayLeftImage()
    
    def onRectifyMatch(self):
        """
        Gets current image list from photo viewer, rectifies them and
        determines the positions of the respective animal on the right image
        using block matching. 
        """
        # check for input and output directories
        if not self.areInputOutputDirsValid(): return
        
        # reset progress bar and label
        self.progressBar_rectify_match.setValue(0)
        self.label_rectify_match_number.setText(str(0))
        
        # get list of images to process (images of the current day)            
        img_list = self.parent().parent().page_home.photo_viewer.image_list.copy()
        
        # create thread and worker
        self.thread = QtCore.QThread()
        self.worker = pp.RectifyMatchWorker(self.matcher, self.models, 
                                            img_list, self.camera_config)    
        
        # move worker to the thread
        self.worker.moveToThread(self.thread)
            
        # connect signals and slots from thread to worker and vice versa
        self.thread.started.connect(self.worker.rectifyMatch)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.worker.finished.connect(self.onRectifyMatchFinished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)    
        self.worker.progress.connect(self.onRectifyMatchProgress)
    
        # start prediction       
        self.setEnabled(False)
        self.thread.start()
            
    def onRectifyMatchProgress(self, i):   
        """ Called to report on the rectification and matching progress. 
        Updates the label displaying the number of rectified and matched 
        images and the progress bar. """
        # update label displaying number of predicted images
        self.label_rectify_match_number.setText(str(i))
        
        # update progress bar
        img_list = self.parent().parent().page_home.photo_viewer.image_list
        num_images = len(img_list[0])
        self.progressBar_rectify_match.setValue(i/num_images*100)
            
    def onRectifyMatchFinished(self): 
        """ Called when the rectification and matching calculations are done.
        Enables the data page and triggers length calculations. """
        self.setEnabled(True)

        # now we need to create new right animal instances
        # for this, we iterate over images
        for j in range(len(self.matcher.merged_objects)):
            merged_objects = self.matcher.merged_objects[j] # all new animals 
            cur_entries = self.matcher.cur_entries[j] # their row index in the data table
            
            # add right coordinates to data model
            for i in range(len(cur_entries)):
                idx = cur_entries[i]
                
                # only continue if the animal is matched
                if merged_objects != [] and merged_objects[i] != []:
                    # the matcher returns rectified coordinates,
                    # they have to be calculated back and just then add them to data model 
                    head = self.matcher.distortPoint([merged_objects[i][6], merged_objects[i][5]], "R")
                    tail = self.matcher.distortPoint([merged_objects[i][8], merged_objects[i][7]], "R")
                    
                    if (np.array(head) < 0).any() or (np.array(tail) < 0).any():
                        head = [-1,-1]
                        tail = [-1,-1]
                        
                    # update data model
                    self.models.model_animals.data.loc[idx, "RX1"] = head[1]
                    self.models.model_animals.data.loc[idx, "RY1"] = head[0]
                    self.models.model_animals.data.loc[idx, "RX2"] = tail[1]
                    self.models.model_animals.data.loc[idx, "RY2"] = tail[0] 
                    
                    # create a new right animal instance
                    animal_remark = str(self.models.model_animals.data.loc[idx, "object_remarks"] )
                    if not animal_remark: animal_remark = ""       
            
                    length = float(self.models.model_animals.data.loc[idx, "length"])
                    print(f"idx: {idx}")
                    animal = Animal(self.models,
                             row_index=idx,
                             position_head=QtCore.QPointF(head[1], head[0]), 
                             position_tail=QtCore.QPointF(tail[1], tail[0]),
                             group=str(self.models.model_animals.data.loc[idx, "group"]),
                             species=str(self.models.model_animals.data.loc[idx, "species"]),
                             remark=animal_remark,
                             length=length)
                    
                    # append animal instance to list of viewers showing right images
                    if self.parent().parent().page_home.photo_viewer.imageArea.animal_painter.image_ending == "*_R.jpg":
                        self.parent().parent().page_home.photo_viewer.imageArea.animal_painter.animal_list.append(animal)  
                        
                    self.parent().parent().page_home.photo_viewer.imageAreaLR.imageAreaR.animal_painter.animal_list.append(animal)  

        # update length calculations
        self.onCalcLength()
    
    def onCheckMatch(self):
        """ 
        Directs to LR screen (showing left and right images) if  at least one
        match is already calculated. 
        """
        # navigate to LR screen
        self.parent().parent().directToHomePage()
        self.parent().parent().page_home.displayBothImages()
    
    def onCalcLength(self):
        """ Gets current image list from photo viewer and calculates the 
        length of animals whose coordinates are valid. """
        
        # @todo check if the coordinate rectification is correct
        print("calc length")
        
        # reset label
        self.label_length_measurement_number.setText(str(0))
        
        # get list of images to process (images of the current day)      
        if self.parent().parent() is None: return
        img_list = self.parent().parent().page_home.photo_viewer.image_list.copy()
                
        # iterate over images and measure length
        if len(img_list) == 0: return
        for path in img_list[0]:                
            # get animals on current image
            file_id = os.path.basename(path).rstrip(".jpg").rstrip(".png").rstrip("_L").rstrip("_R")
            cur_entries = self.models.model_animals.data[self.models.model_animals.data["file_id"] == file_id]
            
            # iterate over animals
            for i in range(len(cur_entries)):
                
                # measure length only if there are valid coordinates for right image and left image
                if cur_entries.iloc[i]["RX1"] > 0 and cur_entries.iloc[i]["RY1"] > 0 \
                and cur_entries.iloc[i]["RX2"] > 0 and cur_entries.iloc[i]["RY2"] > 0 \
                and cur_entries.iloc[i]["LX1"] > 0 and cur_entries.iloc[i]["LY1"] > 0 \
                and cur_entries.iloc[i]["LX2"] > 0 and cur_entries.iloc[i]["LY2"] > 0:

                    # make sure that the entries have the right format (i.e. np float arrays)
                    head_L_entry = np.array([cur_entries.iloc[i]["LX1"], cur_entries.iloc[i]["LY1"]]).astype(np.float64)
                    tail_L_entry = np.array([cur_entries.iloc[i]["LX2"], cur_entries.iloc[i]["LY2"]]).astype(np.float64)
                    head_R_entry = np.array([cur_entries.iloc[i]["RX1"], cur_entries.iloc[i]["RY1"]]).astype(np.float64)
                    tail_R_entry = np.array([cur_entries.iloc[i]["RX2"], cur_entries.iloc[i]["RY2"]]).astype(np.float64)
                                        
                    # undistort points (i.e. rectify)
                    head_L = self.matcher.undistortPoint(head_L_entry, "L")
                    tail_L = self.matcher.undistortPoint(tail_L_entry, "L")
                    head_R = self.matcher.undistortPoint(head_R_entry, "R")
                    tail_R = self.matcher.undistortPoint(tail_R_entry, "R")    
                    
                    # calculate animal length by triangulation        
                    distances = self.distance_measurer.distances(head_L, tail_L, 
                                                                 head_R, tail_R)

                    # add length measurements to model
                    idx = cur_entries.index[i]
                    self.models.model_animals.data.loc[idx, "length"] = distances[0]
                    
                    # update animal length
                    for animal in self.parent().parent().page_home.photo_viewer.imageArea.animal_painter.animal_list:
                        if animal.row_index == idx:
                            print(f"length {distances[0]} set on animal")
                            animal.setLength(distances[0])

                    for animal in self.parent().parent().page_home.photo_viewer.imageAreaLR.imageAreaL.animal_painter.animal_list:
                        if animal.row_index == idx:
                            print(f"length {distances[0]} set on animal")
                            animal.setLength(distances[0])
                    
                    for animal in self.parent().parent().page_home.photo_viewer.imageAreaLR.imageAreaR.animal_painter.animal_list:
                        if animal.row_index == idx:
                            print(f"length {distances[0]} set on animal")
                            animal.setLength(distances[0])
                            
            # update label displaying number of rectified and matched images
            num_imgs = int(self.label_length_measurement_number.text()) + 1
            self.label_length_measurement_number.setText(str(num_imgs))
            
        return 

# --- functions for saving and restoring options --------------------------- # 
    def saveCurrentValues(self, settings):     
        """ Saves current settings on data page for next program start """
        settings.setValue("date", self.calendarWidget.selectedDate())       
        settings.setValue("dataFilter", self.comboBox_image_filter.currentIndex())
        settings.setValue("imgDir", self.lineEdit_img_dir.text())       
        settings.setValue("outDir", self.lineEdit_output_dir.text())
        settings.setValue("imgPrefix", self.lineEdit_img_prefix.text())
        settings.setValue("experimentId", self.lineEdit_exp_id.text())
        
    def restoreValues(self, settings):
        """ Restores settings of page data from last program start """
        self.calendarWidget.setSelectedDate(settings.value("date"))
        self.comboBox_image_filter.setCurrentIndex(settings.value("dataFilter"))
        self.lineEdit_img_dir.setText(settings.value("imgDir"))
        self.lineEdit_output_dir.setText(settings.value("outDir"))
        self.lineEdit_img_prefix.setText(settings.value("imgPrefix"))
        self.lineEdit_exp_id.setText(settings.value("experimentId"))
        
        # do not update the visuals when setting the image directory, 
        # that would override the restored settings of the other fields
        self.onImageDirEditChanged(updateVisuals=False)
        self.onOutDirChanged()
        self.onPrefixEditChanged()
        self.onExpIdEditChanged()
        
# --- initialization -------------------------------------------------------- # 
    def _initUi(self):
        """ Initializes the UI of data page """
        self.setObjectName("page_data")

        # main layout
        self.layout_page_data = QtWidgets.QVBoxLayout(self)
        self.layout_page_data.setContentsMargins(0, 0, 0, 0)
        self.layout_page_data.setSpacing(0)
        self.layout_page_data.setObjectName("layout_page_data")
        
        # create the blue top bar
        self.frame_topBar = TopFrame(":/icons/icons/data_w.png", 
                                     "frame_dataBar", self)     
               
        # create the cotrol bar containing the menu
        self.frame_controlBar = MenuFrame("Data", 
                                          "frame_controlBar_data", self)  
   
        # create the main frame for the data
        self.frame_data = self._createFrameData()
        
        # add widgets to data page
        self.layout_page_data.addWidget(self.frame_topBar)
        self.layout_page_data.addWidget(self.frame_controlBar)
        self.layout_page_data.addWidget(self.frame_data)

    def _initActions(self):
        """ Function to initialize the actions on data page """
        self.calendarWidget.selectionChanged.connect(self.onCalenderSelectionChanged)
        
        self.btn_img_dir.clicked.connect(self.onBrowseImageDir)
        self.btn_out_dir.clicked.connect(self.onBrowseOutDir)
        self.btn_nn_activation.clicked.connect(self.onNnActivated)
        self.btn_pred_check.clicked.connect(self.onCheckPredictions)
        self.btn_rectify_match.clicked.connect(self.onRectifyMatch)
        self.btn_check_match.clicked.connect(self.onCheckMatch)
        self.btn_length_measurement.clicked.connect(self.onCalcLength)
        
        self.lineEdit_img_dir.editingFinished.connect(self.onImageDirEditChanged)
        self.lineEdit_output_dir.editingFinished.connect(self.onOutDirChanged)
        self.lineEdit_img_prefix.editingFinished.connect(self.onPrefixEditChanged)
        self.lineEdit_exp_id.editingFinished.connect(self.onExpIdEditChanged)