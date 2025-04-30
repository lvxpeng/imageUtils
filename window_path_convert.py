import os
import sys


def win_path_convert(path):
    '''window路径转化为linux路径，\转化为/'''
    if sys.platform == 'win32':
        path = path.replace('\\', '/')
    return path


