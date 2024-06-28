## 打开原始的 Verilog 文件
#with open('original.v', 'r', encoding='utf-8') as f:
#    contents = f.readlines()
#
## 删除代码逻辑部分
#new_contents = []
#found_module = False
#for line in contents:
#    if not found_module:
#        if 'module' in line:
#            found_module = True
#            new_contents.append(line)
#        else:
#            new_contents.append(line)
#    else:
#        if 'endmodule' in line:
#            found_module = False
#            new_contents.append(line)
#        elif 'output' in line:
#            # 对 output 端口赋值为 0
#            new_contents.append(line.split()[0] + ' ' + line.split()[1] + ' 0;\n')
#        else:
#            continue
#
## 将处理后的 Verilog 内容写入新文件
#with open('processed.v', 'w') as f:
#    f.writelines(new_contents)

# 打开原始的 Verilog 文件
with open('original.v', 'r', encoding='utf-8') as f:
    contents = f.readlines()

# 保留端口定义部分
new_contents = []
found_ports = False
for line in contents:
    if 'module' in line:
        found_ports = True
    if found_ports:
        if '(' in line and ')' in line:
            new_contents.append(line)
        elif 'output' in line:
            # 对 output 端口赋值为 0
            new_contents.append(line.split()[0] + ' ' + line.split()[1] + ' = 0;\n')
        elif 'endmodule' in line:
            found_ports = False
            new_contents.append(line)
        else:
            continue

# 将处理后的 Verilog 内容写入新文件
with open('processed.v', 'w') as f:
    f.writelines(new_contents)
