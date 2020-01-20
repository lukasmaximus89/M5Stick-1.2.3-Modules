import i2c_bus
from micropython import const

_addr = const(0x53)
_us_addr = const(0x00)
_angle_addr = const(0x10)

class Servo:
    def __init__(self, min_us=700, max_us=2300):
        self.i2c = i2c_bus.get(i2c_bus.PORTA)
        self.min_us = min_us;
        self.max_us = max_us

    def write_us(self, num, us):
        msc = 0
        if us == 0:
            msc = 0
        msc = int(min(self.max_us, max(self.min_us, us)))
        num = min(11, max(0, num))
        us_byte = bytearray(2)
        us_byte[0] = msc & 0x00ff
        us_byte[1] = msc >> 8 & 0x00ff
        self.i2c.writeto_mem(_addr, _us_addr | num, us_byte)
        
    def write_angle(self, num, angle):
        angle = min(180, max(0, angle))
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * angle // 180
        self.write_us(num, us)