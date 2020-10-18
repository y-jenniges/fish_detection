import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from skimage.transform import resize
from scipy.optimize import linear_sum_assignment
from skimage.feature import peak_local_max
from keras.preprocessing.image import load_img, img_to_array
from PyQt5 import QtCore, QtWidgets, QtGui
import Losses

    
"""
Helper function to get an icon from a ressource path
"""       
def getIcon(ressource_path):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(ressource_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    
    return icon

def displayErrorMsg(text, information, windowTitle):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(information)
    msg.setWindowTitle(windowTitle)
    msg.exec_()

class ListViewDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent, listview):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.listview = listview
        self.item_height = 150

    def paint(self, painter, option, index):
        if index:
            icon_height = self.item_height - 20
            model = self.listview.model()
            
            # get icon and text of current entry
            item = model.itemFromIndex(index)
            data = index.model().data(index, QtCore.Qt.UserRole)

            icon = item.icon()
            text = item.text()

            if text != "Unidentified":
                painter.save()
                
                # set background color
                painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
                if option.state & QtWidgets.QStyle.State_Selected:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 203, 221)))
                elif option.state & QtWidgets.QStyle.State_MouseOver:
                    painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 203, 221, 60)))
                else:
                    painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
                painter.drawRect(option.rect)
                
                # rect for icon and text
                rect = option.rect
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
                #painter.setRenderHint(QtGui.QPainter.Antialiasing)
                middle = (rect.bottom() - rect.top()) / 2
                
                # icon position is slightly offset from borders of rect
                pos_icon = QtCore.QPoint(rect.left()+10, rect.top())
                
                # adjust the rect, such that text is drawn vertically centered 
                rect.adjust(0, middle-10, -10, 0)
                painter.drawRect(rect)
    
                # set pen and font
                pen = QtGui.QPen()
                pen.setColor(QtCore.Qt.black)
                painter.setPen(pen)
                painter.setFont(QtGui.QFont("Century Gothic", 12))
               
                # draw icon (as pixmap) and text
                painter.drawText(rect, QtCore.Qt.AlignRight, text)
                
                pixmap = icon.pixmap(QtCore.QSize(icon_height*50, icon_height*50)) # keep resolution large
                pixmap = pixmap.scaled(QtCore.QSize(icon_height, icon_height), QtCore.Qt.KeepAspectRatioByExpanding)
                offset = (self.item_height - pixmap.height())/2
                painter.drawPixmap(QtCore.QPoint(pos_icon.x(), pos_icon.y()+offset), pixmap)
                
                painter.restore()

        else:
            QtGui.QItemDelegate.paint(self, painter, option, index)

        painter.restore()
    
    def sizeHint(self, option, index):
        s = QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)
        
        if index.data() == "Unidentified":
            s.setHeight(0)
        else:
            s.setHeight(self.item_height)
        return s

class ComboboxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent, combobox):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.combobox = combobox
        self.item_height = 150

    def paint(self, painter, option, index):
        if index:
            icon_height = self.item_height - 20
            model = self.combobox.model()
            
            # get icon and text of current entry
            item = model.itemFromIndex(index)
            data = index.model().data(index, QtCore.Qt.UserRole)

            icon = item.icon()
            text = item.text()

            painter.save()
            
            # set background color
            painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
            if option.state & QtWidgets.QStyle.State_Selected:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 203, 221)))
            elif option.state & QtWidgets.QStyle.State_MouseOver:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 203, 221, 60)))
            else:
                painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
            painter.drawRect(option.rect)
            
            painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
            
            # rect for icon and text
            rect = option.rect
            middle = (rect.bottom() - rect.top()) / 2
            
            # icon position is slightly offset from borders of rect
            pos_icon = QtCore.QPoint(rect.left()+5, rect.top())
            
            # adjust the rect, such that text is drawn vertically centered 
            rect.adjust(0, middle-10, -10, 0)
            painter.drawRect(rect)

            # set pen and font
            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.black)
            painter.setPen(pen)
            painter.setFont(QtGui.QFont("Century Gothic", 10))
           
            # draw icon (as pixmap) and text
            painter.drawText(rect, QtCore.Qt.AlignRight, "  " + text)
            
            pixmap = icon.pixmap(QtCore.QSize(icon_height*50, icon_height*50)) # keep resolution large
            #pixmap = pixmap.scaled(QtCore.QSize(icon_height, icon_height), QtCore.Qt.KeepAspectRatioByExpanding)
            #pixmap = icon.pixmap(QtCore.QSize(200, 200))
            pixmap = pixmap.scaled(QtCore.QSize(140, 140), QtCore.Qt.KeepAspectRatio)
            offset = (self.item_height - pixmap.height())/2
            painter.drawPixmap(QtCore.QPoint(pos_icon.x(), pos_icon.y()+offset), pixmap)
            
            painter.restore()

        else:
            QtGui.QItemDelegate.paint(self, painter, option, index)

        painter.restore()
    
    def sizeHint(self, option, index):
        s = QtWidgets.QStyledItemDelegate.sizeHint(self, option, index)
        s.setHeight(self.item_height)
        return s
        
class TextImageItemWidget (QtWidgets.QWidget):
    def __init__ (self, imagePath, title=None, parent = None):
        super(TextImageItemWidget, self).__init__(parent)
         
        # the title is the name of the image
        self.imagePath = imagePath
        if title is None: 
            self.title = os.path.basename(imagePath).split('.')[0]
        else:
            self.title = title
        
        # create the line edit to display the text
        self.lineEdit_text = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_text.sizePolicy().hasHeightForWidth())
        self.lineEdit_text.setSizePolicy(sizePolicy)
        self.lineEdit_text.setMinimumSize(QtCore.QSize(400, 40))
        self.lineEdit_text.setMaximumSize(QtCore.QSize(16777215, 40))
        self.lineEdit_text.setReadOnly(False)
        self.setStyleSheet("background-color:transparent;")
        self.lineEdit_text.setObjectName("lineEdit_text")
        self.lineEdit_text.setText(self.title)
        
        # create the label to display the image      
        pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(self.imagePath))
        self.label_image = QtWidgets.QLabel(self)
        self.label_image.setPixmap(pixmap.scaled(QtCore.QSize(150,100), QtCore.Qt.KeepAspectRatio))      
    
        # a spacer between label and image
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # define the layout
        horizontalLayout = QtWidgets.QHBoxLayout(self)
        horizontalLayout.addWidget(self.lineEdit_text)
        horizontalLayout.addItem(spacer)
        horizontalLayout.addWidget(self.label_image)
        
        # connect the line edit to a slot
        self.lineEdit_text.editingFinished.connect(self.on_lineEdit_changed)

    def set_text(self, text):
        self.lineEdit_text.setText(text)
        self.title = text
        
    def on_lineEdit_changed(self):
        self.focusNextChild() # change focus
        self.title = self.lineEdit_text.text()
        
        

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
        self.btn_user.setIcon(getIcon(":/icons/icons/user_w.png"))
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
        self.btn_menu.setIcon(getIcon(":/icons/icons/menu.png"))
        self.btn_menu.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu.setObjectName("btn_menu")
        horizontalLayout_31.addWidget(self.btn_menu)


# --- neural network helpers ----------------------------------------------- #
def loadImage(fname, factor=32, rescale_range=True):
    "Loads an image as a h*w*3 numpy array in [-1, 1]"

    img = img_to_array(load_img(fname), dtype="uint8")
    
    # if image is still large, downscale it by 25%
    #from PIL import Image, ImageEnhance, ImageOps
    #from skimage.transform import resize
    if img.shape[0] > 2500:
        img = resize(img, (img.shape[0]*0.25, img.shape[1]*0.25))

    rest_x, rest_y = img.shape[0]%factor, img.shape[1]%factor
    if rest_x != 0:
        img = np.pad(img, ((0,factor-rest_x),(0, 0),(0,0)), 'constant', 
                     constant_values=0)
    if rest_y != 0:        
        img = np.pad(img, ((0,0),(0, factor-rest_y),(0,0)), 'constant', 
                     constant_values=0)
       
    if rescale_range:
        # image needs to be in [-1,1]
        img = np.asarray(img)
        img = 2.*img/np.max(img) - 1
    return img

def applyNnToImage(model, image):
    # predicted heatmap
    X = np.expand_dims(image, axis=0)
    yHat = model.predict(X)
    return yHat

def applyThresholdToHm(image, threshold=50):
    img_thr = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO)[1]
    return img_thr

def nonMaxSuppression(image, min_distance=20):
    coordinates = peak_local_max(image, min_distance=min_distance)
    return coordinates
    
def resizeHm(img, hm):
    factor = img.shape[0]//hm.shape[0]
    
    hmResized = np.repeat (hm, factor, axis=0) # y
    hmResized = np.repeat (hmResized, factor, axis=1) #x
    hmResized = np.clip (hmResized*2, 0, 1)
    hmResized = hmResized[:, :, np.newaxis]
        
    return hmResized

def findCoordinates(heatmap, threshold=50, radius=20):
    thr = applyThresholdToHm(heatmap, threshold)
    #plt.imshow(thr)
    #plt.show()
    coordinates = nonMaxSuppression(thr, radius)
    
    # remove coordinates whose x and y are closer than 10px
    df = pd.DataFrame(coordinates)
    df = df.sort_values(0, ignore_index=True)
    

    final_coords = df.copy() 
    
    for i in range(len(df)):
        for j in range(i, len(df)):
            if abs(df.iloc[i][0] - df.iloc[j][0]) < 10 \
            and abs(df.iloc[i][1] - df.iloc[j][1]) < 10 \
            and i != j and j in final_coords.index:
                #print(i,j)
                final_coords.drop(j, inplace=True)  
                
    # drop duplicates
    final_coords = pd.DataFrame(final_coords).drop_duplicates()
    
    # switch x and y
    final_coords = final_coords.reindex(columns=[1,0])
    
    final_coords = final_coords.to_numpy()
    
    return final_coords

def weightedEuclidean(x, y):
    a = 0.54 # put more weight on x-error
    b = 0.46 
    return np.sqrt(a*x*x + b*y*y)


def findHeadTailMatches(heads, tails):
    ht_distances = []
    
    # calculate distance from every head to every tail
    for i in range(len(heads)):
        if len(tails) > 0:
            head = heads[i]
            deltay = abs(np.array(tails)[:,0] - head[0])
            deltax = abs(np.array(tails)[:,1] - head[1])
        
            weighted_delta = weightedEuclidean(deltax, deltay)
            ht_distances.append(weighted_delta)
            
    # calculate matches minimizing the total distance
    ht_distances = np.array(ht_distances)
    matches = np.array([])
    if ht_distances.size != 0:
        head_assignment, tail_assignment = linear_sum_assignment(ht_distances)
        matches = np.array([(heads[head_assignment[i]], tails[tail_assignment[i]]) for i in range(len(tail_assignment))])
    return matches 

def scaleMatchCoordinates(matches, input_res, output_res):
    xfactor = output_res[0]/input_res[0]
    yfactor = output_res[1]/input_res[1]
    
    scaled_matches = []
    for m in matches:
        m = [[m[0][0]*xfactor, m[0][1]*yfactor], # scale head
             [m[1][0]*xfactor, m[1][1]*yfactor]] # scale tail
        scaled_matches.append(m)
    
    return np.array(scaled_matches)

def exportAnimalsToCsv():
    pass





# # -------------------- navigation actions -------------------------------- #    
# def action_to_home_page(self):  
#     self.check_all_settings()
#     self.stackedWidget.setCurrentIndex(0)

# def action_to_data_page(self):
#     self.check_all_settings()
#     self.stackedWidget.setCurrentIndex(1)

# def action_to_settings_page(self):
#     self.check_all_settings()
#     self.stackedWidget.setCurrentIndex(2)
    
# def action_to_handbook_page(self):
#     self.check_all_settings()
#     self.stackedWidget.setCurrentIndex(3)
    
# def action_to_about_page(self):
#     self.check_all_settings()
#     self.stackedWidget.setCurrentIndex(4)
        
# def append_main_menu_to_button(btn):
#     # create the main menu
#     menu = QtWidgets.QMenu()
#     menu.addAction('Home', action_to_home_page)
#     menu.addAction('Data', action_to_data_page)
#     menu.addAction('Settings', action_to_settings_page)
#     menu.addAction('Handbook', action_to_handbook_page)
#     menu.addAction('About', action_to_about_page)
    
#     # set the menu style
#     menu.setStyleSheet("QMenu{background-color: rgb(200, 200, 200); border-radius: 3px; font:12pt 'Century Gothic'}\n"
#                "QMenu::item {background-color: transparent;}\n"
#                "QMenu::item:selected {background-color: rgb(0, 203, 221);}")
    
#     # attach menu to button
#     btn.setMenu(menu)
    
#     # hide the right arrow of the menu
#     btn.setStyleSheet( btn.styleSheet() + "QPushButton::menu-indicator {image: none;}");

