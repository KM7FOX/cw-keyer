from threading import Thread
from queue import Queue
from signal import pause

from km7fox_cw.encoder.straight_key_handler import StraightKeyHandler
from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.decoder.decode import Decoder
from km7fox_cw.keyer.tx_keyer import TxKeyer


class StraightKeyer:
    def __init__(self, smooth: bool=False):
        self.decoder_queue = Queue()
        self.timing = TimingModel()
        send_queue = Queue()
        
        self.key_handler = StraightKeyHandler(self.timing, self.decoder_queue, send_queue)
        self.key_daemon = Thread(target=self.key_handler.run, daemon=True)
        
        self.tx_key_daemon = Thread(
            target=TxKeyer.run, 
            args=(smooth, send_queue, self.timing),
            daemon=True
        ) 
        
    def run(self):
        self.key_daemon.start()
        self.tx_key_daemon.start()
        decoder = Decoder(self.decoder_queue, self.timing).decode_stream()
        for text in decoder:
            yield text
    
    def set_settings(self, tone_on: bool=True, led_on: bool=True, on_air: bool=False):
        self.key_handler.set_settings(tone_on=tone_on, led_on=led_on, on_air=on_air)
        TxKeyer.on_air = on_air
        

