import socket
import ssl
import pprint
import threading
import time
import os
from .gateway import GateWay
from .sdp_controller import SDP_Controll

class Server:
    def __init__(self,host,ca_cert_file,server_pem,server_key):
        self.host=host
        self.ca_cert_file=ca_cert_file
        self.server_pem=server_pem
        self.server_key=server_key

    def handle_client_connection(self,client_socket, context):
        secure_sock = None
        try:
            #서버가 client한테 인증서를 보내는 부분
            # (context.load_cert_chain에서 설정한 인증서를 클라이언트한테 보냄)
            secure_sock = context.wrap_socket(client_socket, server_side=True)

            peername = secure_sock.getpeername()
            print(f"Connection from {peername}")

            # 클라이언트 인증서 확인
            cert = secure_sock.getpeercert()
            if cert:
                print("Client Certificate")
                # pprint.pprint(cert)
            else:
                print("Client did not provide a certificate.")

            # 클라이언트가 보낸 데이터 읽기
            data = secure_sock.recv(1024)
            print(f"Received: {data.decode()}")

            # 응답 전송
            response = b'Hello from server'
            secure_sock.sendall(response)
            print(f"Sent: {response.decode()}")

        except ssl.SSLError as e:
            print(f"SSL Error: {e}")
        except Exception as e:
            print(f"Error handling client connection: {e}")
        finally:
            if secure_sock:
                secure_sock.close()
    
    def start_listening(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.context.load_cert_chain(certfile=self.server_pem, keyfile=self.server_key)
        self.context.load_verify_locations(cafile=self.ca_cert_file)

        # 서버 소켓은 여전히 초기화 하지만, 기다리지는 않는다.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"Server ready, waiting for Gateway to open port ...")

    def accept_connections(self):
        try:
            self.server_socket.listen(10)
            print(f"Server listening on {self.host}")

            while True:
                client_socket, fromaddr = self.server_socket.accept()
                print(f"Connection accepted from {fromaddr}")

                client_thread = threading.Thread(target=self.handle_client_connection, args=(client_socket, self.context))
                client_thread.start()

        except Exception as e:
            print(f"Error handling client connections: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    def bind_to_port(self,port):
        """ Gateway가 인증을 통과한 후 서버가 포트를 바인딩하도록 하기 """
        print(f"server listening on {self.host} {port}")
        self.server_socket.bind((self.host, port))


if __name__ == '__main__':
    sdp_controller=SDP_Controll()
    gateway=GateWay(sdp_controller)

    gateway_thread=threading.Thread(target=gateway.listen)
    gateway_thread.daemon=True
    gateway_thread.start()

    SERVER_PATH="./ssl/server"
    server_list=os.listdir(SERVER_PATH)

    
    for i in range(len(server_list)):
        HOST='127.0.0.1'

        CA_CERT_FILE = "./ssl\RootCA\RootCA_with_ClientCA.pem"
        SERVER_PEM = os.path.join(SERVER_PATH,server_list[i],server_list[i]+".pem")
        SERVER_KEY = os.path.join(SERVER_PATH,server_list[i],server_list[i]+".key")
        server=Server(HOST,CA_CERT_FILE,SERVER_PEM,SERVER_KEY)
        gateway.put_server(server)
        server.start_listening()  # 서버 준비 완료, Gateway에서 포트 열기를 기다림
    while True:
        time.sleep(1)

