from PyQt5 import QtCore, QtGui, QtWidgets

from Helpers import TopFrame, MenuFrame, get_icon
import time
from test_new_zoom import PhotoViewer

"""
Class to create the home page of the software.
"""
class PageHome(QtWidgets.QWidget):
    def __init__(self, parent=None):
        start_time = time.time()
        super(QtWidgets.QWidget, self).__init__(parent)
        
        # init UI and actions
        self.init_ui()
        self.init_actions()
       
        # slider parameters
        self.slider_max = self.photo_viewer.imageArea.width()*10
        self.slider_min = self.photo_viewer.imageArea.width()
        self.factor = 50*(self.slider_max - self.slider_min)/(self.slider_max)      

    def openZoomWidget(self):
        # show the zoom widget if it is not already visible
        if self.widget_zoom.isVisible():
            self.btn_zoom.setIcon(get_icon(":/icons/icons/glass.png")) 
            self.widget_zoom.hide()
        else:
            self.btn_zoom.setIcon(get_icon(":/icons/icons/glass_darkBlue.png")) 
            self.widget_zoom.show()
    
    def onZoomValueChanged(self, value):
        # determine the zoom factor and transform the photo of the photo_viewer
        scale = 1 + value*self.factor/100
        self.photo_viewer.imageArea.setTransform(self.photo_viewer.imageArea.transform().fromScale(scale, scale))

        # if thevalue is smaller 1, make the photo fill the photo_viewer image area
        if value < 1:
            self.photo_viewer.imageArea.resetTransform() 
            self.photo_viewer.imageArea.fitInView()
     
    def on_add_clicked(self):
        self.photo_viewer.imageArea.animal_painter.on_add_animal()
        self.updateAddRemoveIcons()
            
    def on_remove_clicked(self):
        self.photo_viewer.imageArea.animal_painter.on_remove_animal()
        self.updateAddRemoveIcons()

    def updateAddRemoveIcons(self):
        # adapt icon of the add button
        if self.photo_viewer.imageArea.animal_painter.is_add_mode_active:
            self.btn_add.setIcon(get_icon(":/icons/icons/plus_darkBlue.png"))
        else:
            self.btn_add.setIcon(get_icon(":/icons/icons/plus.png"))
            
        # adapt icon of the add button
        if self.photo_viewer.imageArea.animal_painter.is_remove_mode_active:
            self.btn_delete.setIcon(get_icon(":/icons/icons/bin_open_darkBlue.png"))
        else:
            self.btn_delete.setIcon(get_icon(":/icons/icons/bin_closed.png"))        
        
    def init_actions(self):
        # connecting signals and slots
        self.btn_add.clicked.connect(self.on_add_clicked)
        self.btn_delete.clicked.connect(self.on_remove_clicked)
        self.btn_next.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_next_animal)
        self.btn_previous.clicked.connect(self.photo_viewer.imageArea.animal_painter.on_previous_animal)
        self.btn_zoom.clicked.connect(self.openZoomWidget)
        self.slider_zoom.valueChanged.connect(self.onZoomValueChanged)
            
    def init_ui(self):
        # --- top bar  ------------------------------------------------------------------------------------------- #         
        # create the blue top bar
        self.frame_topBar = TopFrame(":/icons/icons/home_w.png", "frame_homeBar")     
        
        
        # --- control bar  ------------------------------------------------------------------------------------------- #         
        # create the cotrol bar containing the menu
        #self.frame_controlBar = MenuFrame("Handbook", "frame_controlBar_handbook")  
        #layout.addWidget(self.frame_controlBar) 
        # main frame
        self.frame_controlBar = QtWidgets.QFrame(self)
        self.frame_controlBar.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_controlBar.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_controlBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_controlBar.setLineWidth(0)
        self.frame_controlBar.setObjectName("frame_controlBar")
        
        # placeholder menu button to keep symmetry
        self.btn_menu2 = QtWidgets.QPushButton(self.frame_controlBar)
        self.btn_menu2.setEnabled(False)     
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu2.sizePolicy().hasHeightForWidth())  
        self.btn_menu2.setSizePolicy(sizePolicy)
        self.btn_menu2.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_menu2.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_menu2.setIconSize(QtCore.QSize(30, 30))
        self.btn_menu2.setObjectName("btn_menu2")

        # button for switching between left, right and both images
        self.btn_imgSwitch = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_imgSwitch.sizePolicy().hasHeightForWidth())
        self.btn_imgSwitch.setSizePolicy(sizePolicy)
        self.btn_imgSwitch.setMinimumSize(QtCore.QSize(60, 40))
        self.btn_imgSwitch.setMaximumSize(QtCore.QSize(60, 40))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.btn_imgSwitch.setFont(font)
        self.btn_imgSwitch.setObjectName("btn_imgSwitch")
        
        # button for opening a widget displaying filters
        self.btn_filter = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_filter.sizePolicy().hasHeightForWidth())
        self.btn_filter.setSizePolicy(sizePolicy)
        self.btn_filter.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_filter.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_filter.setIcon(get_icon(":/icons/icons/filter.png"))
        self.btn_filter.setIconSize(QtCore.QSize(30, 30))
        self.btn_filter.setObjectName("btn_filter")
        
        # combo box for image remarks
        self.comboBox_imgRemark = QtWidgets.QComboBox(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_imgRemark.sizePolicy().hasHeightForWidth())
        self.comboBox_imgRemark.setSizePolicy(sizePolicy)
        self.comboBox_imgRemark.setMinimumSize(QtCore.QSize(0, 40))
        self.comboBox_imgRemark.setMaximumSize(QtCore.QSize(16777215, 40))
        self.comboBox_imgRemark.setEditable(True)
        self.comboBox_imgRemark.setObjectName("comboBox_imgRemark")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        self.comboBox_imgRemark.addItem("")
        
        # button for opening a widget for zooming into photo
        self.btn_zoom = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_zoom.sizePolicy().hasHeightForWidth())
        self.btn_zoom.setSizePolicy(sizePolicy)
        self.btn_zoom.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_zoom.setMaximumSize(QtCore.QSize(40, 40))  
        self.btn_zoom.setIcon(get_icon(":/icons/icons/glass.png"))       
        self.btn_zoom.setIconSize(QtCore.QSize(30, 30))
        self.btn_zoom.setObjectName("btn_zoom")
        
        # button for activating the add-animal-mode
        self.btn_add = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)
        self.btn_add.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_add.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_add.setIcon(get_icon(":/icons/icons/plus.png"))
        self.btn_add.setIconSize(QtCore.QSize(30, 30))
        self.btn_add.setObjectName("btn_add")

        # button for switching to previous animal
        self.btn_previous = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_previous.sizePolicy().hasHeightForWidth())
        self.btn_previous.setSizePolicy(sizePolicy)
        self.btn_previous.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_previous.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_previous.setIcon(get_icon(":/icons/icons/arrow_left_small.png"))
        self.btn_previous.setIconSize(QtCore.QSize(30, 30))
        self.btn_previous.setObjectName("btn_previous")
        
        # playeholder button to keep symmetry 
        # self.btn_placeholder = QtWidgets.QPushButton(self.frame_controlBar)
        # self.btn_placeholder.setEnabled(False)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.btn_placeholder.sizePolicy().hasHeightForWidth())
        # self.btn_placeholder.setSizePolicy(sizePolicy)
        # self.btn_placeholder.setMinimumSize(QtCore.QSize(40, 40))
        # self.btn_placeholder.setMaximumSize(QtCore.QSize(40, 40))
        # self.btn_placeholder.setIconSize(QtCore.QSize(30, 30))
        # self.btn_placeholder.setObjectName("btn_placeholder")
        
        # button for switching to next animal
        self.btn_next = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_next.sizePolicy().hasHeightForWidth())
        self.btn_next.setSizePolicy(sizePolicy)
        self.btn_next.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_next.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_next.setIcon(get_icon(":/icons/icons/arrow_right_small.png"))
        self.btn_next.setIconSize(QtCore.QSize(30, 30))
        self.btn_next.setObjectName("btn_next")
        self.btn_next.setStyleSheet("margin-left: -100; margin-right:-100;")
        #self.btn_next.setMargins(10,10,0,0)
        
        # button to activate the remove-animals-mode
        self.btn_delete = QtWidgets.QPushButton(self.frame_controlBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy)
        self.btn_delete.setMinimumSize(QtCore.QSize(40, 40))
        self.btn_delete.setMaximumSize(QtCore.QSize(40, 40))
        self.btn_delete.setIcon(get_icon(":/icons/icons/bin_closed.png"))
        self.btn_delete.setIconSize(QtCore.QSize(30, 30))
        self.btn_delete.setObjectName("btn_delete")
        
        # button for undoing the last action
        # self.btn_undo = QtWidgets.QPushButton(self.frame_controlBar)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.btn_undo.sizePolicy().hasHeightForWidth())
        # self.btn_undo.setSizePolicy(sizePolicy)
        # self.btn_undo.setMinimumSize(QtCore.QSize(40, 40))
        # self.btn_undo.setMaximumSize(QtCore.QSize(40, 40))
        # self.btn_undo.setIcon(get_icon(":/icons/icons/undo.png"))
        # self.btn_undo.setIconSize(QtCore.QSize(30, 30))
        # self.btn_undo.setObjectName("btn_undo")
    
        # button for the menu
        self.btn_menu = QtWidgets.QPushButton(self.frame_controlBar)
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

        # horizontal spacers
        spacerItem2 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem4 = QtWidgets.QSpacerItem(334, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)    
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum) 
        spacerItem6 = QtWidgets.QSpacerItem(7, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)   
        
        spacerItem7 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        
        # layout
        layout_frame_controlBar = QtWidgets.QHBoxLayout(self.frame_controlBar)
        layout_frame_controlBar.setContentsMargins(11, 5, 11, 5)
        layout_frame_controlBar.setSpacing(4)
        layout_frame_controlBar.setObjectName("layout_frame_controlBar")

        # add widgets to layout 
        layout_frame_controlBar.addWidget(self.btn_menu2)
        layout_frame_controlBar.addItem(spacerItem2)
        layout_frame_controlBar.addWidget(self.btn_imgSwitch)
        layout_frame_controlBar.addWidget(self.btn_filter)
        layout_frame_controlBar.addWidget(self.comboBox_imgRemark)

        layout_frame_controlBar.addItem(spacerItem3)
        #layout_frame_controlBar.addWidget(self.btn_zoom)

        layout_frame_controlBar.addItem(spacerItem7)
        
        layout_frame_controlBar.addWidget(self.btn_zoom)
        layout_frame_controlBar.addItem(spacerItem7)
        layout_frame_controlBar.addWidget(self.btn_add)
        layout_frame_controlBar.addItem(spacerItem7)
        layout_frame_controlBar.addWidget(self.btn_previous)
        layout_frame_controlBar.addItem(spacerItem7)

        #layout_frame_controlBar.addWidget(self.btn_placeholder)
        layout_frame_controlBar.addWidget(self.btn_next)
        layout_frame_controlBar.addItem(spacerItem7)
        layout_frame_controlBar.addWidget(self.btn_delete)

        #layout_frame_controlBar.addWidget(self.btn_undo)
        layout_frame_controlBar.addItem(spacerItem4)
        layout_frame_controlBar.addItem(spacerItem5)
        layout_frame_controlBar.addItem(spacerItem6)
        layout_frame_controlBar.addWidget(self.btn_menu)        
        
        
        # --- photo viewer  ------------------------------------------------------------------------------------------- #        
        self.photo_viewer = PhotoViewer()
        self.photo_viewer.setObjectName("photo_viewer")
        
        
        # --- main widget ------------------------------------------------------------------------------------------- #  
        # set main widget properties
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("#btn_leftImg:hover, #btn_rightImg:hover{background-color:transparent;}")
        self.setObjectName("page_home")
        
        # main layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setObjectName("layout")
        
        # add widgets to main layout
        layout.addWidget(self.frame_topBar)
        layout.addWidget(self.frame_controlBar)
        layout.addWidget(self.photo_viewer)
        
        
        # --- zoom widget  ------------------------------------------------------------------------------------------- # 
        # create the zoom slider widget
        self.widget_zoom = QtWidgets.QWidget(self)
        self.widget_zoom.setMinimumSize(QtCore.QSize(200, 50))
        self.widget_zoom.setMaximumSize(QtCore.QSize(200, 50))
        self.widget_zoom.setObjectName("widget_zoom")
        self.widget_zoom.setAutoFillBackground(True)
        self.widget_zoom.setStyleSheet("background-color: rgb(200, 200, 200, 200); border: none; border-radius: 3px; ")
        
        self.slider_zoom = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_zoom.setMaximum(100)
        self.slider_zoom.setMinimum(0)
        self.slider_zoom.setStyleSheet("QSlider{background-color:transparent; } \n"
                                       "QSlider::groove:horizontal {backgroud:white; height: 4px; margin: 1px 0; border:none; border-radius: 3px;} \n"
                                       "QSlider::handle:horizontal {width: 10px; margin: -10px 0; background:  rgb(0, 203, 221); border-radius: 3px; border:none;}"
                                       "QSlider::handle:horizontal:hover{background: rgb(0, 160, 174);} \n"
                                       "QSlider::handle:horizontal:pressed{background:rgb(0,100,108);} \n"  
                                       "QSlider::add-page:horizontal {background: white;} \n"
                                       "QSlider::sub-page:horizontal {background: rgb(0, 160, 174);}")
     
        layout_zoom = QtWidgets.QHBoxLayout(self.widget_zoom)
        layout_zoom.setContentsMargins(11, 5, 11, 5)
        layout_zoom.setSpacing(4)
        layout_zoom.setObjectName("layout_zoom")
        layout_zoom.addWidget(self.slider_zoom)
        
        self.widget_zoom.hide()  
        self.placeZoomWidget()

        #print(f"page home init: {time.time() - start_time}")
     
    def mousePressEvent(self, event):
        self.updateGeometry()
        # hide the zoom widget if it is open and a click somewhere else is registered
        if self.widget_zoom.isVisible() and not self.widget_zoom.rect().contains(event.pos()):
            self.openZoomWidget()
            
        super().mousePressEvent(event)   
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.placeZoomWidget()
        print("resize")

        
    def placeZoomWidget(self):
        # reset position of zoom widget
        self.widget_zoom.move(0,0)
        
        # map the position of the zoom button to the local coordinate system of the zoom widget
        pos = self.btn_zoom.mapToGlobal(self.btn_zoom.rect().topLeft())
        p = self.widget_zoom.mapFromGlobal(pos)
        
        # move the zoom widget a bit below the button position and center it below the button
        self.widget_zoom.move(p + QtCore.QPoint(-self.widget_zoom.width()/2 + 20, 50))        