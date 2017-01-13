# coding=utf-8
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt

from ..utils.data import new_bound


class Axis:
    """
    base class of axis system
    """
    def __init__(self, data_range=None, width=200,
                 height=300, margin=30, loc=None):
        """
        initial axis
        :param data_range: data range, (min, max)
        :param width: frame width
        :param height: frame height
        :param margin: margin between axis and frame border
        :param loc: ticks loc, tuple or list
        """
        self.data_range = data_range
        self.width = width
        self.height = height
        self.margin = margin
        self.loc = loc
        self.axis_line = None
        self.axis_ticks = None
        self.axis_labels = None
        self.painter = None
        self.axis_pen = QPen(Qt.black, 2)

    def set_painter(self, painter):
        self.painter = painter

    def update(self, width, height, margin, loc):
        self.width = width
        self.height = height
        self.margin = margin
        self.loc = loc
        self.draw_axis()

    def draw_axis(self):
        raise NotImplementedError("no implemented!")


class VerticalAxis(Axis):
    """
    Vertical axis
    """
    def __init__(self, *args, **kwargs):
        super(VerticalAxis, self).__init__(*args, **kwargs)
        self.range = [350, 2500]
        self.maxy = 2500
        self.miny = 350

    def draw_axis(self):
        self.painter.save()
        self.painter.setPen(self.axis_pen)
        miny, maxy, interv = new_bound(* self.range)

