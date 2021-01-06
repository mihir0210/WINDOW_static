from openmdao.api import ExplicitComponent
from WINDOW_openMDAO.Market.capacity_trend import Capacity
from WINDOW_openMDAO.Market.Spot_price import spot_price



import numpy as np
from scipy import interpolate
import csv
import pandas as pd
import ast
import matplotlib.pyplot as plt




class FarmIRR(ExplicitComponent):
    '''
    This class calculates the farm IRR based on the farm power production, spot price, and costs.
    Farm power production at each time instant is based on the time series data for wind speed and direction.
    The power curve data points for each wind direction is imported via a csv. A curve will be fit to each of these
    power curves. For each time instant(for a given wind speed and direction), the farm power can then be extracted.
    '''


    def initialize(self):

        # fixed parameters

        self.metadata.declare('spot_price_file', desc ='Spot price data file')
        self.metadata.declare('time_resolution', desc='length of time series data')



    def setup(self):

        time_points = self.metadata['time_resolution']



        self.add_input('farm_power', shape = time_points)
        self.add_input('investment_costs', val=0.0)
        self.add_input('decommissioning_costs', val=0.0)
        self.add_input('transm_electrical_efficiency', val=0.0)
        self.add_input('operational_lifetime', val=0.0)
        self.add_input('oandm_costs', val=0.0)
        #self.add_input('interest_rate', val=0.0)



        self.add_output('IRR', val=0.0)


        #self.add_output('ramp_90', val=0.0)



    def compute(self, inputs, outputs):


        spot_price_file = self.metadata['spot_price_file']
        farm_power = inputs['farm_power']

        transm_electrical_efficiency = inputs['transm_electrical_efficiency']
        investment_costs = inputs['investment_costs']
        decommissioning_costs = inputs['decommissioning_costs']
        operational_lifetime = inputs['operational_lifetime']
        oandm_costs = inputs['oandm_costs']



        def irr_npv():

            revenue = []

            for y in range(int(operational_lifetime)):

                base_year = 2019
                future_year = base_year + y

                capacity = Capacity(future_year)

                [ratio_wind, ratio_load] = capacity.ref_gen_scenario()

                spot_price_ts = spot_price(ratio_wind, ratio_load)

                #spot_price_new = np.ones(len(spot_price_ts))*100

                elec_farm_power = np.multiply(np.array(farm_power), np.array([transm_electrical_efficiency]))

                yearly_revenue = np.sum(np.multiply(elec_farm_power, spot_price_ts))

                #print yearly_revenue

                revenue.append(yearly_revenue - oandm_costs)

            revenue[-1] = revenue[-1] - decommissioning_costs

            cashflows = [-1 * investment_costs[0], revenue]



            output_list = []

            def removeNestings(cashflows):
                for i in cashflows:
                    if type(i) == list:
                        removeNestings(i)
                    else:
                        output_list.append(i)

            removeNestings(cashflows)

            # print output_list

            cashflows = output_list
            print cashflows

            IRR = np.irr(cashflows)

            discount_rate = 0.05
            NPV = np.npv(discount_rate, cashflows)

            return IRR, NPV



        [IRR, NPV] = irr_npv()

        outputs['IRR'] = IRR

        print IRR

        #ramp =  np.ediff1d(elec_farm_power_ts)

        #pd.DataFrame(ramp).to_csv('farm_ramp_95.csv')
        #pd.DataFrame(farm_power_ts).to_csv('farm_power_95.csv')


































#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":
    #from WINDOW_openMDAO.src.api import beautify_dict
    import matplotlib.pyplot as plt

    ###################################################
    ############### Model Execution ###################
    ###################################################
    inputs = {'investment_costs': 10000000.0, \
              'decommissioning_costs': 6000000.0, \
              'oandm_costs': 50000.0,\
              'transm_electrical_efficiency': 0.95, \
              'operational_lifetime': [25], \
              'interest_rate': 0.075
                            }
    outputs = {}


    model = FarmIRR(wind_file='NL_2019_100m_hourly_ERA5_highwind_withdir.csv', spot_price_file='NL_spot_price_2019.csv', direction_sampling_angle = 30.0)

    model.compute(inputs, outputs)