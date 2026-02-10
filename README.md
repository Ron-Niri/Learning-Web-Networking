# Minimal Python Socket Server
_This readme is AI generated? no wayyyyyy, what are you talking about?_

A lightweight, zero-dependency HTTP web server built using *ONLY* Python's core libraries. This project serves static files (HTML, CSS, JS, Images) from a directory and is pre-configured for containerized deployment (a bit of an overkill, I know).

## 🚀 Features

* **Zero Dependencies**: Uses only Python built-in libraries—no `pip install` required.
* **Multi-threaded**: Handles multiple concurrent client connections using `threading` with daemon support for clean exits.
* **Static File Support**: Automatically maps and serves MIME types for HTML, CSS, JS, and common image formats.
* **Smart Directory Routing**: Automatically resolves directory requests to `index.html` (e.g., `/blog/` serves `/blog/index.html`).
* **Docker Ready**: Optimized with a `python:3.11-slim` image, perfect for deployment on Coolify, Railway, or VPS.

---

## 📂 Project Structure

```text
.
├── main.py               # The Python web server logic
├── Dockerfile            # Container configuration
└── static/               # Website assets (Auto-created on first run)
    ├── index.html        # Home page
    ├── css/              # CSS files
    ├── css/main.css      # Stylesheets
    ├── js/               # JavaScript files
    ├── js/main.js        # Frontend logic
    └── assets/           # Image files
    └── assets/image.png  # Image file
    └── anotherPage/      # Another page
        └── anotherPage/index.html # Another page's html file
```

## 🛠️ Local Development

To run this server locally, you don't need to install anything. Just execute the Python script:

```bash
python main.py
```

## 🐳 Docker Deployment

This project is ready to be containerized. You can build and run it locally using Docker:

```bash
# Build the image
docker build -t python-basic-web-server .

# Run the container
docker run -p 8080:8080 python-basic-web-server
```

To deploy this to Coolify, simply import the repository. Coolify will automatically detect the `Dockerfile` and build the image for you.

## 🎯 Deployment

### Coolify
1. Import the repository to Coolify.
2. Set the **Build Type** to **Dockerfile**.
3. Set the **HOST** in .env to the domain name.
4. Set the **Port** to **8080**.
5. Click **Deploy**.
