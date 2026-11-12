#include <windows.h>
#include <wchar.h>

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR arguments, int show)
{
    (void)instance;
    (void)previous;
    (void)show;
    (void)arguments;
    wchar_t directory[32768];
    DWORD length = GetModuleFileNameW(NULL, directory, 32768);
    if (!length || length >= 32768) return 2;
    wchar_t *separator = wcsrchr(directory, L'\\');
    if (!separator) return 2;
    *separator = L'\0';
    SetCurrentDirectoryW(directory);

    LPCWSTR original = GetCommandLineW();
    if (*original == L'\"') {
        original++;
        while (*original && *original != L'\"') original++;
        if (*original) original++;
    } else {
        while (*original && *original != L' ') original++;
    }
    while (*original == L' ') original++;

    wchar_t command[65536];
    if (swprintf(command, 65536, L"\"%ls\\python\\pythonw.exe\" -m lvgl_mpy_studio %ls", directory, original) < 0) return 2;
    STARTUPINFOW startup = {0};
    startup.cb = sizeof(startup);
    PROCESS_INFORMATION process = {0};
    if (!CreateProcessW(NULL, command, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, directory, &startup, &process)) {
        wchar_t message[512];
        swprintf(message, 512, L"The bundled Python could not be started.\nWindows error: %lu", GetLastError());
        MessageBoxW(NULL, message, L"LVGL MPY Studio", MB_ICONERROR | MB_OK);
        return 1;
    }
    WaitForSingleObject(process.hProcess, INFINITE);
    DWORD result = 1;
    GetExitCodeProcess(process.hProcess, &result);
    CloseHandle(process.hThread);
    CloseHandle(process.hProcess);
    return (int)result;
}
