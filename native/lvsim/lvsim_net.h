/* SPDX-License-Identifier: MIT */
/* Copyright (c) 2026 Nunzio Raciti */
#ifndef LVSIM_NET_H
#define LVSIM_NET_H

#include <stddef.h>
#include <stdint.h>

typedef intptr_t lvsim_socket_t;

#define LVSIM_INVALID_SOCKET ((lvsim_socket_t)-1)
#define LVSIM_NET_ERROR (-2)
#define LVSIM_NET_AGAIN (-1)

lvsim_socket_t lvsim_net_connect(const char *host, uint16_t port);
void lvsim_net_close(lvsim_socket_t socket);
int lvsim_net_send(lvsim_socket_t socket, const void *data, size_t size);
int lvsim_net_recv(lvsim_socket_t socket, void *data, size_t size);
int lvsim_net_wait(lvsim_socket_t socket, int timeout_ms);

#endif
