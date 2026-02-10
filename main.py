import socket, threading, datetime, os # uses os instead of dotenv for using only built in libraries


def get_private_ip():
    """
    Attempts to get the private IP address of the local machine.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('1.1.1.1', 80)) # Connect to a public IP address just to get the socket's ip addr - in this case, used cloudflares's dns server
            ip_address = s.getsockname()[0] # Get the socket's ip addr
        except socket.error:
            ip_address = '127.0.0.1'
    return ip_address

HOST = os.getenv('HOST') or get_private_ip()
PORT = int(os.getenv('PORT') or 8080) # TODO: 80 will require admin permissions in linux and that's a headace for another time... although it should be simple enough (added as todo)...
class WebServe:
    def __init__(self, htmlMsg):
        self.htmlMsg = htmlMsg
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(5)
        if any(HOST.startswith(p) for p in ("192.168.", "10.", "172.", "127.0.0.1")): # if it's localhost then http, else https and no need for port, coolify handles that.
            print(f"Server started on http://{HOST}:{PORT}")
        else:
            print(f"Server started on https://{HOST}")

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
    server = WebServe(htmlMsg=f"<h1>Hello, World! (Kinda overused not gonna lie)</h1> Timetamp of server launch: {datetime.datetime.now().strftime('%H:%M:%S')}")
    server.run()
