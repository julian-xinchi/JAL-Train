#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <string.h>
#include <wchar.h>

int main(int argc, char* argv[]) {

    if (argc < 3) {
        printf("Usage: %s [-r]\n", argv[0]);
        printf(" -r: restore the file to its original content\n");
        return 1;
    }

    char* input_file = argv[1];
    char* output_file = argv[2];
    int restore_mode = (argc >= 4 && strcmp(argv[3], "-r") == 0);
    FILE *in, *out;
    wchar_t ch;

    // 打开utf-8文件
    in = fopen(input_file, "rt, ccs=UTF-8");
    if (in == NULL) {
        printf("Failed to open input file %s!", input_file);
        return 1;
    }

    // 打开utf-16文件
    out = fopen(output_file, "wt, ccs=UTF-8");
    if (out == NULL) {
        printf("Failed to open output file %s!", output_file);
        return 1;
    }

    // 读取utf-8文件内容并写入utf-16文件
    while ((ch = fgetwc(in)) != WEOF) {
        if (restore_mode) {
            ch += 0x1;
        } else {
            ch -= 0x1;
        }
        fputwc(ch, out);
    }

    // 关闭文件
    fclose(in);
    fclose(out);

    return 0;

}

