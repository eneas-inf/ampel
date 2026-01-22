import socket

def start_webserver(port: int = 80):
    s = socket.socket()
    # Damit der Port nach einem Neustart sofort wieder frei ist:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    addr = ('0.0.0.0', port)
    s.bind(addr)
    s.listen(5)
    print("Listening on", addr)
    
    while True:
        conn = None
        try:
            conn, client_addr = s.accept()
            print("Client connected from", client_addr)
            
            req = conn.recv(1024)
            if not req:
                conn.close()
                continue
            
            # Fehlerfreies Decoding
            data = req.decode('utf-8', 'ignore')
            
            # Request-Analyse und Logging
            print("-" * 40)
            lines = data.split('\r\n')
            if len(lines) > 0:
                request_line = lines[0]
                print(f"Request: {request_line}")
                
                parts = request_line.split(' ')
                if len(parts) >= 2:
                    method = parts[0]
                    path = parts[1]
                    print(f"Method: {method}")
                    print(f"Path: {path}")
                    
                    # Button-Press-Erkennung
                    if method == 'POST':
                        if path == '/auto':
                            print(">>> LOG: AUTO button pressed (Request to /auto)")
                        elif path == '/fussgaenger':
                            print(">>> LOG: FUSSGAENGER button pressed (Request to /fussgaenger)")

            # Volle Request-Informationen loggen
            print("Full Request Data:")
            print(data)
            print("-" * 40)
            
            # HTML Antwort senden
            try:
                with open("site.html", "r", encoding="utf-8") as f:
                    content = f.read()
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + content
                conn.sendall(response.encode('utf-8'))
            except FileNotFoundError:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\nDatei nicht gefunden")
            
        except Exception as e:
            print("Fehler beim Verarbeiten:", e)
        finally:
            if conn:
                conn.close()
