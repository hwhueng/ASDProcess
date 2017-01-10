# coding=utf-8
import os
from PyQt5.QtWidgets import (QFileDialog, QAction, QMenu, QHBoxLayout,
                             QVBoxLayout, QMainWindow, QDockWidget, QMenuBar)

from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QSize
from PyQt5.QtGui import QIcon

from .global_path import setdir, getdir, icondir, asdtype


class MainWindow(QMainWindow):
    selected_sig = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.selected_dir = getdir()
        self.selected_file = None
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("ASD高光谱数据处理")
        self.setWindowIcon(QIcon(os.path.join(icondir, "icon.png")))
        # add custom menu
        menu_bar = MenuBar(self)
        menu_bar.file_action_trigger(self.get_open_files)
        menu_bar.dir_action_trigger(self.get_open_dir)
        # add dock widget
        file_list = QDockWidget("光谱文件列表", self)
        file_list.setAllowedAreas(Qt.LeftDockWidgetArea |
                                  Qt.RightDockWidgetArea)
        # itemListWidget = ItemListWidget()

    def get_open_dir(self):
        """
        get current opened directory name
        :return: current directory name
        """
        selected = QFileDialog.getExistingDirectory(self, "选择文件",
                                                    self.selected_dir)
        if selected:
            files = [os.path.join(selected, fi).replace("\\", '/')
                     for fi in os.listdir(selected)]
            self.selected_file = [fi for fi in files if os.path.isfile(fi)]
            self.selected_sig.emit(self.selected_file)
            self.selected_dir = selected
            setdir(self.selectedDir)
        return selected

    def get_open_files(self):
        """
        get open current opened files' name
        :return: file list
        """
        files = QFileDialog.getOpenFileNames(self, "选择文件", self.selected_dir,
                                             asdtype)[0]
        if files:
            self.selected_file = files
            tmp_dir = os.path.dirname(os.path.dirname(files))
            self.selected_dir = tmp_dir
            setdir(tmp_dir)
            self.selected_sig.emit(files)
        return files


class MenuBar(QMenuBar):
    """
    Main window menu bar
    """
    def __init__(self, *args, **kwargs):
        super(MenuBar, self).__init__(*args, **kwargs)
        self.process = QMenu()
        self.process_menu = None
        self.file_action = None
        self.dir_action = None
        self.img_action = None
        self.init_ui()

    def init_ui(self):
        parent = self.parentWidget()
        self.dir_action = QAction("打开文件夹...", parent)
        self.file_action = QAction("打开文件...", parent)
        self.img_action = QAction("保存图像", parent)
        # add file menu
        file_menu = QMenu(self)
        file_menu.addAction(self.dir_action)
        file_menu.addAction(self.file_action)
        file_menu.addSeparator()
        file_menu.addAction(self.img_action)
        self.addMenu(file_menu)

    def set_process_menu(self, process=None):
        self.process_menu = process

    def file_action_trigger(self, func=None):
        self.file_action.triggered.connect(func)

    def dir_action_trigger(self, func=None):
        self.dir_action.triggered.connect(func)

    def img_action_trigger(self, func=None):
        self.img_action.triggered.connect(func)
