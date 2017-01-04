# coding=utf-8
import os


# global curdir
curdir = os.path.expanduser("~")
resource = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icondir = os.path.join(resource, "icons")


def setdir(indir):
    global curdir
    curdir = indir


def getdir():
    global curdir
    return curdir
