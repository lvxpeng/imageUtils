import os
import cv2
from PIL import Image
import numpy as np
import nibabel as nb
from Convert2Nii import save2output
from window_path_convert import win_path_convert


def read_png(path):
    # img = cv2.imread(path)
    img = Image.open(path).convert('L')
    img = np.array(img, dtype=np.float32)[..., np.newaxis]
    img = img / 255.0
    return img
# def save_to_nii(img_numpy, save_path, pixel_size = 0.01):
#     # affine = np.diag([pixel_size, pixel_size,  1.0, 1.0])
#     affine = np.array([
#         [0, -0.055, 0, 0],  # X 轴指向原始图像的「左→右」（但用负号翻转 Y）
#         [0.055, 0, 0, 0],  # Y 轴指向原始图像的「上→下」
#         [0, 0, 1, 0],  # Z 轴不变
#         [0, 0, 0, 1]
#     ])
#     new_img = nb.nifti1.Nifti1Image(img_numpy, affine)
#     save_path = os.path.join(save_path)
#     nb.save(new_img, save_path)
def save_to_nii(img_numpy, save_path, pixel_size=0.025):
    # 原始 affine 矩阵（假设是2D图像）
    base_affine = np.array([
        [0, -pixel_size, 0, 0],
        [pixel_size, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # 绕 X 轴旋转 180 度的旋转矩阵
    Rx_180 = np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1]
    ])

    # 对 affine 的线性变换部分应用旋转（前乘）
    new_linear = Rx_180 @ base_affine[:3, :3]
    new_translation = base_affine[:3, 3]

    # 构建新的 affine 矩阵
    new_affine = np.eye(4)
    new_affine[:3, :3] = new_linear
    new_affine[:3, 3] = new_translation

    # 创建并保存 NIfTI 文件
    new_img = nb.nifti1.Nifti1Image(img_numpy, new_affine)
    nb.save(new_img, save_path)

def mutil_images_to_nii(path, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    img_list = os.listdir(path)
    for img in img_list:
        img_path = os.path.join(path, img)
        img_numpy = read_png(img_path)
        image_size = img_numpy.shape
        index = save2output(self=None, output_path=save_path)
        save_index = os.path.join(save_path, f"{index+1}_norm.nii.gz")
        if image_size[:2] != (512,512):
            image_size = cv2.resize(img_numpy, (512, 512), Image.LANCZOS)
            save_to_nii(image_size, save_index)
        else:
            save_to_nii(img_numpy, save_index)


if __name__ == '__main__':
    path = r"D:\temp\sav\seg"
    path = win_path_convert(path)
    save_path = "D:/temp/sav/gcamp2/"
    mutil_images_to_nii(path, save_path)
    # save_to_nii(read_png(path), save_path)
