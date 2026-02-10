const breakdown = [
    {
        title: "1. Imports & Environment Config",
        code: "import socket, threading, os</br></br>ACCESS_HOST = os.getenv('HOST', 'localhost')</br>BIND_HOST = '0.0.0.0'</br>PORT = int(os.getenv('PORT') or 8080)</br>STATIC_DIR = 'static'",
        desc: "We import <b>socket</b> for networking and <b>os</b> to handle file paths and environment variables. Setting <b>BIND_HOST</b> to '0.0.0.0' allows the server to accept connections from any IP address on the local network."
    },
    {
        title: "2. Initializing the Server",
        code: "class WebServe:</br>    def __init__(self):</br>        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)</br>        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)</br>        self.server.bind((BIND_HOST, PORT))</br>        self.server.listen(5)",
        desc: "The constructor sets up the <b>TCP socket</b>. We use <b>SO_REUSEADDR</b> so you can restart the server instantly without waiting for the OS to timeout the previous port usage."
    },
    {
        title: "3. MIME Type Mapping",
        code: "def get_content_type(self, file_path):</br>    if file_path.endswith('.html'): return 'text/html'</br>    if file_path.endswith('.css'): return 'text/css'</br>    if file_path.endswith('.js'): return 'application/javascript'</br>    if file_path.endswith('.png'): return 'image/png'</br>    return 'text/plain'",
        desc: "Browsers need to know what kind of data they are receiving. This function checks the file extension to set the <b>Content-Type</b> header correctly."
    },
    {
        title: "4. Request Parsing & Security",
        code: "path = request_line.split(' ')[1]</br>requested_path = os.path.join(STATIC_DIR, path.lstrip('/'))</br>if os.path.isdir(requested_path):</br>    requested_path = os.path.join(requested_path, 'index.html')",
        desc: "We extract the URL from the HTTP request. We use <b>lstrip('/')</b> to prevent hackers from using '../' to view system files, and we default to <b>index.html</b> if a folder is requested."
    },
    {
        title: "5. File Handling & HTTP Response",
        code: "if os.path.exists(requested_path) and os.path.isfile(requested_path):</br>    with open(requested_path, 'rb') as f:</br>        content = f.read()</br>    header = f'HTTP/1.1 200 OK\\r\</br>Content-Type: {content_type}\\r\</br>...'</br>    client_socket.sendall(header.encode() + content)",
        desc: "If the file exists, we read it in <b>binary mode ('rb')</b> and wrap it in a valid HTTP/1.1 response. If it doesn't exist, the code sends back a <b>404 Not Found</b> HTML message."
    },
    {
        title: "6. The Multi-threaded Loop",
        code: "while True:</br>    client_socket, addr = self.server.accept()</br>    threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()",
        desc: "The server runs forever. Each time a user connects, it spawns a <b>daemon thread</b>. This prevents the server from freezing for other users while one person is loading a large file."
    },
    {
        title: "7. Main Execution Guard",
        code: "if __name__ == '__main__':</br>    if not os.path.exists(STATIC_DIR):</br>        os.makedirs(STATIC_DIR)</br>    server = WebServe()</br>    server.run()",
        desc: "This ensures that the <b>static</b> directory exists before the server starts. It creates the folder if it's missing, then kicks off the server instance."
    }
];

const container = document.getElementById('explainer-container');

breakdown.forEach(item => {
    const section = document.createElement('div');
    section.className = 'code-section';
    section.innerHTML = `
        <h3>${item.title}</h3>
        <code>${item.code}</code>
        <p class="explanation">${item.desc}</p>
    `;
    container.appendChild(section);
});