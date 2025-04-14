import socket
import ssl
import pprint
import os
import random

class Client:
    def __init__(self,host,port,ca_cert_file,client_crt,client_key):
        self.host=host
        self.port=port
        self.ca_cert_file=ca_cert_file
        self.client_crt=client_crt
        self.client_key=client_key

    def run(self):
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(certfile=self.client_crt, keyfile=self.client_key)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=self.ca_cert_file)
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=self.host)

        try:

            print("Sent client certificate to server")

            # 이후 일반 데이터 송수신
            secure_sock.write(b'hello from client')
            response = secure_sock.recv(1024)
            print(f"Received: {response.decode()}")

        finally:
            secure_sock.close()

if __name__ == '__main__':

    CLIENT_PATH="./ssl/client"
    client_list=os.listdir(CLIENT_PATH)
    port_list=[1234,1235,1236]

    for client_name in client_list:
        HOST = '127.0.0.1'
        PORT =port_list[random.choice([0,1, 2])]

        CA_CERT_FILE = "ssl\RootCA\RootCA_with_ServerCA.pem"
        
        CLIENT_CRT = os.path.join(CLIENT_PATH,client_name,client_name+".crt")
        CLIENT_KEY =  os.path.join(CLIENT_PATH,client_name,client_name+".key")

        client=Client(HOST,PORT,CA_CERT_FILE,CLIENT_CRT,CLIENT_KEY)
        client.run()
        print('finish '+client_name)