import threading
import time

#lock = threading.Lock()
class Regul:
    def __init__(self, PIx, PIy, PIt, h, servo_controller, crazy_logger):
        self._PIx = PIx
        self._PIy = PIy
        self._PIt = PIt
        self._h = h
        self._servo_controller = servo_controller
        self._crazy_logger = crazy_logger
        self._x_ref = 0
        self._y_ref = 0
        self._theta_ref = 0
        
    def limit_v(self,v):
        if v > 1023:
            return 1023
        elif v < -1023:
            return -1023
        return round(v)
    
    def set_ref(self,x,y,theta):
        self._xRef = x
        self._yRef = y 
        self._thetaRef = theta
    
    def runMethod(self, lock):

        while True:
            t = time.time()
            (x , y, theta) = (self._crazy_logger.x(), self._crazy_logger.y(), self._crazy_logger.theta())

            lock.acquire()
            #Calculate output and limit it 
            u_x = self.limit_v(self._PIx.calculate_output(x, self._x_ref))
            u_y = self.limit_v(self._PIy.calculate_output(y, self._y_ref))
            u_t = self.limit_v(self._PIt.calculate_output(theta, self._theta_ref))
            
            #Output the controlsignals
            self._servo_controller.actuate(u_x, u_y, u_t)

            #Update states
            self._PIx.update_state(u_x)
            self._PIy.update_state(u_y)
            self._PIt.update_state(u_t)
            lock.release()

            t1 = time.time()
            calc_time = t1 - t
            sleep_time = self._h - calc_time
            time.sleep(sleep_time)



            
    

