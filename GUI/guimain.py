import gui as guiClass

# This shows how parameters and reference coordinates can be retrieved from GUI
if __name__ == "__main__":
    gui = guiClass.GUI()
    gui.run()

    params = gui.get_parameters()    
    for (i,p) in enumerate(params):
        print(f"Parameter {i+1}: {p}")

    coordinate_list = gui.get_ref_points()
    for coordinates in coordinate_list:
        print(f"Coordinate: ({coordinates[0]}, {coordinates[1]})")