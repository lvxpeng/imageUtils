import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw
import json
import os

# 全局变量定义
polygons = []
numFound = 0
filename = ''
imageWidth = 0
imageHeight = 0
bgcolor = (0, 0, 0)  # 背景颜色为白色
fgcolor = (255, 255, 255)  # 前景色（多边形填充色）为黑色
savedir = ''
selected_json_file = None


def generateImage(filename, preview=False, save=True):
    global savedir
    img = Image.new('RGB', (imageWidth, imageHeight), bgcolor)
    draw = ImageDraw.Draw(img)
    for polygon in polygons:
        draw.polygon(polygon, fill=fgcolor)
    if preview:
        print('Opening preview')
        img.show()
    if save:
        mask_dir = os.path.join(savedir, 'mask')
        os.makedirs(mask_dir, exist_ok=True)
        print('Saving image ' + filename)
        img.save(os.path.join(mask_dir, filename))


def parseJSON(file):
    global polygons, numFound, filename, imageWidth, imageHeight, savedir
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    imageHeight = data['imageHeight']
    imageWidth = data['imageWidth']
    polygons = []  # 清空之前的多边形数据
    for shape in data['shapes']:
        points = [(float(point[0]), float(point[1])) for point in shape['points']]
        polygons.append(points)


def select_json_file():
    global selected_json_file, savedir
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        savedir = os.path.dirname(file_path)
        selected_json_file = file_path
        label_file["text"] = "Selected JSON: " + os.path.basename(file_path)


def convert_to_mask():
    global selected_json_file
    if not selected_json_file:
        messagebox.showwarning("警告", "请先选择一个JSON文件")
        return

    try:
        parseJSON(selected_json_file)
        base_filename = os.path.splitext(os.path.basename(selected_json_file))[0] + '.png'
        generateImage(base_filename, save=True)
        messagebox.showinfo("完成", "Mask生成完成")
    except Exception as e:
        messagebox.showerror("错误", str(e))


def open_mask_directory():
    mask_dir = os.path.join(savedir, 'mask')
    if os.path.exists(mask_dir) and os.path.isdir(mask_dir):
        os.startfile(mask_dir)
    else:
        messagebox.showwarning("警告", "Mask文件夹不存在")


class MaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mask Generator")

        # Label to display the selected JSON file path
        global label_file
        label_file = tk.Label(root, text="No file selected")
        label_file.pack(pady=10)

        # Select JSON File Button
        btn_select_json = tk.Button(root, text="选择JSON文件", command=select_json_file)
        btn_select_json.pack(pady=10)

        # Convert to Mask Button
        btn_convert_mask = tk.Button(root, text="转换为Mask", command=convert_to_mask)
        btn_convert_mask.pack(pady=10)

        # Open Mask Directory Button
        btn_open_mask_dir = tk.Button(root, text="打开Mask目录", command=open_mask_directory)
        btn_open_mask_dir.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MaskGeneratorApp(root)
    root.mainloop()