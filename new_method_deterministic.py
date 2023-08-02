import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib
import csv
from matplotlib.patches import FancyArrowPatch
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from create_corr_vector import corrvec

from scipy.stats import norm
# spot_prices_2022 = np.genfromtxt('NL_prices_2022.csv')
# mu, std = norm.fit(spot_prices_2022)
# print(mu, std)
# import seaborn as sns
#
# ax = sns.distplot(spot_prices_2022)
# plt.xlabel('Spot prices (Euros/MWh)')
# plt.show()

# power_values = [10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 19.23, 20.0] #for a 1 GW farm
power_values = [10.0, 10.99, 12.05, 12.99, 13.51, 14.08, 14.49, 14.93, 15.62, 16.13, 16.67, 17.24, 18.18, 19.23, 20.0, 22.73]
# n_t_ = [100, 91, 83, 77, 71, 67, 62, 58, 55, 52, 50, 44]
rad_values= [90.0, 95.0, 100.0, 105.0, 215 / 2, 110.0, 222 / 2, 225 / 2, 227 / 2, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]

# power_values = [10, 12, 14, 16, 18, 19, 20, 21, 22, 24, 26, 28, 30]
# dia = [180, 190, 200, 210, 220, 222, 225, 227, 230, 240, 250, 260, 270, 280, 290, 300]
# rad_values = [d/2 for d in dia]
# N_T = [213, 193, 175, 160, 147, 145, 141, 139, 136, 125, 116, 108, 101, 95, 89, 84] # for 5D spacing in 150 km2


trans_efficiency = 0.95
p_rated = np.zeros((len(power_values), len(rad_values)))
d_rotor = np.zeros((len(power_values), len(rad_values)))
n_t = np.zeros((len(power_values), len(rad_values)))
v_mean = np.zeros((len(power_values), len(rad_values)))
rotor_costs = np.zeros((len(power_values), len(rad_values)))
RNA_costs = np.zeros((len(power_values), len(rad_values)))
RNA_costsperMW = np.zeros((len(power_values), len(rad_values)))
tower_costs = np.zeros((len(power_values), len(rad_values)))
tower_costsperMW = np.zeros((len(power_values), len(rad_values)))
total_turbine_costs = np.zeros((len(power_values), len(rad_values)))
other_turbine_costs = np.zeros((len(power_values), len(rad_values))) #profits, warranty, assembly, etc.
turbine_costs_perMW = np.zeros((len(power_values), len(rad_values)))
turbine_costs_singleturbine = np.zeros((len(power_values), len(rad_values)))
foundation_costs = np.zeros((len(power_values), len(rad_values)))
foundation_costs_perMW = np.zeros((len(power_values), len(rad_values)))
infield_length = np.zeros((len(power_values), len(rad_values)))
infield_cable_costs = np.zeros((len(power_values), len(rad_values)))
total_electrical_costs = np.zeros((len(power_values), len(rad_values)))

installation_turbine_costs = np.zeros((len(power_values), len(rad_values)))
installation_foundation_costs = np.zeros((len(power_values), len(rad_values)))
installation_electrical_costs = np.zeros((len(power_values), len(rad_values)))
total_installation_costs = np.zeros((len(power_values), len(rad_values)))
installation_costs_perMW = np.zeros((len(power_values), len(rad_values)))

projectdev_costs = np.zeros((len(power_values), len(rad_values)))
other_farm_costs = np.zeros((len(power_values), len(rad_values))) #insurance, contingency, etc.
decom_costs = np.zeros((len(power_values), len(rad_values)))

oandm_costs = np.zeros((len(power_values), len(rad_values)))
total_oandm_costs = np.zeros((len(power_values), len(rad_values)))
farm_capex = np.zeros((len(power_values), len(rad_values)))
farm_area = np.zeros((len(power_values), len(rad_values)))

wake_losses = np.zeros((len(power_values), len(rad_values)))
aep = np.zeros((len(power_values), len(rad_values)))
aep_noloss = np.zeros((len(power_values), len(rad_values)))


fixed_costs = np.zeros((len(power_values), len(rad_values)))
variable_costs = np.zeros((len(power_values), len(rad_values)))
var_fix_ratio = np.zeros((len(power_values), len(rad_values)))
lcoe_recalc = np.zeros((len(power_values), len(rad_values)))
total_revenue = np.zeros((len(power_values), len(rad_values)))
total_revenue_cove = np.zeros((len(power_values), len(rad_values)))

num = np.zeros((len(power_values), len(rad_values)))
total_aep = np.zeros((len(power_values), len(rad_values)))
lcoe = np.zeros((len(power_values), len(rad_values)))
new_lcoe = np.zeros((len(power_values), len(rad_values)))
npv = np.zeros((len(power_values), len(rad_values)))
IRR = np.zeros((len(power_values), len(rad_values)))
mIRR = np.zeros((len(power_values), len(rad_values)))
CoVE = np.zeros((len(power_values), len(rad_values)))
value_factor = np.zeros((len(power_values), len(rad_values)))
lpoe = np.zeros((len(power_values), len(rad_values)))
# rev_by_capex = np.zeros((len(power_values), len(rad_values)))
profitability_index = np.zeros((len(power_values), len(rad_values)))

z_wake = []
z_aep = []
z_oandm = []
z_vmean = []
z_installation = []
z_electrical = []
z_rnaperMW = []
z_towerperMW = []
z_foundationperMW = []

z_turbine = []
z_bos = []
z_CAPEX = []

sp_data = [] #specific power

cost_ratio_sp = []

opt_d_cove = []
opt_p_cove = []
opt_d_npv_all = []
opt_p_npv_all = []
opt_d_irr_all = []
opt_p_irr_all = []
opt_d_mirr_all = []
opt_p_mirr_all = []
opt_d_pi_all = []
opt_p_pi_all = []
opt_d_lpoe = []
opt_p_lpoe = []


opt_d_irr_pos = []
opt_p_irr_pos = []
opt_d_mirr_pos = []
opt_p_mirr_pos = []
opt_d_npv_pos = []
opt_p_npv_pos = []
opt_d_pi_pos = []
opt_p_pi_pos = []

opt_d_irr_neg = []
opt_p_irr_neg = []
opt_d_mirr_neg = []
opt_p_mirr_neg = []
opt_d_npv_neg = []
opt_p_npv_neg = []
opt_d_pi_neg = []
opt_p_pi_neg = []

# opt_d_rev_by_capex = []
# opt_p_rev_by_capex = []
# opt_d_pi = [] #profitability index is same as net revenue over lifetime/capex
# opt_p_pi = []



opt_cove = []
opt_irr= []
opt_mirr= []
opt_npv = []

dict_irr = {}
dict_mIRR = {}
dict_pi = {}
dict_npv = {}
dict_cove = {}

for p in power_values:
    for r in rad_values:
        dict_irr[str(round(p, 2)) + '_' + str(round(r*2, 1))] = []
        dict_mIRR[str(round(p, 2)) + '_' + str(round(r*2, 1))] = []
        dict_pi[str(round(p, 2)) + '_' + str(round(r*2, 1))] = []
        dict_npv[str(round(p, 2)) + '_' + str(round(r*2, 1))] = []
        dict_cove[str(round(p, 2)) + '_' + str(round(r*2, 1))] = []

################ Market prices #################

# spot_prices = np.genfromtxt('NL_2019_spot_price_hourly.csv')
wind_file = 'NorthSea_2019_100m_hourly_ERA5_withdir.csv'
ws_wd = pd.read_csv(wind_file)
wind_speed = ws_wd['wind_speed']

############# Market model input space consists of Mean of spot prices, Std. of spot prices, and correlation with wind

mean_spot_range = np.linspace(40, 100, 13)
# std_spot_range = np.linspace(5, 20, 7) #absolute values
std_spot_range = np.linspace(0.4, 0.4, 1) #as a fraction of the mean
corr_coeff_range = np.linspace(-1,0,11)



import itertools

all_lists = [mean_spot_range, std_spot_range, corr_coeff_range]
all_combinations = list(itertools.product(*all_lists))
n_scenarios = len(all_combinations)


perc_diff_lcoe_design_mirr = [] #len(all_combinations)
perc_diff_lcoe_design_pi = [] #len(all_combinations)
perc_diff_lcoe_design_npv= [] #len(all_combinations)




for idx in range(n_scenarios):

    values = all_combinations[idx]

    mean_spot = values[0]
    # std_spot = values[1]
    std_spot = values[1]*mean_spot
    corr_coeff = values[2]

    guess = np.random.normal(size=len(wind_speed)) #initial guess vector required to generate spot prices
    spot_prices = corrvec(wind_speed, corr_coeff, guess, mean_spot, std_spot)

    print(mean_spot, std_spot, corr_coeff)




    x_data = []
    y_data = []
    z_data = []
    z_data_IRR = []
    z_data_mIRR = []
    z_data_CoVE = []
    z_data_npv = []
    z_data_lpoe = []
    # z_data_rev_by_capex = []
    z_data_npv_by_capex = []
    z_data_profitability_index = []

    for p in power_values:
        for r in rad_values:
            idx_power = power_values.index(p)
            idx_diameter = rad_values.index(r)

            filename = '1000MW_baseline/parameters_' + str(p) + '_' + str(r*2) + '.csv'
            # filename = '1000MW_lowwind/parameters_' + str(p) + '_' + str(r * 2) + '.csv'
            # filename = 'Fixed_area_150/parameters_' + str(p) + '_' + str(r * 2) + '_' + str(N_T[idx_diameter]) + '.csv'
            df = pd.read_csv(filename, header=None,names=['variable', 'data', 'description'])
            variable = df['variable']
            data = df['data']

            var = pd.Series.tolist(variable)


            ###### assign values in the matrix #####

            p_rated[idx_power, idx_diameter] = p
            d_rotor[idx_power, idx_diameter] = r*2


            idx = var.index('a_farm')
            farm_area[idx_power, idx_diameter] = data[idx]

            idx = var.index('O&M Costs')
            oandm_costs[idx_power, idx_diameter] = data[idx]

            idx = var.index('costs_decom_elec')
            decom_costs[idx_power, idx_diameter] = data[idx] #/(1+0.05)**25

            idx = var.index('costs_totalinvestment_elec:')
            farm_capex[idx_power, idx_diameter] = (data[idx])


            idx = var.index('aep_withwake')
            aep[idx_power, idx_diameter] = data[idx]*1e3 #in MWh

            filename_power = '1000MW_baseline/farm_power_' + str(p) + '_' + str(r*2) + '.csv'
            # filename_power = '1000MW_lowwind/farm_power_' + str(p) + '_' + str(r * 2) + '.csv'
            # filename_power = 'Fixed_area_150/farm_power_' + str(float(p)) + '_' + str(r * 2) + '_' + str(N_T[idx_diameter]) + '.csv'
            df_power = pd.read_csv(filename_power, header=None)
            farm_power_ts = df_power.iloc[1::, 1] #farm power time series in MW
            farm_power_ts = pd.Series.to_numpy(farm_power_ts)

            elec_power = farm_power_ts*trans_efficiency*0.97

            # net_revenue = np.zeros(25)  # or 25?
            # for n in range(25):
            #     spot_prices = market_prices(wind_speed)
            #     revenue = elec_power*np.array(spot_prices)
            #     yearly_revenue = sum(revenue)
            #     print(yearly_revenue)
            #     oandm_reduction = 0 #20 % reduction in future
            #     net_yearly_revenue = yearly_revenue - (1 - oandm_reduction)*oandm_costs[idx_power, idx_diameter]
            #     net_revenue[n] = net_yearly_revenue
            #
            #
            #
            # net_revenue[-1] = net_revenue[-1] - decom_costs[idx_power, idx_diameter]


            revenue = elec_power*spot_prices
            yearly_revenue = sum(revenue)
            oandm_reduction = 0 #20 % reduction in futurer5
            net_yearly_revenue = yearly_revenue - (1 - oandm_reduction)*oandm_costs[idx_power, idx_diameter]

            net_revenue = np.zeros(25) #or 25?
            net_revenue[:] = net_yearly_revenue
            net_revenue[-1] = net_yearly_revenue - decom_costs[idx_power, idx_diameter]

            cashflows = []
            cashflows.append(-1*farm_capex[idx_power, idx_diameter])
            for rev in net_revenue:
                cashflows.append(rev)

            # cashflows.append(-1*decom_costs[idx_power, idx_diameter])


            import numpy_financial as npf
            IRR[idx_power, idx_diameter] = npf.irr(cashflows)
            mIRR[idx_power, idx_diameter] = npf.mirr(cashflows, 0.05, 0.05)
            npv[idx_power, idx_diameter] = npf.npv(0.05, cashflows)/1e6


            idx = var.index('lcoe')
            lcoe[idx_power, idx_diameter] = data[idx]*10



            aep_yearly = np.zeros(25)
            fixed_oandm_yearly = np.zeros(25)
            oandm_yearly = np.zeros(25)
            revenue = np.zeros(25)
            revenue_cove = np.zeros(25)
            for idx in range(1,26):
                aep_yearly[idx-1] = aep[idx_power, idx_diameter]*0.97*trans_efficiency/(1+0.05)**idx
                fixed_oandm_yearly[idx-1] = 22.5e6/(1+0.05)**idx
                oandm_yearly[idx-1] = oandm_costs[idx_power, idx_diameter]/(1+0.05)**idx
                revenue[idx-1] = net_yearly_revenue/(1+0.05)**idx
                revenue_cove[idx - 1] = yearly_revenue / (1 + 0.05) ** idx
            total_aep[idx_power, idx_diameter] = np.sum(aep_yearly)
            fixed_oandm = np.sum(fixed_oandm_yearly)
            total_oandm_costs[idx_power, idx_diameter] = np.sum(oandm_yearly)
            total_revenue[idx_power, idx_diameter] = np.sum(revenue)
            total_revenue_cove[idx_power, idx_diameter] = np.sum(revenue_cove)
            # rev_by_capex[idx_power, idx_diameter] = total_revenue[idx_power, idx_diameter]/farm_capex[idx_power, idx_diameter]
            profitability_index[idx_power, idx_diameter] = total_revenue[idx_power, idx_diameter] / farm_capex[idx_power, idx_diameter]

            fixed_revenue = total_aep[idx_power, idx_diameter]*np.mean(spot_prices)
            value_factor[idx_power, idx_diameter] = total_revenue_cove[idx_power, idx_diameter]/fixed_revenue

            num[idx_power, idx_diameter] = lcoe[idx_power, idx_diameter]*total_aep[idx_power, idx_diameter]
            # # lcoe[idx_power, idx_diameter] = num[idx_power, idx_diameter]/total_aep[idx_power, idx_diameter]
            new_lcoe[idx_power, idx_diameter] = (num[idx_power, idx_diameter] - oandm_reduction*total_oandm_costs[idx_power, idx_diameter])/total_aep[idx_power, idx_diameter]

            CoVE[idx_power, idx_diameter] = new_lcoe[idx_power, idx_diameter]/value_factor[idx_power, idx_diameter]



            lpoe[idx_power, idx_diameter] = npv[idx_power, idx_diameter]*1e6/total_aep[idx_power, idx_diameter]



            # print(new_lcoe)

            import math

            val_check = math.isnan(IRR[idx_power, idx_diameter])

            if val_check == False:
                x_data.append(r*2)
                y_data.append(p)
                # sp_data.append(p*1e6/(3.142*r**2))

                z_data.append(new_lcoe[idx_power, idx_diameter])
                z_data_IRR.append(IRR[idx_power, idx_diameter])
                z_data_mIRR.append(mIRR[idx_power, idx_diameter])
                z_data_CoVE.append(CoVE[idx_power, idx_diameter])
                z_data_npv.append(npv[idx_power, idx_diameter])
                z_data_lpoe.append(lpoe[idx_power, idx_diameter])
                # z_data_rev_by_capex.append(rev_by_capex[idx_power, idx_diameter])
                z_data_profitability_index.append(profitability_index[idx_power, idx_diameter])

                dict_irr[str(round(p, 2)) + '_' + str(round(r * 2, 1))].append(IRR[idx_power, idx_diameter])
                dict_mIRR[str(round(p, 2)) + '_' + str(round(r * 2, 1))].append(mIRR[idx_power, idx_diameter])
                dict_pi[str(round(p, 2)) + '_' + str(round(r * 2, 1))].append(profitability_index[idx_power, idx_diameter])
                dict_npv[str(round(p, 2)) + '_' + str(round(r * 2, 1))].append(npv[idx_power, idx_diameter])
                dict_cove[str(round(p, 2)) + '_' + str(round(r * 2, 1))].append(CoVE[idx_power, idx_diameter])
            # z_aep.append(aep[idx_power, idx_diameter])
            # z_oandm.append(oandm_costs[idx_power, idx_diameter])
            # z_CAPEX.append(farm_capex[idx_power, idx_diameter])


    # result_deterministic = np.array(np.where(lcoe == np.amin(lcoe))).flatten()
    # global_optimum_deterministic = [power_values[result_deterministic[0]], rad_values[result_deterministic[1]]]
    # print('Deterministic optimum before surface fit:',power_values[result_deterministic[0]], rad_values[result_deterministic[1]])
    # print('LCoE =', np.amin(lcoe))
    #
    # result_deterministic = np.array(np.where(CoVE == np.amin(CoVE))).flatten()
    # global_optimum_deterministic = [power_values[result_deterministic[0]], rad_values[result_deterministic[1]]]
    # print('Deterministic optimum before surface fit:',power_values[result_deterministic[0]], rad_values[result_deterministic[1]])
    # print('CoVE =', np.amin(CoVE))
    #
    # result_deterministic = np.array(np.where(IRR == np.amax(IRR))).flatten()
    # global_optimum_deterministic = [power_values[result_deterministic[0]], rad_values[result_deterministic[1]]]
    # print('Deterministic optimum before surface fit:',power_values[result_deterministic[0]], rad_values[result_deterministic[1]])
    # print('IRR =', np.amax(IRR))
    #
    # result_deterministic = np.array(np.where(npv == np.amax(npv))).flatten()
    # global_optimum_deterministic = [power_values[result_deterministic[0]], rad_values[result_deterministic[1]]]
    # print('Deterministic optimum before surface fit:',power_values[result_deterministic[0]], rad_values[result_deterministic[1]])
    # print('NPV =', np.amax(npv))

    # def function(data, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14):
    #     x = data[0]
    #     y = data[1]
    #     return p0 + p1 * x + p2 * y + p3 * x ** 2 + p4 * x * y + p5 * y ** 2 + p6 * x ** 3 + p7 * x ** 2 * y + p8 * x * y ** 2 + p9 * y ** 3 + p10*x**4 + p11*x**3*y + p12*x**2*y**2 + p13*x*y**3 + p14*y**4


# def function(data, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20):
#     x = data[0]
#     y = data[1]
#     return p0 + p1 * x + p2 * y + p3 * x ** 2 + p4 * x * y + p5 * y ** 2 + p6 * x ** 3 + p7 * x ** 2 * y + p8 * x * y ** 2 + p9 * y ** 3 + p10*x**4 + p11*x**3*y + p12*x**2*y**2 + p13*x*y**3 + p14*y**4 + p15*x**5 + p16*x**4*y + p17*x**3*y**2 + p18*x**2*y**3 + p19*x*y**4 + p20*y**5
#
#
# num.dump("num_matrix_baseline_course.dat")
# aep.dump("aep_matrix_baseline_course.dat")
# p_rated.dump("power_matrix_baseline_course.dat")
# d_rotor.dump("diameter_matrix_baseline_course.dat")
# lcoe.dump("lcoe_matrix_baseline_course.dat")
#
# aep_noloss.dump("lossless_aep_baseline_course.dat")
# v_mean.dump("v_mean_matrix_baseline_course.dat")
# wake_losses.dump("wake_matrix_baseline_course.dat")
# total_turbine_costs.dump("turbine_costs_matrix_baseline_course.dat")
# foundation_costs.dump("foundation_costs_matrix_baseline_course.dat")
# total_oandm_costs.dump("oandm_costs_matrix_baseline_course.dat")
# total_installation_costs.dump("installation_costs_matrix_baseline_course.dat")
# total_electrical_costs.dump("electrical_costs_matrix_baseline_course.dat")
# other_turbine_costs.dump('other_turbine_costs_baseline_course.dat')
# other_farm_costs.dump('other_farm_costs_baseline_course.dat')
# projectdev_costs.dump('projectdev_costs_baseline_course.dat')
# decom_costs.dump('decom_costs_baseline_course.dat')

# get fit parameters from scipy curve fit
# par = curve_fit(function, [x_data, y_data], z_data)

    p_eval = np.linspace(10, 20, 101)
    # p_eval = np.linspace(10, 30, 210)
    r_eval = np.linspace(90, 150, 242)
    d_eval = [2 * r for r in r_eval]

    [D, P] = np.meshgrid(d_eval, p_eval)

# p = par[0]
#
# lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# #lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10] * P**4 + p[11] * P**3 * D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4 + p[15]*P**5 + p[16]* P**4 *D + p[17] * P**3 * D**2 + p[18]* P**2 * D**3 + p[19]*P* D**4 + p[20]*D**5
#
#
# result_deterministic = np.array(np.where(lcoe_estimate == np.amin(lcoe_estimate))).flatten()
# global_optimum_deterministic = [d_eval[result_deterministic[0]], p_eval[result_deterministic[1]]]
# print('Deterministic optimum after surface fit:',p_eval[result_deterministic[1]], d_eval[result_deterministic[0]])
# print('LCoE =', np.amin(lcoe_estimate))



    #### New generic surface fit code for n degree 2D polynomial
    if len(x_data) != 0:

        x = np.array(x_data)
        y = np.array(y_data)
        z_lcoe = np.array(z_data)
        z_irr = np.array(z_data_IRR)
        z_mirr = np.array(z_data_mIRR)
        z_cove = np.array(z_data_CoVE)
        z_npv = np.array(z_data_npv)
        z_lpoe = np.array(z_data_lpoe)
        # z_rev_by_capex = np.array(z_data_rev_by_capex)
        z_profitability_index = np.array(z_data_profitability_index)

        data_xy = np.array([x,y])
        poly = PolynomialFeatures(degree=4)
        X_t = poly.fit_transform(data_xy.transpose())

        clf_lcoe = LinearRegression()
        clf_lcoe.fit(X_t, z_lcoe)

        clf_irr = LinearRegression()
        clf_irr.fit(X_t, z_irr)


        clf_mirr = LinearRegression()
        clf_mirr.fit(X_t, z_mirr)

        clf_cove = LinearRegression()
        clf_cove.fit(X_t, z_cove)

        clf_npv = LinearRegression()
        clf_npv.fit(X_t, z_npv)

        clf_lpoe = LinearRegression()
        clf_lpoe.fit(X_t, z_lpoe)

        # clf_rev_by_capex = LinearRegression()
        # clf_rev_by_capex .fit(X_t, z_rev_by_capex)

        clf_profitability_index = LinearRegression()
        clf_profitability_index.fit(X_t, z_profitability_index)

        z_pred_lcoe = np.zeros((len(p_eval), len(d_eval)))
        z_pred_irr = np.zeros((len(p_eval), len(d_eval)))
        z_pred_mirr = np.zeros((len(p_eval), len(d_eval)))
        z_pred_cove = np.zeros((len(p_eval), len(d_eval)))
        z_pred_npv = np.zeros((len(p_eval), len(d_eval)))
        z_pred_lpoe = np.zeros((len(p_eval), len(d_eval)))
        # z_pred_rev_by_capex = np.zeros((len(p_eval), len(d_eval)))
        z_pred_profitability_index = np.zeros((len(p_eval), len(d_eval)))

        for p in p_eval:
            for d in d_eval:
                idx_power = np.where(p_eval == p)
                idx_diameter = np.where(d_eval == d)
                data_xy = np.array([[d], [p]])
                X_t = poly.fit_transform(data_xy.transpose())
                # z_pred[idx_power, idx_diameter] = np.polynomial.polynomial.polygrid2d(p,d,clf.coef_)
                z_pred_lcoe[idx_power, idx_diameter] = clf_lcoe.predict(X_t)
                z_pred_irr[idx_power, idx_diameter] = clf_irr.predict(X_t)
                z_pred_mirr[idx_power, idx_diameter] = clf_mirr.predict(X_t)
                z_pred_cove[idx_power, idx_diameter] = clf_cove.predict(X_t)
                z_pred_npv[idx_power, idx_diameter] = clf_npv.predict(X_t)
                z_pred_lpoe[idx_power, idx_diameter] = clf_lpoe.predict(X_t)
                # z_pred_rev_by_capex[idx_power, idx_diameter] = clf_rev_by_capex.predict(X_t)
                z_pred_profitability_index[idx_power, idx_diameter] = clf_profitability_index.predict(X_t)

        p_diff = abs(15 - p_eval)
        d_diff = abs(111 - r_eval)
        idx_power_lcoe = p_diff.argmin()
        idx_diameter_lcoe = d_diff.argmin()

        mirr_lcoe = z_pred_mirr[idx_power_lcoe, idx_diameter_lcoe]
        profitability_index_lcoe = z_pred_profitability_index[idx_power_lcoe, idx_diameter_lcoe]
        npv_lcoe = z_pred_npv[idx_power_lcoe, idx_diameter_lcoe]




        # result_deterministic = np.array(np.where(z_pred_lcoe == np.amin(z_pred_lcoe))).flatten()
        # global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        # print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
        # print('LCoE =', np.amin(z_pred_lcoe))

        # result_deterministic = np.array(np.where(z_pred_lpoe == np.amax(z_pred_lpoe))).flatten()
        # global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        # opt_d_lpoe.append(d_eval[result_deterministic[1]])
        # opt_p_lpoe.append(p_eval[result_deterministic[0]])
        # print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
        # print('LPoE =', np.amax(z_pred_lpoe))

        result_deterministic = np.array(np.where(z_pred_cove == np.amin(z_pred_cove))).flatten()
        global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        opt_d_cove.append(d_eval[result_deterministic[1]])
        opt_p_cove.append(p_eval[result_deterministic[0]])
        opt_cove.append(np.amin(z_pred_cove))
        # print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
        # print('CoVE =', np.amin(z_pred_cove))

        result_deterministic = np.array(np.where(z_pred_irr == np.amax(z_pred_irr))).flatten()
        global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        opt_irr.append(np.amax(z_pred_irr))
        opt_d_irr_all.append(d_eval[result_deterministic[1]])
        opt_p_irr_all.append(p_eval[result_deterministic[0]])

        if np.amax(z_pred_irr)>=0.05:
            opt_d_irr_pos.append(d_eval[result_deterministic[1]])
            opt_p_irr_pos.append(p_eval[result_deterministic[0]])
            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('IRR =', np.amax(z_pred_irr))

        else:
            opt_d_irr_neg.append(d_eval[result_deterministic[1]])
            opt_p_irr_neg.append(p_eval[result_deterministic[0]])
            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('IRR =', np.amax(z_pred_irr))

        result_deterministic = np.array(np.where(z_pred_mirr == np.amax(z_pred_mirr))).flatten()
        global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        opt_mirr.append(np.amax(z_pred_mirr))
        opt_d_mirr_all.append(d_eval[result_deterministic[1]])
        opt_p_mirr_all.append(p_eval[result_deterministic[0]])

        if np.amax(z_pred_mirr)>=0.05:
            opt_d_mirr_pos.append(d_eval[result_deterministic[1]])
            opt_p_mirr_pos.append(p_eval[result_deterministic[0]])
            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('mIRR =', np.amax(z_pred_mirr))
            perc_diff_lcoe_design_mirr.append((np.amax(z_pred_mirr) - mirr_lcoe) * 100 / np.amax(z_pred_mirr))
            print((np.amax(z_pred_mirr) - mirr_lcoe) * 100 / np.amax(z_pred_mirr))
        else:
            opt_d_mirr_neg.append(d_eval[result_deterministic[1]])
            opt_p_mirr_neg.append(p_eval[result_deterministic[0]])
            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('mIRR =', np.amax(z_pred_mirr))


        result_deterministic = np.array(np.where(z_pred_npv == np.amax(z_pred_npv))).flatten()
        global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        opt_npv.append(np.amax(z_pred_npv))
        opt_d_npv_all.append(d_eval[result_deterministic[1]])
        opt_p_npv_all.append(p_eval[result_deterministic[0]])
        if np.amax(z_pred_npv)>=0:
            opt_d_npv_pos.append(d_eval[result_deterministic[1]])
            opt_p_npv_pos.append(p_eval[result_deterministic[0]])

            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('NPV=', np.amax(z_pred_npv))
            perc_diff_lcoe_design_npv.append((np.amax(z_pred_npv) - npv_lcoe) * 100 / np.amax(z_pred_npv))
            print((np.amax(z_pred_npv) - npv_lcoe) * 100 / np.amax(z_pred_npv))
        else:
            opt_d_npv_neg.append(d_eval[result_deterministic[1]])
            opt_p_npv_neg.append(p_eval[result_deterministic[0]])
            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('NPV=', np.amax(z_pred_npv))

        # result_deterministic = np.array(np.where(z_pred_rev_by_capex == np.amax(z_pred_rev_by_capex))).flatten()
        # global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        # opt_d_rev_by_capex.append(d_eval[result_deterministic[1]])
        # opt_p_rev_by_capex.append(p_eval[result_deterministic[0]])

        result_deterministic = np.array(np.where(z_pred_profitability_index == np.amax(z_pred_profitability_index))).flatten()
        global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
        opt_d_pi_all.append(d_eval[result_deterministic[1]])
        opt_p_pi_all.append(p_eval[result_deterministic[0]])

        if np.amax(z_pred_profitability_index)>=1:
            opt_d_pi_pos.append(d_eval[result_deterministic[1]])
            opt_p_pi_pos.append(p_eval[result_deterministic[0]])

            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('PI =', np.amax(z_pred_profitability_index))
            perc_diff_lcoe_design_pi.append((np.amax(z_pred_profitability_index) - profitability_index_lcoe) * 100 / np.amax(z_pred_profitability_index))
            print((np.amax(z_pred_profitability_index) - profitability_index_lcoe) * 100 / np.amax(z_pred_profitability_index))
        else:
            opt_d_pi_neg.append(d_eval[result_deterministic[1]])
            opt_p_pi_neg.append(p_eval[result_deterministic[0]])
            print('Deterministic optimum after new surface fit code:', p_eval[result_deterministic[0]], d_eval[result_deterministic[1]])
            print('PI =', np.amax(z_pred_profitability_index))

        #
        # opt_d_pi.append(d_eval[result_deterministic[1]])
        # opt_p_pi.append(p_eval[result_deterministic[0]])



    # fig, ax = plt.subplots()
    # fs = 16
    # result_deterministic = np.array(np.where(z_pred_rev_by_capex == np.amax(z_pred_rev_by_capex))).flatten()
    # global_optimum_deterministic = [p_eval[result_deterministic[0]], d_eval[result_deterministic[1]]]
    #
    # import seaborn as sns
    # from matplotlib.colors import ListedColormap
    #
    # # my_cmap = sns.color_palette("rocket", as_cmap=True)
    # my_cmap = sns.color_palette("BuGn_r", as_cmap=True)
    # # my_cmap = sns.color_palette("mako", as_cmap=True)
    # # c = plt.contourf(d_rotor,p_rated,property, 50, cmap='YlOrRd')
    # # c = plt.contourf(d_rotor, p_rated, rev_by_capex, 100, cmap=my_cmap.reversed())
    # # c = plt.contourf(d_rotor,p_rated,property, round(n_colorbars), cmap = my_cmap.reversed())
    # c = plt.contourf(d_eval,p_eval,z_pred_rev_by_capex, 30, cmap = my_cmap.reversed())
    #
    # cbar = fig.colorbar(c)
    # plt.plot(d_eval[result_deterministic[1]], p_eval[result_deterministic[0]], 'ko')
    # plt.xlabel('Rotor Diameter (m)', fontsize=fs)
    # plt.ylabel('Rated Power (MW)', fontsize=fs)
    # # plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
    # # cbar.ax.set_ylabel(y_label, fontsize = fs)
    # # plt.legend(loc='upper left',fancybox=True, framealpha=0.5)
    #
    # plt.grid(axis='both', alpha=0.1)
    # ax.tick_params(axis='both', direction='in', length=5)
    # # matplotlib.rcParams['legend.fontsize'] = 12
    # plt.show()


    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.3, 4.5))
    #
    # z_data_IRR = [val*100 for val in z_data_IRR]
    # # #plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
    # plt.scatter(z_data_npv, z_data_IRR, marker='o', c='k', s=20, alpha=0.5)
    # fs = 16
    #
    # plt.xlabel('NPV (M Euros)', fontsize=fs)
    # plt.ylabel('IRR (%)', fontsize=fs)
    # # #plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
    # # cbar.ax.set_ylabel(y_label, fontsize = fs)
    # #
    # plt.grid(axis='both', alpha=0.1)
    # ax.tick_params(axis='both', direction='in', length=5)
    # filename = 'IRR_vs_NPV/' + 'scenario_' + str(no_wind_price) + '_' + str(round(m,1)) + '.png'
    # plt.savefig(filename, bbox_inches='tight', dpi=300)

############################### LCoE vs IRR & LCoE vs NPV #################
    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.3, 4.5))
    # # ax2 = ax1.twinx()
    #
    # ax.scatter(z_data, z_data_IRR,  marker='o', c='k', s=20, alpha=0.5)
    # fs = 16
    #
    # ax.set_xlabel('LCoE (Euros/MWh)', fontsize=fs)
    # ax.set_ylabel('IRR (%)', fontsize=fs)
    # # #plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
    # # cbar.ax.set_ylabel(y_label, fontsize = fs)
    # #
    # plt.grid(axis='both', alpha=0.1)
    # # # plt.xlim([46,52])
    # ax.tick_params(axis='both', direction='in', length=5)
    # filename = 'LCoE_vs_IRR_lowwind/' + 'scenario_' + str(no_wind_price) + '_' + str(round(m,1)) + '.png'
    # plt.savefig(filename, bbox_inches='tight', dpi=300)
    #
    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.3, 4.5))
    # ax.scatter(z_data, z_data_npv,  marker='o', c='k', s=10, alpha=0.5)
    # fs = 16
    #
    # plt.xlabel('LCoE (Euros/MWh)', fontsize=fs)
    # ax.set_ylabel('NPV (M Euros)', fontsize=fs, color='k')
    # # plt.xlim([46, 52])
    # # #plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
    # # cbar.ax.set_ylabel(y_label, fontsize = fs)
    # #
    # plt.grid(axis='both', alpha=0.1)
    # ax.tick_params(axis='both', direction='in', length=5)
    # ax.tick_params(axis='both', direction='in', length=5)
    # filename = 'LCoE_vs_NPV_lowwind/' + 'scenario_' + str(no_wind_price) + '_' + str(round(m,1)) + '.png'
    # # filename = 'LCoE_IRR_NPV/' + 'scenario_' + str(no_wind_price) + '_' + str(round(m, 1)) + '.png'
    # # filename = 'LCoE_IRR_NPV/' + 'PPA_' + str(no_wind_price) + '.png'
    # plt.savefig(filename, bbox_inches='tight', dpi=300)




opt_d_cove = np.array(opt_d_cove)
opt_p_cove = np.array(opt_p_cove)
opt_cove = np.array(opt_cove)
opt_d_irr_all = np.array(opt_d_irr_all)
opt_p_irr_all = np.array(opt_p_irr_all)
opt_irr = np.array(opt_irr)
opt_d_mirr_all = np.array(opt_d_mirr_all)
opt_p_mirr_all = np.array(opt_p_mirr_all)
opt_mirr = np.array(opt_mirr)
opt_d_npv_all = np.array(opt_d_npv_all)
opt_p_npv_all = np.array(opt_p_npv_all)
opt_d_pi_all = np.array(opt_d_pi_all)
opt_p_pi_all = np.array(opt_p_pi_all)
opt_npv = np.array(opt_npv)


opt_d_irr_pos = np.array(opt_d_irr_pos)
opt_p_irr_pos = np.array(opt_p_irr_pos)
opt_d_mirr_pos = np.array(opt_d_mirr_pos)
opt_p_mirr_pos = np.array(opt_p_mirr_pos)
opt_d_npv_pos = np.array(opt_d_npv_pos)
opt_p_npv_pos = np.array(opt_p_npv_pos)
opt_d_pi_pos = np.array(opt_d_pi_pos)
opt_p_pi_pos = np.array(opt_p_pi_pos)

opt_d_irr_neg = np.array(opt_d_irr_neg)
opt_p_irr_neg = np.array(opt_p_irr_neg)
opt_d_mirr_neg = np.array(opt_d_mirr_neg)
opt_p_mirr_neg = np.array(opt_p_mirr_neg)
opt_d_npv_neg = np.array(opt_d_npv_neg)
opt_p_npv_neg = np.array(opt_p_npv_neg)
opt_d_pi_neg = np.array(opt_d_pi_neg)
opt_p_pi_neg = np.array(opt_p_pi_neg)



perc_diff_lcoe_design_pi = np.array(perc_diff_lcoe_design_pi)
perc_diff_lcoe_design_mirr = np.array(perc_diff_lcoe_design_mirr)
perc_diff_lcoe_design_npv = np.array(perc_diff_lcoe_design_npv)



opt_d_cove.dump("New_method/opt_diameter_cove_all.dat")
opt_p_cove.dump("New_method/opt_power_cove_all.dat")
opt_cove.dump("New_method/opt_cove.dat")

opt_d_irr_all.dump("New_method/opt_diameter_irr_all.dat")
opt_p_irr_all.dump("New_method/opt_power_irr_all.dat")
opt_irr.dump("New_method/opt_irr.dat")
opt_d_mirr_all.dump("New_method/opt_diameter_mirr_all.dat")
opt_p_mirr_all.dump("New_method/opt_power_mirr_all.dat")
opt_mirr.dump("New_method/opt_mirr.dat")
opt_d_npv_all.dump("New_method/opt_diameter_npv_all.dat")
opt_p_npv_all.dump("New_method/opt_power_npv_all.dat")
opt_npv.dump("New_method/opt_npv.dat")
opt_d_pi_all.dump("New_method/opt_diameter_pi_all.dat")
opt_p_pi_all.dump("New_method/opt_power_pi_all.dat")


opt_d_irr_pos.dump("New_method/opt_diameter_irr_pos.dat")
opt_p_irr_pos.dump("New_method/opt_power_irr_pos.dat")
opt_d_mirr_pos.dump("New_method/opt_diameter_mirr_pos.dat")
opt_p_mirr_pos.dump("New_method/opt_power_mirr_pos.dat")
opt_d_npv_pos.dump("New_method/opt_diameter_npv_pos.dat")
opt_p_npv_pos.dump("New_method/opt_power_npv_pos.dat")
opt_d_pi_pos.dump("New_method/opt_diameter_pi_pos.dat")
opt_p_pi_pos.dump("New_method/opt_power_pi_pos.dat")
opt_d_irr_neg.dump("New_method/opt_diameter_irr_neg.dat")
opt_p_irr_neg.dump("New_method/opt_power_irr_neg.dat")
opt_d_mirr_neg.dump("New_method/opt_diameter_mirr_neg.dat")
opt_p_mirr_neg.dump("New_method/opt_power_mirr_neg.dat")
opt_d_npv_neg.dump("New_method/opt_diameter_npv_neg.dat")
opt_p_npv_neg.dump("New_method/opt_power_npv_neg.dat")
opt_d_pi_neg.dump("New_method/opt_diameter_pi_neg.dat")
opt_p_pi_neg.dump("New_method/opt_power_pi_neg.dat")

perc_diff_lcoe_design_mirr.dump("New_method/perc_diff_lcoe_design_mirr.dat")
perc_diff_lcoe_design_npv.dump("New_method/perc_diff_lcoe_design_npv.dat")
perc_diff_lcoe_design_pi.dump("New_method/perc_diff_lcoe_design_pi.dat")


import csv

filename = "New_method/dict_irr.csv"
w = csv.writer(open(filename, "w"))
# loop over dictionary keys and values
for key, val in dict_irr.items():

    # write every key and value to file
    w.writerow([key, val])


filename = "New_method/dict_mirr.csv"
w = csv.writer(open(filename, "w"))
# loop over dictionary keys and values
for key, val in dict_mIRR.items():

    # write every key and value to file
    w.writerow([key, val])

filename = "New_method/dict_pi.csv"
w = csv.writer(open(filename, "w"))
# loop over dictionary keys and values
for key, val in dict_pi.items():

    # write every key and value to file
    w.writerow([key, val])

filename = "New_method/dict_npv.csv"
w = csv.writer(open(filename, "w"))
# loop over dictionary keys and values
for key, val in dict_npv.items():

    # write every key and value to file
    w.writerow([key, val])

filename = "New_method/dict_cove.csv"
w = csv.writer(open(filename, "w"))
# loop over dictionary keys and values
for key, val in dict_cove.items():

    # write every key and value to file
    w.writerow([key, val])



sp = 300 #Specific power in W/m2
p_sp = [10,12,14,16,18,20]
d_sp = [((4/3.142)*(p*1e6/sp))**0.5 for p in p_sp]

ref_ratio = var_fix_ratio[0,0]
var_fix_ratio_norm = var_fix_ratio/ref_ratio

ref_aep = total_aep[0,0]
total_aep_norm = total_aep/ref_aep


x_wind = [236.76,231.784,215.35]
y_wind = [13.7, 14.2, 16.2]

x_area = [224.81, 221.327]
y_area = [16, 14.6]


x_dg = [220.83, 225.31]
y_dg= [15.5, 14.9]


x_farmpower = [221.33, 222.3, 222.8, 224.8]
y_farmpower = [12.5,14, 15.9, 17.1]

x_fixedpower = 230.3
y_fixedpower = 13.9

x_fixedarea = 230.3
y_fixedarea = 17.7

# d_rotor = d_rotor[:,:-1]
# p_rated = p_rated[:,:-1]
property = IRR
#property = property[:,:-1]
# y_label = 'IRR (%)'
y_label = 'LCoE (Euros/MWh)'
# y_label = 'CoVE (Euros/MWh)'
# y_label = 'vf'
# y_label = 'NPV (M Euros)'

fs = 16
lw = 1.5
la = 0.3

opt_d_lcoe = 222.3
opt_p_lcoe = 15

n_colorbars = (max(z_data) - min(z_data))/(0.01*min(z_data))
# n_colorbars = (max(z_data_CoVE) - min(z_data_CoVE))/(0.01*min(z_data_CoVE))
# n_colorbars = (max(z_data_IRR) - min(z_data_IRR))/(0.01*max(z_data_IRR))
# n_colorbars = (max(z_data_npv) - min(z_data_npv))/(0.01*max(z_data_npv))

fig,ax = plt.subplots()

import seaborn as sns
from matplotlib.colors import ListedColormap
# my_cmap = sns.color_palette("rocket", as_cmap=True)
my_cmap = sns.color_palette("BuGn_r", as_cmap=True)
# my_cmap = sns.color_palette("mako", as_cmap=True)
# c = plt.contourf(d_rotor,p_rated,property, 50, cmap='YlOrRd')
# c = plt.contourf(d_rotor,p_rated,property, 100, cmap = my_cmap.reversed())
# c = plt.contourf(d_rotor,p_rated,property, round(n_colorbars), cmap = my_cmap.reversed())
# c = plt.contourf(d_eval,p_eval,z_pred_irr*100, round(n_colorbars)-1, cmap = my_cmap.reversed())
c = plt.contourf(d_eval,p_eval,z_pred_lcoe, round(n_colorbars)-1, cmap = my_cmap.reversed(), alpha=.5)
cbar = fig.colorbar(c)

#plt.plot(d_sp, p_sp,'k--',linewidth=lw, alpha=la,label ='Constant specific power line')

#plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
# plt.scatter(d_eval[result_deterministic[1]], p_eval[result_deterministic[0]], marker = 'o', c='w', s = 60, alpha = 0.5 , label='Baseline')
# plt.text(222, 15.7, 'Global optimum (Baseline)', horizontalalignment='center', verticalalignment='center', size = '10')
# plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')

plt.scatter(opt_d_lcoe, opt_p_lcoe, marker = 'o', c='k', s = 80, alpha = 0.5, label='LCoE')
plt.scatter(opt_d_irr_all, opt_p_irr_all, marker = 'o', c='C1', s = 30, alpha = 0.5, label='IRR')
plt.scatter(opt_d_mirr_all, opt_p_mirr_all, marker = 'o', c='C3', s = 30, alpha = 0.5, label='mIRR')
plt.scatter(opt_d_npv_all, opt_p_npv_all, marker = 'o', c='C2', s = 30, alpha = 0.5, label='NPV')
# plt.scatter(opt_d_lpoe, opt_p_lpoe, marker = 'o', c='C3', s = 30, alpha = 0.5, label='LPoE')

# plt.scatter(x_fixedpower, y_fixedpower, marker = 'o', c='k', s = 60, alpha = 0.5)
# plt.text(230, 13.5, 'Global optimum (Fixed power only)', horizontalalignment='center', verticalalignment='center', size = '10')
# plt.scatter(x_fixedarea, y_fixedarea, marker = 'o', c='k', s = 60, alpha = 0.5)
# plt.text(230, 17.2, 'Global optimum (Fixed area only)', horizontalalignment='center', verticalalignment='center', size = '10')

# plt.scatter(x_wind, y_wind, marker='o', c='k', s=20) #,  label ='Wind speed')
# plt.scatter(x_area, y_area, marker='o', c='k', s=20) #, label ='Area')
# plt.scatter(x_dg, y_dg, marker='o', c='k', s=20) #,  label ='Distance to grid')
# plt.scatter(x_farmpower, y_farmpower, marker='o', c='k', s=20) #,  label ='Farm power')

plt.xlabel('Rotor Diameter (m)', fontsize = fs)
plt.ylabel('Rated Power (MW)', fontsize = fs)
#plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
cbar.ax.set_ylabel(y_label, fontsize = fs)
# plt.legend(loc='upper left',fancybox=True, framealpha=0.5)
# plt.xlim(210, 255)
# plt.ylim(12,15.5)
plt.grid(axis = 'both', alpha = 0.1)
ax.tick_params(axis='both',direction='in', length =5)
# matplotlib.rcParams['legend.fontsize'] = 12
plt.show()

# x1 = 250
# y1 = 15
# #### single turbine (10,0.3), turbineperMW (10, -0.4), foundationperMW (10,-0.5), installation (10, -1), electrical (10,-0.7), oandm (10,-1.3), wake (-10,0.3), aep () ###
# dz1_dx = 10
# dz1_dy = -0.6
# arrow = FancyArrowPatch((x1, y1), (x1+dz1_dx, y1+dz1_dy),
#                         arrowstyle='simple', color='k', mutation_scale=10)
# ax.add_patch(arrow)
# plt.savefig('lcoe.png',bbox_inches='tight',dpi=300)
# plt.show()

#
# property = total_aep_norm
# #property = property[:,:-1]
# y_label = 'Lifetime energy production (normalized)'
#
# fs = 16
# lw = 1.5
# la = 0.3
# fig,ax = plt.subplots()
#
# import seaborn as sns
# from matplotlib.colors import ListedColormap
# #my_cmap = sns.color_palette("rocket", as_cmap=True)
# my_cmap = sns.color_palette("mako", as_cmap=True)
# #c = plt.contourf(d_rotor,p_rated,property, 50, cmap='YlOrRd')
# #c = plt.contourf(d_rotor,p_rated,property, 100, cmap = my_cmap.reversed())
# c = plt.contourf(d_rotor,p_rated,property, 50, cmap = my_cmap.reversed())
# #c = plt.contourf(D,P,property, 50, cmap = my_cmap.reversed())
# cbar = fig.colorbar(c)
#
# #plt.plot(d_sp, p_sp,'k--',linewidth=lw, alpha=la,label ='Constant specific power line')
#
# # plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
# # plt.text(229, 16, 'Global optimum', horizontalalignment='center', verticalalignment='center', size = '13')
# #plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')
#
# plt.xlabel('Rotor Diameter (m)', fontsize = fs)
# plt.ylabel('Rated Power (MW)', fontsize = fs)
# #plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
# cbar.ax.set_ylabel(y_label, fontsize = fs)
# # plt.legend(loc='upper left',fancybox=True, framealpha=0.5)
# plt.xlim(rad_values[0]*2, rad_values[-1]*2)
# #plt.ylim(10,20)
# plt.grid(axis = 'both', alpha = 0.1)
# ax.tick_params(axis='both',direction='in', length =5)
# matplotlib.rcParams['legend.fontsize'] = 12

# x1 = 250
# y1 = 15
# #### single turbine (10,0.3), turbineperMW (10, -0.4), foundationperMW (10,-0.5), installation (10, -1), electrical (10,-0.7), oandm (10,-1.3), wake (-10,0.3), aep () ###
# dz1_dx = 10
# dz1_dy = -0.6
# arrow = FancyArrowPatch((x1, y1), (x1+dz1_dx, y1+dz1_dy),
#                         arrowstyle='simple', color='k', mutation_scale=10)
# ax.add_patch(arrow)
# plt.savefig('lcoe.png',bbox_inches='tight',dpi=300)
#plt.savefig('lcoe_robustness.png',bbox_inches='tight',dpi=300)
# plt.savefig('lcoe_baseline_vs_problem_formulation.png',bbox_inches='tight',dpi=300)
# plt.savefig('IRR_Eneco_2030.png',bbox_inches='tight',dpi=300)
# plt.savefig('CoVE_Eneco_2030.png',bbox_inches='tight',dpi=300)
# plt.savefig('vf_NL.png',bbox_inches='tight',dpi=300)
# plt.savefig('NPV_Eneco_2030.png',bbox_inches='tight',dpi=300)
# plt.show()






# plt.scatter(sp_data,z_wake)
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Wake losses (%)', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# ax.tick_params(axis='both',direction='in', length =5)
# plt.show()
#
# plt.scatter(sp_data,z_aep)
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('AEP (GWh)', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# ax.tick_params(axis='both',direction='in', length =5)
# plt.show()
#
# plt.scatter(sp_data,cost_ratio_sp)
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Cost ratio (Variable to fixed)', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# ax.tick_params(axis='both',direction='in', length =5)
# plt.show()




# fig, ax = plt.subplots()
#
# n_t = n_t[0]
# infield_cable_costs = infield_cable_costs[0]
# infield_length= infield_length[0]
# ax.plot(n_t, infield_cable_costs, color = 'red')
# ax.set_xlabel('Number of turbines', fontsize = 16)
# ax.set_ylabel('Infield cable costs', color = 'red', fontsize = 16)
#
# ax2 = ax.twinx()
# ax2.plot(n_t, infield_length, color = 'blue')
# ax2.set_ylabel('Infield cable length', color = 'blue', fontsize = 16)
# plt.show()

#### try to find derivatives of functions ####
#
# func1 = var_fix_ratio + 1
# x = [r*2 for r in rad_values]
# y = power_values
#
# gradients_numerator = np.gradient(func1,x, axis=0)
#
# gradient_diameter = gradients_numerator[0]
# gradient_power = gradients_numerator[1]
#
# print(gradient_diameter)
# print(gradient_power)

# fig, (ax1, ax2) = plt.subplots(1, 2)
# ax1.plot(d_rotor, gradient_diameter)
# ax2.plot(p_rated, gradient_power)


#
#
#
# ###### Fit for AEP ####
# par = curve_fit(function, [y_data, x_data], z_aep)
# p = par[0]
# P = np.array(p_sp)
# D = np.array(d_sp)
#
# aep_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = aep_estimate[0]
# aep_normalized = [a/firstval for a in aep_estimate]
#
#
# ###### Fit for Wake ###
# par = curve_fit(function, [y_data, x_data], z_wake)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# wake_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = wake_estimate[0]
# wake_normalized = [a/firstval for a in wake_estimate]
#
# ###### Fit for mean wind speed ###
# par = curve_fit(function, [y_data, x_data], z_vmean)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# vmean_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = vmean_estimate[0]
# vmean_normalized = [a/firstval for a in vmean_estimate]
#
#
#
#
# plt.figure(num=1, figsize =(4,4))
#
# plt.plot(aep_normalized, color= 'C0', label='AEP', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
# plt.plot(wake_normalized, color = 'C1', label='Wake losses', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
# plt.plot(vmean_normalized, color = 'C2', label='Mean wind speed', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
# plt.xticks([0,1,2,3,4,5], ['10-190', '12-210', '14-225', '16-240', '18-255', '20-270'], rotation=10, fontsize = 10)
# plt.xlabel('Turbine sizes', fontsize = 14)
# plt.ylabel('Normalized quantities', fontsize = 14)
# plt.grid(axis = 'both', alpha = 0.5)
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# matplotlib.rcParams['legend.fontsize'] = 10
# plt.legend()
# # plt.savefig('aep_increase_constant_sp.png',bbox_inches='tight',dpi=300)
# plt.show()
#
#
# ###### Fit for rna and tower ###
# par = curve_fit(function, [y_data, x_data], z_rnaperMW)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# rnaperMW_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = rnaperMW_estimate[0]
# rnaperMW_normalized = [a/firstval for a in rnaperMW_estimate]
#
#
# par = curve_fit(function, [y_data, x_data], z_towerperMW)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# towerperMW_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = towerperMW_estimate[0]
# towerperMW_normalized = [a/firstval for a in towerperMW_estimate]
#
#
# ###### Fit for foundation ###
# par = curve_fit(function,[y_data, x_data], z_foundationperMW)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# foundationperMW_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = foundationperMW_estimate[0]
# foundationperMW_normalized = [a/firstval for a in foundationperMW_estimate]
#
#
#
# plt.figure(num=2, figsize=(4, 4))
#
# plt.plot(rnaperMW_normalized, color= 'C0', label='RNA costs', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
# plt.plot(towerperMW_normalized, color = 'C1', label='Tower costs', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
# plt.plot(foundationperMW_normalized, color = 'C2', label='Foundation costs', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
# plt.xticks([0,1,2,3,4,5], ['10-190', '12-210', '14-225', '16-240', '18-255', '20-270'], rotation=10, fontsize = 10)
# plt.xlabel('Turbine sizes', fontsize = 14)
# plt.ylabel('Normalized quantities', fontsize = 14)
# plt.grid(axis = 'both', alpha = 0.5)
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# matplotlib.rcParams['legend.fontsize'] = 10
# plt.legend()
# # plt.savefig('turbine_foundation_costsperMW.png',bbox_inches='tight',dpi=300)
# plt.show()
#
#
#
# ###### Fit for O&M ####
# par = curve_fit(function, [y_data, x_data], z_oandm)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# oandm_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = oandm_estimate[0]
# oandm_normalized = [a/firstval for a in oandm_estimate]
#
# ###### Fit for installation ###
# par = curve_fit(function, [y_data, x_data], z_installation)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# installation_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = installation_estimate[0]
# installation_normalized = [a/firstval for a in installation_estimate]
#
# ###### Fit for total electrical ###
# par = curve_fit(function, [y_data, x_data], z_electrical)
# P = np.array(p_sp)
# D = np.array(d_sp)
# p = par[0]
#
# electrical_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
# firstval = electrical_estimate[0]
# electrical_normalized = [a/firstval for a in electrical_estimate]
#
#
#
# plt.figure(num=3, figsize=(4, 4), dpi=300)
#
# plt.plot(oandm_normalized, color= 'C0', label='O&M costs', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
# plt.plot(installation_normalized, color = 'C1', label='Installation costs', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
# plt.plot(electrical_normalized, color = 'C2', label='Electrical costs', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
# plt.xticks([0,1,2,3,4,5], ['10-190', '12-210', '14-225', '16-240', '18-255', '20-270'], rotation=10, fontsize = 10)
# plt.xlabel('Turbine sizes', fontsize = 14)
# plt.ylabel('Normalized quantities', fontsize = 14)
# plt.grid(axis = 'both', alpha = 0.5)
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# matplotlib.rcParams['legend.fontsize'] = 10
# plt.legend()
# # plt.savefig('oandm_installation_electrical.png',bbox_inches='tight',dpi=300)
# plt.show()
#


#
# par = curve_fit(function, [x_data, y_data], z_data)
#
# sp = [283, 300, 325, 350, 375, 390] #Specific power in W/m2
# min_lcoe = []
# optimums =[]
#
# for specific_power in sp:
#     p_sp = np.linspace(10, 25, 101)
#     d_sp = [((4/3.142)*(p*1e6/specific_power))**0.5 for p in p_sp]
#
#
#     P = np.array(p_sp)
#     D = np.array(d_sp)
#     p = par[0]
#
#     lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
#     result = np.array(np.where(lcoe_estimate == np.amin(lcoe_estimate))).flatten()
#     min_lcoe.append(lcoe_estimate[result[0]])
#     optimums.append([P[result[0]], D[result[0]]])
#
# print(optimums)
#
# plt.figure(4)
#
# plt.plot(min_lcoe, color= 'C0', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
#
# plt.xticks([0,1,2,3,4,5], ['280', '300', '325', '350', '375', '390'])
# plt.xlabel('Specific Power (W/m$^2$)')
# plt.ylabel('LCoE (Euros/MWh)')
# plt.grid(axis = 'both', alpha = 0.5)
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# # matplotlib.rcParams['legend.fontsize'] = 12
# # plt.legend()
# x = [0.25,1,2,3,4,5]
# y = [a + 0.02 for a in min_lcoe]
# y[0] = y[0] -0.02
# text = ['(12.5, 237)', '(13.5,240)','(14.7,239)','(15.7,239)','(16.5,237)', '(17,235)']
# for i, txt in enumerate(text):
#     plt.annotate(txt, (x[i], y[i]))
# plt.show()


# par = curve_fit(function, [y_data, x_data], z_data)
# p = par[0]
#
# p_eval = np.linspace(10, 20, 121)
# d_eval_opt_ratedpower = [200.0, 210.0, 220.0, 230.0, 240.0, 250.0]
#
# [P, D] = np.meshgrid(p_eval, d_eval_opt_ratedpower)
# #[D, P] = np.meshgrid(d_eval_opt_ratedpower, p_eval)
#
# lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[
#     7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10] * P ** 4 + p[11] * P ** 3 * D + p[
#                     12] * P ** 2 * D ** 2 + p[13] * P * D ** 3 + p[14] * D ** 4
# result = np.where(lcoe_estimate == np.amin(lcoe_estimate, axis=1).reshape(-1, 1))
# listOfCordinates = list(zip(result[0], result[1]))
#
# p_values = []
# for lc in listOfCordinates:
#     p_values.append(P[lc])
#
# opt_ratedpower = p_values
#
# specific_power = [power*1e6/(3.142/4*dia**2) for power,dia in zip(opt_ratedpower, d_eval_opt_ratedpower)]
# # print(opt_ratedpower, specific_power)
#
# p_eval_opt_rotordia = [10, 12, 14, 16, 18, 20]
# r_eval = np.linspace(90, 150, 121)
# d_eval = [2 * r for r in r_eval]
#
# [P, D] = np.meshgrid(p_eval_opt_rotordia, d_eval)
# #[D, P] = np.meshgrid(d_eval, p_eval_opt_rotordia)
#
# lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[
#     7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10] * P ** 4 + p[11] * P ** 3 * D + p[
#                     12] * P ** 2 * D ** 2 + p[13] * P * D ** 3 + p[14] * D ** 4
#
# result = np.where(lcoe_estimate == np.amin(lcoe_estimate, axis=0))
# listOfCordinates = list(zip(result[0], result[1]))
#
# d_values = []
# for lc in listOfCordinates:
#     d_values.append(D[lc])
#
# opt_rotordia = d_values
# specific_power = [power*1e6/(3.142/4*dia**2) for power,dia in zip(p_eval_opt_rotordia, opt_rotordia)]
# # print(opt_rotordia, specific_power)
#
#
# plt.figure(num=5, figsize=(4, 4), dpi=300)
#
# plt.plot(d_eval_opt_ratedpower, opt_ratedpower, color= 'C0', label='Optimum rated power', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
# plt.plot(opt_rotordia, p_eval_opt_rotordia,color = 'C1', label='Optimum rotor diameter', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
# #plt.xticks([0,1,2,3,4,5], ['280', '300', '325', '350', '375', '390'])
# plt.xlabel('Rotor diameter (m)', fontsize = 14)
# plt.ylabel('Rated power (MW)', fontsize = 14)
# plt.grid(axis = 'both', alpha = 0.5)
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# matplotlib.rcParams['legend.fontsize'] = 10
# plt.legend()
# # plt.savefig('opt_power_opt_diameter.png',bbox_inches='tight',dpi=300)
# plt.show()

'''
##### Understanding how major quantities change w.r.t power and diameter change #####

power_deviation = np.linspace(10,20,5)
dia_deviation = np.linspace(180,300,5)

P,D = np.meshgrid(power_deviation, dia_deviation)


par = curve_fit(function, [x_data, y_data], z_aep)
p = par[0]
# P = np.array(power_deviation)
# D = 240*np.ones(len(P))

aep = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
aep_powerdeviation = aep[2,:]
firstval = aep_powerdeviation[0]
aep_normalized_powerdeviation = [a/firstval for a in aep_powerdeviation]


aep_diadeviation = aep[:,2]
firstval = aep_diadeviation[0]
aep_normalized_diadeviation = [a/firstval for a in aep_diadeviation]

#---------------#

par = curve_fit(function, [x_data, y_data], z_oandm)
p = par[0]


oandm= p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
oandm_powerdeviation = oandm[2,:]
firstval = oandm_powerdeviation[0]
oandm_normalized_powerdeviation = [a/firstval for a in oandm_powerdeviation]


oandm_diadeviation = oandm[:,2]
firstval = oandm_diadeviation[0]
oandm_normalized_diadeviation = [a/firstval for a in oandm_diadeviation]

#---------#

par = curve_fit(function, [x_data, y_data], z_bos)
p = par[0]


bos = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
bos_powerdeviation = bos[2,:]
firstval = bos_powerdeviation[0]
bos_normalized_powerdeviation = [a/firstval for a in bos_powerdeviation]


bos_diadeviation = bos[:,2]
firstval = bos_diadeviation[0]
bos_normalized_diadeviation = [a/firstval for a in bos_diadeviation]

#-------#

par = curve_fit(function, [x_data, y_data], z_turbine)
p = par[0]


turbine = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
turbine_powerdeviation = turbine[2,:]
firstval = turbine_powerdeviation[0]
turbine_normalized_powerdeviation = [a/firstval for a in turbine_powerdeviation]

turbine_diadeviation = turbine[:,2]
firstval = turbine_diadeviation[0]
turbine_normalized_diadeviation = [a/firstval for a in turbine_diadeviation]


#------#

par = curve_fit(function, [x_data, y_data], z_CAPEX)
p = par[0]


CAPEX = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
CAPEX_powerdeviation = CAPEX[2,:]
firstval = CAPEX_powerdeviation[0]
CAPEX_normalized_powerdeviation = [a/firstval for a in CAPEX_powerdeviation]


CAPEX_diadeviation = CAPEX[:,2]
firstval = CAPEX_diadeviation[0]
CAPEX_normalized_diadeviation = [a/firstval for a in CAPEX_diadeviation]

P = np.array(power_deviation)
D = np.array(dia_deviation)
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_title('Effect of power variations')
ax2.set_title('Effect of diameter variations')

ax1.plot(P, turbine_normalized_powerdeviation, color= 'C0', label='Turbine costs', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
ax1.plot(P, bos_normalized_powerdeviation, color= 'C1', label='BoS costs', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
ax1.plot(P, CAPEX_normalized_powerdeviation, color= 'C2', label='Farm CAPEX', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
ax1.plot(P, oandm_normalized_powerdeviation, color= 'C3', label='O&M costs', marker = 'o',markerfacecolor = 'C3', markeredgecolor = 'black')
ax1.plot(P, aep_normalized_powerdeviation, color= 'C4', label='AEP', marker = 'o',markerfacecolor = 'C4', markeredgecolor = 'black')
ax1.set(xlabel='Rated power', ylabel='Normalized quantities')
ax2.plot(D, turbine_normalized_diadeviation, color= 'C0', label='Turbine costs', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
ax2.plot(D, bos_normalized_diadeviation, color= 'C1', label='BoS costs', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
ax2.plot(D, CAPEX_normalized_diadeviation, color= 'C2', label='Farm CAPEX', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
ax2.plot(D, oandm_normalized_diadeviation, color= 'C3', label='O&M costs', marker = 'o',markerfacecolor = 'C3', markeredgecolor = 'black')
ax2.plot(D, aep_normalized_diadeviation, color= 'C4', label='AEP', marker = 'o',markerfacecolor = 'C4', markeredgecolor = 'black')
ax2.set(xlabel='Rotor diameter', ylabel='Normalized quantities')
handles, labels = ax2.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center')
#plt.legend()
ax1.text(17, 0.95, 'Rotor diameter: 240 m', horizontalalignment='center', verticalalignment='center', size = '12')
ax2.text(220, 2.27, 'Rated power: 15 MW', horizontalalignment='center', verticalalignment='center', size = '12')
plt.show()

# plt.xlabel('Rotor diameter (m)')
# plt.ylabel('Rated power (MW)')
# plt.grid(axis = 'both', alpha = 0.5)
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# matplotlib.rcParams['legend.fontsize'] = 12
# plt.legend()
# plt.show()'''

###################### OPTIMUM COMPARISON ############

opt_d_lcoe = 230
opt_p_lcoe = 13.8

opt_d_cove_nl = 232
opt_p_cove_nl = 13.7

opt_d_irr_nl = 238
opt_p_irr_nl = 14.1

opt_d_npv_nl = 242
opt_p_npv_nl = 13.9


opt_d_cove_dk = 232
opt_p_cove_dk = 13.6

opt_d_irr_dk = 239
opt_p_irr_dk = 14.2

opt_d_npv_dk = 241
opt_p_npv_dk = 14


opt_d_cove_2030_nl = 246
opt_p_cove_2030_nl  = 11.8

opt_d_irr_2030_nl  = 249
opt_p_irr_2030_nl = 12

opt_d_npv_2030_nl = 259
opt_p_npv_2030_nl = 11.6


x_nl = [opt_d_cove_nl, opt_d_irr_nl, opt_d_npv_nl]
y_nl = [opt_p_cove_nl, opt_p_irr_nl, opt_p_npv_nl]

x_dk = [opt_d_cove_dk, opt_d_irr_dk, opt_d_npv_dk]
y_dk = [opt_p_cove_dk, opt_p_irr_dk, opt_p_npv_dk]

x_2030_nl = [opt_d_cove_2030_nl, opt_d_irr_2030_nl, opt_d_npv_2030_nl]
y_2030_nl = [opt_p_cove_2030_nl, opt_p_irr_2030_nl, opt_p_npv_2030_nl]


# fig,ax = plt.subplots(nrows =1, ncols= 1, figsize=(5.3,4.5))

#
# #plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
# plt.scatter(opt_d_lcoe, opt_p_lcoe, marker = 'o', c='k', s = 80, alpha = 0.5, label='LCoE')
# plt.scatter(x_nl, y_nl, marker = 'o', c='C0', s = 60, alpha = 0.5, label='NL-2019')
# plt.scatter(x_dk, y_dk, marker = '*', c='C1', s = 60, alpha = 0.5, label='DK-2019')
# plt.scatter(x_2030_nl, y_2030_nl, marker = '^', c='C2', s = 60, alpha = 0.5, label='NL-2030')
# plt.text(222, 15.7, 'Global optimum (Baseline)', horizontalalignment='center', verticalalignment='center', size = '10')
# plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')



# plt.xlabel('Rotor Diameter (m)', fontsize = fs)
# plt.ylabel('Rated Power (MW)', fontsize = fs)
# #plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
# cbar.ax.set_ylabel(y_label, fontsize = fs)
#
# plt.grid(axis = 'both', alpha = 0.1)
# ax.tick_params(axis='both',direction='in', length =5)
# plt.legend(fontsize = fs)
# plt.savefig('optimum_comparison.png',bbox_inches='tight',dpi=300)
# plt.show()