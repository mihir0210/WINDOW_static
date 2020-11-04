import numpy as np



def airfoils_coord(type):
    '''Returns the x/c and y/c co-ordinates of the different airfoils used'''
    airfoil_geometry = []

    if type == 0:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\Cylinder_1.txt", unpack=True, skip_header=1)
    elif type == 1:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\Cylinder_2.txt", unpack=True, skip_header=1)
    elif type == 2:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\DU_99_W_405.txt", unpack=True, skip_header=1)
    elif type == 3:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\DU_99_W_350.txt", unpack=True, skip_header=1)
    elif type == 4:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\DU_97_W_300.txt", unpack=True, skip_header=1)
    elif type == 5:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\DU_91_W2_250.txt", unpack=True, skip_header=1)
    elif type == 6:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\DU_93_W_210.txt", unpack=True, skip_header=1)
    elif type == 7:
        airfoil_geometry = np.genfromtxt(r"Airfoils_data\NACA_64_618.txt", unpack=True, skip_header=1)

    return airfoil_geometry


