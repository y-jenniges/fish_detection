from PyQt5 import QtCore, QtGui, QtWidgets

from Helpers import TopFrame, MenuFrame
import time

"""
Class to create the about page of the software. It contains information about the development of the software.
"""
class PageAbout(QtWidgets.QWidget):
    """
    Initialize the UI for the About page. (There are no actions to define here. The interaction with the top and control bar are implemented in the respective classes.)
    """
    def __init__(self, parent=None):
        start_time = time.time()      
        super(QtWidgets.QWidget, self).__init__(parent)
          
        # --- elements in main widget --------------------------------------------------------------------- #
        # top bar (the blue one on every page)
        self.frame_topBar = TopFrame(":/icons/icons/fish_white.png", "frame_aboutBar", self)
               
        # menu bar on about page
        self.frame_controlBar = MenuFrame("About MarOMarker", "frame_controlBar_about", self)
        
        # main content frame of about page
        self.frame_about = QtWidgets.QFrame(self)
        self.frame_about.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_about.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_about.setObjectName("frame_about")
        
        
        # --- frame for the logos --------------------------------------------------------------------- #
        self.frame_logos = QtWidgets.QFrame(self.frame_about)
        self.frame_logos.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_logos.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_logos.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logos.setObjectName("frame_logos")
        
        # uni Bremen logo
        self.label_logo_uni = QtWidgets.QLabel(self.frame_logos)
        self.label_logo_uni.setMaximumSize(QtCore.QSize(400, 16777215))
        self.label_logo_uni.setText("")
        self.label_logo_uni.setPixmap(QtGui.QPixmap(":/logos/logos/logo_uniBremen.png"))
        self.label_logo_uni.setScaledContents(True)
        self.label_logo_uni.setAlignment(QtCore.Qt.AlignCenter)
        self.label_logo_uni.setWordWrap(False)
        self.label_logo_uni.setObjectName("label_logo_uni")      
        
        # awi logo
        self.label_logo_awi = QtWidgets.QLabel(self.frame_logos)
        self.label_logo_awi.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_logo_awi.setText("")
        self.label_logo_awi.setPixmap(QtGui.QPixmap(":/logos/logos/logo_awi.png"))
        self.label_logo_awi.setScaledContents(True)
        self.label_logo_awi.setAlignment(QtCore.Qt.AlignCenter)
        self.label_logo_awi.setObjectName("label_logo_awi")     
        
        # ifam logo
        self.label_logo_ifam = QtWidgets.QLabel(self.frame_logos)
        self.label_logo_ifam.setMaximumSize(QtCore.QSize(280, 16777215))
        self.label_logo_ifam.setText("")
        self.label_logo_ifam.setPixmap(QtGui.QPixmap(":/logos/logos/logo_ifam.png"))
        self.label_logo_ifam.setScaledContents(True)
        self.label_logo_ifam.setAlignment(QtCore.Qt.AlignCenter)
        self.label_logo_ifam.setObjectName("label_logo_ifam")
                     
        # layout for logo frame
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.frame_logos)
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        
        # add logos to layout
        self.horizontalLayout_24.addWidget(self.label_logo_uni)
        self.horizontalLayout_24.addWidget(self.label_logo_awi)
        self.horizontalLayout_24.addWidget(self.label_logo_ifam)
        
        
        # --- content of about page --------------------------------------------------------------------- #
        # text on about page
        self.label_about_text = QtWidgets.QLabel(self.frame_about)
        self.label_about_text.setStyleSheet("color:black; \n"
"padding:10px;\n"
"background-color:rgb(230, 230, 230);\n"
"border-radius:3px;")
        self.label_about_text.setScaledContents(False)
        self.label_about_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_about_text.setWordWrap(True)
        self.label_about_text.setObjectName("label_about_text")
        
        # vertical spacer
        spacerItem62 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        
        # layout of content frame
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.frame_about)    
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        
        # ad widgets to content frame layout
        self.verticalLayout_19.addWidget(self.label_about_text)
        self.verticalLayout_19.addItem(spacerItem62)
        self.verticalLayout_19.addWidget(self.frame_logos)      
        
        
        # --- main widget --------------------------------------------------------------------- #
        # set name
        self.setObjectName("page_about")
        
        # main layout
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        
        # add widgets to layout
        self.verticalLayout_11.addWidget(self.frame_topBar)
        self.verticalLayout_11.addWidget(self.frame_controlBar)
        self.verticalLayout_11.addWidget(self.frame_about)
        
        #print(f"page about init: {time.time() - start_time}")

