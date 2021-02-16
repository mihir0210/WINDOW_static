'''

Takes the slope, constant, and wind speed value as an input to return time series of spot price
based on a simple linear equation (y = mx + c) where x is the wind speed time series

'''




def spot_price(wind_speed, slope, constant):


    m = slope
    c = constant

    spot_price_ts = [m*x + c for x in wind_speed]

    return spot_price_ts