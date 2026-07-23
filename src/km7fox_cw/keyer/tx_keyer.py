from gpiozero import DigitalOutputDevice
from time import sleep
from queue import Queue

from km7fox_cw.encoder.gpio_assignments import assignments
from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.classify_event import classify_event


class TxKeyer:
    on_air = False
    tx_key = DigitalOutputDevice(assignments['tx_key'], initial_value=False)
    
    @classmethod
    def run(cls, smooth: bool, send_queue: Queue, timing_model: TimingModel) -> None:
        while True:           
            event = send_queue.get()
            if smooth and timing_model.ready:
                time_unit = 60 / (50 * timing_model.speed)
                token = classify_event(event, timing_model)
                if token == '.':
                    timing = time_unit
                elif token in ['-', '<EOC>']:
                    timing = time_unit * 3
                else:
                    timing = time_unit * 7
            else:
                timing = event.duration_ms / 1000
                
            if event.state == 'DOWN' and cls.on_air:
                cls.tx_key.on()
                sleep(timing)
                cls.tx_key.off()
            elif event.state == 'UP' and cls.on_air:
                max_gap = timing_model.dit_ms * 7 / 1000
                sleep(min(max_gap, timing))
                
