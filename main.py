import socket, threading, datetime, os # uses os instead of dotenv for using only built in libraries


ACCESS_HOST = os.getenv('HOST',"localhost")
BIND_HOST = "0.0.0.0"
PORT = int(os.getenv('PORT') or 8080) # TODO: 80 will require admin permissions in linux and that's a headace for another time... although it should be simple enough (added as todo)...
class WebServe:
    def __init__(self, htmlMsg,showTimestamp=False):
        self.showTimestamp = showTimestamp
        self.htmlMsg = htmlMsg
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allows the server to be restarted without waiting for the port to be released
        self.server.bind((BIND_HOST, PORT))
        self.server.listen(5)
        if ACCESS_HOST in ("localhost", "127.0.0.1") or ACCESS_HOST.startswith(("192.168.", "10.", "172.")):
            print(f"Server started on http://{ACCESS_HOST}:{PORT}")
        else:
            print(f"Server available at https://{ACCESS_HOST}")

    def handle_client(self, client_socket):   
        request = client_socket.recv(1024).decode() # receive request and cleares buffer... appearntly important.
        response_body = self.htmlMsg 
        if self.showTimestamp:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            response_body += f"<p>User requested from server at: {timestamp}</p>"
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_body}"
        client_socket.sendall(response.encode())
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
    server = WebServe(htmlMsg=f"<h1>Hello, World! (Kinda overused not gonna lie)</h1>",showTimestamp=True)
    server.run()
