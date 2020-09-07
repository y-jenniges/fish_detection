import time

from PyQt5 import QtCore, QtWidgets
import ntpath
from Helpers import TopFrame, MenuFrame
import glob

from Models import TableModel
import pandas as pd
# IMAGE_DIRECTORY_ROOT = "T:/'Center for Scientific Diving'/cosyna_data_all/SVL/Remos-1/"
IMAGE_DIRECTORY_ROOT = "C:/Users/yjenn/Documents/Uni/UniBremen/Semester4/MA/Coding/fish_detection/data/maritime_dataset_25/training_data_animals/"
# IMAGE_DIRECTORY = ""
# IMAGE_PREFIX = ""
# class TableModel(QtCore.QAbstractTableModel):
#     def __init__(self, data):
#         super(TableModel, self).__init__()
#         self._data = data

#     def data(self, index, role):
#         if role == QtCore.Qt.DisplayRole:
#             # See below for the nested-list data structure.
#             # .row() indexes into the outer list,
#             # .column() indexes into the sub-list
#             return self._data[index.row()][index.column()]

#     def rowCount(self, index):
#         # The length of the outer list.
#         return len(self._data)

#     def columnCount(self, index):
#         # The following takes the first sub-list, and returns
#         # the length (only works if all rows are an equal length)
#         return len(self._data[0])

class PageData(QtWidgets.QWidget): 
    """ Class to create the data page of the software """
    # define custom signals
    imageDirChanged = QtCore.pyqtSignal(str)
    resultFilePathChanged = QtCore.pyqtSignal(str)
    imagePrefixChanged = QtCore.pyqtSignal(str)
    experimentIdChanged = QtCore.pyqtSignal(str)
    
    def __init__(self, models, parent=None):
        start_time = time.time()       
        super(QtWidgets.QWidget, self).__init__(parent)
        # data models
        self.models = models
        
        # init UI, actions
        self.init_ui()
        self.init_actions()
        self.init_models()
        
        self.calenderSelectionChanged()
        

    def on_img_dir_edit_changed(self, text=None, updateVisuals=True):
        """ function to handle when the user changes the img_dir line edit """
        if text is None: text = self.lineEdit_img_dir.text()
        if not ntpath.exists(text): # check if path exists
            self.lineEdit_img_dir.setText("")
            print("The entered img dir is not a valid path.") # @todo error prompt
            
        self.updateNumImages()
        self.imageDirChanged.emit(self.lineEdit_img_dir.text())
        #self.on_img_dir_edit_changed(self.lineEdit_img_dir.text())
     
    def on_res_file_edit_changed(self):
        """ function to handle when the user changes the res_file line edit """
        # check if entered result file exists 
        # (else replace it by an empty string)
        if ntpath.exists(self.lineEdit_res_file.text()):
            pass
        else: 
            self.lineEdit_res_file.setText("")
            print(self.lineEdit_res_file.text())
            print("The enered res file is not a valid path.") # @todo error prompt
            
        self.resultFilePathChanged.emit(self.lineEdit_res_file.text())
        
    def on_prefix_edit_changed(self):
        """ function to handle when the user changes the image prefix line edit """
        self.imagePrefixChanged.emit(self.lineEdit_img_prefix.text())
        self.updateNumImages()    
    
    def on_exp_id_edit_changed(self):
        """ function to handle when the user changes the experiment id line edit """
        self.experimentIdChanged.emit(self.lineEdit_exp_id.text())
        
    def updateNumImages(self):
        """ function to check how many images are in the current 
        IMAGE_DIRECTORY and updates the display of this count """
        num_images = str(len(glob.glob(self.lineEdit_img_dir.text() + self.lineEdit_img_prefix.text() + "*_L.jpg")))
        self.label_num_imgs_text.setText(num_images)   
    
    def browseResultFile(self):
        """ function that opens a dialog for the user to select a result file 
        in csv format """
        filename = QtWidgets.QFileDialog.getOpenFileName(filter = "*.csv; *.xlsx")
        self.lineEdit_res_file.setText(filename[0])
        self.resultFilePathChanged.emit(self.lineEdit_res_file.text())
      
    def browseImageDir(self):
        """ function that opens a dialog for the user to select a directory 
        where the images are """
        filename = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Open Directory"), "", QtWidgets.QFileDialog.ShowDirsOnly)
        if len(filename) > 0: 
            if ntpath.exists(filename):
                self.lineEdit_img_dir.setText(filename + "/")
                self.on_img_dir_edit_changed(filename+"/")

    def updateImageDir(self):
        """ function to update the image directory according to the input 
        from the calender widget """
        date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
        directory = IMAGE_DIRECTORY_ROOT + date + "/Time-normized images/"
        
        # enable frame to manipulate data properties
        self.frame_data_information.setEnabled(True) # @todo always enabled
        
        # if directory does not exist, clear the image directory
        if not ntpath.exists(directory):
            self.lineEdit_img_dir.setText("")
        else:
            self.lineEdit_img_dir.setText(directory)
            self.on_img_dir_edit_changed(directory)
        
        # update the number of images
        self.updateNumImages() 

        # adapt experiment id  
        new_exp_id = "Spitzbergen " \
            + str(self.calendarWidget.selectedDate().year())     
        self.lineEdit_exp_id.setText(new_exp_id) 
        self.on_exp_id_edit_changed()
        
        # adapt result file path
        self.lineEdit_res_file.setText(directory
                                       +"result_"
                                       +str(date.rsplit("-",1)[0])
                                       +"neuralNet.csv")
        self.on_res_file_edit_changed() # has to be called manually since the 
        # lineEdit is only connected with "editingFinished" slot
        
        
    def calenderSelectionChanged(self):
        """ function to handle a change of the calender widget selection """
        # set the date label
        self.label_date.setText(self.calendarWidget.selectedDate() \
                                .toString("dd.MM.yyyy")) 
        
        # adapt image directory
        self.updateImageDir()
        
 
    def createFrameData(self):
        """ creates the data page UI """
        # data frame
        frame_data = QtWidgets.QFrame(self)
        frame_data.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        frame_data.setAccessibleName("")
        frame_data.setStyleSheet("QLabel{ \n"
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
"    color: black;"
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
"#btn_res_file, #btn_img_dir, #btn_analyze{\n"
"    background-color: rgb(200, 200, 200);\n"
"}\n"
"\n"
"\n"
"#btn_res_file:hover, #btn_img_dir:hover, #btn_analyze:hover{\n"
"  background-color: rgb(0, 203, 221);\n"
"}\n"
"\n"
"#btn_res_file:pressed, #btn_img_dir:pressed, #btn_analyze:pressed{\n"
"    background-color: rgb(0, 160, 174);\n"
"}")
        frame_data.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_data.setObjectName("frame_data")
        
        # layout for main data frame
        self.layout_frame_data = QtWidgets.QVBoxLayout(frame_data)
        self.layout_frame_data.setObjectName("layout_frame_data")
        
        # frame to display the data selection options
        self.frame_data_options = self.createFrameDataOptions(frame_data)
        
        # button to analye the images using the neural network
        self.btn_analyze = QtWidgets.QPushButton(frame_data)
        self.btn_analyze.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_analyze.setMaximumSize(QtCore.QSize(16777215, 40))
        self.btn_analyze.setObjectName("btn_analyze")      
        
        # frame to display the data table
        self.frame_table = self.createFrameTable(frame_data)
        
        # add widgets to layout
        self.layout_frame_data.addWidget(self.frame_data_options)
        self.layout_frame_data.addWidget(self.btn_analyze)
        self.layout_frame_data.addWidget(self.frame_table)    
        
        return frame_data

    def createFrameTable(self, frame_data):
        """ creates the frame showing the data table """
        # frame for displaying data table
        frame_table = QtWidgets.QFrame(frame_data)
        frame_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_table.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_table.setObjectName("frame_table")
        
        # layout
        self.layout_frame_table = QtWidgets.QVBoxLayout(frame_table)
        self.layout_frame_table.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_table.setSpacing(0)
        self.layout_frame_table.setObjectName("layout_frame_table")
        
        # tab widget to switch between the original table and the summary
        self.tabWidget_2 = QtWidgets.QTabWidget(frame_table)
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
        
        # widget to show the original table
        self.original = QtWidgets.QWidget(self)
        self.original.setObjectName("original") # @todo do i need this widget here?? cant  i just set the layout on the tab? or the table view directly?
        
        # layout to place the original table in
        self.layout_original_table = QtWidgets.QVBoxLayout(self.original)
        self.layout_original_table.setContentsMargins(0, 0, 0, 0)
        self.layout_original_table.setSpacing(0)
        self.layout_original_table.setObjectName("layout_original_table")
        
        # table view to display the original table
        self.tableView_original = QtWidgets.QTableView(self.original)
        self.tableView_original.setObjectName("tableView_original")
        self.layout_original_table.addWidget(self.tableView_original)
        







        # data = pd.read_excel("C:/Users/yjenn/Downloads/result_2015_08_step3.xlsx")
        # df = pd.DataFrame(data)
        
        # self.model = TableModel(df)
        # self.tableView_original.setModel(self.model)#models.model_animals)
            
        # widget to show the summary table
        self.summary = QtWidgets.QWidget(self)  # comment see above @todo
        self.summary.setObjectName("summary")
        
        # layout to place the summary table in
        self.layout_summary_table = QtWidgets.QVBoxLayout(self.summary)
        self.layout_summary_table.setContentsMargins(0, 0, 0, 0)
        self.layout_summary_table.setSpacing(0)
        self.layout_summary_table.setObjectName("layout_summary_table")
        
        # table view to display the summary table
        self.tableView_summary = QtWidgets.QTableView(self.summary)
        self.tableView_summary.setObjectName("tableView_summary")
        self.layout_summary_table.addWidget(self.tableView_summary)
                
        # add tabs (original table and summary) to tab widget
        self.tabWidget_2.addTab(self.original, "")
        self.tabWidget_2.addTab(self.summary, "")
        
        # add tab widget to layout of table frame
        self.layout_frame_table.addWidget(self.tabWidget_2)
        
        return frame_table
    
    def createFrameDataOptions(self, frame_data):
        """ created frame that contains all elements to adapt the 
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
        self.frame_data_selection = self.createFrameDataSelection(frame_data_options)
  
        # frame to display information derived from data selection
        self.frame_data_information = self.createFrameDataInformation(frame_data_options)
   
        # add widgets to layout
        self.layout_frame_data_options.addItem(spacerItem17)
        self.layout_frame_data_options.addWidget(self.frame_data_selection)
        self.layout_frame_data_options.addItem(spacerItem20)
        self.layout_frame_data_options.addWidget(self.frame_data_information)
        self.layout_frame_data_options.addItem(spacerItem22)
        
        return frame_data_options
    
    def createFrameDataSelection(self, frame_data_options):   
        """ creates frame with the main data selection options (calendar and 
        data filter combobox) """
        # data selection frame
        frame_data_selection = QtWidgets.QFrame(frame_data_options)
        frame_data_selection.setStyleSheet("")
        frame_data_selection.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_data_selection.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_data_selection.setObjectName("frame_data_selection")
        
        # layout 
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(frame_data_selection)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        
        # calender widget to select a date from 
        self.calendarWidget = QtWidgets.QCalendarWidget(frame_data_selection)
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
        self.label_date_text.setStyleSheet("")
        self.label_date_text.setObjectName("label_date_text")
        
        # spacer
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
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
        self.label_image_filter.setStyleSheet("")
        self.label_image_filter.setObjectName("label_image_filter")
                
        # spacer
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        # combo box to select a data filter
        self.comboBox_image_filter = QtWidgets.QComboBox(self.frame_img_filter)
        self.comboBox_image_filter.setMinimumSize(QtCore.QSize(250, 40))
        self.comboBox_image_filter.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_image_filter.setObjectName("comboBox_image_filter")
        self.comboBox_image_filter.addItem("")
        self.comboBox_image_filter.addItem("")
        self.comboBox_image_filter.addItem("")
        
        # add widgets to data filter frame
        self.layout_data_filter.addWidget(self.label_image_filter)
        self.layout_data_filter.addItem(spacerItem19)
        self.layout_data_filter.addWidget(self.comboBox_image_filter)
        
        
        # --- add widgets to data selection frame -------------------------- #
        self.verticalLayout_7.addWidget(self.calendarWidget)
        self.verticalLayout_7.addWidget(self.frame_date)        
        self.verticalLayout_7.addWidget(self.frame_img_filter)
        
        return frame_data_selection
        
    def createFrameDataInformation(self, frame_data_options):
        """ creates frame that shows image directory, result file path, 
        image prefix and experiment ID """
        # frame for data information
        frame_data_information = QtWidgets.QFrame(frame_data_options)
        frame_data_information.setEnabled(False)
        frame_data_information.setStyleSheet("")
        frame_data_information.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_data_information.setObjectName("frame_data_information")
        
        # layout
        self.gridLayout_5 = QtWidgets.QGridLayout(frame_data_information)
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        # line edit for the result file path
        self.lineEdit_res_file = QtWidgets.QLineEdit(frame_data_information)
        self.lineEdit_res_file.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_res_file.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_res_file.setObjectName("lineEdit_res_file")
        
        # label to display text "number of images"
        self.label_num_imgs = QtWidgets.QLabel(frame_data_information)
        self.label_num_imgs.setStyleSheet("")
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_img_dir.sizePolicy().hasHeightForWidth())
        self.btn_img_dir.setSizePolicy(sizePolicy)
        self.btn_img_dir.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_img_dir.setMaximumSize(QtCore.QSize(70, 40))
        self.btn_img_dir.setObjectName("btn_img_dir")
        
        # label to display text "experiment id"
        self.label_exp_id = QtWidgets.QLabel(frame_data_information)
        self.label_exp_id.setStyleSheet("")
        self.label_exp_id.setObjectName("label_exp_id")

        # label to display text "image directory"
        self.label_img_dir = QtWidgets.QLabel(frame_data_information)
        self.label_img_dir.setStyleSheet("")
        self.label_img_dir.setObjectName("label_img_dir")

        # line edit to set the image prefix
        self.lineEdit_img_prefix = QtWidgets.QLineEdit(frame_data_information)
        self.lineEdit_img_prefix.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_img_prefix.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_img_prefix.setObjectName("lineEdit_img_prefix")
        
        # label to display the text "result file"
        self.label_res_file = QtWidgets.QLabel(frame_data_information)
        self.label_res_file.setObjectName("label_res_file")
        
        # label to display the number of images in the current directory
        self.label_num_imgs_text = QtWidgets.QLabel(frame_data_information)
        self.label_num_imgs_text.setStyleSheet("padding-left: 10px;")
        self.label_num_imgs_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_num_imgs_text.setObjectName("label_num_imgs_text")
                
        # button to browse files for a result file
        self.btn_res_file = QtWidgets.QPushButton(frame_data_information)
        self.btn_res_file.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_res_file.setMaximumSize(QtCore.QSize(70, 40))
        self.btn_res_file.setObjectName("btn_res_file")
        
        # line edit for the experiment id
        self.lineEdit_exp_id = QtWidgets.QLineEdit(frame_data_information)
        self.lineEdit_exp_id.setMinimumSize(QtCore.QSize(150, 40))
        self.lineEdit_exp_id.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_exp_id.setObjectName("lineEdit_exp_id")
        
        # label to display text "image prefix"
        self.label_img_prefix = QtWidgets.QLabel(frame_data_information)
        self.label_img_prefix.setStyleSheet("")
        self.label_img_prefix.setObjectName("label_img_prefix")
        
        # spacer
        #spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # --- add widgets to data information frame ------------------------ #
        self.gridLayout_5.addWidget(self.lineEdit_res_file, 2, 1, 1, 1)
        self.gridLayout_5.addWidget(self.label_num_imgs, 5, 0, 1, 1)
        self.gridLayout_5.addWidget(self.lineEdit_img_dir, 1, 1, 1, 1)
        self.gridLayout_5.addWidget(self.btn_img_dir, 1, 2, 1, 1)
        self.gridLayout_5.addWidget(self.label_exp_id, 4, 0, 1, 1)
        self.gridLayout_5.addWidget(self.label_img_dir, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.lineEdit_img_prefix, 3, 1, 1, 1)
        self.gridLayout_5.addWidget(self.label_res_file, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.label_num_imgs_text, 5, 1, 1, 1)
        self.gridLayout_5.addWidget(self.btn_res_file, 2, 2, 1, 1)
        self.gridLayout_5.addWidget(self.lineEdit_exp_id, 4, 1, 1, 1)
        self.gridLayout_5.addWidget(self.label_img_prefix, 3, 0, 1, 1)
        #self.gridLayout_5.addItem(spacerItem21, 6, 1, 1, 1)
        
        return frame_data_information
    
    def init_ui(self):
        """ function to initialize the UI of data page """
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
        self.frame_data = self.createFrameData()
        
        # add widgets to data page
        self.layout_page_data.addWidget(self.frame_topBar)
        self.layout_page_data.addWidget(self.frame_controlBar)
        self.layout_page_data.addWidget(self.frame_data)
    
    def init_actions(self):
        """ function to initialize the actions on data page """
        self.calendarWidget.selectionChanged.connect(self.calenderSelectionChanged)
        
        self.btn_img_dir.clicked.connect(self.browseImageDir)
        self.btn_res_file.clicked.connect(self.browseResultFile)
        
        self.lineEdit_img_dir.editingFinished.connect(self.on_img_dir_edit_changed)
        
        self.lineEdit_res_file.editingFinished.connect(self.on_res_file_edit_changed)
        self.lineEdit_img_prefix.editingFinished.connect(self.on_prefix_edit_changed)
        self.lineEdit_exp_id.editingFinished.connect(self.on_exp_id_edit_changed)
  
    def init_models(self):
        self.tableView_original.setModel(self.models.model_animals)
        print("table view connected")
        
# --- functions for saving and restoring options --------------------------- # 
    def saveCurrentValues(self, settings):     
        """ saves current settings on data page fornext program start """
        settings.setValue("date", self.calendarWidget.selectedDate())       
        settings.setValue("dataFilter", self.comboBox_image_filter.currentIndex())
        settings.setValue("imgDir", self.lineEdit_img_dir.text())       
        settings.setValue("resultFile", self.lineEdit_res_file.text())
        settings.setValue("imgPrefix", self.lineEdit_img_prefix.text())
        settings.setValue("experimentId", self.lineEdit_exp_id.text())
        
    def restoreValues(self, settings):
        """ restores settings of page data from last program start """
        self.calendarWidget.setSelectedDate(settings.value("date"))
        self.comboBox_image_filter.setCurrentIndex(settings.value("dataFilter"))
        self.lineEdit_img_dir.setText(settings.value("imgDir"))
        self.lineEdit_res_file.setText(settings.value("resultFile"))
        self.lineEdit_img_prefix.setText(settings.value("imgPrefix"))
        self.lineEdit_exp_id.setText(settings.value("experimentId"))
        
        # do not update the visuals when setting the image directory, 
        # that would override the restored settings of the other fields
        self.on_img_dir_edit_changed(updateVisuals=False)
        self.on_res_file_edit_changed()
        self.on_prefix_edit_changed()
        self.on_exp_id_edit_changed()
        