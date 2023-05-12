import tkinter as tk
import socket
import subprocess
import time
from threading import Thread
import collections
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GUI:
    params = []
    def __init__(self):
        self.fig = plt.figure(figsize=(6,3))
        self.x = collections.deque(np.zeros(100))
        self.y = collections.deque(np.zeros(100))
        self.theta = collections.deque(np.zeros(100))
        self.t = collections.deque(np.arange(0,100))
        self.one = np.ones(100)

        self.robotx = 0
        self.roboty = 0
        self.robottheta = 0

        self.xplot = plt.subplot(311)
        self.yplot = plt.subplot(312)
        self.thetaplot = plt.subplot(313)

        # self.xplot, = plt.plot(self.t, self.x, '-')
        # self.xplot.set_data(self.t,self.x)
    
        # plt.axis([self.t[0], self.t[len(self.t) - 1], -3, 3])
        
        # self.yplot, = plt.plot(self.t, self.y, '-')
        # self.yplot.set_data(self.t,self.y)
        # lntheta, = plt.plot(self.t, self.theta, '-')

        self.root = tk.Tk()
        self.root.geometry("1200x800")
        self.root.title("Project GUI")

        ## Canvas ##
        self.frame = tk.Frame(self.root, width=600, height=600, bg='white', borderwidth=2, relief='groove')
        self.frame.place(relx=0.05, rely=0.15)

        self.canvas = tk.Canvas(self.frame, width=600, height=600)
        self.canvas.pack()

        ## Paramaters ##
        self.parameters_frame = tk.Frame(self.root, width=300, height=500, bg='white',borderwidth=2, relief='groove')
        self.parameters_frame.place(relx=0.6, rely=0.15)
        self.show_parameters()

        self.canvas.bind("<Button-1>", self.mark_point)
        self.points = []

        self.coord_label = tk.Label(self.root, text="Robot Position:")
        self.coord_label.place(relx=0.05, rely=0.05)

        self.coord_text = tk.Text(self.root, width=30, height=2)
        self.coord_text.place(relx=0.2, rely=0.05)

        self.robot_lines = []

        print("Created socket")
        s = socket.create_server(("", 55555))
        s.listen()
        print("Listening")
        self.socket, addr = s.accept()
        print("Accepted")

    def get_parameters(self):
        return self.params

    # Get reference points
    def get_ref_points(self):
        return self.points

    def transform_coords(self, gui_coords):
        x_gui = gui_coords[0]
        y_gui = gui_coords[1]

        scaling_x = x_gui/600
        scaling_y = y_gui/600

        # Predetermined points
        A = [-0.9,0.9]
        B = [1.34059,0.03992]
        C = [-1.76008,-1.34059]
        D = [0.48051,-2.20068]

        # Predetermined slopes for basis vectors
        k_n = 2.60509
        k_p = -0.38387

        # Find points x_m, y_m on line CD, corresponding to scaling_x fractions of the line towards D
        # Call this point E
        x_m = C[0]*(1-scaling_x ) + D[0]*scaling_x
        y_m = C[1]*(1-scaling_x) + D[1]*scaling_x
        E = [x_m,y_m]

        # Find points x_m2, y_m2 on line CA, corresponding to scaling_y fractions of the line towards A
        # Call this point F
        x_m2 = C[0]*scaling_y + A[0]*(1-scaling_y)
        y_m2 = C[1]*scaling_y + A[1]*(1-scaling_y)
        F = [x_m2,y_m2]
        #print(f"E: ({E}), F: ({F})")


        # Find linear equations y_e and y_f
        # y_e is the line being perpendicular to the line CD (parallel to CA) going through E
        # y_f is the line being perpendicular to the line CA (parallel to CD) going through F

        k_e = k_n
        left_side = E[1]
        right_side = k_e * E[0]
        m_e = left_side - right_side
        #print(f"y_e = k_e*x + m_e = {k_e}*x + {m_e}")

        k_f = k_p
        left_side = F[1]
        right_side = k_f * F[0]
        m_f = left_side - right_side
        #print(f"y_f = k_f*x + m_f = {k_f}*x + {m_f}")

        # Find intersection between y_e and y_f, y_f = y_e
        #print(f"k_f = {k_f}, k_e = {k_e}")
        #print(f"y_f = y_e <=> {k_f}x + {m_f} = {k_e}x + {m_e}")

        # Move x to left side
        left = k_f - k_e
        # Move constants to right side
        right = m_e - m_f

        #print(f"Equation to solve for x: {left}x = {right}")
        x = right/left
        y = k_e*x + m_e

        #print(f"x = {x}, y = {y}")
        return [x,y]

    def mark_point(self, event, robot_x=None, robot_y=None):
        """x, y = event.x, event.y
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
        self.points.append((x, y))
        print(f"Marked point at ({x}, {y})")"""

        x, y = event.x, event.y
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")

        # Transform coordinates
        new_coords = self.transform_coords([x,y])
        x = new_coords[0]
        y = new_coords[1]
        Thread(target = self.send_data, kwargs ={"data" : ("POS|{}|{}".format(x,y))}).start()

        self.points.append((x, y))

        print(f"Robot at ({x}, {y})")

        self.coord_text.delete("1.0", tk.END)
        self.coord_text.insert(tk.END, f"({x}, {y})\n")

        if robot_x is not None and robot_y is not None:
            last_x, last_y = self.points[-1]
            line = self.canvas.create_line(last_x, last_y, robot_x, robot_y, fill="red")
            self.robot_lines.append(line)

        if len(self.points) >= 2:
            start_x, start_y = self.points[-2]
            end_x, end_y = self.points[-1]
            line = self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue")
            self.robot_lines.append(line)

    def isFloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def get_input(self, elems):
        self.params.clear()
        # clear erro label
        self.error_label.config(text="")
        for elem in elems:
            param = elem.get(1.0,"end-1c")
            print(param)
            if self.isFloat(param):
                self.params.append(float(param))

            else:
                self.params.append(float(0))
                self.error_label.config(text=f"Wrong format of input: '{param}'")

        print(self.params)


    def show_parameters(self):

        self.parameters_label = tk.Label(self.parameters_frame, text="Choose controller parameters")
        self.parameters_label.place(relx=0.1, rely=0)
        ## K ##
        self.k_label = tk.Label(self.parameters_frame, bg='white', text="K")
        self.k_label.place(relx=0.1, rely=0.1)
        self.k_text = tk.Text(self.parameters_frame, width=10, height=1)
        self.k_text.place(relx=0.4, rely=0.1)
        self.k_text.insert(tk.END, "1.25")
        ## Ti ##
        self.ti_label = tk.Label(self.parameters_frame, bg='white', text="Ti")
        self.ti_label.place(relx=0.1, rely=0.2)
        self.ti_text = tk.Text(self.parameters_frame, width=10, height=1)
        self.ti_text.place(relx=0.4, rely=0.2)
        self.ti_text.insert(tk.END, "15.0")
        ## h ##
        self.h_label = tk.Label(self.parameters_frame, bg='white', text="h")
        self.h_label.place(relx=0.1, rely=0.3)
        self.h_text = tk.Text(self.parameters_frame, width=10, height=1)
        self.h_text.place(relx=0.4, rely=0.3)
        self.h_text.insert(tk.END, "0.01")
        ## beta ##
        self.beta_label = tk.Label(self.parameters_frame, bg='white', text="beta")
        self.beta_label.place(relx=0.1, rely=0.4)
        self.beta_text = tk.Text(self.parameters_frame, width=10, height=1)
        self.beta_text.place(relx=0.4, rely=0.4)
        self.beta_text.insert(tk.END, "0.8")
        ## Tr ##
        self.tr_label = tk.Label(self.parameters_frame, bg='white', text="Tr")
        self.tr_label.place(relx=0.1, rely=0.5)
        self.tr_text = tk.Text(self.parameters_frame, width=10, height=1)
        self.tr_text.place(relx=0.4, rely=0.5)
        self.tr_text.insert(tk.END, "50")
        ## Apply parameters button ##
        self.configuration_button = tk.Button(self.parameters_frame, text="Apply", command= lambda: Thread(target = self.update_params, kwargs ={"controller" : "PID"}).start())
        self.configuration_button.place(relx=0.2, rely=0.9)

        ## Stop button ##
        self.stop_button = tk.Button(self.parameters_frame, text="Stop", command= lambda: Thread(target = self.send_stop).start())
        self.stop_button.place(relx=0.6, rely=0.9)
        ## Error message ##
        self.error_label = tk.Label(self.parameters_frame, bg='white', text="")
        self.error_label.place(relx=0.2, rely=0.8)
        #Thread(target = self.update_params, kwargs ={"Controller" : ("PID")}).start()
        pass

    def update_params(self, controller):
        self.get_input([self.k_text, self.ti_text, self.h_text, self.beta_text, self.tr_text])
        if controller == "PID":
            self.send_data("PID: " + ' '.join([str(x) for x in self.params]))

    def send_data(self, data):
        self.socket.sendall(bytes(data, encoding='utf-8'))
        print('sent| ' + data)

    def send_stop(self):
        self.send_data("STOP")
        print("STOP")

    def get_robot_position_loop(self):
        period = 0.2
        while True:
            t = time.time()
            self.send_data("GETPOS")
            pos = self.socket.recv(1024).decode("utf-8").split("|")

            self.robotx = pos[0]
            self.roboty = pos[1]
            self.robottheta = pos[2]



            # print(pos)
            # self.x = np.concatenate((self.x[1:100],np.array(pos[0])))
            # self.t = self.t + self.one
            # plt.axis([self.t[0], self.t[len(self.t) - 1], -3, 3])
            # self.xplot.set_data(self.t,self.x)


            #printa x (pos[0]) och y (pos[1]) till gui
            #Vet inte hur time funkar är det sekunder? just nu användas 0.2 som period för 5hz.
            t1 = time.time()
            calc_time = t1 - t
            sleep_time = period - calc_time
            if sleep_time < 0: sleep_time = 0
            time.sleep(sleep_time)

    def run(self):
        Thread(target = self.get_robot_position_loop).start()
        ani = FuncAnimation(self.fig, self.update, interval=500)
        plt.show()
        self.root.mainloop()

    def update(self, frame):
        self.x.popleft()
        self.x.append(self.robotx)
        self.y.popleft()
        self.y.append(self.roboty)
        self.theta.popleft()
        self.theta.append(self.robottheta)

        self.xplot.cla()
        self.yplot.cla()
        self.thetaplot.cla()

        self.xplot.plot(self.x)
        self.xplot.set_ylim(-3,3)
        self.yplot.plot(self.y)
        self.yplot.set_ylim(-3,3)
        self.thetaplot.plot(self.theta)
        self.thetaplot.set_ylim(-4,4)

