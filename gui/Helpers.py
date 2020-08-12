from PyQt5 import QtCore, QtWidgets, QtGui
from varname import nameof

# a central point to load all icons (for overview purposes)
class IconLoader():
    def __init__(self):
        self.icon_dict = {}
        
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/user_w.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # define keys (names) and values (icons)
        icon_names = [nameof(icon1), nameof(icon2), nameof(icon9)]
        icons = [icon1, icon2, icon9]
        
        # fill dict
        for i in range(len(icon_names)):
            self.icon_dict[icon_names[i]] = icons[i]

    def get_icon(self, name):
        if name in self.icon_dict:
            return self.icon_dict[name]
        else:
            print(f"Error: There is no icon with name {name} defined.")
            return None
        


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

