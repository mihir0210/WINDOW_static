
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



################################## Fixed power only #######################

power_values = np.array([10.0, 10.99, 12.05, 12.99, 14.08, 14.93, 16.13, 17.24, 18.18, 19.23, 20.0])
rad_values = [90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0,135.0, 140.0, 145.0, 150.0]
dia_values = np.array([r*2 for r in rad_values])

dia_values = (dia_values-np.min(dia_values))/(np.max(dia_values)-np.min(dia_values))
power_values = (power_values-np.min(power_values))/(np.max(power_values)-np.min(power_values))

P_fixedpower = np.load("power_matrix_1000MW_course_5D.dat", allow_pickle=True)
D_fixedpower  = np.load("diameter_matrix_1000MW_course_5D.dat", allow_pickle=True)
num_fixedpower = np.load("num_matrix_1000MW_course_5D.dat", allow_pickle=True)
aep_fixedpower = np.load("aep_matrix_1000MW_course_5D.dat", allow_pickle=True)
lcoe_fixedpower = np.load("lcoe_matrix_1000MW_course_5D.dat", allow_pickle=True)




aep_noloss = np.load("lossless_aep_1000MW_course_5D.dat", allow_pickle=True)
v_mean = np.load("v_mean_matrix_1000MW_course_5D.dat", allow_pickle=True)
wake_losses = np.load("wake_matrix_1000MW_course_5D.dat", allow_pickle=True)
total_turbine_costs = np.load("turbine_costs_matrix_1000MW_course_5D.dat", allow_pickle=True)
foundation_costs = np.load("foundation_costs_matrix_1000MW_course_5D.dat", allow_pickle=True)
total_oandm_costs = np.load("oandm_costs_matrix_1000MW_course_5D.dat", allow_pickle=True)
total_installation_costs = np.load("installation_costs_matrix_1000MW_course_5D.dat", allow_pickle=True)
total_electrical_costs = np.load("electrical_costs_matrix_1000MW_course_5D.dat", allow_pickle=True)
other_turbine_costs = np.load('other_turbine_costs_1000MW_course_5D.dat', allow_pickle=True)
other_farm_costs = np.load('other_farm_costs_1000MW_course_5D.dat', allow_pickle=True)
projectdev_costs = np.load('projectdev_costs_1000MW_course_5D.dat', allow_pickle=True)
decom_costs = np.load('decom_costs_1000MW_course_5D.dat', allow_pickle=True)

num_fixedpower = num_fixedpower*-1*0.97*0.97/1e6
aep_fixedpower = aep_fixedpower
lcoe_fixedpower = lcoe_fixedpower*-1

wake_fixedpower = wake_losses*-1 #/wake_losses[4,4]
aep_noloss_fixedpower = aep_noloss #/aep_noloss[4,4]

total_turbine_costs_fixedpower = total_turbine_costs*-1 #/total_turbine_costs[4,4]
foundation_costs_fixedpower = foundation_costs*-1 #/foundation_costs[4,4]
oandm_costs_fixedpower = total_oandm_costs*-1 #/oandm_costs[4,4]
installation_costs_fixedpower = total_installation_costs*-1 #/total_installation_costs[4,4]
electrical_costs_fixedpower = total_electrical_costs*-1 #/total_electrical_costs[4,4]
other_turbine_costs_fixedpower = other_turbine_costs*-1
other_farm_costs_fixedpower = other_farm_costs*-1
projectdev_costs_fixedpower = projectdev_costs*-1
decom_costs_fixedpower = decom_costs*-1


grad_num_dia_fp  = np.gradient(num_fixedpower,dia_values, axis = 1)/aep_fixedpower
grad_num_power_fp  = np.gradient(num_fixedpower, power_values, axis = 0)/aep_fixedpower

grad_turbinecosts_dia_fp  = np.gradient(total_turbine_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_foundationcosts_dia_fp  = np.gradient(foundation_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_oandmcosts_dia_fp  = np.gradient(oandm_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_installationcosts_dia_fp  = np.gradient(installation_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_electricalcosts_dia_fp  = np.gradient(electrical_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_other_turbine_costs_dia_fp  = np.gradient(other_turbine_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_other_farm_costs_dia_fp  = np.gradient(other_farm_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_projectdev_costs_dia_fp  = np.gradient(projectdev_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower
grad_decom_costs_dia_fp  = np.gradient(decom_costs_fixedpower, dia_values, axis = 1)/aep_fixedpower

grad_turbinecosts_power_fp  = np.gradient(total_turbine_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_foundationcosts_power_fp  = np.gradient(foundation_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_oandmcosts_power_fp  = np.gradient(oandm_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_installationcosts_power_fp  = np.gradient(installation_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_electricalcosts_power_fp  = np.gradient(electrical_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_other_turbine_costs_power_fp  = np.gradient(other_turbine_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_other_farm_costs_power_fp  = np.gradient(other_farm_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_projectdev_costs_power_fp  = np.gradient(projectdev_costs_fixedpower, power_values, axis = 0)/aep_fixedpower
grad_decom_costs_power_fp  = np.gradient(decom_costs_fixedpower, power_values, axis = 0)/aep_fixedpower

grad_other_costs_dia_fp  = grad_other_turbine_costs_dia_fp + grad_other_farm_costs_dia_fp + grad_projectdev_costs_dia_fp + grad_decom_costs_dia_fp
grad_other_costs_power_fp  = grad_other_turbine_costs_power_fp + grad_other_farm_costs_power_fp + grad_projectdev_costs_power_fp + grad_decom_costs_power_fp



grad_aep_dia_fp  = np.gradient(aep_fixedpower,dia_values, axis = 1)*-num_fixedpower/(aep_fixedpower**2)
grad_aep_power_fp  = np.gradient(aep_fixedpower,power_values, axis = 0)*-num_fixedpower/(aep_fixedpower**2)

grad_wake_dia_fp  = -1*aep_noloss_fixedpower*np.gradient(wake_fixedpower,dia_values, axis = 1)*-num_fixedpower/(aep_fixedpower**2)
grad_wake_power_fp  = -1*aep_noloss_fixedpower*np.gradient(wake_fixedpower,power_values, axis = 0)*-num_fixedpower/(aep_fixedpower**2)

grad_aep_noloss_dia_fp  = (1 + wake_fixedpower)*np.gradient(aep_noloss_fixedpower,dia_values, axis = 1)*-num_fixedpower/(aep_fixedpower**2)
grad_aep_noloss_power_fp  = (1 + wake_fixedpower)*np.gradient(aep_noloss_fixedpower, power_values, axis = 0)*-num_fixedpower/(aep_fixedpower**2)

grad_lcoe_dia = np.gradient(lcoe_fixedpower,dia_values, axis = 1)
grad_lcoe_power = np.gradient(lcoe_fixedpower,power_values, axis = 0)
# norm_dia = np.linalg.norm(grad_aep_dia)
# norm_power = np.linalg.norm(grad_aep_power)
# grad_aep_dia = grad_aep_dia/norm_dia
# grad_aep_power = grad_aep_power/norm_power

# mag_num_fixedarea = np.sqrt(grad_num_dia**2 + grad_num_power**2)
# mag_aep_fixedarea = np.sqrt(grad_aep_dia**2 + grad_aep_power**2)
#
# ratio_mag = mag_num_fixedarea/mag_aep_fixedarea
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


# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
#
# axs[0].quiver(D_fixedarea, P_fixedarea,  grad_num_dia, grad_num_power, color = 'r', headlength = 4, scale = 15, alpha = 0.6)
#
# axs[1].quiver(D_fixedarea,  P_fixedarea, grad_aep_dia, grad_aep_power, color = 'r', headlength = 4, scale = 15, alpha = 0.6)

## axs[0].contourf(D_baseline, P_baseline, mag_num)
# axs[0].colorbar()
#
# axs[1].contourf(D_baseline, P_baseline, mag_aep)
# axs[1].colorbar()
# plt.show()



# fig, axs = plt.subplots()
# axs.quiver(D_fixedarea , P_fixedarea ,  grad_lcoe_dia, grad_lcoe_power, color='r', headlength = 4, alpha = 0.5)
# #
# axs.set_ylabel('Rated power (MW)', fontsize = 16)
# axs.set_xlabel('Rotor diameter (m)', fontsize = 16)
# plt.title("Baseline vs Fixed power (1000 MW)", fontsize = 16)
# plt.show()

######################### FIXED AREA ONLY ####################


power_values = np.array([10, 12, 14, 16, 18, 19, 20])
rad_values = [90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]
dia_values = np.array([r*2 for r in rad_values])

dia_values = (dia_values-np.min(dia_values))/(np.max(dia_values)-np.min(dia_values))
power_values = (power_values-np.min(power_values))/(np.max(power_values)-np.min(power_values))

P_fixedarea = np.load("power_matrix_area150_course_5D.dat", allow_pickle=True)
D_fixedarea  = np.load("diameter_matrix_area150_course_5D.dat", allow_pickle=True)
num_fixedarea = np.load("num_matrix_area150_course_5D.dat", allow_pickle=True)
aep_fixedarea = np.load("aep_matrix_area150_course_5D.dat", allow_pickle=True)
lcoe_fixedarea = np.load("lcoe_matrix_area150_course_5D.dat", allow_pickle=True)




aep_noloss = np.load("lossless_aep_area150_course_5D.dat", allow_pickle=True)
v_mean = np.load("v_mean_matrix_area150_course_5D.dat", allow_pickle=True)
wake_losses = np.load("wake_matrix_area150_course_5D.dat", allow_pickle=True)
total_turbine_costs = np.load("turbine_costs_matrix_area150_course_5D.dat", allow_pickle=True)
foundation_costs = np.load("foundation_costs_matrix_area150_course_5D.dat", allow_pickle=True)
total_oandm_costs = np.load("oandm_costs_matrix_area150_course_5D.dat", allow_pickle=True)
total_installation_costs = np.load("installation_costs_matrix_area150_course_5D.dat", allow_pickle=True)
total_electrical_costs = np.load("electrical_costs_matrix_area150_course_5D.dat", allow_pickle=True)
other_turbine_costs = np.load('other_turbine_costs_area150_course_5D.dat', allow_pickle=True)
other_farm_costs = np.load('other_farm_costs_area150_course_5D.dat', allow_pickle=True)
projectdev_costs = np.load('projectdev_costs_area150_course_5D.dat', allow_pickle=True)
decom_costs = np.load('decom_costs_area150_course_5D.dat', allow_pickle=True)

num_fixedarea = num_fixedarea*-1*0.97*0.97/1e6
aep_fixedarea = aep_fixedarea
lcoe_fixedarea = lcoe_fixedarea*-1

wake_fixedarea = wake_losses*-1 #/wake_losses[4,4]
aep_noloss_fixedarea = aep_noloss #/aep_noloss[4,4]

total_turbine_costs_fixedarea = total_turbine_costs*-1 #/total_turbine_costs[4,4]
foundation_costs_fixedarea = foundation_costs*-1 #/foundation_costs[4,4]
oandm_costs_fixedarea = total_oandm_costs*-1 #/oandm_costs[4,4]
installation_costs_fixedarea = total_installation_costs*-1 #/total_installation_costs[4,4]
electrical_costs_fixedarea = total_electrical_costs*-1 #/total_electrical_costs[4,4]
other_turbine_costs_fixedarea = other_turbine_costs*-1
other_farm_costs_fixedarea = other_farm_costs*-1
projectdev_costs_fixedarea = projectdev_costs*-1
decom_costs_fixedarea = decom_costs*-1


grad_num_dia_fa  = np.gradient(num_fixedarea,dia_values, axis = 1)/aep_fixedarea
grad_num_power_fa  = np.gradient(num_fixedarea, power_values, axis = 0)/aep_fixedarea

grad_turbinecosts_dia_fa  = np.gradient(total_turbine_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_foundationcosts_dia_fa  = np.gradient(foundation_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_oandmcosts_dia_fa  = np.gradient(oandm_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_installationcosts_dia_fa  = np.gradient(installation_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_electricalcosts_dia_fa  = np.gradient(electrical_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_other_turbine_costs_dia_fa  = np.gradient(other_turbine_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_other_farm_costs_dia_fa  = np.gradient(other_farm_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_projectdev_costs_dia_fa  = np.gradient(projectdev_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea
grad_decom_costs_dia_fa  = np.gradient(decom_costs_fixedarea, dia_values, axis = 1)/aep_fixedarea

grad_turbinecosts_power_fa  = np.gradient(total_turbine_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_foundationcosts_power_fa  = np.gradient(foundation_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_oandmcosts_power_fa  = np.gradient(oandm_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_installationcosts_power_fa  = np.gradient(installation_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_electricalcosts_power_fa  = np.gradient(electrical_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_other_turbine_costs_power_fa  = np.gradient(other_turbine_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_other_farm_costs_power_fa  = np.gradient(other_farm_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_projectdev_costs_power_fa  = np.gradient(projectdev_costs_fixedarea, power_values, axis = 0)/aep_fixedarea
grad_decom_costs_power_fa  = np.gradient(decom_costs_fixedarea, power_values, axis = 0)/aep_fixedarea

grad_other_costs_dia_fa  = grad_other_turbine_costs_dia_fa + grad_other_farm_costs_dia_fa + grad_projectdev_costs_dia_fa + grad_decom_costs_dia_fa
grad_other_costs_power_fa  = grad_other_turbine_costs_power_fa + grad_other_farm_costs_power_fa + grad_projectdev_costs_power_fa + grad_decom_costs_power_fa



grad_aep_dia_fa  = np.gradient(aep_fixedarea,dia_values, axis = 1)*-num_fixedarea/(aep_fixedarea**2)
grad_aep_power_fa  = np.gradient(aep_fixedarea,power_values, axis = 0)*-num_fixedarea/(aep_fixedarea**2)

grad_wake_dia_fa  = -1*aep_noloss_fixedarea*np.gradient(wake_fixedarea,dia_values, axis = 1)*-num_fixedarea/(aep_fixedarea**2)
grad_wake_power_fa  = -1*aep_noloss_fixedarea*np.gradient(wake_fixedarea,power_values, axis = 0)*-num_fixedarea/(aep_fixedarea**2)

grad_aep_noloss_dia_fa  = (1 + wake_fixedarea)*np.gradient(aep_noloss_fixedarea,dia_values, axis = 1)*-num_fixedarea/(aep_fixedarea**2)
grad_aep_noloss_power_fa  = (1 + wake_fixedarea)*np.gradient(aep_noloss_fixedarea, power_values, axis = 0)*-num_fixedarea/(aep_fixedarea**2)

grad_lcoe_dia = np.gradient(lcoe_fixedarea,dia_values, axis = 1)
grad_lcoe_power = np.gradient(lcoe_fixedarea,power_values, axis = 0)
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


# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))

# axs[0].quiver(D_fixedarea, P_fixedarea,  grad_num_dia, grad_num_power, color = 'r', headlength = 4, scale = 15, alpha = 0.6)
#
# axs[1].quiver(D_fixedarea,  P_fixedarea, grad_aep_dia, grad_aep_power, color = 'r', headlength = 4, scale = 15, alpha = 0.6)

## axs[0].contourf(D_baseline, P_baseline, mag_num)
# axs[0].colorbar()
#
# axs[1].contourf(D_baseline, P_baseline, mag_aep)
# axs[1].colorbar()
# plt.show()


fig, ax = plt.subplots(nrows =1, ncols= 1, figsize=(4.5,4))
scale = 0.0013
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', linewidth = 1, scale = scale)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_fp[4,4], grad_num_power_fp[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_fa[2,4], grad_num_power_fa[2,4], headlength = 2, headaxislength = 2, color='C2', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)

ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', linewidth = 1, scale = scale)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_fp[4,4], grad_aep_power_fp[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)
ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_aep_dia_fa[2,4], grad_aep_power_fa[2,4], headlength = 2, headaxislength = 2, color='C2', linestyle = '-', linewidth = 1, scale = scale, alpha = 0.7)

ax.scatter(D_baseline[4,4], P_baseline[4,4], s=40, color ='black')
ax.legend(['Baseline', 'Fixed power only', 'Fixed area only'])
ax.set_xlabel('Rotor diameter', fontsize = 14)
ax.set_ylabel('Rated power', fontsize = 14)
ax.text(0.18, 0.6, r'$\'{Cost}$', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes)
ax.text(0.8, 0.27, r'$\'{AEP}$', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes)
ax.text(0.5, 0.45, r'Global optimum (Baseline)', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes) #, weight="bold")
ax.text(0.6, 0.27, r'$\'{Cost}$', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes)
ax.text(0.35, 0.75, r'$\'{AEP}$', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes)
ax.tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# plt.savefig('gradient_baseline_vs_fixedpower_&_fixedarea_5D.png',bbox_inches='tight',dpi=300)
plt.show()



#################### POLAR PLOTS ###################


fig, axs = plt.subplots(nrows =1, ncols= 1, figsize=(5.3,4.5), subplot_kw={'projection': 'polar'})

x,y = [0,0]
import math

theta_num_b = (180 - math.degrees(math.atan(abs(grad_num_power_b[4,4]/grad_num_dia_b[4,4]))))*np.pi/180
mag_num_b = np.sqrt(grad_num_power_b[4,4]**2 + grad_num_dia_b[4,4]**2)
theta_aep_b = (360 - math.degrees(math.atan(abs(grad_aep_power_b[4,4]/grad_aep_dia_b[4,4]))))*np.pi/180
mag_aep_b = np.sqrt(grad_aep_power_b[4,4]**2 + grad_aep_dia_b[4,4]**2)


theta_num_fp = (180 - math.degrees(math.atan(abs(grad_num_power_fp[4,4]/grad_num_dia_fp[4,4]))))*np.pi/180
mag_num_fp = np.sqrt(grad_num_power_fp[4,4]**2 + grad_num_dia_fp[4,4]**2)/mag_num_b
theta_aep_fp = (360 - math.degrees(math.atan(abs(grad_aep_power_fp[4,4]/grad_aep_dia_fp[4,4]))))*np.pi/180
mag_aep_fp = np.sqrt(grad_aep_power_fp[4,4]**2 + grad_aep_dia_fp[4,4]**2)/mag_aep_b

axs.annotate("",
            xy=(theta_num_b,1), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C0', alpha=0.7),
            )

axs.annotate("",
            xy=(theta_num_fp,mag_num_fp), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2 ,mutation_scale=15, color='C1', alpha=0.7),
            )

axs.annotate("",
            xy=(theta_aep_b,1), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C0', alpha =0.7),
             )

axs.annotate("",
            xy=(theta_aep_fp,mag_aep_fp), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C1', alpha =0.7),
             )

axs.plot([],[], '', label = 'Baseline')
axs.plot([],[], '', label = 'Fixed power only')
axs.set_rticks([0.5,1, 1.5])
axs.grid(True, alpha = 0.7)
axs.text(np.pi/180*348,0.65, 'D', fontsize = 12)
axs.text(np.pi/180*100,0.65, 'P', fontsize = 12)
axs.set_xticklabels([])
axs.scatter(0,0, s=10, color='k', alpha=1)
axs.text(np.pi/180*155,1.33, r'$\'{Cost}$', fontsize = 12)
axs.text(np.pi/180*340,1.15, r'$\'{AEP}$', fontsize = 12)
axs.text(np.pi/180*190,0.95, 'Baseline optimum', fontsize = 10)
axs.legend(loc = 'lower center', fontsize = 12,ncol=1)
axs.spines['polar'].set_visible(False)
plt.savefig('gradient_baseline_vs_fixedpower.png',bbox_inches='tight',dpi=300)

plt.show()






fig, axs = plt.subplots(nrows =1, ncols= 1, figsize=(5.3,4.5), subplot_kw={'projection': 'polar'})

x,y = [0,0]
import math

theta_num_b = (180 - math.degrees(math.atan(abs(grad_num_power_b[2,4]/grad_num_dia_b[2,4]))))*np.pi/180
mag_num_b = np.sqrt(grad_num_power_b[2,4]**2 + grad_num_dia_b[2,4]**2)
theta_aep_b = (360 - math.degrees(math.atan(abs(grad_aep_power_b[2,4]/grad_aep_dia_b[2,4]))))*np.pi/180
mag_aep_b = np.sqrt(grad_aep_power_b[2,4]**2 + grad_aep_dia_b[2,4]**2)


theta_num_fa = (360 - math.degrees(math.atan(abs(grad_num_power_fa[2,4]/grad_num_dia_fa[2,4]))))*np.pi/180
mag_num_fa = np.sqrt(grad_num_power_fa[2,4]**2 + grad_num_dia_fa[2,4]**2)/mag_num_b
theta_aep_fa = (180 - math.degrees(math.atan(abs(grad_aep_power_fa[2,4]/grad_aep_dia_fa[2,4]))))*np.pi/180
mag_aep_fa = np.sqrt(grad_aep_power_fa[2,4]**2 + grad_aep_dia_fa[2,4]**2)/mag_aep_b



axs.annotate("",
            xy=(theta_num_b,1), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C0', alpha=0.7),
            )

axs.annotate("",
            xy=(theta_num_fa,mag_num_fa), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2 ,mutation_scale=15, color='C1', alpha=0.7),
            )

axs.annotate("",
            xy=(theta_aep_b,1), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C0', alpha =0.7),
             )

axs.annotate("",
            xy=(theta_aep_fa,mag_aep_fa), xycoords='data',
            xytext=(x,y), textcoords='data',
            arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="arc3",lw = 2,mutation_scale=15, color='C1', alpha =0.7),
             )

axs.plot([],[], '', label = 'Baseline')
axs.plot([],[], '', label = 'Fixed area only')
axs.set_rticks([0.5,0.75, 1])
axs.grid(True, alpha = 0.7)
axs.text(np.pi/180*348,0.625, 'D', fontsize = 12)
axs.text(np.pi/180*100,0.625, 'P', fontsize = 12)
axs.set_xticklabels([])
axs.scatter(0,0, s=10, color='k', alpha=1)
axs.text(np.pi/180*160,0.95, r'$\'{Cost}$', fontsize = 12, color='C0')
axs.text(np.pi/180*335,0.8, r'$\'{AEP}$', fontsize = 12, color='C0')
axs.text(np.pi/180*290,0.6, r'$\'{Cost}$', fontsize = 12, color='C1')
axs.text(np.pi/180*127,0.82, r'$\'{AEP}$', fontsize = 12, color='C1')
axs.text(np.pi/180*190,0.6, 'Baseline optimum', fontsize = 10)
axs.legend(loc = 'lower center', fontsize = 12,ncol=1)
axs.spines['polar'].set_visible(False)
plt.savefig('gradient_baseline_vs_fixedarea.png',bbox_inches='tight',dpi=300)

plt.show()



############## BASELINE VS FIXED POWER COMPONENTS ###########

#
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
#
#
# scale = 0.0003
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='none', ec='C2', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='none', ec='C3', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-',fc='none', ec='C4', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-',fc='none', ec='C5', linewidth = 1, scale = scale)
#
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_fp[4,4], grad_turbinecosts_power_fp[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', ec='C0', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_fp[4,4], grad_other_costs_power_fp[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-', ec='C1', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_fp[4,4], grad_foundationcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-', ec='C2', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_fp[4,4], grad_installationcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-', ec='C3', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_fp[4,4], grad_oandmcosts_power_fp[4,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-', ec='C4', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_fp[4,4], grad_electricalcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-', ec='C5', linewidth = 1, scale = scale, alpha = 0.5)
#
#
# #axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2,scale = scale, alpha = 0.5)
#
#
# axs[0].legend(['Turbine', 'Other costs', 'Foundation',  'Installation', 'O&M', 'Electrical'])
#
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 0.9*10e6)
#
# scale = 0.0007
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_b[4,4], -1*grad_wake_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
#
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_fp[4,4], -1*grad_wake_power_fp[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', ec='C0', linewidth = 1, scale = scale, alpha = 0.5)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_fp[4,4], grad_aep_noloss_power_fp[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', ec='C1', linewidth = 1, scale = scale, alpha = 0.5)
# #axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = scale, alpha = 0.5)
#
# axs[1].legend(['Wake losses', 'Gross AEP'])
#
#
#
# # x_tick_labels = [str(round(i,1)) for i in dia_values]
# # y_tick_labels = [str(round(i,1)) for i in power_values]
# #
# # axs[0].set_xticklabels(x_tick_labels)
# # axs[0].set_yticklabels(y_tick_labels)
# axs[0].set_ylabel('Rated power', fontsize = 16)
# axs[0].set_xlabel('Rotor diameter', fontsize = 16)
# axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[0].set_title('Cost components', fontsize = 16)
#
# axs[1].set_xlabel('Rotor diameter', fontsize = 16)
# axs[1].set_ylabel('Rated power', fontsize = 16)
# axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[1].set_title('AEP components', fontsize = 16)
# # axs[1].text(0.6, 0.25, r'$\'{AEP_{gross}}*(1 + \lambda_{wake})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# # axs[1].text(0.5, 0.6, r'$AEP_{gross}*(1 + \'{\lambda_{wake}})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
#
# #plt.savefig('gradient_components_baseline_vs_fixedpower.png',bbox_inches='tight',dpi=300)
# #plt.show()

#
fig, axs = plt.subplots(nrows =1, ncols= 1, figsize=(4.5,4))


#scale = 0.00022

scale = 0.00015

#axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
#axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='none', ec='C3', linewidth = 1, scale = scale)
axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-',fc='none', ec='C5', linewidth = 1, scale = 0.00007)
axs.quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_b[4,4], -1*grad_wake_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)

#axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_fp[4,4], grad_other_costs_power_fp[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-', ec='C1', linewidth = 1, scale = scale, alpha = 0.5)
#axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_fp[4,4], grad_installationcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-', ec='C3', linewidth = 1, scale = scale, alpha = 0.5)
axs.quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_fp[4,4], grad_electricalcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-', ec='C5', linewidth = 1, scale = 0.00007, alpha = 0.7)
axs.quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_fp[4,4], -1*grad_wake_power_fp[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', ec='C0', linewidth = 1, scale = scale, alpha = 0.7)



#axs.legend(['Other costs', 'Installation', 'Electrical', 'Wake losses'])
axs.legend(['Electrical', 'Wake losses'])



# x_tick_labels = [str(round(i,1)) for i in dia_values]
# y_tick_labels = [str(round(i,1)) for i in power_values]
#
# axs[0].set_xticklabels(x_tick_labels)
# axs[0].set_yticklabels(y_tick_labels)
axs.set_ylabel('Rated power', fontsize = 14)
axs.set_xlabel('Rotor diameter', fontsize = 14)
axs.tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
axs.set_title('Differing components', fontsize = 14)


# axs[1].text(0.6, 0.25, r'$\'{AEP_{gross}}*(1 + \lambda_{wake})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# axs[1].text(0.5, 0.6, r'$AEP_{gross}*(1 + \'{\lambda_{wake}})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)

# plt.savefig('gradient_components_baseline_vs_fixedpower_5D.png',bbox_inches='tight',dpi=300)
plt.show()



# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
#
#
# scale = 0.0003
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='none', ec='C2', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='none', ec='C3', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-',fc='none', ec='C4', linewidth = 1, scale = scale)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-',fc='none', ec='C5', linewidth = 1, scale = scale)
#
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_fp[4,4], grad_turbinecosts_power_fp[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', ec='C0', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_fp[4,4], grad_other_costs_power_fp[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-', ec='C1', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_fp[4,4], grad_foundationcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-', ec='C2', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_fp[4,4], grad_installationcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-', ec='C3', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_fp[4,4], grad_oandmcosts_power_fp[4,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-', ec='C4', linewidth = 1, scale = scale, alpha = 0.5)
# axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_fp[4,4], grad_electricalcosts_power_fp[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-', ec='C5', linewidth = 1, scale = scale, alpha = 0.5)
#
#
# #axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2,scale = scale, alpha = 0.5)
#
#
# axs[0].legend(['Turbine', 'Other costs', 'Foundation',  'Installation', 'O&M', 'Electrical'])
#
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
# # axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 0.9*10e6)
#
# scale = 0.0007
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_b[4,4], -1*grad_wake_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
#
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_fp[4,4], -1*grad_wake_power_fp[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', ec='C0', linewidth = 1, scale = scale, alpha = 0.5)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_fp[4,4], grad_aep_noloss_power_fp[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', ec='C1', linewidth = 1, scale = scale, alpha = 0.5)
# #axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = scale, alpha = 0.5)
#
# axs[1].legend(['Wake losses', 'Gross AEP'])
#
#
#
# # x_tick_labels = [str(round(i,1)) for i in dia_values]
# # y_tick_labels = [str(round(i,1)) for i in power_values]
# #
# # axs[0].set_xticklabels(x_tick_labels)
# # axs[0].set_yticklabels(y_tick_labels)
# axs[0].set_ylabel('Rated power', fontsize = 16)
# axs[0].set_xlabel('Rotor diameter', fontsize = 16)
# axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[0].set_title('Differing cost components', fontsize = 16)
#
# axs[1].set_xlabel('Rotor diameter', fontsize = 16)
# axs[1].set_ylabel('Rated power', fontsize = 16)
# axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[1].set_title('Differing AEP components', fontsize = 16)
#
# # #plt.savefig('gradient_components_baseline_vs_fixedpower.png',bbox_inches='tight',dpi=300)
# plt.show()


############ BASELINE VS FIXED AREA COMPONENTS ###########



fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))


scale = 0.0003
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_b[4,4], grad_turbinecosts_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_b[4,4], grad_other_costs_power_b[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_b[4,4], grad_foundationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='none', ec='C2', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_b[4,4], grad_installationcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='none', ec='C3', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_b[4,4], grad_oandmcosts_power_b[4,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-',fc='none', ec='C4', linewidth = 1, scale = scale)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_b[4,4], grad_electricalcosts_power_b[4,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-',fc='none', ec='C5', linewidth = 1, scale = scale)

axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_turbinecosts_dia_fa[2,4], grad_turbinecosts_power_fa[2,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', ec='C0', linewidth = 1, scale = scale, alpha = 0.7)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_other_costs_dia_fa[2,4], grad_other_costs_power_fa[2,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-', ec='C1', linewidth = 1, scale = scale, alpha = 0.7)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_foundationcosts_dia_fa[2,4], grad_foundationcosts_power_fa[2,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-', ec='C2', linewidth = 1, scale = scale, alpha = 0.7)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_installationcosts_dia_fa[2,4], grad_installationcosts_power_fa[2,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-', ec='C3', linewidth = 1, scale = scale, alpha = 0.7)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_oandmcosts_dia_fa[2,4], grad_oandmcosts_power_fa[2,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-', ec='C4', linewidth = 1, scale = scale, alpha = 0.7)
axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_electricalcosts_dia_fa[2,4], grad_electricalcosts_power_fa[2,4], headlength = 2, headaxislength = 2,color='C5', linestyle = '-', ec='C5', linewidth = 1, scale = scale, alpha = 0.7)


#axs[0].quiver(D_baseline[4,4], P_baseline[4,4],  grad_num_dia_b[4,4], grad_num_power_b[4,4], headlength = 2, headaxislength = 2,scale = scale, alpha = 0.5)


axs[0].legend(['Turbine', 'Other costs', 'Foundation',  'Installation', 'O&M', 'Electrical'])

# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_wake_dia_b[4,4], grad_wake_power_b[4,4], headlength = 5, color='b', linestyle = '-',fc='none', ec='b', linewidth = 1, scale=0.5)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 4, color='r', linestyle = '-',fc='none', ec='r', linewidth = 1, scale=10e6)
# axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = 0.9*10e6)

scale = 0.0007
axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_b[4,4], -1*grad_wake_power_b[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1, scale = scale)
axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_b[4,4], grad_aep_noloss_power_b[4,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)

axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], -1*grad_wake_dia_fa[2,4], -1*grad_wake_power_fa[2,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-', ec='C0', linewidth = 1, scale = scale, alpha = 0.7)
axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_noloss_dia_fa[2,4], grad_aep_noloss_power_fa[2,4], headlength = 2, headaxislength = 2, color='C1', linestyle = '-', ec='C1', linewidth = 1, scale = scale, alpha = 0.7)
#axs[1].quiver(D_baseline[4,4],  P_baseline[4,4], grad_aep_dia_b[4,4], grad_aep_power_b[4,4], headlength = 4, scale = scale, alpha = 0.5)

axs[1].legend(['Wake losses', 'Gross AEP'])



# x_tick_labels = [str(round(i,1)) for i in dia_values]
# y_tick_labels = [str(round(i,1)) for i in power_values]
#
# axs[0].set_xticklabels(x_tick_labels)
# axs[0].set_yticklabels(y_tick_labels)
axs[0].set_ylabel('Rated power', fontsize = 14)
axs[0].set_xlabel('Rotor diameter', fontsize = 14)
axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
axs[0].set_title('Differing cost components', fontsize = 14)

axs[1].set_xlabel('Rotor diameter', fontsize = 14)
axs[1].set_ylabel('Rated power', fontsize = 14)
axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
axs[1].set_title('Differing AEP components', fontsize = 14)
# axs[1].text(0.6, 0.25, r'$\'{AEP_{gross}}*(1 + \lambda_{wake})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# axs[1].text(0.5, 0.6, r'$AEP_{gross}*(1 + \'{\lambda_{wake}})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)

# plt.savefig('gradient_components_baseline_vs_fixedarea_5D.png',bbox_inches='tight',dpi=300)
plt.show()