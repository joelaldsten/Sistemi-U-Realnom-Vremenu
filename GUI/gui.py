import tkinter as tk

class MarkingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x800")
                
        params = []


        def get_input(elems):
            for elem in elems:
                param = elem.get(1.0,tk.END)
                print(param)
                params.append(param)

        self.frame = tk.Frame(self.root, width=600, height=600, bg='white', borderwidth=2, relief='groove')
        self.frame.place(relx=0.05, rely=0.15)

        self.canvas = tk.Canvas(self.frame, width=600, height=600)
        self.canvas.pack()

        self.parameters_frame = tk.Frame(self.root, width=300, height=500, bg='white',borderwidth=2, relief='groove')
        self.parameters_frame.place(relx=0.6, rely=0.15)
        self.parameters_label = tk.Label(self.parameters_frame, text="Choose controller parameters")
        self.parameters_label.place(relx=0.1, rely=0)
        
        self.k_label = tk.Label(self.parameters_frame, text="k")
        self.k_label.place(relx=0.1, rely=0.1)

        self.k_text = tk.Text(self.parameters_frame, width=10, height=1)
        self.k_text.place(relx=0.4, rely=0.1)



        self.ti_label = tk.Label(self.parameters_frame, text="ti")
        self.ti_label.place(relx=0.1, rely=0.2)

        self.ti_text = tk.Text(self.parameters_frame, width=10, height=1)
        self.ti_text.place(relx=0.4, rely=0.2)




        self.configuration_button = tk.Button(self.parameters_frame, text="Apply", command= lambda: get_input([self.k_text, self.ti_text]))
        self.configuration_button.place(relx=0.2, rely=0.9)

        self.canvas.bind("<Button-1>", self.mark_point)
        self.points = []

        self.coord_label = tk.Label(self.root, text="Robot Position:")
        self.coord_label.place(relx=0.05, rely=0.05)

        self.coord_text = tk.Text(self.root, width=30, height=2)
        self.coord_text.place(relx=0.2, rely=0.05)

        self.robot_lines = []

        # Create a drop-down menu
        self.menu_bar = tk.Menu(self.root)
        self.controller_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.controller_menu.add_command(label="Start")
        self.controller_menu.add_command(label="Stop")
        self.controller_menu.add_command(label="Pause")
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

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    tool = MarkingTool()


    tool.run()

""" if __name__ == '__main__':
    tool = MarkingTool()
    tool.run()
 """

 