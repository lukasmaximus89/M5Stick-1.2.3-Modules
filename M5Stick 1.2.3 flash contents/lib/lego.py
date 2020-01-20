from micropython import const
import uos as os
import utime as time
import machine
import ustruct
import i2c_bus


M5GO_WHEEL_ADDR = const(0x56)
MOTOR_CTRL_ADDR = const(0x00)
ENCODER_ADDR = const(0x04)

motor1_pwm = 0
motor2_pwm = 0

def dead_area(amt, low, low_up, high, high_up):
    if amt > low_up and amt < high_up:
        amt = 0
    elif amt > high_up and amt < high:
        amt = high
    elif amt > low and amt < low_up:
        amt = low
    return amt 

def constrain(amt, low, high):
    if amt < low:
        return low
    if amt > high:
        return high
    return amt


class NXT_Motor:
    def __init__(self, port):
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self.port = port
        self._position = 0

    def stop(self):
        self.set_pwm(0)

    def set_pwm(self, pwm):
        global motor1_pwm, motor2_pwm
        if self.port == 1:
            motor1_pwm = pwm
        else:
            motor2_pwm = pwm
        buf = ustruct.pack('<hh', int(motor1_pwm), int(motor2_pwm))
        self.i2c.writeto_mem(M5GO_WHEEL_ADDR, MOTOR_CTRL_ADDR, buf)

    def read_encoder(self):
        self.position_update()
        return self._position

    def _read_encoder(self):
        buf = bytearray(4)
        self.i2c.readfrom_mem_into(M5GO_WHEEL_ADDR, ENCODER_ADDR, buf)
        encoder_buf = tuple(ustruct.unpack('<hh', buf))
        if self.port == 1:
            return encoder_buf[0]
        else:
            return encoder_buf[1]
    
    def position_update(self):
        self._position += self._read_encoder()

    def run_to(self, pos, speed):
        error_last_1 = 0
        pwm_last = [255, 255, 255, 255]
        self.position_update()
        _distance = pos
        pwm_now = 0
        kp = 0.85
        kd = 7.5

        tick_now = time.ticks_ms()
        while True:
            time.sleep_ms(1)
            if time.ticks_ms() - tick_now > 10:
                tick_now = time.ticks_ms()
                self.position_update()
                error = _distance - self._position
                pwm_now = kp*error + kd*(error-error_last_1)
                pwm_now = constrain(pwm_now, -speed, speed)
                pwm_now = dead_area(pwm_now, -100, -3, 100, 3)
                pwm_now = -pwm_now
                error_last_1 = error
                self.set_pwm(pwm_now)
                pwm_last = pwm_last[1:4]
                pwm_last.append(pwm_now)
                if pwm_last == [0, 0, 0, 0]:
                    break

    def run_distance(self, distance=500, speed=255):
        error_last_1 = 0
        pwm_last = [255, 255, 255, 255]
        self.position_update()
        _distance = self._position+distance
        pwm_now = 0
        kp = 0.85
        kd = 7.5

        tick_now = time.ticks_ms()
        while True:
            time.sleep_ms(1)
            if time.ticks_ms() - tick_now > 10:
                tick_now = time.ticks_ms()
                self.position_update()
                error = _distance - self._position
                pwm_now = kp*error + kd*(error-error_last_1)
                pwm_now = constrain(pwm_now, -speed, speed)
                pwm_now = dead_area(pwm_now, -100, -3, 100, 3)
                pwm_now = -pwm_now
                error_last_1 = error
                self.set_pwm(pwm_now)
                pwm_last = pwm_last[1:4]
                pwm_last.append(pwm_now)
                if pwm_last == [0, 0, 0, 0]:
                    break