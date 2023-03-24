
import numpy as np
import matplotlib.pyplot as plt


################## Baseline ########

power_values = np.array([10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 19.23, 20.0])
rad_values = [90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0,135.0, 140.0, 145.0, 150.0]
dia_values = np.array([r*2 for r in rad_values])

dia_values = (dia_values-np.min(dia_values))/(np.max(dia_values)-np.min(dia_values))
power_values = (power_values-np.min(power_values))/(np.max(power_values)-np.min(power_values))



P_baseline = np.load("power_matrix_baseline_course.dat", allow_pickle=True)
D_baseline  = np.load("diameter_matrix_baseline_course.dat", allow_pickle=True)
num_baseline = np.load("num_matrix_baseline_course.dat", allow_pickle=True)
aep_baseline = np.load("aep_matrix_baseline_course.dat", allow_pickle=True)
lcoe_baseline = np.load("lcoe_matrix_baseline_course.dat", allow_pickle=True)


aep_noloss = np.load("lossless_aep_baseline_course.dat", allow_pickle=True)
v_mean = np.load("v_mean_matrix_baseline_course.dat", allow_pickle=True)
wake_losses = np.load("wake_matrix_baseline_course.dat", allow_pickle=True)
total_turbine_costs = np.load("turbine_costs_matrix_baseline_course.dat", allow_pickle=True)
foundation_costs = np.load("foundation_costs_matrix_baseline_course.dat", allow_pickle=True)
total_oandm_costs = np.load("oandm_costs_matrix_baseline_course.dat", allow_pickle=True)
total_installation_costs = np.load("installation_costs_matrix_baseline_course.dat", allow_pickle=True)
total_electrical_costs = np.load("electrical_costs_matrix_baseline_course.dat", allow_pickle=True)
other_turbine_costs = np.load('other_turbine_costs_baseline_course.dat', allow_pickle=True)
other_farm_costs = np.load('other_farm_costs_baseline_course.dat', allow_pickle=True)
projectdev_costs = np.load('projectdev_costs_baseline_course.dat', allow_pickle=True)
decom_costs = np.load('decom_costs_baseline_course.dat', allow_pickle=True)


# dia_values  = dia_values/np.linalg.norm(dia_values)
# power_values = power_values/np.linalg.norm(power_values)


num_baseline = num_baseline*-1*0.97*0.97/1e6 #/num_baseline[4,4] #availability and transmission eff
aep_baseline = aep_baseline #/aep_baseline[4,4]
lcoe_baseline = lcoe_baseline*-1 #/np.amin(lcoe_baseline)

wake_baseline = wake_losses*-1 #/wake_losses[4,4]
aep_noloss_baseline = aep_noloss #/aep_noloss[4,4]

total_turbine_costs_baseline = total_turbine_costs*-1 #/total_turbine_costs[4,4]
foundation_costs_baseline = foundation_costs*-1 #/foundation_costs[4,4]
oandm_costs_baseline = total_oandm_costs*-1 #/oandm_costs[4,4]
installation_costs_baseline = total_installation_costs*-1 #/total_installation_costs[4,4]
electrical_costs_baseline = total_electrical_costs*-1 #/total_electrical_costs[4,4]
other_turbine_costs_baseline = other_turbine_costs*-1
other_farm_costs_baseline = other_farm_costs*-1
projectdev_costs_baseline = projectdev_costs*-1
decom_costs_baseline = decom_costs*-1


grad_num_dia_b  = np.gradient(num_baseline,dia_values, axis = 1)/aep_baseline
grad_num_power_b = np.gradient(num_baseline, power_values, axis = 0)/aep_baseline

grad_turbinecosts_dia_b = np.gradient(total_turbine_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_foundationcosts_dia_b = np.gradient(foundation_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_oandmcosts_dia_b = np.gradient(oandm_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_installationcosts_dia_b = np.gradient(installation_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_electricalcosts_dia_b = np.gradient(electrical_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_other_turbine_costs_dia_b = np.gradient(other_turbine_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_other_farm_costs_dia_b = np.gradient(other_farm_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_projectdev_costs_dia_b = np.gradient(projectdev_costs_baseline, dia_values, axis = 1)/aep_baseline
grad_decom_costs_dia_b = np.gradient(decom_costs_baseline, dia_values, axis = 1)/aep_baseline

grad_turbinecosts_power_b = np.gradient(total_turbine_costs_baseline, power_values, axis = 0)/aep_baseline
grad_foundationcosts_power_b = np.gradient(foundation_costs_baseline, power_values, axis = 0)/aep_baseline
grad_oandmcosts_power_b = np.gradient(oandm_costs_baseline, power_values, axis = 0)/aep_baseline
grad_installationcosts_power_b = np.gradient(installation_costs_baseline, power_values, axis = 0)/aep_baseline
grad_electricalcosts_power_b = np.gradient(electrical_costs_baseline, power_values, axis = 0)/aep_baseline
grad_other_turbine_costs_power_b = np.gradient(other_turbine_costs_baseline, power_values, axis = 0)/aep_baseline
grad_other_farm_costs_power_b = np.gradient(other_farm_costs_baseline, power_values, axis = 0)/aep_baseline
grad_projectdev_costs_power_b = np.gradient(projectdev_costs_baseline, power_values, axis = 0)/aep_baseline
grad_decom_costs_power_b = np.gradient(decom_costs_baseline, power_values, axis = 0)/aep_baseline

grad_other_costs_dia_b = grad_other_turbine_costs_dia_b + grad_other_farm_costs_dia_b + grad_projectdev_costs_dia_b + grad_decom_costs_dia_b
grad_other_costs_power_b = grad_other_turbine_costs_power_b + grad_other_farm_costs_power_b + grad_projectdev_costs_power_b + grad_decom_costs_power_b



grad_aep_dia_b = np.gradient(aep_baseline,dia_values, axis = 1)*-num_baseline/(aep_baseline**2)
grad_aep_power_b = np.gradient(aep_baseline,power_values, axis = 0)*-num_baseline/(aep_baseline**2)

grad_wake_dia_b = -1*aep_noloss_baseline*np.gradient(wake_baseline,dia_values, axis = 1)*-num_baseline/(aep_baseline**2)
grad_wake_power_b = -1*aep_noloss_baseline*np.gradient(wake_baseline,power_values, axis = 0)*-num_baseline/(aep_baseline**2)

grad_aep_noloss_dia_b = (1 + wake_baseline)*np.gradient(aep_noloss_baseline,dia_values, axis = 1)*-num_baseline/(aep_baseline**2)
grad_aep_noloss_power_b = (1 + wake_baseline)*np.gradient(aep_noloss_baseline, power_values, axis = 0)*-num_baseline/(aep_baseline**2)

grad_lcoe_dia = np.gradient(lcoe_baseline,dia_values, axis = 1)
grad_lcoe_power = np.gradient(lcoe_baseline,power_values, axis = 0)



# print(grad_lcoe_power[6,5])
# print(grad_num_power_b[6,5])
# print(grad_aep_power_b[6,5])
#
# print(lcoe_baseline[6,5])

grad_lcoe_dia_calculated = (aep_baseline*grad_num_dia_b - num_baseline*grad_aep_dia_b)/np.square(aep_baseline)

# print(grad_aep_power_b)



# norm_dia = np.linalg.norm(grad_aep_dia)
# norm_power = np.linalg.norm(grad_aep_power)
# grad_aep_dia = grad_aep_dia/norm_dia
# grad_aep_power = grad_aep_power/norm_power

# mag_num_baseline = np.sqrt(grad_num_dia**2 + grad_num_power**2)
# mag_aep_baseline = np.sqrt(grad_aep_dia**2 + grad_aep_power**2)
#
# ratio_mag = mag_num_baseline/mag_aep_baseline
# print("-------Baseline --------")
# print(grad_num_dia[1,1])
# print(grad_num_power[1,1])
# print(grad_aep_dia[1,1])
# print(grad_aep_power[1,1])

# xticks = [0, 2, 4, 6, 8, 10, 12]
# yticks = [0, 2, 4, 6, 8, 10]
# xtick_labels = ['180', '200', '220', '240', '260', '280', '300']
# ytick_labels = ['10', '12', '14', '16', '18', '20']
#
# fig, axs = plt.subplots(nrows =2, ncols= 2, figsize=(12,10))
# import seaborn as sns
# from matplotlib.colors import ListedColormap
# my_cmap = sns.color_palette("rocket", as_cmap=True)
# sns.heatmap(grad_lcoe_dia, cmap = my_cmap.reversed(), ax = axs[0,0])
# sns.heatmap(grad_lcoe_power, cmap = my_cmap.reversed(), ax = axs[0,1])
# axs[0,0].invert_yaxis()
# axs[0,1].invert_yaxis()
# # sns.heatmap(ratio_mag, cmap = my_cmap.reversed(), ax = axs[0])
# # axs[0].invert_yaxis()
# axs[0,0].set_xticks(xticks)
# axs[0,0].set_xticklabels(xtick_labels)
# axs[0,0].set_yticks(yticks)
# axs[0,0].set_yticklabels(ytick_labels)
# axs[0,1].set_xticks(xticks)
# axs[0,1].set_xticklabels(xtick_labels)
# axs[0,1].set_yticks(yticks)
# axs[0,1].set_yticklabels(ytick_labels)
# axs[0,0].set_ylabel('Rated power (MW)', fontsize = 16)
# axs[0,0].set_title('LCoE gradient w.r.t. D (baseline)')
# axs[0,1].set_title('LCoE gradient w.r.t. P (baseline)')
# plt.show()

# angle = np.arctan(grad_num_power/grad_num_dia)
#
# angle = angle*(180/3.142)
#
# print(angle)
#
# angle = np.arctan(grad_aep_power/grad_aep_dia)
#
# angle = angle*(180/3.142)
#
# print(angle)

# print(np.sqrt(grad_turbinecosts_power_b[4,4]**2 + grad_turbinecosts_dia_b[4,4]**2))
# print(np.sqrt(grad_foundationcosts_power_b[4,4]**2 + grad_foundationcosts_dia_b[4,4]**2))
# print(np.sqrt(grad_oandmcosts_power_b[4,4]**2 + grad_oandmcosts_dia_b[4,4]**2))
# print(np.sqrt(grad_installationcosts_power_b[4,4]**2 + grad_installationcosts_dia_b[4,4]**2))
# print(np.sqrt(grad_electricalcosts_power_b[4,4]**2 + grad_electricalcosts_dia_b[4,4]**2))
# print(np.sqrt(grad_other_turbine_costs_power_b[4,4]**2 + grad_other_turbine_costs_dia_b[4,4]**2))
# print(np.sqrt(grad_other_farm_costs_power_b[4,4]**2 + grad_other_farm_costs_dia_b[4,4]**2))
# print(np.sqrt(grad_projectdev_costs_power_b[4,4]**2 + grad_projectdev_costs_dia_b[4,4]**2))
# print(np.sqrt(grad_decom_costs_power_b[4,4]**2 + grad_decom_costs_dia_b[4,4]**2))
# print(np.sqrt(grad_num_power_b[4,4]**2 + grad_num_dia_b[4,4]**2))

# print(grad_turbinecosts_power_b[4,4])
# print(grad_foundationcosts_power_b[4,4])
# print(grad_oandmcosts_power_b[4,4])
# print(grad_installationcosts_power_b[4,4])
# print(grad_electricalcosts_power_b[4,4])
# print(grad_other_turbine_costs_power_b[4,4])
# print(grad_other_farm_costs_power_b[4,4])
# print(grad_projectdev_costs_power_b[4,4])
# print(grad_decom_costs_power_b[4,4])
# print(grad_num_power_b[4,4])

# x = [D_baseline[4,4],D_baseline[4,4],D_baseline[4,4],D_baseline[4,4],D_baseline[4,4],D_baseline[4,4]]
# y = [P_baseline[4,4],P_baseline[4,4],P_baseline[4,4],P_baseline[4,4],P_baseline[4,4],P_baseline[4,4]]
# u = [grad_turbinecosts_dia_b[4,4], grad_foundationcosts_dia_b[4,4], grad_oandmcosts_dia_b[4,4],grad_installationcosts_dia_b[4,4],grad_electricalcosts_dia_b[4,4],grad_num_dia_b[4,4]]
# v = [grad_turbinecosts_power_b[4,4], grad_foundationcosts_power_b[4,4],grad_oandmcosts_power_b[4,4], grad_installationcosts_power_b[4,4],grad_electricalcosts_power_b[4,4], grad_num_power_b[4,4]]

# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))

# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 4, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale = 2000)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 4, color='g', linestyle = '-',fc='none', ec='g', linewidth = 1, scale = 1000)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale = 1200)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 4, color='m', linestyle = '-',fc='none', ec='m', linewidth = 1, scale = 900)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 4, color='y', linestyle = '-',fc='none', ec='y', linewidth = 1, scale = 500)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 4, color='c', linestyle = '-',fc='none', ec='c', linewidth = 1, scale = 500)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 4, scale = 3500)

# scale = 0.0003
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 2, headaxislength = 2, color='b', linestyle = '--', linewidth = 1, scale = scale, alpha = 0.5, label='_nolegend_')
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='g', linestyle = '--', linewidth = 1, scale = scale, alpha = 0.5, label='_nolegend_')
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 2, color='r', headaxislength = 2,linestyle = '--', linewidth = 1, scale = scale, alpha = 0.5, label='_nolegend_')
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='m', linestyle = '--', linewidth = 1, scale = scale, alpha = 0.5, label='_nolegend_')
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='y', linestyle = '--', linewidth = 1, scale = scale, alpha = 0.5, label='_nolegend_')
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 2,headaxislength = 2, color='c', linestyle = '--', linewidth = 1, scale = scale, alpha = 0.5, label='_nolegend_')
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2, linestyle = '--',scale = scale, alpha = 0.5, label='_nolegend_')
#

# axs[0].legend(['Turbine', 'Foundation', 'O&M', 'Installation', 'Electrical', 'Other costs'])

# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 0.9*10e6)

# scale = 0.002
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 2, headaxislength = 2, color='b', linestyle = '--', linewidth = 1, scale = 2e-10, alpha = 0.5, label='_nolegend_')
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 2, headaxislength = 2, color='r', linestyle = '--', linewidth = 1, scale = scale, alpha = 0.5, label='_nolegend_')
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, linestyle = '--', scale = scale, alpha = 0.5, label='_nolegend_')

# axs[1].legend(['Wake losses', 'Gross AEP'])

# x_tick_labels = [str(round(i,1)) for i in dia_values]
# y_tick_labels = [str(round(i,1)) for i in power_values]
#
# axs[0].set_xticklabels(x_tick_labels)
# axs[0].set_yticklabels(y_tick_labels)
# axs[0].set_ylabel('Rated power', fontsize = 16)
# axs[0].set_xlabel('Rotor diameter', fontsize = 16)
# axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
#
# axs[1].set_xlabel('Rotor diameter', fontsize = 16)
# axs[1].set_ylabel('Rated power', fontsize = 16)
# axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)




########################### LOW WIND ####################




power_values = [10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 19.23, 20.0] #for a 1000MW farm
rad_values = [90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0,135.0, 140.0, 145.0, 150.0]
dia_values = np.array([r*2 for r in rad_values])

dia_values = (dia_values-np.min(dia_values))/(np.max(dia_values)-np.min(dia_values))
power_values = (power_values-np.min(power_values))/(np.max(power_values)-np.min(power_values))

P_lowwind = np.load("power_matrix_lowwind_course.dat", allow_pickle=True)
D_lowwind   = np.load("diameter_matrix_lowwind_course.dat", allow_pickle=True)
num_lowwind  = np.load("num_matrix_lowwind_course.dat", allow_pickle=True)
aep_lowwind  = np.load("aep_matrix_lowwind_course.dat", allow_pickle=True)
lcoe_lowwind = np.load("lcoe_matrix_lowwind_course.dat",allow_pickle=True )

aep_noloss = np.load("lossless_aep_lowwind_course.dat", allow_pickle=True)
v_mean = np.load("v_mean_matrix_lowwind_course.dat", allow_pickle=True)
wake_losses = np.load("wake_matrix_lowwind_course.dat", allow_pickle=True)

num_lowwind = num_lowwind*-1/1e6 #/num_lowwind[3,5]
aep_lowwind = aep_lowwind #/aep_lowwind[3,5]
lcoe_lowwind = lcoe_lowwind*-1 #/np.amin(lcoe_lowwind)

wake_lowwind = wake_losses*-1 #/wake_losses[4,4]
aep_noloss_lowwind = aep_noloss #/aep_noloss[4,4]


grad_num_dia_lw  = np.gradient(num_lowwind,dia_values, axis = 1)/aep_lowwind
grad_num_power_lw = np.gradient(num_lowwind, power_values, axis = 0)/aep_lowwind

# print(np.sqrt(grad_num_power[4,4]**2 + grad_num_dia[4,4]**2))

# norm_dia = np.linalg.norm(grad_num_dia)
# norm_power = np.linalg.norm(grad_num_power)
# grad_num_dia = grad_num_dia/norm_dia
# grad_num_power = grad_num_power/norm_power


grad_aep_dia_lw = np.gradient(aep_lowwind,dia_values, axis = 1)*-num_lowwind/(aep_lowwind**2)
grad_aep_power_lw = np.gradient(aep_lowwind,power_values, axis = 0)*-num_lowwind/(aep_lowwind**2)

# print(np.sqrt(grad_aep_power[4,4]**2 + grad_aep_dia[4,4]**2))

grad_wake_dia = np.gradient(wake_lowwind,dia_values, axis = 1)*-num_lowwind/(aep_lowwind**2)
grad_wake_power = np.gradient(wake_lowwind,power_values, axis = 0)*-num_lowwind/(aep_lowwind**2)

grad_aep_noloss_dia = np.gradient(aep_noloss_lowwind,dia_values, axis = 1)*-num_lowwind/(aep_lowwind**2)
grad_aep_noloss_power = np.gradient(aep_noloss_lowwind, power_values, axis = 0)*-num_lowwind/(aep_lowwind**2)

# norm_dia = np.linalg.norm(grad_aep_dia)
# norm_power = np.linalg.norm(grad_aep_power)
# grad_aep_dia = grad_aep_dia/norm_dia
# grad_aep_power = grad_aep_power/norm_power

# mag_aep_lowwind = np.sqrt(grad_aep_dia**2 + grad_aep_power**2)
# mag_num_lowwind = np.sqrt(grad_num_dia**2 + grad_num_power**2)
#
#
# ratio_mag = mag_num_lowwind/mag_aep_lowwind

# grad_lcoe_dia = np.gradient(lcoe_lowwind,dia_values, axis = 1)
# grad_lcoe_power = np.gradient(lcoe_lowwind,power_values, axis = 0)
# #
# diff_magnitude_num = mag_num_lowwind - mag_num_baseline
# diff_magnitude_aep = mag_aep_lowwind - mag_aep_baseline
#
# diff_magnitude_num = np.around(diff_magnitude_num, decimals=2)
#
# print(grad_aep_power)
#
# xticks = [0, 2, 5, 10, 12, 14, 16]
# yticks = [0, 2, 4, 6, 8, 10]
# xtick_labels = ['180', '200', '220', '240', '260', '280', '300']
# ytick_labels = ['10', '12', '14', '16', '18', '20']
#
# fig, axs = plt.subplots(nrows =1, ncols= 1, figsize=(10,4))
# import seaborn as sns
# from matplotlib.colors import ListedColormap
# my_cmap = sns.color_palette("rocket", as_cmap=True)
# sns.heatmap(mag_num_baseline, cmap = my_cmap.reversed(), ax = axs[0], vmin = 0.04, vmax = 0.18)
# sns.heatmap(mag_aep_baseline, cmap = my_cmap.reversed(), ax = axs[1], vmin = 0.04, vmax = 0.18)
# axs[0].invert_yaxis()
# axs[1].invert_yaxis()
# sns.heatmap(ratio_mag, cmap = my_cmap.reversed(), ax=axs[1])
# axs[1].invert_yaxis()
# axs[1].set_xticks(xticks)
# axs[1].set_xticklabels(xtick_labels)
# axs[1].set_yticks(yticks)
# axs[1].set_yticklabels(ytick_labels)
#
#
# plt.show()

#
# sns.heatmap(grad_aep_dia, cmap = my_cmap.reversed(), ax = axs[1,0])
# sns.heatmap(grad_aep_power, cmap = my_cmap.reversed(), ax = axs[1,1])
# axs[1,0].invert_yaxis()
# axs[1,1].invert_yaxis()
# axs[1,0].set_xticks(xticks)
# axs[1,0].set_xticklabels(xtick_labels)
# axs[1,0].set_yticks(yticks)
# axs[1,0].set_yticklabels(ytick_labels)
# axs[1,1].set_xticks(xticks)
# axs[1,1].set_xticklabels(xtick_labels)
# axs[1,1].set_yticks(yticks)
# axs[1,1].set_yticklabels(ytick_labels)
# axs[1,0].set_ylabel('Rated power (MW)', fontsize = 16)
# axs[1,0].set_xlabel('Rotor diameter (m)', fontsize = 16)
# axs[1,1].set_xlabel('Rotor diameter (m)', fontsize = 16)
# axs[1,0].set_title('AEP gradient w.r.t. D (low wind)')
# axs[1,1].set_title('AEP gradient w.r.t. P (low wind)')
# plt.show()
#
#
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))

# axs[0].quiver(D_lowwind, P_lowwind,  grad_num_dia, grad_num_power, color='r', headlength = 4, alpha = 0.5)
#axs[1].quiver(D_lowwind,  P_lowwind, grad_aep_dia, grad_aep_power, color='r', headlength = 4, alpha = 0.5, scale = 10)

# axs[0].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# axs[0].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
#axs[0].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 4)

# scale = 0.002
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia[4,4], grad_wake_power[4,4], headlength = 2, headaxislength = 2, color='b', linestyle = '-', linewidth = 1, scale=2e-10)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia[4,4], grad_aep_noloss_power[4,4], headlength = 2, headaxislength = 2, color='r', linestyle = '-', linewidth = 1, scale=scale)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia[4,4], grad_aep_power[4,4], headlength = 2, headaxislength = 2, scale = scale)
# sns.heatmap(diff_magnitude_num, cmap = my_cmap.reversed(), ax = axs[1,0])
# axs[1,0].invert_yaxis()
#
# sns.heatmap(diff_magnitude_aep, cmap = my_cmap.reversed(), ax = axs[1,1])
# axs[1,1].invert_yaxis()
#
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# plt.savefig('gradients_baselinevslowwind_arrows.png',bbox_inches='tight',dpi=300)

# axs[0].set_xlabel('Rotor diameter (m)', fontsize = 16)
# axs[0].set_ylabel('Rated power (MW)', fontsize = 16)
# axs[1].set_xlabel('Rotor diameter (m)', fontsize = 16)

# axs.quiver(D_lowwind, P_lowwind,  grad_lcoe_dia, grad_lcoe_power, color = 'r', alpha=0.6, headlength = 4, scale = 8)
# plt.show()


###################### low farm power #####################

#
# power_values = np.array([10.0, 11.11, 12.0, 13.04, 14.29, 15.0, 16.22, 17.14, 18.18, 19.35, 20.0])
# rad_values = [90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0,135.0, 140.0, 145.0, 150.0]
# dia_values = np.array([r*2 for r in rad_values])
#
# dia_values = (dia_values-np.min(dia_values))/(np.max(dia_values)-np.min(dia_values))
# power_values = (power_values-np.min(power_values))/(np.max(power_values)-np.min(power_values))
#
# P_power600 = np.load("power_matrix_power600_course.dat", allow_pickle=True)
# D_power600  = np.load("diameter_matrix_power600_course.dat", allow_pickle=True)
# num_power600 = np.load("num_matrix_power600_course.dat", allow_pickle=True)
# aep_power600 = np.load("aep_matrix_power600_course.dat", allow_pickle=True)
# lcoe_power600 = np.load("lcoe_matrix_power600_course.dat", allow_pickle=True)
#
# # dia_values  = dia_values/np.linalg.norm(dia_values)
# # power_values = power_values/np.linalg.norm(power_values)
#
# num_power600 = num_power600*-1/np.amin(num_power600)
# aep_power600= aep_power600/np.amin(aep_power600)
# lcoe_power600 = lcoe_power600*-1/np.amin(lcoe_power600)
#
# grad_num_dia  = np.gradient(num_power600,dia_values, axis = 1)
# grad_num_power = np.gradient(num_power600, power_values, axis = 0)
#
# grad_lcoe_dia = np.gradient(lcoe_power600,dia_values, axis = 1)
# grad_lcoe_power = np.gradient(lcoe_power600,power_values, axis = 0)
#
# # norm_dia = np.linalg.norm(grad_num_dia)
# # norm_power = np.linalg.norm(grad_num_power)
# # grad_num_dia = grad_num_dia/norm_dia
# # grad_num_power = grad_num_power/norm_power
#
#
# grad_aep_dia = np.gradient(aep_power600,dia_values, axis = 1)
# grad_aep_power = np.gradient(aep_power600,power_values, axis = 0)
#
# # norm_dia = np.linalg.norm(grad_aep_dia)
# # norm_power = np.linalg.norm(grad_aep_power)
# # grad_aep_dia = grad_aep_dia/norm_dia
# # grad_aep_power = grad_aep_power/norm_power
#
# mag_num_power600 = np.sqrt(grad_num_dia**2 + grad_num_power**2)
# mag_aep_power600 = np.sqrt(grad_aep_dia**2 + grad_aep_power**2)
#
# ratio_mag = mag_num_power600/mag_aep_power600

# diff_magnitude_num = mag_num_power600 - mag_num_baseline
# diff_magnitude_aep = mag_aep_power600 - mag_aep_baseline
#
# axs[0].quiver(D_baseline, P_baseline,  grad_num_dia, grad_num_power, color='r', headlength = 4, alpha = 0.5, scale = 10)
# axs[1].quiver(D_baseline,  P_baseline, grad_aep_dia, grad_aep_power, color='r', headlength = 4, alpha = 0.5, scale = 10)

# sns.heatmap(diff_magnitude_num, cmap = my_cmap.reversed(), ax = axs[1,0])
# axs[1,0].invert_yaxis()
#
# sns.heatmap(diff_magnitude_aep, cmap = my_cmap.reversed(), ax = axs[1,1])
# axs[1,1].invert_yaxis()
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
# axs[0].quiver(D_power600, P_power600,  grad_num_dia, grad_num_power, color='r', headlength = 4, alpha = 0.5, scale = 10)
# axs[1].quiver(D_power600,  P_power600, grad_aep_dia, grad_aep_power, color='r', headlength = 4, alpha = 0.5, scale = 10)
#
# ax = plt.gca()
# ax.tick_params(axis='both',direction='in', length =5)
# # plt.savefig('gradients_baselinevspower600_arrows.png',bbox_inches='tight',dpi=300)
#
# axs[0].set_xlabel('Rotor diameter (m)', fontsize = 16)
# axs[0].set_ylabel('Rated power (MW)', fontsize = 16)
# axs[1].set_xlabel('Rotor diameter (m)', fontsize = 16)
#
# plt.show()



# sns.heatmap(grad_lcoe_dia, cmap = my_cmap.reversed(), ax = axs[1,0])
# sns.heatmap(grad_lcoe_power, cmap = my_cmap.reversed(), ax = axs[1,1])
# axs[1,0].invert_yaxis()
# axs[1,1].invert_yaxis()
# axs[1,0].set_xticks(xticks)
# axs[1,0].set_xticklabels(xtick_labels)
# axs[1,0].set_yticks(yticks)
# axs[1,0].set_yticklabels(ytick_labels)
# axs[1,1].set_xticks(xticks)
# axs[1,1].set_xticklabels(xtick_labels)
# axs[1,1].set_yticks(yticks)
# axs[1,1].set_yticklabels(ytick_labels)
# axs[1,0].set_ylabel('Rated power (MW)', fontsize = 16)
# axs[1,0].set_xlabel('Rotor diameter (m)', fontsize = 16)
# axs[1,1].set_xlabel('Rotor diameter (m)', fontsize = 16)
# axs[1,0].set_title('LCoE gradient w.r.t. D (600 MW)')
# axs[1,1].set_title('LCoE gradient w.r.t. P (600 MW)')
# plt.show()

#
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
#
#
#
# sns.heatmap(diff_magnitude_num, cmap = my_cmap.reversed(), ax = axs[0])
# axs[0].invert_yaxis()
#
# sns.heatmap(diff_magnitude_aep, cmap = my_cmap.reversed(), ax = axs[1])
# axs[1].invert_yaxis()
# plt.show()
#
# fig, axs = plt.subplots()
# axs.quiver(D_power600 , P_power600 ,  grad_lcoe_dia, grad_lcoe_power, color='r', headlength = 4, alpha = 0.5, scale = 8)
#
# axs.set_ylabel('Rated power (MW)', fontsize = 16)
# axs.set_xlabel('Rotor diameter (m)', fontsize = 16)
# plt.title("Farm power: 600 MW", fontsize = 16)
# plt.show()
#
#
#







#################### HIGH FARM POWER ##################


power_values = np.array([10.0, 11.02, 12.07, 13.08, 14.0, 15.05, 16.09, 17.07, 18.18, 19.18, 20.0])
rad_values = [90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0,135.0, 140.0, 145.0, 150.0]
dia_values = np.array([r*2 for r in rad_values])

dia_values = (dia_values-np.min(dia_values))/(np.max(dia_values)-np.min(dia_values))
power_values = (power_values-np.min(power_values))/(np.max(power_values)-np.min(power_values))

P_power1400 = np.load("power_matrix_power1400_course.dat", allow_pickle=True)
D_power1400   = np.load("diameter_matrix_power1400_course.dat", allow_pickle=True)
num_power1400  = np.load("num_matrix_power1400_course.dat", allow_pickle=True)
aep_power1400  = np.load("aep_matrix_power1400_course.dat", allow_pickle=True)
lcoe_power1400  = np.load("lcoe_matrix_power1400_course.dat", allow_pickle=True)


aep_noloss = np.load("lossless_aep_power1400_course.dat", allow_pickle=True)
v_mean = np.load("v_mean_matrix_power1400_course.dat", allow_pickle=True)
wake_losses = np.load("wake_matrix_power1400_course.dat", allow_pickle=True)
total_turbine_costs = np.load("turbine_costs_matrix_power1400_course.dat", allow_pickle=True)
foundation_costs = np.load("foundation_costs_matrix_power1400_course.dat", allow_pickle=True)
total_oandm_costs = np.load("oandm_costs_matrix_power1400_course.dat", allow_pickle=True)
total_installation_costs = np.load("installation_costs_matrix_power1400_course.dat", allow_pickle=True)
total_electrical_costs = np.load("electrical_costs_matrix_power1400_course.dat", allow_pickle=True)
other_turbine_costs = np.load('other_turbine_costs_power1400_course.dat', allow_pickle=True)
other_farm_costs = np.load('other_farm_costs_power1400_course.dat', allow_pickle=True)
projectdev_costs = np.load('projectdev_costs_power1400_course.dat', allow_pickle=True)
decom_costs = np.load('decom_costs_power1400_course.dat', allow_pickle=True)

# dia_values  = dia_values/np.linalg.norm(dia_values)
# power_values = power_values/np.linalg.norm(power_values)



num_power1400  = num_power1400 *-1*0.97*0.97/1e6  #/num_power1400[6,4]
aep_power1400 = aep_power1400 #/aep_power1400[6,4]
lcoe_power1400  = lcoe_power1400 *-1  #/np.amin(lcoe_power1400)


wake_power1400 = wake_losses*-1 #/wake_losses[4,4]
aep_noloss_power1400 = aep_noloss #/aep_noloss[4,4]

total_turbine_costs_power1400 = total_turbine_costs*-1 #/total_turbine_costs[4,4]
foundation_costs_power1400 = foundation_costs*-1 #/foundation_costs[4,4]
oandm_costs_power1400 = total_oandm_costs*-1 #/oandm_costs[4,4]
installation_costs_power1400 = total_installation_costs*-1 #/total_installation_costs[4,4]
electrical_costs_power1400 = total_electrical_costs*-1 #/total_electrical_costs[4,4]
other_turbine_costs_power1400 = other_turbine_costs*-1
other_farm_costs_power1400 = other_farm_costs*-1
projectdev_costs_power1400 = projectdev_costs*-1
decom_costs_power1400 = decom_costs*-1



grad_num_dia_fp  = np.gradient(num_power1400 ,dia_values, axis = 1)/aep_power1400
grad_num_power_fp = np.gradient(num_power1400 , power_values, axis = 0)/aep_power1400

grad_turbinecosts_dia_fp = np.gradient(total_turbine_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_foundationcosts_dia_fp = np.gradient(foundation_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_oandmcosts_dia_fp = np.gradient(oandm_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_installationcosts_dia_fp = np.gradient(installation_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_electricalcosts_dia_fp = np.gradient(electrical_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_other_turbine_costs_dia_fp = np.gradient(other_turbine_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_other_farm_costs_dia_fp = np.gradient(other_farm_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_projectdev_costs_dia_fp = np.gradient(projectdev_costs_power1400, dia_values, axis = 1)/aep_power1400
grad_decom_costs_dia_fp = np.gradient(decom_costs_power1400, dia_values, axis = 1)/aep_power1400

grad_turbinecosts_power_fp = np.gradient(total_turbine_costs_power1400, power_values, axis = 0)/aep_power1400
grad_foundationcosts_power_fp = np.gradient(foundation_costs_power1400, power_values, axis = 0)/aep_power1400
grad_oandmcosts_power_fp = np.gradient(oandm_costs_power1400, power_values, axis = 0)/aep_power1400
grad_installationcosts_power_fp = np.gradient(installation_costs_power1400, power_values, axis = 0)/aep_power1400
grad_electricalcosts_power_fp = np.gradient(electrical_costs_power1400, power_values, axis = 0)/aep_power1400
grad_other_turbine_costs_power_fp = np.gradient(other_turbine_costs_power1400, power_values, axis = 0)/aep_power1400
grad_other_farm_costs_power_fp = np.gradient(other_farm_costs_power1400, power_values, axis = 0)/aep_power1400
grad_projectdev_costs_power_fp = np.gradient(projectdev_costs_power1400, power_values, axis = 0)/aep_power1400
grad_decom_costs_power_fp = np.gradient(decom_costs_power1400, power_values, axis = 0)/aep_power1400

grad_other_costs_dia_fp = grad_other_turbine_costs_dia_fp + grad_other_farm_costs_dia_fp + grad_projectdev_costs_dia_fp + grad_decom_costs_dia_fp
grad_other_costs_power_fp = grad_other_turbine_costs_power_fp + grad_other_farm_costs_power_fp + grad_projectdev_costs_power_fp + grad_decom_costs_power_fp



grad_aep_dia_fp = np.gradient(aep_power1400,dia_values, axis = 1)*-num_power1400/(aep_power1400**2)
grad_aep_power_fp = np.gradient(aep_power1400,power_values, axis = 0)*-num_power1400/(aep_power1400**2)

grad_wake_dia_fp = np.gradient(wake_power1400,dia_values, axis = 1)*-num_power1400/(aep_power1400**2)
grad_wake_power_fp = np.gradient(wake_power1400,power_values, axis = 0)*-num_power1400/(aep_power1400**2)

grad_aep_noloss_dia_fp = np.gradient(aep_noloss_power1400,dia_values, axis = 1)*-num_power1400/(aep_power1400**2)
grad_aep_noloss_power_fp = np.gradient(aep_noloss_power1400, power_values, axis = 0)*-num_power1400/(aep_power1400**2)

grad_lcoe_dia = np.gradient(lcoe_power1400 ,dia_values, axis = 1)
grad_lcoe_power = np.gradient(lcoe_power1400 ,power_values, axis = 0)


# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))

# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 4, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale = 2000)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 4, color='g', linestyle = '-',fc='none', ec='g', linewidth = 1, scale = 1000)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale = 1200)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 4, color='m', linestyle = '-',fc='none', ec='m', linewidth = 1, scale = 900)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 4, color='y', linestyle = '-',fc='none', ec='y', linewidth = 1, scale = 500)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 4, color='c', linestyle = '-',fc='none', ec='c', linewidth = 1, scale = 500)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 4, scale = 3500)

# scale = 0.0003
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_fp[4,4], grad_turbinecosts_power_fp[4,4], headlength = 2, headaxislength = 2, color='b', linestyle = '-', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_fp[4,4], grad_foundationcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='g', linestyle = '-', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_fp[4,4], grad_oandmcosts_power_fp[4,4], headlength = 2, color='r', headaxislength = 2,linestyle = '-', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_fp[4,4], grad_installationcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='m', linestyle = '-', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_fp[4,4], grad_electricalcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='y', linestyle = '-', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_fp[4,4], grad_other_costs_power_fp[4,4], headlength = 2,headaxislength = 2, color='c', linestyle = '-', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_fp[4,4], grad_num_power_fp[4,4], headlength = 2, headaxislength = 2,scale = scale)
#
#
# axs[0].legend(['Turbine', 'Foundation', 'O&M', 'Installation', 'Electrical', 'Other costs', 'Total costs'])

# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 0.9*10e6)

# scale = 0.001
# axs[1].quiver(D_baseline[4,4], P_baseline[4,4], grad_wake_dia_fp[4,4], grad_wake_power_fp[4,4], headlength = 2, headaxislength = 2, color='b', linestyle = '-', linewidth = 1, scale = 1e-10)
# axs[1].quiver(D_baseline[4,4], P_baseline[4,4], grad_aep_noloss_dia_fp[4,4], grad_aep_noloss_power_fp[4,4], headlength = 2, headaxislength = 2, color='r', linestyle = '-',linewidth = 1, scale = scale)
# axs[1].quiver(D_baseline[4,4], P_baseline[4,4], grad_aep_dia_fp[4,4], grad_aep_power_fp[4,4], headlength = 4, scale = scale)

# axs[1].legend(['Wake losses', 'Gross AEP', 'Net AEP'])

# x_tick_labels = [str(round(i,1)) for i in dia_values]
# y_tick_labels = [str(round(i,1)) for i in power_values]
#
# axs[0].set_xticklabels(x_tick_labels)
# axs[0].set_yticklabels(y_tick_labels)
# axs[0].set_title('Baseline vs 1400 MW')
# axs[0].set_ylabel('Rated power', fontsize = 16)
# axs[0].set_xlabel('Rotor diameter', fontsize = 16)
# axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
#
# axs[1].set_title('Baseline vs Low wind')
# axs[1].set_xlabel('Rotor diameter', fontsize = 16)
# axs[1].set_ylabel('Rated power', fontsize = 16)
# axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# #plt.savefig('gradient_components_baseline_vs_farmpower1400.png',bbox_inches='tight',dpi=300)
# plt.show()


######################## Comparing baseline, low wind, farm power cost and AEP plots ##########################


#
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
# scale = 0.001
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_lw[4,4], grad_num_power_lw[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_fp[4,4], grad_num_power_fp[4,4], headlength = 2, headaxislength = 2, color='C2', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
#
# axs[1].quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', linewidth = 1, scale = scale)
# axs[1].quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_lw[4,4], grad_aep_power_lw[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
# axs[1].quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_fp[4,4], grad_aep_power_fp[4,4], headlength = 2, headaxislength = 2, color='C2', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
#
# axs[0].legend(['Cost Baseline', 'Cost Low wind', 'Cost 1400 MW'])
# axs[1].legend(['AEP Baseline', 'AEP low wind', 'AEP 1400 MW'])
# axs[0].set_xlabel('Rotor diameter', fontsize = 16)
# axs[1].set_xlabel('Rotor diameter', fontsize = 16)
# axs[0].set_ylabel('Rated power', fontsize = 16)
# axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# plt.show()


fig, ax = plt.subplots(nrows =1, ncols= 1, figsize=(5.3,4.5))
scale = 0.0013
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', linewidth = 1, scale = scale)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_lw[4,4], grad_num_power_lw[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_fp[4,4], grad_num_power_fp[4,4], headlength = 2, headaxislength = 2, color='C2', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)

ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', linewidth = 1, scale = scale)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_lw[4,4], grad_aep_power_lw[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_fp[4,4], grad_aep_power_fp[4,4], headlength = 2, headaxislength = 2, color='C2', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)

ax.scatter(D_baseline[4,4], P_baseline[4,4], s=40, color ='black')
ax.legend(['Baseline', 'Low wind', 'High farm power'])
ax.set_xlabel('Rotor diameter', fontsize = 16)
ax.set_ylabel('Rated power', fontsize = 16)
ax.text(0.2, 0.75, r'$\'{Cost}$', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes)
ax.text(0.8, 0.25, r'$\'{AEP}$', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes)
ax.text(0.53, 0.45, r'Global optimum (Baseline)', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes) #, weight="bold")
# ax.tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# plt.savefig('gradient_baseline_vs_farmpower1400_&_lowwind.png',bbox_inches='tight',dpi=300)
plt.show()




################## POLAR PLOTS FOR GRADIENTS ########################

# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))

fig, axs = plt.subplots(nrows =1, ncols= 1, figsize=(5.3,4.5), subplot_kw={'projection': 'polar'})

x,y = [0,0]
import math

theta_num_b = (180 - math.degrees(math.atan(abs(grad_num_power_b[4,4]/grad_num_dia_b[4,4]))))*np.pi/180
mag_num_b = np.sqrt(grad_num_power_b[4,4]**2 + grad_num_dia_b[4,4]**2)
theta_aep_b = (360 - math.degrees(math.atan(abs(grad_aep_power_b[4,4]/grad_aep_dia_b[4,4]))))*np.pi/180
mag_aep_b = np.sqrt(grad_aep_power_b[4,4]**2 + grad_aep_dia_b[4,4]**2)


theta_num_lw = (180 - math.degrees(math.atan(abs(grad_num_power_lw[4,4]/grad_num_dia_lw[4,4]))))*np.pi/180
mag_num_lw = np.sqrt(grad_num_power_lw[4,4]**2 + grad_num_dia_lw[4,4]**2)/mag_num_b
theta_aep_lw = (360 - math.degrees(math.atan(abs(grad_aep_power_lw[4,4]/grad_aep_dia_lw[4,4]))))*np.pi/180
mag_aep_lw = np.sqrt(grad_aep_power_lw[4,4]**2 + grad_aep_dia_lw[4,4]**2)/mag_aep_b

print(mag_num_lw, mag_aep_lw)

theta_num_fp = (180 - math.degrees(math.atan(abs(grad_num_power_fp[4,4]/grad_num_dia_fp[4,4]))))*np.pi/180
mag_num_fp = np.sqrt(grad_num_power_fp[4,4]**2 + grad_num_dia_fp[4,4]**2)/mag_num_b
theta_aep_fp = (360 - math.degrees(math.atan(abs(grad_aep_power_fp[4,4]/grad_aep_dia_fp[4,4]))))*np.pi/180
mag_aep_fp = np.sqrt(grad_aep_power_fp[4,4]**2 + grad_aep_dia_fp[4,4]**2)/mag_aep_b


a2 = axs.annotate("",
            xy=(theta_num_b,1), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C0', alpha=0.7),
            )

a1 = axs.annotate("",
            xy=(theta_num_lw,mag_num_lw), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2 ,mutation_scale=15, color='C1', alpha=0.7),
            )



a3 = axs.annotate("",
            xy=(theta_num_fp,mag_num_fp), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2, mutation_scale=15, color='C2', alpha=0.7),
            )

a5 = axs.annotate("",
            xy=(theta_aep_b,1), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C0', alpha =0.7),
            )

a4 = axs.annotate("",
            xy=(theta_aep_lw,mag_aep_lw), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C1', alpha =0.7),
            )



a6 = axs.annotate("",
            xy=(theta_aep_fp,mag_aep_fp), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3", lw = 2,mutation_scale=15,color='C2', alpha =0.7),
            )


axs.plot([],[], '', label = 'Baseline')
axs.plot([],[], '', label = 'Low wind ($0.85\cdot w_\mathrm{s}$)')
axs.plot([],[], '', label = 'High farm power (1400 MW)')


# axs.set_rticks([0.25, 0.75,1.25, 1.75])
axs.set_rticks([0.5,1, 1.35, 1.75])
axs.grid(True, alpha = 0.7)
axs.text(np.pi/180*346,0.65, 'D', fontsize = 12)
axs.text(np.pi/180*100,0.65, 'P', fontsize = 12)
axs.set_xticklabels([])
axs.scatter(0,0, s=10, color='k', alpha=1)
axs.text(np.pi/180*148,1.35, r'$\'{Cost}$', fontsize = 12)
axs.text(np.pi/180*335,1.36, r'$\'{AEP}$', fontsize = 12)
axs.text(np.pi/180*190,1, 'Baseline optimum', fontsize = 10)
axs.legend(loc = 'lower center', fontsize = 12,ncol=1)
axs.spines['polar'].set_visible(False)
plt.savefig('gradient_components_baseline_vs_farmpower1400_&_lowwind_polar.png',bbox_inches='tight',dpi=300)

plt.show()