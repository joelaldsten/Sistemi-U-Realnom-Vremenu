import numpy as np

class PI:

    def __init__(self, pi_paramters):
        self._p = pi_paramters
        self._I = 0
        self._v = 0
        self._e = np.zeros(3)
    
    def calculate_output(self, e):
        self._e = e
        v = self._p.K * (self._p.beta * (self._e)) + self._I
        return v

    def update_state(self, u):
        #self._I += (self._p.K*self._p.h / self._p.Ti)*self._e + (self._p.h / self._p.Tr)*(u - self._v)
        self._I = 0
     
class PIParameters:
    
    def __init__(self, K, Ti, h, beta, Tr):
        self.K = K
        self.Ti = Ti
        self.h = h
        self.beta = beta
        self.Tr = Tr

    