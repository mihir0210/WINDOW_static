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
        self.options.declare('wind_file', desc='wind speed and direction data file')
        self.options.declare('direction_sampling_angle', desc='sector angle for windrose')
        self.options.declare('time_resolution', desc='length of time series data')


    def setup(self):

        time_points = self.options['time_resolution']
        self.add_input('hub_height', val=0.0)

        self.add_input('rated_power', val=0.0)
        self.add_input('rotor_diameter', val=0.0)
        self.add_input('n_t', val=0.0)
        self.add_input('Cp', val=0.0)
        self.add_input('rated_ws', val=0.0)

        self.add_output('farm_power', shape = time_points)
        self.add_output('farm_AEP', val=0.0)


    def compute(self, inputs, outputs):

        hub_height = inputs['hub_height']

        rated_power = inputs['rated_power']*1e3 #convert to W
        rotor_diameter = inputs['rotor_diameter']
        n_t = inputs['n_t']
        Cp = inputs['Cp']
        rated_ws = inputs['rated_ws']




        # with open('farm_pc_directional.csv', mode='r') as infile: #file is generated in the AeroAEP module
        #     reader = csv.reader(infile)
        #     dict_farm_power = dict(reader) # has keys for each wind direction and 'Wind speeds'
        #
        #
        # for key in list(dict_farm_power.keys()):
        #     dict_farm_power[key] = ast.literal_eval(dict_farm_power[key]) #remove string from list

        df = pd.read_csv('farm_pc_directional.csv', index_col=0)
        d = df.to_dict("split")
        dict_farm_power = dict(zip(d["index"], d["data"])) #generate list from the dataframe

        wind_file = self.options['wind_file']
        wind_file = pd.read_csv(wind_file)

        wind_speed_100 = np.array(wind_file['wind_speed'])

        wind_speed = []
        for v in wind_speed_100:
            wind_speed.append(v * (hub_height / 100.0) ** 0.11)  # power law to extrapolate wind speed to hub height

        wind_direction = np.array(wind_file['wind_direction'])

        #print 'mean wind speed', np.mean(wind_speed)

        turbine_power = []


        for idx in range(len(wind_speed)):

            if wind_speed[idx] <= 3 or wind_speed[idx] > 25:
                turbine_power.append(0)

            elif wind_speed[idx] >= rated_ws:
                turbine_power.append(rated_power)

            else:
                turbine_power.append(0.5 * Cp * 1.225 * (3.142/4) * rotor_diameter ** 2 * (wind_speed[idx] ** 3) * 0.944)

        turbine_power_ts = [turbine_power / 1e6 for turbine_power in turbine_power]  # convert to MW

        #print 'Farm AEP without losses:', sum(turbine_power_ts)*n_t



        def wind_bin_allocation():


            direction_sampling_angle = self.options['direction_sampling_angle']

            num_wind_bins = int(360/direction_sampling_angle)

            wind_bin_edges = np.linspace(start=0, stop=360 - int(direction_sampling_angle), num=num_wind_bins)

            bin_allocation = []
            corresponding_bin = []

            for idx in range(len(wind_direction)):
                bin_allocation.append(divmod(int(wind_direction[idx]),int(direction_sampling_angle))[0]) #take only quotient of the division
                if bin_allocation[idx] == num_wind_bins:
                    bin_allocation[idx] = bin_allocation[idx] - 1  # As indexing starts from 0, last bin number would be num_wind_bins - 1

                corresponding_bin.append(int(wind_bin_edges[bin_allocation[idx]])) # corresponding wind direction bin between 0 and 360

            # corresponding bin can be used as a key to access the power curve from dict_farm_power for each time instant

            return corresponding_bin




        def get_farm_power():

            farm_power = []  # time series (hourly) of farm power output

            for idx in range(len(wind_direction)):
                data_farm_power = dict_farm_power[str(float(corresponding_bin[idx]))]
                data_wind_speeds = dict_farm_power['Wind speeds']

                max_power = max(data_farm_power)
                a = min(list(range(len(data_farm_power))), key=lambda i: abs(data_farm_power[i] - max_power)) #index of rated farm power
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

        #print 'AEP with wake:',outputs['farm_AEP']

        #print 'wake losses:', (1- sum(farm_power_ts)/(sum(turbine_power_ts)*n_t))

        field_names = ['Mean wind speed','AEP without losses', 'AEP with wake', 'Wake losses']
        data = {field_names[0]: np.mean(wind_speed), field_names[1]:sum(turbine_power_ts)*n_t, field_names[2]:outputs['farm_AEP'], field_names[3]:(1- sum(farm_power_ts)/(sum(turbine_power_ts)*n_t))}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value])
        csvfile.close()


