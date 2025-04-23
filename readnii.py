import numpy as np  # 转换格式
import nibabel as nib   # 读取数据
import matplotlib.pyplot as plt # 单张图像展示
from nibabel.viewers import OrthoSlicer3D   # nii.gz展示
import matplotlib
matplotlib.use('TkAgg') # 用于滚动查看nii.gz

# 使用 nibabel库读取图像
image_path = r"D:/pythoncode/Registration-CorrMLP/CorrMLP/2D/test/moved/23_slice_norm.nii.gz"
image_obj = nib.load(image_path)
print(f'文件路径： {image_path}')
print(f'图像类型： {type(image_obj)}')

# 提取numpy数组
image_data = image_obj.get_fdata()
# print(type(image_data))

# 查看图像大小
depth, height, width = image_data.shape
print(f"The image object height: {height}, width:{width}, depth:{depth}")
# height, width = image_data.shape
# print(f"The image object height: {height}, width:{width}")

# 查看图像值范围
print(f'image value range: [{image_data.min()}, {image_data.max()}]')

# 可视化图像
OrthoSlicer3D(image_obj.dataobj).show()

# 查看图像成像信息
print(image_obj.header.keys())

# 图像分辨率信息
pixdim =  image_obj.header['pixdim']
# print(f'z轴分辨率： {pixdim[3]}')
print(f'in plane 分辨率： {pixdim[1]} * {pixdim[2]}')

# 依据层厚信息，以及矩阵大小，就可以求出实际的扫描范围。
# z_range = pixdim[3] * depth
x_range = pixdim[1] * height
y_range = pixdim[2] * width
# print(f'扫描范围：', x_range, y_range, z_range)
print(f'扫描范围：', x_range, y_range)

# 查看指定层slice图像
# maxval = 140
# i = np.random.randint(0, maxval)
# # Define a channel to look at
# print(f"Plotting z Layer {i} of Image")
# plt.imshow(image_data[:, :, i], cmap='gray')
# plt.axis('off'); # 关闭网格
# plt.show()


# 读取标签数据
label_path = "C:/Users/asus/Desktop/neurite-oasis.2d.v1.0/OASIS_OAS1_0205_MR1/slice_seg24.nii.gz"
label_obj = nib.load(label_path)
label_array = label_obj.get_fdata()
print(f'label_path: {label_path}')
# 查看label里面有几种值
print(f'标签中有几种值: {np.unique(label_array)}')

# 查看每个标签对应多少像素
print(f'每个标签像素数量：',np.unique(label_array, return_counts=True))


import nibabel as nib
import numpy as np
try:
    # img = nib.load('D:/pythoncode/Registration-CorrMLP/CorrMLP/2D/test/saved/22_slice_norm_warped.nii.gz')
    img = nib.load('D:/idmdownload/neurite-oasis.v1.0/OASIS_OAS1_0377_MR1/aligned_norm.nii.gz')
    data = img.get_fdata()
    print("Successfully loaded.")
    print("Shape:", data.shape)
    print("Data type:", data.dtype)
    print("Min value:", np.min(data))
    print("Max value:", np.max(data))
except Exception as e:
    print(f"Error loading file with nibabel: {e}")


