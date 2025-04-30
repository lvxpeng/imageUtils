import os
import sys
import numpy as np
import window_path_convert
from png_read import save_to_nii



def load_npy(path):
    return np.load(path)
if __name__ == '__main__':
    path = r"D:\temp\functional_atlas.npy"
    path = window_path_convert.win_path_convert(path)
    save_path = r"D:/temp/functional_atlas.nii.gz"
    npy = load_npy(path)
    save_to_nii(npy, save_path)
    print(npy.shape)
    print(npy.dtype)
    print(npy)