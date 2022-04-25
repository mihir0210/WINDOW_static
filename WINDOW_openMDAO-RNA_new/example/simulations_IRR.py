'''
This script is used to create the batch of simulations to be run using WINDOW for different values of
rated power and rotor radius. For each combination,
'''
import os
from IEA_borssele_irregular_new_UC import run_main_script

def batch():
    ###### Run a batch ######
    val_power = 15
    vals_rad = [110, 115, 120, 125, 130, 135, 140] #rotor radius values
    target_IRR = [0.05, 0.1]

    for targIRR in target_IRR:
        IRR = targIRR
        dict = {'target_IRR': IRR}
        f = open('Input/finance.txt', 'w')
        f.write(repr(dict) + '\n')
        f.close()
        for val in vals_rad:
            value_rad = val
            value_power = val_power
            run_main_script(value_rad, value_power)
            old_filename = 'parameters.csv'
            new_filename = 'parameters_' + 'targetIRR_' + str(IRR*100) + '_' + str(value_power) + '_' + str(value_rad) + '.csv'
            os.rename(old_filename, new_filename)


def singlecase():
    ##### Run a single case #####
    value_power = 15
    value_rad = 125 #reference rotor radius
    target_IRR = 0.1
    dict = {'target_IRR':target_IRR}
    f = open('Input/finance.txt', 'w')
    f.write(repr(dict) + '\n')
    f.close()

    run_main_script(value_rad, value_power)
    # old_filename = 'parameters.csv'
    # new_filename = 'parameters_' + str(value_power) + '_' + str(value_rad) + '.csv'
    # os.rename(old_filename, new_filename)

## RUN ##

batch()


#singlecase()
