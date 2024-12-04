import sys
import os
import argparse
import textwrap

mapping = {
    'd0': 0x0,
    'd1': 0x40,
    'd2': 0x80,
    'd3': 0xc0,
    'c0': 0x0,
    'c1': 0x20,
    't0': 0x0,
    't1': 0x20,
    't2': 0x40,
    't3': 0x60,
    't4': 0x80,
    't5': 0xa0,
    't6': 0xc0,
    'NOP': 0x10,
    'CLEAR0': 0x20,
    'CLEAR1': 0x30,
    'SET0': 0x40,
    'SET1': 0x50,
    'IMM': 0x80,
    'CVARM': 0x90,
    'CVAR0': 0xa0,
    'CORDIC0': 0xc0,
    'CORDIC1': 0xd0,
    'MOV1': 0x04,
    'MOVT': 0x14,
    'SKIPN0': 0x28,
    'SKIPN1': 0x38,
    'GOTO': 0x48,
    'GOTO_OFST': 0x58,
    'GOTO_OFSTN': 0x68,
    'HALT': 0x88,
    'LOAD': 0x01,
    'LOAD_OFST': 0x11,
    'STORE': 0x09,
    'STORE_OFST': 0x19,
    'LSF': 0x02,
    'RSF': 0x12,
    'DRSF': 0x06,
    'OR': 0x0a,
    'AND': 0x1a,
    'NOT': 0x2a,
    'XOR': 0x3a,
    'CMPEQ': 0x0e,
    'CMPGT': 0x1e,
    'ADD': 0x03,
    'SUB': 0x13,
    'MUL': 0x07,
    'LMUL': 0x17,
    'DIV': 0x0b,
    'FDIV': 0x2b,
    'MOD': 0x1b,
}

def string_to_binary(string):
    binary = 0
    binary = mapping.get(string, 0x0)
    return binary

# Set up ArgumentParser
description = textwrap.dedent("""\
    This is a sample script to demonstrate how to use
    multi-line description text in ArgumentParser.
    You can add more detailed information here to help
    users better understand the functionality of the script.
""")

parser = argparse.ArgumentParser(description=description)
parser.add_argument('input_file', help='Input file')
parser.add_argument('--size', type=int, help='Number of lines to pad to')
parser.add_argument('-r', '--reverse', action='store_true', help='Whether to reverse the order of lines')

args = parser.parse_args()

if len(sys.argv) < 2:
    print("A text ARG file is required.")
    sys.exit(1)

size = args.size
reverse = args.reverse
input_file = args.input_file
output_file = os.path.splitext(input_file)[0] + ".hex"

#with open(input_file, 'r', encoding='utf-8') as file:
#    lines = file.readlines()
try:
    with open(input_file, 'r', encoding='utf-8') as file:
        raw_lines = file.readlines()
        lines = []

        for line_number, line in enumerate(raw_lines, start=1):
            stripped_line = line.strip()

            # Remove the comment part if present
            comment_index = stripped_line.find("//")
            if comment_index != -1:
                stripped_line = stripped_line[:comment_index].strip()

            # Process each line to remove comments and ignore empty lines
            if stripped_line:  # Only add non-empty lines
                lines.append(stripped_line)
            else:
                continue

            words = [word for part in stripped_line.split(',') for word in part.split()]
            for word in words:
                if word not in mapping:
                    print(f"Error: Unknown string '{word}' found at line {line_number}")
                    sys.exit(1)

except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
    sys.exit(1)

# If the --size parameter is specified, pad the number of lines to the specified size
if size is not None:
    while len(lines) < size:
        lines.append('0\n')

with open(output_file, 'w') as file:
    for line in lines:
        line = line.strip()
        binary_result = 0
        if line.isdigit():
            binary_result = line
            hex_result = hex(int(binary_result,10))
        else:
            strings = [s.strip() for s in line.split(",")]
            for string in strings:
                binary = string_to_binary(string)
                binary_result = binary_result | binary
            hex_result = hex(binary_result)
        file.write(hex_result + "," + "\n")

# If the -r parameter is specified, reverse the order of lines
with open(output_file, 'r') as file:
    lines = file.readlines()

if reverse:
    reversed_lines = lines[::-1]
else:
    reversed_lines = lines

with open(output_file, 'w') as file:
    file.writelines(reversed_lines)
