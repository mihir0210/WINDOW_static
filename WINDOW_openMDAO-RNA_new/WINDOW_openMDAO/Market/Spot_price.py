'''
Takes ratio of future year capacity to base year capacity and gives the time series of spot price for that year
A linear approximation of the market model was made w.r.t wind generation, load, hour of the day, and month of the year
using a robust fit. As only the wind generation and load will change in the future, the spot price for a future year
can be calculated using the same model with new values of wind and load forecasts.
Ratio wind is wind installed capacity in future year / wind installed capacity in 2019
Ratio load is load in future year / load in 2019
'''

import numpy as np
import pandas as pd


def spot_price(ratio_wind, ratio_load):

    #base_year = 2019  The model was trained using data for 2019

    coeff = pd.read_csv('Input/Spot_model_coeffs.csv')
    data = pd.read_csv('Input/Spot_model_data.csv')

    constant = np.array(coeff['constant'])
    wind_coeff = np.array(coeff['wind generation coeff'])
    load_coeff = np.array(coeff['load coeff'])

    wind_forecast = np.array(data['Wind forecast'])
    load_forecast = np.array(data['Load forecast'])
    hour_contribution = np.array(data['Hour contribution'])
    month_contribution = np.array(data['Month contribution'])

    spot_price_future = constant + wind_coeff*wind_forecast*ratio_wind + load_coeff*load_forecast*ratio_load # + hour_contribution + month_contribution

    return spot_price_future
