from openmdao.api import ExplicitComponent
from WINDOW_openMDAO.Market.capacity_trend import Capacity
#from WINDOW_openMDAO.Market.Spot_price import spot_price

from WINDOW_openMDAO.Market.spot_vs_windspeed import spot_price
from WINDOW_openMDAO.Market.Parameters import Parameters




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
        self.metadata.declare('wind_file', desc='wind speed and direction data file')
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

        wind_file = self.metadata['wind_file']
        wind_file = pd.read_csv(wind_file)

        wind_speed = wind_file['wind_speed']


        spot_price_file = self.metadata['spot_price_file']
        farm_power = inputs['farm_power']

        transm_electrical_efficiency = inputs['transm_electrical_efficiency']
        investment_costs = inputs['investment_costs']
        decommissioning_costs = inputs['decommissioning_costs']
        operational_lifetime = inputs['operational_lifetime']
        oandm_costs = inputs['oandm_costs']

        print 'O&M:', oandm_costs

        with open('farm_power_89_hourly.csv', 'w') as csvfile:
            a = csv.writer(csvfile, delimiter=',')
            a.writerow(farm_power)



        def irr_npv():

            revenue = []

            for y in range(int(operational_lifetime)):

                base_year = 2019
                future_year = base_year + y

                #capacity = Capacity(future_year)

                #[ratio_wind, ratio_load] = capacity.ref_gen_scenario()

                parameters = Parameters(future_year, operational_lifetime)

                [slope, constant] = parameters.eneco_coeff()

                #print slope, constant

                spot_price_ = spot_price(wind_speed, slope, constant)

                #only for var_slope()

                spot_price_ts = []

                for p in spot_price_:
                    #spot_price_ts.append(p[0])
                    spot_price_ts.append(p)

                #spot_price_ts = np.ones(len(farm_power))*40



                elec_farm_power = np.multiply(farm_power, transm_electrical_efficiency)

                #print 'elec farm power:', elec_farm_power


                yearly_revenue = np.sum(np.multiply(elec_farm_power, spot_price_ts))

                #print 'Mean spot price:', np.mean(spot_price_ts)
                #print 'Yearly revenue:', yearly_revenue




                revenue.append(max(0,yearly_revenue - oandm_costs))

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

            ##### Write your own IRR function ####

            # Checks where NPV switches sign

            rate = np.linspace(-0.15,0.15,200)
            NPV_pxy = []

            for r in rate:
                val = np.npv(r, cashflows)
                NPV_pxy.append(val[0])


            print NPV_pxy

            asign = np.sign(NPV_pxy)
            signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)
            signchange[0] =0

            for idx in range(len(signchange)):
                if signchange[idx]==1:
                    break



            #min_elem = np.amin(NPV_pxy)
            #loc = np.where(NPV_pxy == min_elem)

            loc = idx


            IRR_new = rate[loc]

            print 'IRR_scneario_inbuilt:', IRR
            print 'IRR_scenario:', IRR_new






            return IRR, NPV



        [IRR, NPV] = irr_npv()

        outputs['IRR'] = IRR

        '''

        #print 'IRR_gradslope:', IRR
        #print 'NPV:', NPV

        #ramp =  np.ediff1d(elec_farm_power_ts)

        #pd.DataFrame(ramp).to_csv('farm_ramp_95.csv')
        #pd.DataFrame(farm_power_ts).to_csv('farm_power_95.csv')

        def irr_npv_new():

            revenue = []

            for y in range(int(operational_lifetime)):
                base_year = 2019
                future_year = base_year + y

                # capacity = Capacity(future_year)

                # [ratio_wind, ratio_load] = capacity.ref_gen_scenario()

                parameters = Parameters(future_year, operational_lifetime)

                [slope, constant] = parameters.highest_slope()



                spot_price_ts = spot_price(wind_speed, slope, constant)'''

        '''
                only for var_slope()

                spot_price_ts = []

                for p in spot_price_:
                    spot_price_ts.append(p[0])'''
        '''
                # spot_price_ts = np.ones(len(farm_power))*40

                elec_farm_power = np.multiply(np.array(farm_power), np.array([transm_electrical_efficiency]))

                yearly_revenue = np.sum(np.multiply(elec_farm_power, spot_price_ts))

                revenue.append(max(0,yearly_revenue - oandm_costs))

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
            #print cashflows

            IRR = np.irr(cashflows)

            discount_rate = 0.05
            NPV = np.npv(discount_rate, cashflows)



            print 'IRR_worstslope:', IRR

            return IRR, NPV



        [IRR, NPV] = irr_npv_new()'''































#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":
    #from WINDOW_openMDAO.src.api import beautify_dict
    import matplotlib.pyplot as plt

    import numpy as np

    a = 500*np.ones([1,8760])
    power = a.tolist()

    ###################################################
    ############### Model Execution ###################
    ###################################################
    inputs = {'investment_costs': [3000000000.0], \
              'decommissioning_costs': 6000000.0, \
              'oandm_costs': 50000.0,\
              'transm_electrical_efficiency': 0.95, \
              'operational_lifetime': 25, \
              'farm_power': power,\

                            }
    outputs = {}


    model = FarmIRR(wind_file='NL_2019_100m_hourly_ERA5_highwind_withdir.csv', spot_price_file='NL_spot_price_2019.csv', time_resolution = 8760)

    model.compute(inputs, outputs)