import socket
import ssl
import time
import os
import random
import json
from utils.crypto_utils import encrypt
import subprocess

class Client:
    def __init__(self, id, ca_cert_file, client_crt, client_key):
        self.id = id
        self.ca_cert_file = ca_cert_file
        self.client_crt = client_crt
        self.client_key = client_key

    def create_packet(self, target_ip, target_port):
        payload = {
            "timestamp": int(time.time()),
            "target_ip": target_ip,
            "client_id": self.id,
            "request_port": target_port
        }
        raw = json.dumps(payload).encode()
        return encrypt(raw)

    def send_spa_packet(self, gateway_ip, gateway_port, target_ip, target_port):
        packet = self.create_packet(target_ip, target_port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(packet, (gateway_ip, gateway_port))
        print(f"📨 Sent SPA packet to Gateway ({gateway_ip}) for {target_ip}:{target_port}")
        sock.close()

    def connect_tls(self, target_ip, target_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', 0))
        sock.settimeout(5)
        try:
            sock.connect((target_ip, target_port))
        except socket.timeout:
            print(f"⏱️ Connection to {target_ip}:{target_port} timed out (SPA not accepted?)")


        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(certfile=self.client_crt, keyfile=self.client_key)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=self.ca_cert_file)
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=target_ip)

        try:
            print("🔐 Sent client certificate to server")
            secure_sock.write(f"hello from {self.id}".encode())
            response = secure_sock.recv(1024)
            print(f"📥 Received: {response.decode()}")
        finally:
            secure_sock.close()

if __name__ == '__main__':
    client_name = os.environ.get("CLIENT_NAME")
    client_number = int(client_name.replace("client", ""))
    client_ip = f"192.168.10.{client_number}"  # 수정한 대역 예시

    target_ips = [f"192.168.20.{i}" for i in range(100, 103)]
    target_ip = random.choice(target_ips)
    target_port = 1234

    gateway_ip = '192.168.10.200'  # client_net에서 보이는 gateway IP
    gateway_port = 1234

    ca_cert_file = "./ssl/RootCA/RootCA_with_ServerCA.pem"
    client_crt = f"./ssl/client/{client_name}/{client_name}.crt"
    client_key = f"./ssl/client/{client_name}/{client_name}.key"

    client = Client(client_name, ca_cert_file, client_crt, client_key)
    subprocess.call("ip route add 192.168.20.0/24 via 192.168.10.200", shell=True)
    # 1. SPA 전송 (gateway는 client_net에서 접근 가능)
    client.send_spa_packet(gateway_ip, gateway_port, target_ip, target_port)

    # 2. SPA 성공 시 TLS 직접 연결 (서버는 다른 네트워크)
    time.sleep(1)  # rule 반영 기다림
    client.connect_tls(target_ip, target_port)
    print(f"✅ Finished client: {client_name}")
