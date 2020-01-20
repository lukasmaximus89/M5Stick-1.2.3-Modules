import i2c_bus

class StepMotor:
    def __init__(self, addr=0x70):
        # self.i2c = 
        # self.i2c = I2C(id=0, sda=a[0], scl=a[1])    
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self.addr = addr
        self.speed = 300

    def Stepmotor_xyz(self, x, y, z, speed=None):   
        str_x = str(x)  
        str_y = str(y)
        str_z = str(z)
        str_speed = str(speed if speed else self.speed)
        RapidMoveCMD = 'G1 X'+str_x+' Y'+str_y+' Z'+str_z+' F'+str_speed
        self.write(RapidMoveCMD)
    
    def write(self, buffer):
        self.i2c.writeto(self.addr, buffer + "\r\n")
    