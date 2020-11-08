import os
from PyQt5 import QtCore, QtWidgets, QtGui
"""
Helper functions and classes
"""   
    
def getIcon(ressource_path):
    """
    Gets an icon from a ressource path.

    Parameters
    ----------
    ressource_path : string
        Path to icon.

    Returns
    -------
    icon : QIcon
        Loaded icon.

    """
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(ressource_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    
    return icon

def displayErrorMsg(text, information, windowTitle):
    """
    Displays an error message with the given text.

    Parameters
    ----------
    text : string
        Error description.
    information : string
        More information about the error.
    windowTitle : string
        Title of error window.
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setInformativeText(information)
    msg.setWindowTitle(windowTitle)
    msg.setWindowIcon(QtGui.QIcon(':/icons/icons/fish.png')) 
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