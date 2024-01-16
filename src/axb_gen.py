import argparse
import re
import sys

def get_file_lines(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    return lines

def update_file(input_file, original_lines, generated_lines):
    if generated_lines != original_lines:
        with open(input_file, 'w') as file:
            file.writelines(generated_lines)
    else:
        print("No changes made to file.")

def find_markers(lines, begin_marker, end_marker):
    begin = None
    end = None

    for i, line in enumerate(lines):
        if begin_marker.search(line):
            begin = i
        elif end_marker.search(line):
            end = i
            break

    if begin is None or end is None:
        sys.stderr.write(f"Error: Could not find markers.\n")
        sys.exit(1)

    # print(f"Found markers at lines {begin+1} and {end+1}.")

    return begin, end

def extract_parameters(input_file):
    define_start_marker = "//SD_AXB_DEFINE_begin"
    define_end_marker = "//SD_AXB_DEFINE_end"
    MSTN = None
    SLVN = None
    xprefix = None
    mst_attr = None
    with open(input_file, "r") as file:
        content = file.read()
        define_start_index = content.find(define_start_marker)
        define_end_index = content.find(define_end_marker, define_start_index)
        if define_start_index != -1 and define_end_index != -1:
            define_block = content[define_start_index + len(define_start_marker):define_end_index]

            match_MSTN = re.search(r'//\s*MSTN\s*=\s*(\d+)', define_block)
            if match_MSTN:
                MSTN = int(match_MSTN.group(1))

            match_SLVN = re.search(r'//\s*SLVN\s*=\s*(\d+)', define_block)
            if match_SLVN:
                SLVN = int(match_SLVN.group(1))

            match_xprefix = re.search(r'//\s*xprefix\s*=\s*(\w+)', define_block)
            if match_xprefix:
                xprefix = match_xprefix.group(1)

            match_mst_attr = re.search(r'//\s*mst_attr\s*=\s*(\w+(?:\s*,\s*\w+)*)', define_block)
            if match_mst_attr:
                mst_attr = match_mst_attr.group(1).split(',')
                mst_attr = [attrib.strip() for attrib in mst_attr]

    if MSTN is None or SLVN is None or mst_attr is None or xprefix is None:
        sys.stderr.write("Error: Could not parse the required parameters.\n")
        sys.exit(1)

    return MSTN, SLVN, xprefix, mst_attr

def get_cur_port_grp(rw_attr, ms_attr):
    cr5_port_list_path = 'cr5_port_list.txt'

    keywords = []
    vlen_values = []
    io_values = []
    default_values = []

    with open(cr5_port_list_path, 'r') as file:
        for line in file:
            line = line.strip()
            parts = [part.strip() for part in line.split(',')]

            if len(parts) >= 3:
                if rw_attr == "r":
                    if re.match(r"^AW_.*", parts[0]) or re.match(r"^W_.*", parts[0]) or re.match(r"^B_.*", parts[0]):
                        continue
                elif rw_attr == "w":
                    if re.match(r"^AR_.*", parts[0]) or re.match(r"^R_.*", parts[0]):
                        continue
                keywords.append(parts[0])
                vlen_values.append(int(parts[1]))
                if ms_attr == "s":
                    if parts[2] == "i":
                        io_values.append("o")
                    else:
                        io_values.append("i")
                else:
                    io_values.append(parts[2])
                if len(parts) >= 4:
                    default_values.append(int(parts[3],16))
                else:
                    default_values.append(int(-1))
            else:
                print(f"Warning: Invalid line in {cr5_port_list_path}: {line}")
                sys.stderr.write(f"Warning: Invalid line in {cr5_port_list_path}: {line}\n")
                sys.exit(1)

    return keywords, vlen_values, io_values, default_values

def generate_stub_codes(keyword, vlen, default_value):
    if default_value == -1:
        default_v = 0
    else:
        default_v = default_value

    if default_v == 0:
        if vlen <= 1:
            stub_line = "assign {keyword} = 1'b0;\n".format(keyword=keyword)
        else:
            stub_line = "assign {keyword} = {{{vlen}{{1'b0}}}};\n".format(keyword=keyword, vlen=vlen)
    else:
        stub_line = "assign {keyword} = {vlen}'h{default_v:0X};\n".format(keyword=keyword, vlen=vlen, default_v=default_v)
        # stub_line = stub_line.replace('0x', '')

    return stub_line

def generate_port_lines(MSTN, SLVN, xprefix, mst_attr):
    keyword_width = 28
    vlen_value_width = 20
    io_value_width = 8
    # Example logic for generating port lines
    lines = []
    stub_lines = []
    for i in range(MSTN):
        keywords, vlen_values, io_values, default_values = get_cur_port_grp(mst_attr[i], "m")
        # print("keywords = ", keywords, "vlen_values = ", vlen_values, "io_values = ", io_values)
        for keyword, vlen, io, default_val in zip(keywords, vlen_values, io_values, default_values):
            keyword = 'm_' + xprefix + '_' + str(i) + '_' + keyword

            if vlen <= 1:
                vlen_value_str = ' ' * vlen_value_width
            else:
                vlen_value_str = "[{}:0]".format(vlen - 1)

            if io == "i":
                io_value = 'input'
            elif io == "o":
                io_value = 'output'
                stub_line = generate_stub_codes(keyword, vlen, default_val)
                stub_lines.append(stub_line)

            formatted_line = "{:<{io_width}}{:<{vlen_width}}{:<{kw_width}},\n".format(
                io_value, vlen_value_str, keyword, io_width=io_value_width, vlen_width=vlen_value_width, kw_width=keyword_width
            )
            lines.append(formatted_line)
    for i in range(SLVN):
        keywords, vlen_values, io_values, default_values = get_cur_port_grp("rw", "s")
        for keyword, vlen, io in zip(keywords, vlen_values, io_values):
            keyword = 's_' + xprefix + '_' + str(i) + '_' + keyword

            if vlen <= 1:
                vlen_value_str = ' ' * vlen_value_width
            else:
                vlen_value_str = "[{}:0]".format(vlen - 1)

            if io == "i":
                io_value = 'input'
            elif io == "o":
                io_value = 'output'
                stub_line = generate_stub_codes(keyword, vlen, default_val)
                stub_lines.append(stub_line)

            formatted_line = "{:<{io_width}}{:<{vlen_width}}{:<{kw_width}},\n".format(
                io_value, vlen_value_str, keyword, io_width=io_value_width, vlen_width=vlen_value_width, kw_width=keyword_width
            )
            lines.append(formatted_line)
    return lines, stub_lines

def block_codes_deal(lines, generated_lines, begin_marker, end_marker, block_sel):
    begin_index, end_index = find_markers(lines, begin_marker, end_marker)
    del lines[begin_index + 1:end_index]
    if block_sel == "on":
        lines[begin_index + 1:end_index] = generated_lines
    elif block_sel == "off":
        pass
    return lines

def generate_port_codes(lines, autoGen_option, stub_option, MSTN, SLVN, xprefix, mst_attr):
    generated_lines, generate_stub_lines = generate_port_lines(MSTN, SLVN, xprefix, mst_attr)

    begin_marker = re.compile(r"//\s*SD_PORT_GEN_begin")
    end_marker = re.compile(r"//\s*SD_PORT_GEN_end")
    lines_0 = block_codes_deal(lines, generated_lines, begin_marker, end_marker, autoGen_option)

    if stub_option:
        begin_marker = re.compile(r"//\s*SD_STUB_GEN_begin")
        end_marker = re.compile(r"//\s*SD_STUB_GEN_end")
        lines = block_codes_deal(lines_0, generate_stub_lines, begin_marker, end_marker, autoGen_option)
    else:
        pass

    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update RTL by inserting generated contents between markers.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')
    parser.add_argument('--autoGen', type=str, choices=['on', 'off'], required=True, help='Whether to generate contents ("on") or clear all auto-Gen blocks ("off").')
    parser.add_argument('--stub', action='store_true', help='Whether to generate stub content.')

    args = parser.parse_args()

    try:
        MSTN, SLVN, xprefix, mst_attr = extract_parameters(args.input_file)
        print("MSTN = ", MSTN, "SLVN = ", SLVN)
        print("Prefix = ", xprefix)
        print("Master Attributes = ", mst_attr)
    except FileNotFoundError:
        sys.stderr.write(f"Error: File {args.input_file} not found.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        sys.exit(1)

    file_old_lines = get_file_lines(args.input_file)
    generated_lines = generate_port_codes(file_old_lines, args.autoGen, args.stub, MSTN, SLVN, xprefix, mst_attr)
    file_old_lines = get_file_lines(args.input_file)
    update_file(args.input_file, file_old_lines, generated_lines)
