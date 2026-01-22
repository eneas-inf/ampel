from ampel import Ampel, AmpelState
from wlanwlan import connect_wifi
from ui import start_webserver

ssid = 'INF-LAB'
password = 'INF-LAB@BBZW-2024'

ip = connect_wifi(ssid, password)
print("Connected with IP:", ip)

ampel1 = Ampel(pinRed=6, pinYellow=7, pinGreen=8)
ampel2 = Ampel(pinRed=18, pinYellow=19, pinGreen=20)

from time import sleep
import random

start_webserver(port=80)

while(True):
    ampel1.set_state(random.randint(AmpelState.RED, AmpelState.GREEN))
    ampel2.set_state(random.randint(AmpelState.RED, AmpelState.GREEN))
    sleep(0.1)
