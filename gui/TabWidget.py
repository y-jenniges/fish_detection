# implementation of TabWidget and TabBar from https://www.manongdao.com/q-367474.html (last access: 11.08.2020)
# allows the tabs to be placed on the left side with horizontal text (per default, Qt only supports vertical text here)
from PyQt5 import QtCore, QtWidgets

"""
This module implementaion was taken from 
.. Stackoverflow
    https://www.manongdao.com/q-367474.html (last access: 11.08.2020)
"""

class TabWidget(QtWidgets.QTabWidget):
    """
    A custom tab widget that uses the custom TabBar to display the tabs on the left side but with horizontal text (default is vertical text).
    """
    def __init__(self, parent=None):
        super(QtWidgets.QTabWidget, self).__init__(parent)
        #QtWidgets.QTabWidget.__init__(self)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)
    
        
class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)
            painter.restore()