import tkinter as tk

class MarkingTool:
    params = []
    def __init__(self):
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

        self.canvas.bind("<Button-1>", self.mark_point)
        self.points = []

        self.coord_label = tk.Label(self.root, text="Robot Position:")
        self.coord_label.place(relx=0.05, rely=0.05)

        self.coord_text = tk.Text(self.root, width=30, height=2)
        self.coord_text.place(relx=0.2, rely=0.05)

        self.robot_lines = []

        self.option_var = tk.StringVar(self.root)
        self.option_var.set("Controller Menu")
        self.option_menu = tk.OptionMenu(self.root, self.option_var, "PID", "Kalman", "MPC", command=self.update_gui)
        self.option_menu.place(relx=0.6, rely=0.05)

        # Create a drop-down menu
        self.menu_bar = tk.Menu(self.root)
        self.controller_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.controller_menu.add_command(label="PID")
        self.controller_menu.add_command(label="Kalman")
        self.controller_menu.add_command(label="MPC")
        self.menu_bar.add_cascade(label="Controller Menu", menu=self.controller_menu)
        self.root.config(menu=self.menu_bar)


    def mark_point(self, event, robot_x=None, robot_y=None):
        """x, y = event.x, event.y
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
        self.points.append((x, y))
        print(f"Marked point at ({x}, {y})")"""

        x, y = event.x, event.y
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
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
    

    def update_gui(self, option):
        frame = self.parameters_frame
        for widgets in frame.winfo_children():
            widgets.destroy()
        if option == "PID":
            self.parameters_label = tk.Label(self.parameters_frame, text="Choose controller parameters")
            self.parameters_label.place(relx=0.1, rely=0)

            ## K ##
            self.k_label = tk.Label(self.parameters_frame, bg='white', text="K")
            self.k_label.place(relx=0.1, rely=0.1)

            self.k_text = tk.Text(self.parameters_frame, width=10, height=1)
            self.k_text.place(relx=0.4, rely=0.1)

            ## Ti ##
            self.ti_label = tk.Label(self.parameters_frame, bg='white', text="Ti")
            self.ti_label.place(relx=0.1, rely=0.2)

            self.ti_text = tk.Text(self.parameters_frame, width=10, height=1)
            self.ti_text.place(relx=0.4, rely=0.2)

            ## h ##
            self.h_label = tk.Label(self.parameters_frame, bg='white', text="h")
            self.h_label.place(relx=0.1, rely=0.3)

            self.h_text = tk.Text(self.parameters_frame, width=10, height=1)
            self.h_text.place(relx=0.4, rely=0.3)

            ## beta ##
            self.beta_label = tk.Label(self.parameters_frame, bg='white', text="beta")
            self.beta_label.place(relx=0.1, rely=0.4)

            self.beta_text = tk.Text(self.parameters_frame, width=10, height=1)
            self.beta_text.place(relx=0.4, rely=0.4)

            ## Tr ##
            self.tr_label = tk.Label(self.parameters_frame, bg='white', text="Tr")
            self.tr_label.place(relx=0.1, rely=0.5)

            self.tr_text = tk.Text(self.parameters_frame, width=10, height=1)
            self.tr_text.place(relx=0.4, rely=0.5)

            ## Apply parameters button ##
            self.configuration_button = tk.Button(self.parameters_frame, text="Apply", command= lambda: self.get_input([self.k_text, self.ti_text, self.h_text, self.beta_text, self.tr_text]))
            self.configuration_button.place(relx=0.2, rely=0.9)
            
            ## Error message ##
            self.error_label = tk.Label(self.parameters_frame, bg='white', text="")
            self.error_label.place(relx=0.2, rely=0.8)
            pass
        elif option == "Kalman":
            self.parameters_label = tk.Label(self.parameters_frame, text="Choose controller parameters")
            self.parameters_label.place(relx=0.1, rely=0)

            ## K ##
            self.k_label = tk.Label(self.parameters_frame, bg='white', text="K")
            self.k_label.place(relx=0.1, rely=0.1)

            self.k_text = tk.Text(self.parameters_frame, width=10, height=1)
            self.k_text.place(relx=0.4, rely=0.1)

            ## Apply parameters button ##
            self.configuration_button = tk.Button(self.parameters_frame, text="Apply", command= lambda: self.get_input([self.k_text]))
            self.configuration_button.place(relx=0.2, rely=0.9)

            ## Error message ##
            self.error_label = tk.Label(self.parameters_frame, bg='white', text="")
            self.error_label.place(relx=0.2, rely=0.8)
            pass
        elif option == "MPC":

            pass 

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    tool = MarkingTool()


    tool.run()

""" if __name__ == '__main__':
    tool = MarkingTool()
    tool.run()
 """

 