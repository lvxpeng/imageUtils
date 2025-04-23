import os
import nibabel as nib
import numpy as np
from PIL import Image


def convert_nifti_to_png(root_folder):
    """
    遍历root_folder下的所有子文件夹，找到slice_norm.nii.gz和slice_seg4.nii.gz，
    并将其转换为PNG格式保存到原nii.gz文件所在的文件夹。

    :param root_folder: 根目录路径，字符串类型
    """
    # 检查根目录是否存在
    if not os.path.exists(root_folder):
        print(f"指定的根目录'{root_folder}'不存在。")
        return

    converted_files = 0
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == 'slice_norm.nii.gz' or filename == 'slice_seg4.nii.gz':
                file_path = os.path.join(foldername, filename)
                try:
                    # 加载NIfTI文件
                    img = nib.load(file_path)
                    # 获取数据并假设是2D的
                    data = img.get_fdata()
                    if len(data.shape) > 2 and data.shape[2] == 1:
                        # 如果是3D数据且第三个维度大小为1，则进行挤压
                        data = np.squeeze(data)

                    # 确保是2D数据
                    if len(data.shape) != 2:
                        print(f"文件{file_path}不是2D图像，跳过转换。")
                        continue

                    # 将数据归一化到0-255范围，并转换为uint8类型
                    data_normalized = ((data - data.min()) / (data.max() - data.min()) * 255).astype(np.uint8)
                    data_rotated = np.rot90(data_normalized, k=-1)

                    # 使用PIL生成图像并保存到与nii.gz文件相同的文件夹中
                    image = Image.fromarray(data_rotated)
                    png_filename = filename.replace('.nii.gz', '.png')
                    save_path = os.path.join(foldername, png_filename)
                    image.save(save_path)
                    print(f"已转换并保存: {save_path}")
                    converted_files += 1
                except Exception as e:
                    print(f"无法处理文件'{file_path}': {e}")

    if converted_files == 0:
        print("没有找到需要转换的文件。")
    else:
        print(f"总共转换了{converted_files}个文件。")




# 设置你的根目录路径
root_folder = 'C:/Users/asus/Desktop/neurite-oasis.2d.v1.0'

# 调用函数
convert_nifti_to_png(root_folder)