import os
import shutil

from PIL import Image


def rename_and_move_files(src_root, dst_root):
    norm_dir = os.path.join(dst_root, 'norm')
    seg_dir = os.path.join(dst_root, 'seg')

    # 创建输出文件夹
    if not os.path.exists(norm_dir):
        os.makedirs(norm_dir)
    if not os.path.exists(seg_dir):
        os.makedirs(seg_dir)

    file_count = {'norm': 1, 'seg': 1}

    # 遍历源目录中的所有文件夹和文件
    for dirpath, _, filenames in os.walk(src_root):
        for filename in filenames:
            if filename == 'slice_norm.nii.gz':
                src_file = os.path.join(dirpath, filename)
                new_filename = f"{file_count['norm']}_slice_norm.nii.gz"
                dst_file = os.path.join(norm_dir, new_filename)
                shutil.copy(src_file, dst_file)
                file_count['norm'] += 1

            elif filename == 'slice_seg24.nii.gz':
                src_file = os.path.join(dirpath, filename)
                new_filename = f"{file_count['seg']}_slice_norm_seg.nii.gz"
                dst_file = os.path.join(seg_dir, new_filename)
                shutil.copy(src_file, dst_file)
                file_count['seg'] += 1


if __name__ == "__main__":
    source_root = "C:/Users/asus\Desktop/neurite-oasis.2d.v1.0"  # 输入你的源文件夹路径
    destination_root = "C:/Users/asus/Desktop/outputnii"  # 输入你的目标文件夹路径

    rename_and_move_files(source_root, destination_root)