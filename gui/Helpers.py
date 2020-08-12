from PyQt5 import QtCore, QtWidgets, QtGui
from varname import nameof


# """
# a central point to load all icons (for overview purposes)
# """
# class IconLoader():
#     def __init__(self):
#         self.icon_dict = {}
        
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/icons/icons/user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon1 = QtGui.QIcon()
        # icon1.addPixmap(QtGui.QPixmap(":/icons/icons/user_w.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap(":/icons/icons/filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon3 = QtGui.QIcon()
        # icon3.addPixmap(QtGui.QPixmap(":/icons/icons/glass.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
             
        # icon4 = QtGui.QIcon()
        # icon4.addPixmap(QtGui.QPixmap(":/icons/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon5 = QtGui.QIcon()
        # icon5.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_left_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon6 = QtGui.QIcon()
        # icon6.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_right_small.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon7 = QtGui.QIcon()
        # icon7.addPixmap(QtGui.QPixmap(":/icons/icons/bin_closed.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon8 = QtGui.QIcon()
        # icon8.addPixmap(QtGui.QPixmap(":/icons/icons/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon9 = QtGui.QIcon()
        # icon9.addPixmap(QtGui.QPixmap(":/icons/icons/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon10 = QtGui.QIcon()
        # icon10.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_left_big.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon11 = QtGui.QIcon()
        # icon11.addPixmap(QtGui.QPixmap(":/icons/icons/arrow_right_big.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon12 = QtGui.QIcon()
        # icon12.addPixmap(QtGui.QPixmap(":/icons/icons/open_image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
              
        # icon13 = QtGui.QIcon()
        # icon13.addPixmap(QtGui.QPixmap(":/icons/icons/camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # icon14 = QtGui.QIcon()
        # icon14.addPixmap(QtGui.QPixmap(":/icons/icons/nn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # icon15 = QtGui.QIcon()
        # icon15.addPixmap(QtGui.QPixmap(":/icons/icons/fish.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        # icon16 = QtGui.QIcon()
        # icon16.addPixmap(QtGui.QPixmap(":/icons/icons/user_b.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        

        # # define keys (names) and values (icons)
        # icon_names = [nameof(icon), nameof(icon1), nameof(icon2), nameof(icon3), nameof(icon4), nameof(icon5), nameof(icon6), nameof(icon7), nameof(icon8), nameof(icon9), nameof(icon10), nameof(icon11), nameof(icon12), nameof(icon13), nameof(icon14), nameof(icon15), nameof(icon16)]
        # icons = [icon, icon1, icon2, icon3, icon4, icon5, icon6, icon7, icon8, icon9, icon10 , icon11, icon12, icon13, icon14, icon15, icon16]
        
        # # fill dict
        # for i in range(len(icon_names)):
        #     self.icon_dict[icon_names[i]] = icons[i]


    # def get_icon(self, name):
    #     if name in self.icon_dict:
    #         return self.icon_dict[name]
    #     else:
    #         print(f"Error: There is no icon with name {name} defined.")
    #         return None
    
"""
Helper function to get an icon from a ressource path
"""       
def get_icon(ressource_path):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(ressource_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    
    return icon

"""
This class creates the blue frame which is at the top on every page. 
"""       
class TopFrame(QtWidgets.QFrame):
    """
    @pixmap_path: path to the pixmap for the icon in the center of the frame (indicating the functionality of the page)
    @frame_name: name of the created frame
    """
    def __init__(self, pixmap_path, frame_name, parent=None):
        super(QtWidgets.QFrame, self).__init__(parent)
    
        self.setMinimumSize(QtCore.QSize(0, 30))
        self.setMaximumSize(QtCore.QSize(16777215, 30))
        self.setStyleSheet("")
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLineWidth(0)
        self.setObjectName(frame_name)
        
        horizontalLayout_34 = QtWidgets.QHBoxLayout(self)
        horizontalLayout_34.setContentsMargins(-1, 2, -1, 2)
        horizontalLayout_34.setObjectName("horizontalLayout_34")
    
        # create a dummy button to keep the frame symmetric
        btn_user_about_2 = QtWidgets.QPushButton(self)
        btn_user_about_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btn_user_about_2.sizePolicy().hasHeightForWidth())
        btn_user_about_2.setSizePolicy(sizePolicy)
        btn_user_about_2.setMinimumSize(QtCore.QSize(25, 25))
        btn_user_about_2.setMaximumSize(QtCore.QSize(25, 25))
        btn_user_about_2.setStyleSheet("")
        btn_user_about_2.setText("")
        btn_user_about_2.setIconSize(QtCore.QSize(20, 20))
        btn_user_about_2.setObjectName("btn_user_about_2")
        horizontalLayout_34.addWidget(btn_user_about_2)
        
        # create a dummy label to keep the frame symmetric (it has to be a member variable such that the invisible text can be adapted. This will change the width of the label)
        self.label_user_id_2 = QtWidgets.QLabel(self)
        self.label_user_id_2.setEnabled(True)
        self.label_user_id_2.setStyleSheet("color:transparent")
        self.label_user_id_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id_2.setObjectName("label_user_id_2")
        horizontalLayout_34.addWidget(self.label_user_id_2)
        
        spacerItem56 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout_34.addItem(spacerItem56)
        
        # central icon on the frame (indicating the functionality of the page)
        # the icon is passed as a variable to this class
        icon = QtWidgets.QLabel(self)
        icon.setMinimumSize(QtCore.QSize(20, 20))
        icon.setMaximumSize(QtCore.QSize(20, 20))
        icon.setText("")
        icon.setPixmap(QtGui.QPixmap(pixmap_path))
        icon.setScaledContents(True)
        icon.setAlignment(QtCore.Qt.AlignCenter)
        icon.setObjectName("icon")
        horizontalLayout_34.addWidget(icon)
        
        spacerItem57 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout_34.addItem(spacerItem57)
        
        # label to display the Id of the current user
        self.label_user_id = QtWidgets.QLabel(self)
        self.label_user_id.setStyleSheet("color:white; font:10pt;")
        self.label_user_id.setTextFormat(QtCore.Qt.AutoText)
        self.label_user_id.setObjectName("label_user_id")
        horizontalLayout_34.addWidget(self.label_user_id)
        
        # button to switch directly to the user settings
        self.btn_user = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_user.sizePolicy().hasHeightForWidth())
        self.btn_user.setSizePolicy(sizePolicy)
        self.btn_user.setMinimumSize(QtCore.QSize(25, 25))
        self.btn_user.setMaximumSize(QtCore.QSize(25, 25))
        self.btn_user.setText("")
        self.btn_user.setIcon(get_icon(":/icons/icons/user_w.png"))
        self.btn_user.setIconSize(QtCore.QSize(20, 20))
        self.btn_user.setObjectName("btn_user")
        horizontalLayout_34.addWidget(self.btn_user)



"""
Frame that contains the menu button. It is similar on most pages, except the home page. 
The latter includes controls instead of a text in this bar.
"""
class MenuFrame(QtWidgets.QFrame):

    def __init__(self, central_text, frame_name, parent=None):
        super(QtWidgets.QFrame, self).__init__(parent)
        
        # set frame properties
        self.setMinimumSize(QtCore.QSize(0, 50))
        self.setMaximumSize(QtCore.QSize(16777215, 50))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setLineWidth(0)
        self.setObjectName(frame_name)
        horizontalLayout_31 = QtWidgets.QHBoxLayout(self)
        
        horizontalLayout_31.setContentsMargins(11, 5, 11, 5)
        horizontalLayout_31.setSpacing(4)
        horizontalLayout_31.setObjectName("horizontalLayout_31")
        
        # create dummy menu button to preserve the symmetry of the frame
        btn_menu_2 = QtWidgets.QPushButton(self)
        btn_menu_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(btn_menu_2.sizePolicy().hasHeightForWidth())
        btn_menu_2.setSizePolicy(sizePolicy)
        btn_menu_2.setMinimumSize(QtCore.QSize(40, 40))
        btn_menu_2.setMaximumSize(QtCore.QSize(40, 40))
        btn_menu_2.setText("")
        btn_menu_2.setIconSize(QtCore.QSize(30, 30))
        btn_menu_2.setObjectName("btn_menu_2")
        horizontalLayout_31.addWidget(btn_menu_2)
        
        spacerItem58 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout_31.addItem(spacerItem58)
        
        spacerItem59 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout_31.addItem(spacerItem59)
        
        # set central text, indicating the functionality of the page
        self.label_settings_3 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_settings_3.setFont(font)
        self.label_settings_3.setStyleSheet("color:black; font: bold 14pt;")
        self.label_settings_3.setObjectName("label_settings_3")
        horizontalLayout_31.addWidget(self.label_settings_3)
        
        spacerItem60 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout_31.addItem(spacerItem60)
        
        spacerItem61 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout_31.addItem(spacerItem61)
        
        # create the menu button
        self.btn_menu = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu.sizePolicy().hasHeightForWidth())
        self.btn_menu.setSizePolicy(sizePolicy)
        self.btn_menu.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu.setText("")
        self.btn_menu.setIcon(get_icon(":/icons/icons/menu.png"))
        self.btn_menu.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu.setObjectName("btn_menu")
        horizontalLayout_31.addWidget(self.btn_menu)












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
        
def append_main_menu_to_button(btn):
    # create the main menu
    menu = QtWidgets.QMenu()
    menu.addAction('Home', action_to_home_page)
    menu.addAction('Data', action_to_data_page)
    menu.addAction('Settings', action_to_settings_page)
    menu.addAction('Handbook', action_to_handbook_page)
    menu.addAction('About', action_to_about_page)
    
    # set the menu style
    menu.setStyleSheet("QMenu{background-color: rgb(200, 200, 200); border-radius: 3px; font:12pt 'Century Gothic'}\n"
               "QMenu::item {background-color: transparent;}\n"
               "QMenu::item:selected {background-color: rgb(0, 203, 221);}")
    
    # attach menu to button
    btn.setMenu(menu)
    
    # hide the right arrow of the menu
    btn.setStyleSheet( btn.styleSheet() + "QPushButton::menu-indicator {image: none;}");

