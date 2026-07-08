"""
This module provides a custom tab widget that enables tabs on the side with 
vertical text. The implementaion was taken from 
https://www.manongdao.com/q-367474.html (last access: 11.08.2020)
"""
from PyQt5 import QtCore, QtWidgets


class TabWidget(QtWidgets.QTabWidget):
    """
    A custom tab widget that uses the custom TabBar to display tabs on 
    the left side but with horizontal text (default is vertical text).
    
    Taken from:
        https://www.manongdao.com/q-367474.html (last access: 11.08.2020)
    """
    def __init__(self, parent=None):
        """
        Init function.

        Parameters
        ----------
        parent : optional
            The default is None.
        """
        super(QtWidgets.QTabWidget, self).__init__(parent)

        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)
    
        
class TabBar(QtWidgets.QTabBar):
    """
    A custom QTabBar that displays the tabs on the left side but with 
    horizontal text (usually it is vertical).
        
    Taken from:
        https://www.manongdao.com/q-367474.html (last access: 11.08.2020)
    """
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