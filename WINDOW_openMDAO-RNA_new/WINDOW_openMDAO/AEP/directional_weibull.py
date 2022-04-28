
import collections
import numpy as np
from scipy.stats import weibull_min

def directional_weibull(wind_direction, direction_sampling_angle, wind_speed_hh):
    num_wind_bins = 360 / direction_sampling_angle
    wind_bin_edges = np.linspace(0, 360, int(num_wind_bins), endpoint=False)
    bin_allocation = []
    corresponding_bin = []
    ws_array_perwd = collections.defaultdict(
        list)  # make an empty dictionary where wind speed array for each wind direction will be stored

    for idx in range(len(wind_direction)):
        bin_allocation.append(
            divmod(int(wind_direction[idx]), int(direction_sampling_angle))[0])  # take only quotient of the division
        if bin_allocation[idx] == num_wind_bins:
            bin_allocation[idx] = bin_allocation[
                                      idx] - 1  # As indexing starts from 0, last bin number would be num_wind_bins - 1
        dir = int(wind_bin_edges[bin_allocation[idx]])
        corresponding_bin.append(dir)  # corresponding wind direction bin between 0 and 360
        ws_array_perwd[str(dir)].append(
            wind_speed_hh[idx])  # add respective wind speed to the list of the given wind direction

    shape_fac = []
    scale_fac = []
    prob = []
    for idx in range(len(wind_bin_edges)):  # loop through different wind directions
        data = ws_array_perwd[str(int(wind_bin_edges[idx]))]  # access wind speed data for that given wind direction
        shape, loc, scale = weibull_min.fit(data, floc=0)  # weibull fit
        shape_fac.append(shape)  # directional shape factor
        scale_fac.append(scale)  # directional scale factor
        prob.append(len(ws_array_perwd[str(int(wind_bin_edges[idx]))]) / len(
            wind_speed_hh))  # directional probability of occurence

    return shape_fac, scale_fac, prob