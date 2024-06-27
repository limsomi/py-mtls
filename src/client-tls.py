import socket
import ssl
import pprint

# Client
if __name__ == '__main__':

    # Server details
    HOST = '127.0.0.1'
    PORT = 1234
    CA_CERT_FILE = "./ssl/CA.pem"
    CLIENT_CRT = "./ssl/client/client.crt"
    CLIENT_KEY = "./ssl/client/client.key"
    SERVER_PEM = "./ssl/server/server.pem"

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1)
    sock.connect((HOST, PORT))

    # Create an SSL context for the client
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    # context.load_verify_locations(SERVER_PEM)
    context.load_cert_chain(certfile=CLIENT_CRT, keyfile=CLIENT_KEY)

    # Load CA certificates to trust
    context.load_verify_locations(cafile=CA_CERT_FILE)

    # Wrap the socket with SSL context
    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock, server_side=False)

    # Get and print server certificate
    cert = secure_sock.getpeercert()
    if cert:
        print("Server Certificate:")
        pprint.pprint(cert)
    else:
        print("Server did not provide a certificate.")

    # Verify server certificate (commented out for now)
    # if not cert or ('organizationName', 'Python CA') not in cert['subject'][2]:
    #     raise Exception("ERROR: Invalid server certificate")

    # Send data to server
    secure_sock.write(b'hello from client')
    
    # Read response from server
    print(secure_sock.read(1024))

    # Close the secure socket and the underlying socket
    secure_sock.close()
    sock.close()