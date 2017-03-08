# coding=utf-8
"""
计算光谱参量
"""
import numpy as np
from .derivation import derivation1
from collections import OrderedDict


def blue_valley_position(data):
    """
    蓝谷位置 380~500nm反射率最小值
    """
    data = data[50:150]
    return np.nanargmin(data) + 400


"""def blue_violet_peek_absorb(data):
    蓝紫波段吸收峰位置：光谱在380~500nm波段反射率的最小值
    @param data 光谱数据，numpy 数组
    @return 吸收峰光谱位置

    return np.nanargmin(np.array(data[30:150])) + 380"""


def blue_edge_amplitude(data):
    """
    蓝边幅值：蓝波段(490~530nm)一阶微分的最大值
    """
    data = derivation1(data)
    return round(np.nanmax(data[140:180]), 6)


def blue_edge_location(data):
    """
    蓝边位置： 光谱在蓝波段(490~530nm)的拐点、一阶导数的最大值所在位置
    """
    data = derivation1(data)
    return np.nanargmax(np.array(data[140:180])) + 490


def blue_edge_value(data):
    """
    蓝边反射率
    """
    loc = blue_edge_location(data)
    return round(data[loc - 350], 6)


def blue_edge_area(data):
    """
    蓝边面积
    """
    data = derivation1(data)
    return round(np.nansum(np.abs(data[140:180])), 6)


def green_peek_value(data):
    """
    绿波段(510~560nm)最大的反射率
    """
    return round(max(data[160:210]), 6)


def green_peek_location(data):
    """
    绿波段(510~560nm)反射峰，即绿峰位置
    """
    return np.array(data[160:210]).argmax() + 510


def green_peek_area(data):
    """
    绿峰面积：510~560nm原始光谱所围城的面积
    """
    return round(np.abs(data[160:210]).sum(), 6)


def yellow_edge_amplitude(data):
    """
    黄边幅值：在黄波段(560~640nm)一阶微分的最大值
    """
    data = derivation1(data)
    return round(max(data[210:290]), 6)


def yellow_edge_location(data):
    """
    黄波段(560~640nm)吸收边即黄边位置：光谱曲线在黄波段的拐点，一阶导数
    在此波段的最大值所在位置
    """
    data = derivation1(data)
    return np.array(data[210:290]).argmax() + 560


def yellow_edge_value(data):
    """
    黄边反射率
    """
    loc = yellow_edge_location(data)
    return round(data[loc - 350], 6)


def yellow_edge_area(data):
    """
    黄波段(560~640nm)一阶微分的积分
    """
    # 因为光谱间隔为1nm，积分公式为 ΣΔf*Δx，所以只需求和
    data = derivation1(data)
    return round(np.abs(data[210:290]).sum(), 6)


def red_valley_location(data):
    """
    红波段(650~690nm)吸收峰(红谷):为光谱在红波段的反射率的最小值所在位置
    """
    return np.array(data[300:340]).argmin() + 650


def red_valley_value(data):
    """
    红谷反射率 光谱在红波段反射率的最小值
    """
    return round(min(data[300:340]), 6)


def red_edge_amplitude(data):
    """
    红边幅值，680~760nm波段一阶微分的最大值
    """
    data = derivation1(data)
    return round(max(data[330:410]), 6)


def red_edge_location(data):
    """
    红边位置:为光谱曲线在红-近红外(680~760nm)波段的拐点，一阶导数的最大值
    """
    data = derivation1(data)
    return np.array(data[330:410]).argmax() + 680


def red_edge_value(data):
    """
    红边反射率
    """
    loc = red_edge_location(data)
    return round(data[loc - 350], 6)


def red_edge_area(data):
    """
    红边面积：680~760nm一阶微分的积分
    """
    data = derivation1(data)
    return round(np.abs(data[330:410]).sum(), 6)


def nir_peek_location(data):
    """
    红外波段(780~950nm)反射率最大值所在位置
    """
    return np.array(data[430:600]).argmax() + 780


def nir_peek_value(data):
    """
    红外波段反射率最大值
    """
    return round(max(data[430:600]), 6)


def nir_moisture_sentive_location(data):
    """
    近红外水分(950-1000nm)吸收谷的中心位置
    """
    data = data[600:650]
    return np.nanargmax(data) + 950


def swir1_peek_location(data):
    """
    短波红外反射率最大值所在位置
    swir1(1100nm-1351nm)
    """
    data = data[750:1000]
    return np.nanargmax(data) + 1100


def swir2_peek_location(data):
    """
    短波红外反射率最大值所在位置
    swir1(1400nm-1800nm)
    """
    data = data[1050:1450]
    return np.nanargmax(data) + 1400


def ratio_rg_rr(data):
    """
    绿峰反射率与红谷反射率的比值
    """
    rg = green_peek_value(data)
    rr = red_valley_value(data)

    return np.divide(rg, rr)


def ratio_rg_rr_n(data):
    """
    绿峰反射率与红谷反射率的归一化比值
    """
    rg = green_peek_value(data)
    rr = red_valley_value(data)
    return np.divide(rg - rr, rg + rr)


def ratio_ar_ab(data):
    """
    红边面积与蓝边面积比值
    """
    ar = red_edge_area(data)
    ab = blue_edge_area(data)
    return np.divide(ar, ab)


def ratio_ar_ab_n(data):
    """
    红边面积与蓝边面积归一化比值
    """
    ar = red_edge_area(data)
    ab = blue_edge_area(data)
    return np.divide(ar - ab, ar + ab)


def ratio_ar_ay(data):
    """
    红边面积与黄边面积的比值
    """
    ar = red_edge_area(data)
    ay = yellow_edge_area(data)
    return np.divide(ar, ay)


def ratio_ar_ay_n(data):
    """
    红边面积与黄边面积的归一化比值
    """
    ar = red_edge_area(data)
    ay = yellow_edge_area(data)
    return np.divide(ar - ay, ar + ay)


translate = OrderedDict([("blue_valley_position", "蓝谷位置"),
                         ("blue_edge_amplitude", "蓝边幅值"),
                         ("blue_edge_location", "蓝边位置"),
                         ("blue_edge_value", "蓝边反射率"),
                         ("blue_edge_area", "蓝边面积"),
                         ("green_peek_value", "绿峰反射率"),
                         ("green_peek_location", "绿峰位置"),
                         ("green_peek_area", "绿峰面积"),
                         ("yellow_edge_amplitude", "黄边幅值"),
                         ("yellow_edge_location", "黄边位置"),
                         ("yellow_edge_area", "黄边面积"),
                         ("yellow_edge_value", "黄边反射率"),
                         ("red_valley_location", "红谷位置"),
                         ("red_valley_value", "红谷反射率"),
                         ("red_edge_amplitude", "红边幅值"),
                         ("red_edge_location", "红边位置"),
                         ("red_edge_area", "红边面积"),
                         ("red_edge_value", "红边反射率"),
                         ("nir_peek_location", "近红外波段峰值位置"),
                         ("nir_peek_value", "近红外波段峰值反射率"),
                         ("nir_moisture_sentive_location", "近红外水分敏感区位置"),
                         ("swir1_peek_location", "短波红外1最大值位置"),
                         ("swir2_peek_location", "短波红外2最大值位置"),
                         ("ratio_rg_rr", "绿峰反射率与红谷反射率的比值"),
                         ("ratio_rg_rr_n", "绿峰反射率与红谷反射率的归一化比值"),
                         ("ratio_ar_ab", "红边面积与蓝边面积的比值"),
                         ("ratio_ar_ab_n", "红边面积与蓝边面积的归一化比值"),
                         ("ratio_ar_ay", "红边面积与黄边面积的比值"),
                         ("ratio_ar_ay_n", "红边面积与黄边面积的归一化比值")])
