from ampel import Ampel, AmpelState
from wlanwlan import connect_wifi
from ui import init_webserver, process_request
import time

# --- Konfiguration ---
SSID = 'INF-LAB'
PASSWORD = 'INF-LAB@BBZW-2024'

# --- Initialisierung ---

# 1. WiFi Verbinden
print("Verbinde mit WiFi...")
try:
    ip = connect_wifi(SSID, PASSWORD)
    print(f"Verbunden! IP-Adresse: {ip}")
except Exception as e:
    print(f"Fehler bei WiFi-Verbindung: {e}")
    # Wir machen weiter, damit die Ampel auch ohne WiFi (lokal/test) initiiert wird,
    # aber der Webserver wird ohne IP nicht erreichbar sein.

# 2. Hardware Setup
# Ampel 1: Autos (Pins 6, 7, 8)
# Ampel 2: Fussgänger (Pins 18, 19, 20)
# Hinweis: Fussgängerampeln nutzen oft kein Gelb, aber wir initialisieren es trotzdem.
ampel_auto = Ampel(pinRed=6, pinYellow=7, pinGreen=8)
ampel_fuss = Ampel(pinRed=18, pinYellow=19, pinGreen=20)

# 3. Webserver Starten
try:
    s = init_webserver(port=80)
    print("Webserver läuft.")
except Exception as e:
    print("Fehler beim Starten des Webservers:", e)
    s = None

# --- Logik ---

def set_initial_state():
    """Setzt den Grundzustand: Autos Grün, Fussgänger Rot"""
    print("Setze Grundzustand")
    ampel_auto.set_state(AmpelState.GREEN)
    ampel_fuss.set_state(AmpelState.RED)

def ablauf_fussgaenger_querung():
    """Führt die Ampelsequenz für Fussgänger durch"""
    print(">>> START: Fussgänger-Sequenz")
    
    # 1. Auto: Grün -> Gelb
    ampel_auto.set_state(AmpelState.YELLOW)
    time.sleep(2)
    
    # 2. Auto: Gelb -> Rot
    ampel_auto.set_state(AmpelState.RED)
    time.sleep(1.5) # Sicherheitszeit ("Räumzeit")
    
    # 3. Fussgänger: Rot -> Grün
    ampel_fuss.set_state(AmpelState.GREEN)
    
    # 4. Grünphase für Fussgänger
    time.sleep(5)
    
    # 5. Fussgänger: Grün -> Rot
    # (Optional: Könnte blinken, hier direkt Rot)
    ampel_fuss.set_state(AmpelState.RED)
    time.sleep(2) # Sicherheitszeit
    
    # 6. Auto: Rot -> Rot-Gelb
    ampel_auto.set_state(AmpelState.RED_YELLOW)
    time.sleep(1.5)
    
    # 7. Auto: Rot-Gelb -> Grün
    ampel_auto.set_state(AmpelState.GREEN)
    
    print(">>> ENDE: Fussgänger-Sequenz")

# Startzustand herstellen
set_initial_state()

# Hauptschleife
print("Bereit. Warte auf Eingaben...")
while True:
    try:
        if s:
            # Prüfe auf Web-Anfragen (non-blocking)
            action = process_request(s)
            
            if action == "fussgaenger":
                # Nur starten, wenn Autos gerade Grün haben (um Mehrfach-Starts zu verhindern)
                if ampel_auto.get_state() == AmpelState.GREEN:
                    ablauf_fussgaenger_querung()
                else:
                    print("Anfrage ignoriert: Ampelzyklus läuft bereits oder nicht im Grundzustand.")
            
            elif action == "auto":
                # "Auto kommt" Button:
                # Eigentlich haben Autos Dauergrün. Falls wir aber eine Logik hätten,
                # wo Autos Rot haben (z.B. gleichberechtigte Kreuzung), würde das hier Grün anfordern.
                # In diesem Szenario (Fussgängerampel) dient es eher zur Bestätigung oder Reset.
                if ampel_auto.get_state() != AmpelState.GREEN:
                    print("Auto-Anforderung erhalten (während Rotphase).")
                    # Hier könnte man die Grünphase für Fussgänger verkürzen oder vormerken,
                    # aber für einfach Logik warten wir einfach ab.
        
        # Kurze Pause um CPU zu entlasten
        time.sleep(0.05)
        
    except KeyboardInterrupt:
        print("Programm beendet.")
        break
    except Exception as e:
        print("Fehler in Hauptschleife:", e)
        time.sleep(1)
