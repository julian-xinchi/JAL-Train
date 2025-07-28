def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        # 读取整个文件内容
        file_content = file.read()
    return file_content

#def extract_matrix_and_count_ones(file_content):
#    start_marker = "//SD_AXB_DEFINE_begin"
#    end_marker = "//SD_AXB_DEFINE_end"
#
#    start_index = file_content.find(start_marker) + len(start_marker)
#    end_index = file_content.find(end_marker)
#    matrix_content = file_content[start_index:end_index].strip()
#
#    matrix = [list(line) for line in matrix_content.splitlines() if line]
#
#    # 统计每行中'1'的数量
#    row_counts = [row.count('1') for row in matrix]
#
#    # 统计每列中'1'的数量
#    col_counts = [sum(1 for row in matrix if row[col] == '1') for col in range(len(matrix[0]))]
#
#    return matrix, row_counts, col_counts

def extract_matrix_and_count_ones(file_content):
    start_marker = "//SD_AXB_DEFINE_begin"
    end_marker = "//SD_AXB_DEFINE_end"

    # 定位开始和结束标记
    start_index = file_content.find(start_marker) + len(start_marker)
    end_index = file_content.find(end_marker)

    # 提取标记之间的内容
    matrix_content = file_content[start_index:end_index].strip()

    # 分割每一行，并去除行首的 "//" 和逗号
    matrix = [line.replace('//', '').replace(',', '').strip() for line in matrix_content.splitlines() if line]

    # 将字符串转换为列表的形式
    matrix = [list(row) for row in matrix]

    # 统计每行中'1'的数量
    row_counts = [row.count('1') for row in matrix]

    # 统计每列中'1'的数量
    col_counts = [sum(1 for row in matrix if row[col] == '1') for col in range(len(matrix[0]))]

    return matrix, row_counts, col_counts

# File path
input_matrix_file_path = 'input_matrix.t'

# Read and process the matrix
file_content = read_matrix_from_file(input_matrix_file_path)
matrix, row_counts, col_counts = extract_matrix_and_count_ones(file_content)

# Print results
print("Matrix:")
for row in matrix:
    print(row)
print("Row counts:", row_counts)
print("Column counts:", col_counts)
print("Matrix row 0:")
print(matrix[0])

def find_nth_one(matrix, row_index, col_index):
    if matrix[row_index][col_index] != '1':
        return None, None  # 如果指定位置不是 '1'，返回 None

    # 在指定行中计算 '1' 的位置
    row_ones_count = matrix[row_index][:col_index].count('1') + 1

    # 在指定列中计算 '1' 的位置
    col_ones_count = sum(1 for i in range(row_index) if matrix[i][col_index] == '1') + 1

    return row_ones_count, col_ones_count


row_index = 1  # 第二行
col_index = 2  # 第三列
row_nth, col_nth = find_nth_one(matrix, row_index, col_index)

if row_nth is not None and col_nth is not None:
    print(f"The '1' at position ({row_index}, {col_index}) is the {row_nth}th '1' in the row and the {col_nth}th '1' in the column.")
else:
    print(f"The position ({row_index}, {col_index}) is not a '1'.")

cons = 10
text = "hello world {} {{".format(cons)
formatted_string = f"{text}}}"
print(formatted_string)
text = f"{{"
xx = len(text)
print(xx)

def find_ones_in_row_and_columns(matrix, selected_row, selected_columns):
    # 获取选定行中所有'1'的索引
    row_ones_indices = [col_index for col_index, value in enumerate(matrix[selected_row]) if value == '1']

    # 获取所有选定列中'1'的索引
    columns_ones_indices = [row_index for row_index, row in enumerate(matrix) if row[selected_columns] == '1']

    return row_ones_indices, columns_ones_indices

# Example usage:
selected_row = 1  # 例如，我们选择第二行（索引为1）
selected_columns = 2  # 例如，我们选择第一列和第三列（索引为0和2）

matrix = [
    ['0', '1', '0', '1'],
    ['1', '0', '1', '1'],
    ['0', '1', '0', '0']
]

row_ones_indices, columns_ones_indices = find_ones_in_row_and_columns(matrix, selected_row, selected_columns)
print("Indices of '1's in the selected row:", row_ones_indices)
row_ones_indices_size = len(row_ones_indices)
print("Size of '1's in the selected row:", row_ones_indices_size)
print("Indices of '1's in the selected columns:", columns_ones_indices)
 