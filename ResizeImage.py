import os
from PIL import Image


def save_resize_img(img_path, img_path_train, width, height):
    # 确保输出目录存在
    if not os.path.exists(img_path_train):
        os.makedirs(img_path_train)

    for filename in os.listdir(img_path):
        image_path = os.path.join(img_path, filename)
        try:
            with Image.open(image_path) as img:
                # 使用 LANCZOS 作为抗锯齿算法
                img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
                # 确保文件路径正确拼接
                save_path = os.path.join(img_path_train, filename)
                img_resized.save(save_path)
                print(f"Resized and saved {filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")


if __name__ == '__main__':
    save_resize_img("D:/temp/json_to_mask", "D:/temp/json_to_mask/512/", 512, 512)