import socket
import ssl
import pprint

def handle_client_connection(client_socket, context):
    secure_sock = None

    try:
        # Wrap the client socket with SSL using the context
        secure_sock = context.wrap_socket(client_socket, server_side=True)

        # Print client information
        peername = secure_sock.getpeername()
        print(f"Connection from {peername}")

        # Print client certificate information if available
        cert = secure_sock.getpeercert()
        if cert:
            print("Client Certificate:")
            pprint.pprint(cert)
        else:
            print("Client did not provide a certificate.")

        # Verify client certificate (adjust this part according to your certificate details)
        # Example: Verify if the client certificate has an organization name 'Python CA'
        # if not cert or ('organizationName', 'Python CA') not in cert['subject'][2]:
        #     raise Exception("ERROR: Invalid client certificate")

        # Read data from client
        data = secure_sock.read(1024)
        print(f"Received: {data.decode()}")  # Decode bytes to string for readability
        response = b'hello from server'
        
        # Send response to client
        secure_sock.write(response)
        print(f"Sent: {response.decode()}")  # Decode bytes to string for readability
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error handling client connection: {e}")
    finally:
        if secure_sock:
            secure_sock.close()

if __name__ == '__main__':
    # Server details
    HOST = '127.0.0.1'
    PORT = 1234
    CA_CERT_FILE = "./ssl/CA.pem"
    CLIENT_PEM = "./ssl/client/client.pem"
    SERVER_PEM = "./ssl/server/server.pem"
    SERVER_KEY = "./ssl/server/server.key"

    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=SERVER_PEM, keyfile=SERVER_KEY)
    # context.load_verify_locations(CLIENT_PEM)

    # Load CA certificates to trust
    context.load_verify_locations(cafile=CA_CERT_FILE)

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print(f"Server listening on {HOST}:{PORT}")

    try:
        while True:
            # Accept client connection
            client_socket, fromaddr = server_socket.accept()
            print(f"Connection accepted from {fromaddr}")
            
            # Handle client connection in a separate function
            handle_client_connection(client_socket, context)
    except KeyboardInterrupt:
        print("Server manually stopped.")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        # Close the server socket
        server_socket.close()