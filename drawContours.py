import cv2
import matplotlib.pyplot as plt
import numpy as np

def load_image(image_path, mode=cv2.IMREAD_GRAYSCALE):
    """加载图像并校验是否成功"""
    image = cv2.imread(image_path, mode)
    if image is None:
        raise ValueError(f"无法加载图像：{image_path}")
    return image

def validate_and_resize(gray_image, atlas_mask):
    """验证图像尺寸一致性，必要时调整尺寸"""
    mask_size = atlas_mask.shape[:2]  # (height, width)
    image_size = gray_image.shape[:2]

    if mask_size != image_size:
        print(f"{image_path} 的尺寸为：{image_size}")
        print(f"{mask_path} 的尺寸为：{mask_size}")
        resized_image = cv2.resize(gray_image, (mask_size[1], mask_size[0]))
        print(f"调整后的 {image_path} 尺寸为：{resized_image.shape[:2]}")
        return resized_image
    return gray_image

def binarize_image(atlas_mask):
    """将图谱二值化"""
    # atlas_mask = cv2.cvtColor(atlas_mask, cv2.COLOR_RGB2GRAY)
    _, binary_atlas = cv2.threshold(atlas_mask, 128, 255, cv2.THRESH_BINARY)
    cv2.imshow('Binary Atlas', binary_atlas)
    return binary_atlas

def clean_image(image):
    """对灰度图像进行一些基本的清理操作"""
    # 定义形态学操作的核
    kernel = np.ones((5, 5), np.uint8)

    # 先腐蚀后膨胀（开运算）
    cleaned_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    # 或者先膨胀后腐蚀（闭运算）
    # cleaned_image = cv2.morphologyEx(cleaned_image, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('Cleaned Image', cleaned_image)
    return cleaned_image
def extract_contours(binary_image):
    """提取二值图像的轮廓"""
    try:
        contours,  Hierarchy = cv2.findContours(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        print('contours:',contours)
        print('The number of Coutours:{}'.format(len(contours)))
        if not contours:
            print("警告：未检测到任何轮廓！")
        return contours
    except Exception as e:
        raise RuntimeError("轮廓提取失败") from e

def draw_contours(gray_image, contours):
    """在灰度图像上绘制轮廓"""
    color_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(color_image, contours, -1, (0, 0, 255), 1)  # 红色轮廓，线宽1
    return color_image

def save_and_display_result(color_image, output_path="mapped_result.png"):
    """保存结果图像并显示"""
    try:
        cv2.imwrite(output_path, color_image)
        print(f"结果已保存至：{output_path}")
    except Exception as e:
        print(f"保存图像失败：{e}")

    # 显示结果（可选）
    cv2.imshow('Mapped Brain Regions', color_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 主流程
if __name__ == "__main__":
    image_path = r'd:/temp/images/0.png'
    mask_path = r'd:/temp/atlas.png'
    output_path = 'mapped_result.png'

    try:
        # 1. 加载图像
        gray_image = load_image(image_path, cv2.IMREAD_GRAYSCALE)
        atlas_mask = load_image(mask_path, cv2.IMREAD_GRAYSCALE)

        # 2. 验证尺寸一致并调整
        gray_image = validate_and_resize(gray_image, atlas_mask)

        # 3. 二值化图谱
        binary_atlas = binarize_image(atlas_mask)

        binary_atlas = clean_image(binary_atlas)

        # 4. 提取轮廓
        contours = extract_contours(binary_atlas)

        # 5. 绘制轮廓
        color_image = draw_contours(gray_image, contours)

        # 6. 保存并显示结果
        # save_and_display_result(color_image, output_path)

        cv2.imshow('Mapped Brain Regions', color_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"程序运行时发生错误：{e}")
