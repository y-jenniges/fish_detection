from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

import PageHome
import PageSettings
import PageAbout
import PageHandbook
import PageData
import Helpers 

import time

class MarOMarker_MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.start_time = time.time()
                
        # init UI and actions
        self.init_ui()
        self.init_actions()

        # translate UI and set starting tabs
        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(1)
        self.page_data.tabWidget_2.setCurrentIndex(0)
        self.page_settings.tabWidget.setCurrentIndex(0)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        
        # main window
        self.setWindowTitle(_translate("MainWindow", "MarOMarker"))
        
        # home page
        self.page_home.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_home.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))
        self.page_home.btn_imgSwitch.setText(_translate("MainWindow", "L"))
        self.page_home.comboBox_imgRemark.setItemText(0, _translate("MainWindow", "image remark..."))
        self.page_home.comboBox_imgRemark.setItemText(1, _translate("MainWindow", "low turbidity"))
        self.page_home.comboBox_imgRemark.setItemText(2, _translate("MainWindow", "medium turbidity"))
        self.page_home.comboBox_imgRemark.setItemText(3, _translate("MainWindow", "high turbidity"))
        self.page_home.comboBox_imgRemark.setItemText(4, _translate("MainWindow", "wrong illumination"))
        self.page_home.comboBox_imgRemark.setItemText(5, _translate("MainWindow", "without flashlight"))
        self.page_home.photo_viewer.label_imgCount.setText(_translate("MainWindow", "01/48"))     
        
        self.page_home.comboBox_imgRemark_dummy.setItemText(0, _translate("MainWindow", "image remark..."))
        self.page_home.comboBox_imgRemark_dummy.setItemText(1, _translate("MainWindow", "low turbidity"))
        self.page_home.comboBox_imgRemark_dummy.setItemText(2, _translate("MainWindow", "medium turbidity"))
        self.page_home.comboBox_imgRemark_dummy.setItemText(3, _translate("MainWindow", "high turbidity"))
        self.page_home.comboBox_imgRemark_dummy.setItemText(4, _translate("MainWindow", "wrong illumination"))
        self.page_home.comboBox_imgRemark_dummy.setItemText(5, _translate("MainWindow", "without flashlight"))
        
        # data page
        self.page_data.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_data.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))   
        self.page_data.frame_controlBar.label_settings_3.setText(_translate("MainWindow", "Data"))        
        self.page_data.label_date_text.setText(_translate("MainWindow", "Date"))
        self.page_data.label_image_filter.setText(_translate("MainWindow", "Image filter"))
        self.page_data.comboBox_image_filter.setItemText(0, _translate("MainWindow", "Not checked"))
        self.page_data.comboBox_image_filter.setItemText(1, _translate("MainWindow", "Species undetermined"))
        self.page_data.comboBox_image_filter.setItemText(2, _translate("MainWindow", "All"))
        self.page_data.lineEdit_res_file.setPlaceholderText(_translate("MainWindow", "Path of result file..."))
        self.page_data.label_num_imgs.setText(_translate("MainWindow", "Numer of images"))
        self.page_data.lineEdit_img_dir.setPlaceholderText(_translate("MainWindow", "Directory to left and right images..."))
        self.page_data.btn_img_dir.setText(_translate("MainWindow", "Browse"))
        self.page_data.label_exp_id.setText(_translate("MainWindow", "Experiment ID"))
        self.page_data.label_img_dir.setText(_translate("MainWindow", "Image directory"))
        self.page_data.btn_apply_diverging_data_info.setText(_translate("MainWindow", "Apply"))
        self.page_data.lineEdit_img_prefix.setPlaceholderText(_translate("MainWindow", "Prefix to select images..."))
        self.page_data.label_res_file.setText(_translate("MainWindow", "Result file"))
        self.page_data.label_num_imgs_text.setText(_translate("MainWindow", "0"))
        self.page_data.btn_res_file.setText(_translate("MainWindow", "Browse"))
        self.page_data.lineEdit_exp_id.setPlaceholderText(_translate("MainWindow", "ID of the experiment..."))
        self.page_data.label_img_prefix.setText(_translate("MainWindow", "Image Prefix"))
        self.page_data.btn_analyze.setText(_translate("MainWindow", "Analyze images"))    
        self.page_data.tabWidget_2.setTabText(self.page_data.tabWidget_2.indexOf(self.page_data.original), _translate("MainWindow", "Original table"))
        self.page_data.tabWidget_2.setTabText(self.page_data.tabWidget_2.indexOf(self.page_data.summary), _translate("MainWindow", "Summarized table"))
        
       
        # texts for settings page
        self.page_settings.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_settings.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))     
        self.page_settings.frame_controlBar.label_settings_3.setText(_translate("MainWindow", "Settings"))     
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
        self.page_settings.btn_apply_camera.setText(_translate("MainWindow", "Apply"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_camera), _translate("MainWindow", "Camera"))
        self.page_settings.label_nn.setText(_translate("MainWindow", "Neural Network"))
        self.page_settings.lineEdit_nn.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        self.page_settings.lineEdit_nn.setPlaceholderText(_translate("MainWindow", "Path to neural network model..."))
        self.page_settings.btn_browse_nn.setText(_translate("MainWindow", "Browse"))
        self.page_settings.btn_apply_nn.setText(_translate("MainWindow", "Apply"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_neuralNet), _translate("MainWindow", "Neural Network"))
        self.page_settings.btn_apply_species.setText(_translate("MainWindow", "Apply"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_species), _translate("MainWindow", "Species"))
        self.page_settings.label_user_id.setText(_translate("MainWindow", "ID"))
        self.page_settings.lineEdit_user_id.setToolTip(_translate("MainWindow", "Enter your user ID (first letter of first name + first letter of last name)"))
        self.page_settings.lineEdit_user_id.setPlaceholderText(_translate("MainWindow", "User ID..."))
        self.page_settings.btn_apply_user.setText(_translate("MainWindow", "Apply"))
        self.page_settings.tabWidget.setTabText(self.page_settings.tabWidget.indexOf(self.page_settings.tab_user), _translate("MainWindow", "User"))       
        self.page_settings.btn_add_species.setText(_translate("MainWindow", "Add"))
        self.page_settings.btn_remove_species.setText(_translate("MainWindow", "Remove"))
        
        # texts for the handbook page
        self.page_handbook.frame_topBar.label_user_id_2.setText(_translate("MainWindow", "yj"))
        self.page_handbook.frame_topBar.label_user_id.setText(_translate("MainWindow", "yj"))
        self.page_handbook.frame_controlBar.label_settings_3.setText(_translate("MainWindow", "Handbook"))
   
        # texts for the about page        
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
 
    def init_ui(self):
        # set up main window properties
        self.setObjectName("MainWindow")
        self.setWindowIcon(QtGui.QIcon(':/icons/icons/fish.png'))    
        self.resize(1200,900)
        self.showMaximized()  
        
        # some general properties
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        #self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)

        # create stacked widget
        self.stackedWidget = QtWidgets.QStackedWidget(self)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setStyleSheet("#frame_controlBar{background-color:rgb(200, 200, 200); }\n"
"#frame_controlBar_data{background-color:rgb(200, 200, 200); }\n"
"#frame_controlBar_settings{background-color:rgb(200, 200, 200); }\n"
"#frame_controlBar_handbook{background-color:rgb(200, 200, 200); }\n"
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
"/*-------------------------- double spin boxes ------------------------*/\n"
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
"    subcontrol-position: top right; /* position at the top right corner */\n"
"\n"
"    width: 16px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */\n"
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
        self.page_home = PageHome.PageHome(self)
        self.stackedWidget.addWidget(self.page_home)
        print(f"home init: {time.time() - self.start_time}")
        
        # data page
        self.page_data = PageData.PageData(self)
        self.stackedWidget.addWidget(self.page_data)
        print(f"data init: {time.time() - self.start_time}")
        
        # settings page
        self.page_settings = PageSettings.PageSettings(self)
        self.stackedWidget.addWidget(self.page_settings)
        print(f"settings init: {time.time() - self.start_time}")
        
        # handbook page
        self.page_handbook = PageHandbook.PageHandbook(self)
        self.stackedWidget.addWidget(self.page_handbook)
        print(f"handbook init: {time.time() - self.start_time}")
        
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

        
    def init_actions(self):   
        # connect user button in top bars
        self.page_home.frame_topBar.btn_user.clicked.connect(self.direct_to_user_settings)  
        self.page_data.frame_topBar.btn_user.clicked.connect(self.direct_to_user_settings)      
        self.page_settings.frame_topBar.btn_user.clicked.connect(self.direct_to_user_settings)
        self.page_handbook.frame_topBar.btn_user.clicked.connect(self.direct_to_user_settings)
        self.page_about.frame_topBar.btn_user.clicked.connect(self.direct_to_user_settings)
    
        # connect menu buttons
        self.append_main_menu_to_button(self.page_home.btn_menu)
        self.append_main_menu_to_button(self.page_data.frame_controlBar.btn_menu)
        self.append_main_menu_to_button(self.page_settings.frame_controlBar.btn_menu)
        self.append_main_menu_to_button(self.page_about.frame_controlBar.btn_menu)
        self.append_main_menu_to_button(self.page_handbook.frame_controlBar.btn_menu)
           
        # @todo implement listener pattern (mainwindow/all pages listen for  user apply button pressed) -> can adapt user id in top bars
        self.page_settings.btn_apply_user.clicked.connect(self.user_apply_btn_pressed)        


    # -------------------- settings -------------------------------- # 
    def apply_settings_decision(self, answer):
        if answer.text() == "&Yes": 
            # apply the new values
            self.apply_all_settings()
        else:
            # restore all not applied values
            self.page_settings.restore_old_settings()
    
    def apply_all_settings(self):
        self.page_settings.camera_apply_btn_pressed()
        self.page_settings.nn_apply_btn_pressed()
        self.user_apply_btn_pressed()
        self.page_settings.species_apply_btn_pressed()

    def check_all_settings(self):
        # check if there are not applied settings
        if self.page_settings.btn_apply_camera.isEnabled() == True or \
            self.page_settings.btn_apply_nn.isEnabled() == True or \
            self.page_settings.btn_apply_species.isEnabled() == True or \
            self.page_settings.btn_apply_user.isEnabled() == True:
 
            # if not all changes to the settings were applied, ask the user what to do
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText("Do you want to apply the changes to the settings?")
            msg.setWindowTitle("Settings changed")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msg.buttonClicked.connect(self.apply_settings_decision)
            msg.exec_()
    
        
    # -------------------- user settings -------------------------------- #     
    def user_apply_btn_pressed(self):
          # disable apply btn
        self.page_settings.btn_apply_user.setEnabled(False)

        # save the new value
        self.page_settings.lineEdit_user_id_oldValue = self.page_settings.lineEdit_user_id.text()    
        
        # update the userId in the top bar of the software (on every page)
        self.page_home.frame_topBar.label_user_id.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_data.frame_topBar.label_user_id.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_settings.frame_topBar.label_user_id.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_about.frame_topBar.label_user_id.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_handbook.frame_topBar.label_user_id.setText(self.page_settings.lineEdit_user_id_oldValue) 
        
        # also update the dummy userIds to preserve the symmetry of the bar
        self.page_home.frame_topBar.label_user_id_2.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_data.frame_topBar.label_user_id_2.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_settings.frame_topBar.label_user_id_2.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_about.frame_topBar.label_user_id_2.setText(self.page_settings.lineEdit_user_id_oldValue)
        self.page_handbook.frame_topBar.label_user_id_2.setText(self.page_settings.lineEdit_user_id_oldValue)
    

        
    def direct_to_user_settings(self):
        self.action_to_settings_page()
        self.page_settings.tabWidget.setCurrentIndex(3)
     
        
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


import ressources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow= MarOMarker_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

