'''
Takes a future year as an input and determines the installed wind capacity and load
for that particular year. Also returns ratio of future year capacity to base year capacity
'''

import numpy as np
import pandas as pd

class Capacity:

    def __init__(self, future_year):
        self.future_year = future_year
        self.base_year = 2019


    def ref_gen_scenario(self):

        # A scenario where wind generation increases linearly

        data = pd.read_csv('Input/reference_gen_scenario.csv')
        year_wind = np.array(data['Year']) # sample years
        onshore_wind = np.array(data['Onshore wind']) # onshore installed capacity
        offshore_wind = np.array(data['Offshore wind']) # offshore installed capacity
        tot_wind = np.add(onshore_wind, offshore_wind) # total installed capacity

        coeff = np.polyfit(year_wind, tot_wind, 1) # linear fit

        p = np.poly1d(coeff) # p can be used as a function to return the capacity for a given year

        wind_future_capacity = p(self.future_year)

        idx = (np.abs(year_wind - self.base_year)).argmin()

        ratio_wind = wind_future_capacity/tot_wind[idx]

        load_increase = 0.015 # a 1.5 % increase in load every year
        ratio_load =  (1 + load_increase)**(self.future_year - self.base_year)

        return ratio_wind, ratio_load

    def amb_gen_scenario(self):
        # A scenario where wind generation meets ambitious government targets

        data = pd.read_csv('Input/ambitious_gen_scenario.csv')
        year_wind = np.array(data['Year']) # sample years
        onshore_wind = np.array(data['Onshore wind']) # onshore installed capacity
        offshore_wind = np.array(data['Offshore wind']) # offshore installed capacity
        tot_wind = np.add(onshore_wind, offshore_wind) # total installed capacity

        coeff = np.polyfit(year_wind, tot_wind, 2) # Second order fit

        p = np.poly1d(coeff) # p can be used as a function to return the capacity for a given year

        wind_future_capacity = p(self.future_year)

        idx = (np.abs(year_wind - self.base_year)).argmin()

        ratio_wind = wind_future_capacity/tot_wind[idx]

        load_increase = 0.015 # a 1.5 % increase in load every year
        ratio_load =  (1 + load_increase)**(self.future_year - self.base_year)

        return ratio_wind, ratio_load





