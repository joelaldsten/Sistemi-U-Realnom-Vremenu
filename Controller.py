import numpy as np
import socket
import queue
from threading import Thread
# Dynamixel packages
from dynamixel.model.xm430_w210_t_r import XM430_W210_T_R
import dynamixel.channel
import time

#Crazy packages
import logging
from threading import Timer

import cflib.crtp  # noqa
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.utils import uri_helper

from control import PI
from control import PIParameters

from regul import Regul

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
        print(s1," ", s2, " ", s3)
        try:
            self.servos[0].goal_velocity.write(s1)
            self.servos[1].goal_velocity.write(s2)
            self.servos[2].goal_velocity.write(s3)
        except:
            for s in self.servos:
                s.bus_watchdog.write(0) # Clear old watchdog error
                s.bus_watchdog.write(100) # 2 second timeout
                s.torque_enable.write(1)
            self.servos[0].goal_velocity.write(s1)
            self.servos[1].goal_velocity.write(s2)
            self.servos[2].goal_velocity.write(s3)
        return None

class CrazyLogger:

    """
    Simple logging class that logs the Crazyflie Stabilizer from a supplied
    link uri.
    """
    # Define which states to log:
    namelink = {'stateEstimate.x': 0, 'stateEstimate.y': 1,'stateEstimate.z': 2, 'stabilizer.yaw':3}
    #_Offset for crazyflie position on robot to center
    position_offset = 0.11

    def __init__(self, link_uri):
        self._cf = Crazyflie(rw_cache='./cache')
        self._state = np.array([0.0,0.0,0.0,0.0])

        # Connect some callbacks from the Crazyflie API
        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)

        print('Connecting to %s' % link_uri)

        # Try to connect to the Crazyflie
        self._cf.open_link(link_uri)

        # Variable used to keep main loop occupied until disconnect
        self.is_connected = True

    def _connected(self, link_uri):
        # This callback is called form the Crazyflie API when a Crazyflie
        # has been connected and the TOCs have been downloaded.
        print('Connected to %s' % link_uri)

        # The definition of the logconfig can be made before connecting
        self._lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        self._lg_stab.add_variable('stateEstimate.x', 'float')
        self._lg_stab.add_variable('stateEstimate.y', 'float')
        self._lg_stab.add_variable('stateEstimate.z', 'float')
        self._lg_stab.add_variable('stabilizer.yaw', 'float')

        # The fetch-as argument can be set to FP16 to save space in the log packet
        #self._lg_stab.add_variable('pm.vbat', 'FP16')

        # Adding the configuration cannot be done until a Crazyflie is
        # connected, since we need to check that the variables we
        # would like to log are in the TOC.
        try:
            self._cf.log.add_config(self._lg_stab)
            # This callback will receive the data
            self._lg_stab.data_received_cb.add_callback(self._stab_log_data)
            # This callback will be called on errors
            self._lg_stab.error_cb.add_callback(self._stab_log_error)
            # Start the logging
            self._lg_stab.start()
        except KeyError as e:
            print('Could not start log configuration,'
                  '{} not found in TOC'.format(str(e)))
        except AttributeError:
            print('Could not add Stabilizer log config, bad configuration.')

    def _stab_log_error(self, logconf, msg):
        # Callback from the log API when an error occurs
        print('Error when logging %s: %s' % (logconf.name, msg))

    def _stab_log_data(self, timestamp, data, logconf):
        # Callback from a the log API when data arrives
        #print(f'[{timestamp}][{logconf.name}]: ', end='')
        for name, value in data.items():
            self._state[self.namelink[name]] = value
            #print(f'{name}: {value:3.3f} ', end='\n')
        #print()

    def _connection_failed(self, link_uri, msg):
        # Callback when connection initial connection fails (i.e no Crazyflie
        # at the specified address)
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.is_connected = False

    def _connection_lost(self, link_uri, msg):
        # Callback when disconnected after a connection has been made (i.e
        # Crazyflie moves out of range)
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        # Callback when the Crazyflie is disconnected (called in all cases)"""
        # print('Disconnected from %s' % link_uri)
        self.is_connected = False

    def disconnect(self):
        self._cf.close_link()

    def x(self):
		# Return x-position of robot center
		# Note that the offset of the crazyflie mount position is included
        return self._state[0] - np.sin(np.deg2rad(self._state[3]))*self.position_offset

    def y(self):
		# Return y-position of robot center
		# Note that the offset of the crazyflie mount position is included
        return self._state[1] + np.cos(np.deg2rad(self._state[3]))*self.position_offset

    def z(self):
		# Return z-position of robot center
        return self._state[2]

    def theta(self):
		# Return direction of robot center, measured in radians between -pi and pi.
		# Note that the offset of the crazyflie mount position is included
        return np.mod(self._state[3]*np.pi/180 + 11*np.pi/6,2*np.pi)-np.pi

    def states(self):
        return self._state

    def close(self):
        self._cf.close_link()


def start_com(q, reg, cl):
    s = socket.socket()
    s.connect(("192.168.0.113", 55555))
    print("Connected")
    while True:
        data = s.recv(1024).decode("utf-8")
        if data == "GETPOS":
            u = reg.get_control_signal()
            s.sendall(bytes("{}|{}|{}|{}|{}|{}".format(cl.x(), cl.y(), cl.theta(), u[0], u[1], u[2]), encoding='utf-8'))
            print("Recived get position")
        elif data.startswith("PID"):
            data = data.split(" ")
            print(data)
            reg.update_params(PIParameters(float(data[1]),float(data[2]),float(data[3]),float(data[4]),float(data[5])))
            print("updated params")
        elif data.startswith("POS"):
            q.put(((float(data.split("|")[1]), float(data.split("|")[2]))))
            print('Received x = {}, y = {}\n'.format(data.split("|")[1], data.split("|")[2]))
        elif data.startswith("STOP"):
            reg.stopRunning()
            print("Recived STOP")
        else:
            print("Received unknown data")
        if not data:
            print("no data")
            break

servo_contr = Servo_controller()
cflib.crtp.init_drivers()                        # Initiate drivers for crazyflie
uri = uri_helper.uri_from_env(default='usb://0') # Connection-uri for crazyflie via USB
cl = CrazyLogger(uri)
time.sleep(1) # Wait for connection to work

q = queue.Queue()
pi = PI(PIParameters(1.75,15,0.01,0.8,50))
reg = Regul(q, pi, 0.01, servo_contr, cl)
Thread(target=start_com, args=(q, reg, cl)).start()
reg.runMethod()

cl.disconnect()
