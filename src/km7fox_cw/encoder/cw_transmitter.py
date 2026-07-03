from gpiozero import TonalBuzzer, LED, DigitalOutputDevice
from time import sleep

from km7fox_cw.morse import MORSE_CODE
from km7fox_cw.encoder.keyer import Keyer


class CWTransmitter:
    def __init__(self, speed: int):
        self.speed = speed
        self.time_unit = 60 / (50 * speed)
        self.reverse_morse = {value: key for key, value in MORSE_CODE.items()}
        
    def send(self, message: str) -> None:
        message = message.upper()
        
        for i, char in enumerate(message):
            if char == ' ':
                Keyer.key_up(4 * self.time_unit)
            else:
                code = self.reverse_morse.get(char)
                if code is None:
                    print('Unknown character: "{char}"')
                    continue
                
                for element in code:
                    timing = 3 * self.time_unit if element == '-' else self.time_unit
                    Keyer.key_down(timing)
                    Keyer.key_up(self.time_unit)

                Keyer.key_up(2 * self.time_unit)
                
    def set_settings(self, tone_on: bool=True, led_on: bool=True, on_air: bool=False):
        Keyer.set_settings(tone_on=tone_on, led_on=led_on, on_air=on_air)
                
    