import socket, threading, datetime


def get_private_ip():
    """
    Attempts to get the private IP address of the local machine.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(0.0) # Set timeout to not blocking
        try:
            s.connect(('1.1.1.1', 80)) # Connect to a public IP address just to get the socket's ip addr - in this case, used cloudflares's dns server
            ip_address = s.getsockname()[0] # Get the socket's ip addr
        except socket.error:
            ip_address = '127.0.0.1'
    return ip_address

HOST = get_private_ip()
PORT = 8080
class WebServe:
    def __init__(self, htmlMsg):
        self.htmlMsg = htmlMsg
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        print(f"Server started on http://{HOST}:{PORT}")

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode()
        print(request)
        client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{self.htmlMsg}".encode())
        client_socket.close()

    def run(self):
        self.server.settimeout(1.0)
        print("Press CTRL+C to terminate server.")
        try:
            while True:
                try:
                    client_socket, addr = self.server.accept()
                    print(f"Accepted connection from {addr}")
                    client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                    client_handler.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("Server terminated.")
        finally:
            self.server.close()
            print("Server socket closed.")

if __name__ == "__main__":
    server = WebServe(htmlMsg=f"<h1>Hello, World!<h1> Timetamp: {datetime.datetime.now().strftime('%H:%M:%S')}")
    server.run()
