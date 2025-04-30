import cv2
import numpy as np
import os
from tqdm import tqdm


def apply_mask_to_image(image_path, mask_path, output_path):
    """
    将mask白色部分保留原图颜色，黑色部分设为纯黑
    :param image_path: 原始图像路径
    :param mask_path: 掩码路径
    :param output_path: 输出路径
    """
    # 读取图像和掩码
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # 确保尺寸一致
    if image.shape[:2] != mask.shape[:2]:
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)

    # 二值化掩码（确保严格黑白）
    _, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # 创建结果图像（全黑背景）
    result = np.zeros_like(image)

    # 将mask白色区域的原图像素复制到结果中
    result[binary_mask == 255] = image[binary_mask == 255]

    # 保存结果（无透明通道的RGB图像）
    cv2.imwrite(output_path, result)


def process_folder(input_image_dir, input_mask_dir, output_dir):
    """ 批量处理所有图像 """
    os.makedirs(output_dir, exist_ok=True)
    image_files = [f for f in os.listdir(input_image_dir) if f.endswith('.png')]

    for img_file in tqdm(image_files, desc="Processing"):
        img_path = os.path.join(input_image_dir, img_file)
        mask_path = os.path.join(input_mask_dir, img_file)
        output_path = os.path.join(output_dir, img_file)
        apply_mask_to_image(img_path, mask_path, output_path)





if __name__ == "__main__":
    # 设置路径（请根据实际情况修改）
    input_image_dir = "D:/pythoncode//MesoNet/MesoNet/mesonet/Model_Training_set/U-Net_brain_boundary_model_data/U-Net_model_data/image"  # 原始图像目录
    input_mask_dir = "D:/pythoncode/MesoNet/MesoNet/mesonet/saved/test5/output_mask"  # 掩码图像目录
    output_dir = "D://temp/sav/seg/"  # 输出目录

    # 处理所有图像
    process_folder(input_image_dir, input_mask_dir, output_dir)
    print("Processing completed!")