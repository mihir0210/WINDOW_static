import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import FancyArrowPatch

power_values = [10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 19.23, 20.0, 22.73]
n_t_ = [100, 91, 83, 77, 71, 67, 62, 58, 55, 52, 50, 44]
#power_values = [10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 20.0, 22.73]
rad_values = [90.0, 95.0, 100.0, 105.0, 215 / 2, 110.0, 222 / 2, 225 / 2, 227 / 2, 115.0, 120.0, 125.0, 130.0,135.0, 140.0, 145.0, 150.0]
trans_efficiency = 0.95
p_rated = np.zeros((len(rad_values), len(power_values)))
d_rotor = np.zeros((len(rad_values), len(power_values)))
n_t = np.zeros((len(rad_values), len(power_values)))
v_mean = np.zeros((len(rad_values), len(power_values)))
rotor_costs = np.zeros((len(rad_values), len(power_values)))
RNA_costs = np.zeros((len(rad_values), len(power_values)))
RNA_costsperMW = np.zeros((len(rad_values), len(power_values)))
tower_costs = np.zeros((len(rad_values), len(power_values)))
tower_costsperMW = np.zeros((len(rad_values), len(power_values)))
total_turbine_costs = np.zeros((len(rad_values), len(power_values)))
other_turbine_costs = np.zeros((len(rad_values), len(power_values))) #profits, warranty, assembly, etc.
turbine_costs_perMW = np.zeros((len(rad_values), len(power_values)))
turbine_costs_singleturbine = np.zeros((len(rad_values), len(power_values)))
foundation_costs = np.zeros((len(rad_values), len(power_values)))
foundation_costs_perMW = np.zeros((len(rad_values), len(power_values)))
infield_length = np.zeros((len(rad_values), len(power_values)))
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
farm_area = np.zeros((len(rad_values), len(power_values)))

wake_losses = np.zeros((len(rad_values), len(power_values)))
aep = np.zeros((len(rad_values), len(power_values)))
aep_noloss = np.zeros((len(rad_values), len(power_values)))


fixed_costs = np.zeros((len(rad_values), len(power_values)))
variable_costs = np.zeros((len(rad_values), len(power_values)))
var_fix_ratio = np.zeros((len(rad_values), len(power_values)))
lcoe_recalc = np.zeros((len(rad_values), len(power_values)))

num = np.zeros((len(rad_values), len(power_values)))
total_aep = np.zeros((len(rad_values), len(power_values)))
lcoe = np.zeros((len(rad_values), len(power_values)))
lcoh = np.zeros((len(rad_values), len(power_values)))

x_data = []
y_data = []
z_data = []
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

for p in power_values:

    for r in rad_values:
        filename = 'H2/parameters_' + str(p) + '_' + str(r*2) + '.csv'
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

        idx = var.index('v_mean')
        v_mean[idx_diameter,idx_power] = data[idx]

        idx = var.index('cost_rotor')
        rotor_costs[idx_diameter, idx_power] = data[idx]*n_t[idx_diameter,idx_power]*0.88 #usd to euro

        idx = var.index('costs_RNA_elec')
        RNA_costs[idx_diameter, idx_power] = data[idx]/1e6  #/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power]
        RNA_costsperMW[idx_diameter, idx_power] = data[idx]/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power]

        idx = var.index('costs_tower')
        tower_costs[idx_diameter, idx_power] = data[idx]*n_t[idx_diameter,idx_power]/1e6
        tower_costsperMW[idx_diameter, idx_power] = tower_costs[idx_diameter, idx_power]/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power]


        idx = var.index('costs_other_turbine_elec')
        other_turbine_costs[idx_diameter, idx_power] = data[idx]/1e6

        total_turbine_costs[idx_diameter, idx_power] = RNA_costs[idx_diameter, idx_power] + tower_costs[idx_diameter, idx_power] + other_turbine_costs[idx_diameter, idx_power] #total cost of wind turbines in the farm
        turbine_costs_perMW[idx_diameter,idx_power] = total_turbine_costs[idx_diameter, idx_power]/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power] #cost normalized with rated power
        turbine_costs_singleturbine[idx_diameter, idx_power] = (total_turbine_costs[idx_diameter, idx_power]/n_t[idx_diameter,idx_power]) #cost of one turbine in the farm

        idx = var.index('costs_monopile')
        idx2 = var.index('costs_tp')
        foundation_costs[idx_diameter, idx_power] = (data[idx]*n_t[idx_diameter,idx_power] + data[idx2]*n_t[idx_diameter,idx_power])/1e6
        foundation_costs_perMW[idx_diameter, idx_power] = foundation_costs[idx_diameter, idx_power]/n_t[idx_diameter,idx_power]/p_rated[idx_diameter,idx_power]

        idx = var.index('infield_length')
        infield_length[idx_diameter, idx_power] = data[idx]/1000

        idx = var.index('costs_infield_cable')
        infield_cable_costs[idx_diameter, idx_power] = data[idx]

        idx = var.index('costs_total_electrical')
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

        idx = var.index('a_farm')
        farm_area[idx_diameter, idx_power] = data[idx]

        idx = var.index('O&M Costs')
        oandm_costs[idx_diameter, idx_power] = data[idx]/1e6

        idx = var.index('costs_totalinvestment_elec:')
        farm_capex[idx_diameter, idx_power] = (data[idx])/1e6

        idx = var.index('wake_losses')
        wake_losses[idx_diameter, idx_power] = data[idx]

        idx = var.index('aep_withwake')
        aep[idx_diameter, idx_power] = data[idx]*1e3/trans_efficiency #in MWh

        idx = var.index('aep_noloss')
        aep_noloss[idx_diameter, idx_power] = data[idx]


        idx = var.index('lcoe')
        lcoe[idx_diameter, idx_power] = data[idx]*10

        idx = var.index('lcoh')
        lcoh[idx_diameter, idx_power] = data[idx]


        aep_yearly = np.zeros(25)
        fixed_oandm_yearly = np.zeros(25)
        for idx in range(1,26):
            aep_yearly[idx-1] = aep[idx_diameter, idx_power]/(1+0.05)**idx
            fixed_oandm_yearly[idx-1] = 22.5e6/(1+0.05)**idx
        total_aep[idx_diameter, idx_power] = np.sum(aep_yearly)
        fixed_oandm = np.sum(fixed_oandm_yearly)


        num[idx_diameter, idx_power] = lcoe[idx_diameter, idx_power]*total_aep[idx_diameter, idx_power]
        # lcoe[idx_diameter, idx_power] = num[idx_diameter, idx_power]/total_aep[idx_diameter, idx_power]

        fixed_decom = 244581803
        installation_export = 29375000.0

        fixed_costs[idx_diameter, idx_power] = fixed_oandm + 35e6 + (94e6 + 53e6) + 40.5e6 + 152100000 + 29375000.0 + installation_export +  fixed_decom # fixed part of oandm, substations, installation substation, export cable and its installation, fixed part of decom
        variable_costs[idx_diameter, idx_power] = num[idx_diameter, idx_power] - fixed_costs[idx_diameter, idx_power]

        var_fix_ratio[idx_diameter, idx_power] = variable_costs[idx_diameter, idx_power]/fixed_costs[idx_diameter, idx_power]
        lcoe_recalc[idx_diameter, idx_power] = (fixed_costs[idx_diameter, idx_power]/total_aep[idx_diameter, idx_power])*(1 + var_fix_ratio[idx_diameter, idx_power])


        x_data.append(p)
        y_data.append(r * 2)
        sp_data.append(p*1e6/(3.142*r**2))
        cost_ratio_sp.append(var_fix_ratio[idx_diameter, idx_power])
        z_data.append(lcoh[idx_diameter, idx_power])
        z_aep.append(aep[idx_diameter, idx_power])
        z_wake.append(wake_losses[idx_diameter, idx_power])
        z_oandm.append(oandm_costs[idx_diameter, idx_power])
        z_vmean.append(v_mean[idx_diameter, idx_power])
        z_installation.append(total_installation_costs[idx_diameter, idx_power])
        z_electrical.append(total_electrical_costs[idx_diameter, idx_power])
        z_rnaperMW.append(RNA_costsperMW[idx_diameter, idx_power])
        z_towerperMW.append(tower_costsperMW[idx_diameter, idx_power])
        z_foundationperMW.append(foundation_costs_perMW[idx_diameter, idx_power])

        z_turbine.append(total_turbine_costs[idx_diameter, idx_power])
        z_bos.append(foundation_costs[idx_diameter, idx_power] + total_installation_costs[idx_diameter, idx_power] + total_electrical_costs[idx_diameter, idx_power])
        z_CAPEX.append(farm_capex[idx_diameter, idx_power])

result_deterministic = np.array(np.where(lcoh == np.amin(lcoh))).flatten()
global_optimum_deterministic = [rad_values[result_deterministic[0]], power_values[result_deterministic[1]]]
print('Deterministic optimum before surface fit:',power_values[result_deterministic[1]], rad_values[result_deterministic[0]])
print('LCoH =', np.amin(lcoh))

def function(data, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14):
    x = data[0]
    y = data[1]
    return p0 + p1 * x + p2 * y + p3 * x ** 2 + p4 * x * y + p5 * y ** 2 + p6 * x ** 3 + p7 * x ** 2 * y + p8 * x * y ** 2 + p9 * y ** 3 + p10*x**4 + p11*x**3*y + p12*x**2*y**2 + p13*x*y**3 + p14*y**4

# def function(data, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20):
#     x = data[0]
#     y = data[1]
#     return p0 + p1 * x + p2 * y + p3 * x ** 2 + p4 * x * y + p5 * y ** 2 + p6 * x ** 3 + p7 * x ** 2 * y + p8 * x * y ** 2 + p9 * y ** 3 + p10*x**4 + p11*x**3*y + p12*x**2*y**2 + p13*x*y**3 + p14*y**4 + p15*x**5 + p16*x**4*y + p17*x**3*y**2 + p18*x**2*y**3 + p19*x*y**4 + p20*y**5
#

# get fit parameters from scipy curve fit
par = curve_fit(function, [x_data, y_data], z_data)

p_eval = np.linspace(10, 22, 121)
r_eval = np.linspace(90, 150, 242)
d_eval = [2 * r for r in r_eval]

[P, D] = np.meshgrid(p_eval, d_eval)

p = par[0]

lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
#lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10] * P**4 + p[11] * P**3 * D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4 + p[15]*P**5 + p[16]* P**4 *D + p[17] * P**3 * D**2 + p[18]* P**2 * D**3 + p[19]*P* D**4 + p[20]*D**5


result_deterministic = np.array(np.where(lcoe_estimate == np.amin(lcoe_estimate))).flatten()
global_optimum_deterministic = [d_eval[result_deterministic[0]], p_eval[result_deterministic[1]]]
print('Deterministic optimum after surface fit:',p_eval[result_deterministic[1]], d_eval[result_deterministic[0]])
print('LCoE =', np.amin(lcoe_estimate))



#### New generic surface fit code for n degree 2D polynomial

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
x = np.array(x_data)
y = np.array(y_data)
z = np.array(z_data)

data_xy = np.array([x,y])
poly = PolynomialFeatures(degree=4)
X_t = poly.fit_transform(data_xy.transpose())

clf = LinearRegression()
clf.fit(X_t, z)

z_pred = np.zeros((len(d_eval), len(p_eval)))

for p in p_eval:
    for d in d_eval:
        idx_power = np.where(p_eval == p)
        idx_diameter = np.where(d_eval == d)
        data_xy = np.array([[p],[d]])
        X_t = poly.fit_transform(data_xy.transpose())
        #z_pred[idx_diameter, idx_power] = np.polynomial.polynomial.polygrid2d(p,d,clf.coef_)
        z_pred[idx_diameter, idx_power] = clf.predict(X_t)

result_deterministic = np.array(np.where(z_pred == np.amin(z_pred))).flatten()
global_optimum_deterministic = [d_eval[result_deterministic[0]], p_eval[result_deterministic[1]]]
print('Deterministic optimum after new surface fit code:',p_eval[result_deterministic[1]], d_eval[result_deterministic[0]])
print('LCoH =', np.amin(z_pred))




# ###### Plot 3-D surface #####
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# # Plot the surface.
# surf = ax.plot_surface(D, P, lcoe_estimate, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
#
# # # Customize the z axis.
# # ax.set_zlim(-1.01, 1.01)
# # ax.zaxis.set_major_locator(LinearLocator(10))
# # # A StrMethodFormatter is used automatically
# # ax.zaxis.set_major_formatter('{x:.02f}')
#
# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)
# ax.set_xlabel('Rotor diameter (m)', fontsize=14)
# ax.set_ylabel('Rated power (MW)', fontsize=14)
# ax.set_zlabel('LCoE (Euros/MWh)', fontsize=14)
#
# plt.show()
#
# ##### Plot showing design space #####

#
# power_values = [10.0, 10.99, 12.05, 12.99, 13.51, 14.08, 14.49, 14.93, 15.62, 16.13, 16.67, 17.24, 18.18, 19.23, 20.0]
# rad_values = [90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]
# dia_values = [2*r for r in rad_values]
# [P, D] = np.meshgrid(power_values, dia_values)
# fig, ax1 = plt.subplots()
#
#
# ticks1 = [10.0, 12.05, 14.08, 16.13, 18.18, 20.0]
# ticks1_labels = ['10', '12', '14', '16', '18', '20']
# ticks2 = [10.0, 12.05, 14.08, 16.13, 18.18, 20.0]
# ticks2_labels =['100', '83', '71', '62', '55', '50']
# plt.scatter(D,P, s=20, c='b')
# ax1.set_xlabel('Rotor diameter (m)', fontsize=14)
# ax1.set_ylabel('Rated power (MW)', fontsize=14)
# ax1.set_yticks(ticks1)
# ax1.set_yticklabels(ticks1_labels)
#
# ax2 = ax1.twinx()
# plt.scatter(D,P, s=20, c='C0', alpha = 0.7, edgecolors='k')
# ax2.set_ylabel('Number of turbines (-)', fontsize=14)
# ax2.set_yticks(ticks2)
# ax2.set_yticklabels(ticks2_labels)
# # plt.grid(axis = 'both', alpha = 0.5)
# # ax2 = plt.gca()
# # ax2.tick_params(axis='both',direction='in', length =5)
# plt.show()
#

# sp = 300 #Specific power in W/m2
# p_sp = [10,12,14,16,18,20]
# d_sp = [((4/3.142)*(p*1e6/sp))**0.5 for p in p_sp]

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

# d_rotor = d_rotor[:,:-1]
# p_rated = p_rated[:,:-1]
property = lcoh
#property = property[:,:-1]
y_label = 'LCoH (Euros/kg)'

fs = 16
lw = 1.5
la = 0.3

n_colorbars = (max(z_data) - min(z_data))/(0.005*min(z_data))

fig,ax = plt.subplots()

import seaborn as sns
from matplotlib.colors import ListedColormap
my_cmap = sns.color_palette("rocket", as_cmap=True)
#my_cmap = sns.color_palette("mako", as_cmap=True)
#c = plt.contourf(d_rotor,p_rated,property, 50, cmap='YlOrRd')
#c = plt.contourf(d_rotor,p_rated,property, 100, cmap = my_cmap.reversed())
c = plt.contourf(d_rotor,p_rated,property, round(n_colorbars), cmap = my_cmap.reversed())
#c = plt.contourf(D,P,property, 50, cmap = my_cmap.reversed())
cbar = fig.colorbar(c)

#plt.plot(d_sp, p_sp,'k--',linewidth=lw, alpha=la,label ='Constant specific power line')

#plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
plt.scatter(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], marker = 'o', c='C4', s = 60, alpha = 0.5) #, label='Baseline')
plt.text(222, 16, 'Global optimum', horizontalalignment='center', verticalalignment='center', size = '13')
# plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')

# plt.scatter(x_wind, y_wind, marker='o', c='k', s=20) #,  label ='Wind speed')
# plt.scatter(x_area, y_area, marker='o', c='k', s=20) #, label ='Area')
# plt.scatter(x_dg, y_dg, marker='o', c='k', s=20) #,  label ='Distance to grid')
# plt.scatter(x_farmpower, y_farmpower, marker='o', c='k', s=20) #,  label ='Farm power')

plt.xlabel('Rotor Diameter (m)', fontsize = fs)
plt.ylabel('Rated Power (MW)', fontsize = fs)
#plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
cbar.ax.set_ylabel(y_label, fontsize = fs)
# plt.legend(loc='upper left',fancybox=True, framealpha=0.5)
#plt.xlim(rad_values[0]*2, rad_values[-1]*2)
#plt.ylim(10,20)
plt.grid(axis = 'both', alpha = 0.1)
ax.tick_params(axis='both',direction='in', length =5)
matplotlib.rcParams['legend.fontsize'] = 12

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
plt.savefig('lcoh.png',bbox_inches='tight',dpi=300)
plt.show()






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




'''
###### Fit for AEP ####
par = curve_fit(function, [x_data, y_data], z_aep)
p = par[0]
P = np.array(p_sp)
D = np.array(d_sp)

aep_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = aep_estimate[0]
aep_normalized = [a/firstval for a in aep_estimate]


###### Fit for Wake ###
par = curve_fit(function, [x_data, y_data], z_wake)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

wake_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = wake_estimate[0]
wake_normalized = [a/firstval for a in wake_estimate]

###### Fit for mean wind speed ###
par = curve_fit(function, [x_data, y_data], z_vmean)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

vmean_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = vmean_estimate[0]
vmean_normalized = [a/firstval for a in vmean_estimate]




plt.figure(num=1, figsize =(4,4))

plt.plot(aep_normalized, color= 'C0', label='AEP', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
plt.plot(wake_normalized, color = 'C1', label='Wake losses', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
plt.plot(vmean_normalized, color = 'C2', label='Mean wind speed', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
plt.xticks([0,1,2,3,4,5], ['10-190', '12-210', '14-225', '16-240', '18-255', '20-270'], rotation=10, fontsize = 10)
plt.xlabel('Turbine sizes', fontsize = 14)
plt.ylabel('Normalized quantities', fontsize = 14)
plt.grid(axis = 'both', alpha = 0.5)
ax = plt.gca()
ax.tick_params(axis='both',direction='in', length =5)
matplotlib.rcParams['legend.fontsize'] = 10
plt.legend()
plt.savefig('aep_increase_constant_sp.png',bbox_inches='tight',dpi=300)



###### Fit for rna and tower ###
par = curve_fit(function, [x_data, y_data], z_rnaperMW)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

rnaperMW_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = rnaperMW_estimate[0]
rnaperMW_normalized = [a/firstval for a in rnaperMW_estimate]


par = curve_fit(function, [x_data, y_data], z_towerperMW)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

towerperMW_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = towerperMW_estimate[0]
towerperMW_normalized = [a/firstval for a in towerperMW_estimate]


###### Fit for foundation ###
par = curve_fit(function, [x_data, y_data], z_foundationperMW)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

foundationperMW_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = foundationperMW_estimate[0]
foundationperMW_normalized = [a/firstval for a in foundationperMW_estimate]



plt.figure(num=2, figsize=(4, 4))

plt.plot(rnaperMW_normalized, color= 'C0', label='RNA costs per MW', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
plt.plot(towerperMW_normalized, color = 'C1', label='Tower costs per MW', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
plt.plot(foundationperMW_normalized, color = 'C2', label='Foundation costs per MW', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
plt.xticks([0,1,2,3,4,5], ['10-190', '12-210', '14-225', '16-240', '18-255', '20-270'], rotation=10, fontsize = 10)
plt.xlabel('Turbine sizes', fontsize = 14)
plt.ylabel('Normalized quantities', fontsize = 14)
plt.grid(axis = 'both', alpha = 0.5)
ax = plt.gca()
ax.tick_params(axis='both',direction='in', length =5)
matplotlib.rcParams['legend.fontsize'] = 10
plt.legend()
plt.savefig('turbine_foundation_costsperMW.png',bbox_inches='tight',dpi=300)
#plt.show()



###### Fit for O&M ####
par = curve_fit(function, [x_data, y_data], z_oandm)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

oandm_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = oandm_estimate[0]
oandm_normalized = [a/firstval for a in oandm_estimate]

###### Fit for installation ###
par = curve_fit(function, [x_data, y_data], z_installation)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

installation_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = installation_estimate[0]
installation_normalized = [a/firstval for a in installation_estimate]

###### Fit for total electrical ###
par = curve_fit(function, [x_data, y_data], z_electrical)
P = np.array(p_sp)
D = np.array(d_sp)
p = par[0]

electrical_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10]*P**4 + p[11]*P**3*D + p[12]*P**2*D**2 + p[13]*P*D**3 + p[14]*D**4
firstval = electrical_estimate[0]
electrical_normalized = [a/firstval for a in electrical_estimate]


plt.figure(num=3, figsize=(4, 4), dpi=300)

plt.plot(oandm_normalized, color= 'C0', label='O&M costs', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
plt.plot(installation_normalized, color = 'C1', label='Installation costs', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
plt.plot(electrical_normalized, color = 'C2', label='Electrical costs', marker = 'o',markerfacecolor = 'C2', markeredgecolor = 'black')
plt.xticks([0,1,2,3,4,5], ['10-190', '12-210', '14-225', '16-240', '18-255', '20-270'], rotation=10, fontsize = 10)
plt.xlabel('Turbine sizes', fontsize = 14)
plt.ylabel('Normalized quantities', fontsize = 14)
plt.grid(axis = 'both', alpha = 0.5)
ax = plt.gca()
ax.tick_params(axis='both',direction='in', length =5)
matplotlib.rcParams['legend.fontsize'] = 10
plt.legend()
plt.savefig('oandm_installation_electrical.png',bbox_inches='tight',dpi=300)
#plt.show()



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
'''

par = curve_fit(function, [x_data, y_data], z_data)
p = par[0]

p_eval = np.linspace(10, 20, 121)
d_eval_opt_ratedpower = [200.0, 210.0, 220.0, 230.0, 240.0, 250.0]

[P, D] = np.meshgrid(p_eval, d_eval_opt_ratedpower)
lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[
    7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10] * P ** 4 + p[11] * P ** 3 * D + p[
                    12] * P ** 2 * D ** 2 + p[13] * P * D ** 3 + p[14] * D ** 4
result = np.where(lcoe_estimate == np.amin(lcoe_estimate, axis=1).reshape(-1, 1))
listOfCordinates = list(zip(result[0], result[1]))

p_values = []
for lc in listOfCordinates:
    p_values.append(P[lc])

opt_ratedpower = p_values

specific_power = [power*1e6/(3.142/4*dia**2) for power,dia in zip(opt_ratedpower, d_eval_opt_ratedpower)]
print(opt_ratedpower, specific_power)

p_eval_opt_rotordia = [10, 12, 14, 16, 18, 20]
r_eval = np.linspace(90, 150, 121)
d_eval = [2 * r for r in r_eval]

[P, D] = np.meshgrid(p_eval_opt_rotordia, d_eval)

lcoe_estimate = p[0] + p[1] * P + p[2] * D + p[3] * P ** 2 + p[4] * P * D + p[5] * D ** 2 + p[6] * P ** 3 + p[
    7] * P ** 2 * D + p[8] * P * D ** 2 + p[9] * D ** 3 + p[10] * P ** 4 + p[11] * P ** 3 * D + p[
                    12] * P ** 2 * D ** 2 + p[13] * P * D ** 3 + p[14] * D ** 4

result = np.where(lcoe_estimate == np.amin(lcoe_estimate, axis=0))
listOfCordinates = list(zip(result[0], result[1]))

d_values = []
for lc in listOfCordinates:
    d_values.append(D[lc])

opt_rotordia = d_values
specific_power = [power*1e6/(3.142/4*dia**2) for power,dia in zip(p_eval_opt_rotordia, opt_rotordia)]
print(opt_rotordia, specific_power)


plt.figure(num=5, figsize=(4, 4), dpi=300)

plt.plot(d_eval_opt_ratedpower, opt_ratedpower, color= 'C0', label='Optimum rated power', marker = 'o',markerfacecolor = 'C0', markeredgecolor = 'black')
plt.plot(opt_rotordia, p_eval_opt_rotordia,color = 'C1', label='Optimum rotor diameter', marker = 'o',markerfacecolor = 'C1', markeredgecolor = 'black')
#plt.xticks([0,1,2,3,4,5], ['280', '300', '325', '350', '375', '390'])
plt.xlabel('Rotor diameter (m)', fontsize = 14)
plt.ylabel('Rated power (MW)', fontsize = 14)
plt.grid(axis = 'both', alpha = 0.5)
ax = plt.gca()
ax.tick_params(axis='both',direction='in', length =5)
matplotlib.rcParams['legend.fontsize'] = 10
plt.legend()
# plt.savefig('opt_power_opt_diameter.png',bbox_inches='tight',dpi=300)
plt.show()

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
