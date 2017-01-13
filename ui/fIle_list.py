# coding=utf-8
import os
from itertools import cycle
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

from .color import cnames
from .global_path import setdir, getdir
from ..core.asd import asd_read


class FileListWidget(QListWidget):
    """
    ASD File List
    """
    selections = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(FileListWidget, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setUniformItemSizes(True)
        self.filters = (".asd", ".ref", ".mn", ".sco", ".dv1", ".dv2")
        self.selected_file = None
        # self.itemSelectionChanged.connect(self.selected_items)
        # self.itemChanged()
        self.colors = cycle(cnames)

    def add_files(self, files):
        """
        add files to item list widget
        :param files: input file list
        :return: no return
        """

        if os.path.isdir(str(files)):
            files = os.listdir(files)

        if not hasattr(files, "__iter__"):
            files = [files]
        # set global path to current dir
        dir_name = os.path.dirname(files[0])
        setdir(dir_name)
        for ff in files:
            if not os.path.exists(ff):
                continue
            dot = ff.rfind(".")
            ends = ff[dot:]
            if ends in self.filters:
                if self.findItems(ff, Qt.MatchExactly):
                    continue
                self.add_item(ff)

    def add_item(self, file_name):
        """
        add single file to item list
        :param file_name: input file name
        :return: no return
        """
        item = FileListItem()
        base_name = os.path.basename(file_name)
        head, data = asd_read(file_name)
        item.setData(Qt.DisplayRole, base_name)
        item.setData(Qt.UserRole, (head, data))
        item.setData(Qt.CheckStateRole, Qt.Unchecked)
        color_name = cnames[next(self.colors)]
        color = QColor()
        color.setNamedColor(color_name)
        item.setData(Qt.DecorationRole, color)
        item.setData(Qt.ToolTipRole, file_name)
        self.addItem(item)
        self.viewport().update()

    def dropEvent(self, evt):
        # super(FileListWidget, self).dropEvent(evt)
        mime = evt.mimeData()
        if mime.hasUrls():
            urls = mime.urls()
            files = [urls[i].toLocalFile() for i in range(len(urls))]
            self.add_files(files)

    def dragEnterEvent(self, evt):
        mime = evt.mimeData()
        if mime.hasUrls():
            evt.accept()
        else:
            evt.ignore()

    def selected_items(self):
        items = self.selectedItems()
        # names = [item.data(Qt.ToolTipRole) for item in items]
        # print(names)
        self.selections.emit(items)


class FileListItem(QListWidgetItem):
    """
    initial file list item
    """
    def __int__(self, *args, **kwargs):
        super(FileListItem, self).__init__(*args)
        self.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsSelectable |
                      Qt.ItemIsEnabled | Qt.ItemIsDragEnabled |
                      Qt.ItemIsDropEnabled)
        self.setCheckState(Qt.Unchecked)
        self.setSelected(True)
