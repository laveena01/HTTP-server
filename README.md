
#  Build Your Own HTTP Server (Python)

This project is a minimal HTTP/1.1 server built from scratch using Python’s low-level `socket` module.
It progressively implements key web server features — parsing HTTP requests, handling different endpoints, serving files, supporting persistent (keep-alive) connections, and more.

---

##  What This Server Can Do

✔ Accept TCP connections on a port (default: `localhost:4221`)
✔ Parse HTTP/1.1 requests (`GET`, `POST`)
✔ Serve endpoints:

| Endpoint                                                                                 | Description                                     |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `/`                                                                                      | Returns `200 OK`                                |
| `/echo/<message>`                                                                        | Returns `<message>` as plain text               |
| `/user-agent`                                                                            | Returns the value of the `User-Agent` header    |
| `/files/<filename>`                                                                      | Reads / writes files from a specified directory |
| ✔ Respect `Content-Length` + request body for `POST`                                     |                                                 |
| ✔ Serve binary files using `application/octet-stream`                                    |                                                 |
| ✔ Keep TCP connections open for multiple HTTP requests (HTTP/1.1 persistent connections) |                                                 |

---

## 🚀 Running the Server

### **1. Prerequisites**

* Python 3.10 or above (3.13 recommended)

### **2. Run the server**

```bash
./your_program.sh --directory /tmp/
```

or:

```bash
python3 -m app.main --directory /tmp/
```

This tells the server to read/write files from `/tmp/`.

---

## 💻 Example Usage

### ➤ Root request

```bash
curl -v http://localhost:4221/
```

### ➤ Echo endpoint

```bash
curl -v http://localhost:4221/echo/banana
```

### ➤ Read file

```bash
echo -n "Hello, World!" > /tmp/foo
curl -v http://localhost:4221/files/foo
```

### ➤ Create file (POST)

```bash
curl -v -X POST http://localhost:4221/files/data --data "Sample123"
```

### ➤ Send two requests over same TCP connection

```bash
curl --http1.1 -v \
    http://localhost:4221/echo/kiwi \
    --next http://localhost:4221/user-agent -H "User-Agent: test-agent"
```

---

##  Project Structure

```
.
├── app/
│   └── main.py      # Core server logic
├── your_program.sh  # Startup script
├── Pipfile          # Dependencies (if using pipenv)
└── README.md
```

---

##  Key Concepts Implemented

* **Sockets & TCP** — No frameworks, only `socket` + `threading`
* **HTTP/1.1 parsing** — Request line, headers, body
* **Content-Length handling** — Safe reading of POST bodies
* **File I/O** — Binary-safe (`rb`/`wb`) for serving files
* **Persistent connections** — Keep-alive by default, close on `Connection: close`
* **Multithreading** — Handle multiple clients simultaneously
* **Gzip compression** - To compress requests 

---




