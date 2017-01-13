# coding=utf-8
"""
draw spectral line series
"""

from PyQt5.QtWidgets import QWidget, QAbstractItemView, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, QRect, QLine, QPoint
from PyQt5.QtGui import QPainter, QPen

import numpy as np


class LineChart(QWidget):
    def __init__(self, *args, **kwargs):
        super(LineChart, self).__init__(*args, **kwargs)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.x_axis = None
        self.y_axis = None
        self.painter = None
        self.axis_pen = QPen(Qt.black, 2)
        self.margin = 40
        self.data = {}
        self.min_y = None
        self.max_y = None
        self.length = 2151

    def draw_vertical(self):
        height = self.height()
        p1 = QPoint(self.margin, self.margin)
        p2 = QPoint(self.margin, height - self.margin)
        axis_line = QLine(p1, p2)
        self.painter.save()
        self.painter.setPen(self.axis_pen)
        self.painter.drawLine(axis_line)
        self.painter.restore()

    def draw_horizon(self):
        width = self.width()
        height = self.height()
        p1 = QPoint(self.margin, height - self.margin)
        p2 = QPoint(width - self.margin, height - self.margin)
        axis_line = QLine(p1, p2)
        self.painter.save()
        self.painter.setPen(self.axis_pen)
        self.painter.drawLine(axis_line)
        self.painter.restore()

    def paintEvent(self, evt):
        self.painter = QPainter()

        self.painter.begin(self)
        self.draw_horizon()
        self.draw_vertical()
        self.draw_vertical_ticks()
        self.draw_horizon_ticks()
        if self.data:
            self.draw_line(self.data)
        self.painter.end()

    def draw_vertical_ticks(self):
        self.painter.save()
        height = self.height()
        st = (height - 2 * self.margin) / 5
        self.painter.translate(self.margin, self.margin)
        for i in range(5):
            pos = int(st * i)
            self.painter.drawLine(0, pos, 4, pos)
        self.painter.restore()

    def draw_horizon_ticks(self):
        self.painter.save()
        width = self.width()
        height = self.height()
        st = (width - 2 * self.margin) / 5
        self.painter.translate(self.margin, height - self.margin - 5)
        for i in range(5):
            pos = int(st * i)
            self.painter.drawLine(pos, 0, pos, 4)
        self.painter.restore()

    def draw_line(self, data):
        ll = self.length
        dmax = self.max_y
        dmin = self.min_y
        width = self.width() - 2 * self.margin
        height = self.height() - 2 * self.margin
        scale_y = (dmax - dmin) / height
        scale_x = ll / width
        points = []
        self.painter.save()
        self.painter.translate(self.margin, self.margin)
        for key in data:
            da = data[key]
            for i in range(ll):
                pos_y = height - (da[i] - dmin) / scale_y
                pos_x = i / scale_x
                points.append(QPoint(pos_x, pos_y))
                if 0 < i:
                    self.painter.drawLine(points[i], points[i - 1])
            points = []
        self.painter.restore()

    def set_items(self, item):
        key = item.data(Qt.ToolTipRole)
        if item.data(Qt.CheckStateRole) == Qt.Checked:
            tmp = item.data(Qt.UserRole)[1]
            # self.length = len(tmp)
            min_ = min(tmp)
            max_ = max(tmp)
            if self.min_y:
                if self.min_y > min_:
                    self.min_y = min_
            else:
                self.min_y = min_
            if self.max_y:
                if self.max_y < max_:
                    self.max_y = max_
            else:
                self.max_y = max_
            self.data[key] = tmp
        else:
            self.data.pop(key)
        self.update()
