import re
import glob
import os
import cv2
import numpy as np
import SimpleITK as sitk
from PIL import Image
import tifffile as tif
import logging

from skimage import io
from skimage.transform import resize
from skimage.util import img_as_ubyte

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Convert2Nii:
    def __init__(self):
        pass

    def _check_paths(self, input_path, output_path):
        """检查输入输出路径"""
        if not os.path.exists(input_path):
            logging.error("Input path does not exist: %s", input_path)
            raise FileNotFoundError(f"Input path does not exist: {input_path}")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logging.info("Created output directory: %s", output_path)

    def png2nii_from_array(self, allpng_array, output_path):
        """将图像数组转换为NII文件"""
        # self._check_paths('', output_path)  # 传递空字符串作为占位符，因为不再需要检查输入路径

        if not allpng_array:
            logging.warning("No valid PNG files found in the input path.")
            return

        logging.info("Total PNG files processed: %d", len(allpng_array))
        png_array = np.array(allpng_array)
        out_nii = sitk.GetImageFromArray(png_array)
        index = save2output(self,output_path= output_path)
        output_file = os.path.join(output_path, '{}out.nii.gz'.format(index+1))
        sitk.WriteImage(out_nii, output_file)
        logging.info("NII file saved to: %s", output_file)


    def png2nii(self, input_path, output_path):
        """将PNG文件转换为NII文件"""
        self._check_paths(input_path, output_path)

        allpng_array = []
        for png in sorted(os.listdir(input_path)):
            if png.lower().endswith('.png'):
                png_path = os.path.join(input_path, png)
                try:
                    png_image = cv2.imread(png_path)
                    if png_image is None:
                        logging.warning("Failed to read PNG file: %s", png_path)
                        continue
                    if png_image.shape[:2] != (512, 512):
                        png_image = cv2.resize(png_image, (512, 512))
                    png_array = Image.fromarray(png_image).convert('L')
                    allpng_array.append(np.array(png_array, dtype=np.uint8))
                except Exception as e:
                    logging.error("Error processing PNG file %s: %s", png_path, str(e))

        if not allpng_array:
            logging.warning("No valid PNG files found in the input path.")
            return

        logging.info("Total PNG files processed: %d", len(allpng_array))
        png_array = np.array(allpng_array)
        out_nii = sitk.GetImageFromArray(png_array)
        index = save2output(self, output_path)
        output_file = os.path.join(output_path, '{}out.nii.gz'.format(index+1))
        sitk.WriteImage(out_nii, output_file)
        logging.info("NII file saved to: %s", output_file)



    def tif2nii(self, input_path, output_path):
      """将TIFF文件转换为NII文件"""
      # outpath = os.path.join(output_path, 'tif_to_image')
      if not os.path.exists(output_path):
          os.makedirs(output_path)
      alltif_array = []
      tif_list = glob.glob(os.path.join(input_path, '*.tif'))
      if tif_list:
          tif_satck = tif.imread(tif_list[0])
          num_images = len(tif_satck)
          for i in  range (num_images):
                tif_image = tif_satck[i]
                if tif_image.shape[:2] != (512, 512):
                    tif_image = resize(tif_image, (512, 512))
                tif_image = img_as_ubyte(tif_image)
                alltif_array.append(tif_image)
                # io.imsave(os.path.join(outpath, f'{i}.png'), tif_image)
      else:
          logging.warning("No valid TIF files found in the input path.")
          return
      self.png2nii_from_array(alltif_array, output_path)



def save2output(self, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        logging.info("Created output directory: %s", output_path)

    max_number = -1
    for file_name in sorted(os.listdir(output_path)):
        if file_name.lower().endswith('.nii.gz'):
            # 使用正则表达式提取文件名中的数字部分
            match = re.search(r'(\d+)', file_name)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number

    # logging.info("The largest number found in .nii.gz files is: %d", max_number)
    return max_number




if __name__ == '__main__':
    input_path = 'D:/temp/tif'
    output_path = 'D:/temp/images/gzsave'
    convert2nii = Convert2Nii()
    try:
        # convert2nii.png2nii(input_path, output_path)
        convert2nii.tif2nii(input_path, output_path)
    except Exception as e:

        logging.error("An error occurred during PNG to NII conversion: %s", str(e))

