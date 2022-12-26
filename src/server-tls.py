#!/bin/usr/env python3
import socket
import ssl
import pprint

#server
if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 1234
    CLIENT_PEM = "./ssl/client/client.pem"
    SERVER_PEM = "./ssl/server/server.pem"
    SERVER_KEY = "./ssl/server/server.key"


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, ca_certs=CLIENT_PEM, certfile=SERVER_PEM, keyfile=SERVER_KEY, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2)

    print(repr(secure_sock.getpeername()))
    print(secure_sock.cipher())
    print(pprint.pformat(secure_sock.getpeercert()))
    cert = secure_sock.getpeercert()
    print(cert)

    # verify client
    if not cert or ('organizationName', 'Python CA') not in cert['subject'][2]: raise Exception("ERROR")

    try:
        data = secure_sock.read(1024)
        print(data)
        data = b'hello from server'
        secure_sock.write(data)
        print(data)
    finally:
        secure_sock.close()
