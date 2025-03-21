import os


def rename_images_in_folder(folder_path):
    # 支持的图片扩展名列表
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']

    # 获取所有图片文件
    images = [f for f in os.listdir(folder_path) if any(f.lower().endswith(ext) for ext in image_extensions)]

    # 检查是否有图片文件
    if not images:
        print("没有找到任何图片文件。")
        return

    # 计算需要几位数字来表示所有的图片
    num_images = len(images)
    digits = len(str(num_images - 1))

    # 确保排序正确，避免 '10.jpg' 在 '2.jpg' 之前
    images.sort()

    # 批量重命名图片
    for i, old_name in enumerate(images):
        extension = os.path.splitext(old_name)[1].lower()  # 获取文件扩展名并转换为小写
        new_name = f"img{str(i).zfill(digits)}{extension}"
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)

        try:
            os.rename(old_path, new_path)
            print(f"已重命名: {old_name} -> {new_name}")
        except Exception as e:
            print(f"无法重命名 {old_name}: {e}")


if __name__ == "__main__":
    # 指定包含图片的文件夹路径
    folder_path = r"d:/temp/100-GaM/"  # 替换为实际路径

    # 执行批量重命名
    rename_images_in_folder(folder_path)