from queue import Queue


from km7fox_cw.decoder.events import EventQueue
from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.decoder.decode import Decoder


class LiveCWDecoder:
    def __init__(self):
        self.decode_queue = Queue()
        self.timing = TimingModel()
        self.event_queue = EventQueue(self.timing, self.decode_queue)
        self.decoder = Decoder(self.decode_queue, self.timing)
        
    def enqueue_event(self, event: str) -> None:
        self.event_queue.enqueue_event(event)
    
    def listen_text(self):
        decoder = self.decoder.decode_stream()
        for text in decoder:
            yield text

    
        