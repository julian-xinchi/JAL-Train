import argparse
import re

def generate_content(input_file, port_option):
    # Example keyword list
    # keywords = ["apple", "banana", "cherry", "date", "elderberry"]
    # int_values = [5, 0, 8, 6, 7]  # List of positive integers corresponding to keywords
    # str_values = ["red", "yellow", "red", "brown", "purple"]  # List of strings corresponding to keywords

    # Define the file path of the file containing the data
    cr5_port_list_path = 'cr5_port_list.txt'

    # Initialize empty lists to store the values
    keywords = []
    int_values = []
    str_values = []

    # Read from the file and populate the lists
    with open(cr5_port_list_path, 'r') as file:
        for line in file:
            # Strip whitespace from the beginning and end of the line
            line = line.strip()
            
            # Split the line by comma and strip spaces from each part
            parts = [part.strip() for part in line.split(',')]
            
            # Ensure the line has exactly three parts
            if len(parts) == 3:
                # Append the values to the respective lists, converting int_values to integers
                keywords.append(parts[0])
                int_values.append(int(parts[1]))
                str_values.append(parts[2])

    # Set character widths
    keyword_width = 16
    int_value_width = 16
    str_value_width = 8

    # Read the template file and insert generated content in a specific area
    begin_marker = re.compile(r"//\s*SD_PORT_GEN_begin")
    end_marker = re.compile(r"//\s*SD_PORT_GEN_end")

    # Read the original file content
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Find markers
    begin_index = None
    end_index = None
    for i, line in enumerate(lines):
        if begin_marker.search(line):
            begin_index = i
        elif end_marker.search(line):
            end_index = i
            break

    if begin_index is not None and end_index is not None:
        # Remove the original generated content (if any)
        del lines[begin_index + 1:end_index]

        # Generate new content or clear content based on the PORT option
        if port_option == "on":
            # Generate new content
            generated_lines = []

            for keyword, int_value, str_value in zip(keywords, int_values, str_values):
                # Check if int_value is 0, and print spaces if it is
                if int_value < 1:
                    int_value_str = ' ' * int_value_width
                else:
                    # int_value_str = "{:<{int_width}}".format(int_value, int_width=int_value_width)
                    int_value_str = "[{}:0]".format(int_value - 1)

                formatted_line = "{:<{kw_width}}{:<{int_width}}{:<{str_width}},\n".format(
                    keyword, int_value_str, str_value, kw_width=keyword_width, int_width=int_value_width, str_width=str_value_width
                )
                generated_lines.append(formatted_line)
            # Insert the generated content between the markers
            lines[begin_index + 1:begin_index + 1] = generated_lines
        elif port_option == "off":
            # Clear the content, no need to add anything
            pass  # The original content has already been removed

        # Write the updated content back to the file
        with open(input_file, "w") as file:
            file.writelines(lines)

        print("Template file has been updated according to PORT option '{}'".format(port_option))
    else:
        print("Error: Could not find markers.")

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Update a file by inserting generated content between markers.')
parser.add_argument('input_file', type=str, help='Path to the input file.')
parser.add_argument('--port', type=str, choices=['on', 'off'], required=True, help='Whether to generate content ("on") or clear content ("off").')

# Parse command line arguments
args = parser.parse_args()

# Call the function, updating the file using command line arguments
generate_content(args.input_file, args.port)
