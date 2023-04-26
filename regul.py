import threading
import time
import numpy as np

class Regul:
    def __init__(self, PI, h, servo_controller, crazy_logger):
        self._PI = PI
        self._h = h
        self._servo_controller = servo_controller
        self._crazy_logger = crazy_logger
        self._x_ref = 0
        self._y_ref = 0
        self._theta_ref = 0
        # Robot parameters
        self._R = 0.16 		# Distance between center of robot and wheels
        self._a1 = 2*np.pi/3 	# Angle between x axis and first wheel
        self._a2 = 4*np.pi/3  # Angle between x axis and second wheel
        self._r = 0.028*0.45/18 # Wheel radius. Has been fudge-factored because the actual velocity of the wheels did not align with the set-points.
    
    def limit_v(self,v):
        if v > 1023:
            return 1023
        elif v < -1023:
            return -1023
        return round(v)
    
    def set_ref(self,x,y,theta):
        self._x_ref = x
        self._y_ref = y 
        self._theta_ref = theta #?

    def phidot(self,xdot,ang):
        M = 1/self._r*np.array([[-np.sin(ang), np.cos(ang), self._R ],[-np.sin(ang+self._a1), np.cos(ang+self._a1), self._R],[-np.sin(ang+self._a2), np.cos(ang+self._a2), self._R]])
        return M.dot(xdot)
    
    def runMethod(self):

        while True:
            print("x:",self._crazy_logger.x(),"\t y:",self._crazy_logger.y(),"\t theta:",self._crazy_logger.theta())
            t = time.time()
            angle = self._crazy_logger.theta()
            e = np.array([self._x_ref - self._crazy_logger.x(), self._y_ref - self._crazy_logger.y(), self._theta_ref - angle])
            
            #Calculate output and limit it 
            v = self._PI.calculate_output(e)
            
            ph = self.phidot(v, angle)
            for i in range(len(ph)):
                ph[i] = self.limit_v(ph[i])
            
            print("theta: ", ph[2])

            #Output the controlsignals
            self._servo_controller.actuate(ph[0], ph[1], ph[2])

            #Update states
            self._PI.update_state(v)

            t1 = time.time()
            calc_time = t1 - t
            sleep_time = self._h - calc_time
            time.sleep(sleep_time)



            
    

