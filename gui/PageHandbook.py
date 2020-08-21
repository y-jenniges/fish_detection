from PyQt5 import QtWidgets
from Helpers import TopFrame, MenuFrame
import time

"""
Class to create the handbook page of the software.
"""
class PageHandbook(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget, self).__init__(parent)
           
        # init UI and actions
        self.init_ui()
        self.init_actions()
 
    def init_ui(self):
        # set widget property
        self.setObjectName("page_handbook")
        
        self.layout_page_handbook = QtWidgets.QVBoxLayout(self)
        self.layout_page_handbook.setContentsMargins(0, 0, 0, 0)
        self.layout_page_handbook.setSpacing(0)
        self.layout_page_handbook.setObjectName("layout_page_handbook")
        
        # create the blue top bar
        self.frame_topBar = TopFrame(":/icons/icons/book.png", "frame_handbookBar", self)     
            
        # create the cotrol bar containing the menu
        self.frame_controlBar = MenuFrame("Handbook", "frame_controlBar_handbook", self)      
        
        # create main frame for the handbook page
        self.frame_handbook = QtWidgets.QFrame(self)
        self.frame_handbook.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_handbook.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_handbook.setObjectName("frame_handbook")
             
        # add widgets to layout
        self.layout_page_handbook.addWidget(self.frame_topBar)
        self.layout_page_handbook.addWidget(self.frame_controlBar)
        self.layout_page_handbook.addWidget(self.frame_handbook)        
        
    def init_actions(self):
        pass