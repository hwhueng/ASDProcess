# coding=utf-8
import numpy as np
from scipy.signal import savgol_filter as sg


def sg_smooth(data, winsize, order, deriv=0, rate=1):
    """
    savitzky-golay 平滑
    @param data 数据
    @param winsize 窗口大小, 必须为奇数
    @param order 多项式次数
    @param deriv 噪声方差
    @param rate 窗口
    @return 平滑后的数据
    winsize = np.int(winsize)
    order = np.int(order)
    data = np.array(data)
    if winsize % 2 != 1 or winsize < 1:
        raise ValueError("winsize必须为奇数且不小于1")
    if winsize < order+2:
        raise ValueError("winsize过小")
    if winsize > len(data):
        raise ValueError("winsize过大")

    order_range = range(order+1)
    half_window = (winsize-1) // 2

    bco = np.mat([[k**i for i in order_range] \
            for k in range(-half_window, half_window+1)])
    mco = np.linalg.pinv(bco).A[deriv] * rate**deriv*factorial(deriv)

    firstvals = data[0] - np.abs(data[1:half_window+1][::-1] - data[0])
    lastvals = data[-1] + np.abs(data[-half_window-1: -1][::-1] - data[-1])

    data = np.concatenate((firstvals, data, lastvals))

    return np.convolve(mco[::-1], data, mode='valid')"""
    return sg(data, winsize, order)


def nansg_smooth(data, winsize, order, deriv=0, rate=1):
    """
    包含水吸收波段的数据平滑
    """
    # 350-1350
    band1 = data[0:1000]
    # 1350-1460 水吸收1
    band2 = data[1000:1110]
    # 1460 - 1790
    band3 = data[1110:1450]
    # 1790 - 1970 水吸收2
    band4 = data[1450:1620]
    # 1970 - 2340
    band5 = data[1620:1989]
    # 2340 - 2500 水吸收3
    band6 = data[1989:2151]
    band1 = sg_smooth(band1, winsize, order, deriv, rate)
    band2 = sg_smooth(band2, winsize, order, deriv, rate)
    band3 = sg_smooth(band3, winsize, order, deriv, rate)
    band4 = sg_smooth(band4, winsize, order, deriv, rate)
    band5 = sg_smooth(band5, winsize, order, deriv, rate)
    band6 = sg_smooth(band6, winsize, order, deriv, rate)

    res = np.concatenate((band1, band2, band3, band4, band5, band6))

    return res


def cubic_smooth5(data, loop=1):
    """
    五点三次平滑
    @param data 光谱数据
    @param loop 迭代次数,默认为一次
    @return loop次迭代平滑后的结果
    """
    length = len(data)
    data = data.copy()
    last = length - 2
    temp = [0 for i in range(length)]

    for i in range(loop):
        temp[0] = (69 * data[0] + 4 * data[1] - 6 * data[2] +
                   4 * data[3] - data[4]) / 70
        temp[1] = (2 * data[0] + 27 * data[1] + 12 * data[2] - 8 * data[3] +
                   2 * data[4]) / 35
        for j in range(2, last):
            temp[j] = (-3 * (data[j - 2] + data[j + 2]) + 12 * (data[j - 1] + data[j + 1]) +
                       17 * data[j]) / 35
        temp[length - 2] = (2 * data[length - 5] - 8 * data[length - 4] + 12 * data[length - 3] +
                            27 * data[length - 2] + 2 * data[length - 1]) / 35
        temp[length - 1] = (-data[length - 5] + 4 * data[length - 4] - 6 * data[length - 3] +
                            4 * data[length - 2] + 69 * data[length - 1]) / 70
        data = temp

    return data


def nancubic_smooth5(data, loop=1):
    """
    包含水吸收波段的数据平滑
    """
    # 350-1350
    band1 = data[0:1000]
    # 1350-1460 水吸收1
    band2 = data[1000:1110]
    # 1460 - 1790
    band3 = data[1110:1450]
    # 1790 - 1970 水吸收2
    band4 = data[1450:1620]
    # 1970 - 2340
    band5 = data[1620:1989]
    # 2340 - 2500 水吸收3
    band6 = data[1989:2151]
    band1 = cubic_smooth5(band1, loop)
    band2 = cubic_smooth5(band2, loop)
    band3 = cubic_smooth5(band3, loop)
    band4 = cubic_smooth5(band4, loop)
    band5 = cubic_smooth5(band5, loop)
    band6 = cubic_smooth5(band6, loop)

    res = np.concatenate((band1, band2, band3, band4, band5, band6))

    return res


def cubic_smooth7(data, loop=1):
    """
    七点三次平滑
    @param data 光谱数据
    @param loop 迭代次数
    @return loop次迭代平滑后的结果
    """

    length = len(data)
    data = data.copy()
    last = length - 3
    temp = [0 for i in range(length)]

    for i in range(loop):
        temp[0] = (39 * data[0] + 8 * data[1] - 4 * data[2] - 4 * data[3] +
                   data[4] + 4 * data[5] - 2 * data[6]) / 42
        temp[1] = (8 * data[0] + 19 * data[1] + 16 * data[2] + 6 * data[3] -
                   4 * data[4] - 7 * data[5] + 4 * data[6]) / 42
        temp[3] = (-4 * data[0] + 16 * data[1] + 19 * data[2] + 12 * data[3] +
                   2 * data[4] - 4 * data[5] + data[6]) / 42

        for j in range(3, last):
            temp[j] = (-2 * (data[j + 3] + data[j - 3]) + 3 * (data[j - 2] +
                       data[j + 2]) + 6 * (data[j - 1] + data[j + 1]) +
                       7 * data[j]) / 21
        temp[length - 3] = (-4 * data[length - 1] + 16 * data[length - 2] +
                            19 * data[length - 3] + 12 * data[length - 4] +
                            2 * data[length - 5] - 4 * data[length - 6] +
                            data[length - 7]) / 42
        temp[length - 2] = (8 * data[length - 1] + 19 * data[length - 2] +
                            16 * data[length - 3] + 6 * data[length - 4] -
                            4 * data[length - 5] - 7 * data[length - 6] +
                            4 * data[length - 7]) / 42
        temp[length - 1] = (39 * data[length - 1] + 8 * data[length - 2] -
                            4 * data[length - 3] - 4 * data[length - 4] +
                            data[length - 5] + 4 * data[length - 6] -
                            2 * data[length - 7]) / 42
        data = temp

    return data


def nancubic_smooth7(data, loop=1):
    """
    包含水吸收波段的数据平滑
    """
    # 350-1350
    band1 = data[0:1000]
    # 1350-1460 水吸收1
    band2 = data[1000:1110]
    # 1460 - 1790
    band3 = data[1110:1450]
    # 1790 - 1970 水吸收2
    band4 = data[1450:1620]
    # 1970 - 2340
    band5 = data[1620:1989]
    # 2340 - 2500 水吸收3
    band6 = data[1989:2151]
    band1 = cubic_smooth7(band1, loop)
    band2 = cubic_smooth7(band2, loop)
    band3 = cubic_smooth7(band3, loop)
    band4 = cubic_smooth7(band4, loop)
    band5 = cubic_smooth7(band5, loop)
    band6 = cubic_smooth7(band6, loop)

    res = np.concatenate((band1, band2, band3, band4, band5, band6))

    return res
