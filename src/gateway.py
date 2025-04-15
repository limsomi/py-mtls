import socket, json, time, subprocess
import threading

class GateWay:
    def __init__(self,sdp_controller,start_port=10000,end_port=20000):
        self.sdp_controller=sdp_controller
        self.start_port = start_port
        self.end_port = end_port
        self.available_ports = list(range(start_port, end_port))  # 미리 포트 풀 생성
        self.server_list=[]

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 7000))
        print("SPA Listener started.")

        while True:
            data, addr = sock.recvfrom(1024)

            payload=self.sdp_controller.spa_auth(data)
            if payload is None:
                print(f"Rejected SPA packet from {addr[0]}")
            else:
                client_id=payload["client_id"]
                print(f"Received packet from {client_id} with target server: {payload['target_server']}")
                dynamic_port=self.available_ports.pop(0)
                print(f"Authorized: id={client_id}, port={dynamic_port}")
                server=self.server_list[payload['target_server']]
                server.bind_to_port(dynamic_port)
                self.open_firewall(addr[0], dynamic_port)
                server_thread = threading.Thread(target=server.accept_connections)
                server_thread.start()
                response=json.dumps({"assigned_port":dynamic_port}).encode()

                sock.sendto(response,addr)

            # try:
            #     payload=self.sdp_controller.spa_auth(data)
            #     if payload is None:
            #         print(f"Rejected SPA packet from {addr[0]}")
            #     else:
            #         client_id=payload["client_id"]
            #         print(f"Received packet from {client_id} with target server: {payload['target_server']}")
            #         dynamic_port=self.available_ports.pop(0)
            #         print(f"Authorized: id={client_id}, port={dynamic_port}")
            #         server=self.server_list[payload['target_server']]
            #         server.bind_to_port(dynamic_port)
            #         self.open_firewall(addr[0], dynamic_port)
            #         server_thread = threading.Thread(target=server.accept_connections)
            #         server_thread.start()
            #         response=json.dumps({"assigned_port":dynamic_port}).encode()

            #         sock.sendto(response,addr)
            # except Exception as e:
            #     print("Invalid packet:", e)

    def open_firewall(self,ip, port):
        #windows 방화벽에서 포트로 들어오는 연결을 허용
        cmd = f'netsh advfirewall firewall add rule name="SPA Open Port {port}" dir=in action=allow protocol=TCP localport={port}'


        subprocess.call(cmd, shell=True)
        print(f"Opened port {port} for {ip}")
    
    def close_firewall(self, ip, port):
        # 방화벽에서 포트를 닫는 명령어
        cmd = f'netsh advfirewall firewall delete rule name="SPA Open Port {port}" protocol=TCP localport={port}'
        subprocess.call(cmd, shell=True)
        print(f"Closed port {port} for {ip}")
    def put_server(self,server):
        self.server_list.append(server)
