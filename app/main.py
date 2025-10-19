import socket  # noqa: F401
import threading
import os
import sys
import gzip
BASE_DIR = None
def get_():
    return  f"HTTP/1.1 200 OK\r\n\r\n".encode("utf-8")

def get_echo(parts,path):
    msg = path[len("/echo/"):]
    for line in parts:
        if line.lower().startswith("accept-encoding:"):
            encoders = line[len("accept-encoding: "):].split(",")
            encoders = [e.strip() for e in encoders]
            if "gzip" in encoders:
                compressed = gzip.compress(msg.encode("utf-8"))
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(compressed)}\r\n\r\n".encode("utf-8")+ compressed
            else:
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n".encode("utf-8")
    
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}".encode("utf-8")

def get_user_agent(parts):
    msg = parts[2][len('User-Agent:')+1:]
    return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(msg)}\r\n\r\n{msg}".encode("utf-8")

def get_files(path):
    filename = path[len("/files/"):].strip()
    filepath = os.path.join(BASE_DIR, filename)
    print(f"Looking for: {filepath}")
    if os.path.exists(filepath):
        with open(filepath,"rb") as f:
            content = f.read()
        return f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n".encode("utf-8")+ content
        # conn.sendall(response.encode("utf-8")+ content)
    else:
        return f"HTTP/1.1 404 Not Found\r\n\r\n".encode("utf-8")
def post(path, parts, req):
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
        return f"HTTP/1.1 201 Created\r\n\r\n".encode("utf-8")
def modify(response):
    header, sep, data = response.decode("utf-8").partition("\r\n\r\n")
    response = header + f"\r\nConnection: close" + sep + data
    return response.encode("utf-8")

def handle(conn, addr):
    with conn:
        while True:
            req = conn.recv(1024)
            if not req:
                break
            req = req.decode("utf-8")
            parts = req.split("\r\n")
            lines = parts[0].split()
            method = lines[0]
            path = lines[1]
            if(method == "GET"):
                if path=='/':
                    response = get_()
                elif path.startswith("/echo/"):
                    response = get_echo(parts, path)
                elif path.startswith("/user-agent"):
                    response = get_user_agent(parts)
                elif path.startswith("/files/"):
                    response = get_files(path)
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode("utf-8")    
            elif(method=="POST"):
                response = post(path, parts, req)
            
            flag = False
            for line in parts:
                if "connection: close" in line.lower():
                    flag = True
                    response = modify(response)
                    break
            
            conn.sendall(response)
            if flag:
                break







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
