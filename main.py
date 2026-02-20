import socket, threading, os, json
# read .env file and set in environ for os.
env_vars = {}
with open(".env", 'r') as file:
    for line in file:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" in line:
            key, value = line.split("=", 1)
            env_vars[key.strip().replace("'", '').replace('"', '')] = value.strip().replace("'", '').replace('"', '')

for env_key, env_value in env_vars.items():
    os.environ[env_key] = env_value


ACCESS_HOST = os.getenv('HOST', "localhost")
BIND_HOST = "0.0.0.0"
PORT = int(os.getenv('PORT') or 8080)
STATIC_DIR = "static"

class WebServe:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((BIND_HOST, PORT))
        self.server.listen(5)
        self.routes = {
            "/api/ping": self.handle_ping,
            "/api/info": self.handle_info,
        }
        print(f"Server started on http://{ACCESS_HOST}:{PORT}")

    def handle_ping(self, request_data):
        return {"message": "pong", "status": "success"}, 200

    def handle_info(self, request_data):
        return {"version": "1.1.0", "server": ACCESS_HOST}, 200
    
    def send_json_response(self, client_socket, data, status_code=200):
        content = json.dumps(data).encode()
        status_text = "OK" if status_code == 200 else "Error"
        header = (
            f"HTTP/1.1 {status_code} {status_text}\r\n"
            f"Content-Type: application/json\r\n"
            f"Content-Length: {len(content)}\r\n"
            f"Connection: close\r\n\r\n"
        )
        client_socket.sendall(header.encode() + content)

    def get_content_type(self, file_path): # instead of mimetypes import
        if file_path.endswith(".html"): return "text/html"
        if file_path.endswith(".css"): return "text/css"
        if file_path.endswith(".js"): return "application/javascript"
        if file_path.endswith(".png"): return "image/png"
        if file_path.endswith(".jpg") or file_path.endswith(".jpeg"): return "image/jpeg"
        return "text/plain"

    def handle_client(self, client_socket):
        try:
            request_data = b""
            while True:
                chunk = client_socket.recv(4096)
                request_data += chunk
                if b"\r\n\r\n" in request_data or not chunk:
                    break
            request = request_data.decode(errors='ignore')
            if not request:
                return
            # parse request
            request_line = request.split('\n')[0]
            path = request_line.split(' ')[1]
            if path.startswith("/api"):
                # Clean the path (remove query strings if they exist)
                clean_path = path.split('?')[0].rstrip('/')
                
                handler = self.routes.get(clean_path)
                if handler:
                    data, status = handler(request)
                    self.send_json_response(client_socket, data, status)
                else:
                    self.send_json_response(client_socket, {"error": "API endpoint doesn't exist"}, 404)
                return
            else:
                # map request to local file system
                requested_path = os.path.join(STATIC_DIR, path.lstrip("/")) # .lstrip("/") stops accessing root of the OS :)
                # made index.html the default page if path is a folder
                if os.path.isdir(requested_path):
                    requested_path = os.path.join(requested_path, "index.html")
                # if exists- serve.
                if os.path.exists(requested_path) and os.path.isfile(requested_path):
                    with open(requested_path, "rb") as f:
                        content = f.read()
                    
                    content_type = self.get_content_type(requested_path)
                    header = (
                        f"HTTP/1.1 200 OK\r\n"
                        f"Content-Type: {content_type}\r\n"
                        f"Content-Length: {len(content)}\r\n"
                        f"Connection: close\r\n\r\n"
                    )
                    client_socket.sendall(header.encode() + content)
                else:
                    # 404 res
                    msg = "<h1>404 Not Found</h1><p>The resource you requested does not exist.</p>".encode()
                    header = f"HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\nContent-Length: {len(msg)}\r\n\r\n"
                    client_socket.sendall(header.encode() + msg)
                    client_socket.shutdown(socket.SHUT_WR)
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            client_socket.close()

    def run(self):
        self.server.settimeout(1.0)
        try:
            while True:
                try:
                    client_socket, addr = self.server.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nServer terminated.")
        finally:
            self.server.close()

if __name__ == "__main__":
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
    
    server = WebServe()
    server.run()