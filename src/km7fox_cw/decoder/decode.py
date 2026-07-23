from queue import Queue, Empty

from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.morse import MORSE_CODE
from km7fox_cw.classify_event import classify_event


EOM_SCALAR = 7.5

class Decoder:
    def __init__(self, decoder_queue: Queue, timing: TimingModel):
        self.decoder_queue = decoder_queue
        self.timing = timing
        
    def decode_stream(self):
        event_buffer = []
        sending = False
        while True:
            if not self.timing.ready:
                continue
            
            try:
                event = self.decoder_queue.get(timeout=EOM_SCALAR * self.timing.dit_ms / 1000)
            except Empty:
                token = "<EOM>"
            else:
                token = classify_event(event, self.timing)

            if token in (".", "-"):
                event_buffer.append(token)
                sending = True
            elif token == "<EOM>":
                if event_buffer:
                    yield self._get_char(event_buffer) + " "
                elif sending:
                    sending = False
                    yield "\n\n"
            elif token in ("<EOC>", "<EOW>") and event_buffer:
                yield self._get_char(event_buffer) + (" " if token == "<EOW>" else "")
                    
    def _get_char(self, event_buffer: list[str]) -> str:
        code = "".join(event_buffer)
        event_buffer.clear()
        return MORSE_CODE.get(code, "*") 

