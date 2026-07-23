from threading import Thread
from queue import Queue
from signal import pause

from km7fox_cw.encoder.straight_key_handler import StraightKeyHandler
from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.decoder.decode import Decoder
from km7fox_cw.encoder.smooth import SmoothKeyer


class StraightKeyer:
    def __init__(self, smooth: bool=False):
        self.decoder_queue = Queue()
        self.timing = TimingModel()
        self.smooth = smooth
        
        if smooth:
            send_queue = Queue()
            smooth_keyer = SmoothKeyer(send_queue, self.timing)
            self.smooth_daemon = Thread(target=smooth_keyer.run, daemon=True)
        else:
            send_queue = None
            
        self.key_handler = StraightKeyHandler(self.timing, self.decoder_queue, send_queue)
        self.key_daemon = Thread(target=self.key_handler.run, daemon=True)
        
    def run(self):
        if self.smooth:
            self.smooth_daemon.start()
        self.key_daemon.start()
        decoder = Decoder(self.decoder_queue, self.timing).decode_stream()
        for text in decoder:
            yield text
            
    def stop(self):
        if self.send_queue is not None:
            self.send_queue.put(None)
            self.smooth_daemon.join()
    
    def set_settings(self, tone_on: bool=True, led_on: bool=True, on_air: bool=False):
        self.key_handler.set_settings(tone_on=tone_on, led_on=led_on, on_air=on_air)
        

