from threading import Thread
from queue import Queue
from signal import pause

from km7fox_cw.encoder.straight_key_handler import StraightKeyHandler
from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.decoder.decode import Decoder


class StraightKeyer:
    def __init__(self, smooth: bool=False):
        self.decoder_queue = Queue()
        self.timing = TimingModel()
        
        if smooth:
            self.send_queue = Queue()
            # add sender
            
        else:
            self.send_queue = None
            
        self.key_handler = StraightKeyHandler(self.timing, self.decoder_queue, self.send_queue)
        self.key_daemon = Thread(target=self.key_handler.run, daemon=True)
        
    def run(self):
        self.key_daemon.start()
        decoder = Decoder(self.decoder_queue, self.timing).decode_stream()
        for text in decoder:
            yield text
            
    def stop(self):
        pass
    
    def set_settings(self, tone_on: bool=True, led_on: bool=True, on_air: bool=False):
        self.key_handler.set_settings(tone_on=tone_on, led_on=led_on, on_air=on_air)
        

