# coding=utf-8
import os
from PyQt5.QtWidgets import (QFileDialog, QAction, QMenu, QHBoxLayout,
                             QVBoxLayout, QMainWindow, QDockWidget, QMenuBar)

from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QSize
from PyQt5.QtGui import QIcon

from .global_path import setdir, getdir, icondir


class MainWindow(QMainWindow):
    selectSignal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.selectedDir = getdir()
        self.selectedFile = None
        self.initUI()

    def initUI(self):
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("ASD高光谱数据处理")
        # layout
        self.layout = QVBoxLayout()
        self.statusbar = self.statusBar
        self.setWindowIcon(QIcon(os.path.join(icondir, "icon.png")))


class MenuBar(QMenuBar):

    def __init__(self, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)
        self.process = QMenu()
        self.processMenu = None

    def setProcessMenu(self, process=None):
        self.processMenu = process

