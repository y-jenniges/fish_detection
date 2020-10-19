import os
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import Helpers


class WelcomeWindow(QtWidgets.QMainWindow):
    """
    MainWindow class that displays the welcome screen and some initially 
    required settings (user ID, camera configuration path).
    """
    
    def __init__(self, mainWindow, parent=None):
        """
        Init function. Initalizes the GUI and actions for this window.

        Parameters
        ----------
        mainWindow : QMainWindow
            The main window that is enabled as soon as the welcome window
            is edited.
        parent : optional
            The default is None.
        """
        QtWidgets.QMainWindow.__init__(self)
        
        self.main_window = mainWindow
         
        self._initUi()
        self._initActions()
        
    def _initUi(self):  
        """ Init the UI. """
        self.setObjectName("WelcomeWindow")
        self.setWindowIcon(QtGui.QIcon(':/icons/icons/fish.png')) 
        self.resize(797, 502)
        self.setStyleSheet(
            "/* --- Buttons --------------------------------------------- */\n"
            "QPushButton{\n"
            "	background-color: rgb(150, 150, 150);\n"
            "    outline:none;\n"
            "    border: none; \n"
            "    border-width: 0px;\n"
            "    border-radius: 3px;\n"
            "	color: black;\n"
            "	font: 10pt \"Century Gothic\";\n"
            "}\n"
            "QPushButton:hover{\n"
            "	background-color: rgb(0, 203, 221);\n"
            "}\n"
            "QPushButton:pressed{\n"
            "	background-color: rgb(0, 160, 174);\n"
            "}\n"
            "/* --- Labels ---------------------------------------------- */\n"
            "QLabel{\n"
            "	color: black;\n"
            "	font: 12pt \"Century Gothic\";\n"
            "}\n"
            "/* --- Line edits------------------------------------------- */\n"
            "QLineEdit{\n"
            "	background-color:white;\n"
            "	border-radius: 3px;\n"
            "	color: black;\n"
            "	font: 10pt \"Century Gothic\";\n"
            "	selection-background-color:rgb(0, 203, 221);\n"
            "	selection-color:white;\n"
            "	padding-left: 10px;\n"
            "}")
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # label to welcome the user
        self.label_hello = QtWidgets.QLabel(self.centralwidget)
        self.label_hello.setObjectName(u"label_hello")
        self.label_hello.setStyleSheet(u"font: 24pt")
        self.label_hello.setScaledContents(False)
        self.label_hello.setWordWrap(True)

        # label to request filling in information
        self.label_fill_in = QtWidgets.QLabel(self.centralwidget)
        self.label_fill_in.setObjectName(u"label_fill_in")

        # label to request entering the user ID
        self.label_enter_id = QtWidgets.QLabel(self.centralwidget)
        self.label_enter_id.setObjectName(u"label_enter_id")

        # line edit to enter user ID
        self.lineEdit_user_id = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_user_id.setObjectName(u"lineEdit_user_id")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, 
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEdit_user_id.sizePolicy().hasHeightForWidth())
        self.lineEdit_user_id.setSizePolicy(sizePolicy)
        self.lineEdit_user_id.setMinimumSize(QtCore.QSize(200, 40))
        self.lineEdit_user_id.setMaximumSize(QtCore.QSize(200, 40))
        self.lineEdit_user_id.setMaxLength(3)
        self.lineEdit_user_id.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_user_id.setCursorPosition(0)
        self.lineEdit_user_id.setReadOnly(False)
        self.lineEdit_user_id.setObjectName("lineEdit_user_id")

        # set a validator to ensure that the user ID consists of up to three 
        # letters (at least one letter)
        reg_ex = QtCore.QRegExp("[a-zA-Z]{1,3}")
        input_validator = QtGui.QRegExpValidator(reg_ex, self.lineEdit_user_id)
        self.lineEdit_user_id.setValidator(input_validator)
        
        # label to request to choose a camera configuration file
        self.label_choose_config = QtWidgets.QLabel(self.centralwidget)
        self.label_choose_config.setObjectName(u"label_choose_config")

        # frame containing the config line edit and browse button
        self.frame_cam_config = QtWidgets.QFrame(self.centralwidget)
        self.frame_cam_config.setObjectName(u"frame_cam_config")
        self.frame_cam_config.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_cam_config)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_config = QtWidgets.QLineEdit(self.frame_cam_config)
        self.lineEdit_config.setObjectName(u"lineEdit_config")
        self.lineEdit_config.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_config.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_config.setReadOnly(True)

        # button to browse for a camera config file
        self.btn_browse_config = QtWidgets.QPushButton(self.frame_cam_config)
        self.btn_browse_config.setObjectName(u"btn_browse_config")
        self.btn_browse_config.setMinimumSize(QtCore.QSize(80, 40))
        self.btn_browse_config.setMaximumSize(QtCore.QSize(80, 40))

        self.horizontalLayout_2.addWidget(self.lineEdit_config)
        self.horizontalLayout_2.addWidget(self.btn_browse_config)

        # frame containing a spacer and the ok-button
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QtWidgets.QSpacerItem(
            685, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
   
        # confirmation button
        self.btn_ok = QtWidgets.QPushButton(self.frame)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setMinimumSize(QtCore.QSize(80, 40))
        self.btn_ok.setMaximumSize(QtCore.QSize(80, 40))

        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.horizontalLayout.addWidget(self.btn_ok)

        # add widgets to main layout
        self.verticalLayout.addWidget(self.label_hello)
        self.verticalLayout.addWidget(self.label_fill_in)
        self.verticalLayout.addWidget(self.label_enter_id)
        self.verticalLayout.addWidget(self.lineEdit_user_id)
        self.verticalLayout.addWidget(self.label_choose_config)
        self.verticalLayout.addWidget(self.frame_cam_config)
        self.verticalLayout.addWidget(self.frame)

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        """ Retranslates UI. """
        self.setWindowTitle(QtCore.QCoreApplication.translate("WelcomeWindow", u"Welcome", None))
        self.label_hello.setText(QtCore.QCoreApplication.translate("WelcomeWindow", u"Hello and welcome to MarOMarker (Marine Organism Marker).\n"
"", None))
        self.label_fill_in.setText(QtCore.QCoreApplication.translate("WelcomeWindow", u"Please fill in the following fields. You can change them later in \u201cSettings\u201d.", None))
        self.label_enter_id.setText(QtCore.QCoreApplication.translate("WelcomeWindow", u"Enter your personal ID.", None))
        self.lineEdit_user_id.setPlaceholderText(QtCore.QCoreApplication.translate("WelcomeWindow", u"User ID...", None))
        self.lineEdit_user_id.setToolTip(QtCore.QCoreApplication.translate("WelcomeWindow",u"User ID = first letter of first name + first letter of last name", None))
        
        self.label_choose_config.setText(QtCore.QCoreApplication.translate("WelcomeWindow", u"Choose a camera configuration file.", None))
        self.lineEdit_config.setText("")
        self.lineEdit_config.setPlaceholderText(QtCore.QCoreApplication.translate("WelcomeWindow", u"Path to camera configuration file...", None))
        self.lineEdit_config.setToolTip(QtCore.QCoreApplication.translate("WelcomeWindow", u"Path to camera configuration file", None))
        
        self.btn_browse_config.setText(QtCore.QCoreApplication.translate("WelcomeWindow", u"Browse", None))
        self.btn_ok.setText(QtCore.QCoreApplication.translate("WelcomeWindow", u"OK", None))
           
    def onUserIdChanged(self, text):
        """ Handles when user ID is changed. It adaptes the user ID on 
        settings page. """
        # set user ID on settings page
        self.main_window.page_settings.lineEdit_user_id.setText(text)
    
    def onBrowseConfig(self):
        """ Opens a file explorer to browse for a camera configuration file
        and adapts the config path on settings page accordingly. """
        if self.main_window is not None:
            filename = QtWidgets.QFileDialog.getOpenFileName(filter = "*.csv")
            path = filename[0]
            
            # check if path is valid
            if path != "" and os.path.isfile(path): 
                df = pd.read_csv(path)
            
                # check format of file
                if(self.main_window.page_settings.check_config_format(df)):
                    self.lineEdit_config.setText(path)
                    self.main_window.page_settings.apply_configFile(path)
                    
    def onOk(self):
        """ Handles clicking on the confirmation button: It closes the current
        window (if a user ID and config path are entered) and enables the
        main window. """
        # check if user ID is entered
        if self.lineEdit_user_id.text() != "":
            # check if config file is selected
            if self.lineEdit_config.text() != "" and os.path.isfile(
                    self.lineEdit_config.text()):
                # close welcome window
                self.close()
                
                # enable main window
                self.main_window.setEnabled(True)
            else:
                Helpers.displayErrorMsg(
                    "Invalid Camera Configuration", 
                    "Please specify a valid camera configuration file.", 
                    "Error")
        
        else:
            Helpers.displayErrorMsg(
                "No User ID", 
                "Please specify a user ID first (first letter of first name +"
                " first letter of last name).", 
                "Error")
        
    def _initActions(self):
        """ Init actions for the window. """
        self.btn_browse_config.clicked.connect(self.onBrowseConfig)
        self.btn_ok.clicked.connect(self.onOk)
        
        self.lineEdit_user_id.textChanged.connect(self.onUserIdChanged)
        self.lineEdit_user_id.returnPressed.connect(lambda: self.focusNextChild())