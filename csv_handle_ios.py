import csv

# 读取CSV文件
input_file = 'D:/deeplabcut/gcampandios-zju-2025-03-08/labeled-data/multi/S2 MUT 7I/CollectedData_zju.csv'
# output_file = 'D:/deeplabcut/gcampandios-zju-2025-03-08/labeled-data/multi/O1 MUT 7I/CollectedData_zju.csv'

output_file = input_file
# 打开CSV文件并读取内容
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    rows = list(reader)

# 在第二行插入空白行
rows.insert(1, [])

# 在A2插入字段"individuals"
rows[1].insert(0, 'individuals')

# 在D列之前插入18列空白列
for row in rows:
    row[3:3] = [''] * 18  # 在索引3处插入18个空字符串

# 填充字段
# D1到U1填入字段zju
rows[0][3:21] = ['zju'] * 18

# D2到U2填入字段gcamp
rows[1][3:21] = ['gcamp'] * 18

# V2到AM2填入字段ios
rows[1][21:39] = ['ios'] * 18

# D3到U3填入a,a,b,b,c,c,d,d,e,e,f,f,g,g,h,h,i,i
pattern3 = ['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd', 'e', 'e', 'f', 'f', 'g', 'g', 'h', 'h', 'i', 'i']
rows[2][3:21] = pattern3

# D4到U4填入x,y,x,y,x,y,x,y,x,y,x,y,x,y,x,y,x,y
pattern4 = ['x', 'y'] * 9
rows[3][3:21] = pattern4

# 写入修改后的内容到新的CSV文件
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)

print(f"处理完成，结果已保存到 {output_file}")


