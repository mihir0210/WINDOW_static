import pandas as pd
from openmdao.api import ExplicitComponent
from WINDOW_openMDAO.input_params import max_n_turbines

from WINDOW_openMDAO.AEP.FastAEP.call_aep_workflow_once import call_aep

import csv


class AEPFast(ExplicitComponent):
    def __init__(self, wake_model, turbulence_model, merge_model, artif_angles, nbins, windrose_file, power_curve_file,
                 ct_curve_file):
        super(AEPFast, self).__init__()
        self.artif_angles = artif_angles
        self.nbins = nbins
        self.windrose_file = windrose_file
        self.power_curve_file = power_curve_file
        self.ct_curve_file = ct_curve_file
        self.wake_model = wake_model
        self.turbulence_model = turbulence_model
        self.merge_model = merge_model

    def setup(self):
        self.add_input("layout", shape=(max_n_turbines, 2))
        self.add_input("n_turbines", val=0)
        self.add_input('machine_rating', units='W', desc='machine rating', val=5e6)
        self.add_input('turbine_radius', val=63.0)
        self.add_input('cut_in_speed', units = 'm/s', desc = 'cut-in wind speed', val=4)
        self.add_input('cut_out_speed', units = 'm/s', desc = 'cut-out wind speed', val=25)
        self.add_input('rated_wind_speed', units = 'm/s', desc = 'rated wind speed', val=11.4)       
        
        
        self.add_output("AEP", val=0.0)
        self.add_output("max_TI", shape=max_n_turbines)
        self.add_output("efficiency", val=0.0)


    def compute(self, inputs, outputs):
        n_turbines = int(inputs["n_turbines"])
        layout = inputs["layout"][:n_turbines]
        # layout = []
        # for t in layout2:
        #     if t[0] >= 0.0 and t[1] >= 0.0:
        #         layout.append(t)
        diff = max_n_turbines - len(layout)
        AEP, max_TI, efficiency, dict_farm_power = fun_aep_fast(self.wake_model, self.turbulence_model, self.merge_model,
                                               self.power_curve_file, self.ct_curve_file, self.windrose_file, layout,
                                               self.nbins, self.artif_angles, \
                                               inputs['cut_in_speed'], \
                                               inputs['cut_out_speed'], \
                                               inputs['rated_wind_speed'], \
                                               inputs['turbine_radius'], \
                                               inputs['machine_rating'])
        max_TI += [0.0 for _ in range(diff)]
        outputs['AEP'], outputs['max_TI'], outputs['efficiency'] = AEP, max_TI, efficiency
        #print 'Efficiency:', efficiency
        #print dict_farm_power['60']



        # Write farm power dictionary to a dataframe and then to a csv file
        df = pd.DataFrame.from_dict(dict_farm_power, orient='index')
        df.to_csv("farm_pc_directional.csv")






        # outputs['AEP'] = 2710828306070.0
        #print 'AEP Done'

def fun_aep_fast(wake_model, turbulence_model, merge_model, power_curve_file, ct_curve_file, windrose_file, layout,
                 nbins, artif_angle, cutin, cutout, rated_wind, rotor_radius, rated_power):

    return call_aep(wake_model, turbulence_model, merge_model, power_curve_file, ct_curve_file, windrose_file, layout,
                    nbins, artif_angle, cutin, cutout, rated_wind, rotor_radius, rated_power)
