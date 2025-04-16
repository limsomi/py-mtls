import socket
import subprocess
from sdp import SDP_Controll

class GateWay:
    def __init__(self, sdp_controller):
        self.sdp_controller = sdp_controller

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 1234))
        print("🔐 SPA Listener started.")

        # 시스템 라우팅 & 기본 정책 DROP
        # subprocess.call("sysctl -w net.ipv4.ip_forward=1", shell=True)
        subprocess.call("iptables -P FORWARD DROP", shell=True)
        subprocess.call("iptables -I INPUT -p udp --dport 1234 -j ACCEPT", shell=True)
        subprocess.call('iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE',shell=True)
        subprocess.call('iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT',shell=True)
        # subprocess.call('ip route add 192.168.20.0/24 dev eth1',shell=True)


        while True:
            data, addr = sock.recvfrom(2048)
            try:
                payload = self.sdp_controller.spa_auth(data, addr)
                if payload is None:
                    print(f"❌ Rejected SPA packet from {addr[0]}")
                    continue

                source_ip = addr[0]
                target_ip = payload["target_ip"]
                target_port = payload["request_port"]
                self.allow_forward(source_ip, target_ip, target_port)

            except Exception as e:
                print("❗ Invalid packet:", e)

    def allow_forward(self, source_ip, target_ip, port):
        cmd = f"iptables -I FORWARD -p tcp -d {target_ip} --dport {port} -s {source_ip} -j ACCEPT"
        subprocess.call(cmd, shell=True)
        print(f"✅ FORWARD {source_ip} → {target_ip}:{port} allowed")

if __name__ == '__main__':
    sdp = SDP_Controll()
    gateway = GateWay(sdp)
    gateway.listen()
