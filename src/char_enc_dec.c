#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 1024

// 将字符 c 替换为下一行对应的字符
char replace_char(char c) {
    switch (c) {
        case '1': return 'z';
        case '2': return 'x';
        case '3': return 'c';
        case '4': return 'v';
        case '5': return 'b';
        case '6': return 'n';
        case '7': return 'm';
        case '8': return ',';
        case '9': return '.';
        case '0': return '/';
        case 'q': return '1';
        case 'w': return '2';
        case 'e': return '3';
        case 'r': return '4';
        case 't': return '5';
        case 'y': return '6';
        case 'u': return '7';
        case 'i': return '8';
        case 'o': return '9';
        case 'p': return '0';
        case 'a': return 'q';
        case 's': return 'w';
        case 'd': return 'e';
        case 'f': return 'r';
        case 'g': return 't';
        case 'h': return 'y';
        case 'j': return 'u';
        case 'k': return 'i';
        case 'l': return 'o';
        case ';': return 'p';
        case 'z': return 'a';
        case 'x': return 's';
        case 'c': return 'd';
        case 'v': return 'f';
        case 'b': return 'g';
        case 'n': return 'h';
        case 'm': return 'j';
        case ',': return 'k';
        case '.': return 'l';
        case '/': return ';';
        case '!': return 'Z';
        case '@': return 'X';
        case '#': return 'C';
        case '$': return 'V';
        case '%': return 'B';
        case '^': return 'N';
        case '&': return 'M';
        case '*': return '<';
        case '(': return '>';
        case ')': return '?';
        case 'Q': return '!';
        case 'W': return '@';
        case 'E': return '#';
        case 'R': return '$';
        case 'T': return '%';
        case 'Y': return '^';
        case 'U': return '&';
        case 'I': return '*';
        case 'O': return '(';
        case 'P': return ')';
        case 'A': return 'Q';
        case 'S': return 'W';
        case 'D': return 'E';
        case 'F': return 'R';
        case 'G': return 'T';
        case 'H': return 'Y';
        case 'J': return 'U';
        case 'K': return 'I';
        case 'L': return 'O';
        case ':': return 'P';
        case 'Z': return 'A';
        case 'X': return 'S';
        case 'C': return 'D';
        case 'V': return 'F';
        case 'B': return 'G';
        case 'N': return 'H';
        case 'M': return 'J';
        case '<': return 'K';
        case '>': return 'L';
        case '?': return ':';
        default : return c;
    }
}

// 将字符 c 恢复为上一行对应的字符
char restore_char(char c) {
    switch (c) {
        case 'z': return '1';
        case 'x': return '2';
        case 'c': return '3';
        case 'v': return '4';
        case 'b': return '5';
        case 'n': return '6';
        case 'm': return '7';
        case ',': return '8';
        case '.': return '9';
        case '/': return '0';
        case '1': return 'q';
        case '2': return 'w';
        case '3': return 'e';
        case '4': return 'r';
        case '5': return 't';
        case '6': return 'y';
        case '7': return 'u';
        case '8': return 'i';
        case '9': return 'o';
        case '0': return 'p';
        case 'q': return 'a';
        case 'w': return 's';
        case 'e': return 'd';
        case 'r': return 'f';
        case 't': return 'g';
        case 'y': return 'h';
        case 'u': return 'j';
        case 'i': return 'k';
        case 'o': return 'l';
        case 'p': return ';';
        case 'a': return 'z';
        case 's': return 'x';
        case 'd': return 'c';
        case 'f': return 'v';
        case 'g': return 'b';
        case 'h': return 'n';
        case 'j': return 'm';
        case 'k': return ',';
        case 'l': return '.';
        case ';': return '/';
        case 'Z': return '!';
        case 'X': return '@';
        case 'C': return '#';
        case 'V': return '$';
        case 'B': return '%';
        case 'N': return '^';
        case 'M': return '&';
        case '<': return '*';
        case '>': return '(';
        case '?': return ')';
        case '!': return 'Q';
        case '@': return 'W';
        case '#': return 'E';
        case '$': return 'R';
        case '%': return 'T';
        case '^': return 'Y';
        case '&': return 'U';
        case '*': return 'I';
        case '(': return 'O';
        case ')': return 'P';
        case 'Q': return 'A';
        case 'W': return 'S';
        case 'E': return 'D';
        case 'R': return 'F';
        case 'T': return 'G';
        case 'Y': return 'H';
        case 'U': return 'J';
        case 'I': return 'K';
        case 'O': return 'L';
        case 'P': return ':';
        case 'A': return 'Z';
        case 'S': return 'X';
        case 'D': return 'C';
        case 'F': return 'V';
        case 'G': return 'B';
        case 'H': return 'N';
        case 'J': return 'M';
        case 'K': return '<';
        case 'L': return '>';
        case ':': return '?';
        default : return c;
    }
}

// 将文件中的字符进行替换，并将结果写入目标文件
int replace_file(FILE* src_file, FILE* dest_file) {
    char buffer[BUFFER_SIZE];
    size_t read_count;

    while ((read_count = fread(buffer, sizeof(char), BUFFER_SIZE, src_file)) > 0) {
        for (size_t i = 0; i < read_count; i++) {
            buffer[i] = replace_char(buffer[i]);
        }

        fwrite(buffer, sizeof(char), read_count, dest_file);
    }

    return 0;
}

// 将文件中的字符恢复为原始字符，并将结果写入目标文件
int restore_file(FILE* src_file, FILE* dest_file) {
    char buffer[BUFFER_SIZE];
    size_t read_count;

    while ((read_count = fread(buffer, sizeof(char), BUFFER_SIZE, src_file)) > 0) {
        for (size_t i = 0; i < read_count; i++) {
            // 将字符再替换回原始字符
            buffer[i] = restore_char(buffer[i]);
        }

        fwrite(buffer, sizeof(char), read_count, dest_file);

    }

return 0;

}

int main(int argc, char* argv[]) {

    if (argc < 3) {
        printf("Usage: %s [-r]\n", argv[0]);
        printf(" -r: restore the file to its original content\n");
        return 1;
    }

    char* input_file = argv[1];
    char* output_file = argv[2];
    int restore_mode = (argc >= 4 && strcmp(argv[3], "-r") == 0);

    FILE* src_file = fopen(input_file, "rb");
    if (src_file == NULL) {
        printf("Failed to open input file: %s\n", input_file);
        return 1;
    }

    FILE* dest_file = fopen(output_file, "wb");
    if (dest_file == NULL) {
        printf("Failed to open output file: %s\n", output_file);
        return 1;
    }

    if (restore_mode) {
        printf("Restoring file...\n");
        restore_file(src_file, dest_file);
    } else {
        printf("Replacing file...\n");
        replace_file(src_file, dest_file);
    }

    printf("Done!\n");

    fclose(src_file);
    fclose(dest_file);

    return 0;

}

