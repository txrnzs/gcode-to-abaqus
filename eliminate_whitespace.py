import numpy as np

Delta = 0.1  # 在路径末尾需要延长的长度(mm)
Point_Before = []  # 修改之前的点
Point_Modified = []
filename = 'T275-V10-H0_2(实际大小)_event_series.inp'

with open(filename, 'r') as file:
    lines = file.readlines()  # 逐行读取文件内容

    for line in lines:
        row = line.strip().split(',')  # 文件中的数据以逗号分隔
        Point_Before.append([float(x) for x in row])  # 将每一行数据存储为一个数组，并添加到二维数组中

del Point_Before[-1]  # 删除最后一行数据
t0 = Point_Before[0][0]
for row in Point_Before:
    row[0] = row[0] - t0
    Point_Modified.append([x for x in row])
# 输出二维数组中的数据
numRows = len(Point_Before)
i = 0
while i < numRows - 1:
    startP = Point_Before[i]
    endP = Point_Before[i + 1]
    if (startP[4] > 0) and (startP[3] == endP[3]):  # 如果场变量不为0 并且线段的起始点在一个平面上 那么这两个点需要被修改
        if startP[2] != endP[2]:  # 若同一平面内前后两个点的x坐标存在不同，则修改相应的坐标值
            dY = endP[2] - startP[2]
            if round(dY, 2) > 0:
                Point_Modified[i][2] = Point_Modified[i][2] - dY / abs(dY) * Delta
                Point_Modified[i + 1][2] = Point_Modified[i + 1][2] + dY / abs(dY) * Delta
    i = i + 1

with open('output.inp', 'w') as file:
    for row in Point_Modified:
        line = ','.join(str(element) for element in row)  # 将行中的元素转换为字符串，并用逗号连接
        file.write(line + '\n')  # 将每一行写入文件，并在行末添加换行符

'''
import pandas as pd
df = pd.DataFrame(Point_Modified) # 将数组转换为pandas数据框
df.to_excel("Point_Modified.xlsx") # 将数据框写入excel文件
'''
