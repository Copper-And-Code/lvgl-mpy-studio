/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#include "lvsim_net.h"
#include "lvsim_time.h"

#include <stdint.h>
#include <stdio.h>
#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
typedef SOCKET test_socket_t;
#define TEST_INVALID_SOCKET INVALID_SOCKET
#define TEST_CLOSE closesocket
#else
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
typedef int test_socket_t;
#define TEST_INVALID_SOCKET (-1)
#define TEST_CLOSE close
#endif

#define CHECK(condition) do { if (!(condition)) { fprintf(stderr, "check failed at line %d\n", __LINE__); return 1; } } while (0)

static test_socket_t open_server(uint16_t *port) {
    test_socket_t server = socket(AF_INET, SOCK_STREAM, 0);
    if (server == TEST_INVALID_SOCKET) return TEST_INVALID_SOCKET;
    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    address.sin_port = 0;
    if (bind(server, (struct sockaddr *)&address, sizeof(address)) != 0 || listen(server, 1) != 0) {
        TEST_CLOSE(server);
        return TEST_INVALID_SOCKET;
    }
#ifdef _WIN32
    int length = (int)sizeof(address);
#else
    socklen_t length = sizeof(address);
#endif
    if (getsockname(server, (struct sockaddr *)&address, &length) != 0) {
        TEST_CLOSE(server);
        return TEST_INVALID_SOCKET;
    }
    *port = ntohs(address.sin_port);
    return server;
}

int main(void) {
#ifdef _WIN32
    WSADATA data;
    CHECK(WSAStartup(MAKEWORD(2, 2), &data) == 0);
#endif
    uint16_t port;
    test_socket_t server = open_server(&port);
    CHECK(server != TEST_INVALID_SOCKET);
    lvsim_socket_t client = lvsim_net_connect("127.0.0.1", port);
    CHECK(client != LVSIM_INVALID_SOCKET);
    test_socket_t peer = accept(server, NULL, NULL);
    CHECK(peer != TEST_INVALID_SOCKET);

    CHECK(lvsim_net_send(client, "ping", 4) == 0);
    char buffer[4];
    CHECK(recv(peer, buffer, sizeof(buffer), 0) == 4);
    CHECK(memcmp(buffer, "ping", 4) == 0);
    CHECK(send(peer, "pong", 4, 0) == 4);
    CHECK(lvsim_net_wait(client, 1000) == 1);
    int received = 0;
    while (received < 4) {
        int count = lvsim_net_recv(client, buffer + received, sizeof(buffer) - (size_t)received);
        if (count == LVSIM_NET_AGAIN) {
            CHECK(lvsim_net_wait(client, 1000) == 1);
            continue;
        }
        CHECK(count > 0);
        received += count;
    }
    CHECK(memcmp(buffer, "pong", 4) == 0);

    lvsim_time_open();
    uint32_t started = lvsim_time_ms();
    lvsim_sleep_ms(2);
    uint32_t elapsed = lvsim_time_ms() - started;
    lvsim_time_close();
    CHECK(elapsed >= 1 && elapsed < 1000);

    lvsim_net_close(client);
    TEST_CLOSE(peer);
    TEST_CLOSE(server);
#ifdef _WIN32
    WSACleanup();
#endif
    puts("NET_OK");
    return 0;
}
