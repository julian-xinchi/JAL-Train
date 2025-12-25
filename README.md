# General description
Training/Practices SET...

rdc.c -> A simple tool to Draw math function's curve in a GUI

char_enc_dec.c/cht_enc_dec.c -> two simple enc/dec

axb.py -> AXB auto RTL generate script

# Revision brief
2023/5/10, create master branch, initial check-in:

ADD rdc_boxed.exe which can draw curve of sin(2\*pi\*exci_x)\*sin(2\*pi\*sig_x), dll already integrated.

  Four text boxes included:

      Amplitude(0.0~1.0):

      Excitation waves(10.0~100.0): --means how many periods of excitation waves displayed in the GUI
                                    --fractional part supported

      Signal waves(0.5~5.0):        --means how many periods of signal waves displayed in the GUI
                                    --fractional part supported

      Noise factor(0.0~0.5)
  
  One "Generate" button included, when press the button, new curve decided by parameters in four text boxes will be drawn in GUI.

2023/5/18:
ADD char_enc_dec.c program:

  file_enc_dec.exe file_orig.txt file_enc.txt     --encode file_orig.txt to file_enc.txt

  file_enc_dec.exe file_enc.txt file_dec.txt -r   --decode file_enc.txt to file_dec.txt

Encode method: replace character of "q,w,e,...,o,p" with character of "1,2,...,9,0" in standard 101 keyboard, etc.

2023/5/22
ADD cht_enc_dec.c program (chinese supported):

  cht_enc_dec.exe file_orig.txt file_enc.txt     --encode file_orig.txt to file_enc.txt

  cht_enc_dec.exe file_enc.txt file_dec.txt -r   --decode file_enc.txt to file_dec.txt

2024/1/19
ADD src/axb.py and its related files a_mst_port_list.txt, hash_table_formatted.v

2024/6/28
ADD several python excercises, for excel processing in python: pip install openpyxl

2024/8/29
ADD src/cht_codec_gui.c

2024/12/4
Improve src/mcore_comp.py: add option "-r"/"--size" and basic input file check

2025/9/10
ADD tmp/note.txt to backup work note

2025/11/20
ADD src/extrac_addr_def.py, and complete AXB parameter definition extractor script(excel_proc.py).

2025/12/23
src/extrac_addr_def.py: improve the script robustness for corner cases

2025/12/24
ADD src/extrac_pipeline_def.py: extract pipeline definition from excel file, and generate Verilog parameter definition
ps: One example of excel file is in tmp/ folder

2025/12/25
Major improvement to src/extrac_pipeline_def.py using VSC/TRAE's AI,
optimize the code structure, add comments, etc.

