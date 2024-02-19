import os
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
    marker_exist = True

    for i, line in enumerate(lines):
        if begin_marker.search(line):
            begin = i
        elif end_marker.search(line):
            end = i
            break

    if begin is None or end is None:
        marker_exist = False
        #sys.stderr.write(f"Error: Could not find markers.\n")
        #sys.exit(1)

    # print(f"Found markers at lines {begin+1} and {end+1}.")

    return marker_exist, begin, end

def extract_code_block(content, start_marker, end_marker):
    start_index = content.find(start_marker) + len(start_marker)
    end_index = content.find(end_marker, start_index)
    return content[start_index:end_index] if start_index != -1 and end_index != -1 else None

def extract_parameters(input_file):
    define_start_marker = "//SD_AXB_DEFINE_begin"
    define_end_marker = "//SD_AXB_DEFINE_end"
    parameters = {
        'PROJ': None,
        'MSTN': None,
        'SLVN': None,
        'xprefix': None,
        'mst_attr': None
    }
    regex_patterns = {
        'PROJ': r'//\s*PROJ\s*=\s*(\w+)',
        'MSTN': r'//\s*MSTN\s*=\s*(\d+)',
        'SLVN': r'//\s*SLVN\s*=\s*(\d+)',
        'xprefix': r'//\s*xprefix\s*=\s*(\w+)',
        'mst_attr': r'//\s*mst_attr\s*=\s*(\w+(?:\s*,\s*\w+)*)'
    }

    with open(input_file, "r") as file:
        content = file.read()
        define_block = extract_code_block(content, define_start_marker, define_end_marker)

        if define_block:
            for key, pattern in regex_patterns.items():
                match = re.search(pattern, define_block)
                if match:
                    if key == 'mst_attr':
                        parameters[key] = [attr.strip() for attr in match.group(1).split(',')]
                    else:
                        parameters[key] = int(match.group(1)) if key in ['MSTN', 'SLVN'] else match.group(1)

    if None in parameters.values():
        sys.stderr.write("Error: Could not parse the required parameters.\n")
        sys.exit(1)

    return parameters

def get_cur_port_grp(proj_name, MSTN, xprefix, rw_attr, ms_attr):
    mst_port_list_file = xprefix + '_' + 'mst_port_list.txt'
    mst_port_list_path = os.path.join(proj_name, mst_port_list_file)

    keywords = []
    vlen_values = []
    io_values = []
    default_values = []

    with open(mst_port_list_path, 'r') as file:
        for line in file:
            line = line.strip()
            parts = [part.strip() for part in line.split(',')]

            if len(parts) == 1 and parts[0] == '':
                continue
            elif len(parts) >= 3:
                if rw_attr == "r":
                    if re.match(r"^Aw_.*", parts[0]) or re.match(r"^W_.*", parts[0]) or re.match(r"^B_.*", parts[0]):
                        continue
                elif rw_attr == "w":
                    if re.match(r"^Ar_.*", parts[0]) or re.match(r"^R_.*", parts[0]):
                        continue
                keywords.append(parts[0])
                if re.match(r".*_Id$", parts[0]) and ms_attr == 's':
                    f_vlen = int(parts[2]) + MSTN.bit_length()
                else:
                    f_vlen = int(parts[2])
                vlen_values.append(f_vlen)
                if ms_attr == "s":
                    if parts[1] == "i":
                        io_values.append("o")
                    else:
                        io_values.append("i")
                else:
                    io_values.append(parts[1])
                if len(parts) >= 4 and not re.match(r"^\s*$", parts[3]):
                    default_values.append(int(parts[3],16))
                else:
                    default_values.append(int(-1))
            else:
                sys.stderr.write(f"Error: Invalid line in {mst_port_list_path}: {line}\n")
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

def generate_port_lines(proj_name, MSTN, SLVN, xprefix, mst_attr):
    keyword_width = 40
    vlen_value_width = 32
    io_value_width = 8
    # Example logic for generating port lines
    lines = []
    stub_lines = []
    for i in range(MSTN):
        keywords, vlen_values, io_values, default_values = get_cur_port_grp(proj_name, MSTN, xprefix, mst_attr[i], "m")
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

            formatted_line = "{:<{io_width}}{:<{vlen_width}}{:<{kw_width}}, //\n".format(
                io_value, vlen_value_str, keyword, io_width=io_value_width, vlen_width=vlen_value_width, kw_width=keyword_width
            )
            lines.append(formatted_line)
    for i in range(SLVN):
        keywords, vlen_values, io_values, default_values = get_cur_port_grp(proj_name, MSTN, xprefix, "rw", "s")
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

            formatted_line = "{:<{io_width}}{:<{vlen_width}}{:<{kw_width}}, //\n".format(
                io_value, vlen_value_str, keyword, io_width=io_value_width, vlen_width=vlen_value_width, kw_width=keyword_width
            )
            lines.append(formatted_line)
    return lines, stub_lines

def code_block_proc(lines, begin_marker, end_marker):
    marker_exist, begin_index, end_index = find_markers(lines, begin_marker, end_marker)
    if marker_exist:
        #print("debug pompt begin_index = ", begin_index, "end_index = ", end_index)
        del lines[begin_index + 1:end_index]
    else:
        pass
    return lines, begin_index

def generate_port_codes(lines, autoGen_option, proj_name, MSTN, SLVN, xprefix, mst_attr):
    generated_lines, generate_stub_lines = generate_port_lines(proj_name, MSTN, SLVN, xprefix, mst_attr)

    begin_marker = re.compile(r"//\s*SD_AXB_PORT_GEN_begin")
    end_marker = re.compile(r"//\s*SD_AXB_PORT_GEN_end")
    lines, inserted_index = code_block_proc(lines, begin_marker, end_marker)
    if 'p' in autoGen_option or 'a' in autoGen_option:
        lines[inserted_index + 1: inserted_index + 1] = generated_lines
    else:
        pass

    begin_marker = re.compile(r"//\s*SD_AXB_STUB_GEN_begin")
    end_marker = re.compile(r"//\s*SD_AXB_STUB_GEN_end")
    lines, inserted_index = code_block_proc(lines, begin_marker, end_marker)
    if 's' in autoGen_option:
        lines[inserted_index + 1: inserted_index + 1] = generate_stub_lines
    else:
        pass

    return lines

def verilog_features(value):
    valid_chars = set('piwfasn')
    if not isinstance(value, str) or not set(value).issubset(valid_chars) or len(set(value)) != len(value):
        raise argparse.ArgumentTypeError("--autoGen requires a string containing any combination of \
                                         'p', 'i', 'w', 'a', 'f', 's', 'n' with no repetitions.")
    return value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Update RTL by inserting generated contents between markers.",
        formatter_class=argparse.RawTextHelpFormatter,  #use RawTextHelpFormatter
        epilog='Example of use: python axb_gen.py dut.v --autoGen as'
    )
    #parser = argparse.ArgumentParser(description='Update RTL by inserting generated contents between markers.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')
    #parser.add_argument('--autoGen', type=str, choices=['on', 'off'], \
    #                     required=True, help='Whether to generate contents ("on") or clear all auto-Gen blocks ("off").')
    parser.add_argument('--autoGen', type=verilog_features, default='n', help=(
        'Accepts any combination of the characters "p", "i", "w", "f", "a", "s", "n" with no repetitions, representing which part of Verilog Code to generate:\n'
        'p -> port list;\n'
        'i -> instance codes;\n'
        'w -> wire definition;\n'
        'f -> function logic codes;\n'
        'a -> all of the above;\n'
        's -> stub codes;\n'
        'n -> none, collapse all autoGen blocks.'
    ))
    #parser.add_argument('--stub', action='store_true', help='Whether to generate stub content.')

    args = parser.parse_args()

    try:
        params = extract_parameters(args.input_file)
        proj_name = params['PROJ']
        MSTN = params['MSTN']
        SLVN = params['SLVN']
        xprefix = params['xprefix']
        mst_attr = params['mst_attr']
        #proj_name, MSTN, SLVN, xprefix, mst_attr = extract_parameters(args.input_file)
        print("MSTN = ", MSTN, "; SLVN = ", SLVN)
        print("Prefix = ", xprefix)
        print("Master Attributes = ", mst_attr)
    except FileNotFoundError:
        sys.stderr.write(f"Error: File {args.input_file} not found.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An error occurred when extracting parameters: {e}\n")
        sys.exit(1)

    file_old_lines = get_file_lines(args.input_file)
    generated_lines = generate_port_codes(file_old_lines, args.autoGen, proj_name, MSTN, SLVN, xprefix, mst_attr)
    file_old_lines = get_file_lines(args.input_file)
    update_file(args.input_file, file_old_lines, generated_lines)
