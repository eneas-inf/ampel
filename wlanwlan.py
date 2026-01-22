import network
import time
import rp2

def connect_wifi(ssid:str, password:str, max_wait:int = 30):
    rp2.country('CH')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)
    wlan.disconnect()
    time.sleep(1)
    wlan.connect(ssid, password)
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    if wlan.status() != 3:
        raise RuntimeError(f'network connection failed. Status: {wlan.status()}')
    status = wlan.ifconfig()
    print(f"Connected to {ssid} with IP {status[0]}")
    return status[0]
