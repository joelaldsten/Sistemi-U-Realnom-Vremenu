import threading
import time

#lock = threading.Lock()
class Regul:
    def __init__(self, PIx, PIy, PIt, h):
        self._PIx = PIx
        self._PIy = PIy
        self._PIt = PIt
        self._h = h
        
    def limit(self,v):
        return 0

    def runMethod(self, lock):
        t = round(time.time()*1000)

        while True:
            (x , y, theta) = None #change to real cordinates
            (x_ref, y_ref, theta_ref) = None #Change to ref from GUI

            e_x = x_ref - x
            e_y = y_ref - y
            e_t = theta_ref - theta

            lock.acquire()
            u_x = limit(self._PIx.calculate_output(x, x_ref))
            u_y = limit(self._PIy.calculate_output(y, y_ref))
            u_t = limit(self._PIt.calculate_output(theta, theta_ref))
            
            #output u_x u_y u_t

            self._PIx.update_state(u_x)
            self._PIy.update_state(u_y)
            self._PIt.update_state(u_t)
            lock.release()

            t1 = round(time.time()*1000)
            calc_time = t1 - t
            sleep_time = self._h - calc_time
            time.sleep(sleep_time)



            
    

