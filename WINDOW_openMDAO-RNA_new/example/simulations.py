'''
This script is used to create the batch of simulations to be run using WINDOW for different values of
rated power and rotor radius. For each combination,
'''
import os
import numpy as np
from IEA_borssele_irregular_new_UC import run_main_script

power_values_600MWfarm = [10, 12, 15, 20, 30]
power_values_1000MWfarm = [10, 11.11, 12.5, 14.28, 16.67, 20, 25]
power_values_1400MWfarm = [10, 11.66, 14, 15.55, 17.5, 20, 23.33]
def batch():
    ###### Run a batch ######

    vals_power = [power_values_1400MWfarm[6]]
    vals_rad = np.linspace(90,150,13)


    for val in vals_rad:
        value_rad = val
        for val1 in vals_power:
                value_power = val1
                lcoe = run_main_script(value_rad, value_power)
                old_filename = 'parameters.csv'
                new_filename = 'parameters_' + str(value_power) + '_' + str(value_rad*2) + '.csv'
                os.rename(old_filename, new_filename)


def singlecase():
    ##### Run a single case #####
    value_power = 10
    value_rad = 180/2 #reference rotor radius

    # dict = {'target_IRR':target_IRR}
    # f = open('Input/finance.txt', 'w')
    # f.write(repr(dict) + '\n')
    # f.close()

    run_main_script(value_rad, value_power)
    old_filename = 'parameters.csv'
    new_filename = 'parameters_' + str(value_power) + '_' + str(value_rad*2) + '.csv'
    os.rename(old_filename, new_filename)

## RUN ##


#batch()
#singlecase()

##### Create a lookup table for Diameter vs Number of turbines ####



def fixed_area(a_const):
    n_t = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]
    dia = [180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]



    import pandas as pd
    area_database = pd.read_csv('area_database.csv', header=None)
    area_database = pd.DataFrame.to_numpy(area_database)

    rated_power = np.linspace(10, 30, 11)
    #rated_power = np.linspace(10, 15, 2)
    #rated_power = np.linspace(22,30,5)
    rated_power = rated_power.tolist()

    # [P,D] = np.meshgrid(rated_power,dia)
    # lcoe_matrix = np.zeros(np.shape(P))

    d = dia[12]
    idx = dia.index(d)
    area_values = area_database[idx] #list of area values for a given value of radius
    area_values = area_values[area_values != 0]
    a_const = a_const*1.03 #Area constraint in km2 with 3 % margin
    vals = area_values[area_values<a_const]
    loc = np.where(area_values == vals[-1]) #location of largest possible area below the constraint
    idx_nt = loc[0][0] #location of number of turbines permitted
    N_t = n_t[idx_nt] #Number of turbines permitted within the area
    lcoe_dia = []

    for p in rated_power:
        idx_power = rated_power.index(p)
        value_power = p
        value_rad = d/2
        lcoe = run_main_script(value_rad, value_power, N_t)
        old_filename = 'parameters.csv'
        new_filename = 'parameters_' + str(value_power) + '_' + str(value_rad * 2) + '_' + str(N_t) + '.csv'
        os.rename(old_filename, new_filename)
        lcoe_dia.append(lcoe*10) #lcoe values for a given diameter and all power values
       #lcoe_matrix[idx][idx_power] = lcoe

    #print(lcoe_dia)
    data = {str(d): lcoe_dia}
    import csv
    if idx == 0:
        with open('lcoe_matrix.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value])
        csvfile.close()
    else:
        with open('lcoe_matrix.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value])
        csvfile.close()



fixed_area(250)



