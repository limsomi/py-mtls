import socket
import ssl
import pprint
import os
import random

class Client:
    def __init__(self,ca_cert_file,client_crt,client_key):
        self.ca_cert_file=ca_cert_file
        self.client_crt=client_crt
        self.client_key=client_key

    def run(self,host_ip):
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0',0))
        sock.connect((host_ip, 1234))

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(certfile=self.client_crt, keyfile=self.client_key)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=self.ca_cert_file)
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=host_ip)

        try:

            print("Sent client certificate to server")

            # 이후 일반 데이터 송수신
            secure_sock.write(b'hello from client')
            response = secure_sock.recv(1024)
            print(f"Received: {response.decode()}")

        finally:
            secure_sock.close()

if __name__ == '__main__':
    client_name = os.environ.get("CLIENT_NAME")
    client_number = int(client_name.replace("client", ""))
    client_ip = f"192.168.100.{client_number}"

    host_ips = [f"192.168.100.{i}" for i in range(100, 103)]
    host_ip=random.choice(host_ips)
   
    ca_cert_file = "./ssl/RootCA/RootCA_with_ServerCA.pem"
    client_crt = f"./ssl/client/{client_name}/{client_name}.crt"
    client_key = f"./ssl/client/{client_name}/{client_name}.key"

    client = Client(ca_cert_file, client_crt, client_key)
    client.run(host_ip)
    print(f"✅ Finished client: {client_name}")