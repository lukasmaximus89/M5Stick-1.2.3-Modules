from machine import ADC
from machine import PWM
from machine import Pin
_pin_adc_map ={}
_pin_pwm_map = {}
_pin_io_map = {}

def pinDeinit():
    global _pin_adc_map, _pin_pwm_map, _pin_io_map
    _pin_adc_map ={}
    _pin_pwm_map = {}
    _pin_io_map = {}

class M5_Pin:
    def __init__(self):
        self._pin_adc_map = _pin_adc_map
        self._pin_pwm_map = _pin_pwm_map
        self._pin_io_map = _pin_io_map
        self._ATTN = ADC.ATTN_11DB
        self._WIDTH = ADC.WIDTH_12BIT

    def analogRead(self, pin):
        if str(pin) not in self._pin_adc_map.keys():
            try:
                self._pin_adc_map[str(pin)] = ADC(pin)
                self._pin_adc_map[str(pin)].atten(self._ATTN)
                self._pin_adc_map[str(pin)].width(self._WIDTH)
            except:
                return 0

        data = self._pin_adc_map[str(pin)].read()
        ad_data = int(data * 1024 / 3300)
        return ad_data
    
    def analogWrite(self, pin, duty, pwm = 38000):
        if str(pin) not in self._pin_pwm_map.keys():
            try:
                self._pin_pwm_map[str(pin)] = PWM(pin, freq=pwm, duty=duty, timer=1)
                return 1
            except:
                return 0
        else:
            self._pin_pwm_map[str(pin)].duty(duty)
            return 1
    
    def pin_mode(self, pin, mode, pull=Pin.PULL_FLOAT):
        if str(pin) not in self._pin_io_map.keys():
            pull = machine.Pin.PULL_UP if mode == machine.Pin.IN else pull
            self._pin_io_map[str(pin)] = Pin(pin, mode=mode, pull=pull)
        else:
            self._pin_io_map[str(pin)].init(mode=mode, pull=pull)
        
    def digitalWrite(self, pin, value):
        if str(pin) not in self._pin_io_map.keys():
            self._pin_io_map[str(pin)] = Pin(pin, mode=Pin.INOUT)
        self._pin_io_map[str(pin)].value(value)
        
    def digitalRead(self, pin):
        if str(pin) not in self._pin_io_map.keys():
            self._pin_io_map[str(pin)] = Pin(pin, mode=Pin.INOUT)
        return self._pin_io_map[str(pin)].value()

    def toggle(self, pin):
        self.digitalWrite(pin, 1- self.digitalRead(pin))


