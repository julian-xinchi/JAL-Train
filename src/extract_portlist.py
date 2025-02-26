import re
import sys

def extract_module_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Pattern to match module "any string" (...)
    pattern1 = re.compile(r'module\s+(\w+)\s*\((.*?)\);', re.DOTALL)

    # Pattern to match module "any string" #(...) (...)
    pattern2 = re.compile(r'module\s+(\w+)\s*#\s*\((.*?)\)\s*\((.*?)\);', re.DOTALL)

    matches1 = pattern1.findall(content)
    matches2 = pattern2.findall(content)

    # Extracting content from matches
    extracted_content = []
    for match in matches1:
        module_name = match[0]
        module_content = match[1].strip()
        extracted_content.append((module_name, module_content))

    for match in matches2:
        module_name = match[0]
        module_content = match[2].strip()
        extracted_content.append((module_name, module_content))

    return extracted_content

def filter_io_fields(content):
    # Patterns to match
    pattern1 = re.compile(r'\b(input|output)\s+(\w+)')
    pattern2 = re.compile(r'\b(input|output)\s*(\[.*?\])\s*(\w+)')

    extracted_fields = []

    for line in content:
        match1 = pattern1.search(line)
        match2 = pattern2.search(line)

        if match2:
            extracted_fields.append(f"{match2.group(1):<8}{match2.group(2):<32}{match2.group(3):<32},\n")
        elif match1:
            extracted_fields.append(f"{match1.group(1):<8}{'':<32}{match1.group(2):<32},\n")

    return extracted_fields

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_filename> <output_filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    extracted_content = extract_module_content(input_filename)

    with open(output_filename, 'w') as output_file:
        for module_name, content in extracted_content:
            lines = content.split('\n')  # 对每个字符串元素调用 split 方法，将其分割成行
            extracted_fields = filter_io_fields(lines)

            output_file.write(f"Module: {module_name}\n")
            for field in extracted_fields:
                output_file.write(field)
            output_file.write(f"{'-' * 72}\n")
