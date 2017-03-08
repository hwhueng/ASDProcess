# coding=utf-8
from PyQt5.QtWidgets import QGraphicsScene


class LineChartScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super(LineChartScene, self).__init__(*args, **kwargs)
