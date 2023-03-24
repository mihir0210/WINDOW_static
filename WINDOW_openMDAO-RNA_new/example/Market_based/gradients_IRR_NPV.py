
import numpy as np
import matplotlib.pyplot as plt

#lcoe_opt = [14.49, 225]
power_values = [10.0, 10.99, 12.05, 12.99, 13.51, 14.08, 14.49, 14.93, 15.62, 16.13, 16.67, 17.24, 18.18, 19.23, 20.0, 22.73]
# n_t_ = [100, 91, 83, 77, 71, 67, 62, 58, 55, 52, 50, 44]
rad_values= [90.0, 95.0, 100.0, 105.0, 215 / 2, 110.0, 222 / 2, 225 / 2, 227 / 2, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]

dia_values = np.array([r*2 for r in rad_values])

dia_values = (dia_values-np.min(dia_values))/(np.max(dia_values)-np.min(dia_values))
power_values = (power_values-np.min(power_values))/(np.max(power_values)-np.min(power_values))

# print(dia_values)
# print(power_values)

P_baseline = np.load("power_matrix_baseline_course.dat", allow_pickle=True)
D_baseline  = np.load("diameter_matrix_baseline_course.dat", allow_pickle=True)
lcoe_baseline = np.load("lcoe_matrix_baseline_course.dat", allow_pickle=True)
lcoe_baseline = lcoe_baseline*-1
num_baseline = np.load("num_matrix_baseline_course.dat", allow_pickle=True)
aep_baseline = np.load("total_aep_matrix_baseline_course.dat", allow_pickle=True)
num_baseline = num_baseline*-1*0.95*0.97/1e6

total_revenue_60_0 = np.load("total_revenue_60_0_course.dat", allow_pickle=True)/1e6
total_revenue_90_0 = np.load("total_revenue_90_0_course.dat", allow_pickle=True)/1e6
total_revenue_90_3 = np.load("total_revenue_90_3_course.dat", allow_pickle=True)/1e6
total_revenue_110_3 = np.load("total_revenue_110_3_course.dat", allow_pickle=True)/1e6
irr_60_0 = np.load("irr_matrix_60_0_course.dat", allow_pickle=True)
npv_60_0  = np.load("npv_matrix_60_0_course.dat", allow_pickle=True)
irr_90_0 = np.load("irr_matrix_90_0_course.dat", allow_pickle=True)
npv_90_0  = np.load("npv_matrix_90_0_course.dat", allow_pickle=True)
irr_90_3 = np.load("irr_matrix_90_3_course.dat", allow_pickle=True)
npv_90_3  = np.load("npv_matrix_90_3_course.dat", allow_pickle=True)
irr_110_3 = np.load("irr_matrix_110_3_course.dat", allow_pickle=True)
npv_110_3  = np.load("npv_matrix_110_3_course.dat", allow_pickle=True)

# irr_slope1 = np.load("irr_matrix_60_1_course.dat", allow_pickle=True)
# npv_slope1 = np.load("npv_matrix_60_1_course.dat", allow_pickle=True)

# irr_60_0 = irr_60_0/np.amax(irr_60_0)
# npv_60_0  = npv_60_0/np.amax(npv_60_0)
# irr_90_0 = irr_90_0/np.amax(irr_90_0)
# npv_90_0 = npv_90_0/np.amax(npv_90_0)
# irr_90_3 = irr_90_3/np.amax(irr_90_3)
# npv_90_3 = npv_90_3/np.amax(npv_90_3)
# irr_110_3 = irr_110_3/np.amax(irr_110_3)
# npv_110_3 = npv_110_3/np.amax(npv_110_3)


# irr_noslope = irr_noslope/np.amax(irr_noslope)
# npv_noslope  = npv_noslope/np.amax(npv_noslope)
# irr_slope1 = irr_slope1/np.amax(irr_slope1)
# npv_slope1 = npv_slope1/np.amax(npv_slope1)

# print(irr_noslope)
# print(npv_noslope)

grad_num_dia  = np.gradient(num_baseline,dia_values, axis = 1) #/aep_baseline
grad_num_power = np.gradient(num_baseline, power_values, axis = 0) #/aep_baseline

grad_aep_dia = np.gradient(aep_baseline,dia_values, axis = 1) #*-num_baseline/(aep_baseline**2)
grad_aep_power = np.gradient(aep_baseline,power_values, axis = 0) #*-num_baseline/(aep_baseline**2)

grad_lcoe_dia = np.gradient(lcoe_baseline,dia_values, axis = 1)
grad_lcoe_power = np.gradient(lcoe_baseline,power_values, axis = 0)

grad_revenue_dia_60_0 = np.gradient(total_revenue_60_0,dia_values, axis = 1)
grad_revenue_power_60_0 = np.gradient(total_revenue_60_0,power_values, axis = 0)

grad_irr_dia_60_0 = np.gradient(irr_60_0,dia_values, axis = 1)
grad_irr_power_60_0 = np.gradient(irr_60_0,power_values, axis = 0)


grad_npv_dia_60_0 = np.gradient(npv_60_0,dia_values, axis = 1)
grad_npv_power_60_0 = np.gradient(npv_60_0,power_values, axis = 0)

grad_revenue_dia_90_0 = np.gradient(total_revenue_90_0,dia_values, axis = 1)
grad_revenue_power_90_0 = np.gradient(total_revenue_90_0,power_values, axis = 0)


grad_irr_dia_90_0 = np.gradient(irr_90_0,dia_values, axis = 1)
grad_irr_power_90_0 = np.gradient(irr_90_0,power_values, axis = 0)

grad_npv_dia_90_0 = np.gradient(npv_90_0,dia_values, axis = 1)
grad_npv_power_90_0 = np.gradient(npv_90_0,power_values, axis = 0)

grad_revenue_dia_90_3 = np.gradient(total_revenue_90_3,dia_values, axis = 1)
grad_revenue_power_90_3 = np.gradient(total_revenue_90_3,power_values, axis = 0)

grad_irr_dia_90_3 = np.gradient(irr_90_3,dia_values, axis = 1)
grad_irr_power_90_3 = np.gradient(irr_90_3,power_values, axis = 0)

grad_npv_dia_90_3 = np.gradient(npv_90_3,dia_values, axis = 1)
grad_npv_power_90_3 = np.gradient(npv_90_3,power_values, axis = 0)

grad_revenue_dia_110_3 = np.gradient(total_revenue_110_3,dia_values, axis = 1)
grad_revenue_power_110_3 = np.gradient(total_revenue_110_3,power_values, axis = 0)

grad_irr_dia_110_3 = np.gradient(irr_110_3,dia_values, axis = 1)
grad_irr_power_110_3 = np.gradient(irr_110_3,power_values, axis = 0)

grad_npv_dia_110_3 = np.gradient(npv_110_3,dia_values, axis = 1)
grad_npv_power_110_3 = np.gradient(npv_110_3,power_values, axis = 0)

# fig, ax = plt.subplots(nrows =1, ncols= 1, figsize=(5.5,4))
# scale = 0.5
# # ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_lcoe_dia[4,4], grad_lcoe_power[4,4], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='none', ec='C0', linewidth = 1) #, scale = scale)
# ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_irr_dia_noslope[4,4], grad_irr_power_noslope[4,4], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='none', ec='C1', linewidth = 1, scale = scale)
# # ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_irr_dia_slope1[4,4], grad_irr_power_slope1[4,4], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='none', ec='C2', linewidth = 1, scale = scale)
# # # ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_npv_dia_noslope[4,4], grad_npv_power_noslope[4,4], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='none', ec='C3', linewidth = 1, scale = scale)
# # ax.quiver(D_baseline[4,4], P_baseline[4,4],  grad_npv_dia_slope1[4,4], grad_npv_power_slope1[4,4], headlength = 2, color='C4', headaxislength = 2,linestyle = '-',fc='none', ec='C4', linewidth = 1, scale = scale)
#
# ax.set_ylabel('Rated power', fontsize = 16)
# ax.set_xlabel('Rotor diameter', fontsize = 16)
# ax.tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# plt.show()




fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))


########### Non Normalized ############


scale = 0.04
axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_60_0[6,7], grad_irr_power_60_0[6,7], headlength = 2, headaxislength = 2, color='C1', linestyle = '-',fc='C1', ec='C1', linewidth = 1, scale = scale, alpha = 0.6)
axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_90_0[6,7], grad_irr_power_90_0[6,7], headlength = 2,headaxislength = 2, color='C2', linestyle = '-',fc='C2', ec='C2', linewidth = 1, scale = scale, alpha = 0.6)
axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_90_3[6,7], grad_irr_power_90_3[6,7], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='C3', ec='C3', linewidth = 1, scale = scale, alpha = 0.6)
axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_110_3[6,7], grad_irr_power_110_3[6,7], headlength = 2, headaxislength = 2,color='C4', linestyle = '-',fc='C4', ec='C4', linewidth = 1, scale = scale, alpha = 0.6)
axs[0].legend(['c = 60, m = 0', 'c = 90, m = 0', 'c = 90, m = -3', 'c = 110, m = -3'])
#
scale = 3000
axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_60_0[6,7], grad_npv_power_60_0[6,7], headlength = 4, headaxislength = 4, color='C1', linestyle = '-',fc='C1', ec='C1', linewidth = 1, scale = scale, alpha = 1)
axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_90_0[6,7], grad_npv_power_90_0[6,7], headlength = 4, headaxislength = 4, color='C2', linestyle = '-',fc='C2', ec='C2', linewidth = 1, scale = scale, alpha = 0.6)
axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_90_3[6,7], grad_npv_power_90_3[6,7], headlength = 4, headaxislength = 4,color='C3', linestyle = '-',fc='C3', ec='C3', linewidth = 1, scale = scale, alpha = 1)
axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_110_3[6,7], grad_npv_power_110_3[6,7], headlength = 4, headaxislength = 4,color='C4', linestyle = '-',fc='C4', ec='C4', linewidth = 1, scale = scale, alpha =0.6)
axs[1].legend(['c = 60, m = 0', 'c = 90, m = 0', 'c = 90, m = -3', 'c = 110, m = -3'])

########### Normalized ############


# scale = 0.3
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_60_0[6,7], grad_irr_power_60_0[6,7], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='C0', ec='C0', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_90_0[6,7], grad_irr_power_90_0[6,7], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='C1', ec='C1', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_90_3[6,7], grad_irr_power_90_3[6,7], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='C2', ec='C2', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_110_3[6,7], grad_irr_power_110_3[6,7], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='C3', ec='C3', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].legend(['c = 60, m = 0', 'c = 90, m = 0', 'c = 90, m = -3', 'c = 110, m = -3'])
#
# scale = 2.2
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_60_0[6,7], grad_npv_power_60_0[6,7], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='C0', ec='C0', linewidth = 1, scale = scale, alpha = 0.8)
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_90_0[6,7], grad_npv_power_90_0[6,7], headlength = 2, headaxislength = 2, color='C1', linestyle = '-',fc='C1', ec='C1', linewidth = 1, scale = scale, alpha = 0.6)
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_90_3[6,7], grad_npv_power_90_3[6,7], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='C2', ec='C2', linewidth = 1, scale = scale, alpha = 0.4)
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_110_3[6,7], grad_npv_power_110_3[6,7], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='C3', ec='C3', linewidth = 1, scale = scale, alpha = 0.4)
# axs[1].legend(['c = 60, m = 0', 'c = 90, m = 0', 'c = 90, m = -3', 'c = 110, m = -3'])
#


# x_tick_labels = [str(round(i,1)) for i in dia_values]
# y_tick_labels = [str(round(i,1)) for i in power_values]
#
# axs[0].set_xticklabels(x_tick_labels)
# axs[0].set_yticklabels(y_tick_labels)
axs[0].set_ylabel('Rated power', fontsize = 16)
axs[0].set_xlabel('Rotor diameter', fontsize = 16)
axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
axs[0].set_title('IRR', fontsize = 16)

axs[1].set_xlabel('Rotor diameter', fontsize = 16)
axs[1].set_ylabel('Rated power', fontsize = 16)
axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
axs[1].set_title('NPV', fontsize = 16)
# axs[1].text(0.6, 0.25, r'$\'{AEP_{gross}}*(1 - \lambda_{wake})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# axs[1].text(0.5, 0.6, r'$AEP_{gross}*\'{\lambda_{wake}}$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# plt.savefig('IRR_NPV_gradients.png',bbox_inches='tight',dpi=300)
# plt.savefig('normalized_IRR_NPV_gradients.png',bbox_inches='tight',dpi=300)
plt.show()



fig, ax = plt.subplots(nrows =1, ncols= 1, figsize=(5.5,4))





scale = 6000
ax.quiver(D_baseline[6,7], P_baseline[6,7],  grad_num_dia[6,7], grad_num_power[6,7], headlength = 2, headaxislength = 2, color='C0', linestyle = '-',fc='C0', ec='C0', linewidth = 1, scale = scale, alpha = 0.6)
ax.quiver(D_baseline[6,7], P_baseline[6,7],  grad_revenue_dia_60_0[6,7], grad_revenue_power_60_0[6,7], headlength = 2,headaxislength = 2, color='C1', linestyle = '-',fc='C1', ec='C1', linewidth = 1, scale = scale, alpha = 0.6)
ax.quiver(D_baseline[6,7], P_baseline[6,7], grad_revenue_dia_90_0[6,7], grad_revenue_power_90_0[6,7], headlength = 2, headaxislength = 2,color='C2', linestyle = '-',fc='C2', ec='C2', linewidth = 1, scale = scale, alpha = 0.6)
ax.quiver(D_baseline[6,7], P_baseline[6,7],  grad_revenue_dia_90_3[6,7], grad_revenue_power_90_3[6,7], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='C3', ec='C3', linewidth = 1, scale = scale, alpha = 0.6)
ax.quiver(D_baseline[6,7], P_baseline[6,7],  grad_revenue_dia_110_3[6,7], grad_revenue_power_110_3[6,7], headlength = 2, headaxislength = 2,color='C4', linestyle = '-',fc='C4', ec='C4', linewidth = 1, scale = scale, alpha = 0.6)
ax.legend(['Costs','Revenue (c = 60, m = 0)', 'Revenue (c = 90, m = 0)', 'Revenue (c = 90, m = -3)', 'Revenue (c = 110, m = -3)'])

#


# x_tick_labels = [str(round(i,1)) for i in dia_values]
# y_tick_labels = [str(round(i,1)) for i in power_values]
#
# axs[0].set_xticklabels(x_tick_labels)
# axs[0].set_yticklabels(y_tick_labels)
ax.set_ylabel('Rated power', fontsize = 16)
ax.set_xlabel('Rotor diameter', fontsize = 16)
ax.tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[0].set_title('IRR', fontsize = 16)


# axs[1].text(0.6, 0.25, r'$\'{AEP_{gross}}*(1 - \lambda_{wake})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# axs[1].text(0.5, 0.6, r'$AEP_{gross}*\'{\lambda_{wake}}$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# plt.savefig('cost_vs_revenue_gradients.png',bbox_inches='tight',dpi=300)
# plt.savefig('normalized_IRR_NPV_gradients.png',bbox_inches='tight',dpi=300)
plt.show()










#### POLAR PLOTS #######


fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
import math
mag_grad_irr_60_0 = np.sqrt(grad_irr_dia_60_0[6,7]**2 + grad_irr_power_60_0[6,7]**2)
theta_grad_irr_60_0 = (90 + math.degrees(math.atan(abs(grad_irr_dia_60_0[6,7]/grad_irr_power_60_0[6,7]))))*np.pi/180

mag_grad_irr_90_0 = np.sqrt(grad_irr_dia_90_0[6,7]**2 + grad_irr_power_90_0[6,7]**2)
theta_grad_irr_90_0 = (90 + math.degrees(math.atan(abs(grad_irr_dia_90_0[6,7]/grad_irr_power_90_0[6,7]))))*np.pi/180

mag_grad_irr_90_3 = np.sqrt(grad_irr_dia_90_3[6,7]**2 + grad_irr_power_90_3[6,7]**2)
theta_grad_irr_90_3 = (270 + math.degrees(math.atan(abs(grad_irr_dia_90_3[6,7]/grad_irr_power_90_3[6,7]))))*np.pi/180

mag_grad_irr_110_3 = np.sqrt(grad_irr_dia_110_3[6,7]**2 + grad_irr_power_110_3[6,7]**2)
theta_grad_irr_110_3 = (180 + math.degrees(math.atan(abs(grad_irr_power_110_3[6,7]/grad_irr_dia_110_3[6,7]))))*np.pi/180

r_grad_irr_60_0 = mag_grad_irr_60_0/mag_grad_irr_90_0
r_grad_irr_90_0 = mag_grad_irr_90_0/mag_grad_irr_90_0
r_grad_irr_90_3 = mag_grad_irr_90_3/mag_grad_irr_90_0
r_grad_irr_110_3 = mag_grad_irr_110_3/mag_grad_irr_90_0


print(r_grad_irr_60_0, r_grad_irr_90_0, r_grad_irr_90_3, r_grad_irr_110_3)
print(theta_grad_irr_60_0, theta_grad_irr_90_0, theta_grad_irr_90_3, theta_grad_irr_110_3)

# theta = [theta_grad_irr_60_0, theta_grad_irr_90_0, theta_grad_irr_90_3, theta_grad_irr_110_3]
# r = [r_grad_irr_60_0, r_grad_irr_90_0, r_grad_irr_90_3, r_grad_irr_110_3]
plt.polar([0,theta_grad_irr_60_0], [0,r_grad_irr_60_0], marker = 'o')
plt.polar(theta_grad_irr_90_0, r_grad_irr_90_0)
plt.polar(theta_grad_irr_90_3, r_grad_irr_90_3)
plt.polar(theta_grad_irr_110_3, r_grad_irr_110_3)

# ax.plot(theta_grad_irr_60_0, r_grad_irr_60_0, alpha=0.75)
# ax.plot(theta_grad_irr_90_0, r_grad_irr_90_0, alpha=0.75)
# ax.plot(theta_grad_irr_90_3, r_grad_irr_90_3, alpha=0.75)
# ax.plot(theta_grad_irr_110_3, r_grad_irr_110_3, alpha=0.75)
ax.legend(['c = 60, m = 0', 'c = 90, m = 0', 'c = 90, m = -3', 'c = 110, m = -3'])
# ax.set_thetamin(0)
# ax.set_thetamax(180)

plt.show()
#
# scale = 0.04
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_60_0[6,7], grad_irr_power_60_0[6,7], headlength = 2, headaxislength = 2, color='C1', linestyle = '-',fc='C1', ec='C1', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_90_0[6,7], grad_irr_power_90_0[6,7], headlength = 2,headaxislength = 2, color='C2', linestyle = '-',fc='C2', ec='C2', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_90_3[6,7], grad_irr_power_90_3[6,7], headlength = 2, headaxislength = 2,color='C3', linestyle = '-',fc='C3', ec='C3', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].quiver(D_baseline[6,7], P_baseline[6,7],  grad_irr_dia_110_3[6,7], grad_irr_power_110_3[6,7], headlength = 2, headaxislength = 2,color='C4', linestyle = '-',fc='C4', ec='C4', linewidth = 1, scale = scale, alpha = 0.6)
# axs[0].legend(['c = 60, m = 0', 'c = 90, m = 0', 'c = 90, m = -3', 'c = 110, m = -3'])
# #
# scale = 3000
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_60_0[6,7], grad_npv_power_60_0[6,7], headlength = 4, headaxislength = 4, color='C1', linestyle = '-',fc='C1', ec='C1', linewidth = 1, scale = scale, alpha = 1)
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_90_0[6,7], grad_npv_power_90_0[6,7], headlength = 4, headaxislength = 4, color='C2', linestyle = '-',fc='C2', ec='C2', linewidth = 1, scale = scale, alpha = 0.6)
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_90_3[6,7], grad_npv_power_90_3[6,7], headlength = 4, headaxislength = 4,color='C3', linestyle = '-',fc='C3', ec='C3', linewidth = 1, scale = scale, alpha = 1)
# axs[1].quiver(D_baseline[6,7],  P_baseline[6,7], grad_npv_dia_110_3[6,7], grad_npv_power_110_3[6,7], headlength = 4, headaxislength = 4,color='C4', linestyle = '-',fc='C4', ec='C4', linewidth = 1, scale = scale, alpha =0.6)
# axs[1].legend(['c = 60, m = 0', 'c = 90, m = 0', 'c = 90, m = -3', 'c = 110, m = -3'])
#
#
# axs[0].set_ylabel('Rated power', fontsize = 16)
# axs[0].set_xlabel('Rotor diameter', fontsize = 16)
# axs[0].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[0].set_title('IRR', fontsize = 16)
#
# axs[1].set_xlabel('Rotor diameter', fontsize = 16)
# axs[1].set_ylabel('Rated power', fontsize = 16)
# axs[1].tick_params(which='both', bottom=False, top=False, labelbottom=False, left=False, labelleft=False)
# axs[1].set_title('NPV', fontsize = 16)
# # axs[1].text(0.6, 0.25, r'$\'{AEP_{gross}}*(1 - \lambda_{wake})$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# # axs[1].text(0.5, 0.6, r'$AEP_{gross}*\'{\lambda_{wake}}$', horizontalalignment='center',  verticalalignment='center', transform=axs[1].transAxes)
# # plt.savefig('IRR_NPV_gradients.png',bbox_inches='tight',dpi=300)
# # plt.savefig('normalized_IRR_NPV_gradients.png',bbox_inches='tight',dpi=300)
# plt.show()
