'''
Use this script to check the sensitivity of the design optimum to change in O&M model form and parameters

-The deterministic results from the turbine files are read into matrices
- The uncertainties in fixed operational costs, scaling of day-rates with rotor diameter, and in failure rates are tested
- The O&M function is re-written to include these uncertainties.
- N combinations of these values are run to determine the effect of uncertainty in O&M on the global optimum
'''


import numpy as np


def oandm_detailed(rotor_diameter, rna_costs, array_cable_costs, distance_to_harbour, n_t, fixed_costs, replacement_perc, day_rate, alpha):


    ####### INPUT PARAMS ######

    shift_time = 24 # shift time
    pound_to_euro = 1.17  # to convert BVG estimates to euros
    n_technicians = 50 * (n_t / 100)  # taken from BVG. Scales with Number of turbines
    salary_technician = 1e5  # salary in euros per technician per year

    dayrate_ctv = 3000
    dayrate_wtiv = 4.2e5
    dayrate_jackup = 1.4e5
    dayrate_clv = 100000
    dayrate_dsv = 75000

    dayrate_hlv = day_rate * (rotor_diameter/200)**alpha  # https://journals-sagepub-com.tudelft.idm.oclc.org/doi/pdf/10.1260/0309-524X.39.1.1


    mobilization_wtiv = 2e6
    mobilization_jackup = 500000
    mobilization_dsv = 225000
    mobilization_clv = 550000
    mobilization_hlv = 500000

    # speed of different vessels in km/h
    speed_ctv = 40
    speed_hlv = 7
    speed_clv = 6

    # travel time for one round-trip in hours

    traveltime_ctv = 2 * distance_to_harbour / speed_ctv
    traveltime_hlv = 2 * distance_to_harbour / speed_hlv
    traveltime_clv = 2 * distance_to_harbour / speed_clv


    ###### OPERATIONAL COSTS ####
    #fixed_costs = 25e6*pound_to_euro  # insurance, logistics, training, survey, etc. taken from BVG
    operational_costs = fixed_costs #insurance, logistics, training, survey, etc. (Average of High estimates taken from IEA Task 26 baseline document and BVG)

    #### PREVENTIVE MAINTENANCE AND CORRECTIVE INSPECTION ###

    service_hours_pertub = 50 #services hours per turbine
    service_hours_substation = 30*4 # 30 hours and 4 expected trips
    service_hours_structure = 4 #expected hours for the support structure
    total_service_hours = (service_hours_structure + service_hours_pertub)*n_t + service_hours_substation
    no_ctv = 2
    total_no_trips = 5
    no_days = np.ceil(total_service_hours/no_ctv/shift_time + (traveltime_ctv*no_ctv*total_no_trips/24))

    cost_inspection_preventive = no_days*no_ctv*dayrate_ctv

    rp_preinspection = 7.5
    ene_preinspection = 0.4
    no_ctvs = 1
    total_no_trips = 1
    no_days = np.ceil(ene_preinspection* rp_preinspection*n_t/shift_time/no_ctvs + (traveltime_ctv*no_ctv*total_no_trips/24))

    cost_inspection_corrective = no_days*dayrate_ctv

    cost_inspection = cost_inspection_corrective + cost_inspection_preventive


    ##### TURBINE CORRECTIVE MAINTENANCE ####

    # ene stands for expected number of events/turbine/year
    # rp stands for repair time in hours
    # sp stands for spare part cost (Expressed as a % of RNA costs)


    ene_minor_repair = 3
    rp_minor_repair = 7.5
    sp_minor_repair = 0.001

    no_ctvs = 2
    total_no_trips = 10
    no_days = np.ceil(ene_minor_repair*rp_minor_repair*n_t/shift_time/no_ctvs + traveltime_ctv*no_ctv*total_no_trips/24)
    cost_vessels_minor_repair = no_days*no_ctvs*dayrate_ctv
    cost_sp_minor_repair = sp_minor_repair*rna_costs

    ene_major_repair = 0.3
    rp_major_repair = 22
    sp_major_repair = 0.005

    no_ctvs = 2
    total_no_trips = 1
    no_days = np.ceil(ene_major_repair*rp_major_repair*n_t/shift_time/no_ctvs + traveltime_ctv*no_ctv*total_no_trips/24)
    cost_vessels_major_repair = no_days*no_ctvs*dayrate_ctv
    cost_sp_major_repair = sp_major_repair*rna_costs


    ene_major_replacement = replacement_perc #between 5 and 10 %
    rp_major_replacement = 34
    sp_major_replacement = 0.1


    no_instances = ene_major_replacement*n_t
    no_mobilizations = np.ceil(no_instances/1)  # depends on the strategy. Assumed that the operator clubs major repairs and calls for a HLV once for x turbine replacements
    no_days = np.ceil(rp_major_replacement/shift_time + traveltime_hlv/24)
    cost_vessels_major_replacement = (no_days*dayrate_hlv + mobilization_hlv*2)*no_mobilizations
    cost_sp_major_replacement = sp_major_replacement*rna_costs*no_instances

    total_cost_turbine_maintenance = cost_vessels_minor_repair + cost_vessels_major_repair + cost_vessels_major_replacement + cost_sp_minor_repair + cost_sp_major_repair + cost_sp_major_replacement
    total_cost_turbine_maintenance_sp = cost_sp_minor_repair + cost_sp_major_repair + cost_sp_major_replacement

    ##### BOS CORRECTIVE MAINTENANCE ####

    ene_scour_repair = 0.023
    rp_scour_repair = 8

    no_instances = ene_scour_repair*n_t
    no_days =np.ceil(rp_scour_repair/shift_time + traveltime_clv/24)
    cost_vessels_scour_repair = (no_days*dayrate_dsv + mobilization_dsv*2)*no_instances

    ene_cable_replacement = 0.0004
    rp_cable_replacement = 32

    no_instances = ene_cable_replacement*n_t
    no_days = np.ceil(rp_cable_replacement/shift_time)
    cost_vessels_cable_replacement = (no_days*dayrate_clv + mobilization_clv*2)*no_instances
    perc_cable_down = 6/n_t # one cable connects 6 turbines in a row. Any fault needs to have cable length equivalent to 6 turbines replaced
    cost_sp_cable_replacement = perc_cable_down*array_cable_costs*no_instances

    cost_transformer_repair = 200000 #from IEA Baseline document

    total_cost_bos_maintenance = cost_sp_cable_replacement + cost_vessels_cable_replacement + cost_vessels_scour_repair + cost_transformer_repair
    total_cost_bos_maintenance_sp = cost_sp_cable_replacement + cost_transformer_repair


    vessel_cost = cost_vessels_minor_repair + cost_vessels_major_repair + cost_vessels_major_replacement + cost_vessels_scour_repair + cost_vessels_cable_replacement
    n_tech = np.ceil(n_technicians*(n_t/100)) #number of technicians scale with number of turbines
    costs_om = operational_costs + cost_inspection + vessel_cost + total_cost_turbine_maintenance_sp + total_cost_bos_maintenance_sp  + n_tech*salary_technician

    # print('Operational costs:', operational_costs)
    # print('Inspection cost:', cost_inspection)
    # print('vessel costs:', vessel_cost)
    # print('Turbine maintenance spare part:', total_cost_turbine_maintenance_sp)
    # print('BoS maintenance spare part:', total_cost_bos_maintenance_sp)
    # print('Salary technician:', salary_technician*n_technicians)

    availability = 0.97  # for the same farm

    return costs_om, availability




import random

import pandas as pd
from scipy.optimize import curve_fit

power_values = [10, 11.11, 12.5, 14.28, 16.67, 20]
rad_values = [90.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]
trans_efficiency = 0.95

p_rated = np.zeros((len(rad_values), len(power_values)))
d_rotor = np.zeros((len(rad_values), len(power_values)))
n_t = np.zeros((len(rad_values), len(power_values)))
rated_ws = np.zeros((len(rad_values), len(power_values)))
farm_area = np.zeros((len(rad_values), len(power_values)))

rna_costs = np.zeros((len(rad_values), len(power_values)))
infield_costs = np.zeros((len(rad_values), len(power_values)))
oandm_costs = np.zeros((len(rad_values), len(power_values)))
farm_capex = np.zeros((len(rad_values), len(power_values)))
decom = np.zeros((len(rad_values), len(power_values)))

aep = np.zeros((len(rad_values), len(power_values)))
lcoe = np.zeros((len(rad_values), len(power_values)))

num = np.zeros((len(rad_values), len(power_values)))
total_aep = np.zeros((len(rad_values), len(power_values)))

x_data = []
y_data = []
z_data = []


for p in power_values:
    for r in rad_values:
        filename = 'parameters_' + str(p) + '_' + str(r*2) + '.csv'
        df = pd.read_csv(filename, header=None,names=['variable', 'data', 'description'])
        variable = df['variable']
        data = df['data']

        var = pd.Series.tolist(variable)

        idx_power = power_values.index(p)
        idx_diameter = rad_values.index(r)

        ###### assign values in the matrix #####

        p_rated[idx_diameter,idx_power] = p
        d_rotor[idx_diameter,idx_power] = r*2

        idx = var.index('n_t')
        n_t[idx_diameter,idx_power] = data[idx]

        idx = var.index('a_farm')
        farm_area[idx_diameter, idx_power] = data[idx]

        idx = var.index('costs_RNA_elec')
        rna_costs[idx_diameter,idx_power] = data[idx]

        idx = var.index('costs_infield_cable')
        infield_costs[idx_diameter,idx_power] = data[idx]


        idx = var.index('O&M Costs')
        oandm_costs[idx_diameter, idx_power] = data[idx]
        #
        # idx = var.index('costs_totalinvestment_elec:')
        # farm_capex[idx_diameter, idx_power] = data[idx]

        idx = var.index('aep_withwake')
        aep[idx_diameter, idx_power] = data[idx]*1e3/trans_efficiency #in MWh

        # idx = var.index('costs_decom_elec')
        # decom[idx_diameter, idx_power] = data[idx]

        idx = var.index('lcoe')
        lcoe[idx_diameter, idx_power] = data[idx]*10 #in Eur/MWh

        aep_yearly = np.zeros(25)
        for idx in range(1,26):
            aep_yearly[idx-1] = aep[idx_diameter, idx_power]/(1+0.05)**idx
        total_aep[idx_diameter, idx_power] = np.sum(aep_yearly)

        num[idx_diameter, idx_power] = lcoe[idx_diameter, idx_power]*total_aep[idx_diameter, idx_power] #- 5e5*farm_area[idx_diameter, idx_power]
        lcoe[idx_diameter, idx_power] = num[idx_diameter, idx_power]/total_aep[idx_diameter, idx_power]

        x_data.append(p)
        y_data.append(r * 2)
        z_data.append(lcoe[idx_diameter, idx_power])


def function(data, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14):
    x = data[0]
    y = data[1]
    return p0 + p1 * x + p2 * y + p3 * x ** 2 + p4 * x * y + p5 * y ** 2 + p6 * x ** 3 + p7 * x ** 2 * y + p8 * x * y ** 2 + p9 * y ** 3 + p10 * x ** 4 + p11 * x ** 3 * y + p12 * x ** 2 * y ** 2 + p13 * x * y ** 3 + p14 * y ** 4


# get fit parameters from scipy curve fit
par = curve_fit(function, [x_data, y_data], z_data)

p_eval = np.linspace(10, 20, 101)
r_eval = np.linspace(90, 150, 121)
d_eval = [2 * r for r in r_eval]

[P, D] = np.meshgrid(p_eval, d_eval)

p = par[0]

lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[
    7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10] * P ** 4 + p[11] * P ** 3 * D + p[
                    12] * P ** 2 * D ** 2 + p[13] * P * D ** 3 + p[14] * D ** 4

result_deterministic = np.array(np.where(lcoe_estimate == np.amin(lcoe_estimate))).flatten()
global_optimum_deterministic = [d_eval[result_deterministic[0]], p_eval[result_deterministic[1]]]
print('Deterministic optimum after surface fit:', p_eval[result_deterministic[1]], d_eval[result_deterministic[0]])

###### O&M sensitivity #####



lb_fixed_costs = 10e6
ub_fixed_costs = 30e6
fixed_costs_values = np.linspace(lb_fixed_costs, ub_fixed_costs, 9)
fixed_costs_values = fixed_costs_values.tolist()

lb_replacement_perc = 0.04
ub_replacement_perc = 0.10
replacement_perc_values = np.linspace(lb_replacement_perc, ub_replacement_perc, 4)
replacement_perc_values = replacement_perc_values.tolist()

lb_day_rate = 100000
ub_day_rate = 300000
day_rate_values = np.linspace(lb_day_rate, ub_day_rate, 5)
day_rate_values = day_rate_values.tolist()

lb_alpha = 0
ub_alpha = 2
alpha_values = np.linspace(lb_alpha, ub_alpha, 5)
alpha_values = alpha_values.tolist()

import itertools

all_lists = [fixed_costs_values, replacement_perc_values, day_rate_values, alpha_values]
all_combinations = list(itertools.product(*all_lists))





n_runs = len(all_combinations)


global_optimum = []
p_eval_opt_rotordia = [10, 12, 14, 16, 18, 20]
opt_rotordia = np.zeros((n_runs, len(p_eval_opt_rotordia)))



for idx in range(n_runs):

    values = all_combinations[idx]
    distance_to_harbour = 40  # in km
    fixed_costs = values[0]
    replacement_perc = values[1]
    day_rate = values[2]
    alpha = values[3]
    new_lcoe = np.zeros((len(rad_values), len(power_values)))
    new_num = np.zeros((len(rad_values), len(power_values)))
    x_data = []
    y_data = []
    z_data = []



    for r in rad_values:
        idx_diameter = rad_values.index(r)

        for p in power_values:
            idx_power = power_values.index(p)

            oandm_yearly = oandm_costs[idx_diameter, idx_power]
            N_t = n_t[idx_diameter,idx_power]
            RNA_costs = rna_costs[idx_diameter,idx_power]/N_t
            array_cable_costs = infield_costs[idx_diameter,idx_power]


            oandm_discounted = []
            for l in range(1,25):
                oandm_discounted.append(oandm_yearly/(1+0.05)**l)

            old_oandm = sum(oandm_discounted)

            [new_oandm_yearly, availability] = oandm_detailed(2*r, RNA_costs, array_cable_costs, distance_to_harbour,
                                                      N_t, fixed_costs, replacement_perc, day_rate, alpha)

            oandm_discounted = []
            for l in range(1, 25):
                oandm_discounted.append(new_oandm_yearly / (1 + 0.05) ** l)

            new_oandm = sum(oandm_discounted)



            new_num[idx_diameter, idx_power] = num[idx_diameter, idx_power] - old_oandm + new_oandm
            new_lcoe[idx_diameter, idx_power] = new_num[idx_diameter, idx_power]/total_aep[idx_diameter, idx_power]




            x_data.append(p)
            y_data.append(r*2)
            z_data.append(new_lcoe[idx_diameter, idx_power])


    def function(data, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14):
        x = data[0]
        y = data[1]
        return p0 + p1 * x + p2 * y + p3 * x ** 2 + p4 * x * y + p5 * y ** 2 + p6 * x ** 3 + p7 * x ** 2 * y + p8 * x * y ** 2 + p9 * y ** 3 + p10 * x ** 4 + p11 * x ** 3 * y + p12 * x ** 2 * y ** 2 + p13 * x * y ** 3 + p14 * y ** 4


    # get fit parameters from scipy curve fit
    par = curve_fit(function, [x_data, y_data], z_data)
    p = par[0]

    p_eval = np.linspace(10,20,101)
    r_eval = np.linspace(90,150,121)
    d_eval = [2*r for r in r_eval]

    [P,D] = np.meshgrid(p_eval, d_eval)

    lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
    result = np.array(np.where(lcoe_estimate == np.amin(lcoe_estimate))).flatten()
    global_optimum.append([p_eval[result[1]], d_eval[result[0]]])



    np.savetxt("global_optimum_oandm_sensitivity.csv", global_optimum, delimiter=",")


    [P, D] = np.meshgrid(p_eval_opt_rotordia, d_eval)
    lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
    result = np.where(lcoe_estimate == np.amin(lcoe_estimate, axis=0))
    listOfCordinates = list(zip(result[0], result[1]))


    d_values = []
    for lc in listOfCordinates:
        d_values.append(D[lc])

    opt_rotordia[idx] = d_values

np.savetxt("opt_rotordia_perPrated_oandm_sensitivity.csv", opt_rotordia)

    # listOfCordinates = list(zip(result[0], result[1]))
    # # travese over the list of cordinates
    # for cord in listOfCordinates:
    #     print(cord)
y_coords = [p[0] for p in global_optimum]
x_coords = [p[1] for p in global_optimum]


import matplotlib.pyplot as plt
plt.figure(1)
plt.scatter(x_coords, y_coords, marker='o', c='b', s=10)
plt.plot(global_optimum_deterministic[0], global_optimum_deterministic[1], 'o', color='red', label='Deterministic optimum')
plt.xlabel('Rotor diameter (m)')
plt.ylabel('Rated power (MW)')
plt.title('Uncertainty in global optimum w.r.t O&M parameters')
plt.legend()
plt.show()


#### Rotor diameter horizontal bars ####

width_bar = np.amax(opt_rotordia, axis=0) - np.amin(opt_rotordia, axis=0)
start_point = np.amin(opt_rotordia, axis=0)


plt.figure(2)
plt.barh(p_eval_opt_rotordia, width_bar, height=0.5, left=start_point, edgecolor='black')
plt.xlabel('Rotor diameter (m)')
plt.ylabel('Rated power (MW)')
plt.title('Uncertainty in optimum rotor diameter w.r.t O&M parameters')
plt.show()