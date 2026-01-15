import socket
import network
import time

def connect_wifi(ssid:str, password:str, max_wait:int = 100):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    status = wlan.ifconfig()
    return status[0]

def start_webserver(port: int = 80):
    s = socket.socket()
    addr = ('0.0.0.0', port)
    s.bind(addr)
    s.listen(5)
    print("Listening on", addr)
    def generate_page():
        html = """<html>
        <head>
        <title>Pico Ampel</title>
        </head>
        <body>
        <h1>Pico Ampel Control</h1>
        <p>
        <a href="/auto"><button class="btn">AUTO KOMMT</button></a>
        <a href="/fussgänger"><button class="btn">fussgänger</button></a>
        </p>
        </body>
        </html>"""
        return html
    while True:
        conn, client_addr = s.accept()
        print("Client connected from", client_addr)
        request = conn.recv(1024).decode()
        print("Request:", request)
        # Process the request to update LED status
        if "GET /auto" in request:
            print ("AUTO button pressed")
        elif "GET /fussgänger" in request:
            print ("fussgänger button pressed")
        # Always serve the main page with the updated status message
        response_body = generate_page()
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response_body
        conn.send(response.encode())
        conn.close()
