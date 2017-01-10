# coding=utf-8
import os
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from ..core.asd import asd_read


class FileListWidget(QListWidget):
    """
    ASD File List
    """
    def __init__(self, *args, **kwargs):
        super(FileListWidget, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.filters = (".asd", ".ref", ".mn", ".dv1", ".dv2")
        self.selected_file = None
        self.upload_func = None

    def add_files(self, files):
        """
        add files to item list widget
        :param files: input file list
        :return: no return
        """
        if not hasattr(files, "__iter__"):
            files = [files]
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