# coding=utf-8
import os
import struct
import csv


def asd_read(infile):
    """
    read asd binary file
    :param infile: asd input file name
    :return: file head and reflection data
    """
    if not os.path.exists(infile) or not os.path.isfile(infile):
        raise FileNotFoundError("%s not exists or not a file" % str(infile))

    fdata = open(infile, "rb")
    head = fdata.read(484)
    if head[:3] != b"ASD":
        head = _asd_head(head)
        data = _asd_source_data(fdata)
    else:
        data = struct.unpack("2151f", fdata.read())

    return head, data


def _asd_head(header):
    """
    modify asd source file header to reflection mode
    :param header: asd file header, 484 bits
    :return modified asd file header
    """
    # replace data type to reflection
    h1 = list(struct.unpack('484b', header))
    h1[0] = ord('A')
    h1[1] = ord('S')
    h1[2] = ord('D')
    h1[179] = 16
    h1[199] = 0
    header = struct.pack('484b', *h1)
    return header


def _asd_source_data(data_section):
    """
    read asd source binary data
    :param data_section: input binary data without head section
    :return: reflection data
    """
    ref1 = struct.unpack('2151d', data_section.read(17208))
    data_section.read(18)
    cur = data_section.tell()
    ref2 = []
    for i in range(1, 30):
        data_section.seek(cur + i)
        ref2 = struct.unpack('2151d', data_section.read(17208))
        if 0 < abs(max(ref2)) < 1e10 and 0 < abs(min(ref2)) < 1e10:
            break
    return [ref1[i] / ref2[i] for i in range(2151)]


def asd_write(out_file_name, head, data):
    """
    write asd reflection binary data
    :param out_file_name: the output file name
    :param head: file header
    :param data: reflection data
    :return: if success, return 0, else raise IOError
    """
    try:
        if not ".ref" not in out_file_name:
            out_file_name += ".ref"
        out = open(out_file_name, 'wb')
        out.write(head)
        out.write(struct.pack('2151f', *data))
        out.close()
    except IOError:
        raise IOError("Can not write file")
    return 0


def asd_write_csv(data, output_file, header=None, start=350):
    """
    save asd binary data to a csv file
    :param data: input binary asd file
    :param output_file: output csv file name
    :param header: csv file header
    :param start: start band
    :return: 0 if success
    """
    if ".csv" not in output_file:
        output_file += ".csv"

    if header is None:
        header = ["", output_file.split(".")[0]]
    ll = len(data)
    bands = [i + start for i in range(ll)]

    with open(output_file, "w", newline="") as text:
        writer = csv.writer(text)
        writer.writerow(header)
        for row in zip(bands, data):
            writer.writerow(row)
    return 0
