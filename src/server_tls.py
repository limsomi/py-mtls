import socket
import ssl
import pprint
import threading
import random
import os
from .gateway import GateWay
from .sdp_controller import SDP_Controll

class Server:
    def __init__(self,host,port,ca_cert_file,server_pem,server_key):
        self.host=host
        self.port=port
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

    def run(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.verify_mode = ssl.CERT_REQUIRED #클라이언트도 자신의 인증서를 보내야함
        context.load_cert_chain(certfile=self.server_pem, keyfile=self.server_key)
        context.load_verify_locations(cafile=CA_CERT_FILE)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host,self.port))
        server_socket.listen(10)  # 최대 10개의 연결을 대기

        print(f"Server listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, fromaddr = server_socket.accept()
                print(f"Connection accepted from {fromaddr}")
                
                # 스레드 생성하여 클라이언트 처리
                client_thread = threading.Thread(target=self.handle_client_connection, args=(client_socket, context))
                client_thread.start()

        except KeyboardInterrupt:
            print("Server manually stopped.")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_socket.close()


if __name__ == '__main__':
    sdp_controller=SDP_Controll()
    gateway=GateWay(sdp_controller)

    gateway_thread=threading.Thread(target=gateway.listen)
    gateway_thread.daemon=True
    gateway_thread.start()

    SERVER_PATH="./ssl/server"
    server_list=os.listdir(SERVER_PATH)
    port_list=[1234,1235,1236]
    
    for i in range(len(server_list)):
        HOST='127.0.0.1'
        PORT=port_list[i]
        CA_CERT_FILE = "./ssl\RootCA\RootCA_with_ClientCA.pem"
        SERVER_PEM = os.path.join(SERVER_PATH,server_list[i],server_list[i]+".pem")
        SERVER_KEY = os.path.join(SERVER_PATH,server_list[i],server_list[i]+".key")
        server=Server(HOST,PORT,CA_CERT_FILE,SERVER_PEM,SERVER_KEY)
        server_thread = threading.Thread(target=server.run)
        server_thread.start()

