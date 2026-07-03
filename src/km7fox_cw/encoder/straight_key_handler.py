from gpiozero import TonalBuzzer, LED, Button, DigitalOutputDevice
from signal import pause
from queue import Queue

from km7fox_cw.decoder.events import EventQueue
from km7fox_cw.decoder.timing_model import TimingModel
from km7fox_cw.encoder.keyer import Keyer
from km7fox_cw.encoder.gpio_assignments import assignments


class StraightKeyHandler:
    def __init__(self, timing: TimingModel, decoder_queue: Queue, debug: bool=False):
        self.timing = timing
        self.decoder_queue = decoder_queue
        self.debug = debug
        
        self.event_queue = EventQueue(self.timing, self.decoder_queue, debug=self.debug)
        self.key = Button(assignments['straight_key'], pull_up=True, bounce_time=0.05)
        
    def run(self):
        def key_down():
            Keyer.key_down()
            self.event_queue.enqueue_event('DOWN')

        def key_up():
            Keyer.key_up()
            self.event_queue.enqueue_event('UP')

        self.key.when_activated = key_down
        self.key.when_deactivated = key_up
        pause()
        
    def set_settings(self, tone_on: bool=True, led_on: bool=True, on_air: bool=False):
        Keyer.set_settings(tone_on=tone_on, led_on=led_on, on_air=on_air)
        
