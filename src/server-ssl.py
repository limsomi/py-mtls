#!/bin/usr/env python3
import socket
import ssl
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Server"

def tcp():
    ## SOCKET
    print("Running Server")
    print(f"HOST: {HOST}\nPORT: {PORT}\nSSL_VERSION: {ssl.PROTOCOL_TLS}\nCERT: {SERVER_PEM}\nKEY: {SERVER_KEY}\n")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, certfile=SERVER_PEM, keyfile=SERVER_KEY, ssl_version=ssl.PROTOCOL_TLS)

    try:
        data = secure_sock.read(1024)
        print(data)
        data = b'hello from server'
        secure_sock.write(data)
        print(data)
    finally:
        secure_sock.close()

def http():
    # HTTP
    app.run(host=HOST, port=PORT,ssl_context=(SERVER_PEM, SERVER_KEY))

if __name__ == '__main__':
    
    HOST = '127.0.0.1'
    PORT = 1234
    CLIENT_PEM = "./ssl/client/client.pem"
    SERVER_PEM = "./ssl/server/server.pem"
    SERVER_KEY = "./ssl/server/server.key"

    # HTTP
    # http()

    # TCP
    tcp()