import sys
import openpyxl
import re
import argparse
import inspect

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Extract pipeline definitions from Excel.')
parser.add_argument('excel_file', help='Path to the Excel file')
parser.add_argument('sheet_name', help='Name of the sheet')
parser.add_argument('--keyrow', type=int, default=2, help='Row number for master keywords (default: 2)')
parser.add_argument('--keycol', type=int, default=2, help='Column number for slave keywords (default: 2)')

args = parser.parse_args()

excel_file = args.excel_file
sheet_name = args.sheet_name
header_row = args.keyrow
key_col = args.keycol

# Local parameters for extraction positions
master_pos = 1
slave_pos1 = 1
slave_pos2 = 1

# Open the Excel file and the specified worksheet
workbook = openpyxl.load_workbook(excel_file)
if sheet_name in workbook.sheetnames:
    sheet = workbook[sheet_name]
else:
    print(f"Sheet '{sheet_name}' not found in workbook. Available sheets: {workbook.sheetnames}")
    sys.exit(1)

header_row = args.keyrow
data_start_row = header_row + 1

# Configuration for extraction position
# extract_position: position from the right, starting at 1 (1=last character, 2=second last, etc.)
extract_position = 1

# Find all matching masters and slaves
master_matching = []
for col in range(1, sheet.max_column + 1):
    hv = sheet.cell(row=header_row, column=col).value
    if hv and re.match(r'^m_.*_\d+$', str(hv).strip(), re.IGNORECASE):
        master_matching.append((col, str(hv).strip()))

slave_matching = []
for row in range(data_start_row, sheet.max_row + 1):
    cv = sheet.cell(row=row, column=key_col).value
    if cv and re.match(r'^s_.*_\d+$', str(cv).strip(), re.IGNORECASE):
        slave_matching.append((row, str(cv).strip()))

# Calculate max ranges
max_master_col = max((col for col, _ in master_matching), default=0)
max_slave_row = max((row for row, _ in slave_matching), default=0)

# output filename based on sheet_name
out_fname = re.sub(r'\W+', '_', sheet_name) + '_def.txt'

# Process both modes
for mode in ['master', 'slave']:
    if mode == 'master':
        matching_items = master_matching
    else:
        matching_items = slave_matching

    if not matching_items:
        print(f"Warning: No matching items found for {mode} mode.")
        continue

    # Open a text file and write contents
    with open(out_fname, 'w' if mode == 'master' else 'a') as file:
        if mode == 'master':
            bpp_data = []  # list of (label, count, br_bpp_str)
            fpp_data = []  # list of (label, count, br_fpp_str)
        else:
            bpp_data1 = []
            fpp_data1 = []
            bpp_data2 = []
            fpp_data2 = []
        for idx, (item_num, item_header) in enumerate(matching_items, start=0):
            # extract digit from item_header
            m = re.search(r'_(\d+)$', item_header)
            if not m:
                continue
            digit = int(m.group(1))
            if digit != idx:
                continue  # skip if digit does not match index
            if mode == 'master':
                label = f"M{idx}"
                # list of rightmost 'B' (last digit after decimal)
                br_bpp = []
                # list of leftmost 'B' (first digit before decimal)
                br_fpp = []
            else:
                label = f"S{idx}"
                # for slave, two sets
                br_bpp1 = []
                br_fpp1 = []
                br_bpp2 = []
                br_fpp2 = []
            # count of valid cells
            count = 0
            if mode == 'master':
                # process master mode
                r = data_start_row
                while r <= max_slave_row:
                    cv = sheet.cell(row=r, column=item_num).value
                    if cv is None:
                        break
                    s = str(cv).strip()
                    # skip 'NA' or 'N'
                    if s.upper() in ['NA', 'N']:
                        r += 1
                        continue
                    # process s
                    separator = None
                    if ',' in s:
                        separator = ','
                    elif '.' in s:
                        separator = '.'
                    elif '\uFF0C' in s:
                        # Chinese comma
                        separator = '\uFF0C'

                    if separator:
                        parts = s.split(separator)
                        if len(parts) != 2 or not parts[0] or not parts[1]:
                            print(f"Error: Invalid separator usage in cell at row {r}, col {item_num}: {s} (line {inspect.currentframe().f_lineno})")
                            sys.exit(1)
                        left = parts[0]
                        right = parts[1]
                        if not all(c in '01' for c in left) or not all(c in '01' for c in right):
                            print(f"Error: Non-binary characters in separated parts at row {r}, col {item_num}: {s} (line {inspect.currentframe().f_lineno})")
                            sys.exit(1)
                    else:
                        # no separator, must be all '0' or '1'
                        if all(c in '01' for c in s):
                            mid = len(s) // 2
                            left = s[:mid]
                            right = s[mid:]
                        else:
                            print(f"Error: Invalid format in cell at row {r}, col {item_num}: {s} (line {inspect.currentframe().f_lineno})")
                            sys.exit(1)

                    # extract using position from the right
                    extract_index = -master_pos
                    # rightmost digit
                    br_bpp.append(right[extract_index])
                    count += 1
                    # leftmost digit before decimal
                    br_fpp.append(left[extract_index])
                    r += 1
            else:
                # process slave mode
                for col in range(key_col + 1, max_master_col + 1):
                    cv = sheet.cell(row=item_num, column=col).value
                    if cv is None:
                        break
                    s = str(cv).strip()
                    # skip 'NA' or 'N'
                    if s.upper() in ['NA', 'N']:
                        continue
                    # process s
                    separator = None
                    if ',' in s:
                        separator = ','
                    elif '.' in s:
                        separator = '.'
                    elif '\uFF0C' in s:
                        # Chinese comma
                        separator = '\uFF0C'

                    if separator:
                        parts = s.split(separator)
                        if len(parts) != 2 or not parts[0] or not parts[1]:
                            print(f"Error: Invalid separator usage in cell at row {item_num}, col {col}: {s} (line {inspect.currentframe().f_lineno})")
                            sys.exit(1)
                        left = parts[0]
                        right = parts[1]
                        if not all(c in '01' for c in left) or not all(c in '01' for c in right):
                            print(f"Error: Non-binary characters in separated parts at row {item_num}, col {col}: {s} (line {inspect.currentframe().f_lineno})")
                            sys.exit(1)
                    else:
                        # no separator, must be all '0' or '1'
                        if all(c in '01' for c in s):
                            mid = len(s) // 2
                            left = s[:mid]
                            right = s[mid:]
                        else:
                            print(f"Error: Invalid format in cell at row {item_num}, col {col}: {s} (line {inspect.currentframe().f_lineno})")
                            sys.exit(1)

                    # extract using position from the right
                    # slave mode, extract twice
                    extract_index1 = -slave_pos1
                    br_bpp1.append(right[extract_index1])
                    br_fpp1.append(left[extract_index1])
                    extract_index2 = -slave_pos2
                    br_bpp2.append(right[extract_index2])
                    br_fpp2.append(left[extract_index2])
                    count += 1

            # merge strings: smallest row number at the right (reverse the list)
            if mode == 'master':
                br_bpp_str = ''.join(reversed(br_bpp))
                br_fpp_str = ''.join(reversed(br_fpp))
                bpp_data.append((label, count, br_bpp_str))
                fpp_data.append((label, count, br_fpp_str))
            else:
                br_bpp_str1 = ''.join(reversed(br_bpp1))
                br_fpp_str1 = ''.join(reversed(br_fpp1))
                bpp_data1.append((label, count, br_bpp_str1))
                fpp_data1.append((label, count, br_fpp_str1))
                br_bpp_str2 = ''.join(reversed(br_bpp2))
                br_fpp_str2 = ''.join(reversed(br_fpp2))
                bpp_data2.append((label, count, br_bpp_str2))
                fpp_data2.append((label, count, br_fpp_str2))

        # Print results
        if mode == 'master':
            for label, count, br_fpp_str in fpp_data:
                file.write(f"{f'localparam {label}_BRCH_ARBI_VFPPEN':<40}{f'= {count}\'b{br_fpp_str}':<40};\n")
            for label, count, br_bpp_str in bpp_data:
                file.write(f"{f'localparam {label}_BRCH_ARBI_VFPPEN':<40}{f'= {count}\'b{br_bpp_str}':<40};\n") 
            file.write("\n")
            for label, _, _ in fpp_data:
                file.write(f"{f'localparam {label}_BCH_ARBO_FPPEN':<40}{f'= 1\'b0':<40};\n")
            for label, _, _ in bpp_data:
                file.write(f"{f'localparam {label}_BCH_ARBO_BPPEN':<40}{f'= 1\'b0':<40};\n")
            for label, _, _ in fpp_data:
                file.write(f"{f'localparam {label}_RCH_ARBO_FPPEN':<40}{f'= 1\'b0':<40};\n")
            for label, _, _ in bpp_data:
                file.write(f"{f'localparam {label}_RCH_ARBO_BPPEN':<40}{f'= 1\'b0':<40};\n")
            file.write("\n")
        else:
            # slave mode - first extraction with ACH
            for label, count, br_fpp_str in fpp_data1:
                file.write(f"{f'localparam {label}_ACH_ARBI_VFPPEN':<40}{f'= {count}\'b{br_fpp_str}':<40};\n")
            for label, count, br_bpp_str in bpp_data1:
                file.write(f"{f'localparam {label}_ACH_ARBI_VBPPEN':<40}{f'= {count}\'b{br_bpp_str}':<40};\n") 
            file.write("\n")
            for label, _, _ in fpp_data1:
                file.write(f"{f'localparam {label}_ACH_ARBO_FPPEN':<40}{f'= 1\'b0':<40};\n")
            for label, _, _ in bpp_data1:
                file.write(f"{f'localparam {label}_ACH_ARBO_BPPEN':<40}{f'= 1\'b0':<40};\n")
            file.write("\n")
            # slave mode - second extraction with WCH
            for label, count, br_fpp_str in fpp_data2:
                file.write(f"{f'localparam {label}_WCH_ARBI_VFPPEN':<40}{f'= {count}\'b{br_fpp_str}':<40};\n")
            for label, count, br_bpp_str in bpp_data2:
                file.write(f"{f'localparam {label}_WCH_ARBI_VBPPEN':<40}{f'= {count}\'b{br_bpp_str}':<40};\n") 
            file.write("\n")
            for label, _, _ in fpp_data2:
                file.write(f"{f'localparam {label}_WCH_ARBO_FPPEN':<40}{f'= 1\'b0':<40};\n")
            for label, _, _ in bpp_data2:
                file.write(f"{f'localparam {label}_WCH_ARBO_BPPEN':<40}{f'= 1\'b0':<40};\n")
            file.write("\n")

print(f"Contents written to file: {out_fname}")