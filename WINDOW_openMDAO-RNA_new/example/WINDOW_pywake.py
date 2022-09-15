import py_wake
from py_wake import NOJ, BastankhahGaussian, IEA37SimpleBastankhahGaussian, flow_map

from py_wake.site import XRSite
from py_wake.site.shear import PowerShear
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from py_wake.utils import weibull
from numpy import newaxis as na

f = [5.1,4.3, 4.3, 6.6, 8.9, 6.5, 8.7, 11.5, 12, 11.1, 11.4, 9.6]
f = [f/100 for f in f]
A = [8.65, 8.86, 8.15, 9.98, 11.35, 10.96, 11.28, 11.5, 11.08, 10.94, 11.27, 10.55]
k = [2.11, 2.05, 2.35, 2.55, 2.81, 2.74, 2.63, 2.4, 2.23, 2.28, 2.29, 2.28]
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


from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
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

noj = NOJ(site, ref_windturbine)
simulationResult = noj(x,y)


print ("Total AEP using NOJ: %f GWh"%simulationResult.aep().sum())
# simulationResult.aep()

aep_with_wake_loss = simulationResult.aep().sum().data
aep_witout_wake_loss = simulationResult.aep(with_wake_loss=False).sum().data
wake_losses = (aep_witout_wake_loss-aep_with_wake_loss) / aep_witout_wake_loss

print('Wake losses using NOJ=', wake_losses)


bastan = BastankhahGaussian(site,ref_windturbine)
simulationResult = bastan(x,y)


print ("Total AEP using BastankhahGaussian: %f GWh"%simulationResult.aep().sum())
# simulationResult.aep()

aep_with_wake_loss = simulationResult.aep().sum().data
aep_witout_wake_loss = simulationResult.aep(with_wake_loss=False).sum().data
wake_losses = (aep_witout_wake_loss-aep_with_wake_loss) / aep_witout_wake_loss

print('Wake losses using BastankhahGaussian=', wake_losses)



ieabastan = IEA37SimpleBastankhahGaussian(site,ref_windturbine)
simulationResult = ieabastan(x,y)

print ("Total AEP using IEA BastankhahGaussian: %f GWh"%simulationResult.aep().sum())
# simulationResult.aep()

aep_with_wake_loss = simulationResult.aep().sum().data
aep_witout_wake_loss = simulationResult.aep(with_wake_loss=False).sum().data
wake_losses = (aep_witout_wake_loss-aep_with_wake_loss) / aep_witout_wake_loss

print('Wake losses using IEA BastankhahGaussian=', wake_losses)
#
# flow = simulationResult.flow_map()
# flow.FlowMap.plot_aep_map(levels=100, cmap=None, plot_colorbar=True, plot_windturbines=True, normalize_with=1, ax=None)


from py_wake import HorizontalGrid
for grid in [None, # defaults to HorizontalGrid(resolution=500, extend=0.2)
             HorizontalGrid(x=None, y=None, resolution=100, extend=1), # custom resolution and extend
             HorizontalGrid(x = np.arange(482000,500000,100),
                            y = np.arange(5.724e6,5.74e6,100)) # custom x and y
            ]:

    plt.figure()
    simulationResult.flow_map(grid=grid, # defaults to HorizontalGrid(resolution=500, extend=0.2), see below
                            wd=210,
                            ws=10).plot_wake_map()
    plt.xlabel('Easting [$10^5$ m]')
    plt.xticks([485000, 490000, 495000, 500000],['4.85', '4.9', '4.95', '5'])
    plt.ylabel('Northing [$10^6$ m]')
    plt.yticks([5.725e6, 5.73e6, 5.735e6, 5.74e6], ['5.725', '5.73', '5.735', '5.74'])
    plt.ylim([5.7250e6, 5.74e6])
    plt.show()

# flow_map.plot_wake_map()
# plt.ylim([5.7250e6, 5.74e6])
#
# plt.show()