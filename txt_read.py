# 假设文件名为 data.txt
file_path = "D:/idmdownload/FIRE/Ground Truth/control_points_A01_1_2.txt"

# 初始化一个空列表来存储每一行的数据
data_list = []

# 打开文件并读取内容
with open(file_path, 'r') as file:
    for line in file:
        # 去除行末的换行符，并按空格分割数据
        row = tuple(map(float, line.strip().split()))
        # 将每一行的数据添加到列表中
        data_list.append(row)

# 将列表转换为元组
data_tuple = tuple(data_list)

# 输出结果
print(data_tuple)
print(data_tuple[0][1])
