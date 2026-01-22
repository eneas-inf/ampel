import socket

def start_webserver(port: int = 80):
    s = socket.socket()
    addr = ('0.0.0.0', port)
    s.bind(addr)
    s.listen(5)
    print("Listening on", addr)
    while True:
        conn, client_addr = s.accept()
        print("Client connected from", client_addr)
        data = conn.recv(1024)
        if not data:
            conn.close()
            continue
        request = data.decode("utf-8", "ignore")
        print("Request:", request)
        # Process the request to update LED status
        if "GET /auto" in request:
            print ("AUTO button pressed")
        elif "GET /fussgaenger" in request:
            print ("fussgaenger button pressed")
        # Always serve the main page with the updated status message
        with open("site.html", "r") as f:
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + f.read()
            conn.send(response.encode())
            conn.close()