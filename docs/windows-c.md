# Building the C target on Windows

MicroPython Debug needs no toolchain. The C target needs `gcc`, `ar` and `make` for Windows x86-64; the IDE finds them automatically in `PATH`, in MSYS2 or in the directory set by `LVGL_MPY_STUDIO_TOOLCHAIN`.

## MSYS2 MinGW64

1. Install MSYS2 from the official page: <https://www.msys2.org/>.
2. Open the **MSYS2 MINGW64** terminal and install the toolchain:

   ```sh
   pacman -S --needed mingw-w64-x86_64-toolchain
   ```

3. Add `C:\msys64\mingw64\bin` to the Windows `PATH`, or start the IDE from an environment where that directory is in `PATH`.

## w64devkit

1. Download w64devkit from the official project: <https://github.com/skeeto/w64devkit>.
2. Extract the archive and add its `bin` directory to `PATH`.
3. Alternatively, set `LVGL_MPY_STUDIO_TOOLCHAIN` to the w64devkit root directory.

From `cmd`, check:

```bat
gcc --version
ar --version
make --version
```

If the IDE cannot find one of these commands, the C build shows a message with these links. No toolchain is downloaded or installed automatically.
