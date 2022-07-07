import pandas as pd
import numpy as np

power_values = [10, 11.11, 12.5, 14.28, 16.67, 20]
rad_values = [90.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]

p_rated = np.zeros((len(rad_values), len(power_values)))
d_rotor = np.zeros((len(rad_values), len(power_values)))
n_t = np.zeros((len(rad_values), len(power_values)))

rotor_costs = np.zeros((len(rad_values), len(power_values)))
RNA_costs = np.zeros((len(rad_values), len(power_values)))
tower_costs = np.zeros((len(rad_values), len(power_values)))
other_turbine_costs = np.zeros((len(rad_values), len(power_values))) #profits, warranty, assembly, etc.
turbine_costs_perMW = np.zeros((len(rad_values), len(power_values)))
turbine_costs_singleturbine = np.zeros((len(rad_values), len(power_values)))
foundation_costs = np.zeros((len(rad_values), len(power_values)))
foundation_costs_perMW = np.zeros((len(rad_values), len(power_values)))
infield_cable_costs = np.zeros((len(rad_values), len(power_values)))
total_electrical_costs = np.zeros((len(rad_values), len(power_values)))

installation_turbine_costs = np.zeros((len(rad_values), len(power_values)))
installation_foundation_costs = np.zeros((len(rad_values), len(power_values)))
installation_electrical_costs = np.zeros((len(rad_values), len(power_values)))
total_installation_costs = np.zeros((len(rad_values), len(power_values)))
installation_costs_perMW = np.zeros((len(rad_values), len(power_values)))

projectdev_costs = np.zeros((len(rad_values), len(power_values)))
other_farm_costs = np.zeros((len(rad_values), len(power_values))) #insurance, contingency, etc.

oandm_costs = np.zeros((len(rad_values), len(power_values)))
farm_capex = np.zeros((len(rad_values), len(power_values)))

wake_losses = np.zeros((len(rad_values), len(power_values)))
aep = np.zeros((len(rad_values), len(power_values)))

lcoe = np.zeros((len(rad_values), len(power_values)))

for p in power_values:
    for r in rad_values:
        filename = 'parameters_' + str(p) + '_' + str(r) + '.csv'
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

        idx = var.index('cost_rotor')
        rotor_costs[idx_diameter, idx_power] = data[idx]*n_t[idx_diameter,idx_power]*0.88 #usd to euro

        idx = var.index('costs_RNA_elec')
        RNA_costs[idx_diameter, idx_power] = data[idx]/1e6/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power]

        idx = var.index('costs_tower')
        tower_costs[idx_diameter, idx_power] = data[idx]*n_t[idx_diameter,idx_power]

        idx = var.index('costs_other_turbine_elec')
        other_turbine_costs[idx_diameter, idx_power] = data[idx]

        total_turbine_costs = RNA_costs[idx_diameter, idx_power] + tower_costs[idx_diameter, idx_power] + other_turbine_costs[idx_diameter, idx_power] #total cost of wind turbines in the farm
        turbine_costs_perMW[idx_diameter,idx_power] = total_turbine_costs/1e6/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power] #cost normalized with rated power
        turbine_costs_singleturbine[idx_diameter, idx_power] = (total_turbine_costs/1e6/n_t[idx_diameter,idx_power]) #cost of one turbine in the farm

        idx = var.index('costs_monopile')
        idx2 = var.index('costs_tp')
        foundation_costs[idx_diameter, idx_power] = (data[idx]*n_t[idx_diameter,idx_power] + data[idx2]*n_t[idx_diameter,idx_power])/1e6
        foundation_costs_perMW[idx_diameter, idx_power] = foundation_costs[idx_diameter, idx_power]/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power]

        idx = var.index('costs_infield_cable')
        infield_cable_costs[idx_diameter, idx_power] = data[idx]

        idx = var.index('costs_total_elecrtical')
        total_electrical_costs[idx_diameter, idx_power] = (data[idx] + infield_cable_costs[idx_diameter, idx_power])/1e6

        idx = var.index('costs_installation_turbine')
        installation_turbine_costs[idx_diameter, idx_power] = data[idx]

        idx = var.index('installation_foundation')
        installation_foundation_costs[idx_diameter, idx_power] = data[idx]

        idx = var.index('costs_installation_electrical')
        installation_electrical_costs[idx_diameter, idx_power] = data[idx]

        total_installation_costs[idx_diameter, idx_power] = (installation_turbine_costs[idx_diameter, idx_power] + installation_foundation_costs[idx_diameter, idx_power] + installation_electrical_costs[idx_diameter, idx_power])/1e6
        installation_costs_perMW[idx_diameter, idx_power] = total_installation_costs[idx_diameter, idx_power]/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power]


        idx = var.index('costs_projectdev_elec')
        projectdev_costs[idx_diameter, idx_power] = data[idx]

        idx = var.index('costs_farm_other_elec')
        other_farm_costs[idx_diameter, idx_power] = data[idx]/1e6

        idx = var.index('O&M Costs')
        oandm_costs[idx_diameter, idx_power] = data[idx]/1e6

        idx = var.index('costs_totalinvestment_elec:')
        farm_capex[idx_diameter, idx_power] = data[idx]/1e6

        idx = var.index('wake_losses')
        wake_losses[idx_diameter, idx_power] = data[idx]

        idx = var.index('aep_withwake')
        aep[idx_diameter, idx_power] = data[idx]

        idx = var.index('lcoe')
        lcoe[idx_diameter, idx_power] = data[idx]*10


property = RNA_costs
y_label = 'RNA costs per MW (Million euros)'

p_sp = [10,12,14,16,18,20]
d_sp = [205.99955298145505, 225.66120400784706, 243.74195814422887, 260.5711137591711, 276.3774022806618, 291.3273616691687]

import matplotlib.pyplot as plt
import matplotlib

fs = 12
lw = 1.5
la = 0.5
fig,ax = plt.subplots()

c = plt.contourf(d_rotor,p_rated,property, 50, cmap='YlGnBu')
cbar = fig.colorbar(c)

plt.plot(d_sp, p_sp,'k--',linewidth=lw, alpha=la,label ='Constant specific power line')
#plt.plot(240, 16.67, 'ko')
#plt.text(240, 17.5, 'Global optimum', horizontalalignment='center', verticalalignment='center', size = '13')
# plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')

plt.xlabel('Rotor Diameter (m)', fontsize = fs)
plt.ylabel('Rated Power (MW)', fontsize = fs)
plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
cbar.ax.set_ylabel(y_label, fontsize = fs)
# plt.legend(loc='upper left',fancybox=True, framealpha=0.5)
plt.show()
plt.xlim(rad_values[0]*2, rad_values[-1]*2)
plt.grid(axis = 'both', alpha = 0.5)
ax.tick_params(axis='both',direction='in', length =5)
matplotlib.rcParams['legend.fontsize'] = 12
