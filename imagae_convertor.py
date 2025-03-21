import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import numpy as np
from PIL import Image, ImageSequence
import cv2
import os
import tifffile
import shutil

class TifConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TIF Converter")
        self.file_path = ""

        # Import TIF Button
        btn_import_tif = tk.Button(root, text="导入TIF", command=self.import_tif)
        btn_import_tif.pack(pady=10)

        # Convert to Images Button
        btn_convert_images = tk.Button(root, text="转换为图片", command=self.convert_to_images)
        btn_convert_images.pack(pady=10)

        # Convert to Video Button
        btn_convert_video = tk.Button(root, text="转换为视频", command=self.convert_to_video)
        btn_convert_video.pack(pady=10)

        # Open Image Directory Button
        self.btn_open_image_dir = tk.Button(root, text="打开图片目录", state=tk.DISABLED, command=self.open_image_directory)
        self.btn_open_image_dir.pack(pady=10)

        # Open Video Directory Button
        self.btn_open_video_dir = tk.Button(root, text="打开视频目录", state=tk.DISABLED, command=self.open_video_directory)
        self.btn_open_video_dir.pack(pady=10)

    def import_tif(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("TIF/TIFF files", "*.tif;*.tiff")])
        if not self.file_path:
            messagebox.showwarning("警告", "没有选择文件")
        else:
            messagebox.showinfo("信息", f"选择了文件: {self.file_path}")

    def convert_to_images(self):
        if not self.file_path:
            messagebox.showwarning("警告", "请先导入TIF文件")
            return

        output_dir = os.path.join(os.path.dirname(self.file_path), 'tif_to_image')
        os.makedirs(output_dir, exist_ok=True)

        with Image.open(self.file_path) as im:
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                frame.save(os.path.join(output_dir, f"{i}.png"))

        messagebox.showinfo("完成", "图片转换完成")
        self.btn_open_image_dir.config(state=tk.NORMAL)

    def convert_to_video(self):
        if not self.file_path:
            messagebox.showwarning("警告", "请先导入TIF文件")
            return

        # 提取文件名（不带扩展名）用于视频文件命名
        file_name_without_ext = os.path.splitext(os.path.basename(self.file_path))[0]
        temp_image_dir = os.path.join(os.path.dirname(self.file_path), 'temp_images')
        video_dir = os.path.join(os.path.dirname(self.file_path), 'tif_to_video')
        os.makedirs(temp_image_dir, exist_ok=True)
        os.makedirs(video_dir, exist_ok=True)
        video_path = os.path.join(video_dir, f"{file_name_without_ext}.avi")

        # 先转换成图片并保存到临时文件夹
        with Image.open(self.file_path) as im:
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                frame.save(os.path.join(temp_image_dir, f"{i}.png"))

        images = [img for img in sorted(os.listdir(temp_image_dir)) if img.endswith(".png")]
        if not images:
            messagebox.showwarning("警告", "无法找到转换后的图片")
            shutil.rmtree(temp_image_dir, ignore_errors=True)
            return

        # 检查第一个图片是否可以被正确读取
        first_image_path = os.path.join(temp_image_dir, images[0])
        frame = cv2.imread(first_image_path)
        if frame is None:
            messagebox.showerror("错误", f"无法读取图片: {first_image_path}")
            shutil.rmtree(temp_image_dir, ignore_errors=True)
            return

        height, width, layers = frame.shape
        size = (width, height)

        out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'),30, size)

        for image in images:
            img_path = os.path.join(temp_image_dir, image)
            frame = cv2.imread(img_path)
            if frame is None:
                messagebox.showerror("错误", f"无法读取图片: {img_path}")
                out.release()
                shutil.rmtree(temp_image_dir, ignore_errors=True)
                return

            out.write(frame)

        out.release()
        shutil.rmtree(temp_image_dir, ignore_errors=True)  # 清理临时文件夹
        messagebox.showinfo("完成", f"视频 {file_name_without_ext}.avi 转换完成")
        self.btn_open_video_dir.config(state=tk.NORMAL)
    # def convert_to_video(self):
    #     if not self.file_path:
    #         messagebox.showwarning("警告", "请先导入TIF文件")
    #         return
    #
    #     file_name_without_ext = os.path.splitext(os.path.basename(self.file_path))[0]
    #     video_dir = os.path.join(os.path.dirname(self.file_path), 'tif_to_video')
    #     os.makedirs(video_dir, exist_ok=True)
    #     video_path = os.path.join(video_dir, f"{file_name_without_ext}.avi")
    #
    #     with tifffile.TiffFile(self.file_path) as tif:
    #         pages = tif.pages
    #         first_page = pages[0].asarray()
    #
    #         # 检查并处理可能存在的Alpha通道
    #         if len(first_page.shape) == 3 and first_page.shape[2] > 3:
    #             first_page = first_page[:, :, :3]  # 只取前三通道（RGB）
    #
    #         # 确保图像数据是uint8类型
    #         if first_page.dtype != 'uint8':
    #             first_page = (first_page * 255).astype(np.uint8)
    #
    #         # 根据图像的形状确定高度、宽度和图层数量
    #         if len(first_page.shape) == 2:  # 如果是灰度图像
    #             height, width = first_page.shape
    #             layers = 1
    #             print(f"First frame is grayscale: shape={first_page.shape}, dtype={first_page.dtype}")
    #         else:  # 如果是彩色图像
    #             height, width, layers = first_page.shape
    #             print(f"First frame is color: shape={first_page.shape}, dtype={first_page.dtype}")
    #
    #         size = (width, height)
    #
    #         out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'DIVX'), 20, size, isColor=layers > 1)
    #
    #         for page in pages:
    #             frame = page.asarray()
    #
    #             # 检查并处理可能存在的Alpha通道
    #             if len(frame.shape) == 3 and frame.shape[2] > 3:
    #                 frame = frame[:, :, :3]
    #
    #             # 确保每一帧都是uint8类型
    #             if frame.dtype != 'uint8':
    #                 frame = (frame * 255).astype(np.uint8)
    #
    #             # 如果是灰度图像，则增加通道
    #             if len(frame.shape) == 2:
    #                 frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    #
    #             bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) if layers > 1 else frame
    #             out.write(bgr_frame)
    #
    #             print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}, min: {frame.min()}, max: {frame.max()}")
    #
    #         out.release()
    #
    #     messagebox.showinfo("完成", f"视频 {file_name_without_ext}.avi 转换完成")
    #     self.btn_open_video_dir.config(state=tk.NORMAL)

    def open_image_directory(self):
        image_dir = os.path.join(os.path.dirname(self.file_path), 'tif_to_image')
        if os.path.exists(image_dir):
            os.startfile(image_dir)

    def open_video_directory(self):
        video_dir = os.path.join(os.path.dirname(self.file_path), 'tif_to_video')
        if os.path.exists(video_dir):
            os.startfile(video_dir)


if __name__ == "__main__":
    root = tk.Tk()
    app = TifConverterApp(root)
    root.mainloop()