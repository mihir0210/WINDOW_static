'''
This function returns the efficiency of the alkaline system depending on input load
The efficiency is in the form of kWh needed per kg of hydrogen
'''

import scipy
from scipy.interpolate import interp1d

def alkaline_efficiency(input_load, str):

    if str == 'variable':

        #Alkaline has two regions: 0 - 30 % and 30-100 %

        #### Region 1: 0- 30 % ####
        x1 = [0, 15, 20, 25, 30] # Input load in %
        y1 = [1000, 95, 75, 60, 50] # Energy consumed in kWh

        f1 = interp1d(x1,y1)

        '''
        However, the controller can choose to operate only a few electrolysers
        at 30 % load instead of dividing the farm power across all electrolysers.
        Hence, the assumption is that as long as farm power is 30 % of electrolyser rated,
        the electrolyser can always operate at 30 % input load
        '''

        #### Region 2: 30 - 100 % ####

        x2 = [30, 35, 50, 65, 80, 100]
        y2 = [50, 52, 58, 64, 69, 77]

        f2 = interp1d(x2,y2)

        if input_load<=30:
            #E_consumption = f1(input_load)
            E_consumption = y1[-1]


        elif input_load>30:
            E_consumption = f2(input_load)

    elif str == 'constant':
        E_consumption_volume = 4.4 #kWh per Nm3 of Hydrogen production
        E_consumption = E_consumption_volume/0.09 #Converting to kWh required per kg of Hydrogen production

    return E_consumption


def pemdecentralized_efficiency(input_load, str):

    if str == 'variable':

        #Pem has two regions: 0 - 30 % and 30-100 %

        #### Region 1: 0- 30 % ####
        x1 = [0, 15, 20, 25, 30] # Input load in %
        y1 = [1000, 95, 75, 60, 47] # Energy consumed in kWh

        f1 = interp1d(x1,y1)

        '''
        However, the controller can choose to operate only a few electrolysers
        at 30 % load instead of dividing the farm power across all electrolysers.
        Hence, the assumption is that as long as farm power is 30 % of electrolyser rated,
        the electrolyser can always operate at 30 % input load
        '''

        #### Region 2: 30 - 100 % ####

        x2 = [30, 35, 50, 65, 80, 90, 100]
        y2 = [47, 48, 53, 57, 61, 64, 67]

        f2 = interp1d(x2,y2)

        if input_load<=30:
            #E_consumption = f1(input_load)
            E_consumption = y1[-1]


        elif input_load>30:
            E_consumption = f2(input_load)

    elif str == 'constant':
        E_consumption_volume = 4.9 #kWh per Nm3 of Hydrogen production
        E_consumption = E_consumption_volume/0.09 #Converting to kWh required per kg of Hydrogen production

    return E_consumption
