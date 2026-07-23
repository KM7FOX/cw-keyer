from gpiozero import TonalBuzzer, LED, DigitalOutputDevice
from time import sleep
from queue import Queue
from threading import Thread

from km7fox_cw.morse import MORSE_CODE
from km7fox_cw.keyer.keyer import Keyer
from km7fox_cw.keyer.tx_keyer import TxKeyer
from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.events import Event


class CWTransmitter:
    def __init__(self, speed: int=10):
        self.speed = speed
        self.reverse_morse = {value: key for key, value in MORSE_CODE.items()}
        
        self.send_queue = Queue()
        timing = TimingModel()
        self.time_unit = 60 / (50 * self.speed)
        timing.dit_ms = self.time_unit
        timing.speed = self.speed
        tx_keyer_daemon = Thread(
            target=TxKeyer.run, 
            args=(False, self.send_queue, timing), 
            daemon=True
        )
        tx_keyer_daemon.start()
        
    def send(self, message: str) -> None:
        message = message.upper()
        
        for i, char in enumerate(message):
            if char == ' ':
                self.send_queue.put(Event('UP', 0, 4 * self.time_unit))
                Keyer.key_up(4 * self.time_unit)
            else:
                code = self.reverse_morse.get(char)
                if code is None:
                    print('Unknown character: "{char}"')
                    continue
                
                for element in code:
                    timing = 3 * self.time_unit if element == '-' else self.time_unit
                    self.send_queue.put(Event('DOWN', 0, timing * 1000))
                    Keyer.key_down(timing)
                    Keyer.key_up(self.time_unit)

                self.send_queue.put(Event('UP', 0, 2 * self.time_unit * 1000))
                Keyer.key_up(2 * self.time_unit)
                
    def set_settings(self, tone_on: bool=True, led_on: bool=True, on_air: bool=False):
        Keyer.set_settings(tone_on=tone_on, led_on=led_on, on_air=on_air)
        TxKeyer.on_air = on_air
                
    