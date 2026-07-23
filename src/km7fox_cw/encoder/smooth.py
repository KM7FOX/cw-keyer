from queue import Queue

from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.classify_event import classify_event
from km7fox_cw.encoder.keyer import Keyer


class SmoothKeyer:
    def __init__(self, send_queue: Queue, timing: TimingModel):
        self.send_queue = send_queue
        self.timing = timing
        
    def run(self):
        while True:
            if not self.timing.ready:
                continue
            
            event = self.send_queue.get()
            if event is None:
                break
            
            token = classify_event(event, self.timing)
            if token == '.':
                Keyer.key_down(self.timing.dit_ms)
                Keyer.key_up(self.timing.dit_ms)
            elif token == '-':
                Keyer.key_down(self.timing.dit_ms * 3)
                Keyer.key_up(self.timing.dit_ms)
            elif token == '<EOC>':
                Keyer.key_up(self.timing.dit_ms * 2)
            elif token == '<EOW>':
                Keyer.key_up(self.timing.dit_ms * 6)
            
            
        
        