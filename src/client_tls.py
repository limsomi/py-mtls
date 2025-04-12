import socket
import ssl
import pprint
import os
import random
def client_run(HOST,PORT,CA_CERT_FILE,CLIENT_CRT,CLIENT_KEY,CLIENT):
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain(certfile=CLIENT_CRT, keyfile=CLIENT_KEY)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile=CA_CERT_FILE)
    secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=HOST)

    try:

        print("Sent client certificate to server")

        # 이후 일반 데이터 송수신
        secure_sock.write(b'hello from client')
        response = secure_sock.recv(1024)
        print(f"Received: {response.decode()}")

    finally:
        secure_sock.close()

# Client
if __name__ == '__main__':

    CLIENT_PATH="./ssl/client"
    client_list=os.listdir(CLIENT_PATH)
    port_list=[1234,1235,1236]

    for client in client_list:
        HOST = '127.0.0.1'
        PORT =port_list[random.choice([0,1, 2])]

        CA_CERT_FILE = "ssl\RootCA\RootCA_with_ServerCA.pem"
        
        CLIENT_CRT = os.path.join(CLIENT_PATH,client,client+".crt")
        CLIENT_KEY =  os.path.join(CLIENT_PATH,client,client+".key")

        client_run(HOST,PORT,CA_CERT_FILE,CLIENT_CRT,CLIENT_KEY,client)
        print('finish '+client)