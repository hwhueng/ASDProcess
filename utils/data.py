# coding=utf-8

import numpy as np
from fractions import Fraction


def check_data(data):
    if not hasattr(data, "__iter__"):
        data = [data]

    col = len(data[0])
    for da in data:
        if len(da) != col or not is_number(da):
            return False
    return True


def is_number(data):
    for i in data:
        try:
            tts = float(i)
        except ValueError:
            print("包含非数值数据")
            return False
    return True


def get_data_range(data):
    """
    获取数据的最大和最小值
    """
    data = np.array(data)
    return np.nanmin(data), np.nanmax(data)


def new_bound(vmin, vmax, ticks=7):
    """
    计算在给定ticks下的数据的新边界，
    返回新的上下边界和数据间隔
    """
    if vmin == vmax:
        if vmin > 0:
            vmin = 0
        elif vmin < 0:
            vmax = 0
        else:
            vmax = 1

    if ticks <= 0:
        ticks = 2
    delta = abs(vmax - vmin) / (ticks - 1)
    # print("delta:", delta)
    t3 = "%.2E" % delta
    p3 = t3.find("E")
    order3 = int(t3[p3 + 1:])

    # 获取间隔数据
    interv = float(t3[:p3]) / 10
    inv = [0.1, 0.2, 0.5, 1.0]
    for i in inv:
        if interv <= i:
            interv = i
            break
    if order3 < 0:
        interv = Fraction(int(interv * 10), 10 ** abs(int(order3)))
    else:
        interv = interv * 10 * 10**order3
    lower = interv * round(vmin / interv)
    upper = interv * round(vmax / interv)

    if upper < vmax:
        upper += interv

    if lower > vmin:
        lower -= interv

    return lower, upper, interv
