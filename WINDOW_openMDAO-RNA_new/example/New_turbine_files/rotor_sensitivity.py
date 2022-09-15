'''
Use this script to check the sensitivity of the design optimum to change in rotor model form and parameters

-The deterministic results from the turbine files are read into matrices
- For each rotor diameter, a range of blade mass values are defined. This is defined based on uncertainties in the mass
scaling coefficient and the initial value of the 15 MW - 240 m reference turbine. The scaling coefficient with R ranges
from 2-3 and the initial blade mass of the 15 MW - 240 m rotor ranges from 60-70 tonnes.
- For every simulation, a random value from the mass range (for the respective rotor diameter) is picked, and the LCoE is recalculated.
- Once a set of simulation is complete (running it for 10-20 MW and 180-300 m), the optimum power for each rotor diameter
and the global optimum is calculated.
- This set is then repeated about n times to try out every possible combination of blade mass values from the defined range

- It is assumed that this change in blade mass because of the uncertainties doesn't affect the other farm costs. However,
it should be kept in mind that this is not completely true. The change in blade mass changes the RNA mass and hence,
the tower and support struc. mass (the change is found to be 1-2 % though). Also, a change in turbine and farm CAPEX
changes other financial costs that are a % share of the total CAPEX. This effect is also ignored.
'''
import random

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

power_values = [10, 11.11, 12.5, 14.28, 16.67, 20, 25]
rad_values = [90.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]
trans_efficiency = 0.95

p_rated = np.zeros((len(rad_values), len(power_values)))
d_rotor = np.zeros((len(rad_values), len(power_values)))
n_t = np.zeros((len(rad_values), len(power_values)))
rated_ws = np.zeros((len(rad_values), len(power_values)))
farm_area = np.zeros((len(rad_values), len(power_values)))

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

        idx = var.index('v_rated')
        rated_ws[idx_diameter, idx_power] = data[idx]

        idx = var.index('a_farm')
        farm_area[idx_diameter, idx_power] = data[idx]


        # idx = var.index('O&M Costs')
        # oandm_costs[idx_diameter, idx_power] = data[idx]
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

        num[idx_diameter, idx_power] = lcoe[idx_diameter, idx_power]*total_aep[idx_diameter, idx_power] # - 5e5*farm_area[idx_diameter, idx_power]
        lcoe[idx_diameter, idx_power] = num[idx_diameter, idx_power]/total_aep[idx_diameter, idx_power]

        x_data.append(p)
        y_data.append(r * 2)
        z_data.append(lcoe[idx_diameter, idx_power])


def function(data, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14):
    x = data[0]
    y = data[1]
    return p0 + p1 * x + p2 * y + p3 * x ** 2 + p4 * x * y + p5 * y ** 2 + p6 * x ** 3 + p7 * x ** 2 * y + p8 * x * y ** 2 + p9 * y ** 3 + p10*x**4 + p11*x**3*y + p12*x**2*y**2 + p13*x*y**3 + p14*y**4


# get fit parameters from scipy curve fit
par = curve_fit(function, [x_data, y_data], z_data)

p_eval = np.linspace(10, 20, 101)
r_eval = np.linspace(90, 150, 121)
d_eval = [2 * r for r in r_eval]

[P, D] = np.meshgrid(p_eval, d_eval)

p = par[0]

lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4

result_deterministic = np.array(np.where(lcoe_estimate == np.amin(lcoe_estimate))).flatten()
global_optimum_deterministic = [d_eval[result_deterministic[0]], p_eval[result_deterministic[1]]]
print('Deterministic optimum after surface fit:',p_eval[result_deterministic[1]], d_eval[result_deterministic[0]])




##### ROTOR SENSITIVITY #########

coeff_low = 2
coeff_high = 3.5
coeff_geom_upscaling = 3

ref_lowmass = 50
ref_highmass = 80
ref_radius = 120
ref_ratedws = 10.43
ref_mass_blade = 62186
ref_cost_blade = 985696.556741233

mass_uncertainty = 0.2 #in percentage

lower_bound = np.zeros(len(rad_values))
upper_bound = np.zeros(len(rad_values))

# for idx in range(len(rad_values)):
#     if rad_values[idx]<=ref_radius:
#         lower_bound[idx] = ref_mass_blade*(rad_values[idx]/ref_radius)**coeff_high
#         upper_bound[idx] = ref_mass_blade*(rad_values[idx]/ref_radius)**coeff_low
#
#     else:
#         lower_bound[idx] = ref_mass_blade*(rad_values[idx]/ref_radius)**coeff_low
#         upper_bound[idx] = ref_mass_blade*(rad_values[idx]/ref_radius)**coeff_high

for idx in range(len(rad_values)):
    if rad_values[idx]==ref_radius:
        lower_bound[idx] = ref_mass_blade
        upper_bound[idx] = ref_mass_blade


    else:
        lower_bound[idx] = (1-mass_uncertainty)*ref_mass_blade*(rad_values[idx]/ref_radius)**coeff_geom_upscaling
        upper_bound[idx] = (1+mass_uncertainty)*ref_mass_blade*(rad_values[idx]/ref_radius)**coeff_geom_upscaling



##### RUN MONTE CARLO #####





global_optimum = []
p_eval_opt_rotordia = [10, 12, 14, 16, 18, 20]
d_eval_opt_ratedpower = [200.0, 210.0, 220.0, 230.0, 240.0, 250.0]


coeff_values = np.linspace(coeff_low, coeff_high, 4)
coeff_values = coeff_values.tolist()
mass_weightage_values = np.linspace(0.6,1,8)
mass_weightage_values = mass_weightage_values.tolist()
nonmass_coeff_values = np.linspace(1.5,4, 11)
nonmass_coeff_values = nonmass_coeff_values.tolist()
new_ref_cost_values = np.linspace(0.75 * ref_cost_blade, 1.25 * ref_cost_blade, 6)
new_ref_cost_values = new_ref_cost_values.tolist()

import itertools

all_lists = [mass_weightage_values, nonmass_coeff_values, new_ref_cost_values]
all_combinations = list(itertools.product(*all_lists))

n_runs = len(all_combinations)
opt_rotordia = np.zeros((n_runs, len(p_eval_opt_rotordia)))
opt_ratedpower = np.zeros((n_runs, len(d_eval_opt_ratedpower)))

for idx in range(n_runs):
    values = all_combinations[idx]
    #mass_scalingcoeff = np.random.choice(coeff_values)
    mass_weightage = values[0]
    exponent_nonmass_costs = values[1]
    new_ref_cost_blade = values[2]
    new_lcoe = np.zeros((len(rad_values), len(power_values)))
    new_num = np.zeros((len(rad_values), len(power_values)))
    x_data = []
    y_data = []
    z_data = []

    for r in rad_values:
        idx_diameter = rad_values.index(r)
        low = lower_bound[idx_diameter]
        high = upper_bound[idx_diameter]
        guess_blade_mass = random.uniform(low,high)

        for p in power_values:

            idx_power = power_values.index(p)


            regular_blade_mass = (ref_mass_blade*(r/120)**3)*(rated_ws[idx_diameter, idx_power]/ref_ratedws)**2
            old_blade_costs = 0.6*ref_cost_blade*(regular_blade_mass/65000) + 0.4*ref_cost_blade*(r/120)**2

            #new_blade_mass = (ref_mass_blade*(r/120)**mass_scalingcoeff)*(rated_ws[idx_diameter, idx_power]/ref_ratedws)**2
            new_blade_mass = guess_blade_mass*(rated_ws[idx_diameter, idx_power]/ref_ratedws)**2
            new_blade_costs = mass_weightage*new_ref_cost_blade*(new_blade_mass/65000) + (1-mass_weightage)*new_ref_cost_blade*(r/120)**exponent_nonmass_costs





            new_num[idx_diameter, idx_power] = num[idx_diameter, idx_power] - old_blade_costs * 3*n_t[idx_diameter, idx_power]*0.88 + new_blade_costs*3*n_t[idx_diameter, idx_power]*0.88
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


    p_eval = np.linspace(10,25,151)
    r_eval = np.linspace(90,150,200)
    d_eval = [2*r for r in r_eval]

    [P,D] = np.meshgrid(p_eval, d_eval)

    lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
    result = np.array(np.where(lcoe_estimate == np.amin(lcoe_estimate))).flatten()
    global_optimum.append([p_eval[result[1]], d_eval[result[0]]])

    np.savetxt("global_optimum_rotor_sensitivity.csv", global_optimum, delimiter=",")


    [P, D] = np.meshgrid(p_eval_opt_rotordia, d_eval)
    lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
    result = np.where(lcoe_estimate == np.amin(lcoe_estimate, axis=0))
    listOfCordinates = list(zip(result[0], result[1]))


    d_values = []
    for lc in listOfCordinates:
        d_values.append(D[lc])

    opt_rotordia[idx] = d_values


    np.savetxt("opt_rotordia_perPrated_rotor_sensitivity.csv", opt_rotordia)


    [P, D] = np.meshgrid(p_eval, d_eval_opt_ratedpower)
    lcoe_estimate= p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
    result = np.where(lcoe_estimate == np.amin(lcoe_estimate, axis=1).reshape(-1,1))
    listOfCordinates = list(zip(result[0], result[1]))


    p_values = []
    for lc in listOfCordinates:
        p_values.append(P[lc])

    opt_ratedpower[idx] = p_values

    np.savetxt("opt_ratedpower_perrotordiameter_rotor_sensitivity.csv", opt_ratedpower)



    # listOfCordinates = list(zip(result[0], result[1]))
    # # travese over the list of cordinates
    # for cord in listOfCordinates:
    #     print(cord)
y_coords = [p[0] for p in global_optimum]
x_coords = [p[1] for p in global_optimum]


import matplotlib.pyplot as plt
plt.figure(1)
plt.scatter(x_coords, y_coords, marker='o', c='black', s=10)
plt.plot(global_optimum_deterministic[0], global_optimum_deterministic[1], 'o', color='red', label='Deterministic optimum')
plt.xlabel('Rotor diameter (m)')
plt.ylabel('Rated power (MW)')
plt.title('Uncertainty in global optimum w.r.t Rotor parameters')
plt.legend()
plt.show()


#### Box plots ####


plt.figure(2)

plt.boxplot(opt_rotordia, vert=0, whis=3)
plt.yticks([1,2,3,4,5,6],['10', '12', '14', '16', '18', '20'])
plt.xlabel('Rotor diameter (m)')
plt.ylabel('Rated power (MW)')
plt.title('Uncertainty in optimum rotor diameter w.r.t Rotor parameters')
plt.show()

plt.figure(3)

plt.boxplot(opt_ratedpower, whis=2)
plt.xticks([1,2,3,4,5,6],['200', '210', '220', '230', '240', '250'])
plt.xlabel('Rotor diameter (m)')
plt.ylabel('Rated power (MW)')
plt.title('Uncertainty in optimum rated power w.r.t Rotor parameters')
plt.show()