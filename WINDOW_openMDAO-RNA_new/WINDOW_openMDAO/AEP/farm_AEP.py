from openmdao.api import ExplicitComponent
import numpy as np
from scipy import interpolate
from scipy.stats import weibull_min
import csv
import pandas as pd
import ast
import matplotlib.pyplot as plt
import collections
from .directional_weibull import directional_weibull



class FarmAEP(ExplicitComponent):
    '''
    This class runs Py_Wake (https://topfarm.pages.windenergy.dtu.dk/PyWake/) for the given site and turbine,
    and returns wake losses, hourly farm power, and the AEP.
    '''


    def __init__(self, n_layout, wind_file, ct_file, power_file, direction_sampling_angle, time_resolution):
        super(FarmAEP, self).__init__()
        self.n_layout = n_layout
        self.time_resolution = time_resolution
        self.wind_file = wind_file
        self.ct_file = ct_file
        self.power_file = power_file
        self.direction_sampling_angle = direction_sampling_angle


    def setup(self):


        self.add_input('x_coord', desc='New scaled x coordinates of the turbines in the farm', shape=(self.n_layout,1))
        self.add_input('y_coord', desc='New scaled y coordinates of the turbines in the farm', shape=(self.n_layout,1))

        self.add_input('hub_height', val=0.0)
        self.add_input('rated_power', val=0.0)
        self.add_input('rotor_diameter', val=0.0)

        self.add_output('max_TI', shape = self.n_layout, desc='Maximum local turbulence intensity')
        self.add_output('farm_power', shape = self.time_resolution)
        self.add_output('farm_AEP', val=0.0)


    def compute(self, inputs, outputs):

        wind_file = self.wind_file
        ct_file = self.ct_file
        power_file = self.power_file
        n_t = self.n_layout #number of turbines
        direction_sampling_angle = self.direction_sampling_angle


        x_coord = inputs['x_coord']
        y_coord = inputs['y_coord']

        x_coord = [item for sublist in x_coord for item in sublist] #make it one flat list
        y_coord = [item for sublist in y_coord for item in sublist] #make it one flat list

        hub_height = inputs['hub_height']
        rated_power = inputs['rated_power']*1e3 #convert to W
        rotor_diameter = inputs['rotor_diameter']


        ws_wd = pd.read_csv(wind_file)
        wind_speed_100 = ws_wd['wind_speed']
        wind_direction = ws_wd['wind_direction']


        wind_speed_hh = [] #wind speed at hub height
        for v in wind_speed_100:
            wind_speed_hh.append(float(v * (hub_height / 100.0) ** 0.11))  # power law to extrapolate wind speed to hub height

        #print 'mean wind speed', np.mean(wind_speed)


        shape_fac, scale_fac, prob = directional_weibull(wind_direction, direction_sampling_angle, wind_speed_hh) #fit a weibull curve for each wind direction


        def run_pywake(shape_fac, scale_fac, prob):
            from py_wake import NOJ, BastankhahGaussian, IEA37SimpleBastankhahGaussian, flow_map
            from py_wake.deficit_models import TurboGaussianDeficit
            from py_wake.wind_turbines.power_ct_functions import PowerCtFunctionList, PowerCtTabular
            from py_wake.site import XRSite
            from py_wake.wind_turbines import WindTurbine
            from py_wake.turbulence_models import STF2017TurbulenceModel
            from py_wake.site.shear import PowerShear
            import xarray as xr

            f = prob
            A = scale_fac
            k = shape_fac
            wd = np.linspace(0, 360, len(f), endpoint=False) #wind directions
            ti = .1 #turbulence intensity
            x_i = x_coord
            y_i = y_coord


            site = XRSite(
                ds=xr.Dataset(
                    data_vars={'Sector_frequency': ('wd', f), 'Weibull_A': ('wd', A), 'Weibull_k': ('wd', k), 'TI': ti},
                    coords={'wd': wd}), initial_position=np.array([x_i, y_i]).T)  # Use weibull parameters only to define site
            x, y = site.initial_position.T



            ct_data = pd.read_csv(ct_file, delimiter='\t', header=None)
            power_data = pd.read_csv(power_file, delimiter='\t', header=None)
            u = ct_data[:][0]
            ct = ct_data[:][1]
            power = power_data[:][1]

            ref_windturbine = WindTurbine(name='turbine',
                                          diameter=rotor_diameter[0],
                                          hub_height=hub_height[0],
                                          powerCtFunction=PowerCtTabular(u, power, 'W', ct))

            ref_windturbine.powerCtFunction = PowerCtFunctionList(
                key='operating',
                powerCtFunction_lst=[PowerCtTabular(ws=u, power=power, power_unit='w', ct=ct),
                                     WindTurbine(name='turbine',
                                                 diameter=rotor_diameter[0],
                                                 hub_height=hub_height[0],
                                                 powerCtFunction=PowerCtTabular(u, power, 'W', ct)).powerCtFunction],
                # 1=Normal operation
                default_value=1)


            ###### TIME SERIES APPROACH #####
            ws = np.array(wind_speed_hh)
            wd = np.array(wind_direction)
            dir = wd[859]
            speed = ws[859]
            ti = 0.1 + np.zeros(len(ws)) #turbulence intensity vector with a constant value
            time_stamp = np.arange(len(ws))
            operating = np.ones((len(x), len(time_stamp))) #operating condition of each turbine

            wf_model = BastankhahGaussian(site, ref_windturbine, turbulenceModel=STF2017TurbulenceModel())
            sim_res_time = wf_model(x, y,  # wind turbine positions
                                    wd=wd,  # Wind direction time series
                                    ws=ws,  # Wind speed time series
                                    time=time_stamp,  # time stamps
                                    TI=ti,  # turbulence intensity time series
                                    operating=operating  # time dependent operating variable
                                    )

            #print("Total AEP using time series: %f GWh" % sim_res_time.aep().sum())

            # _ = site.plot_wd_distribution(n_wd=12, ws_bins=[0,5,10,15,20,25])
            # plt.show()

            aep_with_wake_loss = sim_res_time.aep().sum().data
            aep_without_wake_loss = sim_res_time.aep(with_wake_loss=False).sum().data
            wake_losses = (aep_without_wake_loss - aep_with_wake_loss) / aep_without_wake_loss

            ti_eff = sim_res_time.TI_eff.values
            max_ti_eff = np.max(ti_eff, axis=1) #maximum of each turbine
            #print(np.max(ti_eff))

            # with open('ti.csv', 'w') as file:
            #     writer = csv.writer(file)
            #     for idx in range(len(ti_eff)):
            #         writer.writerow(ti_eff[idx])
            # file.close()


            farm_power_output = np.sum(sim_res_time.Power.values, axis=0)/ 1e6 #Hourly farm power in MW

            return max_ti_eff, wake_losses, farm_power_output, aep_with_wake_loss, aep_without_wake_loss




        max_ti_eff, wake_losses, farm_power_ts, aep_with_wake, aep_without_wake = run_pywake(shape_fac, scale_fac, prob)
        #cf = sum(farm_power_ts)/(8760*74*5)

        #df = pd.DataFrame(farm_power_ts)
        #df.to_csv('farm_power_75_10min.csv')

        outputs['max_TI'] = max_ti_eff
        outputs['farm_power'] = farm_power_ts # in MW
        outputs['farm_AEP'] = sum(farm_power_ts)*1e6  # in Wh


        field_names = ['v_mean','n_t','aep_noloss', 'aep_withwake', 'wake_losses']
        description = ['Mean wind speed at hub height',  'Number of turbines', 'Annual energy production without wakes (GWh)', 'Annual energy production with wake losses (GWh)', 'Wake losses']
        data = {field_names[0]: [np.mean(wind_speed_hh), description[0]], field_names[1]: [n_t, description[1]],field_names[2]:[aep_without_wake, description[2]], field_names[3]:[outputs['farm_AEP'][0]/1e9, description[3]], field_names[4]:[wake_losses, description[4]]}
        with open('parameters.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in list(data.items()):
                writer.writerow([key, value[0], value[1]])
        csvfile.close()


