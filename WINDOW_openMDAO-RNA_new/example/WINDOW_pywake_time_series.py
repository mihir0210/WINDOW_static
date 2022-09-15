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

###### TRY TIME SERIES ####

f = [0.05468036529680365, 0.07054794520547945, 0.06529680365296804, 0.0639269406392694, 0.05251141552511415, 0.0613013698630137, 0.09817351598173515, 0.21141552511415526, 0.12659817351598174, 0.07294520547945206, 0.06757990867579909, 0.05502283105022831]
A = [7.97598824292, 8.895343617819092, 8.040400979156388, 8.754263642500261, 8.19442600045026, 10.226991643666453, 11.36612257509728, 12.800107552391886, 11.62311498472577, 11.213500809393757, 10.076845014037533, 10.22919976349926]
k = [2.5719462157424857, 2.5010984134615803, 2.6592331426836946, 2.5795714298239445, 2.0943899073778756, 2.367448307385878, 2.4598425725613566, 2.6151448972081908, 2.41997559154084, 1.9715859991758635, 2.0668204884992294, 2.3240268789376666]
wd = np.linspace(0, 360, len(f), endpoint=False)
ti = .1


## Set turbine positions
df = pd.read_csv('Input/Rectangular_layout_70turbines_7D.dat', delimiter=' ')
x_i = []
y_i = []
for idx in range(len(df['x'])):
    x_i.append(df['x'][idx])
    y_i.append(df['y'][idx])
x_i_array = np.array(x_i)
y_i_array = np.array(y_i)

site = XRSite(
    ds=xr.Dataset(data_vars={'Sector_frequency': ('wd', f), 'Weibull_A': ('wd', A), 'Weibull_k': ('wd', k), 'TI': ti},
                  coords={'wd': wd}),initial_position= np.array([x_i, y_i]).T)


x, y = site.initial_position.T

from py_wake.wind_turbines import WindTurbine
ct_data = pd.read_csv('Input/ct_rna.dat', delimiter='\t', header=None)
power_data = pd.read_csv('Input/power_rna.dat', delimiter='\t', header=None)
u = ct_data[:][0]
ct = ct_data[:][1]
power = power_data[:][1]

ref_windturbine = WindTurbine(name='15MW_turbine',
                    diameter=240,
                    hub_height=150,
                    powerCtFunction=PowerCtTabular(u,power,'W',ct))

ref_windturbine.powerCtFunction = PowerCtFunctionList(
    key='operating',
    powerCtFunction_lst=[PowerCtTabular(ws=u, power=power, power_unit='w', ct=ct), WindTurbine(name='15MW_turbine',
                    diameter=240,
                    hub_height=150,
                    powerCtFunction=PowerCtTabular(u,power,'W',ct)).powerCtFunction], # 1=Normal operation
    default_value=1)

ws_wd = pd.read_csv('Input/NorthSea_2019_100m_hourly_ERA5_withdir.csv')
ws = ws_wd['wind_speed']
wd = ws_wd['wind_direction']
ws = np.array(ws)*(150/100)**0.11
wd = np.array(wd)
ti = 0.1 + np.zeros(len(ws))

time_stamp = np.arange(len(ws))
operating = np.ones((len(x), len(time_stamp)))


wf_model = IEA37SimpleBastankhahGaussian(site, ref_windturbine)
sim_res_time = wf_model(x, y, # wind turbine positions
                        wd=wd, # Wind direction time series
                        ws=ws, # Wind speed time series
                        time=time_stamp, # time stamps
                        TI=ti, # turbulence intensity time series
                        operating=operating # time dependent operating variable
                  )

print("Total AEP using time series: %f GWh"%sim_res_time.aep().sum())

aep_with_wake_loss = sim_res_time.aep().sum().data
aep_without_wake_loss = sim_res_time.aep(with_wake_loss=False).sum().data
wake_losses = (aep_without_wake_loss-aep_with_wake_loss) / aep_without_wake_loss

print('Wake losses using time series=', wake_losses)


farm_power = np.sum(sim_res_time.Power.values, axis=0)/1e6
# type(farm_power)
print('farm power =', farm_power)
print(sum(farm_power))


# print(sum(sim_res_time.Power[0][:]))

