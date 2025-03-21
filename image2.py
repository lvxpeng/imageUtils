from PIL import Image

def make_white_transparent(input_image_path, output_image_path):
    # 打开图像
    image = Image.open(input_image_path).convert("RGBA")
    datas = image.getdata()

    new_data = []
    for item in datas:
        # 如果像素是白色 (255, 255, 255)，则将其透明度设为 0
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    # 更新图像数据
    image.putdata(new_data)
    # 保存图像
    image.save(output_image_path, "PNG")
def augment_image(image_path,output_path):
        image = Image.open(image_path)
        image = image.resize((512, 512),Image.LANCZOS)
        image.save(output_path)


# 示例调用
input_image_path = "d:/temp/atlas.png"
output_image_path = "d:/temp/aug_atlas.png"
augment_image(input_image_path,output_image_path)
# make_white_transparent(input_image_path, output_image_path)
