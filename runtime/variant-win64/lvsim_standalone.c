#ifdef LVSIM_STANDALONE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef _WIN32
#include <unistd.h>
#endif

#ifdef _WIN32
#include <io.h>
#include <wchar.h>
#include <windows.h>
#endif

#undef main
int micropython_main(int argc, char **argv);

static void lvsim_set_env(const char *name, const char *value) {
    #ifdef _WIN32
    _putenv_s(name, value == NULL ? "" : value);
    #else
    if (value == NULL) {
        unsetenv(name);
    } else {
        setenv(name, value, 1);
    }
    #endif
}

static void lvsim_redirect_log(void) {
    #ifdef _WIN32
    wchar_t path[32768];
    DWORD length = GetModuleFileNameW(NULL, path, sizeof(path) / sizeof(path[0]));
    if (length == 0 || length >= sizeof(path) / sizeof(path[0])) {
        return;
    }
    wchar_t *separator = wcsrchr(path, L'\\');
    if (separator != NULL) {
        *separator = L'\0';
        SetCurrentDirectoryW(path);
        *separator = L'\\';
    }
    wchar_t *extension = wcsrchr(path, L'.');
    if (extension == NULL) {
        return;
    }
    wcscpy(extension, L".log");
    if (_wfreopen(path, L"w", stdout) != NULL) {
        _dup2(_fileno(stdout), _fileno(stderr));
        setvbuf(stdout, NULL, _IOLBF, 0);
    }
    #endif
}

int main(int argc, char **argv) {
    static const char *variables[] = {
        "LVSIM_SOCKET", "LVSIM_CONNECT", "LVSIM_TOKEN", "LVSIM_HEADLESS",
        "LVSIM_DUMP", "LVSIM_FRAMES", "LVSIM_TICK_MS",
    };
    lvsim_redirect_log();
    for (size_t i = 0; i < sizeof(variables) / sizeof(variables[0]); ++i) {
        lvsim_set_env(variables[i], NULL);
    }
    #ifdef LVSIM_ONEFILE
    // The game is appended to this file: start-up must find it even if the program was
    // launched from PATH, so it gets the real path in LVSIM_SELF. The current folder
    // must not be able to replace anything.
    static char self[4096];
    #ifdef _WIN32
    DWORD length = GetModuleFileNameA(NULL, self, sizeof(self));
    if (length > 0 && length < sizeof(self)) {
        argv[0] = self;
        lvsim_set_env("LVSIM_SELF", self);
    }
    #else
    ssize_t length = readlink("/proc/self/exe", self, sizeof(self) - 1);
    if (length > 0) {
        self[length] = '\0';
        argv[0] = self;
        lvsim_set_env("LVSIM_SELF", self);
    }
    #endif
    lvsim_set_env("MICROPYPATH", ".frozen");
    #define LVSIM_ENTRY "import sys\nsys.path[:] = ['.frozen']\nimport lms_boot"
    if (argc == 2 && strcmp(argv[1], "--licenses") == 0) {
        char *arguments[] = {argv[0], "-c", "import sys\nsys.path[:] = ['.frozen']\nimport lms_licenses"};
        return micropython_main(3, arguments);
    }
    #else
    #define LVSIM_ENTRY "import main; main.main()"
    lvsim_set_env("MICROPYPATH", ".");
    #endif
    if (argc == 2 && strcmp(argv[1], "--selftest") == 0) {
        lvsim_set_env("LVSIM_HEADLESS", "1");
        lvsim_set_env("LVSIM_FRAMES", "1");
        lvsim_set_env("LVSIM_DUMP", "selftest.raw");
        argc = 1;
    }
    if (argc == 1) {
        char *arguments[] = {argv[0], "-c", LVSIM_ENTRY};
        return micropython_main(3, arguments);
    }
    return micropython_main(argc, argv);
}
#endif
