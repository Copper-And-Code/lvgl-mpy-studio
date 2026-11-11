LVSIM_DIR := $(USERMOD_DIR)
LVSIM_TARGET := $(shell $(CC) -dumpmachine)
SRC_USERMOD_C += $(LVSIM_DIR)/modlvsim.c
SRC_USERMOD_LIB_C += $(LVSIM_DIR)/lvsim_io.c
CFLAGS_USERMOD += -I$(LVSIM_DIR)
ifneq (,$(findstring mingw32,$(LVSIM_TARGET)))
SRC_USERMOD_LIB_C += $(LVSIM_DIR)/lvsim_net_win32.c $(LVSIM_DIR)/lvsim_time_win32.c
CFLAGS_USERMOD += $(SDL2_CFLAGS)
LDFLAGS_USERMOD += $(SDL2_LIBS) -lws2_32 -lwinmm
else
SRC_USERMOD_LIB_C += $(LVSIM_DIR)/lvsim_net_posix.c $(LVSIM_DIR)/lvsim_time_posix.c
SDL2_CFLAGS ?= $(shell pkg-config --cflags sdl2)
SDL2_LIBS ?= $(shell pkg-config --libs sdl2)
CFLAGS_USERMOD += $(SDL2_CFLAGS)
LDFLAGS_USERMOD += $(SDL2_LIBS)
# Single-file executable: starts without arguments, see runtime/variant-win64/lvsim_standalone.c
ifneq ($(LVSIM_STANDALONE),)
SRC_USERMOD_LIB_C += $(LVSIM_STANDALONE)
endif
endif
