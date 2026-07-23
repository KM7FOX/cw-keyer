from dataclasses import dataclass
from collections import deque
from time import perf_counter_ns
from queue import Queue

from km7fox_cw.decoder.timing_model import TimingModel


@dataclass
class Event:
    state: str          # "DOWN" or "UP"
    timestamp_ns: int
    duration_ms: int = 0
    
    
class EventQueue:
    def __init__(self, timing: TimingModel, decoder_queue: Queue, send_queue: Queue):
        self.event_queue = deque()
        self.decoder_queue = decoder_queue
        self.timing = timing
        self.down_times = []
        self.send_queue = send_queue
               
    def enqueue_event(self, state: str) -> None:
        self.event_queue.append(Event(state, perf_counter_ns()))
        elapsed = 0
        if len(self.event_queue) > 1:
            current, previous = self.peek_event(-1), self.peek_event(-2)
            elapsed = current.timestamp_ns - previous.timestamp_ns
            elapsed //= 1_000_000
            previous.duration_ms = elapsed
            
            if previous.state == 'DOWN' and elapsed > 0:
                self.down_times.append(elapsed)
                
            event = self.dequeue_event()
            self.decoder_queue.put(event)
            if self.send_queue is not None:
                self.send_queue.put(event) 
                  
        # Bootstrap timings
        if len(self.down_times) > 1 and not self.timing.ready:
            if self.timing.try_bootstrap(self.down_times):
                self.down_times.clear()
                        
        # Update timings
        if len(self.down_times) >= 10 and self.timing.ready:
            if self.timing.refine_centers(self.down_times):
                self.down_times.clear()
        
    def peek_event(self, index: int=0) -> Event:
        if index >= len(self.event_queue):
            return None
        return self.event_queue[index]
    
    def dequeue_event(self) -> Event:
        return self.event_queue.popleft()
    