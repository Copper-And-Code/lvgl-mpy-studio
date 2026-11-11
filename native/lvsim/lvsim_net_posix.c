/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#define _POSIX_C_SOURCE 200809L
#include "lvsim_net.h"
#include "lvsim_time.h"

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <poll.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static int wait_events(lvsim_socket_t socket, short events, int timeout_ms) {
    struct pollfd descriptor = {(int)socket, events, 0};
    for (;;) {
        int result = poll(&descriptor, 1, timeout_ms);
        if (result < 0 && errno == EINTR) continue;
        return result;
    }
}

lvsim_socket_t lvsim_net_connect(const char *host, uint16_t port) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd < 0) return LVSIM_INVALID_SOCKET;
    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_port = htons(port);
    if (inet_pton(AF_INET, host, &address.sin_addr) != 1) {
        close(fd);
        return LVSIM_INVALID_SOCKET;
    }
    for (int attempt = 0; attempt < 100; attempt++) {
        if (connect(fd, (struct sockaddr *)&address, sizeof(address)) == 0) {
            int flags = fcntl(fd, F_GETFL, 0);
            int enabled = 1;
            if (flags < 0 || fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0) break;
            setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &enabled, sizeof(enabled));
            return (lvsim_socket_t)fd;
        }
        if (errno != ECONNREFUSED && errno != EINTR) break;
        lvsim_sleep_ms(20);
    }
    close(fd);
    return LVSIM_INVALID_SOCKET;
}

void lvsim_net_close(lvsim_socket_t socket) {
    if (socket != LVSIM_INVALID_SOCKET) close((int)socket);
}

int lvsim_net_send(lvsim_socket_t socket, const void *data, size_t size) {
    const uint8_t *bytes = data;
    while (size) {
        ssize_t written = send((int)socket, bytes, size, MSG_NOSIGNAL);
        if (written < 0) {
            if (errno == EINTR) continue;
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
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
        ssize_t count = recv((int)socket, data, size, 0);
        if (count >= 0) return (int)count;
        if (errno == EINTR) continue;
        if (errno == EAGAIN || errno == EWOULDBLOCK) return LVSIM_NET_AGAIN;
        return LVSIM_NET_ERROR;
    }
}

int lvsim_net_wait(lvsim_socket_t socket, int timeout_ms) {
    return wait_events(socket, POLLIN, timeout_ms);
}
