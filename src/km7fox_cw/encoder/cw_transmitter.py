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
        self.reverse_morse = {value: key for key, value in MORSE_CODE.items()}
        
        self.send_queue = Queue()
        self.timing = TimingModel()
        self.set_speed(speed)
        tx_keyer_daemon = Thread(
            target=TxKeyer.run, 
            args=(False, self.send_queue, self.timing), 
            daemon=True
        )
        tx_keyer_daemon.start()
        
    def send(self, message: str) -> None:
        message = message.upper()
        
        for i, char in enumerate(message):
            if char == ' ':
                self.send_queue.put(Event('UP', 0, 4 * self.timing.dit_ms))
                Keyer.key_up(4 * self.timing.dit_ms)
            else:
                code = self.reverse_morse.get(char)
                if code is None:
                    print('Unknown character: "{char}"')
                    continue
                
                for element in code:
                    timing = 3 * self.timing.dit_ms if element == '-' else self.timing.dit_ms
                    self.send_queue.put(Event('DOWN', 0, timing * 1000))
                    Keyer.key_down(timing)
                    Keyer.key_up(self.timing.dit_ms)

                self.send_queue.put(Event('UP', 0, 2 * self.timing.dit_ms * 1000))
                Keyer.key_up(2 * self.timing.dit_ms)
                
    def set_settings(self, tone_on: bool=True, led_on: bool=True, on_air: bool=False):
        Keyer.set_settings(tone_on=tone_on, led_on=led_on, on_air=on_air)
        TxKeyer.on_air = on_air
        
    def set_speed(self, speed):
        time_unit = 60 / (50 * speed)
        self.timing.dit_ms = time_unit
        self.timing.speed = speed
                
    