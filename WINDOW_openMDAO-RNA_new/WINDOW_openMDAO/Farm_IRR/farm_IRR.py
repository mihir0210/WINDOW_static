from openmdao.api import ExplicitComponent
from time import clock
from numpy import genfromtxt
import numpy as np
import scipy
import csv
import pandas as pd
import ast



class FarmIRR(ExplicitComponent):

    def initialize(self):

        # fixed parameters
        self.metadata.declare('wind_file', desc='wind speed and direction data file')
        self.metadata.declare('spot_price_file', desc ='Spot price data file')


    def setup(self):


        #self.add_input('elec_power_bin', shape=31)
        #self.add_input('weibull_scale', val=2.11)
        #self.add_input('weibull_shape', val=8.15)

        self.add_input('investment_costs', val=0.0)
        self.add_input('decommissioning_costs', val=0.0)
        self.add_input('transm_electrical_efficiency', val=0.0)
        self.add_input('operational_lifetime', val=0.0)
        self.add_input('interest_rate', val=0.0)

        '''
        self.add_input('cut_in_speed', units='m/s', desc='cut-in wind speed')
        self.add_input('rated_wind_speed', units='m/s', desc='rated wind speed')
        self.add_input('cut_out_speed', units='m/s', desc='cut-out wind speed')
        self.add_input('swept_area', units='m**2', desc='rotor swept area')
        self.add_input('machine_rating', units='kW', desc='machine rating')
        self.add_input('drive_train_efficiency', desc='efficiency of aerodynamic to electrical conversion')
        self.add_input('rotor_cp', desc='rotor power coefficient')
        '''


        self.add_output('IRR', val=0.0)
        self.add_output('ramp_90', val=0.0)

        #self.declare_partals(of='LCOE', wrt=['investment_costs', 'oandm_costs', 'decommissioning_costs', 'AEP', 'transm_electrical_efficiency', 'operational_lifetime', 'interest_rate'], method='fd')

    def compute(self, inputs, outputs):
        with open('farm_pc_directional.csv', mode='r') as infile:
            reader = csv.reader(infile)
            dict_farm_power = dict(reader)

        for key in dict_farm_power.keys():
            dict_farm_power[key] = ast.literal_eval(dict_farm_power[key]) #remove string from list

        wind_file = self.metadata['wind_file']
        spot_price_file = self.metadata['spot_price_file']

        wind_file = pd.read_csv(wind_file)

        wind_speed = np.array(wind_file['wind_speed'])
        wind_direction = np.array(wind_file['wind_direction'])






#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":
    #from WINDOW_openMDAO.src.api import beautify_dict
    import matplotlib.pyplot as plt

    ###################################################
    ############### Model Execution ###################
    ###################################################
    inputs = {'investment_costs': 10000000.0, \
              'decommissioning_costs': 6000000.0, \
              'transm_electrical_efficiency': 0.95, \
              'operational_lifetime': [25], \
              'interest_rate': 0.075
                            }
    outputs = {}


    model = FarmIRR(wind_file='NL_2019_100m_hourly_ERA5_highwind_withdir.csv', spot_price_file='NL_spot_price_2019.csv')

    model.compute(inputs, outputs)