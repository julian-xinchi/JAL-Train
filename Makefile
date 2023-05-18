# 源文件
SRC = src\rdc.c
SRC2 = src\char_enc_dec.c
# SDL 库的位置
SDLDIR = D:\mingw64\x86_64-w64-mingw32\lib
# 编译参数
CFLAGS = -I $(SDLDIR)\include -L $(SDLDIR)\lib -lmingw32 -lSDL2main -lSDL2 -lSDL2_ttf -O2 -mwindows
CFLAGS2 = -I $(SDLDIR)\include -L $(SDLDIR)\lib -lmingw32 -O2 -mwindows
# 选择编译器
CC = D:\mingw64\bin\g++.exe

compile: $(SRC)
	$(CC) $(SRC) $(CFLAGS) -o rdc.exe

compile2: $(SRC2)
	$(CC) $(SRC2) $(CFLAGS2) -o file_enc_dec.exe

clean:
	del rdc.exe
