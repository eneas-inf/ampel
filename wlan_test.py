# Bibliotheken laden
import network
import time
from time import sleep

# WLAN-Konfiguration
wlanSSID = 'INF-LAB'
wlanPW = 'INF-LAB@BBZW-2024'
network.country('CH')

# WLAN-Verbindung herstellen
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print('WLAN-Verbindung herstellen')
    wlan.active(True)
    wlan.connect(wlanSSID, wlanPW)
    sleep(5)

# WLAN-Verbindung prüfen
if wlan.isconnected():
    print('WLAN-Verbindung hergestellt')
else:
    print('Keine WLAN-Verbindung')

# WLAN-Verbindungsstatus
print('WLAN-Status:', wlan.status())