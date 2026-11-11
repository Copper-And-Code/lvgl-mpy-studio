# lvsim protocol 2

TCP stream transport on loopback only. The IDE listens on `127.0.0.1` and a port chosen by the system; the simulator gets address and port in `LVSIM_CONNECT` and a random 16-byte token, encoded as 32 hexadecimal characters, in `LVSIM_TOKEN`. The client uses `TCP_NODELAY`.

Every message is `[type:u8][length:u32][payload]`, all little-endian. The length excludes the 5-byte header. Largest size accepted: 64 MiB.

| Type | Value | Direction | Payload |
|---|---:|---|---|
| HELLO | 1 | simulator → IDE | `width:u16 height:u16 format:u8 version:u8 token:byte[16]`; format 1 = RGB565, version = 2 |
| RECT | 2 | simulator → IDE | `x:i16 y:i16 w:i16 h:i16 pixels:byte[]`; RGB565, 2 bytes per pixel, packed rows |
| PRESENT | 3 | simulator → IDE | empty |
| POINTER | 4 | IDE → simulator | `x:i16 y:i16 pressed:u8` |
| KEY | 5 | IDE → simulator | `code:u32 pressed:u8` |
| WHEEL | 6 | IDE → simulator | `delta:i16` |
| QUIT | 7 | IDE → simulator | empty |
| STOP | 8 | IDE → simulator | empty |

`HELLO` must be the first message and arrive within 2 seconds of the connection. The IDE closes the connection if the token does not match, if the message is not a valid `HELLO`, or if a second connection arrives during the session.

Reading from the socket does not block. `PRESENT` marks the end of a frame. `STOP` asks to interrupt the user code with `KeyboardInterrupt`, without closing the simulator. The IDE stops a session with `STOP`, then `QUIT` after 500 ms, and finally kills the process after 2 seconds. `QUIT` and closing the socket end the loop without errors, so the simulator does not outlive the IDE.
