'''
Takes a future year as an input and determines the installed wind capacity and load
for that particular year. Also returns ratio of future year capacity to base year capacity
'''

import numpy as np

def capacity(future_year):

    base_year = 2019

    year_wind = np.array([2015,2016,2017,2018,2019,2020, 2030]) # sample years
    onshore_wind = np.array([2646, 3284, 3479, 3675, 3669, 3973, 8000]) # onshore installed capacity
    offshore_wind = np.array([228, 357, 638, 957, 957, 1709, 11500]) # offshore installed capacity
    tot_wind = np.add(onshore_wind, offshore_wind) # total installed capacity

    coeff = np.polyfit(year_wind, tot_wind, 2) # fit a second degree polynomial

    p = np.poly1d(coeff) # p can be used as a function to return the capacity for a given year

    wind_future_capacity = p(future_year)

    idx = (np.abs(year_wind - base_year)).argmin()

    ratio_wind = wind_future_capacity/tot_wind[idx]

    load_increase = 0.02 # a 2% increase in load every year
    ratio_load =  (1 + load_increase)**(future_year - base_year)

    return ratio_wind, ratio_load
