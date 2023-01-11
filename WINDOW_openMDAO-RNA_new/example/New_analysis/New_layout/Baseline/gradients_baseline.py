
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

fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))

# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 4, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale = 2000)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 4, color='g', linestyle = '-',fc='none', ec='g', linewidth = 1, scale = 1000)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale = 1200)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 4, color='m', linestyle = '-',fc='none', ec='m', linewidth = 1, scale = 900)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 4, color='y', linestyle = '-',fc='none', ec='y', linewidth = 1, scale = 500)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 4, color='c', linestyle = '-',fc='none', ec='c', linewidth = 1, scale = 500)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 4, scale = 3500)

scale = 0.0003
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='none', ec='C2', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='none', ec='C3', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-',fc='none', ec='C4', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-',fc='none', ec='C5', linewidth = 1, scale = scale)

#axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2,scale = scale, alpha = 0.5)


axs[0].legend(['Turbine', 'Other costs', 'Foundation',  'Installation', 'O&M', 'Electrical'])

# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 0.9*10e6)

scale = 0.0007
axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_b[4,4], -1*grad_wake_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
#axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = scale, alpha = 0.5)

axs[1].legend(['Wake losses', 'Gross AEP'])



# x_tick_labels = [str(round(i,1)) for i in dia_values]
# y_tick_labels = [str(round(i,1)) for i in power_values]
#
# axs[0].set_xticklabels(x_tick_labels)
# axs[0].set_yticklabels(y_tick_labels)
axs[0].set_ylabel('Rated power', fontsize = 16)
axs[0].set_xlabel('Rotor diameter', fontsize = 16)
axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
axs[0].set_title('Cost components', fontsize = 16)

axs[1].set_xlabel('Rotor diameter', fontsize = 16)
axs[1].set_ylabel('Rated power', fontsize = 16)
axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
axs[1].set_title('AEP components', fontsize = 16)
axs[1].text(0.6, 0.25, r'$\'{AEP_{gross}}*(1 + \lambda_{wake})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
axs[1].text(0.5, 0.6, r'$AEP_{gross}*(1 + \'{\lambda_{wake}})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
#plt.savefig('gradient_components_baseline.png',bbox_inches='tight',dpi=300)
plt.show()



# fig, axs = plt.subplots()
# axs.quiver(D_baseline , P_baseline ,  grad_lcoe_dia, grad_lcoe_power, headlength = 4, scale = 5)
#
# axs.set_ylabel('Rated power (MW)', fontsize = 16)
# axs.set_xlabel('Rotor diameter (m)', fontsize = 16)
# plt.title("Baseline vs 1400 MW", fontsize = 16)
# plt.show()

# fig, axs = plt.subplots(nrows =1, ncols= 3, figsize=(15,4))
#
#
#
# color1 = -1*np.sqrt(abs(grad_num_dia_b)**2 + abs(grad_num_power_b)**2)
# color2 = -1*np.sqrt(abs(grad_aep_dia_b)**2 + abs(grad_aep_power_b)**2)
# color3 = -1*np.sqrt(abs(grad_lcoe_dia)**2 + abs(grad_lcoe_power)**2)
#
# axs[0].quiver(D_baseline, P_baseline,  grad_num_dia_b, grad_num_power_b, color1, headlength = 2, headaxislength = 2)
# axs[1].quiver(D_baseline, P_baseline, grad_aep_dia_b, grad_aep_power_b,color2, headlength = 2, headaxislength = 2)
# axs[2].quiver(D_baseline, P_baseline, grad_lcoe_dia, grad_lcoe_power,color3, headlength = 2, headaxislength = 2)
#
# axs[0].set_ylabel('Rated power (MW)', fontsize = 16)
# axs[0].set_xlabel('Rotor diameter (m)', fontsize = 16)
# #axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[0].set_title('Cost gradients (descent)', fontsize = 16)
#
# axs[1].set_xlabel('Rotor diameter (m)', fontsize = 16)
# #axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[1].set_title('AEP gradients (ascent)', fontsize = 16)
#
# axs[2].set_xlabel('Rotor diameter (m)', fontsize = 16)
# #axs[2].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[2].set_title('LCoE gradients (descent)', fontsize = 16)
# #plt.savefig('gradient_baseline.png',bbox_inches='tight',dpi=300)
# plt.show()




################## Components ####################

#
# fig, axs = plt.subplots()
#
# # axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 4, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale = 2000)
# # axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 4, color='g', linestyle = '-',fc='none', ec='g', linewidth = 1, scale = 1000)
# # axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale = 1200)
# # axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 4, color='m', linestyle = '-',fc='none', ec='m', linewidth = 1, scale = 900)
# # axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 4, color='y', linestyle = '-',fc='none', ec='y', linewidth = 1, scale = 500)
# # axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 4, color='c', linestyle = '-',fc='none', ec='c', linewidth = 1, scale = 500)
# # axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 4, scale = 3500)
#
# scale = 0.0003
# l = 0.5
# axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', linewidth = l, scale = scale)
# axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C1', linestyle = '-', linewidth = l, scale = scale)
# axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 2, color='C2', headaxislength = 2,linestyle = '-', linewidth = l, scale = scale)
# axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-', linewidth = l, scale = scale)
# axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C4', linestyle = '-', linewidth = l, scale = scale)
# axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 2,headaxislength = 2, color='C5', linestyle = '-', linewidth = l, scale = scale)
# #axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2,scale = scale, alpha = 0.5)
#
#
# #axs[0].legend(['Turbine', 'Foundation', 'O&M', 'Installation', 'Electrical', 'Other costs', 'Total costs'])
#
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 0.9*10e6)
#
#
# axs.quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_b[4,4], -1*grad_wake_power_b[4,4], headlength = 2, headaxislength = 2, color='C6', linestyle = '-', linewidth = l, scale = scale)
# axs.quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 2, headaxislength = 2, color='C7', linestyle = '-', linewidth = l, scale = scale)
# #axs.quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = scale, alpha = 0.5)
#
# #axs[1].legend(['Wake losses', 'Gross AEP', 'Net AEP'])
#
# axs.legend(['Turbine', 'Foundation', 'O&M', 'Installation', 'Electrical', 'Other costs', 'Wake losses', 'Gross AEP'])
#
# # x_tick_labels = [str(round(i,1)) for i in dia_values]
# # y_tick_labels = [str(round(i,1)) for i in power_values]
# #
# # axs[0].set_xticklabels(x_tick_labels)
# # axs[0].set_yticklabels(y_tick_labels)
# axs.set_ylabel('Rated power', fontsize = 16)
# axs.set_xlabel('Rotor diameter', fontsize = 16)
# axs.tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
#
# #plt.savefig('gradient_components_baseline.png',bbox_inches='tight',dpi=300)
# plt.show()

