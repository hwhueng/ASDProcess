# coding=utf-8
import os
import struct
from .asd import asd_read


def water_remove(data):
    """
    remove water absorb bands
    :param data: reflection data
    :return data without water absorb bands
    """
    try:
        res = data
        # remove water bands
        # 1350-1460
        for i in range(999, 1110):
            res[i] = float("nan")
        # 1790-1970
        for i in range(1450, 1620):
            res[i] = float("nan")
        # 2340-2500
        for i in range(1989, 2151):
            res[i] = float("nan")
    except ValueError:
        raise ValueError("illegal data")

    return res


def water_remove_file(filename):
    """
    asd file which need remove water bands
    :param filename asd file name
    :return data without water absorb bands
    """
    head, bands_value = asd_read(filename)

    return head, water_remove(bands_value)


def process_dir(data_dir, result_dir=None):
    """
    batch processing water remove
    :param data_dir: directory where asd binary file located
    :param result_dir: directory to save processed file results
    :return no return
    """

    if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
        raise OSError("%s is not a dir" % data_dir)

    # get the parent directory of the input data dir
    pardir = os.path.abspath(os.path.join(data_dir, os.pardir))

    # if result directory is not given, create in pardir
    if result_dir is None:
        result_dir = os.path.join(pardir, "water_removed")

    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    listdir = os.listdir(data_dir)

    for filename in listdir:
        file_ = os.path.join(data_dir, filename)
        head, data = asd_read(file_)
        data = water_remove(data)
        data = struct.pack("2151b", *data)
        out_file = os.path.join(result_dir, filename+".ref")
        with open(out_file, "wb") as asd_:
            asd_.write(head)
            asd_.write(data)
