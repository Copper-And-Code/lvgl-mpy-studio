/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#include "lvsim_net.h"
#include "lvsim_time.h"

#include <winsock2.h>
#include <ws2tcpip.h>
#include <string.h>

static int started;

static int wait_events(lvsim_socket_t socket, short events, int timeout_ms) {
    WSAPOLLFD descriptor = {(SOCKET)socket, events, 0};
    for (;;) {
        int result = WSAPoll(&descriptor, 1, timeout_ms);
        if (result == SOCKET_ERROR && WSAGetLastError() == WSAEINTR) continue;
        return result;
    }
}

lvsim_socket_t lvsim_net_connect(const char *host, uint16_t port) {
    WSADATA data;
    if (!started && WSAStartup(MAKEWORD(2, 2), &data) != 0) return LVSIM_INVALID_SOCKET;
    started = 1;
    SOCKET fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd == INVALID_SOCKET) {
        WSACleanup();
        started = 0;
        return LVSIM_INVALID_SOCKET;
    }
    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_port = htons(port);
    address.sin_addr.s_addr = inet_addr(host);
    if (address.sin_addr.s_addr == INADDR_NONE) {
        closesocket(fd);
        WSACleanup();
        started = 0;
        return LVSIM_INVALID_SOCKET;
    }
    for (int attempt = 0; attempt < 100; attempt++) {
        if (connect(fd, (struct sockaddr *)&address, sizeof(address)) == 0) {
            u_long enabled = 1;
            if (ioctlsocket(fd, FIONBIO, &enabled) == SOCKET_ERROR) break;
            setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, (const char *)&enabled, sizeof(enabled));
            return (lvsim_socket_t)fd;
        }
        int error = WSAGetLastError();
        if (error != WSAECONNREFUSED && error != WSAEINTR) break;
        lvsim_sleep_ms(20);
    }
    closesocket(fd);
    WSACleanup();
    started = 0;
    return LVSIM_INVALID_SOCKET;
}

void lvsim_net_close(lvsim_socket_t socket) {
    if (socket != LVSIM_INVALID_SOCKET) closesocket((SOCKET)socket);
    if (started) {
        WSACleanup();
        started = 0;
    }
}

int lvsim_net_send(lvsim_socket_t socket, const void *data, size_t size) {
    const uint8_t *bytes = data;
    while (size) {
        int written = send((SOCKET)socket, (const char *)bytes, (int)size, 0);
        if (written == SOCKET_ERROR) {
            int error = WSAGetLastError();
            if (error == WSAEINTR) continue;
            if (error == WSAEWOULDBLOCK) {
                if (wait_events(socket, POLLOUT, 100) >= 0) continue;
            }
            return LVSIM_NET_ERROR;
        }
        bytes += written;
        size -= (size_t)written;
    }
    return 0;
}

int lvsim_net_recv(lvsim_socket_t socket, void *data, size_t size) {
    for (;;) {
        int count = recv((SOCKET)socket, (char *)data, (int)size, 0);
        if (count >= 0) return count;
        int error = WSAGetLastError();
        if (error == WSAEINTR) continue;
        if (error == WSAEWOULDBLOCK) return LVSIM_NET_AGAIN;
        return LVSIM_NET_ERROR;
    }
}

int lvsim_net_wait(lvsim_socket_t socket, int timeout_ms) {
    return wait_events(socket, POLLIN, timeout_ms);
}
