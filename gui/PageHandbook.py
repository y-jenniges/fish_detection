from PyQt5 import QtWidgets

from Helpers import TopFrame, MenuFrame
import time
"""
Class to create the handbook page of the software.
"""
class PageHandbook(QtWidgets.QFrame):

    def __init__(self, parent=None):
        start_time = time.time()
        super(QtWidgets.QFrame, self).__init__(parent)
           
        # set widget property
        self.setObjectName("page_handbook")
        
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        
        # create the blue top bar
        self.frame_topBar = TopFrame(":/icons/icons/book.png", "frame_handbookBar")     
        self.verticalLayout_12.addWidget(self.frame_topBar)
        
        # create the cotrol bar containing the menu
        self.frame_controlBar = MenuFrame("Handbook", "frame_controlBar_handbook")  
        self.verticalLayout_12.addWidget(self.frame_controlBar)
        
        # create main frame for the handbook page
        self.frame_handbook = QtWidgets.QFrame(self)
        self.frame_handbook.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_handbook.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_handbook.setObjectName("frame_handbook")
        self.verticalLayout_12.addWidget(self.frame_handbook)
        
        #print(f"page handbook init: {time.time() - start_time}")