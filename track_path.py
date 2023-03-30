import numpy as np
import pandas as pd
import sys

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

logging.basicConfig(level=logging.ERROR)


########################################################################
# 				SUPPORTING CLASSES AND FUNCTIONS
########################################################################

def load_servos():
#"""
#Servo load function, based on the dynamixel implementation of Anders Blomdell.
#"""

# The speed and channel numbers can be found and checked via the dynamixel software "dynamixel wizard".
# The device can be found by e.g. lsusb, and is currently adapted for the three-color robots.

    channel = dynamixel.channel.Channel(speed=57600,device='/dev/ttyACM0')
    servos = [ XM430_W210_T_R(channel, 1),
               XM430_W210_T_R(channel, 2),
               XM430_W210_T_R(channel, 3) ]
    for s in servos:
        s.torque_enable.write(0)
        print(s.model_number.read(), s.id.read())
        s.operating_mode.write(1)
        s.bus_watchdog.write(0) # Clear old watchdog error
        s.bus_watchdog.write(100) # 2 second timeout
        s.torque_enable.write(1)
        
    return servos

class SimplePI:
    """ 
    Simple PI implementation with basic anti-windup. The _saturation - variable sets the saturation of the anti-windup.
    """
    
    _saturation = 0.1
    
    def __init__(self,kp,ki,dt):
        """ Initialize the controller """

        self.e = np.zeros(3)
        self.dt = dt # Sample rate
        self.kp = kp # P-part gain
        self.ki = ki # I-part gain
    
    def update_control(self,e):
        self.e += e*self.dt # Update cumulative error
        
        # Saturate internal error for anti-windup
        self.e = np.sign(self.e)*np.array([min(ei,self._saturation) for ei in abs(self.e)])
        
        # Return control signal
        return self.kp*e + self.ki*self.e
     

class CrazyLogger:
    
    """
    Simple logging class that logs the Crazyflie Stabilizer from a supplied
    link uri and disconnects after 150s.
    """
    # Define which states to log:
    namelink = {'stateEstimate.x': 0, 'stateEstimate.y': 1,'stateEstimate.z': 2, 'stabilizer.yaw':3}
    #_Offset for crazyflie position on robot to center
    position_offset = 0.11

    def __init__(self, link_uri):
        """ Initialize and run the example with the specified link_uri """

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
        """ This callback is called form the Crazyflie API when a Crazyflie
        has been connected and the TOCs have been downloaded."""
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

        # Start a timer to disconnect in 150s
        t = Timer(150, self._cf.close_link)
        t.start()

    def _stab_log_error(self, logconf, msg):
        """Callback from the log API when an error occurs"""
        print('Error when logging %s: %s' % (logconf.name, msg))

    def _stab_log_data(self, timestamp, data, logconf):
        """Callback from a the log API when data arrives"""
        #print(f'[{timestamp}][{logconf.name}]: ', end='')
        for name, value in data.items():
            self._state[self._namelink[name]] = value
            #print(f'{name}: {value:3.3f} ', end='\n')
        #print()

    def _connection_failed(self, link_uri, msg):
        """Callback when connection initial connection fails (i.e no Crazyflie
        at the specified address)"""
        print('Connection to %s failed: %s' % (link_uri, msg))
        self.is_connected = False

    def _connection_lost(self, link_uri, msg):
        """Callback when disconnected after a connection has been made (i.e
        Crazyflie moves out of range)"""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        """Callback when the Crazyflie is disconnected (called in all cases)"""
        print('Disconnected from %s' % link_uri)
        self.is_connected = False
        
    def x(self):
		""" Return x-position of robot center"""
		# Note that the offset of the crazyflie mount position is included
        return self._state[0] - np.sin(np.deg2rad(self._state[3]))*self._position_offset 
    
    def y(self):
		""" Return y-position of robot center"""
		# Note that the offset of the crazyflie mount position is included
        return self._state[1] + np.cos(np.deg2rad(self._state[3]))*self._position_offset 
    
    def z(self):
		""" Return z-position of robot center"""
        return self._state[2]
    
    def theta(self):
		""" Return direction of robot center, measured in radians between -pi and pi."""
		# Note that the offset of the crazyflie mount position is included
        return np.mod(self._state[3]*np.pi/180 + 11*np.pi/6,2*np.pi)-np.pi
    
    def states(self):
        return self._state
    
    def close(self):
        self._cf.close_link()
          
########################################################################
# 					MAIN SCRIPT
########################################################################        
if __name__ == '__main__':
    
    # Read input trajectory filename
    if len(sys.argv) > 1:
        print("Input file name:",sys.argv[1])
        filename = sys.argv[1]
    else:
        print("No file name inupt. Using default file name: trajectory.csv")
        filename = "trajectory.csv"

	# Load trajectory
    print("Attempting to load trajectory file",filename)
    trajectory = pd.read_csv(filename)
    print("\nTrajectory loaded.")
    x = trajectory.x.to_numpy()
    y = trajectory.y.to_numpy()
    # Update theta to be in correct range (-pi,pi)
    theta = ((trajectory.theta + np.pi).mod(2*np.pi)-np.pi).to_numpy() # Put theta in range -pi -> pi instead of 0 -> 2pi
    
    #Find derivatives
    trajectory[["xdot","ydot","thetadot"]] = trajectory[["x","y","theta"]].diff(axis = 0).fillna(0)/0.1
        
    #FUDGE FACTOR TO DECREASE SPEED FOR TESTING!!!!
    # Should probably be removed in future iterations. Was included because
    # the robot was exceeding servo speed settings.
    fudgefactor = 3.0
    velref = trajectory[['xdot','ydot','thetadot']].to_numpy()/fudgefactor
    
    # Create time vector
    dt = trajectory.t.diff().mean()*fudgefactor
    t = trajectory.t.to_numpy()*fudgefactor
    tend = t[-1]
    n = t.size
    print("Sample time:",dt)
    print("Experiment time:",tend)
    print("Time steps:",n)

	# Read controller parameters
    if len(sys.argv) > 3:
        print("\nController parameters:")
        kp = float(sys.argv[2])
        ki = float(sys.argv[3])
    else:
        print("\nNo controller paramater input. Using default values:")
        kp = 0.1
        ki = 0.01

    print("kp =",kp)
    print("ki =",ki)

	
	# Robot parameters
    R = 0.16 		# Distance between center of robot and wheels
    a1 = 2*np.pi/3 	# Angle between x axis and first wheel
    a2 = 4*np.pi/3  # Angle between x axis and second wheel
    r = 0.028*0.45/18 # Wheel radius. Has been fudge-factored because the actual velocity of the wheels did not align with the set-points.

    print("Bot dimensions:")
    print("R =",R)
    print("R =",r)
    
    def phidot(xdot,ang):
        """Returns reference velocities for the wheels, given current system state and reference velocities"""
        M = -1/r*np.array([[-np.sin(ang), np.cos(ang), R ],[-np.sin(ang+a1), np.cos(ang+a1), R],[-np.sin(ang+a2), np.cos(ang+a2), R]])
        return M.dot(xdot)    
    
    
    # Initiate experiment
    print('Initiating experiment')
    servos = load_servos()			# Use predefined funtion to initiate servo connection
    cflib.crtp.init_drivers()       # Initiate drivers for crazyflie
    uri = uri_helper.uri_from_env(default='usb://0') # Connection-uri for crazyflie via USB
    cl = CrazyLogger(uri)           # Create a crazyflie-based logger
    pi = SimplePI(kp,ki,dt)         # Create a PI-controller 


    time.sleep(1) # Wait for connection to work
    t0 = time.time()
    
    # Main control loop
    for i in range(n-1):
		
		# Read current position error:
        e = np.array([trajectory.x.iloc[i]-cl.x(),trajectory.y.iloc[i]-cl.y(),trajectory.theta.iloc[i]-cl.theta()])
        
        # Create reference speed through feed-forward (velref) and feedback (pi):
        xdot = velref[i,:] + pi.update_control(e)
        
        # Transform from x,y,theta-speeds to wheel rotational speeds.
        ph = phidot(xdot,cl.theta())
        
        # Set all servospeeds (enact control signal)
		for (j,s) in enumerate(servos):
            s.goal_velocity.write(round(ph[j]))
        
        # Printing position and tracking error
        print("x:",cl.x(),"\t y:",cl.y(),"\t theta:",cl.theta())
        print("Position error:",e,"\n")
            
		# Wait until next loop-iteration
        time.sleep(max(t[i+1]+t0-time.time(),0))
        
        
        
    # Shutdown
    print("Experiment done, shutting down servos and logger")
    for s in servos:
        s.goal_velocity.write(0)
    print("Finishing position: x =",cl.x(),"\t y= ",cl.y(),"\t theta =",cl.theta())
    cl.close()    


