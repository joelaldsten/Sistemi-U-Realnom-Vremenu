import threading
import queue
import time
import numpy as np

class Regul:
    def __init__(self, q, PI, h, servo_controller, crazy_logger):
        self.q = q
        self.lock = threading.Lock()
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
        self._distance_min = 0.05
        self._shouldStop = False

        self.controll_signal = np.zeros(3)

    def get_control_signal(self):
        return self.controll_signal    
    
    def limit_v(self,v):
        if v > 1023:
            return 1023
        elif v < -1023:
            return -1023
        return round(v)
    
    def stopRunning(self):
        self.lock.acquire()
        self._shouldStop = True
        self.lock.release()
    
    def set_ref(self,pos):
        self._x_ref = pos[0]
        self._y_ref = pos[1]
        self._theta_ref = self._crazy_logger.theta()

    def update_params(self, params):
        self.lock.acquire()
        self._PI.setParam(params)
        self._h = self._PI._p.h
        self.lock.release()

    def phidot(self,xdot,ang):
        M = -1/self._r*np.array([[-np.sin(ang), np.cos(ang), self._R ],[-np.sin(ang+self._a1), np.cos(ang+self._a1), self._R],[-np.sin(ang+self._a2), np.cos(ang+self._a2), self._R]])
        return M.dot(xdot)
    
    def runMethod(self):
        while self.q.empty():
            time.sleep(0.5)
        self.set_ref(self.q.get())

        while True:
            print("x:",self._crazy_logger.x(),"\t y:",self._crazy_logger.y(),"\t theta:",self._crazy_logger.theta())
            t = time.time()
            angle = self._crazy_logger.theta()
            self.lock.acquire()
            e = np.array([self._x_ref - self._crazy_logger.x(), self._y_ref - self._crazy_logger.y(), self._theta_ref - angle])
            
            # #Calculate output and limit it 
            ph = self.phidot(e, angle)

            v = self._PI.calculate_output(ph)

            for i in range(len(v)):
                v[i] = self.limit_v(v[i])
            v = v.astype(np.int64)
            

            #Output the controlsignals
            self._servo_controller.actuate(v[0], v[1], v[2])
            self.controll_signal = v

            #Update states
            self._PI.update_state(v)
            d = np.sqrt(np.power(self._x_ref - self._crazy_logger.x(), 2) + np.power(self._y_ref - self._crazy_logger.y(),2))
            self.lock.release()
            if d < self._distance_min or self._shouldStop:
                self._servo_controller.actuate(0, 0, 0)
                self.controll_signal = np.zeros(3)
                if self._shouldStop:
                    while not self.q.empty():
                        self.q.get()
                    self._shouldStop = False
                while self.q.empty():
                    time.sleep(0.5)
                self.set_ref(self.q.get())
                self._PI._I = 0
                self._PI._v = 0

            t1 = time.time()
            calc_time = t1 - t
            sleep_time = self._h - calc_time
            if sleep_time < 0: sleep_time = 0
            time.sleep(sleep_time)
