import numpy as np




from numpy import genfromtxt
from WINDOW_openMDAO.src.AbsRevenue.revenue import AbsRevenue


class Revenue_based(AbsRevenue):
    '''
    A model to determine lifetime revenue of the wind farm
    '''

    def initialize(self):

        # fixed parameters
        self.metadata.declare('wind_speed_file', desc='wind speed data file')
        self.metadata.declare('spot_price_file', desc ='Spot price data file')


    def compute(self, inputs, outputs):

        wind_speed_file = self.metadata['wind_speed_file']
        spot_price_file = self.metadata['spot_price_file']



        # inputs

        cut_in_speed = inputs['cut_in_speed']
        rated_wind_speed = inputs['rated_wind_speed']
        cut_out_speed = inputs['cut_out_speed']
        swept_area = inputs['swept_area']
        machine_rating = inputs['machine_rating']
        eta_dt = inputs['drive_train_efficiency']
        rotor_cp = inputs['rotor_cp']
        farm_eff = inputs['farm_eff']
        n_turbines = inputs['n_turbines']

        total_investment = inputs['total_investment']
        O_M = inputs['O_M']

        lifetime = 20 # farm lifetime in years

        #wind_speeds = pd.read_csv(wind_speed_file)
        #spot_prices = pd.read_csv(spot_price_file)

        wind_speeds = genfromtxt(wind_speed_file)
        spot_prices = genfromtxt(spot_price_file)



        farm_power = []
        rho_air = 1.225



        # aerodynamic calculations
        for v in wind_speeds:
            if v < cut_in_speed or v > cut_out_speed:
                farm_power_ = 0.0
            elif v < rated_wind_speed:
                farm_power_ = rotor_cp * 0.5 * rho_air * swept_area * (v**3) * eta_dt * n_turbines/1000000.0

            else:
                farm_power_ = machine_rating*n_turbines/1000.0
            farm_power.append(farm_power_)

        farm_power = np.array(farm_power)
        #print farm_power
        farm_power = farm_power*farm_eff # for wake effects


        revenue = np.sum(np.multiply(farm_power, spot_prices))/4.0 #revenue in one year

        Revenue = revenue
        #print revenue

        yearly_revenue = revenue - O_M

        #print yearly_revenue
        years = np.ones((1,lifetime))

        revenue_cashflow = yearly_revenue*years

        revenue_cashflow = np.ndarray.tolist(revenue_cashflow)

        #print revenue_cashflow

        cashflows = [-1*total_investment, revenue_cashflow]

        output_list = []

        def removeNestings(cashflows):
            for i in cashflows:
                if type(i) == list:
                    removeNestings(i)
                else:
                    output_list.append(i)

        removeNestings(cashflows)
        #print cashflows
        #print output_list

        cashflows = output_list


        IRR = np.irr(cashflows)
        print IRR
        #IRR = np.irr(output_list)

        discount_rate = 0.05

        NPV = np.npv(discount_rate, cashflows)
        #print NPV









        # outputs

        outputs['Revenue'] = Revenue
        outputs['NPV'] = NPV
        outputs['IRR'] = IRR


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
              'rotor_cp': 0.467403, \
              'farm_eff': 0.9,\
              'n_turbines': 73,\
              'total_investment': 665000000.0,\
              'O_M': 1000000
              }
    outputs = {}

    model = Revenue_based(wind_speed_file='NL_wind_speed.csv', spot_price_file='NL_spot_price.csv')

    model.compute(inputs, outputs)

    ###################################################
    ############### Post Processing ###################
    ###################################################


