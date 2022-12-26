#!/bin/usr/env python3

import socket
import ssl

HOST = '127.0.0.1'
PORT = 1234

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE)
    s.sendall(b"hello from client")

    new = s.recv(4096)
    if not new:
        s.close()
    print(new)