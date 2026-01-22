import socket
import select

def init_webserver(port: int = 80):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    addr = ('0.0.0.0', port)
    s.bind(addr)
    s.listen(5)
    s.setblocking(False)  # Non-blocking mode
    print("Listening on", addr)
    return s

def process_request(s):
    try:
        # Check if there is a connection waiting
        readable, _, _ = select.select([s], [], [], 0)
        if not readable:
            return None

        conn, client_addr = s.accept()
        # print("Client connected from", client_addr)
        conn.settimeout(3.0) # Increased timeout for receiving data
        
        try:
            req = conn.recv(1024)
            if not req:
                conn.close()
                return None
            
            data = req.decode('utf-8', 'ignore')
            
            # Simple parsing
            action = None
            if "POST /auto" in data:
                action = "auto"
                print(">>> LOG: AUTO button pressed")
            elif "POST /fussgaenger" in data:
                action = "fussgaenger"
                print(">>> LOG: FUSSGAENGER button pressed")
            
            # Send Response
            try:
                with open("site.html", "r", encoding="utf-8") as f:
                    content = f.read()
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + content
                conn.sendall(response.encode('utf-8'))
            except Exception as e:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\nFile not found")
                
        except OSError as e:
            if e.args[0] == 110: # ETIMEDOUT
                # print("Connection timed out")
                pass
            else:
                print("Socket error during request:", e)
        except Exception as e:
            print("Error processing request:", e)
        finally:
            conn.close()
            
        return action
        
    except Exception as e:
        # print("Socket error:", e)
        return None
