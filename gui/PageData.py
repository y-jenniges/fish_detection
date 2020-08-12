import time

from PyQt5 import QtCore, QtWidgets

from Helpers import TopFrame, MenuFrame

"""
Class to create the data page of the software.
"""
class PageData(QtWidgets.QFrame):
    
    def __init__(self, parent=None):
        start_time = time.time()
        
        super(QtWidgets.QFrame, self).__init__(parent)
    
        self.setObjectName("page_data")
        
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        
        # create the blue top bar
        self.frame_topBar = TopFrame(":/icons/icons/data_w.png", "frame_dataBar")     
        self.verticalLayout_5.addWidget(self.frame_topBar)
        
        # create the cotrol bar containing the menu
        self.frame_controlBar = MenuFrame("Data", "frame_controlBar_data")  
        self.verticalLayout_5.addWidget(self.frame_controlBar)        
        
        
        self.frame_data = QtWidgets.QFrame(self)
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
        
        #print(f"page data init: {time.time() - start_time}")