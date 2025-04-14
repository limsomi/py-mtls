import socket, json, time, subprocess
from crypto_utils import decrypt

class GateWay:
    def __init__(self):
        self.listen()

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 7000))
        print("SPA Listener started.")

        while True:
            data, addr = sock.recvfrom(1024)
            try:
                decrypted = decrypt(data)
                payload = json.loads(decrypted.decode())

                if abs(time.time() - payload["timestamp"]) > 30:
                    print("Rejected: Expired packet")
                    continue
                
                print(f"Authorized: {addr[0]}")
                self.open_firewall(addr[0], payload["request_port"])

            except Exception as e:
                print("Invalid packet:", e)

    def open_firewall(self,ip, port):
        cmd = 'netsh advfirewall firewall add rule name="SPA Open SSH" dir=in action=allow protocol=TCP localport=22'
        subprocess.call(cmd, shell=True)
        print(f"Opened port {port} for {ip}")

if __name__=='__main__':
    gateway=GateWay()
