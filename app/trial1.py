import socket  # noqa: F401
import threading
import os
import sys
BASE_DIR = None
def handle(conn, addr):
    with conn:
        req = conn.recv(1024).decode("utf-8")
        parts = req.split("\r\n")
        lines = parts[0].split()
        method = lines[0]
        path = lines[1]
        if(method == "GET"):
            if path=='/':
                response = "HTTP/1.1 200 OK\r\n\r\n"
            elif path.startswith("/echo/"):
                for line in parts:
                    if line.lower().startswith("accept-encoding:"):
                        encoder = line[len("accept-encoding: "):]
                        if(encoder.lower() != "invalid-encoding"):
                            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: {encoder}\r\n\r\n"
                        else:
                            response = f""
                msg = path[len("/echo/"):]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}"
            elif path.startswith("/user-agent"):
                msg = parts[2][len('User-Agent:')+1:]
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}"
            elif path.startswith("/files/"):
                filename = path[len("/files/"):].strip()
                filepath = os.path.join(BASE_DIR, filename)
                print(f"Looking for: {filepath}")
                if os.path.exists(filepath):
                    with open(filepath,"rb") as f:
                        content = f.read()
                    response =f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n"
                    conn.sendall(response.encode("utf-8")+ content)
                    return
                else:
                    response = f"HTTP/1.1 404 Not Found\r\n\r\n"

            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.send(response.encode("utf-8"))
        elif(method=="POST"):
            if path.startswith("/files/"):
                filename = path[len("/files/"):].strip()
                filepath = os.path.join(BASE_DIR, filename)
                length =0
                for line in parts:
                    if line.lower().startswith("content-length"):
                        length = (int)(line[16:17])
                        break
                msg = req.split("\r\n\r\n")[1]
                msg_bytes = msg.encode("utf-8")
                with open(filepath, "wb") as f:
                    f.write(msg_bytes)
                conn.send(b"HTTP/1.1 201 Created\r\n\r\n")




def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    global BASE_DIR
    # print(sys.argv)
    if  len(sys.argv) >=3 and sys.argv[1]=="--directory":
        BASE_DIR = sys.argv[2]

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while(True):
        conn , addr = server_socket.accept() # wait for client
        threading.Thread(target= handle, args=(conn, addr),daemon=True).start()
        

    

if __name__ == "__main__":
    main()
