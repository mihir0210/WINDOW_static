

import numpy as np

import matplotlib.pyplot as plt


P_600 = np.load("power_matrix_600MW.dat", allow_pickle=True)
D_600 = np.load("diameter_matrix_600MW.dat", allow_pickle=True)
lcoe_600 = np.load("lcoe_matrix_600MW.dat", allow_pickle=True)

P_1000 = np.load("power_matrix_1000MW.dat", allow_pickle=True)
D_1000  = np.load("diameter_matrix_1000MW.dat", allow_pickle=True)
lcoe_1000  = np.load("lcoe_matrix_1000MW.dat", allow_pickle=True)

P_1400 = np.load("power_matrix_1400MW.dat", allow_pickle=True)
D_1400 = np.load("diameter_matrix_1400MW.dat", allow_pickle=True)
lcoe_1400 = np.load("lcoe_matrix_1400MW.dat", allow_pickle=True)

fs = 16
lw = 1.5
la = 0.3
#fig,ax = plt.subplots()

import seaborn as sns
from matplotlib.colors import ListedColormap
my_cmap = sns.color_palette("rocket", as_cmap=True)
#my_cmap = sns.color_palette("mako", as_cmap=True)
# c = plt.contourf(D,P,lcoe_matrix_150, 100, cmap='YlOrRd')
# plt.show()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
#fig.suptitle('Horizontally stacked subplots')
fig.set_figheight(4)
fig.set_figwidth(15)

ax1.contourf(D_600,P_600,lcoe_600,50, cmap=my_cmap.reversed())
ax1.plot(226.3, 12.4 , 'ko')
ax1.plot(221.3, 12.5, 'ro')
ax1.set_title("Farm power: 600 MW", fontsize = fs)
ax1.set_xlabel("Rotor diameter (m)", fontsize = fs)
ax1.set_ylabel('Rated power (MW)', fontsize = fs)
ax1.tick_params(axis='both',direction='in', length =5)
ax1.text(226.5, 11.5, 'New optimum', horizontalalignment='center', verticalalignment='center', size = '13')


ax2.contourf(D_1000,P_1000,lcoe_1000,50, cmap=my_cmap.reversed())
ax2.plot(225.3, 14.1, 'ko')
ax2.plot(222.3, 15, 'ro')
ax2.set_title("Farm power: 1000 MW", fontsize = fs)
ax2.set_xlabel("Rotor diameter (m)", fontsize = fs)
ax2.tick_params(axis='both',direction='in', length =5)
ax2.text(225.3, 13, 'New optimum', horizontalalignment='center', verticalalignment='center', size = '13')


ax3.contourf(D_1400,P_1400,lcoe_1400,50, cmap=my_cmap.reversed())
ax3.plot(224.3, 14.9, 'ko')
ax3.plot(224.8,17.1, 'ro')
ax3.set_title("Farm power: 1400 MW", fontsize = fs)
ax3.set_xlabel("Rotor diameter (m)", fontsize = fs)
ax3.tick_params(axis='both',direction='in', length =5)
ax3.text(224.3, 14, 'New optimum', horizontalalignment='center', verticalalignment='center', size = '13')




plt.grid(axis = 'both', alpha = 0.1)

# plt.savefig('fixed_poweronly_comparison.png',bbox_inches='tight',dpi=300)
# plt.show()


##### Analyze farm power ####

sp_data_1000MW = []
z_aep_1000MW = []
cost_ratio_1000MW = []
wake_1000MW = []
lcoe_1000MW = []
num_1000MW = []

with open("aep_1000MW_7D.txt", "r") as f:
  for line in f:
    z_aep_1000MW.append(float(line.strip()))

with open("sp_1000MW_7D.txt", "r") as f:
  for line in f:
    sp_data_1000MW.append(float(line.strip()))

with open("cost_ratio_1000MW_7D.txt", "r") as f:
  for line in f:
    cost_ratio_1000MW.append(float(line.strip()))

with open("wake_1000MW_7D.txt", "r") as f:
  for line in f:
    wake_1000MW.append(float(line.strip()))

with open("lcoe_1000MW_7D.txt", "r") as f:
  for line in f:
    lcoe_1000MW.append(float(line.strip()))

with open("num_1000MW_7D.txt", "r") as f:
  for line in f:
    num_1000MW.append(float(line.strip()))
# cond = [i for i in range(len(sp_data_1000MW)) if sp_data_1000MW[i] > 200 and sp_data_1000MW[i] < 600] #remove specific power values below 200 and above 600
# sp_data_1000MW = [sp_data_1000MW[idx] for idx in cond]
# z_aep_1000MW= [z_aep_1000MW[idx] for idx in cond]
# cost_ratio_1000MW = [cost_ratio_1000MW[idx] for idx in cond]
# wake_1000MW = [wake_1000MW[idx] for idx in cond]


sp_data_600MW = []
z_aep_600MW = []
cost_ratio_600MW = []
wake_600MW = []
lcoe_600MW = []
num_600MW = []

with open("aep_600MW_7D.txt", "r") as f:
  for line in f:
    z_aep_600MW.append(float(line.strip()))

with open("sp_600MW_7D.txt", "r") as f:
  for line in f:
    sp_data_600MW.append(float(line.strip()))

with open("cost_ratio_600MW_7D.txt", "r") as f:
  for line in f:
    cost_ratio_600MW.append(float(line.strip()))

with open("wake_600MW_7D.txt", "r") as f:
  for line in f:
    wake_600MW.append(float(line.strip()))

with open("lcoe_600MW_7D.txt", "r") as f:
  for line in f:
    lcoe_600MW.append(float(line.strip()))

with open("num_600MW_7D.txt", "r") as f:
  for line in f:
    num_600MW.append(float(line.strip()))

# cond = [i for i in range(len(sp_data_600MW)) if sp_data_600MW[i] > 200 and sp_data_600MW[i] < 600] #remove specific power values below 200 and above 600
# sp_data_600MW = [sp_data_600MW[idx] for idx in cond]
# z_aep_600MW = [z_aep_600MW[idx] for idx in cond]
# cost_ratio_600MW= [cost_ratio_600MW[idx] for idx in cond]
# wake_600MW = [wake_600MW[idx] for idx in cond]




sp_data_1400MW = []
z_aep_1400MW = []
cost_ratio_1400MW = []
wake_1400MW = []
lcoe_1400MW = []
num_1400MW = []

with open("aep_1400MW_7D.txt", "r") as f:
  for line in f:
    z_aep_1400MW.append(float(line.strip()))

with open("sp_1400MW_7D.txt", "r") as f:
  for line in f:
    sp_data_1400MW.append(float(line.strip()))

with open("cost_ratio_1400MW_7D.txt", "r") as f:
  for line in f:
    cost_ratio_1400MW.append(float(line.strip()))

with open("wake_1400MW_7D.txt", "r") as f:
  for line in f:
    wake_1400MW.append(float(line.strip()))

with open("lcoe_1400MW_7D.txt", "r") as f:
  for line in f:
    lcoe_1400MW.append(float(line.strip()))

with open("num_1400MW_7D.txt", "r") as f:
  for line in f:
    num_1400MW.append(float(line.strip()))



# cond = [i for i in range(len(sp_data_1400MW)) if sp_data_1400MW[i] > 200 and sp_data_1400MW[i] < 600] #remove specific power values below 200 and above 600
# sp_data_1400MW = [sp_data_1400MW[idx] for idx in cond]
# z_aep_1400MW= [z_aep_1400MW[idx] for idx in cond]
# cost_ratio_1400MW = [cost_ratio_1400MW[idx] for idx in cond]
# wake_1400MW= [wake_1400MW[idx] for idx in cond]



fs= 16
s = 20
# plt.scatter(sp_data_600MW, norm_cost_ratio_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW, norm_cost_ratio_1000MW, s = s,marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW, norm_cost_ratio_1400MW, s = s,marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized cost ratio', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power constrained (No area constraints)')
#
# plt.legend()
# plt.show()
#
# plt.scatter(sp_data_600MW, cost_ratio_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW, cost_ratio_1000MW, s = s,marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW, cost_ratio_1400MW, s = s,marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Cost ratio', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
#
# plt.legend()
# plt.show()
#
# plt.scatter(sp_data_600MW, norm_aep_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW, norm_aep_1000MW,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW, norm_aep_1400MW,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized AEP', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()
#
# plt.scatter(sp_data_600MW, z_aep_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW, z_aep_1000MW,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW, z_aep_1400MW,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('AEP (GWh)', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()
#
# plt.scatter(sp_data_600MW, norm_wake_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW, norm_wake_1000MW,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW, norm_wake_1400MW,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized wake losses', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()
#
# plt.scatter(sp_data_600MW, wake_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW, wake_1000MW,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW, wake_1400MW,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Wake losses', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()
#
# w600 = np.array(wake_600MW)
# w1000 = np.array(wake_1000MW)
# w1400 = np.array(wake_1400MW)
# grad_wake_sp_600 = np.gradient(w600, sp_data_600MW)
# grad_wake_sp_1000 = np.gradient(w1000, sp_data_1000MW)
# grad_wake_sp_1400 = np.gradient(w1400, sp_data_1400MW)
#
#
# plt.scatter(sp_data_600MW, grad_wake_sp_600,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW,grad_wake_sp_1000,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW,grad_wake_sp_1400,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Gradient of Wake losses', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()
#
#
# cost_ratio_600MW = [c/max(cost_ratio_600MW) for c in cost_ratio_600MW]
# cost_ratio_1000MW = [c/max(cost_ratio_1000MW) for c in cost_ratio_1000MW]
# cost_ratio_1400MW = [c/max(cost_ratio_1400MW) for c in cost_ratio_1400MW]
# #
# cr600 = np.array(cost_ratio_600MW)
# cr1000 = np.array(cost_ratio_1000MW)
# cr1400 = np.array(cost_ratio_1400MW)
# grad_cr_sp_600 = np.gradient(cr600, sp_data_600MW)
# grad_cr_sp_1000 = np.gradient(cr1000, sp_data_1000MW)
# grad_cr_sp_1400 = np.gradient(cr1400, sp_data_1400MW)
#
# # grad_cr_sp_600 = [grad/max(grad_cr_sp_600) for grad in grad_cr_sp_600]
# # grad_cr_sp_1000 = [grad/max(grad_cr_sp_1000) for grad in grad_cr_sp_1000]
# # grad_cr_sp_1400 = [grad/max(grad_cr_sp_1400) for grad in grad_cr_sp_1400]
#
# plt.scatter(sp_data_600MW, cost_ratio_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW,cost_ratio_1000MW,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW,cost_ratio_1400MW ,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized Cost ratio', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()


cost_ratio_600MW = [c/max(cost_ratio_600MW) for c in cost_ratio_600MW]
cost_ratio_1000MW = [c/max(cost_ratio_1000MW) for c in cost_ratio_1000MW]
cost_ratio_1400MW = [c/max(cost_ratio_1400MW) for c in cost_ratio_1400MW]

num_600MW = [a/max(num_600MW) for a in num_600MW]
num_1000MW = [a/max(num_1000MW) for a in num_1000MW]
num_1400MW = [a/max(num_1400MW) for a in num_1400MW]

z_aep_600MW = [a/max(z_aep_600MW) for a in z_aep_600MW]
z_aep_1000MW = [a/max(z_aep_1000MW) for a in z_aep_1000MW]
z_aep_1400MW = [a/max(z_aep_1400MW) for a in z_aep_1400MW]

# wake_600MW = [a/max(wake_600MW) for a in wake_600MW]
# wake_1000MW = [a/max(wake_1000MW) for a in wake_1000MW]
# wake_1400MW = [a/max(wake_1400MW) for a in wake_1400MW]
#
# aep600 = np.array(z_aep_600MW)
# aep1000 = np.array(z_aep_1000MW)
# aep1400 = np.array(z_aep_1400MW)
# grad_aep_sp_600 = np.gradient(aep600, sp_data_600MW)
# grad_aep_sp_1000 = np.gradient(aep1000, sp_data_1000MW)
# grad_aep_sp_1400 = np.gradient(aep1400, sp_data_1400MW)

wake_loss_factor_600MW = [1-w for w in wake_600MW]
wake_loss_factor_1000MW = [1-w for w in wake_1000MW]
wake_loss_factor_1400MW = [1-w for w in wake_1400MW]

wake_loss_factor_600MW = [a/max(wake_loss_factor_600MW) for a in wake_loss_factor_600MW]
wake_loss_factor_1000MW = [a/max(wake_loss_factor_1000MW) for a in wake_loss_factor_1000MW]
wake_loss_factor_1400MW = [a/max(wake_loss_factor_1400MW) for a in wake_loss_factor_1400MW]

fig, axs = plt.subplots(nrows =1, ncols= 3, figsize=(16,4))
# axs[0].scatter(sp_data_600MW, cost_ratio_600MW, s = s, marker = 'o', label = '600 MW')
# axs[0].scatter(sp_data_1000MW, cost_ratio_1000MW, s = s, marker = '^', label = '1000 MW')
# axs[0].scatter(sp_data_1400MW, cost_ratio_1400MW, s = s, marker = 'v', label = '1400 MW')
# axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[0].set_ylabel('Normalized Cost Ratio', fontsize = fs)
# axs[0].legend()

axs[0].scatter(sp_data_600MW, num_600MW, s = s, marker = 'o', label = '600 MW')
axs[0].scatter(sp_data_1000MW, num_1000MW, s = s, marker = '^', label = '1000 MW')
axs[0].scatter(sp_data_1400MW, num_1400MW, s = s, marker = 'v', label = '1400 MW')
axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[0].set_ylabel('Normalized Costs', fontsize = fs)
axs[0].legend()

axs[1].scatter(sp_data_600MW, z_aep_600MW, s = s, marker = 'o', label = '600 MW')
axs[1].scatter(sp_data_1000MW, z_aep_1000MW, s = s, marker = '^', label = '1000 MW')
axs[1].scatter(sp_data_1400MW, z_aep_1400MW, s = s, marker = 'v', label = '1400 MW')
axs[1].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[1].set_ylabel('Normalized AEP', fontsize = fs)
axs[1].legend()

axs[2].scatter(sp_data_600MW, wake_loss_factor_600MW, s = s, marker = 'o', label = '600 MW')
axs[2].scatter(sp_data_1000MW, wake_loss_factor_1000MW, s = s, marker = '^', label = '1000 MW')
axs[2].scatter(sp_data_1400MW, wake_loss_factor_1400MW, s = s, marker = 'v', label = '1400 MW')
axs[2].set_ylabel('Normalized wake factor', fontsize = fs)
axs[2].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[2].legend()

# plt.savefig("plots/fixed_farmpower_sensitivity.png",bbox_inches='tight',dpi=100)
# plt.show()








##### Analyze differences in problem formulation ####

sp_data_baseline = []
z_aep_baseline = []
cost_ratio_baseline = []
wake_baseline = []
num_baseline = []

with open("aep_baseline.txt", "r") as f:
  for line in f:
    z_aep_baseline.append(float(line.strip()))


with open("sp_baseline.txt", "r") as f:
  for line in f:
    sp_data_baseline.append(float(line.strip()))

with open("cost_ratio_baseline.txt", "r") as f:
  for line in f:
    cost_ratio_baseline.append(float(line.strip()))

with open("wake_baseline.txt", "r") as f:
  for line in f:
    wake_baseline.append(float(line.strip()))

with open("num_baseline.txt", "r") as f:
  for line in f:
    num_baseline.append(float(line.strip()))

# cond = [i for i in range(len(sp_data_baseline)) if sp_data_baseline[i] > 200 and sp_data_baseline[i] < 600] #remove specific power values below 200 and above 600
# sp_data_baseline= [sp_data_baseline[idx] for idx in cond]
# z_aep_area100= [z_aep_area100[idx] for idx in cond]
# cost_ratio_area100 = [cost_ratio_area100[idx] for idx in cond]
# wake_area100 = [wake_area100[idx] for idx in cond]

sp_data_1000MW_7D = []
z_aep_1000MW_7D = []
cost_ratio_1000MW_7D  = []
wake_1000MW_7D  = []
num_1000MW_7D = []

with open("aep_1000MW_7D.txt", "r") as f:
  for line in f:
    z_aep_1000MW_7D.append(float(line.strip()))


with open("sp_1000MW_7D.txt", "r") as f:
  for line in f:
    sp_data_1000MW_7D.append(float(line.strip()))


with open("cost_ratio_1000MW_7D.txt", "r") as f:
  for line in f:
    cost_ratio_1000MW_7D.append(float(line.strip()))

with open("wake_1000MW_7D.txt", "r") as f:
  for line in f:
    wake_1000MW_7D.append(float(line.strip()))

with open("num_1000MW_7D.txt", "r") as f:
  for line in f:
    num_1000MW_7D.append(float(line.strip()))

# z_aep_area200= [z_aep_area200[idx] for idx in cond]
# cost_ratio_area200 = [cost_ratio_area200[idx] for idx in cond]
# wake_area200 = [wake_area200[idx] for idx in cond]


# cost_ratio_area100= [(a-min(cost_ratio_area100))/(max(cost_ratio_area100) - min(cost_ratio_area100)) for a in cost_ratio_area100]
# cost_ratio_area200 = [(a-min(cost_ratio_area200))/(max(cost_ratio_area200) - min(cost_ratio_area200)) for a in cost_ratio_area200]

cost_ratio_baseline= [a/max(cost_ratio_baseline) for a in cost_ratio_baseline]
cost_ratio_1000MW_7D= [a/max(cost_ratio_1000MW_7D) for a in cost_ratio_1000MW_7D]

num_baseline = [a/max(num_baseline) for a in num_baseline]
num_1000MW_7D= [a/max(num_1000MW_7D) for a in num_1000MW_7D]

# z_aep_area100= [(a-min(z_aep_area100))/(max(z_aep_area100) - min(z_aep_area100)) for a in z_aep_area100]
# z_aep_area200 = [(a-min(z_aep_area200))/(max(z_aep_area200) - min(z_aep_area200)) for a in z_aep_area200]

z_aep_baseline= [a/max(z_aep_baseline) for a in z_aep_baseline]
z_aep_1000MW_7D = [a/max(z_aep_1000MW_7D) for a in z_aep_1000MW_7D]



wake_loss_factor_baseline = [1-w for w in wake_baseline]
wake_loss_factor_1000MW_7D = [1-w for w in wake_1000MW_7D]


wake_loss_factor_baseline = [a/max(wake_loss_factor_baseline) for a in wake_loss_factor_baseline]
wake_loss_factor_1000MW_7D = [a/max(wake_loss_factor_1000MW_7D) for a in wake_loss_factor_1000MW_7D]

# plt.scatter(sp_data_baseline, cost_ratio_area100,s = s, marker = '^', label = 'Area: 100 km2')
# plt.scatter(sp_data_baseline,cost_ratio_area200,s = s, marker = 'o', label = 'Area: 200 km2')
#
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized Cost ratio', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()


# plt.scatter(sp_data_baseline, z_aep_area100,s = s, marker = '^', label = 'Area: 100 km2')
# plt.scatter(sp_data_baseline,z_aep_area200,s = s, marker = 'o', label = 'Area: 200 km2')
#
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized AEP', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()


# plt.scatter(sp_data_baseline, wake_area100,s = s, marker = '^', label = 'Area: 100 km2')
# plt.scatter(sp_data_baseline,wake_area200,s = s, marker = 'o', label = 'Area: 200 km2')
#
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Wake losses', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()



fig, axs = plt.subplots(nrows =1, ncols= 3, figsize=(16,4))


# axs[0].scatter(sp_data_baseline, cost_ratio_baseline,s = s, marker = '^', label = 'Area constrained')
# axs[0].scatter(sp_data_1000MW_7D,cost_ratio_1000MW_7D,s = s, marker = 'o', label = 'No area constraints')
# axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[0].set_ylabel('Normalized cost ratio', fontsize = fs)
# axs[0].legend()

axs[0].scatter(sp_data_baseline, num_baseline,s = s, marker = '^', label = 'Baseline')
axs[0].scatter(sp_data_1000MW_7D,num_1000MW_7D,s = s, marker = 'o', label = 'Fixed power only')
axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[0].set_ylabel('Normalized costs', fontsize = fs)
axs[0].legend()

axs[1].scatter(sp_data_baseline, z_aep_baseline,s = s, marker = '^', label = 'Baseline')
axs[1].scatter(sp_data_1000MW_7D,z_aep_1000MW_7D,s = s, marker = 'o', label = 'Fixed power only')
axs[1].set_ylabel('Normalized AEP', fontsize = fs)
axs[1].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[1].legend()

axs[2].scatter(sp_data_baseline, wake_loss_factor_baseline,s = s, marker = '^', label = 'Baseline')
axs[2].scatter(sp_data_1000MW_7D,wake_loss_factor_1000MW_7D,s = s, marker = 'o', label = 'Fixed power only')
axs[2].set_ylabel('Normalized wake factor', fontsize = fs)
axs[2].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[2].legend()


# plt.savefig("plots/fixedpower_problem_sensitivity.png",bbox_inches='tight',dpi=100)
# plt.show()



######## LCoE ########


lcoe_baseline = []
lcoe_1000MW_7D = []


with open("lcoe_baseline.txt", "r") as f:
  for line in f:
    lcoe_baseline.append(float(line.strip()))


with open("lcoe_1000MW_7D.txt", "r") as f:
  for line in f:
    lcoe_1000MW_7D.append(float(line.strip()))




plt.scatter(sp_data_baseline, lcoe_baseline,s = s, marker = '^', label = 'Area constrained')
plt.scatter(sp_data_1000MW_7D,lcoe_1000MW_7D,s = s, marker = 'o', label = 'No area constraints')
plt.xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
plt.ylabel('LCoE (Euros/MWh)', fontsize = fs)
plt.legend()
# plt.savefig("plots/lcoe_fixedpower_problem_sensitivity.png",bbox_inches='tight',dpi=100)
# plt.show()


plt.scatter(sp_data_600MW, lcoe_600MW, s = s, marker = 'o', label = '600 MW')
plt.scatter(sp_data_1000MW, lcoe_1000MW, s = s, marker = '^', label = '1000 MW')
plt.scatter(sp_data_1400MW, lcoe_1400MW, s = s, marker = 'v', label = '1400 MW')
plt.xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
plt.ylabel('LCoE (Euros/MWh)', fontsize = fs)
plt.legend()
# plt.savefig("plots/lcoe_fixedpower_comparison_diffpowers.png",bbox_inches='tight',dpi=300)
# plt.show()


######################### Gradients ####################
# power_values = np.array([10.0, 10.99, 12.05, 12.99, 13.51, 14.08, 14.49, 14.93, 15.62, 16.13, 16.67, 17.24, 18.18, 19.23, 20.0, 22.73])
# rad_values = [90.0, 95.0, 100.0, 105.0, 215/2, 110.0, 222/2, 225/2, 227/2, 115.0, 120.0, 125.0, 130.0, 135.0, 140.0, 145.0, 150.0]
# dia_values = np.array([r*2 for r in rad_values])
#
# P_1000 = np.load("power_matrix_1000MW_course.dat", allow_pickle=True)
# D_1000  = np.load("diameter_matrix_1000MW_course.dat", allow_pickle=True)
# lcoe_1000  = np.load("lcoe_matrix_1000MW_course.dat", allow_pickle=True)
# num_1000 = np.load("numerator_matrix_1000MW_course.dat", allow_pickle=True)
# aep_1000 = np.load("aep_matrix_1000MW_course.dat", allow_pickle=True)
#
#
# grads_num = np.gradient(num_1000, dia_values, power_values)
# xgrad_num = grads_num[0]
# ygrad_num = grads_num[1]
#
# grads_aep = np.gradient(aep_1000, dia_values, power_values)
# xgrad_aep = grads_aep[0]
# ygrad_aep = grads_aep[1]
#
# #mag = np.sqrt(xgrad_num**2 + ygrad_num**2)
#
#
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
#
# axs[0].quiver(D_1000, P_1000, xgrad_num, ygrad_num)
#
# axs[1].quiver(D_1000, P_1000, xgrad_aep, ygrad_aep)
#
# plt.show()






