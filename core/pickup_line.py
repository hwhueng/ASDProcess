# coding=utf-8
"""
自动挑线
"""
import os
import numpy as np
import matplotlib.pyplot as plt

from .asd import asd_read, asd_write, asd_write_csv


class PickUpLine:
    def __init__(self, dirname, resdir=None, threshold=0.02, winsize=100,
                 group=10, plot=False):
        """"
        initial parameters
        :param dirname: asd data located directory
        :param resdir: save result data directory
        :param threshold: pick up threshold
        :param winsize: the move window size
        :param group: spectral lines of each group, default 10
        :param plot: if True, draw and save the spectral curve
        """
        self.dirname = dirname
        self.resdir = resdir
        self.threshold = threshold
        self.winsize = winsize
        self.group = group
        self.plot = plot

    def line_choose(self, data_group):
        """
        pick up line in data group
        :param data_group: group * data length array
        :return: index of reserve lines
        """
        data = np.array(data_group)
        half_threshold = self.threshold / 2
        result_index = [i for i in range(self.group)]
        i = 0
        while i < self.group:
            j = 0
            while j < 2151:
                if len(result_index) < 4:
                    return []
                end = j + self.winsize
                if 1000 <= j < 1150 or 1000 < end < 1150:
                    j = 1150
                    continue
                elif 1450 <= j < 1650 or 1450 < end < 1650:
                    j = 1650
                    continue
                elif j >= 1950 or end > 1950:
                    break
                test_data = data[:, j:end]
                mean_row = np.mean(test_data, axis=1)
                mean_row_std = np.std(mean_row)
                mean_all = np.mean(test_data)
                delta = mean_row - mean_all
                pop_index = np.argmax(np.abs(delta))
                max_dis = np.max(mean_row) - np.min(mean_row)
                if max_dis > self.threshold or mean_row_std > half_threshold:
                    data = np.delete(data, pop_index, 0)
                    result_index.pop(int(pop_index))
                    j += self.winsize
                    continue
                j += self.winsize // 2
            i += 1
        return result_index

    def get_file_list(self):
        """
        get file list and reshape to n * self.group matrix
        :return: group matrix
        """
        file_list = os.listdir(self.dirname)
        file_list.sort()
        row = len(file_list) // self.group
        col = self.group
        file_matrix = []
        for i in range(row):
            file_matrix.append(file_list[i * col:(i + 1) * col])
        return file_matrix

    def run(self):
        """
        run pick up line processing
        :return: no return
        """
        file_matrix = self.get_file_list()
        if not self.resdir:
            pardir = os.path.abspath(os.path.join(self.dirname, os.pardir))
            self.resdir = os.path.join(pardir, self.dirname + "_result")
        _make_dir(self.resdir)
        row = len(file_matrix)
        # save csv format data
        csv_dir = os.path.join(self.resdir, "data_csv")
        _make_dir(csv_dir)
        # save binary format data
        bin_dir = os.path.join(self.resdir, "data_binary")
        _make_dir(bin_dir)
        # save bad data group, binary format
        fail_dir = os.path.join(self.resdir, "data_fail")
        _make_dir(fail_dir)
        # save good data group, binary format
        good_dir = os.path.join(self.resdir, "data_good")
        _make_dir(good_dir)

        # save plot image
        plot_dir = os.path.join(self.resdir, "plot")
        _make_dir(plot_dir)
        # save bad data group image
        fail_plot_dir = os.path.join(plot_dir, "fail")
        _make_dir(fail_plot_dir)
        # save good data group image
        good_plot_dir = os.path.join(plot_dir, "good")
        _make_dir(good_plot_dir)

        # save log
        good = os.path.join(self.resdir, "good.txt")
        file_log = open(good, "w")

        for i in range(row):
            group_name = [os.path.join(self.dirname, name)
                          for name in file_matrix[i]]
            group_data = []
            head = None
            # save good data
            good_data = []
            for name in group_name:
                head, data = asd_read(name)
                group_data.append(data)
            # line choose
            result_index = self.line_choose(group_data)
            length = len(result_index)
            print("Processing:[", group_name[i][0], "-->",
                  group_name[i][-1])
            if length > 3:
                good_file = []
                for j in result_index:
                    good_file.append(file_matrix[i][j])
                    good_data.append(group_data[j])
                file_log.write(str(good_file) + "\n")
                mean_data = np.mean(good_data, axis=0)
                # save good data's mean
                name_ = os.path.join(good_dir, group_name[i][0])
                asd_write(name_, head, mean_data)
                asd_write_csv(mean_data, group_name[i][0])
                plot_name = os.path.join(good_plot_dir, group_name[i][0])
            else:
                plot_name = os.path.join(fail_plot_dir, group_name[i][0])

            if self.plot:
                _plot_data(plot_name, group_data, good_data)
        file_log.close()


def _plot_data(file_name, data_group, good_group):
    """
    plot data
    :param file_name: output image name
    :param data_group: orig group data
    :param good_group: good data
    :return: no return
    """
    x = [i + 350 for i in range(2151)]
    file_name += ".png"
    if good_group:
        fig = plt.figure(figsize=(32, 18))
        plt.subplot(211)
        for da in good_group:
            plt.plot(x, da)
        plt.subplot(212)
        for da in data_group:
            plt.plot(x, da)
    else:
        fig = plt.figure(figsize=(16, 9))
        for da in data_group:
            plt.plot(x, da)
    plt.xlim([350, 2500])
    plt.ylim([0, 1])
    plt.savefig(file_name)
    plt.close(fig)


def _make_dir(dir_name):
    """
    try to make directory with the giving name
    :param dir_name: directory name
    :return: no return
    """
    if not os.path.exists(dir_name) or \
       not os.path.isdir(dir_name):
        os.mkdir(dir_name)
