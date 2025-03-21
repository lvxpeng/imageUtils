import os
from PIL import Image


def rotate_images_in_place(directory):
    # 初始化旋转角度和计数器
    rotation_angle = 3
    counter = 0

    # 遍历指定目录中的所有文件
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(directory, filename)

            try:
                with Image.open(file_path) as img:
                    # 第一张图片不旋转
                    if counter == 0:
                        rotated_img = img
                    elif counter % 2 == 1:  # 对于奇数索引（第二张，第四张...），左旋
                        rotated_img = img.rotate(rotation_angle * (counter // 2 + 1), expand=True)
                    else:  # 对于偶数索引（第三张，第五张...），右旋
                        rotated_img = img.rotate(-rotation_angle * (counter // 2), expand=True)

                    # 保存旋转后的图像到原位置
                    rotated_img.save(file_path)
                    print(f"Processed and replaced {filename}")

                # 增加计数器
                counter += 1

            except IOError:
                print(f"Cannot process image file {filename}")


# 使用函数
image_directory = 'D:/deeplabcut/iosandgcamp-zju-2025-01-09/labeled-data/S2 MUT 5'  # 替换为你的图片目录路径
rotate_images_in_place(image_directory)