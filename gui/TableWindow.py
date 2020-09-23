from PyQt5 import QtCore, QtWidgets, QtGui

class TableWindow(QtWidgets.QMainWindow):
    """
    MainWindow class to display the current data table and to offer the 
    option to save the table.
    """
    def __init__(self, models, parent=None):
        """
        Init function. Initalizes the GUI and actions for this window.

        Parameters
        ----------
        models : Models
            Contains all necessary data models, i.e. models for the animal 
            species, group, remark, as well as image remark and the general
            animal data from the result table.
        parent : optional
            The default is None.

        """
        super(TableWindow, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon(':/icons/icons/fish.png'))  
        self.setObjectName("window_table")
        
        # data models
        self.models = models
        
        # central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setStyleSheet( 
            "/*------------------------ tab widget -----------------------*/\n"
            "QTabWidget{font: 10pt \"Century Gothic\";}\n"
            "\n"
            "QTabWidget::pane { /* frame of tab widget */\n"
            "    border:None;\n"
            "}\n"
            "QTabBar::tab {\n"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "                                stop: 0 #E1E1E1, \n"
            "                                stop: 0.4 #DDDDDD,\n"
            "                                stop: 0.5 #D8D8D8, \n"
            "                                stop: 1.0 #D3D3D3);\n"
            "    border: None;\n"
            "    min-width: 10ex;\n"
            "    padding: 5px;\n"
            "    padding-bottom:5px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected, QTabBar::tab:hover {\n"
            "    background: white;\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected {\n"
            "    border-color: #9B9B9B;\n"
            "    border-bottom-color: #C2C7CB; /* same as pane color */\n"
            "}\n"
            "\n"
            "QTabBar::tab:!selected {\n"
            "    margin-top:0px; /* non-selected tabs smaller */\n"
            "}\n"
            "/*------------------------ table view -----------------------*/\n"
            "QTableView{\n"
            "    font: 10pt \"Century Gothic\";\n"
            "    background-color: white;  \n"
            "    border-radius:3px;\n"
            "    color: black;"
            "}\n"
            "/*------------------------- buttons -------------------------*/\n"
            "QPushButton{\n"
            "    font: 10pt \"Century Gothic\";\n"
            "    border:none; border-radius:3px;\n"
            "    padding:10; background-color: rgb(200, 200, 200);"
            "}\n"
            "QPushButton:hover{background-color: rgb(0, 203, 221);}\n"
            "QPushButton:pressed{background-color: rgb(0, 160, 174);}\n"
            "")
        
        # layout
        self.layout_win_table = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout_win_table.setContentsMargins(11, 11, 11, 11)
        self.layout_win_table.setSpacing(7)
        self.layout_win_table.setObjectName("layout_win_table")
        
        # button to save the current table
        self.btn_save_table = QtWidgets.QPushButton(self.central_widget)
        self.btn_save_table.clicked.connect(self.onBtnSaveTable)
        
        # frame showing the table
        self.frame_table = self._createFrameTable(self.central_widget)
        
        # set the model of the table view
        self.tableView_original.setModel(self.models.model_animals)
        
        # add widgets to layout
        self.layout_win_table.addWidget(self.btn_save_table)
        self.layout_win_table.addWidget(self.frame_table)
        
        # set central widget
        self.setCentralWidget(self.central_widget)
        
        # show window
        self.show()
        
    def onBtnSaveTable(self):
        """
        Function to save the current data table. For this, it opens a "Save as"
        file dialog.

        """
        # create a file dialog
        dialog = QtWidgets.QFileDialog()
        filename = dialog.getSaveFileName(self, 'Save Table', filter="*.csv")
        
        # export to CSV
        self.models.model_animals.exportToCsv(res_file_path="", 
                                              file_id=None, 
                                              out_file_path=filename[0])

    def _createFrameTable(self, parent):
        """
        Function to create the frame showing the data table.

        Parameters
        ----------
        parent : optional
            The default is None.

        Returns
        -------
        frame_table : QFrame
            frame containing a tab widget (one tab for the current table, 
                                           one tab for a summary)

        """
        # frame for displaying data table
        frame_table = QtWidgets.QFrame(parent)
        frame_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        frame_table.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_table.setObjectName("frame_table")
        
        # layout
        self.layout_frame_table = QtWidgets.QVBoxLayout(frame_table)
        self.layout_frame_table.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_table.setSpacing(0)
        self.layout_frame_table.setObjectName("layout_frame_table")
        
        # tab widget to switch between the original table and the summary
        self.tabWidget = QtWidgets.QTabWidget(frame_table)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")
        
        # widget to show the original table
        self.original = QtWidgets.QWidget(self)
        self.original.setObjectName("original") 
        
        # layout to place the original table in
        self.layout_original_table = QtWidgets.QVBoxLayout(self.original)
        self.layout_original_table.setContentsMargins(0, 0, 0, 0)
        self.layout_original_table.setSpacing(0)
        self.layout_original_table.setObjectName("layout_original_table")
        
        # table view to display the original table
        self.tableView_original = QtWidgets.QTableView(self.original)
        self.tableView_original.setObjectName("tableView_original")
        self.layout_original_table.addWidget(self.tableView_original)

        # widget to show the summary table
        self.summary = QtWidgets.QWidget(self)  # comment see above @todo
        self.summary.setObjectName("summary")
        
        # layout to place the summary table in
        self.layout_summary_table = QtWidgets.QVBoxLayout(self.summary)
        self.layout_summary_table.setContentsMargins(0, 0, 0, 0)
        self.layout_summary_table.setSpacing(0)
        self.layout_summary_table.setObjectName("layout_summary_table")
        
        # table view to display the summary table
        self.tableView_summary = QtWidgets.QTableView(self.summary)
        self.tableView_summary.setObjectName("tableView_summary")
        self.layout_summary_table.addWidget(self.tableView_summary)
                
        # add tabs (original table and summary) to tab widget
        self.tabWidget.addTab(self.original, "")
        self.tabWidget.addTab(self.summary, "")
        
        # add tab widget to layout of table frame
        self.layout_frame_table.addWidget(self.tabWidget)
        
        return frame_table
