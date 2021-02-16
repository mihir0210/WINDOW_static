from openmdao.api import ExplicitComponent




import numpy as np
from scipy import interpolate
import csv
import pandas as pd
import ast
import matplotlib.pyplot as plt




class FarmAEP(ExplicitComponent):
    '''
    This class calculates the farm IRR based on the farm power production, spot price, and costs.
    Farm power production at each time instant is based on the time series data for wind speed and direction.
    The power curve data points for each wind direction is imported via a csv. A curve will be fit to each of these
    power curves. For each time instant(for a given wind speed and direction), the farm power can then be extracted.
    '''


    def initialize(self):

        # fixed parameters
        self.metadata.declare('wind_file', desc='wind speed and direction data file')
        self.metadata.declare('direction_sampling_angle', desc='sector angle for windrose')
        self.metadata.declare('time_resolution', desc='length of time series data')


    def setup(self):

        time_points = self.metadata['time_resolution']

        self.add_output('farm_power', shape = time_points)
        self.add_output('farm_AEP', val=0.0)


    def compute(self, inputs, outputs):


        with open('farm_pc_directional.csv', mode='r') as infile: #file is generated in the AeroAEP module
            reader = csv.reader(infile)
            dict_farm_power = dict(reader) # has keys for each wind direction and 'Wind speeds'


        for key in dict_farm_power.keys():
            dict_farm_power[key] = ast.literal_eval(dict_farm_power[key]) #remove string from list

        wind_file = self.metadata['wind_file']


        wind_file = pd.read_csv(wind_file)

        wind_speed = np.array(wind_file['wind_speed'])
        wind_direction = np.array(wind_file['wind_direction'])







        def wind_bin_allocation():


            direction_sampling_angle = self.metadata['direction_sampling_angle']

            num_wind_bins = 360/direction_sampling_angle

            wind_bin_edges = np.linspace(start=0, stop=360 - direction_sampling_angle, num=num_wind_bins)




            bin_allocation = []
            corresponding_bin = []

            for idx in range(len(wind_direction)):
                bin_allocation.append(int(wind_direction[idx])/int(direction_sampling_angle))
                if bin_allocation[idx] == num_wind_bins:
                    bin_allocation[idx] = bin_allocation[idx] - 1  # As indexing starts from 0, last bin number would be num_wind_bins - 1
                corresponding_bin.append(int(wind_bin_edges[bin_allocation[idx]])) # corresponding wind direction bin between 0 and 360

            # corresponding bin can be used as a key to access the power curve from dict_farm_power for each time instant

            return corresponding_bin




        def get_farm_power():

            farm_power = []  # time series (hourly) of farm power output

            for idx in range(len(wind_direction)):
                data_farm_power = dict_farm_power[str(corresponding_bin[idx])]
                data_wind_speeds = dict_farm_power['Wind speeds']

                max_power = max(data_farm_power)
                a = min(range(len(data_farm_power)), key=lambda i: abs(data_farm_power[i] - max_power)) #index of rated farm power
                rated_ws = data_wind_speeds[a] # rated farm wind speed

                # use data until rated wind speed to perform a cubic curve fit

                new_data_farm_power = data_farm_power[:a+1]
                new_data_wind_speeds = data_wind_speeds[:a+1]



                f = interpolate.interp1d(new_data_wind_speeds, new_data_farm_power, kind = 'cubic')

                if wind_speed[idx] <= data_wind_speeds[0] or wind_speed[idx] > data_wind_speeds[-2]:
                    farm_power.append(0)

                elif wind_speed[idx] >= rated_ws:
                    farm_power.append(max(data_farm_power))

                else:
                    farm_power.append(f(wind_speed[idx]))

            farm_power_output = [farm_power/1e6 for farm_power in farm_power] # convert to MW


            return farm_power_output





        corresponding_bin = wind_bin_allocation()

        farm_power_ts = get_farm_power()
        #cf = sum(farm_power_ts)/(8760*74*5)

        #df = pd.DataFrame(farm_power_ts)
        #df.to_csv('farm_power_75_10min.csv')

        outputs['farm_power'] = farm_power_ts # in MW
        outputs['farm_AEP'] = sum(farm_power_ts)*1e6  # in Wh

        print 'AEP IRR module:',outputs['farm_AEP']