import os


def delete_specific_file(root_folder, file_name='slice_seg24.nii.gz'):
    """
    遍历root_folder下的所有子文件夹，找到并删除指定名称的文件。

    :param root_folder: 根目录路径，字符串类型
    :param file_name: 要删除的文件名，默认为'slice_orig.nii.gz'
    """
    # 检查根目录是否存在
    if not os.path.exists(root_folder):
        print(f"指定的根目录'{root_folder}'不存在。")
        return

    deleted_files = 0
    # 使用os.walk递归地遍历所有子目录
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename == file_name:
                file_path = os.path.join(foldername, filename)
                try:
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
                    deleted_files += 1
                except Exception as e:
                    print(f"无法删除文件'{file_path}': {e}")

    if deleted_files == 0:
        print(f"没有找到名为'{file_name}'的文件。")
    else:
        print(f"总共删除了{deleted_files}个文件。")


# 设置你的根目录路径
root_folder = "D:/idmdownload/neurite-oasis.v1.0/"

# 调用函数
delete_specific_file(root_folder)