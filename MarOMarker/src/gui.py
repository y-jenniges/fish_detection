import time
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from Models import Models
import PageHome
import PageSettings
import PageAbout
import PageData
#import PageHandbook
from TableWindow import TableWindow
from WelcomeWindow import WelcomeWindow
"""
MarOMarker is a program for the semi-automatic annotation and 
measurement of marine organisms on stereoscopic images. 
Copyright(C) 2020  Yvonne Jenniges

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Cou can contact me by yvonne.jenniges@gmx.de
"""


class MarOMarker_MainWindow(QtWidgets.QMainWindow):
    """ 
    Main window class for MarOMarker. 
    
    Remark: 
        The stylesheets are partly taken and adapted from QT stylesheet 
        examples accessible at https://doc.qt.io/qt-5/stylesheet-examples.html
        (last access 15.10.2020)
        
    Attributes
    -----------
    settings : QSettings
        Used to store program settings for the next session. 
    models : Models
        Data models necessary for the workflow. 
    page_home : PageHome
        Home page of the software. 
    page_data : PageData
        Data page of the software.
    page_settings : PageSettings
        Settings page of the software.
    page_about : PageAbout
        About page of the software.
    """
    
    def __init__(self):
        """
        Init function of main window. It initializes UI, actions, data models
        and provides a variable (settings) for saving values for the next 
        session.
        """
        QtWidgets.QMainWindow.__init__(self)
        self.start_time = time.time()
                
        # variable to save settings outside program
        self.settings = QtCore.QSettings("MarOMarker", "MarOMarker")        
        
        # init data models
        self.models = Models()

        # init UI and actions
        self._initUi()
        self._initActions()

        # translate UI and set starting tabs
        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(1)
        self.window_table.tabWidget.setCurrentIndex(0)
        self.page_settings.tabWidget.setCurrentIndex(0)
        
        # restore values from previous session
        self.restorePreviousValues()
        
        # disable image directory selection options
        self.page_data.frame_data_information.setEnabled(False)

        print(self.settings.fileName())

    def showWelcome(self):
        """ Creates and shows the welcome screen. A user ID and camera config
        path have to be entered here before continuing. """
        # disable all other windows
        self.setEnabled(False)
        
        # create welcome window
        self.welcome_window = WelcomeWindow(self)
        
        # center welcome window on screen 
        qtRectangle = self.welcome_window.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.welcome_window.move(qtRectangle.topLeft())
        
        # put window to front
        self.welcome_window.raise_()
        self.welcome_window.activateWindow()
  
        self.welcome_window.show()

    def restorePreviousValues(self):
        """
        Tries to restore values from previous session (saved on closeEvent)
        """
        try:
            self.models.restoreValues(self.settings)
            self.resize(self.settings.value("windowSize"))
            self.move(self.settings.value("windowPosition"))
            self.window_table.resize(self.settings.value("tableWindowSize"))
            self.window_table.move(self.settings.value("tableWindowPosition"))
            
            self.page_settings.restoreValues(self.settings)
            self.page_data.restoreValues(self.settings)
        
        except:
            # check if any key exists, if not, show welcome screen 
            if not self.settings.contains("windowSize"):
                self.showWelcome()                
        
    # save some values and options when closing the program
    def closeEvent(self, event):
        """
        Saving some values when closing the program, like window size and 
        position, settings, secific model information. It also saves the 
        current image and updates the CSV table.

        Parameters
        ----------
        event : QEvent
            The event called when closing the program.
        """
        print("close event")
        self.settings.setValue("windowSize", self.size())
        self.settings.setValue("windowPosition", self.pos())
        self.settings.setValue("tableWindowSize", self.window_table.size())
        self.settings.setValue("tableWindowPosition", self.window_table.pos())
        
        self.page_settings.saveCurrentValues(self.settings)
        self.page_data.saveCurrentValues(self.settings)
        self.models.saveCurrentValues(self.settings)
        
        # save image data, update CSV output file
        index = self.page_home.photo_viewer.cur_image_index
        if index < len(self.page_home.photo_viewer.image_list):        
            cur_file_id = os.path.basename(
                self.page_home.photo_viewer.image_list[index])[:-6]
            output_dir = self.page_data.lineEdit_output_dir.text()
            res_file_name = self.getResultFileName()
            self.models.model_animals.exportToCsv(output_dir=output_dir,
                                                  filename=res_file_name,
                                                  file_id=cur_file_id)

        # close table window
        if self.window_table is not None:
            self.window_table.close()
        
        # close welcome window
        if self.window_welcome is not None:
            self.window_welcome.close()
        
    def retranslateUi(self):
        """
        Function to retranslate the UI and set the inital texts.
        """
        _translate = QtCore.QCoreApplication.translate
        
        # main window
        self.setWindowTitle(_translate("MainWindow", "MarOMarker"))
        
        # texts for table window
        self.window_table.setWindowTitle(_translate("MainWindow", "MarOMarker - Data Table"))
        self.window_table.btn_save_table.setText(_translate("MainWindow", "Save current table"))
        self.window_table.tabWidget.setTabText(self.window_table.tabWidget.indexOf(self.window_table.original), _translate("MainWindow", "Current table"))
        self.window_table.tabWidget.setTabText(self.window_table.tabWidget.indexOf(self.window_table.summary), _translate("MainWindow", "Summarized table"))
     
        # texts for home page
        self.page_home.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_home.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))
        self.page_home.btn_imgSwitch.setText(_translate("MainWindow", "L"))
        self.page_home.comboBox_imgRemark.lineEdit().setPlaceholderText(_translate("MainWindow", "Image remark..."))   
        self.page_home.photo_viewer.label_imgCount.setText(_translate("MainWindow", "01/48"))   
        self.page_home.comboBox_imgRemark.setToolTip(_translate("MainWindow", "Remark to the current image"))
        
        self.page_home.frame_topBar.btn_user.setToolTip(_translate("MainWindow", "User profile"))
        self.page_home.btn_filter.setToolTip(_translate("MainWindow", "Image filters"))
        self.page_home.btn_imgSwitch.setToolTip(_translate("MainWindow", "Switch to left, right or left-right image(s) (shortcuts: 1, 2, 3)"))
        self.page_home.btn_zoom.setToolTip(_translate("MainWindow", "Image zoom"))
        self.page_home.btn_add.setToolTip(_translate("MainWindow", "Add animal mode (O: head, X: tail, shortcut: +)"))
        self.page_home.btn_previous.setToolTip(_translate("MainWindow", "Previous animal (shortcut: a)"))
        self.page_home.btn_next.setToolTip(_translate("MainWindow", "Next animal (shortcut: d)"))
        self.page_home.btn_delete.setToolTip(_translate("MainWindow", "Remove animal mode (shortcut: -)"))
        self.page_home.btn_undo.setToolTip(_translate("MainWindow", "Undo last action"))
        self.page_home.photo_viewer.btn_previous_image.setToolTip(_translate("MainWindow", "Previous image (shortcut: left arrow)"))
        self.page_home.photo_viewer.btn_next_image.setToolTip(_translate("MainWindow", "Next image (shortcut: right arrow)"))
        #self.page_home.photo_viewer.btn_openImg.setToolTip(_translate("MainWindow", "Open image in separate window"))
        
        # texts for data page
        self.page_data.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_data.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))   
        self.page_data.frame_controlBar.label_settings_3.setText(_translate("MainWindow", "Data"))        
        self.page_data.label_date_text.setText(_translate("MainWindow", "Date"))
        self.page_data.label_image_filter.setText(_translate("MainWindow", "Image filter"))
        self.page_data.comboBox_image_filter.setItemText(0, _translate("MainWindow", "Not checked"))
        self.page_data.comboBox_image_filter.setItemText(1, _translate("MainWindow", "Species undetermined"))
        self.page_data.comboBox_image_filter.setItemText(2, _translate("MainWindow", "All"))
        self.page_data.lineEdit_output_dir.setPlaceholderText(_translate("MainWindow", "Path to output directory..."))
        self.page_data.label_num_imgs.setText(_translate("MainWindow", "#Images (left+right)"))
        self.page_data.lineEdit_img_dir.setPlaceholderText(_translate("MainWindow", "Directory to left and right images..."))
        self.page_data.btn_img_dir.setText(_translate("MainWindow", "Browse"))
        self.page_data.label_exp_id.setText(_translate("MainWindow", "Experiment ID"))
        self.page_data.label_img_dir.setText(_translate("MainWindow", "Image directory"))
        self.page_data.lineEdit_img_prefix.setPlaceholderText(_translate("MainWindow", "Prefix to select images..."))
        self.page_data.label_out_dir.setText(_translate("MainWindow", "Output directory"))
        self.page_data.label_num_imgs_text.setText(_translate("MainWindow", "0"))
        self.page_data.btn_out_dir.setText(_translate("MainWindow", "Browse"))
        self.page_data.lineEdit_exp_id.setPlaceholderText(_translate("MainWindow", "ID of the experiment..."))
        self.page_data.label_img_prefix.setText(_translate("MainWindow", "Image prefix"))
        self.page_data.label_data_selection.setText(_translate("MainWindow", "Select date and\noutput directory"))
        
        self.page_data.btn_nn_activation.setText(_translate("MainWindow", "Run neural network"))
        self.page_data.label_nn_activation.setText(_translate("MainWindow", "Run neural network"))
        self.page_data.label_nn_activation_text.setText(_translate("MainWindow", "   #Predicted images: "))
        self.page_data.label_nn_activation_number.setText(_translate("MainWindow", "0"))
        
        self.page_data.btn_pred_check.setText(_translate("MainWindow", "Check predictions on Home screen (L)"))
        self.page_data.label_prediction_check.setText(_translate("MainWindow", "Check predictions"))
        self.page_data.label_pred_check_text.setText(_translate("MainWindow", ""))#"   #Checked images: "))
        self.page_data.label_pred_check_number.setText(_translate("MainWindow", ""))#"0"))
        
        self.page_data.btn_rectify_match.setText(_translate("MainWindow", "Rectify and match"))
        self.page_data.label_rectify_match.setText(_translate("MainWindow", "Run rectification and matching"))
        self.page_data.label_rectify_match_text.setText(_translate("MainWindow", "   #Rectified images with matched animals: "))
        self.page_data.label_rectify_match_number.setText(_translate("MainWindow", "0"))

        self.page_data.btn_check_match.setText(_translate("MainWindow", "Check matching on Home screen (LR)"))
        self.page_data.label_check_match.setText(_translate("MainWindow", "Check matching"))
        self.page_data.label_check_match_text.setText(_translate("MainWindow", ""))#"   #Checked images: "))
        self.page_data.label_check_match_number.setText(_translate("MainWindow", ""))#"0"))
       
        self.page_data.btn_length_measurement.setText(_translate("MainWindow", "Calculate length"))
        self.page_data.label_length_measurement.setText(_translate("MainWindow", "Run length measurement"))
        self.page_data.label_length_measurement_text.setText(_translate("MainWindow", "   #Calculated images: "))
        self.page_data.label_length_measurement_number.setText(_translate("MainWindow", "0"))
        
        self.page_data.frame_topBar.btn_user.setToolTip(_translate("MainWindow", "User profile"))
        self.page_data.lineEdit_img_dir.setToolTip(_translate("MainWindow", "Directory, where left and right images are (automatically set by date selection)"))
        self.page_data.lineEdit_output_dir.setToolTip(_translate("MainWindow", "Output file is generated here"))
        self.page_data.lineEdit_img_prefix.setToolTip(_translate("MainWindow", "Optional prefix for images to search for"))
        self.page_data.lineEdit_exp_id.setToolTip(_translate("MainWindow", "ID of the experiment for which the photos were taken"))
        
        # texts for settings page
        self.page_settings.frame_top_bar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_settings.frame_top_bar.label_user_id.setText(_translate("MainWindow", "yj"))     
        self.page_settings.frame_control_bar.label_settings_3.setText(_translate("MainWindow", "Settings"))     
        self.page_settings.lineEdit_config_path.setToolTip(_translate("MainWindow", "Select a camera configuration file using the \"Load\" button on the right"))
        self.page_settings.lineEdit_config_path.setPlaceholderText(_translate("MainWindow", "Path to camera configuration file..."))    
        self.page_settings.btn_load.setText(_translate("MainWindow", "Load"))
        self.page_settings.btn_save.setText(_translate("MainWindow", "Save"))
        self.page_settings.label_offset.setText(_translate("MainWindow", "Y-offset"))
        self.page_settings.label_unit_offset.setText(_translate("MainWindow", "pixel"))
        self.page_settings.label_distance_cameras.setText(_translate("MainWindow", "Distance between cameras"))
        self.page_settings.label_unit_ditance_cameras.setText(_translate("MainWindow", "mm"))
        self.page_settings.label_distance_chip_lense.setText(_translate("MainWindow", "Distance between chip and lense"))
        self.page_settings.label_unit_chip_lense.setText(_translate("MainWindow", "pixel"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_camera), _translate("MainWindow", "Camera"))
        self.page_settings.label_nn.setText(_translate("MainWindow", "Neural network"))
        self.page_settings.lineEdit_nn.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        self.page_settings.lineEdit_nn.setPlaceholderText(_translate("MainWindow", "Path to neural network model..."))
        self.page_settings.btn_browse_nn.setText(_translate("MainWindow", "Browse"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_neuralNet), _translate("MainWindow", "Neural Network"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_species), _translate("MainWindow", "Species"))
        self.page_settings.label_user_id.setText(_translate("MainWindow", "ID"))
        self.page_settings.lineEdit_user_id.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        self.page_settings.lineEdit_user_id.setPlaceholderText(_translate("MainWindow", "User ID..."))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_user), _translate("MainWindow", "User"))       
        self.page_settings.btn_add_species.setText(_translate("MainWindow", "Add"))
        self.page_settings.btn_remove_species.setText(_translate("MainWindow", "Remove"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_other), _translate("MainWindow", "Other"))
        self.page_settings.label_root_dir.setText("Image root directory")
        self.page_settings.btn_browse_root_dir.setText(_translate("MainWindow", "Browse"))
        
        self.page_settings.frame_top_bar.btn_user.setToolTip(_translate("MainWindow", "User profile"))
        
        # texts for the handbook page
        # self.page_handbook.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        # self.page_handbook.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))
        # self.page_handbook.frame_controlBar.label_settings_3.setText(_translate("MainWindow", "Handbook"))
        
        # self.page_handbook.frame_top_bar.btn_user.setToolTip(_translate("MainWindow", "User profile"))
   
        # texts for the about page        
        self.page_about.frame_top_bar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_about.frame_top_bar.label_user_id.setText(_translate("MainWindow", "yj"))     
        self.page_about.frame_control_bar.label_settings_3.setText(_translate("MainWindow", "About MarOMarker"))
        self.page_about.label_about_text.setText(
            _translate("MainWindow", "This software (MarOMarker) was developed " + \
                       "in the scope of the Master\'s thesis <em>Semiautomatic " + \
                       "Detection and Measurement of Marine Life on Underwater " + \
                       "Stereoscopic Photographs Using a CNN</em> by " +\
                       "Yvonne Jenniges. The thesis was a cooperation between " +\
                       "the University of Bremen, the Alfred Wegener Institute " +\
                       "and the Fraunhofer IFAM.\n"
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
            
        self.page_about.frame_top_bar.btn_user.setToolTip(_translate("MainWindow", "User profile"))
 
    def _initUi(self):
        """
        Function to initialize the UI.
        """
        # set up main window properties
        self.setObjectName("MainWindow")
        self.setWindowIcon(QtGui.QIcon(':/icons/icons/fish.png'))    
        
        # some general properties
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        
        # create stacked widget
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setStyleSheet(
            "/* --- Control bars ---------------------------------------- */\n"
            "#frame_controlBar{background-color:rgb(200, 200, 200); }\n"
            "#frame_controlBar_data{background-color:rgb(200, 200, 200);}\n"
            "#frame_control_bar_settings{background-color:rgb(200, 200, 200);}\n"
            "#frame_control_bar_handbook{background-color:rgb(200, 200, 200);}\n"
            "#frame_control_bar_about{background-color:rgb(200, 200, 200); }\n"
            "\n"
            "/* --- Buttons --------------------------------------------- */\n"
            "QPushButton{\n"
            "    background-color:transparent;\n"
            "    outline:none;\n"
            "    border: none; \n"
            "    border-width: 0px;\n"
            "    border-radius: 3px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(0, 203, 221);\n"
            "}\n"
            "QPushButton:pressed {\n"
            "    background-color: rgb(0, 160, 174);\n"
            "}\n"
            "\n"
            "#btn_imgSwitch{\n"
            "    font: bold 14pt \"Century Gothic\";\n"
            "    color:black;\n"
            "    border-radius: 3px;\n"
            "    border: none; \n"
            "    background-color: rgb(150, 150, 150);\n"
            "    outline:none;\n"
            "}\n"
            "#btn_imgSwitch:hover{\n"
            "    background-color: rgb(0, 203, 221);\n"
            "}\n"
            "#btn_imgSwitch:pressed{\n"
            "    background-color: rgb(0, 160, 174);\n"
            "}\n"
            "#btn_user:hover,\n"
            "#btn_user_data:hover,\n"
            "#btn_user_settings:hover,\n"
            "#btn_user_handbook:hover,\n"
            "#btn_user_about:hover{\n"
            "    background-color: rgb(0, 160, 174);\n"
            "}\n"
            "#btn_user:pressed, \n"
            "#btn_user_data:pressed, \n"
            "#btn_user_settings:pressed,\n"
            "#btn_user_handbook:pressed,\n"
            "#btn_user_about:pressed{\n"
            "    background-color: rgb(0,100,108);\n"
            "}\n"
            "/* --- Comboboxes ------------------------------------------ */\n"
            "QComboBox QAbstractItemView {\n"
            "    border: none;\n"
            "    selection-background-color: rgb(0, 203, 221);\n"
            "    background-color:white;"
            "\n}"
            "QComboBox {\n"
            "    border-radius: 3px;\n"
            "    padding: 1px 18px 1px 10px;\n"
            "    background-color: white;\n"
            "    border:none;\n"
            "    font: 12pt \"Century Gothic\";\n"
            "}\n"
            "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "     stop: 0 rgb(200, 200, 200), stop: 0.8 rgb(255, 255, 255));\n"
            "}\n"
            "/* shift text when popup opens */ \n"
            "QComboBox:on { \n"
            "    padding-top: 3px;\n"
            "    padding-left: 4px;\n"
            "}\n"
            "QComboBox::drop-down {\n"
            "    subcontrol-origin: padding;\n"
            "    subcontrol-position: top right;\n"
            "    width: 40px;\n"
            "    border-left-width: 1px; \n"
            "    border-left-color: none; \n"
            "    border-left-style: solid; \n"
            "    border-top-right-radius: 3px; \n"
            "    border-bottom-right-radius: 3px;\n"
            "}\n"
            "QComboBox::down-arrow {\n"
            "    image: url(:/icons/icons/arrow_down.png);\n"
            "    padding-right:8px;\n"
            "}\n"
            "/* shift arrow when popup opens */ \n"
            "QComboBox::down-arrow:on { \n"
            "    top: 1px;\n"
            "    left: 1px;\n"
            "}\n"
            "#comboBox_menu, "
            "#comboBox_menu_2, "
            "#comboBox_menu_3, "
            "#comboBox_menu_4{\n"
            "    padding: 1px 1px 1px 1px;\n"
            "    background-color:transparent;\n"
            "    border:none;\n"
            "    border-radius: 0px;\n"
            "    color:transparent;\n"
            "    image: url(:/icons/icons/menu.png);\n"
            "}\n"
            "#comboBox_menu:on, "
            "#comboBox_menu_2:on, "
            "#comboBox_menu_3:on, "
            "#comboBox_menu_4:on{ \n"
            "    padding-top: 3px;\n"
            "    padding-left: 4px;\n"
            "}\n"
            "QComboBox#comboBox_menu::down-arrow {image: none;}\n"
            "QComboBox#comboBox_menu_2::down-arrow {image: none;}\n"
            "QComboBox#comboBox_menu_3::down-arrow {image: none;}\n"
            "QComboBox#comboBox_menu_4::down-arrow {image: none;}\n"
            "\n"
            "/*--- Labels -----------------------------------------------*/\n"
            "QLabel{\n"
            "    color:white;\n"
            "    font: 12pt \"Century Gothic\"\n"
            "}\n"
            "#label_settings, #label_data{\n"
            "    color:black;\n"
            "    font: bold 14pt \"Century Gothic\";\n"
            "}\n"
            "#label_imgCount{\n"
            "    color:black;\n"
            "    font: 10pt \"Century Gothic\";\n"
            "}\n"
            "/*--- Menu bars --------------------------------------------*/\n"
            "#frame_homeBar,\n"
            "#frame_dataBar,\n"
            "#frame_settings_bar,\n"
            "#frame_handbook_bar,\n"
            "#frame_about_bar{\n"
            "    background-color: rgb(0, 203, 221);"
            "}\n"
            "/*--- Double spin boxes ------------------------------------*/\n"
            "\n"
            "QDoubleSpinBox {\n"
            "    padding-right: 15; /* make room for the arrows */\n"
            "    /*border-image: url(:/images/frame.png) 4;*/\n"
            "    border-radius: 3px;\n"
            "	selection-background-color:rgb(0, 203, 221);\n"
            "	font:12pt \"Century Gothic\";\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button {\n"
            "    subcontrol-origin: border;\n"
            "    subcontrol-position: top right; \n"
            "    width: 16px; \n"
            "    border-image: url(:/icons/icons/arrow_up.png) 1;\n"
            "    border-width: 1px;\n"
            "	margin:2px;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button:hover {\n"
            "    border-image: url(:/icons/icons/arro"
                                    "w_up_blue.png) 1;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button:pressed {\n"
            "    border-image: url(:/icons/icons/arrow_up_darkblue.png) 1;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::down-button {\n"
            "    subcontrol-origin: border;\n"
            "    subcontrol-position: bottom right; /* position at bottom right corner */\n"
            "\n"
            "    width: 16px;\n"
            "    border-image: url(:/icons/icons/arrow_down.png) 1;\n"
            "    border-width: 1px;\n"
            "    border-top-width: 0;\n"
            "	 margin:2px;\n"
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
             
        print(f"gui init: {time.time() - self.start_time}")
        
        # home page
        self.page_home = PageHome.PageHome(self.models, self)
        self.stackedWidget.addWidget(self.page_home)
        print(f"home init: {time.time() - self.start_time}")
        
        # data page
        self.page_data = PageData.PageData(self.models, self)
        self.stackedWidget.addWidget(self.page_data)
        print(f"data init: {time.time() - self.start_time}")
        
        # settings page
        self.page_settings = PageSettings.PageSettings(self.models, self)
        self.stackedWidget.addWidget(self.page_settings)
        print(f"settings init: {time.time() - self.start_time}")
        
        # handbook page
        #self.page_handbook = PageHandbook.PageHandbook(self)
        #self.stackedWidget.addWidget(self.page_handbook)
        #print(f"handbook init: {time.time() - self.start_time}")
        
        # about page
        self.page_about = PageAbout.PageAbout(self)
        self.stackedWidget.addWidget(self.page_about)
        print(f"about init: {time.time() - self.start_time}")
        
        # set central widget and statusBar
        self.setCentralWidget(self.stackedWidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setEnabled(True)
        self.statusbar.setBaseSize(QtCore.QSize(0, 10))
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)    
     
        # create table window
        self.window_table = TableWindow(self.models, None)
        
        # create welcome window
        self.window_welcome = None
     
    def onImageDirChanged(self, text):
        """ Called when the image directory on the data page was changed. """
        self.page_home.photo_viewer.setImageDir(text)
        
    def onImagePrefixChanged(self, text):
        """ Called when the image prefix on the data page was changed. """
        self.page_home.photo_viewer.setImagePrefix(text)
        
    # def onImageEndingChanged(self, text): #(where used?)
    #     self.page_home.photo_viewer.setImageEnding(text)
        
    def onOutDirChanged(self, text):
        """ Called when the output directory on the data page was changed. """
        self.page_home.photo_viewer.setOutDir(text)
        
    def getResultFileName(self, isInProgress=False):
        """
        Defines the convention for the result file name. It is 
        results_yyyy_MM_STATE.csv, where _STATE is empty if the image editing 
        is finished or "inProgress".

        Parameters
        ----------
        isInProgress : bool, optional
            Indicates if the image editing is finished or not. The default is True.

        Returns
        -------
        name : string
            Name of the result file.

        """
        if hasattr(self, 'page_data'):
            month = self.page_data.calendarWidget.selectedDate().toString("yyyy_MM")
            state = "" if not isInProgress else "inProgress"
            name = "results_" + month + "_" +  state + ".csv"
            return name
        else:
            return None
           
    def _initActions(self):
        """ 
        Function to initialize actions.
        """
        # connect user button in top bars
        self.page_home.frame_topBar.btn_user.clicked.connect(self.directToUserSettings)  
        self.page_data.frame_topBar.btn_user.clicked.connect(self.directToUserSettings)      
        self.page_settings.frame_top_bar.btn_user.clicked.connect(self.directToUserSettings)
        #self.page_handbook.frame_topBar.btn_user.clicked.connect(self.directToUserSettings)
        self.page_about.frame_top_bar.btn_user.clicked.connect(self.directToUserSettings)
        
        # connect custom signals
        self.page_settings.userIdChanged.connect(self.updateUserIds)
        self.page_data.imageDirChanged.connect(self.onImageDirChanged)
        self.page_data.imagePrefixChanged.connect(self.onImagePrefixChanged)
        self.page_data.outputDirectoryChanged.connect(self.onOutDirChanged)
    
        # connect menu buttons
        self._appendMainMenuToButton(self.page_home.btn_menu)
        self._appendMainMenuToButton(self.page_data.frame_controlBar.btn_menu)
        self._appendMainMenuToButton(self.page_settings.frame_control_bar.btn_menu)
        self._appendMainMenuToButton(self.page_about.frame_control_bar.btn_menu)
        #self._appendMainMenuToButton(self.page_handbook.frame_controlBar.btn_menu)

    def updateUserIds(self, value):    
        """
        Function to update user ID in top bar of all pages.

        Parameters
        ----------
        value : string
            New user ID.
        """
        # update the userId in the top bar of the software (on every page)
        self.page_home.frame_topBar.label_user_id.setText(value)
        self.page_data.frame_topBar.label_user_id.setText(value)
        self.page_settings.frame_top_bar.label_user_id.setText(value)
        self.page_about.frame_top_bar.label_user_id.setText(value)
        #self.page_handbook.frame_topBar.label_user_id.setText(value) 
        
        # also update the dummy userIds to preserve the symmetry of the bar
        self.page_home.frame_topBar.label_user_id_2.setText(value)
        self.page_data.frame_topBar.label_user_id_2.setText(value)
        self.page_settings.frame_top_bar.label_user_id_2.setText(value)
        self.page_about.frame_top_bar.label_user_id_2.setText(value)
        #self.page_handbook.frame_topBar.label_user_id_2.setText(value)
        
    # -------------------- navigation actions -------------------------------- #    
    def directToUserSettings(self):
        """ Directs to user section of settings page. """
        self.directToSettingsPage()
        self.page_settings.tabWidget.setCurrentIndex(3)
        
    def directToHomePage(self): 
        """ Directs to home page. """
        self.stackedWidget.setCurrentIndex(0)

    def directToDataPage(self):
        """ Directs to data page. """
        self.stackedWidget.setCurrentIndex(1)
    
    def directToSettingsPage(self):
        """ Directs to settings page. """
        self.stackedWidget.setCurrentIndex(2)
        
    def directToHandbookPage(self):
        """ Directs to handbook page. """
        self.stackedWidget.setCurrentIndex(3)
        
    def directToABoutPage(self):
        """ Directs to about page. """
        self.stackedWidget.setCurrentIndex(3)
        
    def _onExitButton(self):
        """ Closes the program. """
        self.close()
        
    def _appendMainMenuToButton(self, btn):
        """
        Appends the menu to a given button. 

        Parameters
        ----------
        btn : QPushButton
            Button to append the menu to.
        """
        # create the main menu
        menu = QtWidgets.QMenu()
        menu.addAction("Home", self.directToHomePage)
        menu.addAction("Data", self.directToDataPage)
        menu.addAction("Settings", self.directToSettingsPage)
        #menu.addAction("Handbook", self.directToHandbookPage)
        menu.addAction("About", self.directToABoutPage)
        menu.addAction("Exit", self._onExitButton)
        
        # set the menu style
        menu.setStyleSheet("QMenu{background-color: rgb(200, 200, 200); "
                           "border-radius: 3px; font:12pt 'Century Gothic'}\n"
                           "QMenu::item {background-color: transparent;}\n"
                           "QMenu::item:selected {background-color: rgb(0, 203, 221);}")
        
        # attach menu to button
        btn.setMenu(menu)
        
        # hide the right arrow of the menu
        btn.setStyleSheet(btn.styleSheet() + 
                          "QPushButton::menu-indicator {image: none;}");


import ressources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow= MarOMarker_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

