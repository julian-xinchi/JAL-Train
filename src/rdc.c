

//void main() {
//    //generate Cordic tables
//    int i;
//    for (i = 0; i < 16; i++) {
//        printf("0x%08x, ", (int)(0x100000000 * atan(1.0 / (1 << i))));
//    }
//
//    //generate 1/sqrt(2) table
//    for (i = 0; i < 16; i++) {
//        printf("0x%08x, ", (int)(0x100000000 / sqrt(2.0) * (1 << i)));
//    }
//
//    return 0;
//
//}

//#include <stdio.h>
//#include <stdlib.h>
//#include <math.h>
//#include <SDL2/SDL.h>
////#include <graphics.h>
//
//const int WINDOW_WIDTH = 800;
//const int WINDOW_HEIGHT = 600;
//
//int main(int argc, char *argv[]) {
//    SDL_Window *window = NULL;
//    SDL_Renderer *renderer = NULL;
//    SDL_Event event;
//    int quit = 0;
//    double phase = 0.0;
//    double frequency = 1.0;
//    double amplitude = 100.0;
//    int center_x = WINDOW_WIDTH / 2;
//    int center_y = WINDOW_HEIGHT / 2;
//
//    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
//        fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
//        return 1;
//    }
//
//    window = SDL_CreateWindow("Sine Wave", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
//
//    if (window == NULL) {
//        fprintf(stderr, "SDL_CreateWindow failed: %s\n", SDL_GetError());
//        return 1; 
//    }
//
//    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
//
//    if (renderer == NULL) {
//        fprintf(stderr, "SDL_CreateRenderer failed: %s\n", SDL_GetError());
//        return 1;
//    }
//
//    while (!quit) {
//        while (SDL_PollEvent(&event)) {
//            if (event.type == SDL_QUIT) {
//                quit = 1;
//            }
//        }
//
//        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
//        SDL_RenderClear(renderer);
//
//        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
//        SDL_RenderDrawLine(renderer, 0, center_y, WINDOW_WIDTH, center_y);
//
//        for (int x = 0; x < WINDOW_WIDTH; x++) {
//            double y = center_y - amplitude * sin(2 * M_PI * frequency * x / WINDOW_WIDTH + phase);
//            SDL_RenderDrawPoint(renderer, x, (int) y);
//        }
//
//        SDL_RenderPresent(renderer);
//
//        phase += 0.1;
//    }
//
//    SDL_DestroyRenderer(renderer);
//    SDL_DestroyWindow(window);
//    SDL_Quit();
//
//    return 0;
//}

//#include <stdio.h>
//#include <math.h>
//#include <conio.h>
//
//const int WIDTH = 80;
//const int HEIGHT = 20;
//
//int main() {
//    for (int y = 0; y < HEIGHT; y++) {
//        for (int x = 0; x < WIDTH; x++) {
//            double y_sin = sin((double) x / WIDTH * 4 * M_PI);
//            int y_screen = (int) ((y_sin + 1) / 2 * HEIGHT);
//
//            if (y_screen == y) {
//                putchar('*');
//            } else if (y == HEIGHT - 1) {
//                putchar('-');
//            } else {
//                putchar(' ');
//            }
//        }
//
//        putchar('\n');
//    }
//
//    return 0;
//}


//////////////////////////////////////////////
//// 程序：画贝塞尔曲线的函数
//// 编译环境：Visual Studio 2019，EasyX_20211109
////
//
//#include <graphics.h>
//#include <conio.h>
//using namespace std;
//
//// 画贝塞尔曲线的函数，包括这个 Vec2 结构体
//struct Vec2
//{
//	double x, y;
//};
//void drawBezierCurve(COLORREF color, const unsigned int len, ...)
//{
//	if (len <= 0) return;
//
//	va_list list;
//	va_start(list, len);
//	Vec2* temp = new Vec2[len];
//	for (int i = 0; i < len; i++)
//		temp[i] = va_arg(list, Vec2);
//	va_end(list);
//
//	if (len == 1)
//	{
//		putpixel(temp->x, temp->y, color);
//		return;
//	}
//
//	Vec2* parent = nullptr, * child = nullptr;
//	Vec2 lastPoint = temp[0];
//	setlinecolor(color);
//	for (double LineNum = 0; LineNum < 1 + 1.0 / 100; LineNum += 1.0 / 100)
//	{
//		int size = len;
//		parent = temp;
//		while (size > 1)
//		{
//			child = new Vec2[size - 1];
//			for (int i = 0; i < size - 1; i++)
//			{
//				child[i].x = parent[i].x + (parent[i + 1].x - parent[i].x) * LineNum;
//				child[i].y = parent[i].y + (parent[i + 1].y - parent[i].y) * LineNum;
//			}
//			if (parent != temp)delete[] parent;
//			parent = child;
//			size--;
//		}
//		line(lastPoint.x, lastPoint.y, parent->x, parent->y);
//		lastPoint.x = parent->x;
//		lastPoint.y = parent->y;
//		delete[] parent;
//		parent = nullptr;
//		child = nullptr;
//	}
//	delete[] temp;
//}
//
//int main()
//{
//	initgraph(640, 480);
//
//	Vec2 a = { 100, 80 };
//	Vec2 b = { 540, 80 };
//	Vec2 c = { 540, 400 };
//	Vec2 d = { 100, 400 };
//
//	setlinecolor(BLUE);
//	line(a.x, a.y, b.x, b.y);
//	line(b.x, b.y, c.x, c.y);
//	line(c.x, c.y, d.x, d.y);
//
//	drawBezierCurve(RED, 4, a, b, c, d);
//
//	_getch();
//	closegraph();
//	return 0;
//}

//#include <stdio.h>
//#include <stdlib.h>
//#include <math.h>
//#include <SDL2/SDL.h>
//
////const int WINDOW_WIDTH = 800;
////const int WINDOW_HEIGHT = 600;
//const int WINDOW_WIDTH = 1600;
//const int WINDOW_HEIGHT = 900;
//
////void draw_sine_wave(SDL_Renderer *renderer, double amplitude, double frequency, int resolution) {
////    double x_scale = (double)WINDOW_WIDTH / resolution;
////    double y_scale = (double)WINDOW_HEIGHT / 2 / amplitude;
////    double phase = 0.0;
////
////    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
////
////    for (int i = 0; i < resolution - 1; i++) {
////        double x1 = i * x_scale;
////        double x2 = (i + 1) * x_scale;
////        double y1 = amplitude * sin(x1 * frequency + phase) * sin(16.25 * x1 * frequency + phase);
////        double y2 = amplitude * sin(x2 * frequency + phase) * sin(16.25 * x2 * frequency + phase);
////
////        SDL_RenderDrawLine(renderer, (int) x1, (int) (WINDOW_HEIGHT / 2 - y1 * y_scale), (int) x2, (int) (WINDOW_HEIGHT / 2 - y2 * y_scale));
////    }
////}
//
//void draw_sine_wave(SDL_Renderer *renderer, double amplitude, double exci_freq, double signal_freq) {
//    double exci_x_scale = (double)(exci_freq / WINDOW_WIDTH);
//    double signal_x_scale = (double)(signal_freq / WINDOW_WIDTH);
//    double y_scale = (double)WINDOW_HEIGHT / 6;
//    double phase = 0.0;
//    double pi = M_PI;
//
//    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
//    SDL_RenderDrawLine(renderer, 0, WINDOW_HEIGHT / 6, WINDOW_WIDTH, WINDOW_HEIGHT / 6);
//    SDL_RenderDrawLine(renderer, 0, WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6, WINDOW_WIDTH, WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6);
//    SDL_RenderDrawLine(renderer, 0, WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6, WINDOW_WIDTH, WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6);
//
//    SDL_SetRenderDrawColor(renderer, 64, 64, 64, 255);
//    for (int i = 0; i < ceil(exci_freq * 2); i++) {
//        int current_x = (int)(i * WINDOW_WIDTH / (exci_freq * 2));
//        //SDL_RenderDrawLine(renderer, current_x, WINDOW_HEIGHT / 6, current_x, WINDOW_HEIGHT * 5 / 6);
//        SDL_RenderDrawLine(renderer, current_x, 0, current_x, WINDOW_HEIGHT - 1);
//    }
//
//    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
//
//    for (int i = 0; i <WINDOW_WIDTH  - 1; i++) {
//        double x1 = i;
//        double x2 = i+1;
//        double exci_x1 = i * exci_x_scale;
//        double signal_x1 = i * signal_x_scale;
//        double exci_x2 = (i + 1) * exci_x_scale;
//        double signal_x2 = (i + 1) * signal_x_scale;
//        double exci_y1 = amplitude * sin(2 * pi * exci_x1 + phase);
//        double exci_y2 = amplitude * sin(2 * pi * exci_x2 + phase);
//        double signal_y1 = amplitude * sin(2 * pi * signal_x1 + phase);
//        double signal_y2 = amplitude * sin(2 * pi * signal_x2 + phase);
//        double y1 = amplitude * sin(2 * pi * exci_x1 + phase) * sin(2 * pi * signal_x1 + phase);
//        double y2 = amplitude * sin(2 * pi * exci_x2 + phase) * sin(2 * pi * signal_x2 + phase);
//
//        SDL_RenderDrawLine(renderer, (int) x1, (int) (WINDOW_HEIGHT / 6 - exci_y1 * y_scale),
//                                     (int) x2, (int) (WINDOW_HEIGHT / 6 - exci_y2 * y_scale));
//        SDL_RenderDrawLine(renderer, (int) x1, (int) (WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6 - signal_y1 * y_scale),
//                                     (int) x2, (int) (WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6 - signal_y2 * y_scale));
//        SDL_RenderDrawLine(renderer, (int) x1, (int) (WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6 - y1 * y_scale),
//                                     (int) x2, (int) (WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6 - y2 * y_scale));
//    }
//
//    SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
//    for (int i = 0; i < ceil(signal_freq * 2); i++) {
//        int current_x = (int)(i * WINDOW_WIDTH / (signal_freq * 2));
//        SDL_RenderDrawLine(renderer, current_x, 0, current_x, WINDOW_HEIGHT - 1);
//        //SDL_RenderDrawPoint(renderer, i, WINDOW_HEIGHT / 6);
//        //SDL_RenderDrawPoint(renderer, i, WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6);
//        //SDL_RenderDrawPoint(renderer, i, WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6);
//    }
//
//}
//
//int main(int argc, char *argv[]) {
//    SDL_Window *window = NULL;
//    SDL_Renderer *renderer = NULL;
//    SDL_Event event;
//    int quit = 0;
////    double amplitude = 1.0;
////    double frequency = 1.0;
////    int resolution = 100;
//    double amplitude = 0.8;
//    double exci_freq = 32.5;
//    double signal_freq = 2.0;
//
//    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
//        fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
//        return 1;
//    }
//
//    window = SDL_CreateWindow("Sine Wave", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
//
//    if (window == NULL) {
//        fprintf(stderr, "SDL_CreateWindow failed: %s\n", SDL_GetError());
//        return 1; 
//    }
//
//    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
//
//    if (renderer == NULL) {
//        fprintf(stderr, "SDL_CreateRenderer failed: %s\n", SDL_GetError());
//        return 1;
//    }
//
//    while (!quit) {
//        while (SDL_PollEvent(&event)) {
//            if (event.type == SDL_QUIT) {
//                quit = 1;
//            }
//        }
//
//        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
//        SDL_RenderClear(renderer);
//
//        //draw_sine_wave(renderer, amplitude, frequency, resolution);
//        draw_sine_wave(renderer, amplitude, exci_freq, signal_freq);
//
//        SDL_RenderPresent(renderer);
//    }
//
//    SDL_DestroyRenderer(renderer);
//    SDL_DestroyWindow(window);
//    SDL_Quit();
//
//    return 0;
//
//}

//#include <stdio.h>
//#include <stdlib.h>
//#include <stdint.h>
//#include <math.h>
////#include <SDL2/SDL.h>
//
//#define WIDTH 1600
//#define HEIGHT 900
//#define BYTES_PER_PIXEL 3
//#define BMP_HEADER_SIZE 54
//#define FILE_SIZE WIDTH * HEIGHT * BYTES_PER_PIXEL + BMP_HEADER_SIZE
//
//void draw_sine_wave(uint8_t *data, double amplitude, double exci_freq, double signal_freq) {
//    double exci_x_scale = (double)(exci_freq / WIDTH);
//    double signal_x_scale = (double)(signal_freq / WIDTH);
//    double y_scale = (double)HEIGHT / 6;
//    double phase = 0.0;
//    double pi = 3.1415926;
//    double x1,x2,y1,y2,y;
//    int dy;
//
//    for (int i = 0; i < WIDTH; i++) {
//        dy = (int)(HEIGHT * 5 / 6);
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL] = 0x3f;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 1] = 0x3f;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 2] = 0x3f;
//
//        dy = (int)(HEIGHT * 3 / 6);
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL] = 0x3f;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 1] = 0x3f;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 2] = 0x3f;
//
//        dy = (int)(HEIGHT * 1 / 6);
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL] = 0x3f;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 1] = 0x3f;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 2] = 0x3f;
//    }
//
//    for (int i = 0; i < ceil(exci_freq * 2); i++) {
//        int current_x = (int)(i * WIDTH / (exci_freq * 2));
//        for (int j = 0; j < HEIGHT; j++) {
//            data[j * WIDTH * BYTES_PER_PIXEL + current_x * BYTES_PER_PIXEL] = 0x3f;
//            data[j * WIDTH * BYTES_PER_PIXEL + current_x * BYTES_PER_PIXEL + 1] = 0x3f;
//            data[j * WIDTH * BYTES_PER_PIXEL + current_x * BYTES_PER_PIXEL + 2] = 0x3f;
//        }
//    }
//
//    for (int i = 0; i < WIDTH; i++) {
//        x1 = i * exci_x_scale;
//        y1 = sin(2 * pi * x1 + phase);
//        y = amplitude * y1;
//        dy = (int)(y * y_scale + HEIGHT * 5 / 6);
//
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL] = 0x00;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 1] = 0x00;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 2] = 0xff;
//
//        x2 = i * signal_x_scale;
//        y2 = sin(2 * pi * x2 + phase);
//        y = amplitude * y2;
//        dy = (int)(y * y_scale + HEIGHT * 3 / 6);
//
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL] = 0xff;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 1] = 0xff;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 2] = 0xff;
//
//        y = amplitude * y1 * y2;
//        dy = (int)(y * y_scale + HEIGHT * 1 / 6);
//
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL] = 0x00;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 1] = 0x00;
//        data[dy * WIDTH * BYTES_PER_PIXEL + i * BYTES_PER_PIXEL + 2] = 0xff;
//
//    }
//
//    for (int i = 0; i < ceil(signal_freq * 2); i++) {
//        int current_x = (int)(i * WIDTH / (signal_freq * 2));
//        for (int j = 0; j < HEIGHT; j++) {
//            data[j * WIDTH * BYTES_PER_PIXEL + current_x * BYTES_PER_PIXEL] = 0x7f;
//            data[j * WIDTH * BYTES_PER_PIXEL + current_x * BYTES_PER_PIXEL + 1] = 0x00;
//            data[j * WIDTH * BYTES_PER_PIXEL + current_x * BYTES_PER_PIXEL + 2] = 0x00;
//        }
//    }
//
//}
//
//int main() {
//
//uint8_t *data = (uint8_t *)malloc(WIDTH * HEIGHT * BYTES_PER_PIXEL);
//
//if (data == NULL) {
//    printf("Error: failed to allocate memory for image data\n");
//    return -1;
//}
//
//double amplitude = 0.8;
//double exci_freq = 16.3;
//double signal_freq = 1.5;
//
//draw_sine_wave(data, amplitude, exci_freq, signal_freq);
//
//FILE *fp;
//fp = fopen("func_wave.bmp", "wb");
//if (fp == NULL) {
//    printf("Error: failed to create bmp file\n");
//    return -1;
//}
//
//uint8_t bmp_header[BMP_HEADER_SIZE] = {
//    'B', 'M',             // BMP file magic number
//    FILE_SIZE & 0xff,     // file size
//    (FILE_SIZE >> 8) & 0xff,
//    (FILE_SIZE >> 16) & 0xff,
//    (FILE_SIZE >> 24) & 0xff,
//    0, 0, 0, 0,           // reserved
//    BMP_HEADER_SIZE, 0, 0, 0,  // data offset
//    40, 0, 0, 0,          // header size
//    WIDTH & 0xff,         // image width
//    (WIDTH >> 8) & 0xff,
//    (WIDTH >> 16) & 0xff,
//    (WIDTH >> 24) & 0xff,
//    HEIGHT & 0xff,        // image height
//    (HEIGHT >> 8) & 0xff,
//    (HEIGHT >> 16) & 0xff,
//    (HEIGHT >> 24) & 0xff,
//    1, 0,                 // color planes
//    BYTES_PER_PIXEL * 8,  // bits per pixel
//    0, 0, 0, 0,           // compression method, image size, horizontal and vertical resolution, colors, important colors
//};
//
//fwrite(bmp_header, sizeof(bmp_header), 1, fp);
//fwrite(data, WIDTH * HEIGHT * BYTES_PER_PIXEL, 1, fp);
//
//fclose(fp);
//free(data);
//
//printf("func_wave.bmp created\n");
//return 0;
//
//}

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>

//const int DEFAULT_WINDOW_WIDTH = 1600;
//const int DEFAULT_WINDOW_HEIGHT = 900;
//const double DEFAULT_AMPLITUDE = 0.8;
//const double DEFAULT_EXCI_FREQ = 32.5;
//const double DEFAULT_SIGNAL_FREQ = 2.0;
////const int MAX_TEXT_LENGTH = 20;
const int WINDOW_WIDTH = 1600;
const int WINDOW_HEIGHT = 900;

//void draw_sine_wave(SDL_Renderer *renderer, double amplitude, double exci_freq, double signal_freq, int WINDOW_WIDTH, int WINDOW_HEIGHT) {
//void draw_sine_wave(SDL_Renderer *renderer, double amplitude, double exci_freq, double signal_freq) {
void draw_sine_wave(SDL_Renderer *renderer, double amplitude, double exci_freq, double signal_freq, double noise_factor) {
    // 绘制正弦波的代码
    // ...
    double exci_x_scale = (double)(exci_freq / WINDOW_WIDTH);
    double signal_x_scale = (double)(signal_freq / WINDOW_WIDTH);
    double y_scale = (double)WINDOW_HEIGHT / 6;
    double phase = 0.0;
    double pi = M_PI;

    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
    SDL_RenderDrawLine(renderer, 0, WINDOW_HEIGHT / 6, WINDOW_WIDTH, WINDOW_HEIGHT / 6);
    SDL_RenderDrawLine(renderer, 0, WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6, WINDOW_WIDTH, WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6);
    SDL_RenderDrawLine(renderer, 0, WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6, WINDOW_WIDTH, WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6);

    SDL_SetRenderDrawColor(renderer, 64, 64, 64, 255);
    for (int i = 0; i < ceil(exci_freq * 2); i++) {
        int current_x = (int)(i * WINDOW_WIDTH / (exci_freq * 2));
        //SDL_RenderDrawLine(renderer, current_x, WINDOW_HEIGHT / 6, current_x, WINDOW_HEIGHT * 5 / 6);
        SDL_RenderDrawLine(renderer, current_x, 0, current_x, WINDOW_HEIGHT - 1);
    }

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);

    for (int i = 0; i <WINDOW_WIDTH  - 1; i++) {
        double x1 = i;
        double x2 = i+1;
        double exci_x1 = i * exci_x_scale;
        double signal_x1 = i * signal_x_scale;
        double exci_x2 = (i + 1) * exci_x_scale;
        double signal_x2 = (i + 1) * signal_x_scale;
        double exci_y1 = amplitude * sin(2 * pi * exci_x1 + phase);
        double exci_y2 = amplitude * sin(2 * pi * exci_x2 + phase);
        double signal_y1 = amplitude * sin(2 * pi * signal_x1 + phase);
        double signal_y2 = amplitude * sin(2 * pi * signal_x2 + phase);
        //double y1 = amplitude * sin(2 * pi * exci_x1 + phase) * sin(2 * pi * signal_x1 + phase);
        //double y2 = amplitude * sin(2 * pi * exci_x2 + phase) * sin(2 * pi * signal_x2 + phase);
        //double noise = add_noise ? amplitude * 0.1 * ((double)rand() / RAND_MAX - 0.5) : 0.0;
        double noise = amplitude * noise_factor * ((double)rand() / RAND_MAX - 0.5);
        double y1 = amplitude * sin(2 * pi * exci_x1 + phase) * sin(2 * pi * signal_x1 + phase) + noise;
        double y2 = amplitude * sin(2 * pi * exci_x2 + phase) * sin(2 * pi * signal_x2 + phase) + noise;

        SDL_RenderDrawLine(renderer, (int) x1, (int) (WINDOW_HEIGHT / 6 - exci_y1 * y_scale),
                                     (int) x2, (int) (WINDOW_HEIGHT / 6 - exci_y2 * y_scale));
        SDL_RenderDrawLine(renderer, (int) x1, (int) (WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6 - signal_y1 * y_scale),
                                     (int) x2, (int) (WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6 - signal_y2 * y_scale));
        SDL_RenderDrawLine(renderer, (int) x1, (int) (WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6 - y1 * y_scale),
                                     (int) x2, (int) (WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6 - y2 * y_scale));
    }

    SDL_SetRenderDrawColor(renderer, 0, 0, 255, 255);
    for (int i = 0; i < ceil(signal_freq * 2); i++) {
        int current_x = (int)(i * WINDOW_WIDTH / (signal_freq * 2));
        SDL_RenderDrawLine(renderer, current_x, 0, current_x, WINDOW_HEIGHT - 1);
        //SDL_RenderDrawPoint(renderer, i, WINDOW_HEIGHT / 6);
        //SDL_RenderDrawPoint(renderer, i, WINDOW_HEIGHT / 3 + WINDOW_HEIGHT / 6);
        //SDL_RenderDrawPoint(renderer, i, WINDOW_HEIGHT * 2 / 3 + WINDOW_HEIGHT / 6);
    }

}

//void render_text(SDL_Renderer *renderer, TTF_Font *font, const char *text, SDL_Rect rect) {
//    SDL_Surface *surface;
//    SDL_Texture *texture;
//    SDL_Color color = {255, 255, 255, 255};
//
//    surface = TTF_RenderUTF8_Blended(font, text, color);
//    texture = SDL_CreateTextureFromSurface(renderer, surface);
//
//    SDL_FreeSurface(surface);
//
//    SDL_RenderCopy(renderer, texture, NULL, &rect);
//
//    SDL_DestroyTexture(texture);
//}
//
//int main(int argc, char *argv[]) {
//    SDL_Window *window = NULL;
//    SDL_Renderer *renderer = NULL;
//    SDL_Event event;
//    int quit = 0;
//    double amplitude = DEFAULT_AMPLITUDE;
//    double exci_freq = DEFAULT_EXCI_FREQ;
//    double signal_freq = DEFAULT_SIGNAL_FREQ;
//    int window_width = DEFAULT_WINDOW_WIDTH;
//    int window_height = DEFAULT_WINDOW_HEIGHT;
//    char amplitude_text[20] = "1.0";
//    char exci_freq_text[20] = "32.5";
//    char signal_freq_text[20] = "2.0";
//    char window_width_text[20] = "1600";
//    char window_height_text[20] = "900";
//    TTF_Font *font;
//    SDL_Surface *surface;
//    SDL_Texture *texture;
//    SDL_Rect text_rect;
//    SDL_Rect input_rect;
//    SDL_Rect button_rect;
//    SDL_Rect output_rect;
//    SDL_bool input_active = SDL_FALSE;
//    SDL_bool redraw = SDL_TRUE;
//    SDL_bool quit_on_button_click = SDL_FALSE;
//
//    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
//        fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
//        return 1;
//    }
//
//    if (TTF_Init() < 0) {
//        fprintf(stderr, "TTF_Init failed: %s\n", TTF_GetError());
//        return 1;
//    }
//
//    window = SDL_CreateWindow("Sine Wave", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
//
//    if (window == NULL) {
//        fprintf(stderr, "SDL_CreateWindow failed: %s\n", SDL_GetError());
//        return 1; 
//    }
//
//    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
//
//    if (renderer == NULL) {
//        fprintf(stderr, "SDL_CreateRenderer failed: %s\n", SDL_GetError());
//        return 1;
//    }
//
//    font = TTF_OpenFont("C:\\Windows\\Fonts\\DejaVuSans.ttf", 16);
//
//    if (font == NULL) {
//        fprintf(stderr, "TTF_OpenFont failed: %s\n", TTF_GetError());
//        return 1;
//    }
//
//    while (!quit) {
//        // 处理事件
//        while (SDL_PollEvent(&event)) {
//            switch (event.type) {
//                case SDL_QUIT:
//                    quit = 1;
//                    break;
//                case SDL_KEYDOWN:
//                    if (input_active) {
//                        if (event.key.keysym.sym == SDLK_RETURN) {
//                            input_active = SDL_FALSE;
//                        } else if (event.key.keysym.sym == SDLK_BACKSPACE && strlen(amplitude_text) > 0) {
//                            amplitude_text[strlen(amplitude_text) - 1] = '\0';
//                            redraw = SDL_TRUE;
//                        } else if (strlen(amplitude_text) < 19 && event.key.keysym.sym >= SDLK_0 && event.key.keysym.sym <= SDLK_9) {
//                            amplitude_text[strlen(amplitude_text)] = event.key.keysym.sym;
//                            redraw = SDL_TRUE;
//                        }
//                    }
//                    break;
//                case SDL_MOUSEBUTTONDOWN:
//                    if (event.button.button == SDL_BUTTON_LEFT) {
//                        int x = event.button.x;
//                        int y = event.button.y;
//                        if (x >= button_rect.x && y >= button_rect.y && x < button_rect.x + button_rect.w && y < button_rect.y + button_rect.h) {
//                            amplitude = atof(amplitude_text);
//                            exci_freq = atof(exci_freq_text);
//                            signal_freq = atof(signal_freq_text);
//                            window_width = atoi(window_width_text);
//                            window_height = atoi(window_height_text);
//                            quit_on_button_click = SDL_TRUE;
//                        } else if (x >= input_rect.x && y >= input_rect.y && x < input_rect.x + input_rect.w && y < input_rect.y + input_rect.h) {
//                            input_active = SDL_TRUE;
//                        }
//                    }
//                    break;
//            }
//        }
//
//        if (redraw) {
//            SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
//            SDL_RenderClear(renderer);
//
//            text_rect.x = 10;
//            text_rect.y = 10;
//            text_rect.w = 60;
//            text_rect.h = 20;
//
//            render_text(renderer, font, "Window Width:", text_rect);
//
//            input_rect.x = text_rect.x + text_rect.w + 5;
//            input_rect.y = text_rect.y;
//            input_rect.w = 60;
//            input_rect.h = 20;
//
//            if (input_active && input_rect.h > 0) {
//                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
//                SDL_RenderFillRect(renderer, &input_rect);
//            }
//
//            if (!input_active && strlen(window_width_text) > 0) {
//                output_rect.x = input_rect.x;
//                output_rect.y = input_rect.y;
//                output_rect.w = input_rect.w;
//                output_rect.h = input_rect.h;
//
//                render_text(renderer, font, window_width_text, output_rect);
//            }
//
//            text_rect.y += text_rect.h + 10;
//
//            render_text(renderer, font, "Window Height:", text_rect);
//
//            input_rect.y += text_rect.h + 10;
//
//            if (input_active && input_rect.h > 0) {
//                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
//                SDL_RenderFillRect(renderer, &input_rect);
//            }
//
//            if (!input_active && strlen(window_height_text) > 0) {
//                output_rect.x = input_rect.x;
//                output_rect.y = input_rect.y;
//                output_rect.w = input_rect.w;
//                output_rect.h = input_rect.h;
//
//                render_text(renderer, font, window_height_text, output_rect);
//            }
//
//            text_rect.y += text_rect.h + 10;
//
//            render_text(renderer, font, "Amplitude:", text_rect);
//
//            input_rect.y += text_rect.h + 10;
//
//            if (input_active && input_rect.h > 0) {
//                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
//                SDL_RenderFillRect(renderer, &input_rect);
//            }
//
//            if (!input_active && strlen(amplitude_text) > 0) {
//                output_rect.x = input_rect.x;
//                output_rect.y = input_rect.y;
//                output_rect.w = input_rect.w;
//                output_rect.h = input_rect.h;
//
//                render_text(renderer, font, amplitude_text, output_rect);
//            }
//
//            text_rect.y += text_rect.h + 10;
//
//            render_text(renderer, font, "Excitation Frequency:", text_rect);
//
//            input_rect.y += text_rect.h + 10;
//
//            if (input_active && input_rect.h > 0) {
//                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
//                SDL_RenderFillRect(renderer, &input_rect);
//            }
//
//            if (!input_active && strlen(exci_freq_text) > 0) {
//                output_rect.x = input_rect.x;
//                output_rect.y = input_rect.y;
//                output_rect.w = input_rect.w;
//                output_rect.h = input_rect.h;
//
//                render_text(renderer, font, exci_freq_text, output_rect);
//            }
//
//            text_rect.y += text_rect.h + 10;
//
//            render_text(renderer, font, "Signal Frequency:", text_rect);
//
//            input_rect.y += text_rect.h + 10;
//
//            if (input_active && input_rect.h > 0) {
//                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
//                SDL_RenderFillRect(renderer, &input_rect);
//            }
//
//            if (!input_active && strlen(signal_freq_text) > 0) {
//                output_rect.x = input_rect.x;
//                output_rect.y = input_rect.y;
//                output_rect.w = input_rect.w;
//                output_rect.h = input_rect.h;
//
//                render_text(renderer, font, signal_freq_text, output_rect);
//            }
//
//            button_rect.x = 10;
//            button_rect.y = input_rect.y + input_rect.h + 10;
//            button_rect.w = 60;
//            button_rect.h = 20;
//
//            if (quit_on_button_click) {
//                SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255);
//            } else {
//                SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
//            }
//
//            SDL_RenderFillRect(renderer, &button_rect);
//
//            render_text(renderer, font, "Generate", button_rect);
//
//            SDL_RenderPresent(renderer);
//
//            redraw = SDL_FALSE;
//        }
//
//        draw_sine_wave(renderer, amplitude, exci_freq, signal_freq, window_width, window_height);
//
//        SDL_Delay(2000);
//
//        //if (quit_on_button_click) {
//        //    break;
//        //}
//    }
//
//    SDL_DestroyRenderer(renderer);
//    SDL_DestroyWindow(window);
//
//    TTF_Quit();
//    SDL_Quit();
//
//    return 0;
//
//}

int main(int argc, char *argv[]) {
    SDL_Window *window = NULL;
    SDL_Renderer *renderer = NULL;
    SDL_Event event;
    TTF_Font *font = NULL;
    SDL_Surface *text_surface = NULL;
    SDL_Texture *text_texture = NULL;
    SDL_Rect text_rect;
    SDL_Rect text_rect_exci;
    SDL_Rect text_rect_sig;
    SDL_Rect text_rect_nf;
    SDL_Rect button_rect;
    SDL_Color text_color_par = {15, 15, 15};
    SDL_Color text_color = {255, 255, 255};
    Sint32 cursor = 0;
    Sint32 selection_len = 0;
    char* composition;
    double amplitude = 0.8;
    double exci_freq = 32.5;
    double signal_freq = 2.0;
    double noise_factor = 0.0;
    char amplitude_text[20] = "0.8";
    char exci_freq_text[20] = "32.5";
    char signal_freq_text[20] = "2.0";
    char noise_factor_text[20] = "0.0";
    int quit = 0;
    SDL_bool redraw = SDL_TRUE;
    SDL_bool amp_text_enable = SDL_FALSE;
    SDL_bool exci_freq_text_enable = SDL_FALSE;
    SDL_bool signal_freq_text_enable = SDL_FALSE;
    SDL_bool noise_factor_text_enable = SDL_FALSE;
    //int pos_x_t, pos_y_t;

    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
        return 1;
    }

    if (TTF_Init() < 0) {
        fprintf(stderr, "TTF_Init failed: %s\n", TTF_GetError());
        return 1;
    }

    font = TTF_OpenFont("C:\\Windows\\Fonts\\Arial.ttf", 16);

    if (font == NULL) {
        fprintf(stderr, "TTF_OpenFont failed: %s\n", TTF_GetError());
        return 1;
    }

    window = SDL_CreateWindow("Sine Wave", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);

    if (window == NULL) {
        fprintf(stderr, "SDL_CreateWindow failed: %s\n", SDL_GetError());
        return 1; 
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    if (renderer == NULL) {
        fprintf(stderr, "SDL_CreateRenderer failed: %s\n", SDL_GetError());
        return 1;
    }

    while (!quit) {
        if (redraw) {
            // Clear screen
            SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
            SDL_RenderClear(renderer);

            if (amplitude > 1.0) {
                amplitude = 1.0;
                strcpy(amplitude_text, "1.0");
            } else if (amplitude < 0.0) {
                amplitude = 0.0;
                strcpy(amplitude_text, "0.0");
            }

            if (noise_factor > 0.5) {
                noise_factor = 0.5;
                strcpy(noise_factor_text, "0.5");
            } else if (noise_factor < 0.0) {
                noise_factor = 0.0;
                strcpy(noise_factor_text, "0.0");
            }

            draw_sine_wave(renderer, amplitude, exci_freq, signal_freq, noise_factor);

            // Render amplitude text box
            text_surface = TTF_RenderText_Solid(font, "Amplitude(0.0~1.0):", text_color);
            text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
            text_rect.x = 0;
            text_rect.y = 0;
            text_rect.w = text_surface->w;
            text_rect.h = text_surface->h;
            //pos_x_t = text_surface->w;
            //pos_y_t = text_surface->h;
            SDL_RenderCopy(renderer, text_texture, NULL, &text_rect);
            text_rect.x = text_surface->w + 10;

            if (amplitude_text [0] != '\0') {
                text_surface = TTF_RenderText_Solid(font, amplitude_text, text_color_par);
                text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
                //text_rect.x = pos_x_t + 10;
                text_rect.w = text_surface->w;
                text_rect.h = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect);
                SDL_RenderCopy(renderer, text_texture, NULL, &text_rect);
            } else {
                //text_rect.x = pos_x_t + 10;
                text_rect.w = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect);
            }

            // Render excitation waves text box
            text_surface = TTF_RenderText_Solid(font, "Excitation waves(10.0~100.0):", text_color);
            text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
            //text_rect_exci.x = 0;
            //text_rect_exci.y = pos_y_t + 10;
            text_rect_exci.x = text_rect.x + text_rect.w + 10;
            text_rect_exci.y = 0;
            text_rect_exci.w = text_surface->w;
            text_rect_exci.h = text_surface->h;
            //pos_x_t = text_surface->w;
            //pos_y_t = text_rect_exci.y + text_surface->h;
            SDL_RenderCopy(renderer, text_texture, NULL, &text_rect_exci);
            text_rect_exci.x = text_rect_exci.x + text_rect_exci.w + 10;

            if (exci_freq_text [0] != '\0') {
                text_surface = TTF_RenderText_Solid(font, exci_freq_text, text_color_par);
                text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
                //text_rect_exci.x = pos_x_t + 10;
                text_rect_exci.w = text_surface->w;
                text_rect_exci.h = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect_exci);
                SDL_RenderCopy(renderer, text_texture, NULL, &text_rect_exci);
            } else {
                //text_rect_exci.x = pos_x_t + 10;
                text_rect_exci.w = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect_exci);
            }

            // Render signal waves text box
            text_surface = TTF_RenderText_Solid(font, "Signal waves(0.5~5.0):", text_color);
            text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
            //text_rect_sig.x = 0;
            //text_rect_sig.y = pos_y_t + 10;
            text_rect_sig.x = text_rect_exci.x + text_rect_exci.w + 10;
            text_rect_sig.y = 0;
            text_rect_sig.w = text_surface->w;
            text_rect_sig.h = text_surface->h;
            //pos_x_t = text_surface->w;
            SDL_RenderCopy(renderer, text_texture, NULL, &text_rect_sig);
            text_rect_sig.x = text_rect_sig.x + text_rect_sig.w + 10;

            if (signal_freq_text [0] != '\0') {
                text_surface = TTF_RenderText_Solid(font, signal_freq_text, text_color_par);
                text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
                //text_rect_sig.x = pos_x_t + 10;
                text_rect_sig.w = text_surface->w;
                text_rect_sig.h = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect_sig);
                SDL_RenderCopy(renderer, text_texture, NULL, &text_rect_sig);
            } else {
                //text_rect_sig.x = pos_x_t + 10;
                text_rect_sig.w = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect_sig);
            }

            // Render noise factor text box
            text_surface = TTF_RenderText_Solid(font, "Noise factor(0.0~0.5):", text_color);
            text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
            text_rect_nf.x = text_rect_sig.x + text_rect_sig.w + 10;
            text_rect_nf.y = 0;
            text_rect_nf.w = text_surface->w;
            text_rect_nf.h = text_surface->h;
            //pos_x_t = text_surface->w;
            SDL_RenderCopy(renderer, text_texture, NULL, &text_rect_nf);
            text_rect_nf.x = text_rect_nf.x + text_rect_nf.w + 10;

            if (noise_factor_text [0] != '\0') {
                text_surface = TTF_RenderText_Solid(font, noise_factor_text, text_color_par);
                text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
                //text_rect_nf.x = pos_x_t + 10;
                text_rect_nf.w = text_surface->w;
                text_rect_nf.h = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect_nf);
                SDL_RenderCopy(renderer, text_texture, NULL, &text_rect_nf);
            } else {
                //text_rect_nf.x = pos_x_t + 10;
                text_rect_nf.w = text_surface->h;
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 63);
                SDL_RenderFillRect(renderer, &text_rect_nf);
            }

            // Render "Generate" button
            text_surface = TTF_RenderText_Solid(font, "Generate", text_color);
            text_texture = SDL_CreateTextureFromSurface(renderer, text_surface);
            button_rect.x = 0;
            button_rect.y = WINDOW_HEIGHT - 1 - text_surface->h * 1.3;
            button_rect.w = text_surface->w * 1.3;
            button_rect.h = text_surface->h * 1.3;
            SDL_SetRenderDrawColor(renderer, 127, 63, 127, 255);
            SDL_RenderFillRect(renderer, &button_rect);
            button_rect.x = text_surface->w * 0.15;
            button_rect.y = WINDOW_HEIGHT - 1 - text_surface->h * 1.15;
            button_rect.w = text_surface->w;
            button_rect.h = text_surface->h;
            SDL_RenderCopy(renderer, text_texture, NULL, &button_rect);

            SDL_RenderPresent(renderer);

            redraw = SDL_FALSE;

        } else {

            SDL_Delay(200);

        }

        while (SDL_PollEvent(&event)) {
            switch (event.type) {
                case SDL_QUIT:
                    quit = 1;
                    break;
                case SDL_TEXTINPUT:
                    {
                        if (amp_text_enable) {
                            strcat(amplitude_text, event.text.text);
                        } else if (exci_freq_text_enable) {
                            strcat(exci_freq_text, event.text.text);
                        } else if (signal_freq_text_enable) {
                            strcat(signal_freq_text, event.text.text);
                        } else if (noise_factor_text_enable) {
                            strcat(noise_factor_text, event.text.text);
                        }
                        redraw = SDL_TRUE;
                    }
                    break;
                case SDL_TEXTEDITING:
                    {
                        composition = event.edit.text;
                        cursor = event.edit.start;
                        selection_len = event.edit.length;
                        printf("composition: %s, cursor: %d, selection_len: %d\n", cursor, selection_len, composition);
                    }
                    break;
                case SDL_MOUSEBUTTONDOWN:
                    {
                        int x = event.button.x;
                        int y = event.button.y;
                        if (x >= text_rect.x && x < text_rect.x + text_rect.w &&
                            y >= text_rect.y && y < text_rect.y + text_rect.h) {
                            SDL_StartTextInput();
                            amp_text_enable = SDL_TRUE;
                            exci_freq_text_enable = SDL_FALSE;
                            signal_freq_text_enable = SDL_FALSE;
                            noise_factor_text_enable = SDL_FALSE;
                        } else if (x >= text_rect_exci.x && x < text_rect_exci.x + text_rect_exci.w &&
                                   y >= text_rect_exci.y && y < text_rect_exci.y + text_rect_exci.h) {
                            SDL_StartTextInput();
                            amp_text_enable = SDL_FALSE;
                            exci_freq_text_enable = SDL_TRUE;
                            signal_freq_text_enable = SDL_FALSE;
                            noise_factor_text_enable = SDL_FALSE;
                        } else if (x >= text_rect_sig.x && x < text_rect_sig.x + text_rect_sig.w &&
                                   y >= text_rect_sig.y && y < text_rect_sig.y + text_rect_sig.h) {
                            SDL_StartTextInput();
                            amp_text_enable = SDL_FALSE;
                            exci_freq_text_enable = SDL_FALSE;
                            signal_freq_text_enable = SDL_TRUE;
                            noise_factor_text_enable = SDL_FALSE;
                        } else if (x >= text_rect_nf.x && x < text_rect_nf.x + text_rect_nf.w &&
                                   y >= text_rect_nf.y && y < text_rect_nf.y + text_rect_nf.h) {
                            SDL_StartTextInput();
                            amp_text_enable = SDL_FALSE;
                            exci_freq_text_enable = SDL_FALSE;
                            signal_freq_text_enable = SDL_FALSE;
                            noise_factor_text_enable = SDL_TRUE;
                        } else if (x >= button_rect.x && x < button_rect.x + button_rect.w &&
                                   y >= button_rect.y && y < button_rect.y + button_rect.h) {
                            amplitude = atof(amplitude_text);
                            exci_freq = atof(exci_freq_text);
                            signal_freq = atof(signal_freq_text);
                            noise_factor = atof(noise_factor_text);
                            redraw = SDL_TRUE;
                        } else {
                            SDL_StopTextInput();
                        }
                    }
                    break;
                case SDL_KEYDOWN:
                    {
                        if (event.key.keysym.sym == SDLK_RETURN) {
                            amplitude = atof(amplitude_text);
                            exci_freq = atof(exci_freq_text);
                            signal_freq = atof(signal_freq_text);
                            noise_factor = atof(noise_factor_text);
                        } else if (event.key.keysym.sym == SDLK_BACKSPACE) {
                            if (amp_text_enable && strlen(amplitude_text) > 0) {
                                amplitude_text[strlen(amplitude_text) - 1] = '\0';
                                redraw = SDL_TRUE;
                            } else if (exci_freq_text_enable && strlen(exci_freq_text) > 0) {
                                exci_freq_text[strlen(exci_freq_text) - 1] = '\0';
                                redraw = SDL_TRUE;
                            } else if (signal_freq_text_enable && strlen(signal_freq_text) > 0) {
                                signal_freq_text[strlen(signal_freq_text) - 1] = '\0';
                                redraw = SDL_TRUE;
                            } else if (noise_factor_text_enable && strlen(noise_factor_text) > 0) {
                                noise_factor_text[strlen(noise_factor_text) - 1] = '\0';
                                redraw = SDL_TRUE;
                            } else {
                                SDL_StopTextInput();
                            }
                        }
                    }
                    break;
            }
        }
    }

    //int t = round(SDL_GetTicks() / 1000);

    // Clean up
    SDL_FreeSurface(text_surface);
    SDL_DestroyTexture(text_texture);

    TTF_CloseFont(font);
    TTF_Quit();
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;

}
