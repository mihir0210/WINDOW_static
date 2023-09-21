'''
This script is used to create the batch of simulations to be run using WINDOW for different values of
rated power and rotor radius. For each combination,
'''
import os
import numpy as np
from IEA_borssele_irregular_new_UC import run_main_script


power_values_farm = [10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 19.23, 20.0, 22.73] #for a 1 GW farm

power_values_600MW = [10.0, 10.53, 11.11, 11.54, 12.0, 12.5, 13.04, 14.29, 15.0, 16.22, 17.14, 18.18, 19.35, 20.0, 22.22]
power_values_800MW = [10.0, 11.11, 12.12, 12.5, 13.11, 13.56, 14.04, 14.55, 15.09, 16.0, 17.02, 18.18, 19.05, 20.0, 22.22]
power_values_1000MW = [10.0, 10.99, 12.05, 12.99, 13.51, 14.08, 14.49, 14.93, 15.62, 16.13, 16.67, 17.24, 18.18, 19.23, 20.0, 22.73]
power_values_1200MW = [10.0, 11.01, 12.0, 13.04, 14.12, 15.0, 15.58, 16.0, 16.67, 17.14, 17.65, 18.18, 18.46, 19.05, 20.0, 22.22]
power_values_1400MW = [10.0, 11.02, 12.07, 13.08, 14.0, 15.05, 16.09, 16.67, 17.07, 17.5, 18.18, 18.67, 19.18, 20.0, 22.22]

def batch():
    ###### Run a batch ######

    vals_power = [power_values_1000MW[15]]
    # vals_power = [power_values_farm[11]]

    #vals_rad = np.linspace(90,150,13)
    vals_rad = [90.0, 95.0, 100.0, 105.0, 215 / 2, 110.0, 222 / 2, 225 / 2, 227 / 2, 115.0, 120.0, 125.0, 130.0,135.0, 140.0, 145.0, 150.0]
    #vals_rad = [215/2, 222/2, 225/2, 227/2]
    #vals_rad = [200/2]


    for val in vals_rad:
        value_rad = val
        for val1 in vals_power:
                value_power = val1
                lcoe = run_main_script(value_rad, value_power)
                #lcoe = run_main_script(value_rad, value_power, NT)
                old_filename = 'parameters.csv'
                new_filename = 'parameters_' + str(value_power) + '_' + str(value_rad*2) + '.csv'
                os.rename(old_filename, new_filename)


def singlecase():
    ##### Run a single case #####
    power_values_farm = [10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 19.23, 20.0, 22.73]
    #power_values_sensitivity_600MW = [10.0, 12.0, 14.29, 16.22, 18.18, 20.0, 22.22]
    #power_values_sensitivity_800MW = [10.0, 12.12, 14.04, 16.0, 18.18, 20.0, 22.22]
    # power_values_sensitivity_1200MW = [10.0, 12.0, 14.12, 16.0, 18.18, 20.0, 22.22]
    value_power = power_values_farm[8]
    # value_power = power_values_sensitivity_1200MW[0]
    value_rad =280/2 #reference rotor radius

    # dict = {'target_IRR':target_IRR}
    # f = open('Input/finance.txt', 'w')
    # f.write(repr(dict) + '\n')
    # f.close()

    run_main_script(value_rad, value_power)
    old_filename = 'parameters.csv'
    new_filename = 'parameters_' + str(value_power) + '_' + str(value_rad*2) + '.csv'
    #new_filename = 'parameters_' + str(value_power) + '_' + str(value_rad * 2) + '_7D' + '.csv'
    os.rename(old_filename, new_filename)

## RUN ##


# batch()
singlecase()

##### Create a lookup table for Diameter vs Number of turbines ####



def fixed_area(a_const):



    dia = [180, 190, 200, 210, 220, 222, 225, 227, 230, 240, 250, 260, 270, 280, 290, 300]

    if a_const == 100:
        n_t = [80, 72, 66, 61, 56, 55, 54, 53, 52, 48, 45, 42, 39, 37, 35, 33]  # for 7D spacing in 100 km2

    elif a_const == 150:
        #n_t = [115, 104, 95, 87, 80, 79, 77, 76, 74, 69, 64, 60, 56, 52, 49, 47]  # for 7D spacing in 150 km2
        n_t = [213, 193, 175, 160, 147, 145, 141, 139, 136, 125, 116, 108, 101, 95, 89, 84] # for 5D spacing in 150 km2

    elif a_const == 200:
        n_t = [150, 135, 123, 113, 104, 102, 99, 98, 96, 89, 82, 77, 72, 67, 63, 60]  # for 7D spacing in 200 km2





    # import pandas as pd
    # area_database = pd.read_csv('area_database.csv', header=None)
    # #area_database = pd.read_excel('area_database_5D.xlsx', header=None)
    # area_database = pd.DataFrame.to_numpy(area_database)

    # rated_power = np.linspace(10, 30, 11)
    #
    # #rated_power = np.linspace(10, 15, 2)
    # #rated_power = np.linspace(22,30,5)
    # rated_power = rated_power.tolist()
    # rated_power = [19.0, 21.0]
    rated_power = [10, 12, 14, 16, 18, 19, 20, 21, 22, 24, 26, 28, 30]

    # [P,D] = np.meshgrid(rated_power,dia)
    # lcoe_matrix = np.zeros(np.shape(P))

    # d = dia[0]
    # idx = dia.index(d)
    # area_values = area_database[idx] #list of area values for a given value of radius
    # area_values = area_values[area_values != 0]
    # a_const = a_const*1.04 #Area constraint in km2 with 3 % margin
    # vals = area_values[area_values<a_const]
    # loc = np.where(area_values == vals[-1]) #location of largest possible area below the constraint
    # idx_nt = loc[0][0] #location of number of turbines permitted
    # N_t = n_t[idx_nt] #Number of turbines permitted within the area
    # lcoe_dia = []


    d = dia[15]
    idx = dia.index(d)
    N_t = n_t[idx] #Number of turbines permitted within the area
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



# fixed_area(150)



