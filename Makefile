# 源文件
SRC = src\rdc.c
SRC2 = src\char_enc_dec.c
SRC3 = src\cht_enc_dec.c
SRC_TEST = src\test.c
# SDL 库的位置
SDLDIR = D:\mingw64\x86_64-w64-mingw32\lib
# 编译参数
CFLAGS = -I $(SDLDIR)\include -L $(SDLDIR)\lib -lmingw32 -O2 #-mwindows
CFLAGS_SDL = -I $(SDLDIR)\include -L $(SDLDIR)\lib -lmingw32 -lSDL2main -lSDL2 -lSDL2_ttf -O2 -mwindows
# 选择编译器
CC = D:\mingw64\bin\g++.exe

compile: $(SRC)
	$(CC) $(SRC) $(CFLAGS_SDL) -o rdc.exe

comp2: $(SRC2)
	$(CC) $(SRC2) $(CFLAGS) -o file_enc_dec.exe

comp3: $(SRC3)
	$(CC) $(SRC3) $(CFLAGS) -o cht_enc_dec.exe

comptest: $(SRC_TEST)
	$(CC) $(SRC_TEST) $(CFLAGS) -o test.exe

clean:
	del rdc.exe \
	del file_enc_dec.exe
