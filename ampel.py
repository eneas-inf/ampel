from machine import Pin

class AmpelState:
    RED = 1
    YELLOW = 2
    GREEN = 3
    OFF = 4

class Ampel:
    def __init__(self, pinRed: int, pinYellow: int, pinGreen: int):
        self.pinRed = Pin(pinRed, Pin.OUT)
        self.pinYellow = Pin(pinYellow, Pin.OUT)
        self.pinGreen = Pin(pinGreen, Pin.OUT)
        self.state = AmpelState.OFF

    def set_state(self, state: int):
        pin = {
            AmpelState.RED: self.pinRed,
            AmpelState.YELLOW: self.pinYellow,
            AmpelState.GREEN: self.pinGreen,
            AmpelState.OFF: None
        }[state]
        for p in [self.pinRed, self.pinYellow, self.pinGreen]:
            if p == pin:
                p.on()
            elif p:
                p.off()
        self.state = state

    def get_state(self) -> int:
        return self.state
