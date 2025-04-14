import socket, time, json
from crypto_utils import encrypt

def create_packet():
    payload = {
        "timestamp": int(time.time()),
        "client_id": "client123",
        "request_port": 22
    }
    raw = json.dumps(payload).encode()
    return encrypt(raw)

def send_packet(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = create_packet()
    sock.sendto(packet, (target_ip, target_port))
    print("SPA packet sent.")

send_packet("127.0.0.1", 7000)  # 서버의 SPA 리스너 포트
