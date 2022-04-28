
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import weibull_min, weibull_max
import matplotlib.pyplot as plt


ws_wd = pd.read_csv('Input/NorthSea_2019_100m_hourly_ERA5_withdir.csv')
ws = ws_wd['wind_speed']
wd = ws_wd['wind_direction']
ws = np.array(ws)*(150/100)**0.11
wd = np.array(wd)
sector_angle = 30.0
num_wind_bins = 360/sector_angle
bins = np.linspace(0, 360, int(num_wind_bins), endpoint=False)

bin_allocation = []
corresponding_bin = []

# directional_param = np.zeros(len(bins),3)  #shape, scale, probability
# keys = []
# for val in bins:
#     keys.append(str(int(val)))
# ws_array_perwd = dict.fromkeys(keys)

import collections

ws_array_perwd = collections.defaultdict(list)

for idx in range(len(wd)):
    bin_allocation.append(divmod(int(wd[idx]), int(sector_angle))[0])  # take only quotient of the division
    if bin_allocation[idx] == num_wind_bins:
        bin_allocation[idx] = bin_allocation[idx] - 1  # As indexing starts from 0, last bin number would be num_wind_bins - 1
    dir = int(bins[bin_allocation[idx]])
    corresponding_bin.append(dir)  # corresponding wind direction bin between 0 and 360
    ws_array_perwd[str(dir)].append(ws[idx])

shape_fac = []
scale_fac = []
prob = []
for idx in range(len(bins)):
    data = ws_array_perwd[str(int(bins[idx]))]
    shape, loc, scale = weibull_min.fit(data, floc=0)
    shape_fac.append(shape)
    scale_fac.append(scale)
    prob.append(len(ws_array_perwd[str(int(bins[idx]))])/len(ws))


# print('shape factor =', shape_fac)
# print('scale factor =', scale_fac)
# print('probability=', prob)


# shape, loc, scale = weibull_min.fit(ws, floc=0)


import py_wake
from py_wake import NOJ, BastankhahGaussian, IEA37SimpleBastankhahGaussian, flow_map
from py_wake.wind_turbines.power_ct_functions import PowerCtFunctionList, PowerCtTabular
from py_wake.site import XRSite
from py_wake.site.shear import PowerShear
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from py_wake.utils import weibull
from numpy import newaxis as na

f = prob
A = scale_fac
k = shape_fac
wd = np.linspace(0, 360, len(f), endpoint=False)
ti = .1


## Set turbine positions
df = pd.read_csv('Input/Rectangular_layout_70turbines_7D.dat', delimiter=' ')
x_i = []
y_i = []
for idx in range(70):
    x_i.append(df['x'][idx])
    y_i.append(df['y'][idx])
x_i_array = np.array(x_i)
y_i_array = np.array(y_i)

site = XRSite(
    ds=xr.Dataset(data_vars={'Sector_frequency': ('wd', f), 'Weibull_A': ('wd', A), 'Weibull_k': ('wd', k), 'TI': ti},
                  coords={'wd': wd}),initial_position= np.array([x_i, y_i]).T)

# _ = site.plot_wd_distribution(n_wd=12, ws_bins=[0,5,10,15,20,25])
# # _ = site.plot_ws_distribution(wd=[0,90,180,270])
# plt.show()

from py_wake.wind_turbines import WindTurbine
ct_data = pd.read_csv('Input/ct_rna.dat', delimiter='\t', header=None)
power_data = pd.read_csv('Input/power_rna.dat', delimiter='\t', header=None)
u = ct_data[0:61][0]
ct = ct_data[0:61][1]
power = power_data[0:61][1]

ref_windturbine = WindTurbine(name='15MW_turbine',
                    diameter=240,
                    hub_height=150,
                    powerCtFunction=PowerCtTabular(u,power,'W',ct))

x, y = site.initial_position.T
# windTurbines = V80()
# site=Hornsrev1Site()

_ = site.plot_wd_distribution(n_wd=12, ws_bins=[0,5,10,15,20,25])



wf = IEA37SimpleBastankhahGaussian(site,ref_windturbine)
simulationResult = wf(x,y)

print ("Total AEP: %f GWh"%simulationResult.aep().sum())
# simulationResult.aep()

aep_with_wake_loss = simulationResult.aep().sum().data
aep_witout_wake_loss = simulationResult.aep(with_wake_loss=False).sum().data
wake_losses = (aep_witout_wake_loss-aep_with_wake_loss) / aep_witout_wake_loss

print('Wake losses:', wake_losses)

from py_wake import HorizontalGrid
for grid in [None, # defaults to HorizontalGrid(resolution=500, extend=0.2)
             HorizontalGrid(x=None, y=None, resolution=100, extend=1), # custom resolution and extend
             HorizontalGrid(x = np.arange(-1000,1000,100),
                            y = np.arange(-500,500,100)) # custom x and y
            ]:
    plt.figure()
    simulationResult.flow_map(grid=grid, wd=230, ws=[9]).plot_wake_map()
    plt.show()