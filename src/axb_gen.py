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

def get_cur_port_grp(rw_attr, ms_attr):
    cr5_port_list_path = 'cr5_port_list.txt'

    keywords = []
    vlen_values = []
    io_values = []

    with open(cr5_port_list_path, 'r') as file:
        for line in file:
            line = line.strip()
            parts = [part.strip() for part in line.split(',')]

            if len(parts) >= 3:
                if rw_attr == "r":
                    if re.match (parts[0], r"^AW_.*") or re.match (parts[0], r"^W_.*") or re.match (parts[0], r"^B_.*") :
                        break
                elif rw_attr == "w":
                    if re.match (parts[0], r"^AR_.*") or re.match (parts[0], r"^R_.*"):
                        break
                keywords.append(parts[0])
                vlen_values.append(int(parts[1]))
                if ms_attr == "s":
                    if parts[2] == "i":
                        io_values.append("o")
                    else:
                        io_values.append("i")
                else:
                    io_values.append(parts[2])
            else:
                print(f"Warning: Invalid line in {cr5_port_list_path}: {line}")
                sys.stderr.write(f"Warning: Invalid line in {cr5_port_list_path}: {line}\n")
                sys.exit(1)

    return keywords, vlen_values, io_values

def extract_parameters(input_file):
    define_start_marker = "//SD_AXB_DEFINE_begin"
    define_end_marker = "//SD_AXB_DEFINE_end"
    N = None
    channel_attrib = None
    with open(input_file, "r") as file:
        content = file.read()
        define_start_index = content.find(define_start_marker)
        define_end_index = content.find(define_end_marker, define_start_index)
        if define_start_index != -1 and define_end_index != -1:
            define_block = content[define_start_index + len(define_start_marker):define_end_index]

            match_N = re.search(r'//\s*N\s*=\s*(\d+)', define_block)
            if match_N:
                N = int(match_N.group(1))

            match_xprefix = re.search(r'//\s*xprefix\s*=\s*(\w+)', define_block)
            if match_xprefix:
                xprefix = match_xprefix.group(1)

            match_channel_attrib = re.search(r'//\s*channel_attrib\s*=\s*(\w+(?:\s*,\s*\w+)*)', define_block)
            if match_channel_attrib:
                channel_attrib = match_channel_attrib.group(1).split(',')
                channel_attrib = [attrib.strip() for attrib in channel_attrib]

    if N is None or channel_attrib is None or xprefix is None:
        sys.stderr.write("Error: Could not parse the required parameters.\n")
        sys.exit(1)

    return N, xprefix, channel_attrib

def generate_content(lines, port_option):
    keyword_width = 28
    vlen_value_width = 20
    io_value_width = 8

    begin_marker = re.compile(r"//\s*SD_PORT_GEN_begin")
    end_marker = re.compile(r"//\s*SD_PORT_GEN_end")

    begin_index, end_index = find_markers(lines, begin_marker, end_marker)

    del lines[begin_index + 1:end_index]

    if port_option == "on":
        generated_lines = []

        for i in range(N):
            keywords, vlen_values, io_values = get_cur_port_grp(channel_attrib[i], "m")
            for keyword, vlen_value, io_value in zip(keywords, vlen_values, io_values):
                keyword = 'm_' + xprefix + '_' + str(i) + '_' + keyword

                if vlen_value <= 1:
                    vlen_value_str = ' ' * vlen_value_width
                else:
                    vlen_value_str = "[{}:0]".format(vlen_value - 1)

                if io_value == "i":
                    io_value = "input"
                elif io_value == "o":
                    io_value = "output"

                formatted_line = "{:<{io_width}}{:<{vlen_width}}{:<{kw_width}},\n".format(
                    io_value, vlen_value_str, keyword, io_width=io_value_width, vlen_width=vlen_value_width, kw_width=keyword_width
                )
                generated_lines.append(formatted_line)
        lines[begin_index + 1:begin_index + 1] = generated_lines

    elif port_option == "off":
        pass

    print(f"Generated {len(lines)} lines.")

    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update RTL by inserting generated contents between markers.')
    parser.add_argument('input_file', type=str, help='Path to the input file.')
    parser.add_argument('--autoGen', type=str, choices=['on', 'off'], required=True, help='Whether to generate content ("on") or clear content ("off").')

    args = parser.parse_args()

    try:
        N, xprefix, channel_attrib = extract_parameters(args.input_file)
        print("N = ", N)
        print("Prefix = ", xprefix)
        print("Channel Attributes = ", channel_attrib)
    except FileNotFoundError:
        sys.stderr.write(f"Error: File {args.input_file} not found.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        sys.exit(1)

    file_old_lines = get_file_lines(args.input_file)
    generated_lines = generate_content(file_old_lines, args.autoGen)
    with open(args.input_file, 'w') as file:
        file.writelines(generated_lines)
