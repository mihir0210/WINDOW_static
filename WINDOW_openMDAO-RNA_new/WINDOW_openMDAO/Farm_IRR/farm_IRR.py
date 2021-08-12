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

        self.add_input('H2_produced', shape=time_points)
        self.add_input('H2_CAPEX', val=0.0)
        self.add_input('H2_OPEX',val=0.0)
        self.add_input('power_curtailed', shape=time_points)




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

        H2_CAPEX = inputs['H2_CAPEX']
        H2_OPEX = inputs['H2_OPEX']
        H2_produced = inputs['H2_produced']
        power_curtailed = inputs['power_curtailed']

        #print 'O&M:', oandm_costs

        with open('farm_power_89_hourly.csv', 'w') as csvfile:
            a = csv.writer(csvfile, delimiter=',')
            a.writerow(farm_power)



        def irr_npv():

            revenue = []
            y_revenue =[]

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
                y_revenue.append(yearly_revenue)

            revenue[-1] = revenue[-1] - decommissioning_costs

            cashflows = [-1 * investment_costs[0], revenue]

            r = 0.05
            revenues = []
            var_costs =[]

            for t in range(len(operational_lifetime)):
                revenues.append(y_revenue[t]/(1+r)**(t+1))
                var_costs.append(oandm_costs/(1+r)**(t+1))

            var_costs[-1] = var_costs[-1] + decommissioning_costs

            num = sum(revenues)
            den = investment_costs[0] + sum(var_costs)

            revenue_costs = num/den

            print 'Revenue/Costs:', revenue_costs







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

            ##### Write your own IRR function ####

            # Checks where NPV switches sign

            rate = np.linspace(-0.15,0.15,200)
            NPV_pxy = []

            for r in rate:
                val = np.npv(r, cashflows)
                NPV_pxy.append(val[0])


            #print NPV_pxy

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

            #print 'IRR_scneario_inbuilt:', IRR
            #print 'IRR_scenario:', IRR_new






            return IRR, NPV



        #[IRR, NPV] = irr_npv()

        def irr_withH2():

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


                yearly_revenue_elec = np.multiply(elec_farm_power, spot_price_ts) #from electricity only

                #print 'Mean spot price:', np.mean(spot_price_ts)
                #print 'Yearly revenue:', yearly_revenue

                ### yearly revenue from H2 (and elec) ###

                H2_price = 3.5*0.88 # Assume it to be $3-5/kg; Converted to euros


                yearly_revenue_H2 = [] #from H2 (and elec only available power exceeds electrolyser rated or when it's less than base load of electrolyser)
                #yearly_revenue_H2 = np.multiply(H2_produced, H2_price)

                for idx in range(len(H2_produced)):
                    if power_curtailed[idx]>0:
                        hydrogen_revenue = H2_produced[idx]*H2_price
                        elec_revenue = power_curtailed[idx]*spot_price_ts[idx]
                        yearly_revenue_H2.append(hydrogen_revenue + elec_revenue)


                    else:
                        hydrogen_revenue = H2_produced[idx] * H2_price
                        yearly_revenue_H2.append(hydrogen_revenue)




                yearly_revenue_ts = yearly_revenue_elec

                count = 0

                for idx in range(len(yearly_revenue_elec)):
                    if yearly_revenue_ts[idx]<yearly_revenue_H2[idx]:
                        yearly_revenue_ts[idx] = yearly_revenue_H2[idx]
                        count = count + 1


                #print count
                #yearly_revenue = np.sum(yearly_revenue_ts)
                yearly_revenue = np.sum(yearly_revenue_H2)






                revenue.append(max(0,yearly_revenue - oandm_costs - H2_OPEX[0]))

            print 'Yearly revenue H2:', np.sum(yearly_revenue_H2)
            revenue[-1] = revenue[-1] - decommissioning_costs



            cashflows = [-1 * (investment_costs[0] + H2_CAPEX[0]), revenue]





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

            discount_rate = -0.1115
            NPV = np.npv(discount_rate, cashflows)

            tot_investment = (investment_costs[0] + H2_CAPEX[0])

            #print 'NPV with irr% dr:', NPV

            ##### Write your own IRR function ####

            # Checks where NPV switches sign

            rate = np.linspace(-0.15,0.15,200)
            NPV_pxy = []

            for r in rate:
                val = np.npv(r, cashflows)
                NPV_pxy.append(val[0])


            #print NPV_pxy

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

            print 'IRR_withH2_inbuilt:', IRR
            print 'IRR_withH2:', IRR_new











            return IRR





        IRR_withH2 = irr_withH2()



        '''

        #print 'IRR_gradslope:', IRR
        #print 'NPV:', NPV

        #ramp =  np.ediff1d(elec_farm_power_ts)

        #pd.DataFrame(ramp).to_csv('farm_ramp_95.csv')
        #pd.DataFrame(farm_power_ts).to_csv('farm_power_95.csv') '''

        def irr_withH2_other():

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


                yearly_revenue_elec = np.multiply(elec_farm_power, spot_price_ts) #from electricity only

                #print 'Mean spot price:', np.mean(spot_price_ts)
                #print 'Yearly revenue:', yearly_revenue

                ### yearly revenue from H2 (and elec) ###

                H2_price = 100*0.88 # Assume it to be $3-5/kg; Converted to euros


                yearly_revenue_H2 = [] #from H2 (and elec only available power exceeds electrolyser rated or when it's less than base load of electrolyser)
                #yearly_revenue_H2 = np.multiply(H2_produced, H2_price)

                for idx in range(len(H2_produced)):
                    if power_curtailed[idx]>0:
                        hydrogen_revenue = H2_produced[idx]*H2_price
                        elec_revenue = power_curtailed[idx]*spot_price_ts[idx]
                        yearly_revenue_H2.append(hydrogen_revenue + elec_revenue)


                    else:
                        hydrogen_revenue = H2_produced[idx] * H2_price
                        yearly_revenue_H2.append(hydrogen_revenue)




                yearly_revenue_ts = yearly_revenue_elec

                count = 0

                for idx in range(len(yearly_revenue_elec)):
                    if yearly_revenue_ts[idx]<yearly_revenue_H2[idx]:
                        yearly_revenue_ts[idx] = yearly_revenue_H2[idx]
                        count = count + 1


                #print count
                #yearly_revenue = np.sum(yearly_revenue_ts)
                yearly_revenue = np.sum(yearly_revenue_H2)






                revenue.append(max(0,yearly_revenue - oandm_costs - H2_OPEX[0]))

            print 'Yearly revenue H2:', np.sum(yearly_revenue_H2)
            revenue[-1] = revenue[-1] - decommissioning_costs

            cashflows = [-1 * (investment_costs[0] + H2_CAPEX[0]), revenue]





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


            #print NPV_pxy

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

            print 'IRR_withH2_other_inbuilt:', IRR
            print 'IRR_withH2_other:', IRR_new

            return IRR



        #IRR = irr_withH2_other()

        outputs['IRR'] = IRR_withH2
        #outputs['IRR'] = IRR




























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