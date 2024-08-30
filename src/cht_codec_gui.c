#include <windows.h>
#include <winuser.h>
#include <commdlg.h>
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <stdbool.h>  // Add this line to include the C99 boolean type

// Constants
#define MAX_PATH_LENGTH 260

// Global variables
HWND hwndInputFile;
HWND hwndOutputFile;
HWND hwndRestoreMode;
HBRUSH hBrushStatic;

// Function prototypes
void ProcessFiles(const wchar_t* inputFile, const wchar_t* outputFile, int restoreMode);
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);
void BrowseFile(HWND hwnd, bool saveMode, HWND hwndTarget);

// Main function
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const wchar_t CLASS_NAME[] = L"myWindowClass";
    LPCWSTR WINDOW_TITLE = L"FileProcessing";

    WNDCLASSEXW wc = { };

    wc.cbSize = sizeof(WNDCLASSEXW);
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hbrBackground = (HBRUSH)(GetStockObject(WHITE_BRUSH));
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wc.style = CS_HREDRAW | CS_VREDRAW;

    RegisterClassExW(&wc);

    HWND hwnd = CreateWindowExW(
        0,
        CLASS_NAME,
        WINDOW_TITLE,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 520, 200,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);

    // The message loop
    MSG msg = { };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

// Window procedure
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_CREATE: {
            // Create a brush and set the color
            //hBrushStatic = CreateSolidBrush(RGB(173, 216, 230));
            hBrushStatic = CreateSolidBrush(RGB(255, 255, 255));

            CreateWindowW(L"STATIC", L"Input File:", WS_VISIBLE | WS_CHILD, 10, 10, 80, 20, hwnd, NULL, NULL, NULL);
            hwndInputFile = CreateWindowW(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL, 100, 10, 300, 20, hwnd, NULL, NULL, NULL);
            CreateWindowW(L"BUTTON", L"Browse...", WS_VISIBLE | WS_CHILD, 410, 10, 80, 20, hwnd, (HMENU)1, NULL, NULL);

            CreateWindowW(L"STATIC", L"Output File:", WS_VISIBLE | WS_CHILD, 10, 40, 80, 20, hwnd, NULL, NULL, NULL);
            hwndOutputFile = CreateWindowW(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL, 100, 40, 300, 20, hwnd, NULL, NULL, NULL);
            CreateWindowW(L"BUTTON", L"Browse...", WS_VISIBLE | WS_CHILD, 410, 40, 80, 20, hwnd, (HMENU)2, NULL, NULL);

            hwndRestoreMode = CreateWindowW(L"BUTTON", L"Restore Mode", WS_VISIBLE | WS_CHILD | BS_CHECKBOX, 10, 70, 120, 20, hwnd, (HMENU)4, NULL, NULL);

            CreateWindowW(L"BUTTON", L"Process", WS_VISIBLE | WS_CHILD, 10, 100, 80, 40, hwnd, (HMENU)3, NULL, NULL);

            // Add swap button
            CreateWindowW(L"BUTTON", L"Swap", WS_VISIBLE | WS_CHILD, 410, 70, 80, 20, hwnd, (HMENU)5, NULL, NULL);
        }
        break;

        case WM_CTLCOLORSTATIC: {
            HDC hdcStatic = (HDC) wParam;
            // Set the background color
            //SetBkColor(hdcStatic, RGB(173, 216, 230));
            SetBkColor(hdcStatic, RGB(255, 255, 255));
            return (INT_PTR)hBrushStatic;
        }

        case WM_COMMAND: {
            switch (LOWORD(wParam)) {
                case 1: // Input File Browse
                    BrowseFile(hwnd, false, hwndInputFile);
                    break;
                case 2: // Output File Browse
                    BrowseFile(hwnd, true, hwndOutputFile);
                    break;
                case 3: { // Process
                        wchar_t inputFile[MAX_PATH_LENGTH];
                        wchar_t outputFile[MAX_PATH_LENGTH];

                        GetWindowTextW(hwndInputFile, inputFile, MAX_PATH_LENGTH);
                        GetWindowTextW(hwndOutputFile, outputFile, MAX_PATH_LENGTH);
                        int restoreMode = SendMessage(hwndRestoreMode, BM_GETCHECK, 0, 0) == BST_CHECKED;

                        ProcessFiles(inputFile, outputFile, restoreMode);
                    }
                    break;
                case 4: // Restore Mode Checkbox
                    if (SendMessage(hwndRestoreMode, BM_GETCHECK, 0, 0) == BST_CHECKED) {
                        SendMessage(hwndRestoreMode, BM_SETCHECK, BST_UNCHECKED, 0);
                    } else {
                        SendMessage(hwndRestoreMode, BM_SETCHECK, BST_CHECKED, 0);
                    }
                    break;
                case 5: { // Swap
                    wchar_t inputFile[MAX_PATH_LENGTH];
                    wchar_t outputFile[MAX_PATH_LENGTH];

                    // Get the contents of the two text boxes
                    GetWindowTextW(hwndInputFile, inputFile, MAX_PATH_LENGTH);
                    GetWindowTextW(hwndOutputFile, outputFile, MAX_PATH_LENGTH);

                    // Swap the contents of the two text boxes
                    SetWindowTextW(hwndInputFile, outputFile);
                    SetWindowTextW(hwndOutputFile, inputFile);
                }
                break;
            }
        }
        break;

        case WM_DESTROY:
            DeleteObject(hBrushStatic);
            PostQuitMessage(0);
            return 0;
    }

    return DefWindowProcW(hwnd, uMsg, wParam, lParam);
}

// Function to browse for a file
void BrowseFile(HWND hwnd, bool saveMode, HWND hwndTarget) {
    OPENFILENAMEW ofn;
    wchar_t szFile[MAX_PATH_LENGTH] = L"";

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = hwnd;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = L"All\0*.*\0Text\0*.TXT\0";
    ofn.nFilterIndex = 1;
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrInitialDir = NULL;
    ofn.Flags = OFN_PATHMUSTEXIST | (saveMode ? OFN_OVERWRITEPROMPT : OFN_FILEMUSTEXIST);

    if (saveMode ? GetSaveFileNameW(&ofn) : GetOpenFileNameW(&ofn)) {
        SetWindowTextW(hwndTarget, ofn.lpstrFile);
    }
}

// Function to process files based on restore mode
void ProcessFiles(const wchar_t* inputFile, const wchar_t* outputFile, int restoreMode) {
    FILE *in, *out;
    wchar_t ch;

    // Open input file
    in = _wfopen(inputFile, L"rt, ccs=UTF-8");
    if (in == NULL) {
        MessageBoxW(NULL, L"Failed to open input file!", L"Error", MB_OK);
        return;
    }

    // Open output file
    out = _wfopen(outputFile, L"wt, ccs=UTF-8");
    if (out == NULL) {
        MessageBoxW(NULL, L"Failed to open output file!", L"Error", MB_OK);
        fclose(in);
        return;
    }

    // Read input file and write to output file, optionally reversing the encoding
    while ((ch = fgetwc(in)) != WEOF) {
        if (restoreMode) {
            if (ch != '\n' && ch != '\r') {
                ch -= 0x77;
            }
        } else {
            if (ch != '\n' && ch != '\r') {
                ch += 0x77;
            }
        }
        fputwc(ch, out);
    }

    // Close files
    fclose(in);
    fclose(out);

    if (restoreMode) {
        MessageBoxW(NULL, L"File decoding completed!", L"Success", MB_OK);
    } else {
        MessageBoxW(NULL, L"File encoding completed!", L"Success", MB_OK);
    }
}
