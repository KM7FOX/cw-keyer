from gpiozero import TonalBuzzer, LED, DigitalOutputDevice
from time import sleep

from km7fox_cw.encoder.gpio_assignments import assignments


class Keyer:
    tone_on = True
    led_on = True
    on_air = False
    tone = 550
    smooth = False
    
    buzzer = TonalBuzzer(assignments['buzzer'])
    led = LED(assignments['led'])
    tx_key = None
    
    @classmethod
    def key_down(cls, timing: float=0.0) -> None:
        if cls.tone_on:
            cls.buzzer.play(cls.tone)
        if cls.led_on:
            cls.led.on()
        # if cls.on_air:
        #     cls.tx_key.on()
        sleep(timing)
        
    @classmethod
    def key_up(cls, timing: float=0.0) -> None:
        cls.buzzer.stop()
        cls.led.off()
        # cls.tx_key.off()
        sleep(timing)
        
    @classmethod
    def set_settings(cls, tone_on: bool=True, led_on: bool=True, 
                     on_air: bool=False, tone: int=550) -> None:
        cls.tone_on = tone_on
        cls.led_on = led_on
        cls.on_air = on_air
        cls.tone = tone
         