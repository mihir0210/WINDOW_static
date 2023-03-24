import numpy as np
import matplotlib.pyplot as plt



# opt_d_cove = np.load("opt_diameter_cove.dat", allow_pickle=True)
# opt_p_cove= np.load("opt_power_cove.dat", allow_pickle=True)
# opt_cove= np.load("opt_cove.dat", allow_pickle=True)
# opt_d_irr= np.load("opt_diameter_irr.dat", allow_pickle=True)
# opt_p_irr= np.load("opt_power_irr.dat", allow_pickle=True)
# opt_irr= np.load("opt_irr.dat", allow_pickle=True)
# opt_d_npv= np.load("opt_diameter_npv.dat", allow_pickle=True)
# opt_p_npv= np.load("opt_power_npv.dat", allow_pickle=True)
# opt_npv= np.load("opt_npv.dat", allow_pickle=True)

# opt_d_cove = np.load("opt_diameter_cove_highprices.dat", allow_pickle=True)
# opt_p_cove= np.load("opt_power_cove_highprices.dat", allow_pickle=True)
# opt_cove= np.load("opt_cove_highprices.dat", allow_pickle=True)
# opt_d_irr= np.load("opt_diameter_irr_highprices.dat", allow_pickle=True)
# opt_p_irr= np.load("opt_power_irr_highprices.dat", allow_pickle=True)
# opt_irr= np.load("opt_irr_highprices.dat", allow_pickle=True)
# opt_d_npv= np.load("opt_diameter_npv_highprices.dat", allow_pickle=True)
# opt_p_npv= np.load("opt_power_npv_highprices.dat", allow_pickle=True)
# opt_npv= np.load("opt_npv_highprices.dat", allow_pickle=True)

opt_d_cove = np.load("opt_diameter_cove_highprices_baseline.dat", allow_pickle=True)
opt_p_cove= np.load("opt_power_cove_highprices_baseline.dat", allow_pickle=True)
opt_cove= np.load("opt_cove_highprices_baseline.dat", allow_pickle=True)
opt_d_irr= np.load("opt_diameter_irr_highprices_baseline.dat", allow_pickle=True)
opt_p_irr= np.load("opt_power_irr_highprices_baseline.dat", allow_pickle=True)
opt_irr= np.load("opt_irr_highprices_baseline.dat", allow_pickle=True)
opt_d_npv= np.load("opt_diameter_npv_highprices_baseline.dat", allow_pickle=True)
opt_p_npv= np.load("opt_power_npv_highprices_baseline.dat", allow_pickle=True)
opt_npv= np.load("opt_npv_highprices_baseline.dat", allow_pickle=True)
opt_d_lpoe = np.load("opt_diameter_lpoe_highprices_baseline.dat", allow_pickle=True)
opt_p_lpoe = np.load("opt_power_lpoe_highprices_baseline.dat", allow_pickle=True)

# opt_d_cove = np.load("opt_diameter_cove_PPA.dat", allow_pickle=True)
# opt_p_cove= np.load("opt_power_cove_PPA.dat", allow_pickle=True)
# opt_cove= np.load("opt_cove_PPA.dat", allow_pickle=True)
# opt_d_irr= np.load("opt_diameter_irr_PPA.dat", allow_pickle=True)
# opt_p_irr= np.load("opt_power_irr_PPA.dat", allow_pickle=True)
# opt_irr= np.load("opt_irr_PPA.dat", allow_pickle=True)
# opt_d_npv= np.load("opt_diameter_npv_PPA.dat", allow_pickle=True)
# opt_p_npv= np.load("opt_power_npv_PPA.dat", allow_pickle=True)
# opt_npv= np.load("opt_npv_PPA.dat", allow_pickle=True)


# opt_d_cove = np.load("opt_diameter_cove_scurve_baseline.dat", allow_pickle=True)
# opt_p_cove= np.load("opt_power_cove_scurve_baseline.dat", allow_pickle=True)
# opt_cove= np.load("opt_cove_scurve_baseline.dat", allow_pickle=True)
# opt_d_irr= np.load("opt_diameter_irr_scurve_baseline.dat", allow_pickle=True)
# opt_p_irr= np.load("opt_power_irr_scurve_baseline.dat", allow_pickle=True)
# opt_irr= np.load("opt_irr_scurve_baseline.dat", allow_pickle=True)
# opt_d_npv= np.load("opt_diameter_npv_scurve_baseline.dat", allow_pickle=True)
# opt_p_npv= np.load("opt_power_npv_scurve_baseline.dat", allow_pickle=True)
# opt_npv= np.load("opt_npv_scurve_baseline.dat", allow_pickle=True)
lcoe_matrix = np.load("lcoe_matrix_baseline_fine.dat", allow_pickle=True)
D = np.load("diameter_matrix_fine.dat", allow_pickle=True)
P = np.load("power_matrix_fine.dat", allow_pickle=True)

# opt_d_cove = np.load("opt_diameter_cove_flatprices.dat", allow_pickle=True)
# opt_p_cove= np.load("opt_power_cove_flatprices.dat", allow_pickle=True)
# opt_cove= np.load("opt_cove_flatprices.dat", allow_pickle=True)
# opt_d_irr= np.load("opt_diameter_irr_flatprices.dat", allow_pickle=True)
# opt_p_irr= np.load("opt_power_irr_flatprices.dat", allow_pickle=True)
# opt_irr= np.load("opt_irr_flatprices.dat", allow_pickle=True)
# opt_d_npv= np.load("opt_diameter_npv_flatprices.dat", allow_pickle=True)
# opt_p_npv= np.load("opt_power_npv_flatprices.dat", allow_pickle=True)
# opt_npv= np.load("opt_npv_flatprices.dat", allow_pickle=True)

# opt_d_cove = np.load("opt_diameter_cove_fixedintercept.dat", allow_pickle=True)
# opt_p_cove= np.load("opt_power_cove_fixedintercept.dat", allow_pickle=True)
# opt_cove= np.load("opt_cove_fixedintercept.dat", allow_pickle=True)
# opt_d_irr= np.load("opt_diameter_irr_fixedintercept.dat", allow_pickle=True)
# opt_p_irr= np.load("opt_power_irr_fixedintercept.dat", allow_pickle=True)
# opt_irr= np.load("opt_irr_fixedintercept.dat", allow_pickle=True)
# opt_d_npv= np.load("opt_diameter_npv_fixedintercept.dat", allow_pickle=True)
# opt_p_npv= np.load("opt_power_npv_fixedintercept.dat", allow_pickle=True)
# opt_npv= np.load("opt_npv_fixedintercept.dat", allow_pickle=True)

# opt_d_cove = np.load("opt_diameter_cove_reducedoandm.dat", allow_pickle=True)
# opt_p_cove= np.load("opt_power_cove_reducedoandm.dat", allow_pickle=True)
# opt_cove= np.load("opt_cove_reducedoandm.dat", allow_pickle=True)
# opt_d_irr= np.load("opt_diameter_irr_reducedoandm.dat", allow_pickle=True)
# opt_p_irr= np.load("opt_power_irr_reducedoandm.dat", allow_pickle=True)
# opt_irr= np.load("opt_irr_reducedoandm.dat", allow_pickle=True)
# opt_d_npv= np.load("opt_diameter_npv_reducedoandm.dat", allow_pickle=True)
# opt_p_npv= np.load("opt_power_npv_reducedoandm.dat", allow_pickle=True)
# opt_npv= np.load("opt_npv_reducedoandm.dat", allow_pickle=True)


fig,ax = plt.subplots(nrows =1, ncols= 1, figsize=(5.3,4.5))
# opt_d_lcoe = 229.8
# opt_p_lcoe = 13.8

# opt_d_lcoe = 225
# opt_p_lcoe = 13.3

opt_d_lcoe = 222.3
opt_p_lcoe = 15

import seaborn as sns
from matplotlib.colors import ListedColormap
# my_cmap = sns.color_palette("rocket", as_cmap=True)
# my_cmap = sns.color_palette("BuGn_r", as_cmap=True)
my_cmap = sns.color_palette("mako", as_cmap=True)
# c = plt.contourf(d_rotor,p_rated,property, 50, cmap='YlOrRd')
# c = plt.contourf(d_rotor,p_rated,property, 100, cmap = my_cmap.reversed())
# c = plt.contourf(d_rotor,p_rated,property, round(n_colorbars), cmap = my_cmap.reversed())
# c = plt.contourf(d_eval,p_eval,z_pred_irr*100, round(n_colorbars)-1, cmap = my_cmap.reversed())
c = plt.contourf(D,P,lcoe_matrix, 27, cmap = my_cmap.reversed(), alpha=0.6)
cbar = fig.colorbar(c)
#
# #plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
plt.scatter(opt_d_lcoe, opt_p_lcoe, marker = 'o', c='k', s = 80, alpha = 0.5, label='LCoE')
# plt.scatter(opt_d_cove, opt_p_cove, marker = 'o', c='C0', s = 30, alpha = 0.5, label='CoVE')
plt.scatter(opt_d_irr, opt_p_irr, marker = 'o', c='C0', s = 30, alpha = 0.5, label='IRR')
plt.scatter(opt_d_npv, opt_p_npv, marker = 'o', c='C1', s = 30, alpha = 0.5, label='NPV')
plt.scatter(opt_d_lpoe, opt_p_lpoe, marker = 'o', c='C3', s = 30, alpha = 0.5, label='LPoE')
# plt.text(222, 15.7, 'Global optimum (Baseline)', horizontalalignment='center', verticalalignment='center', size = '10')
# plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')

fs = 16

plt.xlabel('Rotor Diameter (m)', fontsize = fs)
plt.ylabel('Rated Power (MW)', fontsize = fs)
# #plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
cbar.ax.set_ylabel('LCoE (Euros/MWh)', fontsize = fs)
plt.xlim(210, 255)
plt.ylim(12,15.5)
plt.grid(axis = 'both', alpha = 0.1)
ax.tick_params(axis='both',direction='in', length =5)
plt.legend(loc = 'upper right', fontsize = fs)
# plt.savefig('optimum_comparison_diff_scenarios_highprices.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_flatprices.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_fixedintercept.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_reducedoandm.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_highprices_baseline.png',bbox_inches='tight',dpi=1200)
# plt.savefig('optimum_comparison_diff_scenarios_scurve_baseline.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_PPA.png',bbox_inches='tight',dpi=300)
plt.show()




fig,ax = plt.subplots(nrows =1, ncols= 1, figsize=(5.3,4.5))
# opt_d_lcoe = 229.8
# opt_p_lcoe = 13.8

# opt_d_lcoe = 225
# opt_p_lcoe = 13.3

opt_d_lcoe = 222.3
opt_p_lcoe = 15
#
# #plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
plt.scatter(opt_npv, opt_irr, marker = 'o', c='k', s = 80, alpha = 0.5)
# plt.scatter(opt_d_cove, opt_p_cove, marker = 'o', c='C0', s = 30, alpha = 0.5, label='CoVE')
# plt.scatter(opt_d_irr, opt_p_irr, marker = 'o', c='C1', s = 30, alpha = 0.5, label='IRR')
# plt.scatter(opt_d_npv, opt_p_npv, marker = 'o', c='C2', s = 30, alpha = 0.5, label='NPV')
# plt.text(222, 15.7, 'Global optimum (Baseline)', horizontalalignment='center', verticalalignment='center', size = '10')
# plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')

fs = 16

plt.xlabel('Optimum NPV (M Euros)', fontsize = fs)
plt.ylabel('Optimum IRR (%)', fontsize = fs)
# #plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
# cbar.ax.set_ylabel(y_label, fontsize = fs)
#
plt.grid(axis = 'both', alpha = 0.1)
ax.tick_params(axis='both',direction='in', length =5)
# plt.legend(fontsize = fs)
# plt.savefig('optimum_comparison_diff_scenarios_highprices.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_flatprices.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_fixedintercept.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_reducedoandm.png',bbox_inches='tight',dpi=300)
# plt.savefig('optimum_comparison_diff_scenarios_highprices_baseline.png',bbox_inches='tight',dpi=300)
plt.show()






