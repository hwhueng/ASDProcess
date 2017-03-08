# coding=utf-8
"""
计算光谱微分
"""


def derivation1(data):
    """
    计算光谱一阶微分
    @param data 光谱数据
    @return data 光谱的一阶微分
    """

    # 初始化数据
    length = len(data)
    der = [float('nan') for i in range(length)]

    last = length - 1

    for i in range(1, last):
        der[i] = (data[i + 1] - data[i - 1]) / 2

    return der


def derivation2(data):
    """
    计算光谱二阶微分
    @param data 光谱数据
    @return 光谱二阶微分数据
    """

    length = len(data)
    der = [float('nan') for i in range(length)]

    last = length - 2

    for i in range(2, last):
        der[i] = (data[i + 2] - 2 * data[i] + data[i - 2]) / 4

    return der


def derivation3(data):
    """
    计算光谱3阶微分
    @param data 光谱数据
    @return 光谱三阶微分数据
    """

    length = len(data)
    der = [float('nan') for i in range(length)]

    last = length - 3

    for i in range(3, last):
        der[i] = (data[i + 3] - 3 * data[i + 1] + 3 * data[i - 1] - data[i - 3]) / 8

    return der
