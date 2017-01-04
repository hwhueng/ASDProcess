# coding=utf-8
"""
常用的数据变化方法
"""

import math


def log(data):
    """
    对数变换
    """
    res = []
    for da in data:
        if da <= 0:
            res.append(float("nan"))
        else:
            res.append(math.log10(da))
    return res


def inverse(data):
    """
    倒数变换
    """
    res = []
    for da in data:
        if da == 0:
            res.append(float('nan'))
        else:
            res.append(1 / da)
    return res


def log_inverse(data):
    """
    倒数对数变换
    """
    res = []
    for da in data:
        if da <= 0:
            res.append(float("nan"))
        else:
            res.append(math.log10(1 / da))
    return res
