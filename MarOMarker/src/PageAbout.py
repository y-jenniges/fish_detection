from PyQt5 import QtCore, QtGui, QtWidgets
from Helpers import TopFrame, MenuFrame


class PageAbout(QtWidgets.QWidget):
    """
    Class to create the about page of the software. It contains information 
    about the scope of the development of the software.
    
    Attributes
    ----------
    frame_top_bar : TopFrame
        Frame at the top of the window to display user ID and an icon
    frame_control_bar : MenuFrame
        Frame below the top bar to display controls of the page and the menu
    label_about_text : string
        Text for the about page
    """
    
    def __init__(self, parent=None):
        """
        Init function. Here, only UI components have to be defined. 
        (There are no actions to be defined here. The 
        interaction with the top and control bar are implemented in the 
        respective classes.)

        Parameters
        ----------
        parent : optional
            The default is None.
        """
        super(QtWidgets.QWidget, self).__init__(parent)          
        # --- elements in main widget --------------------------------------- #
        # top bar (the blue one on every page)
        self.frame_top_bar = TopFrame(":/icons/icons/fish_white.png",
                                     "frame_about_bar", self)
               
        # menu bar on about page
        self.frame_control_bar = MenuFrame("About MarOMarker",
                                          "frame_control_bar_about", self)
        
        # main content frame of about page
        self._frame_about = QtWidgets.QFrame(self)
        self._frame_about.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._frame_about.setFrameShadow(QtWidgets.QFrame.Raised)
        self._frame_about.setObjectName("frame_about")
        
        # --- frame for the logos ------------------------------------------- #
        self._frame_logos = QtWidgets.QFrame(self._frame_about)
        self._frame_logos.setMaximumSize(QtCore.QSize(16777215, 70))
        self._frame_logos.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._frame_logos.setFrameShadow(QtWidgets.QFrame.Raised)
        self._frame_logos.setObjectName("frame_logos")
        
        # uni Bremen logo
        # self._label_logo_uni = QtWidgets.QLabel(self._frame_logos)
        # self._label_logo_uni.setMaximumSize(QtCore.QSize(400, 16777215))
        # self._label_logo_uni.setText("")
        # self._label_logo_uni.setPixmap(QtGui.QPixmap(
        #     ":/logos/logos/logo_uniBremen.png"))
        # self._label_logo_uni.setScaledContents(True)
        # self._label_logo_uni.setAlignment(QtCore.Qt.AlignCenter)
        # self._label_logo_uni.setWordWrap(False)
        # self._label_logo_uni.setObjectName("label_logo_uni")
        
        # awi logo
        self._label_logo_awi = QtWidgets.QLabel(self._frame_logos)
        self._label_logo_awi.setMaximumSize(QtCore.QSize(200, 16777215))
        self._label_logo_awi.setText("")
        self._label_logo_awi.setPixmap(QtGui.QPixmap(
            ":/logos/logos/logo_awi.png"))
        self._label_logo_awi.setScaledContents(True)
        self._label_logo_awi.setAlignment(QtCore.Qt.AlignCenter)
        self._label_logo_awi.setObjectName("label_logo_awi")
        
        # ifam logo
        self._label_logo_ifam = QtWidgets.QLabel(self._frame_logos)
        self._label_logo_ifam.setMaximumSize(QtCore.QSize(280, 16777215))
        self._label_logo_ifam.setText("")
        self._label_logo_ifam.setPixmap(QtGui.QPixmap(
            ":/logos/logos/logo_ifam.png"))
        self._label_logo_ifam.setScaledContents(True)
        self._label_logo_ifam.setAlignment(QtCore.Qt.AlignCenter)
        self._label_logo_ifam.setObjectName("label_logo_ifam")
                     
        # layout for logo frame
        self._layout_logo_frame = QtWidgets.QHBoxLayout(self._frame_logos)
        self._layout_logo_frame.setContentsMargins(0, 0, 0, 0)
        self._layout_logo_frame.setSpacing(0)
        self._layout_logo_frame.setObjectName("layout_logo_frame")
        
        # add logos to layout
        #self._layout_logo_frame.addWidget(self._label_logo_uni)
        self._layout_logo_frame.addWidget(self._label_logo_awi)
        self._layout_logo_frame.addWidget(self._label_logo_ifam)
           
        # --- content of about page ----------------------------------------- #
        # text on about page
        self.label_about_text = QtWidgets.QLabel(self._frame_about)
        self.label_about_text.setStyleSheet(
            "color:black; \n"
            "padding:10px;\n"
            "background-color:rgb(230, 230, 230);\n"
            "border-radius:3px;")
        self.label_about_text.setScaledContents(False)
        self.label_about_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_about_text.setWordWrap(True)
        self.label_about_text.setObjectName("label_about_text")
        
        # vertical spacer
        _spacer_item = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        
        # layout of content frame
        self._layout_content_frame = QtWidgets.QVBoxLayout(self._frame_about)
        self._layout_content_frame.setObjectName("layout_content_frame")
        
        # add widgets to content frame layout
        self._layout_content_frame.addWidget(self.label_about_text)
        self._layout_content_frame.addItem(_spacer_item)
        self._layout_content_frame.addWidget(self._frame_logos)
            
        # --- main widget --------------------------------------------------- #
        self.setObjectName("page_about")
        
        # main layout
        self._layout_about_page = QtWidgets.QVBoxLayout(self)
        self._layout_about_page.setContentsMargins(0, 0, 0, 0)
        self._layout_about_page.setSpacing(0)
        self._layout_about_page.setObjectName("layout_page_about")
        
        # add widgets to _layout_about_page
        self._layout_about_page.addWidget(self.frame_top_bar)
        self._layout_about_page.addWidget(self.frame_control_bar)
        self._layout_about_page.addWidget(self._frame_about)
