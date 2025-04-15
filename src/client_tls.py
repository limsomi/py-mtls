import socket,time,json
import ssl
import pprint
import os
import random
from utils.crypto_utils import *

class Client:
    def __init__(self,ca_cert_file,client_crt,client_key,id):
        self.id=id
        self.ca_cert_file=ca_cert_file
        self.client_crt=client_crt
        self.client_key=client_key

    def create_packet(self,server_id):
        payload = {
            "timestamp": int(time.time()),
            "target_server":server_id,
            "client_id": self.id,
        }
        raw = json.dumps(payload).encode()
        return encrypt(raw)

    # send_packet("127.0.0.1", 7000)  # 서버의 SPA 리스너 포트
    def send_packet(self,target_id, target_port,sock):
        packet = self.create_packet(target_id)
        sock.sendto(packet, ("127.0.0.1", target_port))
        print("SPA packet sent.")

    def run(self,target_id):
        #send spa packet
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 0)) 

        self.send_packet(target_id,7000,sock)
        time.sleep(1)
        data, _ = sock.recvfrom(1024)
        response = json.loads(data.decode())


        #mTLS connection
        sock_tls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tls.connect(('127.0.0.1', response['assigned_port']))

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(certfile=self.client_crt, keyfile=self.client_key)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=self.ca_cert_file)
        secure_sock = context.wrap_socket(sock_tls, server_side=False, server_hostname='127.0.0.1')

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
    port_list=[0,1,2]

    for client_name in client_list:
        target_id =random.choice([0,1, 2])

        CA_CERT_FILE = "ssl\RootCA\RootCA_with_ServerCA.pem"
        
        CLIENT_CRT = os.path.join(CLIENT_PATH,client_name,client_name+".crt")
        CLIENT_KEY =  os.path.join(CLIENT_PATH,client_name,client_name+".key")
        
        client=Client(CA_CERT_FILE,CLIENT_CRT,CLIENT_KEY,client_name)
        client.run(target_id)
        print('finish '+client_name)