import socket, json, time, subprocess

class GateWay:
    def __init__(self,sdp_controller):
        self.sdp_controller=sdp_controller

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 7000))
        print("SPA Listener started.")

        while True:
            data, addr = sock.recvfrom(1024)
            try:
                payload=self.sdp_controller.spa_auth(data)
                if payload is None:
                    print(f"Rejected SPA packet from {addr[0]}")
                    continue
                else:
                    print(f"Authorized: {addr[0]}")
                    self.open_firewall(addr[0], payload["request_port"])
            except Exception as e:
                print("Invalid packet:", e)

    def open_firewall(self,ip, port):
        #windows 방화벽에서 포트로 들어오는 연결을 허용
        cmd = f'netsh advfirewall firewall add rule name="SPA Open SSH" dir=in action=allow protocol=TCP localport={port}'
        subprocess.call(cmd, shell=True)
        print(f"Opened port {port} for {ip}")
    
    def close_firewall(self, ip, port):
        # 방화벽에서 포트를 닫는 명령어
        cmd = f'netsh advfirewall firewall delete rule name="SPA Open Port {port}" protocol=TCP localport={port}'
        subprocess.call(cmd, shell=True)
        print(f"Closed port {port} for {ip}")

# if __name__=='__main__':
#     gateway=GateWay()
