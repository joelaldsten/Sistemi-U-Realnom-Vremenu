# Dynamixel packages
from dynamixel.model.xm430_w210_t_r import XM430_W210_T_R
import dynamixel.channel
import time

class Servo_controller:

    def __init__(self):
        self.channel = dynamixel.channel.Channel(speed=57600,device='/dev/ttyACM0')
        self.servos = [XM430_W210_T_R(self.channel, 1),
                       XM430_W210_T_R(self.channel, 2),
                       XM430_W210_T_R(self.channel, 3)]
        for s in self.servos:
            s.torque_enable.write(0)
            print(s.model_number.read(), s.id.read())
            s.operating_mode.write(1)
            s.bus_watchdog.write(0) # Clear old watchdog error
            s.bus_watchdog.write(100) # 2 second timeout
            s.torque_enable.write(1)

    def actuate(self, s1, s2, s3):
        self.servos[0].goal_velocity.write(s1)
        self.servos[1].goal_velocity.write(s2)
        self.servos[2].goal_velocity.write(s3)
        return None

servo_contr = Servo_controller()
for i in range(10):
    servo_contr.actuate(100, 0, 0)
    time.sleep(0.1)
for i in range(10):
    servo_contr.actuate(0, 0, 0)
    time.sleep(0.1)
for i in range(10):
    servo_contr.actuate(0, 100, 0)
    time.sleep(0.1)
for i in range(10):
    servo_contr.actuate(0, 0, 0)
    time.sleep(0.1)
for i in range(10):
    servo_contr.actuate(0, 0, 100)
    time.sleep(0.1)
for i in range(10):
    servo_contr.actuate(0, 0, 0)
    time.sleep(0.1)
for i in range(10):
    servo_contr.actuate(1023,1023,1023)
    time.sleep(0.1)