from openmdao.api import ExplicitComponent
from time import clock
from numpy import genfromtxt
import numpy as np
import scipy

from scipy import stats
from scipy.stats import norm

class single_turbine(ExplicitComponent):

    def initialize(self):

        # fixed parameters
        self.metadata.declare('wind_speed_file', desc='wind speed data file')
        self.metadata.declare('spot_price_file', desc ='Spot price data file')


    def setup(self):
        self.add_input('elec_power_bin', shape=31)
        self.add_input('weibull_scale', val=2.11)
        self.add_input('weibull_shape', val=8.15)

        self.add_input('investment_costs', val=0.0)
        self.add_input('decommissioning_costs', val=0.0)
        self.add_input('transm_electrical_efficiency', val=0.0)
        self.add_input('operational_lifetime', val=0.0)
        self.add_input('interest_rate', val=0.0)


        self.add_input('cut_in_speed', units='m/s', desc='cut-in wind speed')
        self.add_input('rated_wind_speed', units='m/s', desc='rated wind speed')
        self.add_input('cut_out_speed', units='m/s', desc='cut-out wind speed')
        self.add_input('swept_area', units='m**2', desc='rotor swept area')
        self.add_input('machine_rating', units='kW', desc='machine rating')
        self.add_input('drive_train_efficiency', desc='efficiency of aerodynamic to electrical conversion')
        self.add_input('rotor_cp', desc='rotor power coefficient')


        self.add_output('LCOE', val=0.0)
        self.add_output('IRR', val=0.0)
        self.add_output('ramp_90', val=0.0)

        #self.declare_partals(of='LCOE', wrt=['investment_costs', 'oandm_costs', 'decommissioning_costs', 'AEP', 'transm_electrical_efficiency', 'operational_lifetime', 'interest_rate'], method='fd')

    def compute(self, inputs, outputs):


        wind_speed_file = self.metadata['wind_speed_file']
        spot_price_file = self.metadata['spot_price_file']


        wind_speeds = genfromtxt(wind_speed_file)
        spot_prices = genfromtxt(spot_price_file)



        investment_costs = inputs['investment_costs']
        decommissioning_costs = inputs['decommissioning_costs']
        transm_electrical_efficiency = inputs['transm_electrical_efficiency']
        operational_lifetime = inputs['operational_lifetime'][0]
        interest_rate = inputs['interest_rate']

        cut_in_speed = inputs['cut_in_speed']
        rated_wind_speed = inputs['rated_wind_speed']
        cut_out_speed = inputs['cut_out_speed']
        swept_area = inputs['swept_area']
        machine_rating = inputs['machine_rating']
        eta_dt = inputs['drive_train_efficiency']
        rotor_cp = inputs['rotor_cp']



        '''
        LCoE calculation
        '''


        def weib(U, k, a):
            # U is the range of wind speeds
            # k is the shape parameter
            # a is the scale parameter (higher)
            return (k / a) * (U / a) ** (k - 1) * np.exp(-(U / a) ** k)

        U = np.linspace(start =0, stop=30, num=31)
        k = inputs['weibull_shape']
        a = inputs['weibull_scale']

        pdf = weib(U, k, a )

        elec_power = [i*1000 for i in inputs['elec_power_bin']] #converting to W


        #print pdf
        print elec_power
        print operational_lifetime



        AEP_ = np.multiply(elec_power, pdf)*8760
        AEP = np.sum(AEP_)  # annual energy production

        print AEP

        #oandm_costs = 16.0 * AEP / 1000000.0

        oandm_costs = 70*machine_rating  # 70 euros/kW/year

        #### Make 3  functions for different LCoE methods
        ### Annuity based, NPV based, and FCR based. All LCoE values are in cents/kWh




        def LCoE_annuity():



            annuity = 1.0 / interest_rate * (1.0 - 1.0 / (1.0 + interest_rate) ** operational_lifetime)







            lcoe_previous = (investment_costs * 100.0) / (annuity * (AEP / 1000.0)) + oandm_costs * 100.0 / (AEP / 1000.0) + decommissioning_costs * 100.0 * (1.0 + interest_rate) ** (- operational_lifetime) / (annuity * (AEP / 1000.0))
            # print (investment_costs * 100.0) / (annuity * (AEP / 1000.0))
            # print oandm_costs * 100.0 / (AEP / 1000.0)
            # print decommissioning_costs * 100.0 * (1.0 + interest_rate) ** (- operational_lifetime) / (annuity * (AEP / 1000.0))
            lcoe = lcoe_previous / transm_electrical_efficiency

            return lcoe

        def LCoE_discounted():


            n = range(int(operational_lifetime))
            n.remove(0)
            n.append(int(operational_lifetime))



            a = np.sum((oandm_costs*100 / (1 + interest_rate) ** t) for t in n)
            b = np.sum(((AEP/1000.0) / (1 + interest_rate) ** t) for t in n)
            lcoe = (investment_costs*100 + a) / b
            return lcoe

        def LCoE_FCR():

            #https://www.nrel.gov/docs/fy20osti/74598.pdf

            FCR = 0.075

            lcoe = ((investment_costs*100*FCR) + oandm_costs*100)/(AEP/1000)

            return lcoe

        lcoe = LCoE_annuity()








        '''
        IRR calculation
        '''


        turbine_power = []
        rho_air = 1.225



        # aerodynamic and electrical power calculations
        for v in wind_speeds:
            if v < cut_in_speed or v > cut_out_speed:
                turbine_power_ = 0.0
            elif v < rated_wind_speed:
                turbine_power_ = rotor_cp * 0.5 * rho_air * swept_area * (v**3) * eta_dt/1000000.0

            else:
                turbine_power_ = machine_rating/1000.0
            turbine_power.append(turbine_power_)

        turbine_power = np.array(turbine_power)
        #print farm_power



        revenue = np.sum(np.multiply(turbine_power, spot_prices))  #revenue in one year

        Revenue = revenue
        #print revenue
        #print oandm_costs

        yearly_revenue = revenue - oandm_costs

        #print yearly_revenue

        #print yearly_revenue
        years = np.ones((1,int(operational_lifetime)))

        revenue_cashflow = yearly_revenue*years

        #revenue_cashflow[-1] = revenue_cashflow[-1] - decommissioning_costs

        revenue_cashflow = np.ndarray.tolist(revenue_cashflow)



        #print revenue_cashflow

        cashflows = [-1*investment_costs, revenue_cashflow]

        output_list = []

        def removeNestings(cashflows):
            for i in cashflows:
                if type(i) == list:
                    removeNestings(i)
                else:
                    output_list.append(i)

        removeNestings(cashflows)

        #print output_list

        cashflows = output_list
        print cashflows

        IRR = np.irr(cashflows)





        def ramp():
            power_ramp = np.ediff1d(turbine_power)



            norm_power_ramp = [x*100/(machine_rating/1000) for x in power_ramp] # normalize with rated power

            #print '% power ramp:', norm_power_ramp
            norm_power_ramp = np.sort(np.abs(norm_power_ramp))

            #print norm_power_ramp
            cdf = scipy.stats.norm.cdf(norm_power_ramp, loc=np.mean(norm_power_ramp), scale=np.std(norm_power_ramp))

            #print cdf

            ### find element in cdf closest to 90 % probability and find the corresponding power ramp

            abs_val_array = np.abs(cdf - 0.9)
            idx = abs_val_array.argmin()
            ramp_90 = norm_power_ramp[idx]      # 90 % probability that the ramp rate is under this value
            return ramp_90


        ramp_90 = ramp()

        print 'ramp_90:', ramp_90




        # print(lcoe)
        # print(clock())
        print 'Turbine AEP:', AEP
        print 'Turbine LCOE:', lcoe
        print 'Turbine IRR:', IRR


        outputs['LCOE'] = lcoe
        outputs['IRR'] = IRR
        outputs['ramp_90'] = ramp_90


#############################################################################
##############################  UNIT TESTING ################################
#############################################################################
if __name__ == "__main__":
    #from WINDOW_openMDAO.src.api import beautify_dict
    import matplotlib.pyplot as plt

    ###################################################
    ############### Model Execution ###################
    ###################################################
    inputs = {'cut_in_speed': 3.0, \
              'rated_wind_speed': 11,\
              'cut_out_speed': 25.0, \
              'swept_area': 12445.26, \
              'machine_rating': 5000., \
              'drive_train_efficiency': 0.95, \
              'rotor_cp': 0.48, \
              'elec_power_bin': [0.0, 0.0, 0.0, 0.0, 2.59767225e+02, 5.07357861e+02, 8.76714383e+02, 1.39218997e+03, \
                                2.07813780e+03, 2.95891104e+03, 4.05886289e+03, 5000.0, 5000.0, 5000.0,5000.0,5000.0, \
                                 5000.0,5000.0,5000.0,5000.0, 5000.0,5000.0,5000.0,5000.0, 5000.0,5000.0,0.0,0.0, 0.0,0.0, 0.0],\

              'weibull_shape': 2.11,\
              'weibull_scale': 8.15, \

              'investment_costs': 10000000.0, \
              'decommissioning_costs': 6000000.0, \
              'transm_electrical_efficiency': 0.95, \
              'operational_lifetime': [25], \
              'interest_rate': 0.075
                            }
    outputs = {}


    model = single_turbine(wind_speed_file='NL_wind_speed.csv', spot_price_file='NL_spot_price.csv')

    model.compute(inputs, outputs)