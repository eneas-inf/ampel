from machine import Pin

class AmpelState:
    RED = 1
    YELLOW = 2
    GREEN = 3
    OFF = 4
    RED_YELLOW = 5

class Ampel:
    def __init__(self, pinRed: int, pinYellow: int, pinGreen: int):
        self.pinRed = Pin(pinRed, Pin.OUT)
        self.pinYellow = Pin(pinYellow, Pin.OUT)
        self.pinGreen = Pin(pinGreen, Pin.OUT)
        self.state = AmpelState.OFF

    def set_state(self, state: int):
        # Reset all first
        self.pinRed.off()
        self.pinYellow.off()
        self.pinGreen.off()
        
        if state == AmpelState.RED:
            self.pinRed.on()
        elif state == AmpelState.YELLOW:
            self.pinYellow.on()
        elif state == AmpelState.GREEN:
            self.pinGreen.on()
        elif state == AmpelState.RED_YELLOW:
            self.pinRed.on()
            self.pinYellow.on()
            
        self.state = state

    def get_state(self) -> int:
        return self.state
