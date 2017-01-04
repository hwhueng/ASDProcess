# coding=utf-8
import math


def continuum_points(data):
    """"
    连续统去除节点
    @param data 平滑去水吸收波段的数据
    @return 连续统节点序列
    """
    # 节点
    p = []
    i = 0
    length = len(data)
    # 最后一个数据的索引
    last = length - 1

    while i < length:
        if i == 0:
            p.append(i)
        if i == last:
            if not math.isnan(data[i]):
                p.append(i)
            return p
        j = i + 1
        while j < length:
            if j == last:
                if not math.isnan(data[j]):
                    p.append(j)
                return p
            # 如果反射率为nan，继续
            if math.isnan(data[j]):
                j += 1
                continue
            m = j + 1
            while m < length:
                temp = (data[j] - data[i]) * (m - i) / (j - i) + data[i]
                # 如果存在交点，j往前移动
                if temp < data[m]:
                    j += 1
                    break
                # 如果遍历了所有的点，j是包络节点
                if m == last:
                    i = j
                    j += 1
                    p.append(i)
                    break
                m += 1
        # 如果所有点都遍历了，退出循环
    return p


def continuum_line(data, points):
    """
    generate continuum line
    :param data: reflection data
    :param  points: continuum nodes
    :return continuum line points
    """
    num = len(points)
    length = len(data)
    # initial line
    line = [float('nan') for i in range(length)]

    for i in range(1, num):
        start = points[i-1]
        end = points[i]
        for j in range(start, end + 1):
            temp = (data[end] - data[start])*(j-start)/(end-start)+data[start]
            line[j] = round(temp, 7)

    return line


def continuum_removal(data, line):
    """
    continuum removal
    :param line: continuum line data
    :param data: reflection data
    :return continuum removal data
    """
    length = len(data)
    # initial data
    removal = [float('nan') for i in range(length)]

    for i in range(length):
        if not math.isnan(data[i]):
            removal[i] = round(data[i] / line[i], 7)

    return removal


def continuum(data):
    """
    calculate continuum removal data
    :param data: the spectrum data
    :return continuum removal data
    """
    points = continuum_points(data)
    lines = continuum_line(data, points)
    return continuum_removal(data, lines)
