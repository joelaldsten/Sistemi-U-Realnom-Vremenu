import numpy as np

class PI:

    def __init__(self, pi_paramters):
        self._p = pi_paramters
        self._I = 0
        self._v = 0
        self._e = np.zeros(3)
        self._extra_K = np.array([1,1,0.25])
    
    def calculate_output(self, e):
        self._e = e
        self._v = self._p.K*self._extra_K * (self._p.beta * (self._e)) + self._I
        return self._v

    def update_state(self, u):
        self._I += (self._p.K*self._extra_K*self._p.h / self._p.Ti)*self._e + (self._p.h / self._p.Tr)*(u - self._v)
        print("inegral action: ", self._I)
        #self._I = 0

    def setParam(self, newParams):
        self._p = newParams
     
class PIParameters:
    
    def __init__(self, K, Ti, h, beta, Tr):
        self.K = K
        self.Ti = Ti
        self.h = h
        self.beta = beta
        self.Tr = Tr

    