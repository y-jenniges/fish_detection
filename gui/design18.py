# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yjenn\Documents\Uni\UniBremen\Semester4\MA\Coding\fish_detection\gui\design18.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from TabWidget import TabWidget
import page_settings
import PageAbout
import Helpers 

import pandas as pd
import numpy as np

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):  
        # create icon loader
        self.icon_loader = Helpers.IconLoader()
        
        # set up main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1244, 822)
        MainWindow.setWindowIcon(QtGui.QIcon(':/icons/icons/fish.png'))
        
        # create a size policy for the main window
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        
        # add user icon to button 
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setProperty("btn_user", icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("#frame_controlBar{background-color:rgb(200, 200, 200); }\n"
"#frame_controlBar_2{background-color:rgb(200, 200, 200); }\n"
"#frame_controlBar_3{background-color:rgb(200, 200, 200); }\n"
"#frame_controlBar_4{background-color:rgb(200, 200, 200); }\n"
"#frame_controlBar_about{background-color:rgb(200, 200, 200); }\n"
"\n"
"QPushButton{\n"
"background-color:transparent;\n"
"outline:none;\n"
"border: none; \n"
"border-width: 0px;\n"
"border-radius: 3px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  background-color: rgb(0, 203, 221);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgb(0, 160, 174);\n"
"}\n"
"\n"
"/*\n"
"#btn_menu{\n"
"background-color:transparent;\n"
"outline:none;\n"
"border: none; \n"
"}\n"
"#btn_menu:hover {\n"
"     background-color: rgb(0, 203, 221);\n"
"}\n"
"\n"
"#btn_menu:pressed {\n"
"background-color: rgb(0, 160, 174);\n"
"}\n"
"*/\n"
"\n"
"#btn_imgSwitch{\n"
"    font: bold 14pt \"Century Gothic\";\n"
"    color:black;\n"
"    border-radius: 3px;\n"
"    border: none; \n"
"    background-color:rgb(150, 150, 150);\n"
"    outline:none;\n"
"}\n"
"\n"
"#btn_imgSwitch:hover{\n"
"background-color: rgb(0, 203, 221);\n"
"}\n"
"#btn_imgSwitch:pressed{\n"
"background-color:  rgb(0, 160, 174);\n"
"}\n"
"\n"
"\n"
"#btn_user:hover,\n"
"#btn_user_data:hover,\n"
"#btn_user_settings:hover,\n"
"#btn_user_handbook:hover,\n"
"#btn_user_about:hover{\n"
"background-color:  rgb(0, 160, 174);\n"
"}\n"
"\n"
"#btn_user:pressed, \n"
"#btn_user_data:pressed, \n"
"#btn_user_settings:pressed,\n"
"#btn_user_handbook:pressed,\n"
"#btn_user_about:pressed{\n"
"background-color: rgb(0,100,108);\n"
"\n"
"}\n"
"\n"
"\n"
"/*\n"
"#comboBox_menu{\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 10px;\n"
"    background-color:white;\n"
"    border:none;\n"
"}\n"
"*/\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: none;\n"
"    selection-background-color: rgb(0, 203, 221);\n"
"    background-color:white;\n"
"}\n"
"\n"
"\n"
"QComboBox {\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 10px;\n"
"    background-color:white;\n"
"    border:none;\n"
"    font: 12pt \"Century Gothic\";\n"
"}\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 rgb(200, 200, 200), stop: 0.8 rgb(255, 255, 255));\n"
"}\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 40px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: none;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/icons/icons/arrow_down.png);\n"
"    padding-right:8px;\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"\n"
"\n"
"#comboBox_menu, #comboBox_menu_2, #comboBox_menu_3, #comboBox_menu_4{\n"
"    padding: 1px 1px 1px 1px;\n"
"    background-color:transparent;\n"
"    border:none;\n"
"    border-radius: 0px;\n"
"    color:transparent;\n"
"    image: url(:/icons/icons/menu.png);\n"
"}\n"
"\n"
"#comboBox_menu:on, #comboBox_menu_2:on, #comboBox_menu_3:on, #comboBox_menu_4:on{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox#comboBox_menu::down-arrow {image: none;}\n"
"QComboBox#comboBox_menu_2::down-arrow {image: none;}\n"
"QComboBox#comboBox_menu_3::down-arrow {image: none;}\n"
"QComboBox#comboBox_menu_4::down-arrow {image: none;}\n"
"\n"
"QLabel{\n"
"    color:white;\n"
"    font: 12pt \"Century Gothic\"\n"
"}\n"
"\n"
"#label_user_id, #label_user_id_2{\n"
"    color:white;\n"
"    font: 10pt \"Century Gothic\";\n"
"}\n"
"\n"
"#label_settings, #label_data{\n"
"    color:black;\n"
"    font: bold 14pt \"Century Gothic\";\n"
"}\n"
"\n"
"#label_imgCount{\n"
"    color:black;\n"
"    font: 10pt \"Century Gothic\";\n"
"}\n"
"\n"
"#frame_homeBar,\n"
"#frame_dataBar,\n"
"#frame_settingsBar,\n"
"#frame_handbookBar,\n"
"#frame_aboutBar\n"
"{background-color: rgb(0, 203, 221);}\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        
        # home page
        self.page_home = QtWidgets.QWidget()
        self.page_home.setFocusPolicy(QtCore.Qt.NoFocus)
        self.page_home.setStyleSheet("#btn_leftImg:hover, #btn_rightImg:hover{background-color:transparent;}")
        self.page_home.setObjectName("page_home")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_home)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_homeBar = QtWidgets.QFrame(self.page_home)
        self.frame_homeBar.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_homeBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_homeBar.setStyleSheet("")
        self.frame_homeBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_homeBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_homeBar.setLineWidth(0)
        self.frame_homeBar.setObjectName("frame_homeBar")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_homeBar)
        self.horizontalLayout_3.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_user_2 = QtWidgets.QPushButton(self.frame_homeBar)
        self.btn_user_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user_2.sizePolicy().hasHeightForWidth())
        self.btn_user_2.setSizePolicy(sizePolicy)
        self.btn_user_2.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user_2.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user_2.setStyleSheet("")
        self.btn_user_2.setText("")
        self.btn_user_2.setIconSize(QtCore.QSize(20, 20))
        self.btn_user_2.setObjectName("btn_user_2")
        self.horizontalLayout_3.addWidget(self.btn_user_2)
        self.label_user_id_2 = QtWidgets.QLabel(self.frame_homeBar)
        self.label_user_id_2.setEnabled(True)
        self.label_user_id_2.setStyleSheet("color:transparent")
        self.label_user_id_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_2.setObjectName("label_user_id_2")
        self.horizontalLayout_3.addWidget(self.label_user_id_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.icon_home = QtWidgets.QLabel(self.frame_homeBar)
        self.icon_home.setMinimumSize(QtCore.QSize(20, 20))
        self.icon_home.setMaximumSize(QtCore.QSize(20, 20))
        self.icon_home.setText("")
        self.icon_home.setPixmap(QtGui.QPixmap(":/icons/icons/home_w.png"))
        self.icon_home.setScaledContents(True)
        self.icon_home.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_home.setObjectName("icon_home")
        self.horizontalLayout_3.addWidget(self.icon_home)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_user_id = QtWidgets.QLabel(self.frame_homeBar)
        self.label_user_id.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id.setObjectName("label_user_id")
        self.horizontalLayout_3.addWidget(self.label_user_id)
        self.btn_user = QtWidgets.QPushButton(self.frame_homeBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user.sizePolicy().hasHeightForWidth())
        self.btn_user.setSizePolicy(sizePolicy)
        self.btn_user.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user.setText("")
        self.btn_user.setIcon(self.icon_loader.get_icon("icon1"))
        self.btn_user.setIconSize(QtCore.QSize(20, 20))
        self.btn_user.setObjectName("btn_user")
        self.horizontalLayout_3.addWidget(self.btn_user)
        self.verticalLayout.addWidget(self.frame_homeBar)
        self.frame_controlBar = QtWidgets.QFrame(self.page_home)
        self.frame_controlBar.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_controlBar.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_controlBar.setStyleSheet("")
        self.frame_controlBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_controlBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_controlBar.setLineWidth(0)
        self.frame_controlBar.setObjectName("frame_controlBar")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_controlBar)
        self.horizontalLayout_4.setContentsMargins(11, 5, 11, 5)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.btn_menu2 = QtWidgets.QPushButton(self.frame_controlBar)
        self.btn_menu2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu2.sizePolicy().hasHeightForWidth())
        self.btn_menu2.setSizePolicy(sizePolicy)
        self.btn_menu2.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu2.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu2.setText("")
        self.btn_menu2.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu2.setObjectName("btn_menu2")
        self.horizontalLayout_4.addWidget(self.btn_menu2)
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.btn_imgSwitch = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
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
        self.btn_imgSwitch.setStyleSheet("")
        self.btn_imgSwitch.setObjectName("btn_imgSwitch")
        self.horizontalLayout_4.addWidget(self.btn_imgSwitch)
        self.btn_filter = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_filter.sizePolicy().hasHeightForWidth())
        self.btn_filter.setSizePolicy(sizePolicy)
        self.btn_filter.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_filter.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_filter.setText("")
        self.btn_filter.setIcon(self.icon_loader.get_icon("icon2"))
        self.btn_filter.setIconSize(QtCore.QSize(30, 30))
        self.btn_filter.setObjectName("btn_filter")
        self.horizontalLayout_4.addWidget(self.btn_filter)
        self.comboBox_imgRemark = QtWidgets.QComboBox(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_imgRemark.sizePolicy().hasHeightForWidth())
        self.comboBox_imgRemark.setSizePolicy(sizePolicy)
        self.comboBox_imgRemark.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_imgRemark.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_imgRemark.setEditable(True)
        self.comboBox_imgRemark.setObjectName("comboBox_imgRemark")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_imgRemark)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.btn_zoom = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_zoom.sizePolicy().hasHeightForWidth())
        self.btn_zoom.setSizePolicy(sizePolicy)
        self.btn_zoom.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_zoom.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_zoom.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom.setIcon(icon3)
        self.btn_zoom.setIconSize(QtCore.QSize(30, 30))
        self.btn_zoom.setObjectName("btn_zoom")
        self.horizontalLayout_4.addWidget(self.btn_zoom)
        self.btn_add = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_add.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_add.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon4)
        self.btn_add.setIconSize(QtCore.QSize(30, 30))
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_4.addWidget(self.btn_add)
        self.btn_previous = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_previous.sizePolicy().hasHeightForWidth())
        self.btn_previous.setSizePolicy(sizePolicy)
        self.btn_previous.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_previous.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_previous.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_left_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_previous.setIcon(icon5)
        self.btn_previous.setIconSize(QtCore.QSize(30, 30))
        self.btn_previous.setObjectName("btn_previous")
        self.horizontalLayout_4.addWidget(self.btn_previous)
        self.btn_placeholder = QtWidgets.QPushButton(self.frame_controlBar)
        self.btn_placeholder.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_placeholder.sizePolicy().hasHeightForWidth())
        self.btn_placeholder.setSizePolicy(sizePolicy)
        self.btn_placeholder.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_placeholder.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_placeholder.setText("")
        self.btn_placeholder.setIconSize(QtCore.QSize(30, 30))
        self.btn_placeholder.setObjectName("btn_placeholder")
        self.horizontalLayout_4.addWidget(self.btn_placeholder)
        self.btn_next = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_next.sizePolicy().hasHeightForWidth())
        self.btn_next.setSizePolicy(sizePolicy)
        self.btn_next.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_next.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_next.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_right_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_next.setIcon(icon6)
        self.btn_next.setIconSize(QtCore.QSize(30, 30))
        self.btn_next.setObjectName("btn_next")
        self.horizontalLayout_4.addWidget(self.btn_next)
        self.btn_delete = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy)
        self.btn_delete.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_delete.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_delete.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/bin_closed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon7)
        self.btn_delete.setIconSize(QtCore.QSize(30, 30))
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_4.addWidget(self.btn_delete)
        self.btn_undo = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_undo.sizePolicy().hasHeightForWidth())
        self.btn_undo.setSizePolicy(sizePolicy)
        self.btn_undo.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_undo.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_undo.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_undo.setIcon(icon8)
        self.btn_undo.setIconSize(QtCore.QSize(30, 30))
        self.btn_undo.setObjectName("btn_undo")
        self.horizontalLayout_4.addWidget(self.btn_undo)
        spacerItem4 = QtWidgets.QSpacerItem(354, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        
        self.btn_menu = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu.sizePolicy().hasHeightForWidth())
        self.btn_menu.setSizePolicy(sizePolicy)
        self.btn_menu.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu.setText("")
        self.icon9 = QtGui.QIcon()
        self.icon9.addPixmap(QtGui.QPixmap(":/icons/icons/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_menu.setIcon(self.icon9)
        self.btn_menu.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu.setObjectName("btn_menu")
        self.append_main_menu_to_button(self.btn_menu)
        
        self.horizontalLayout_4.addWidget(self.btn_menu)
        self.verticalLayout.addWidget(self.frame_controlBar)
        self.frame_imgDisplay = QtWidgets.QFrame(self.page_home)
        self.frame_imgDisplay.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_imgDisplay.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_imgDisplay.setLineWidth(0)
        self.frame_imgDisplay.setObjectName("frame_imgDisplay")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_imgDisplay)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame_left = QtWidgets.QFrame(self.frame_imgDisplay)
        self.frame_left.setMinimumSize(QtCore.QSize(60, 0))
        self.frame_left.setMaximumSize(QtCore.QSize(60, 16777215))
        self.frame_left.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_left.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_left.setStyleSheet("")
        self.frame_left.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left.setObjectName("frame_left")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_left)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.btn_leftImg = QtWidgets.QPushButton(self.frame_left)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_leftImg.sizePolicy().hasHeightForWidth())
        self.btn_leftImg.setSizePolicy(sizePolicy)
        self.btn_leftImg.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_left_big.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_leftImg.setIcon(icon10)
        self.btn_leftImg.setIconSize(QtCore.QSize(20, 40))
        self.btn_leftImg.setCheckable(False)
        self.btn_leftImg.setFlat(False)
        self.btn_leftImg.setObjectName("btn_leftImg")
        self.verticalLayout_2.addWidget(self.btn_leftImg)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem8)
        self.label_imgCount = QtWidgets.QLabel(self.frame_left)
        self.label_imgCount.setMinimumSize(QtCore.QSize(0, 40))
        self.label_imgCount.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_imgCount.setAlignment(QtCore.Qt.AlignCenter)
        self.label_imgCount.setObjectName("label_imgCount")
        self.verticalLayout_2.addWidget(self.label_imgCount)
        self.horizontalLayout_5.addWidget(self.frame_left)
        self.frame_img = QtWidgets.QFrame(self.frame_imgDisplay)
        self.frame_img.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_img.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_img.setObjectName("frame_img")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_img)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.image = QtWidgets.QLabel(self.frame_img)
        self.image.setText("")
        self.image.setPixmap(QtGui.QPixmap("../data/maritime_dataset_25/training_data_animals/0.jpg"))
        self.image.setScaledContents(True)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setObjectName("image")
        self.gridLayout_2.addWidget(self.image, 0, 0, 1, 1)
        self.horizontalLayout_5.addWidget(self.frame_img)
        self.frame_right = QtWidgets.QFrame(self.frame_imgDisplay)
        self.frame_right.setMinimumSize(QtCore.QSize(60, 0))
        self.frame_right.setMaximumSize(QtCore.QSize(60, 16777215))
        self.frame_right.setStyleSheet("")
        self.frame_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_right.setObjectName("frame_right")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_right)
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        self.btn_rightImg = QtWidgets.QPushButton(self.frame_right)
        self.btn_rightImg.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_right_big.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_rightImg.setIcon(icon11)
        self.btn_rightImg.setIconSize(QtCore.QSize(20, 40))
        self.btn_rightImg.setObjectName("btn_rightImg")
        self.verticalLayout_3.addWidget(self.btn_rightImg)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem10)
        self.btn_openImg = QtWidgets.QPushButton(self.frame_right)
        self.btn_openImg.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_openImg.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_openImg.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/icons/open_image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_openImg.setIcon(icon12)
        self.btn_openImg.setIconSize(QtCore.QSize(30, 30))
        self.btn_openImg.setObjectName("btn_openImg")
        self.verticalLayout_3.addWidget(self.btn_openImg)
        self.horizontalLayout_5.addWidget(self.frame_right)
        self.verticalLayout.addWidget(self.frame_imgDisplay)
        self.stackedWidget.addWidget(self.page_home)
        
        # data page
        self.page_data = QtWidgets.QWidget()
        self.page_data.setObjectName("page_data")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_data)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_dataBar = QtWidgets.QFrame(self.page_data)
        self.frame_dataBar.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_dataBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_dataBar.setStyleSheet("")
        self.frame_dataBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_dataBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dataBar.setLineWidth(0)
        self.frame_dataBar.setObjectName("frame_dataBar")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_dataBar)
        self.horizontalLayout_9.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.btn_user_data_2 = QtWidgets.QPushButton(self.frame_dataBar)
        self.btn_user_data_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user_data_2.sizePolicy().hasHeightForWidth())
        self.btn_user_data_2.setSizePolicy(sizePolicy)
        self.btn_user_data_2.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user_data_2.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user_data_2.setStyleSheet("")
        self.btn_user_data_2.setText("")
        self.btn_user_data_2.setIconSize(QtCore.QSize(20, 20))
        self.btn_user_data_2.setObjectName("btn_user_data_2")
        self.horizontalLayout_9.addWidget(self.btn_user_data_2)
        
        self.label_user_id_data_2 = QtWidgets.QLabel(self.frame_dataBar)
        self.label_user_id_data_2.setEnabled(True)
        self.label_user_id_data_2.setStyleSheet("color:transparent")
        self.label_user_id_data_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_data_2.setObjectName("label_user_id_data_2")
        self.horizontalLayout_9.addWidget(self.label_user_id_data_2)
        
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem11)
        self.icon_home_3 = QtWidgets.QLabel(self.frame_dataBar)
        self.icon_home_3.setMinimumSize(QtCore.QSize(20, 20))
        self.icon_home_3.setMaximumSize(QtCore.QSize(20, 20))
        self.icon_home_3.setText("")
        self.icon_home_3.setPixmap(QtGui.QPixmap(":/icons/icons/data_w.png"))
        self.icon_home_3.setScaledContents(True)
        self.icon_home_3.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_home_3.setObjectName("icon_home_3")
        self.horizontalLayout_9.addWidget(self.icon_home_3)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem12)
        
        self.label_user_id_data = QtWidgets.QLabel(self.frame_dataBar)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_user_id_data.setFont(font)
        self.label_user_id_data.setStyleSheet("font:10pt;")
        self.label_user_id_data.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_data.setObjectName("label_user_id_data")
        self.horizontalLayout_9.addWidget(self.label_user_id_data)
        
        self.btn_user_data = QtWidgets.QPushButton(self.frame_dataBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user_data.sizePolicy().hasHeightForWidth())
        self.btn_user_data.setSizePolicy(sizePolicy)
        self.btn_user_data.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user_data.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user_data.setText("")
        self.btn_user_data.setIcon(self.icon_loader.get_icon("icon1"))
        self.btn_user_data.setIconSize(QtCore.QSize(20, 20))
        self.btn_user_data.setObjectName("btn_user_data")
        self.horizontalLayout_9.addWidget(self.btn_user_data)
        
        self.verticalLayout_5.addWidget(self.frame_dataBar)
        self.frame_controlBar_3 = QtWidgets.QFrame(self.page_data)
        self.frame_controlBar_3.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_controlBar_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_controlBar_3.setStyleSheet("")
        self.frame_controlBar_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_controlBar_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_controlBar_3.setLineWidth(0)
        self.frame_controlBar_3.setObjectName("frame_controlBar_3")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_controlBar_3)
        self.horizontalLayout_8.setContentsMargins(11, 5, 11, 5)
        self.horizontalLayout_8.setSpacing(4)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        
        
        self.btn_menu2_3 = QtWidgets.QPushButton(self.frame_controlBar_3)
        self.btn_menu2_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu2_3.sizePolicy().hasHeightForWidth())
        self.btn_menu2_3.setSizePolicy(sizePolicy)
        self.btn_menu2_3.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu2_3.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu2_3.setText("")
        self.btn_menu2_3.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu2_3.setObjectName("btn_menu2_3")
        self.horizontalLayout_8.addWidget(self.btn_menu2_3)
        
        spacerItem13 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem13)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem14)
        self.label_data = QtWidgets.QLabel(self.frame_controlBar_3)
        self.label_data.setStyleSheet("color:black; font:bold;")
        self.label_data.setObjectName("label_data")
        self.horizontalLayout_8.addWidget(self.label_data)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem15)
        spacerItem16 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem16)
        self.btn_menu_3 = QtWidgets.QPushButton(self.frame_controlBar_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu_3.sizePolicy().hasHeightForWidth())
        self.btn_menu_3.setSizePolicy(sizePolicy)
        self.btn_menu_3.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu_3.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu_3.setText("")
        self.btn_menu_3.setIcon(self.icon9)
        self.btn_menu_3.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu_3.setObjectName("btn_menu_3")
       
        self.append_main_menu_to_button(self.btn_menu_3)       
        self.horizontalLayout_8.addWidget(self.btn_menu_3)
        
        self.verticalLayout_5.addWidget(self.frame_controlBar_3)
        self.frame_data = QtWidgets.QFrame(self.page_data)
        self.frame_data.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.frame_data.setAccessibleName("")
        self.frame_data.setStyleSheet("QLabel{ \n"
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
"\n"
"QTableView{\n"
"    font: 10pt \"Century Gothic\";\n"
"    background-color: white;  \n"
"    border-radius:3px;\n"
"}\n"
"\n"
"/*-------------------------- line edit ------------------------*/\n"
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
"}\n"
"\n"
"#btn_apply_diverging_data_info{\n"
"    background-color:rgb(150, 150, 150);\n"
"}\n"
"\n"
"#btn_res_file, #btn_img_dir, #btn_analyze{\n"
"    background-color: rgb(200, 200, 200);\n"
"}\n"
"\n"
"\n"
"#btn_apply_diverging_data_info:hover, #btn_res_file:hover, #btn_img_dir:hover, #btn_analyze:hover{\n"
"  background-color: rgb(0, 203, 221);\n"
"}\n"
"\n"
"#btn_apply_diverging_data_info:pressed, #btn_res_file:pressed, #btn_img_dir:pressed, #btn_analyze:pressed{\n"
"    background-color: rgb(0, 160, 174);\n"
"}")
        self.frame_data.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_data.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_data.setObjectName("frame_data")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_data)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.frame_data_options = QtWidgets.QFrame(self.frame_data)
        self.frame_data_options.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_data_options.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_data_options.setObjectName("frame_data_options")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.frame_data_options)
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        spacerItem17 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem17)
        self.frame_data_selection = QtWidgets.QFrame(self.frame_data_options)
        self.frame_data_selection.setStyleSheet("")
        self.frame_data_selection.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_data_selection.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_data_selection.setObjectName("frame_data_selection")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_data_selection)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.frame_data_selection)
        self.calendarWidget.setStyleSheet("QCalenderWidget{\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"/* buttons in navigation bar*/\n"
"QCalendarWidget QToolButton {\n"
"      color: white;\n"
"    font: 12pt \"Century Gothic\";\n"
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
"      background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(150, 150, 150), stop:1 rgb(200, 200, 200));\n"
"    border-radius: 3px;\n"
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
"/*-------------------------- spin box to select a year ------------------------*/\n"
"\n"
"QCalendarWidget QSpinBox {\n"
"    padding-right: 15px; /* make room for the arrows */\n"
"    /*border-image: url(:/images/frame.png) 4;*/\n"
"    border-radius: 3px;\n"
"    selection-background-color:rgb(0, 203, 221);\n"
"    font:12pt \"Century Gothic\";\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(150, 150, 150), stop:1 rgb(200, 200, 200));\n"
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
"    subcontrol-position: bottom right; /* position at bottom right corner */\n"
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
        self.calendarWidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Germany))
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout_7.addWidget(self.calendarWidget)
        self.frame_date = QtWidgets.QFrame(self.frame_data_selection)
        self.frame_date.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_date.setMaximumSize(QtCore.QSize(16777214, 40))
        self.frame_date.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_date.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_date.setObjectName("frame_date")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_date)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_date_text = QtWidgets.QLabel(self.frame_date)
        self.label_date_text.setStyleSheet("")
        self.label_date_text.setObjectName("label_date_text")
        self.horizontalLayout.addWidget(self.label_date_text)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem18)
        self.label_date = QtWidgets.QLabel(self.frame_date)
        self.label_date.setObjectName("label_date")
        self.horizontalLayout.addWidget(self.label_date)
        self.verticalLayout_7.addWidget(self.frame_date)
        self.frame_img_filter = QtWidgets.QFrame(self.frame_data_selection)
        self.frame_img_filter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_img_filter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_img_filter.setObjectName("frame_img_filter")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_img_filter)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_image_filter = QtWidgets.QLabel(self.frame_img_filter)
        self.label_image_filter.setStyleSheet("")
        self.label_image_filter.setObjectName("label_image_filter")
        self.horizontalLayout_2.addWidget(self.label_image_filter)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem19)
        self.comboBox_image_filter = QtWidgets.QComboBox(self.frame_img_filter)
        self.comboBox_image_filter.setMinimumSize(QtCore.QSize(250, 40))
        self.comboBox_image_filter.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_image_filter.setObjectName("comboBox_image_filter")
        self.comboBox_image_filter.addItem("")
        self.comboBox_image_filter.addItem("")
        self.comboBox_image_filter.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_image_filter)
        self.verticalLayout_7.addWidget(self.frame_img_filter)
        self.horizontalLayout_22.addWidget(self.frame_data_selection)
        spacerItem20 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem20)
        self.frame_data_information = QtWidgets.QFrame(self.frame_data_options)
        self.frame_data_information.setEnabled(False)
        self.frame_data_information.setStyleSheet("")
        self.frame_data_information.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_data_information.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_data_information.setObjectName("frame_data_information")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_data_information)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lineEdit_res_file = QtWidgets.QLineEdit(self.frame_data_information)
        self.lineEdit_res_file.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_res_file.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_res_file.setObjectName("lineEdit_res_file")
        self.gridLayout_5.addWidget(self.lineEdit_res_file, 2, 1, 1, 1)
        self.label_num_imgs = QtWidgets.QLabel(self.frame_data_information)
        self.label_num_imgs.setStyleSheet("")
        self.label_num_imgs.setObjectName("label_num_imgs")
        self.gridLayout_5.addWidget(self.label_num_imgs, 5, 0, 1, 1)
        self.lineEdit_img_dir = QtWidgets.QLineEdit(self.frame_data_information)
        self.lineEdit_img_dir.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_img_dir.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_img_dir.setObjectName("lineEdit_img_dir")
        self.gridLayout_5.addWidget(self.lineEdit_img_dir, 1, 1, 1, 1)
        self.frame_num_imgs = QtWidgets.QFrame(self.frame_data_information)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_num_imgs.sizePolicy().hasHeightForWidth())
        self.frame_num_imgs.setSizePolicy(sizePolicy)
        self.frame_num_imgs.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_num_imgs.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_num_imgs.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_num_imgs.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_num_imgs.setObjectName("frame_num_imgs")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame_num_imgs)
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.btn_img_dir = QtWidgets.QPushButton(self.frame_num_imgs)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_img_dir.sizePolicy().hasHeightForWidth())
        self.btn_img_dir.setSizePolicy(sizePolicy)
        self.btn_img_dir.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_img_dir.setMaximumSize(QtCore.QSize(70, 40))
        self.btn_img_dir.setObjectName("btn_img_dir")
        self.horizontalLayout_21.addWidget(self.btn_img_dir)
        self.gridLayout_5.addWidget(self.frame_num_imgs, 1, 2, 1, 1)
        self.frame_apply_diverging_data_info = QtWidgets.QFrame(self.frame_data_information)
        self.frame_apply_diverging_data_info.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_apply_diverging_data_info.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_apply_diverging_data_info.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_apply_diverging_data_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_apply_diverging_data_info.setObjectName("frame_apply_diverging_data_info")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.frame_apply_diverging_data_info)
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.gridLayout_5.addWidget(self.frame_apply_diverging_data_info, 3, 2, 1, 1)
        self.label_exp_id = QtWidgets.QLabel(self.frame_data_information)
        self.label_exp_id.setStyleSheet("")
        self.label_exp_id.setObjectName("label_exp_id")
        self.gridLayout_5.addWidget(self.label_exp_id, 4, 0, 1, 1)
        self.label_img_dir = QtWidgets.QLabel(self.frame_data_information)
        self.label_img_dir.setStyleSheet("")
        self.label_img_dir.setObjectName("label_img_dir")
        self.gridLayout_5.addWidget(self.label_img_dir, 1, 0, 1, 1)
        self.btn_apply_diverging_data_info = QtWidgets.QPushButton(self.frame_data_information)
        self.btn_apply_diverging_data_info.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_apply_diverging_data_info.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_apply_diverging_data_info.setStyleSheet("font:bold;")
        self.btn_apply_diverging_data_info.setObjectName("btn_apply_diverging_data_info")
        self.gridLayout_5.addWidget(self.btn_apply_diverging_data_info, 7, 2, 1, 1)
        self.lineEdit_img_prefix = QtWidgets.QLineEdit(self.frame_data_information)
        self.lineEdit_img_prefix.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_img_prefix.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_img_prefix.setObjectName("lineEdit_img_prefix")
        self.gridLayout_5.addWidget(self.lineEdit_img_prefix, 3, 1, 1, 1)
        self.label_res_file = QtWidgets.QLabel(self.frame_data_information)
        self.label_res_file.setStyleSheet("")
        self.label_res_file.setObjectName("label_res_file")
        self.gridLayout_5.addWidget(self.label_res_file, 2, 0, 1, 1)
        self.label_num_imgs_text = QtWidgets.QLabel(self.frame_data_information)
        self.label_num_imgs_text.setStyleSheet("padding-left: 10px;")
        self.label_num_imgs_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_num_imgs_text.setObjectName("label_num_imgs_text")
        self.gridLayout_5.addWidget(self.label_num_imgs_text, 5, 1, 1, 1)
        self.frame_img_dir = QtWidgets.QFrame(self.frame_data_information)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_img_dir.sizePolicy().hasHeightForWidth())
        self.frame_img_dir.setSizePolicy(sizePolicy)
        self.frame_img_dir.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_img_dir.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_img_dir.setObjectName("frame_img_dir")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_img_dir)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.gridLayout_5.addWidget(self.frame_img_dir, 0, 2, 1, 1)
        self.btn_res_file = QtWidgets.QPushButton(self.frame_data_information)
        self.btn_res_file.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_res_file.setMaximumSize(QtCore.QSize(70, 40))
        self.btn_res_file.setObjectName("btn_res_file")
        self.gridLayout_5.addWidget(self.btn_res_file, 2, 2, 1, 1)
        self.lineEdit_exp_id = QtWidgets.QLineEdit(self.frame_data_information)
        self.lineEdit_exp_id.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_exp_id.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_exp_id.setObjectName("lineEdit_exp_id")
        self.gridLayout_5.addWidget(self.lineEdit_exp_id, 4, 1, 1, 1)
        self.label_img_prefix = QtWidgets.QLabel(self.frame_data_information)
        self.label_img_prefix.setStyleSheet("")
        self.label_img_prefix.setObjectName("label_img_prefix")
        self.gridLayout_5.addWidget(self.label_img_prefix, 3, 0, 1, 1)
        spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem21, 6, 1, 1, 1)
        self.horizontalLayout_22.addWidget(self.frame_data_information)
        spacerItem22 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem22)
        self.verticalLayout_13.addWidget(self.frame_data_options)
        self.btn_analyze = QtWidgets.QPushButton(self.frame_data)
        self.btn_analyze.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_analyze.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_analyze.setObjectName("btn_analyze")
        self.verticalLayout_13.addWidget(self.btn_analyze)
        self.frame_table = QtWidgets.QFrame(self.frame_data)
        self.frame_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_table.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_table.setObjectName("frame_table")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_table)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.frame_table)
        self.tabWidget_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_2.setAutoFillBackground(False)
        self.tabWidget_2.setStyleSheet("/*-------------------------- tab widget ------------------------*/\n"
"QTabWidget{\n"
"    font: 10pt \"Century Gothic\";\n"
"}\n"
"\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"       border:None;\n"
"}\n"
"\n"
"\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"    border: None;\n"
"    min-width: 10ex;\n"
"    padding: 5px;\n"
"    padding-bottom:5px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: white;\n"
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
"")
        self.tabWidget_2.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.original = QtWidgets.QWidget()
        self.original.setObjectName("original")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.original)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.tableView_original = QtWidgets.QTableView(self.original)
        self.tableView_original.setObjectName("tableView_original")
        self.verticalLayout_15.addWidget(self.tableView_original)
        self.tabWidget_2.addTab(self.original, "")
        self.summary = QtWidgets.QWidget()
        self.summary.setObjectName("summary")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.summary)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.tableView_summary = QtWidgets.QTableView(self.summary)
        self.tableView_summary.setObjectName("tableView_summary")
        self.verticalLayout_16.addWidget(self.tableView_summary)
        self.tabWidget_2.addTab(self.summary, "")
        self.verticalLayout_14.addWidget(self.tabWidget_2)
        self.verticalLayout_13.addWidget(self.frame_table)
        self.verticalLayout_5.addWidget(self.frame_data)
        self.stackedWidget.addWidget(self.page_data)
        
        self.setup_page_settings()
        #self.page_settings = page_settings.SettingsPage(self)
        #self.stackedWidget.addWidget(self.page_settings)
        
        # handbook page
        self.page_handbook = QtWidgets.QWidget()
        self.page_handbook.setObjectName("page_handbook")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.page_handbook)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.frame_handbookBar = QtWidgets.QFrame(self.page_handbook)
        self.frame_handbookBar.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_handbookBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_handbookBar.setStyleSheet("")
        self.frame_handbookBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_handbookBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_handbookBar.setLineWidth(0)
        self.frame_handbookBar.setObjectName("frame_handbookBar")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.frame_handbookBar)
        self.horizontalLayout_30.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.btn_user_handbook_2 = QtWidgets.QPushButton(self.frame_handbookBar)
        self.btn_user_handbook_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user_handbook_2.sizePolicy().hasHeightForWidth())
        self.btn_user_handbook_2.setSizePolicy(sizePolicy)
        self.btn_user_handbook_2.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user_handbook_2.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user_handbook_2.setStyleSheet("")
        self.btn_user_handbook_2.setText("")
        self.btn_user_handbook_2.setIconSize(QtCore.QSize(20, 20))
        self.btn_user_handbook_2.setObjectName("btn_user_handbook_2")
        self.horizontalLayout_30.addWidget(self.btn_user_handbook_2)
        
        self.label_user_id_handbook_2 = QtWidgets.QLabel(self.frame_handbookBar)
        self.label_user_id_handbook_2.setEnabled(True)
        self.label_user_id_handbook_2.setStyleSheet("color:transparent")
        self.label_user_id_handbook_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_handbook_2.setObjectName("label_user_id_handbook_2")
        self.horizontalLayout_30.addWidget(self.label_user_id_handbook_2)
        
        spacerItem50 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_30.addItem(spacerItem50)
        self.icon_settings_2 = QtWidgets.QLabel(self.frame_handbookBar)
        self.icon_settings_2.setMinimumSize(QtCore.QSize(20, 20))
        self.icon_settings_2.setMaximumSize(QtCore.QSize(20, 20))
        self.icon_settings_2.setText("")
        self.icon_settings_2.setPixmap(QtGui.QPixmap(":/icons/icons/book.png"))
        self.icon_settings_2.setScaledContents(True)
        self.icon_settings_2.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_settings_2.setObjectName("icon_settings_2")
        self.horizontalLayout_30.addWidget(self.icon_settings_2)
        spacerItem51 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_30.addItem(spacerItem51)
        
        self.label_user_id_handbook = QtWidgets.QLabel(self.frame_handbookBar)
        self.label_user_id_handbook.setStyleSheet("color:white; font:10pt;")
        self.label_user_id_handbook.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_handbook.setObjectName("label_user_id_handbook")
        self.horizontalLayout_30.addWidget(self.label_user_id_handbook)
        
        self.btn_user_handbook = QtWidgets.QPushButton(self.frame_handbookBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user_handbook.sizePolicy().hasHeightForWidth())
        self.btn_user_handbook.setSizePolicy(sizePolicy)
        self.btn_user_handbook.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user_handbook.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user_handbook.setText("")
        self.btn_user_handbook.setIcon(self.icon_loader.get_icon("icon1"))
        self.btn_user_handbook.setIconSize(QtCore.QSize(20, 20))
        self.btn_user_handbook.setObjectName("btn_user_handbook")
        self.horizontalLayout_30.addWidget(self.btn_user_handbook)
        self.verticalLayout_12.addWidget(self.frame_handbookBar)
        self.frame_controlBar_4 = QtWidgets.QFrame(self.page_handbook)
        self.frame_controlBar_4.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_controlBar_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_controlBar_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_controlBar_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_controlBar_4.setLineWidth(0)
        self.frame_controlBar_4.setObjectName("frame_controlBar_4")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(self.frame_controlBar_4)
        self.horizontalLayout_29.setContentsMargins(11, 5, 11, 5)
        self.horizontalLayout_29.setSpacing(4)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.btn_menu_settings_3 = QtWidgets.QPushButton(self.frame_controlBar_4)
        self.btn_menu_settings_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu_settings_3.sizePolicy().hasHeightForWidth())
        self.btn_menu_settings_3.setSizePolicy(sizePolicy)
        self.btn_menu_settings_3.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings_3.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings_3.setText("")
        self.btn_menu_settings_3.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu_settings_3.setObjectName("btn_menu_settings_3")
        self.horizontalLayout_29.addWidget(self.btn_menu_settings_3)
        spacerItem52 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_29.addItem(spacerItem52)
        spacerItem53 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_29.addItem(spacerItem53)
        self.label_settings_2 = QtWidgets.QLabel(self.frame_controlBar_4)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_settings_2.setFont(font)
        self.label_settings_2.setStyleSheet("color:black; font: bold 14pt;")
        self.label_settings_2.setObjectName("label_settings_2")
        self.horizontalLayout_29.addWidget(self.label_settings_2)
        spacerItem54 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_29.addItem(spacerItem54)
        spacerItem55 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_29.addItem(spacerItem55)
        
        self.btn_menu_settings_4 = QtWidgets.QPushButton(self.frame_controlBar_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu_settings_4.sizePolicy().hasHeightForWidth())
        self.btn_menu_settings_4.setSizePolicy(sizePolicy)
        self.btn_menu_settings_4.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings_4.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings_4.setText("")
        self.btn_menu_settings_4.setIcon(self.icon9)
        self.btn_menu_settings_4.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu_settings_4.setObjectName("btn_menu_settings_4")
        self.append_main_menu_to_button(self.btn_menu_settings_4)
        self.horizontalLayout_29.addWidget(self.btn_menu_settings_4)
        
        self.verticalLayout_12.addWidget(self.frame_controlBar_4)
        self.frame_handbook = QtWidgets.QFrame(self.page_handbook)
        self.frame_handbook.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_handbook.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_handbook.setObjectName("frame_handbook")
        self.verticalLayout_12.addWidget(self.frame_handbook)
        self.stackedWidget.addWidget(self.page_handbook)
        
        # about page
        self.page_about = PageAbout.PageAbout()
        self.stackedWidget.addWidget(self.page_about)
        self.horizontalLayout_15.addWidget(self.stackedWidget)
        
#         self.page_about = QtWidgets.QWidget()
#         self.page_about.setObjectName("page_about")
#         self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.page_about)
#         self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
#         self.verticalLayout_11.setSpacing(0)
#         self.verticalLayout_11.setObjectName("verticalLayout_11")
#         self.frame_aboutBar = QtWidgets.QFrame(self.page_about)
#         self.frame_aboutBar.setMinimumSize(QtCore.QSize(0, 30))
#         self.frame_aboutBar.setMaximumSize(QtCore.QSize(16777215, 30))
#         self.frame_aboutBar.setStyleSheet("")
#         self.frame_aboutBar.setFrameShape(QtWidgets.QFrame.NoFrame)
#         self.frame_aboutBar.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_aboutBar.setLineWidth(0)
#         self.frame_aboutBar.setObjectName("frame_aboutBar")
#         self.horizontalLayout_34 = QtWidgets.QHBoxLayout(self.frame_aboutBar)
#         self.horizontalLayout_34.setContentsMargins(-1, 2, -1, 2)
#         self.horizontalLayout_34.setObjectName("horizontalLayout_34")
#         self.btn_user_about_2 = QtWidgets.QPushButton(self.frame_aboutBar)
#         self.btn_user_about_2.setEnabled(False)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.btn_user_about_2.sizePolicy().hasHeightForWidth())
#         self.btn_user_about_2.setSizePolicy(sizePolicy)
#         self.btn_user_about_2.setMinimumSize(QtCore.QSize(25, 25))
#         self.btn_user_about_2.setMaximumSize(QtCore.QSize(25, 25))
#         self.btn_user_about_2.setStyleSheet("")
#         self.btn_user_about_2.setText("")
#         self.btn_user_about_2.setIconSize(QtCore.QSize(20, 20))
#         self.btn_user_about_2.setObjectName("btn_user_about_2")
#         self.horizontalLayout_34.addWidget(self.btn_user_about_2)
        
#         self.label_user_id_about_2 = QtWidgets.QLabel(self.frame_aboutBar)
#         self.label_user_id_about_2.setEnabled(True)
#         self.label_user_id_about_2.setStyleSheet("color:transparent")
#         self.label_user_id_about_2.setTextFormat(QtCore.Qt.AutoText)
#         self.label_user_id_about_2.setObjectName("label_user_id_about_2")
#         self.horizontalLayout_34.addWidget(self.label_user_id_about_2)
        
#         spacerItem56 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         self.horizontalLayout_34.addItem(spacerItem56)
#         self.icon_settings_3 = QtWidgets.QLabel(self.frame_aboutBar)
#         self.icon_settings_3.setMinimumSize(QtCore.QSize(20, 20))
#         self.icon_settings_3.setMaximumSize(QtCore.QSize(20, 20))
#         self.icon_settings_3.setText("")
#         self.icon_settings_3.setPixmap(QtGui.QPixmap(":/icons/icons/fish_white.png"))
#         self.icon_settings_3.setScaledContents(True)
#         self.icon_settings_3.setAlignment(QtCore.Qt.AlignCenter)
#         self.icon_settings_3.setObjectName("icon_settings_3")
#         self.horizontalLayout_34.addWidget(self.icon_settings_3)
#         spacerItem57 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         self.horizontalLayout_34.addItem(spacerItem57)
        
#         self.label_user_id_about = QtWidgets.QLabel(self.frame_aboutBar)
#         self.label_user_id_about.setStyleSheet("color:white; font:10pt;")
#         self.label_user_id_about.setTextFormat(QtCore.Qt.AutoText)
#         self.label_user_id_about.setObjectName("label_user_id_about")
#         self.horizontalLayout_34.addWidget(self.label_user_id_about)
        
#         self.btn_user_about = QtWidgets.QPushButton(self.frame_aboutBar)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.btn_user_about.sizePolicy().hasHeightForWidth())
#         self.btn_user_about.setSizePolicy(sizePolicy)
#         self.btn_user_about.setMinimumSize(QtCore.QSize(25, 25))
#         self.btn_user_about.setMaximumSize(QtCore.QSize(25, 25))
#         self.btn_user_about.setText("")
#         self.btn_user_about.setIcon(self.icon1)
#         self.btn_user_about.setIconSize(QtCore.QSize(20, 20))
#         self.btn_user_about.setObjectName("btn_user_about")
#         self.horizontalLayout_34.addWidget(self.btn_user_about)
#         self.verticalLayout_11.addWidget(self.frame_aboutBar)
#         self.frame_controlBar_5 = QtWidgets.QFrame(self.page_about)
#         self.frame_controlBar_5.setMinimumSize(QtCore.QSize(0, 50))
#         self.frame_controlBar_5.setMaximumSize(QtCore.QSize(16777215, 50))
#         self.frame_controlBar_5.setFrameShape(QtWidgets.QFrame.NoFrame)
#         self.frame_controlBar_5.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_controlBar_5.setLineWidth(0)
#         self.frame_controlBar_5.setObjectName("frame_controlBar_5")
#         self.horizontalLayout_31 = QtWidgets.QHBoxLayout(self.frame_controlBar_5)
#         self.horizontalLayout_31.setContentsMargins(11, 5, 11, 5)
#         self.horizontalLayout_31.setSpacing(4)
#         self.horizontalLayout_31.setObjectName("horizontalLayout_31")
#         self.btn_menu_settings_5 = QtWidgets.QPushButton(self.frame_controlBar_5)
#         self.btn_menu_settings_5.setEnabled(False)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.btn_menu_settings_5.sizePolicy().hasHeightForWidth())
#         self.btn_menu_settings_5.setSizePolicy(sizePolicy)
#         self.btn_menu_settings_5.setMinimumSize(QtCore.QSize(40, 40))
#         self.btn_menu_settings_5.setMaximumSize(QtCore.QSize(40, 40))
#         self.btn_menu_settings_5.setText("")
#         self.btn_menu_settings_5.setIconSize(QtCore.QSize(30, 30))
#         self.btn_menu_settings_5.setObjectName("btn_menu_settings_5")
#         self.horizontalLayout_31.addWidget(self.btn_menu_settings_5)
#         spacerItem58 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
#         self.horizontalLayout_31.addItem(spacerItem58)
#         spacerItem59 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         self.horizontalLayout_31.addItem(spacerItem59)
#         self.label_settings_3 = QtWidgets.QLabel(self.frame_controlBar_5)
#         font = QtGui.QFont()
#         font.setFamily("Century Gothic")
#         font.setPointSize(14)
#         font.setBold(True)
#         font.setItalic(False)
#         font.setWeight(75)
#         self.label_settings_3.setFont(font)
#         self.label_settings_3.setStyleSheet("color:black; font: bold 14pt;")
#         self.label_settings_3.setObjectName("label_settings_3")
#         self.horizontalLayout_31.addWidget(self.label_settings_3)
#         spacerItem60 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         self.horizontalLayout_31.addItem(spacerItem60)
#         spacerItem61 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
#         self.horizontalLayout_31.addItem(spacerItem61)
        
#         self.btn_menu_settings_6 = QtWidgets.QPushButton(self.frame_controlBar_5)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.btn_menu_settings_6.sizePolicy().hasHeightForWidth())
#         self.btn_menu_settings_6.setSizePolicy(sizePolicy)
#         self.btn_menu_settings_6.setMinimumSize(QtCore.QSize(40, 40))
#         self.btn_menu_settings_6.setMaximumSize(QtCore.QSize(40, 40))
#         self.btn_menu_settings_6.setText("")
#         self.btn_menu_settings_6.setIcon(self.icon9)
#         self.btn_menu_settings_6.setIconSize(QtCore.QSize(30, 30))
#         self.btn_menu_settings_6.setObjectName("btn_menu_settings_6")
#         self.append_main_menu_to_button(self.btn_menu_settings_6)
#         self.horizontalLayout_31.addWidget(self.btn_menu_settings_6)
        
#         self.verticalLayout_11.addWidget(self.frame_controlBar_5)
#         self.frame_about = QtWidgets.QFrame(self.page_about)
#         self.frame_about.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame_about.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_about.setObjectName("frame_about")
#         self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.frame_about)
#         self.verticalLayout_19.setObjectName("verticalLayout_19")
#         self.label_about_text = QtWidgets.QLabel(self.frame_about)
#         self.label_about_text.setStyleSheet("color:black; \n"
# "padding:10px;\n"
# "background-color:rgb(230, 230, 230);\n"
# "border-radius:3px;")
#         self.label_about_text.setScaledContents(False)
#         self.label_about_text.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_about_text.setWordWrap(True)
#         self.label_about_text.setObjectName("label_about_text")
#         self.verticalLayout_19.addWidget(self.label_about_text)
#         spacerItem62 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
#         self.verticalLayout_19.addItem(spacerItem62)
#         self.frame_logos = QtWidgets.QFrame(self.frame_about)
#         self.frame_logos.setMaximumSize(QtCore.QSize(16777215, 70))
#         self.frame_logos.setFrameShape(QtWidgets.QFrame.NoFrame)
#         self.frame_logos.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame_logos.setObjectName("frame_logos")
#         self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.frame_logos)
#         self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
#         self.horizontalLayout_24.setSpacing(0)
#         self.horizontalLayout_24.setObjectName("horizontalLayout_24")
#         self.label_logo_uni = QtWidgets.QLabel(self.frame_logos)
#         self.label_logo_uni.setMaximumSize(QtCore.QSize(400, 16777215))
#         self.label_logo_uni.setText("")
#         self.label_logo_uni.setPixmap(QtGui.QPixmap(":/logos/logos/logo_uniBremen.png"))
#         self.label_logo_uni.setScaledContents(True)
#         self.label_logo_uni.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_logo_uni.setWordWrap(False)
#         self.label_logo_uni.setObjectName("label_logo_uni")
#         self.horizontalLayout_24.addWidget(self.label_logo_uni)
#         self.label_logo_awi = QtWidgets.QLabel(self.frame_logos)
#         self.label_logo_awi.setMaximumSize(QtCore.QSize(200, 16777215))
#         self.label_logo_awi.setText("")
#         self.label_logo_awi.setPixmap(QtGui.QPixmap(":/logos/logos/logo_awi.png"))
#         self.label_logo_awi.setScaledContents(True)
#         self.label_logo_awi.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_logo_awi.setObjectName("label_logo_awi")
#         self.horizontalLayout_24.addWidget(self.label_logo_awi)
#         self.label_logo_ifam = QtWidgets.QLabel(self.frame_logos)
#         self.label_logo_ifam.setMaximumSize(QtCore.QSize(280, 16777215))
#         self.label_logo_ifam.setText("")
#         self.label_logo_ifam.setPixmap(QtGui.QPixmap(":/logos/logos/logo_ifam.png"))
#         self.label_logo_ifam.setScaledContents(True)
#         self.label_logo_ifam.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_logo_ifam.setObjectName("label_logo_ifam")
#         self.horizontalLayout_24.addWidget(self.label_logo_ifam)
#         self.verticalLayout_19.addWidget(self.frame_logos)
#         self.verticalLayout_11.addWidget(self.frame_about)
#         self.stackedWidget.addWidget(self.page_about)
#         self.horizontalLayout_15.addWidget(self.stackedWidget)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setBaseSize(QtCore.QSize(0, 10))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MarOMarker"))
        MainWindow.setProperty("user_id", _translate("MainWindow", "mm"))
        self.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.label_user_id.setText(_translate("MainWindow", "yj"))
        self.btn_imgSwitch.setText(_translate("MainWindow", "L"))
        self.comboBox_imgRemark.setItemText(0, _translate("MainWindow", "image remark..."))
        self.comboBox_imgRemark.setItemText(1, _translate("MainWindow", "low turbidity"))
        self.comboBox_imgRemark.setItemText(2, _translate("MainWindow", "medium turbidity"))
        self.comboBox_imgRemark.setItemText(3, _translate("MainWindow", "high turbidity"))
        self.comboBox_imgRemark.setItemText(4, _translate("MainWindow", "wrong illumination"))
        self.comboBox_imgRemark.setItemText(5, _translate("MainWindow", "without flashlight"))
        self.label_imgCount.setText(_translate("MainWindow", "01/48"))
        self.label_user_id_data_2.setText(_translate("MainWindow", "yj"))
        self.label_user_id_data.setText(_translate("MainWindow", "yj"))
        self.label_data.setText(_translate("MainWindow", "Data"))
        self.label_date_text.setText(_translate("MainWindow", "Date"))
        self.label_date.setText(_translate("MainWindow", "10.08.2020"))
        self.label_image_filter.setText(_translate("MainWindow", "Image filter"))
        self.comboBox_image_filter.setItemText(0, _translate("MainWindow", "Not checked"))
        self.comboBox_image_filter.setItemText(1, _translate("MainWindow", "Species undetermined"))
        self.comboBox_image_filter.setItemText(2, _translate("MainWindow", "All"))
        self.lineEdit_res_file.setPlaceholderText(_translate("MainWindow", "Path of result file..."))
        self.label_num_imgs.setText(_translate("MainWindow", "Numer of images"))
        self.lineEdit_img_dir.setText(_translate("MainWindow", "helge:// SVL/Remos-1/.../time-normized/"))
        self.lineEdit_img_dir.setPlaceholderText(_translate("MainWindow", "Directory to left and right images..."))
        self.btn_img_dir.setText(_translate("MainWindow", "Browse"))
        self.label_exp_id.setText(_translate("MainWindow", "Experiment ID"))
        self.label_img_dir.setText(_translate("MainWindow", "Image directory"))
        self.btn_apply_diverging_data_info.setText(_translate("MainWindow", "Apply"))
        self.lineEdit_img_prefix.setText(_translate("MainWindow", "TN_Exif_"))
        self.lineEdit_img_prefix.setPlaceholderText(_translate("MainWindow", "Prefix to select images..."))
        self.label_res_file.setText(_translate("MainWindow", "Result file"))
        self.label_num_imgs_text.setText(_translate("MainWindow", "48"))
        self.btn_res_file.setText(_translate("MainWindow", "Browse"))
        self.lineEdit_exp_id.setPlaceholderText(_translate("MainWindow", "ID of the experiment..."))
        self.label_img_prefix.setText(_translate("MainWindow", "Image Prefix"))
        self.btn_analyze.setText(_translate("MainWindow", "Analyze images"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.original), _translate("MainWindow", "Original table"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.summary), _translate("MainWindow", "Summarized table"))
        
        self.label_user_id_settings_2.setText(_translate("MainWindow", "yj"))
        self.label_user_id_settings.setText(_translate("MainWindow", "yj"))
        self.label_settings.setText(_translate("MainWindow", "Settings"))
        self.lineEdit_config_path.setToolTip(_translate("MainWindow", "Select a camera configuration file using the \"Load\" button on the right"))
        self.lineEdit_config_path.setPlaceholderText(_translate("MainWindow", "Path to camera configuration file..."))
        self.btn_load.setText(_translate("MainWindow", "Load"))
        self.btn_save.setText(_translate("MainWindow", "Save"))
        self.label_offset.setText(_translate("MainWindow", "Y-offset"))
        self.label_unit_offset.setText(_translate("MainWindow", "pixel"))
        self.label_distance_cameras.setText(_translate("MainWindow", "Distance between cameras"))
        self.label_unit_ditance_cameras.setText(_translate("MainWindow", "mm"))
        self.label_distance_chip_lense.setText(_translate("MainWindow", "Distance between chip and lense"))
        self.label_unit_chip_lense.setText(_translate("MainWindow", "pixel"))
        self.btn_apply_camera.setText(_translate("MainWindow", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_camera), _translate("MainWindow", "Camera"))
        self.label_nn.setText(_translate("MainWindow", "Neural Network"))
        self.lineEdit_nn.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        self.lineEdit_nn.setPlaceholderText(_translate("MainWindow", "Path to neural network model..."))
        self.btn_browse_nn.setText(_translate("MainWindow", "Browse"))
        self.btn_apply_nn.setText(_translate("MainWindow", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_neuralNet), _translate("MainWindow", "Neural Network"))
        self.btn_apply_species.setText(_translate("MainWindow", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_species), _translate("MainWindow", "Species"))
        self.label_distance_chip_lense_4.setText(_translate("MainWindow", "ID"))
        self.lineEdit_user_id.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        self.lineEdit_user_id.setPlaceholderText(_translate("MainWindow", "User ID..."))
        self.btn_apply_user.setText(_translate("MainWindow", "Apply"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user), _translate("MainWindow", "User"))
        
        # self.page_settings.label_user_id_settings_2.setText(_translate("MainWindow", "yj"))
        # self.page_settings.label_user_id_settings.setText(_translate("MainWindow", "yj"))
        # self.page_settings.label_settings.setText(_translate("MainWindow", "Settings"))
        # self.page_settings.lineEdit_config_path.setToolTip(_translate("MainWindow", "Select a camera configuration file using the \"Load\" button on the right"))
        # self.page_settings.lineEdit_config_path.setPlaceholderText(_translate("MainWindow", "Path to camera configuration file..."))
        # self.page_settings.btn_load.setText(_translate("MainWindow", "Load"))
        # self.page_settings.btn_save.setText(_translate("MainWindow", "Save"))
        # self.page_settings.label_offset.setText(_translate("MainWindow", "Y-offset"))
        # self.page_settings.label_unit_offset.setText(_translate("MainWindow", "pixel"))
        # self.page_settings.label_distance_cameras.setText(_translate("MainWindow", "Distance between cameras"))
        # self.page_settings.label_unit_ditance_cameras.setText(_translate("MainWindow", "mm"))
        # self.page_settings.label_distance_chip_lense.setText(_translate("MainWindow", "Distance between chip and lense"))
        # self.page_settings.label_unit_chip_lense.setText(_translate("MainWindow", "pixel"))
        # self.page_settings.btn_apply_camera.setText(_translate("MainWindow", "Apply"))
        # self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_camera), _translate("MainWindow", "Camera"))
        # self.page_settings.label_nn.setText(_translate("MainWindow", "Neural Network"))
        # self.page_settings.lineEdit_nn.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        # self.page_settings.lineEdit_nn.setPlaceholderText(_translate("MainWindow", "Path to neural network model..."))
        # self.page_settings.btn_browse_nn.setText(_translate("MainWindow", "Browse"))
        # self.page_settings.btn_apply_nn.setText(_translate("MainWindow", "Apply"))
        # self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_neuralNet), _translate("MainWindow", "Neural Network"))
        # self.page_settings.btn_apply_species.setText(_translate("MainWindow", "Apply"))
        # self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_species), _translate("MainWindow", "Species"))
        # self.page_settings.label_distance_chip_lense_4.setText(_translate("MainWindow", "ID"))
        # self.page_settings.lineEdit_user_id.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        # self.page_settings.lineEdit_user_id.setPlaceholderText(_translate("MainWindow", "User ID..."))
        # self.page_settings.btn_apply_user.setText(_translate("MainWindow", "Apply"))
        # self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_user), _translate("MainWindow", "User"))       
        

        
        self.label_user_id_handbook_2.setText(_translate("MainWindow", "yj"))
        self.label_user_id_handbook.setText(_translate("MainWindow", "yj"))
        self.label_settings_2.setText(_translate("MainWindow", "Handbook"))

        # self.label_user_id_about_2.setText(_translate("MainWindow", "yj"))
        # self.label_user_id_about.setText(_translate("MainWindow", "yj"))
#         self.label_settings_3.setText(_translate("MainWindow", "About MarOMarker"))
#         self.label_about_text.setText(_translate("MainWindow", "This software (MarOMarker) was developed in the scope of the Master\'s thesis <em>Semiautomatic Detection and Measurement of Marine Life on Underwater Stereoscopic Photographs Using a CNN</em> by Yvonne Jenniges. The thesis was a cooperation between the University of Bremen, the Alfred Wegener Institute and the Fraunhofer IFAM.\n"
# "<br>\n"
# "<br>\n"
# "<br>\n"
# "Yvonne Jenniges <br>\n"
# "yvonne.jenniges@gmx.de <br>\n"
# "<br>\n"
# "Supervisors <br>\n"
# "Prof. Dr.-Ing. Udo Frese <br>\n"
# "Prof. Dr. Philipp Fischer<br>\n"
# "<br>\n"
# "September 2020"))
        # @todo!! in PageAbout: add these somewhere       
        self.page_about.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_about.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))
        
        self.page_about.frame_controlBar.label_settings_3.setText(_translate("MainWindow", "About MarOMarker"))
        self.page_about.label_about_text.setText(_translate("MainWindow", "This software (MarOMarker) was developed in the scope of the Master\'s thesis <em>Semiautomatic Detection and Measurement of Marine Life on Underwater Stereoscopic Photographs Using a CNN</em> by Yvonne Jenniges. The thesis was a cooperation between the University of Bremen, the Alfred Wegener Institute and the Fraunhofer IFAM.\n"
"<br>\n"
"<br>\n"
"<br>\n"
"Yvonne Jenniges <br>\n"
"yvonne.jenniges@gmx.de <br>\n"
"<br>\n"
"Supervisors <br>\n"
"Prof. Dr.-Ing. Udo Frese <br>\n"
"Prof. Dr. Philipp Fischer<br>\n"
"<br>\n"
"September 2020"))
    
        # connect user button in topBar
        self.btn_user.clicked.connect(self.direct_to_user_settings)
        self.btn_user_data.clicked.connect(self.direct_to_user_settings)
        self.btn_user_handbook.clicked.connect(self.direct_to_user_settings)
        #self.btn_user_about.clicked.connect(self.direct_to_user_settings)
        
        self.page_about.frame_topBar.btn_user.clicked.connect(self.direct_to_user_settings)
    
        # connect menu buttons
        self.append_main_menu_to_button(self.page_about.frame_controlBar.btn_menu)
    

    def apply_settings_decision(self, answer):
        if answer.text() == "&Yes": 
            # apply the new values
            self.apply_all_settings()
        else:
            # restore all not applied values
            self.restore_old_settings()
    
    def apply_all_settings(self):
        self.camera_apply_btn_pressed()
        self.nn_apply_btn_pressed()
        self.user_apply_btn_pressed()
        self.species_apply_btn_pressed()
    
    def restore_old_settings(self):
        print(self.lineEdit_config_path_oldValue)
        
        if self.btn_apply_camera.isEnabled() == True:   
            self.spinBox_offset.setValue(self.spinBox_offset_oldValue)
            self.spinBox_distance_cameras.setValue(self.spinBox_distance_cameras_oldValue)
            self.spinBox_distance_chip_lense.setValue(self.spinBox_distance_chip_lense_oldValue)
            self.lineEdit_config_path.setText(self.lineEdit_config_path_oldValue)   
            self.btn_apply_camera.setEnabled(False)
        
        if self.btn_apply_nn.isEnabled() == True:
            self.lineEdit_nn.setText(self.lineEdit_nn_oldValue)
            self.btn_apply_nn.setEnabled(False)
            
        if self.btn_apply_species.isEnabled() == True:
            print("not implemented yet")
            self.btn_apply_species.setEnabled(False)
        
        if self.btn_apply_user.isEnabled() == True:
             self.lineEdit_user_id.setText(self.lineEdit_user_id_oldValue)
             self.btn_apply_user.setEnabled(False)
             
    # -------------------- species settings -------------------------------- # 
    def species_apply_btn_pressed(self):
        print("not implemented yet")
        
    def species_changed(self):
        self.btn_apply_species.setEnabled(True)
        
    # -------------------- user settings -------------------------------- #     
    def user_apply_btn_pressed(self):
         # disable apply btn
        self.btn_apply_user.setEnabled(False)

        # save the new value
        self.lineEdit_user_id_oldValue = self.lineEdit_user_id.text()    
        
        # update the userId in the top bar of the software (on every page)
        self.label_user_id.setText(self.lineEdit_user_id_oldValue)
        self.label_user_id_data.setText(self.lineEdit_user_id_oldValue)
        self.label_user_id_settings.setText(self.lineEdit_user_id_oldValue)
        self.label_user_id_handbook.setText(self.lineEdit_user_id_oldValue)
        
        # @todo
        self.label_user_id_about.setText(self.lineEdit_user_id_oldValue)
        
        # also update the dummy userIds to preserve the symmetry of the bar
        self.label_user_id_2.setText(self.lineEdit_user_id_oldValue)
        self.label_user_id_data_2.setText(self.lineEdit_user_id_oldValue)
        self.label_user_id_settings_2.setText(self.lineEdit_user_id_oldValue)
        self.label_user_id_handbook_2.setText(self.lineEdit_user_id_oldValue)
        
        # @todo
        self.label_user_id_about_2.setText(self.lineEdit_user_id_oldValue)
        
    
    def user_id_changed(self):
        self.btn_apply_user.setEnabled(True)
        
    def direct_to_user_settings(self):
        self.action_to_settings_page()
        self.tabWidget.setCurrentIndex(3)
    
    # -------------------- nn settings -------------------------------- # 
    def nn_apply_btn_pressed(self):
        # disable apply btn
        self.btn_apply_nn.setEnabled(False)

        # save the new value
        self.lineEdit_nn_oldValue = self.lineEdit_nn.text()
    
    def nn_path_changed(self):
        self.btn_apply_nn.setEnabled(True)
        
    def browse_for_nn(self):
        filename = QtWidgets.QFileDialog.getOpenFileName()
        self.lineEdit_nn.setText(filename[0])
        # @todo!! make use of NN
    
    # -------------------- camera settings -------------------------------- # 
    def camera_apply_btn_pressed(self):
        # disable apply btn
        self.btn_apply_camera.setEnabled(False)
        
        # save the new values of the spinBoxes and the file path
        self.lineEdit_config_path_oldValue = self.lineEdit_config_path.text()
        self.spinBox_offset_oldValue = self.spinBox_offset.value()
        self.spinBox_distance_cameras_oldValue = self.spinBox_distance_cameras.value()
        self.spinBox_distance_chip_lense_oldValue = self.spinBox_distance_chip_lense.value()
        

    def camera_spinBox_changed(self):
        # enable apply button
        self.btn_apply_camera.setEnabled(True)
        
        # remove file path (it is not valid for the new spinBox values anymore)
        self.lineEdit_config_path.setText("")
        
    
    def check_all_settings(self):
        # check if there are not applied settings
        if self.btn_apply_camera.isEnabled() == True or \
            self.btn_apply_nn.isEnabled() == True or \
            self.btn_apply_species.isEnabled() == True or \
            self.btn_apply_user.isEnabled() == True:
 
            # if not all changes to the settings were applied, ask the user what to do
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("Do you want to apply the changes to the settings?")
            msg.setWindowTitle("Settings changed")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msg.buttonClicked.connect(self.apply_settings_decision)
            msg.exec_()


    
    def load_config(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(filter = "*.csv")
        df = pd.read_csv(filename[0])
        
        # check format of file
        if(self.check_config_format(df)):           
            # set the respective spinBox values
            self.spinBox_offset.setValue(df["y-offset"][0])
            self.spinBox_distance_cameras.setValue(df["camera-distance"][0])
            self.spinBox_distance_chip_lense.setValue(df["chip-distance"][0])
            
            # display the path to the file in the respective lineEdit
            self.lineEdit_config_path.setText(filename[0])
            

        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("File Format Error")
            msg.setInformativeText('The given CSV file is not in the required format. Please make sure that it has the following columns with the correct data types:\n   "y-offset" (int64) \n   "camera-distance" (float64) \n   "chip-distance" (int64)')
            msg.setWindowTitle("Error")
            msg.exec_()
      
    def check_config_format(self, df_config):
        type_dict = dict(df_config.dtypes)

        # check if the necessary columns are present in the dataframe
        if "y-offset" in df_config.columns and "camera-distance" in df_config.columns and "chip-distance" in df_config.columns:
            # check if the dataformat is correct
            # if type_dict["y-offset"] == np.int64 and type_dict["camera-distance"] == np.float64 and type_dict["chip-distance"] == np.int64:
            #     return True
            # else:
            #     return False
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
      
        
    # -------------------- navigation actions -------------------------------- #    
    def action_to_home_page(self):  
        self.check_all_settings()
        self.stackedWidget.setCurrentIndex(0)

    def action_to_data_page(self):
        self.check_all_settings()
        self.stackedWidget.setCurrentIndex(1)
    
    def action_to_settings_page(self):
        self.check_all_settings()
        self.stackedWidget.setCurrentIndex(2)
        
    def action_to_handbook_page(self):
        self.check_all_settings()
        self.stackedWidget.setCurrentIndex(3)
        
    def action_to_about_page(self):
        self.check_all_settings()
        self.stackedWidget.setCurrentIndex(4)
        
        
    def append_main_menu_to_button(self, btn):
        # create the main menu
        menu = QtWidgets.QMenu()
        menu.addAction('Home', self.action_to_home_page)
        menu.addAction('Data', self.action_to_data_page)
        menu.addAction('Settings', self.action_to_settings_page)
        menu.addAction('Handbook', self.action_to_handbook_page)
        menu.addAction('About', self.action_to_about_page)
        
        # set the menu style
        menu.setStyleSheet("QMenu{background-color: rgb(200, 200, 200); border-radius: 3px; font:12pt 'Century Gothic'}\n"
                   "QMenu::item {background-color: transparent;}\n"
                   "QMenu::item:selected {background-color: rgb(0, 203, 221);}")
        
        # attach menu to button
        btn.setMenu(menu)
        
        # hide the right arrow of the menu
        btn.setStyleSheet( btn.styleSheet() + "QPushButton::menu-indicator {image: none;}");

    
    def setup_page_settings(self):
        self.page_settings = QtWidgets.QWidget()
        self.page_settings.setStyleSheet("/*-------------------------- line edit ------------------------*/\n"
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
        self.page_settings.setObjectName("page_settings")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_settings)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_settingsBar = QtWidgets.QFrame(self.page_settings)
        self.frame_settingsBar.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_settingsBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_settingsBar.setStyleSheet("")
        self.frame_settingsBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_settingsBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_settingsBar.setLineWidth(0)
        self.frame_settingsBar.setObjectName("frame_settingsBar")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_settingsBar)
        self.horizontalLayout_7.setContentsMargins(-1, 2, -1, 2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.btn_user_settings_2 = QtWidgets.QPushButton(self.frame_settingsBar)
        self.btn_user_settings_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user_settings_2.sizePolicy().hasHeightForWidth())
        self.btn_user_settings_2.setSizePolicy(sizePolicy)
        self.btn_user_settings_2.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user_settings_2.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user_settings_2.setStyleSheet("")
        self.btn_user_settings_2.setText("")
        self.btn_user_settings_2.setIconSize(QtCore.QSize(20,20))
        self.btn_user_settings_2.setObjectName("btn_user_settings_2")
        self.horizontalLayout_7.addWidget(self.btn_user_settings_2)
        self.label_user_id_settings_2 = QtWidgets.QLabel(self.frame_settingsBar)
        self.label_user_id_settings_2.setEnabled(True)
        self.label_user_id_settings_2.setStyleSheet("color:transparent")
        self.label_user_id_settings_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_settings_2.setObjectName("label_user_id_settings_2")
        self.horizontalLayout_7.addWidget(self.label_user_id_settings_2)
        spacerItem23 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem23)
        self.icon_settings = QtWidgets.QLabel(self.frame_settingsBar)
        self.icon_settings.setMinimumSize(QtCore.QSize(20, 20))
        self.icon_settings.setMaximumSize(QtCore.QSize(20, 20))
        self.icon_settings.setText("")
        self.icon_settings.setPixmap(QtGui.QPixmap(":/icons/icons/settings.png"))
        self.icon_settings.setScaledContents(True)
        self.icon_settings.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_settings.setObjectName("icon_settings")
        self.horizontalLayout_7.addWidget(self.icon_settings)
        spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem24)
        self.label_user_id_settings = QtWidgets.QLabel(self.frame_settingsBar)
        self.label_user_id_settings.setStyleSheet("color:white; font:10pt;")
        self.label_user_id_settings.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_settings.setObjectName("label_user_id_settings")
        self.horizontalLayout_7.addWidget(self.label_user_id_settings)
        self.btn_user_settings = QtWidgets.QPushButton(self.frame_settingsBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user_settings.sizePolicy().hasHeightForWidth())
        self.btn_user_settings.setSizePolicy(sizePolicy)
        self.btn_user_settings.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user_settings.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user_settings.setText("")
        self.btn_user_settings.setIcon(self.icon_loader.get_icon("icon1"))
        self.btn_user_settings.setIconSize(QtCore.QSize(20, 20))
        self.btn_user_settings.setObjectName("btn_user_settings")
        self.horizontalLayout_7.addWidget(self.btn_user_settings)
        self.verticalLayout_4.addWidget(self.frame_settingsBar)
        self.frame_controlBar_2 = QtWidgets.QFrame(self.page_settings)
        self.frame_controlBar_2.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_controlBar_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_controlBar_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_controlBar_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_controlBar_2.setLineWidth(0)
        self.frame_controlBar_2.setObjectName("frame_controlBar_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_controlBar_2)
        self.horizontalLayout_6.setContentsMargins(11, 5, 11, 5)
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.btn_menu_settings_2 = QtWidgets.QPushButton(self.frame_controlBar_2)
        self.btn_menu_settings_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu_settings_2.sizePolicy().hasHeightForWidth())
        self.btn_menu_settings_2.setSizePolicy(sizePolicy)
        self.btn_menu_settings_2.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings_2.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings_2.setText("")
        self.btn_menu_settings_2.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu_settings_2.setObjectName("btn_menu_settings_2")
        self.horizontalLayout_6.addWidget(self.btn_menu_settings_2)
        spacerItem25 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem25)
        spacerItem26 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem26)
        self.label_settings = QtWidgets.QLabel(self.frame_controlBar_2)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_settings.setFont(font)
        self.label_settings.setStyleSheet("color:black; font: bold;")
        self.label_settings.setObjectName("label_settings")
        self.horizontalLayout_6.addWidget(self.label_settings)
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem27)
        spacerItem28 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem28)
        
        self.btn_menu_settings = QtWidgets.QPushButton(self.frame_controlBar_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu_settings.sizePolicy().hasHeightForWidth())
        self.btn_menu_settings.setSizePolicy(sizePolicy)
        self.btn_menu_settings.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu_settings.setText("")
        self.btn_menu_settings.setIcon(self.icon9)
        self.btn_menu_settings.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu_settings.setObjectName("btn_menu_settings")
        self.append_main_menu_to_button(self.btn_menu_settings)
        self.horizontalLayout_6.addWidget(self.btn_menu_settings)
  
        self.verticalLayout_4.addWidget(self.frame_controlBar_2)
        self.frame_settings = QtWidgets.QFrame(self.page_settings)
        self.frame_settings.setStyleSheet("")
        self.frame_settings.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_settings.setObjectName("frame_settings")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_settings)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        
        
        #self.tabWidget = QtWidgets.QTabWidget(self.frame_settings)
        self.tabWidget = TabWidget(self.frame_settings)
        
        
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
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
        
        self.icon13 = QtGui.QIcon()
        pix = QtGui.QPixmap(":/icons/icons/camera.png")
        self.icon13.addPixmap(pix, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_camera, self.icon13, "")
        
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
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/icons/nn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_neuralNet, icon14, "")
        
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
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/icons/fish.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_species, icon15, "")
        
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
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/icons/user_b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_user, icon16, "")

        
        self.horizontalLayout_10.addWidget(self.tabWidget)
        self.verticalLayout_4.addWidget(self.frame_settings)
        self.stackedWidget.addWidget(self.page_settings)

        # initalize first values for variables on settings page
        self.lineEdit_config_path_oldValue = self.lineEdit_config_path.text()
        self.spinBox_offset_oldValue = self.spinBox_offset.value()
        self.spinBox_distance_cameras_oldValue = self.spinBox_distance_cameras.value()
        self.spinBox_distance_chip_lense_oldValue = self.spinBox_distance_chip_lense.value()
        self.lineEdit_nn_oldValue = self.lineEdit_nn.text()
        self.lineEdit_user_id_oldValue = self.lineEdit_user_id.text() 
        
        # connect signals and slots
        self.btn_load.clicked.connect(self.load_config)
        self.btn_save.clicked.connect(self.save_config)
        
        self.btn_apply_camera.clicked.connect(self.camera_apply_btn_pressed)
        self.spinBox_offset.valueChanged.connect(self.camera_spinBox_changed)
        self.spinBox_distance_cameras.valueChanged.connect(self.camera_spinBox_changed)
        self.spinBox_distance_chip_lense.valueChanged.connect(self.camera_spinBox_changed)
        
        self.btn_apply_user.clicked.connect(self.user_apply_btn_pressed)
        self.lineEdit_user_id.textEdited.connect(self.user_id_changed)
        
        self.btn_apply_nn.clicked.connect(self.nn_apply_btn_pressed)
        self.btn_browse_nn.clicked.connect(self.browse_for_nn)
        self.lineEdit_nn.textChanged.connect(self.nn_path_changed)
        
        self.btn_user_settings.clicked.connect(self.direct_to_user_settings)
                 

import ressources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

