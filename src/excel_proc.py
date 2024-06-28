import sys
import openpyxl

# 检查是否提供了足够的命令行参数
if len(sys.argv) < 3:
    print("Usage: python script.py excel_file sheet_name start_cell end_cell")
    sys.exit(1)

# 从命令行参数获取Excel文件名、工作表名、起始单元格和结束单元格地址
excel_file = sys.argv[1]
sheet_name = sys.argv[2]
# start_cell = sys.argv[3]
# end_cell = sys.argv[4]

# 打开Excel文件和指定的工作表
workbook = openpyxl.load_workbook(excel_file)
sheet = workbook[sheet_name]

# 计算起始和结束的行号和列号
# start_col, start_row = openpyxl.utils.cell.coordinate_from_string(start_cell)  # 如A1 -> ('A', 1)
# end_col, end_row = openpyxl.utils.cell.coordinate_from_string(end_cell)  # 如A5 -> ('A', 5)

# 初始化一个空列表来存储行号
master_rows = []

# 遍历A列找到所有值为"master"（不区分大小写）的行
for row in sheet['A']:
    if row.value and row.value.lower() == "master":
        master_rows.append(row.row)

# 初始化一个空列表来存储行号
slave_rows = []

# 遍历A列找到所有值为"master"（不区分大小写）的行
for row in sheet['A']:
    if row.value and row.value.lower() == "slave":
        slave_rows.append(row.row)

# 打开文本文件并写入内容
with open('params.txt', 'w') as file:
    i = 0
    for row in master_rows:
        cell_address = f"O{row}"
        cell_value = sheet[cell_address].value
        file.write(f"{f'localparam M{i}_OTN ':<40}{f'= {cell_value}':<40};\n")
        i = i + 1
    i = 0
    for row in slave_rows:
        cell_address = f"O{row}"
        cell_value = sheet[cell_address].value
        file.write(f"{f'localparam S{i}_OTN ':<40}{f'= {cell_value}':<40};\n")
        i = i + 1

# 关闭Excel文件
workbook.close()

print("Contents written to params.txt")