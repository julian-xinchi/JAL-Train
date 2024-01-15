import argparse
import re
import sys

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def parse_define_block(content, start_marker, end_marker):
    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index)
    if start_index != -1 and end_index != -1:
        define_block = content[start_index + len(start_marker):end_index]
        return define_block
    return None

def extract_parameters_from_block(define_block):
    # Extract parameters from the define block
    # ... similar to the existing regex extraction logic ...

def extract_parameters(input_file):
    define_start_marker = "//SD_AXB_DEFINE_begin"
    define_end_marker = "//SD_AXB_DEFINE_end"
    content = read_file(input_file)
    define_block = parse_define_block(content, define_start_marker, define_end_marker)
    if define_block:
        return extract_parameters_from_block(define_block)
    else:
        raise ValueError("Define block not found")

def read_port_list(port_list_path):
    # Read the port list and return it as a tuple of lists
    # ... similar to the existing logic ...

def generate_port_lines(N, xprefix, keywords, vlen_values, io_values):
    # Generate the lines to be inserted into the input file
    # ... similar to the existing logic ...

def find_markers(lines, begin_marker, end_marker):
    begin = None
    end = None
    for i, line in enumerate(lines):
        if begin_marker.search(line):
            begin = i
        elif end_marker.search(line):
            end = i
            break
    return begin, end

def update_file(input_file, generated_content, begin_index, end_index):
    # Update the file content with the generated content
    # ... similar to the existing logic ...

def main(input_file, port_option):
    try:
        N, xprefix, channel_attrib = extract_parameters(input_file)
        print("N = ", N)
        print("Prefix = ", xprefix)
        print("Channel Attributes = ", channel_attrib)

        cr5_port_list_path = 'cr5_port_list.txt'
        keywords, vlen_values, io_values = read_port_list(cr5_port_list_path)

        generated_lines = generate_port_lines(N, xprefix, keywords, vlen_values, io_values) if port_option == "on" else []

        file_content = read_file(input_file)
        lines = file_content.splitlines(keepends=True)
        begin_marker = re.compile(r"//\s*SD_PORT_GEN_begin")
        end_marker = re.compile(r"//\s*SD_PORT_GEN_end")
        begin_index, end_index = find_markers(lines, begin_marker, end_marker)
        if begin_index is not None and end_index is not None:
            update_file(input_file, generated_lines, begin_index, end_index)
        else:
            print("Error: Could not find markers.")
    except FileNotFoundError:
        sys.stderr.write(f"Error: File {input_file} not found.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update RTL by inserting generated contents between markers.')
    parser








import argparse
import re
import sys

# ... [previous code] ...

def extract_parameters_from_block(define_block):
    # Example regex for extracting parameters
    pattern = r'(\w+) = (\w+)'  # Adjust the regex pattern as needed
    matches = re.findall(pattern, define_block)
    parameters = {key: value for key, value in matches}
    return parameters

def read_port_list(port_list_path):
    # Example logic for reading port list
    with open(port_list_path, 'r') as file:
        ports = file.readlines()
    # Assuming the format of each line is "keyword vlen io"
    keywords = []
    vlen_values = []
    io_values = []
    for port in ports:
        keyword, vlen, io = port.strip().split()
        keywords.append(keyword)
        vlen_values.append(vlen)
        io_values.append(io)
    return keywords, vlen_values, io_values

def generate_port_lines(N, xprefix, keywords, vlen_values, io_values):
    # Example logic for generating port lines
    lines = []
    for keyword, vlen, io in zip(keywords, vlen_values, io_values):
        line = f"{xprefix}{keyword} [{vlen}:0] {io};"
        lines.append(line)
    return lines

def update_file(input_file, generated_content, begin_index, end_index):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    updated_lines = lines[:begin_index + 1] + generated_content + lines[end_index:]
    with open(input_file, 'w') as file:
        file.writelines(updated_lines)

# ... [previous code] ...

parser = argparse.ArgumentParser(description='Update RTL by inserting generated contents between markers.')
parser.add_argument('input_file', type=str, help='The input file to process.')
parser.add_argument('--port', dest='port_option', choices=['on', 'off'], default='off', help='Turn port generation on or off.')
args = parser.parse_args()

main(args.input_file, args.port_option)



