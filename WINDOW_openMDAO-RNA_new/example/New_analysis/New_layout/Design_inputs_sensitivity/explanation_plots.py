
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

##### Analyze farm power ####

sp_data_1000MW = [] # Has more points than baseline
z_aep_1000MW = []
cost_ratio_1000MW = []
wake_1000MW = []
lcoe_1000MW = []
num_1000MW = []

with open("aep_1000MW.txt", "r") as f:
  for line in f:
    z_aep_1000MW.append(float(line.strip()))

with open("sp_1000MW.txt", "r") as f:
  for line in f:
    sp_data_1000MW.append(float(line.strip()))

with open("cost_ratio_1000MW.txt", "r") as f:
  for line in f:
    cost_ratio_1000MW.append(float(line.strip()))

with open("wake_1000MW.txt", "r") as f:
  for line in f:
    wake_1000MW.append(float(line.strip()))

with open("lcoe_1000MW.txt", "r") as f:
  for line in f:
    lcoe_1000MW.append(float(line.strip()))

with open("num_1000MW.txt", "r") as f:
  for line in f:
    num_1000MW.append(float(line.strip()))


# cond = [i for i in range(len(sp_data_1000MW)) if sp_data_1000MW[i] > 200 and sp_data_1000MW[i] < 600] #remove specific power values below 200 and above 600
# sp_data_1000MW = [sp_data_1000MW[idx] for idx in cond]
# z_aep_1000MW= [z_aep_1000MW[idx] for idx in cond]
# cost_ratio_1000MW = [cost_ratio_1000MW[idx] for idx in cond]
# wake_1000MW = [wake_1000MW[idx] for idx in cond]

norm_aep_1000MW = [aep/max(z_aep_1000MW) for aep in z_aep_1000MW]
norm_cost_ratio_1000MW = [cr/max(cost_ratio_1000MW) for cr in cost_ratio_1000MW]
norm_wake_1000MW = [w/max(wake_1000MW) for w in wake_1000MW]

sp_data_600MW = []
z_aep_600MW = []
cost_ratio_600MW = []
wake_600MW = []
lcoe_600MW = []
num_600MW = []

with open("aep_600MW.txt", "r") as f:
  for line in f:
    z_aep_600MW.append(float(line.strip()))

with open("sp_600MW.txt", "r") as f:
  for line in f:
    sp_data_600MW.append(float(line.strip()))

with open("cost_ratio_600MW.txt", "r") as f:
  for line in f:
    cost_ratio_600MW.append(float(line.strip()))

with open("wake_600MW.txt", "r") as f:
  for line in f:
    wake_600MW.append(float(line.strip()))

with open("lcoe_600MW.txt", "r") as f:
  for line in f:
    lcoe_600MW.append(float(line.strip()))

with open("num_600MW.txt", "r") as f:
  for line in f:
    num_600MW.append(float(line.strip()))

# cond = [i for i in range(len(sp_data_600MW)) if sp_data_600MW[i] > 200 and sp_data_600MW[i] < 600] #remove specific power values below 200 and above 600
# sp_data_600MW = [sp_data_600MW[idx] for idx in cond]
# z_aep_600MW = [z_aep_600MW[idx] for idx in cond]
# cost_ratio_600MW= [cost_ratio_600MW[idx] for idx in cond]
# wake_600MW = [wake_600MW[idx] for idx in cond]

norm_aep_600MW = [aep/max(z_aep_600MW ) for aep in z_aep_600MW ]
norm_cost_ratio_600MW = [cr/max(cost_ratio_600MW ) for cr in cost_ratio_600MW ]
norm_wake_600MW  = [w/max(wake_600MW ) for w in wake_600MW ]


sp_data_1400MW = []
z_aep_1400MW = []
cost_ratio_1400MW = []
wake_1400MW = []
lcoe_1400MW = []
num_1400MW = []

with open("aep_1400MW.txt", "r") as f:
  for line in f:
    z_aep_1400MW.append(float(line.strip()))

with open("sp_1400MW.txt", "r") as f:
  for line in f:
    sp_data_1400MW.append(float(line.strip()))

with open("cost_ratio_1400MW.txt", "r") as f:
  for line in f:
    cost_ratio_1400MW.append(float(line.strip()))

with open("wake_1400MW.txt", "r") as f:
  for line in f:
    wake_1400MW.append(float(line.strip()))

with open("lcoe_1400MW.txt", "r") as f:
  for line in f:
    lcoe_1400MW.append(float(line.strip()))

with open("num_1400MW.txt", "r") as f:
  for line in f:
    num_1400MW.append(float(line.strip()))

# cond = [i for i in range(len(sp_data_1400MW)) if sp_data_1400MW[i] > 200 and sp_data_1400MW[i] < 600] #remove specific power values below 200 and above 600
# sp_data_1400MW = [sp_data_1400MW[idx] for idx in cond]
# z_aep_1400MW= [z_aep_1400MW[idx] for idx in cond]
# cost_ratio_1400MW = [cost_ratio_1400MW[idx] for idx in cond]
# wake_1400MW= [wake_1400MW[idx] for idx in cond]



fs= 16
s = 20


plt.scatter(sp_data_600MW, lcoe_600MW,s = s, marker = '^', label = '600 MW')
plt.scatter(sp_data_1000MW,lcoe_1000MW,s = s, marker = 'o', label = '1000 MW')
plt.scatter(sp_data_1400MW,lcoe_1400MW,s = s, marker = 'v', label = '1400 MW')
plt.xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
plt.ylabel('LCoE (Euros/MWh)', fontsize = fs)
plt.grid(axis = 'both', alpha = 0.1)
plt.title('Power and Area constrained')
plt.legend()
plt.savefig("plots/lcoe_farmpower_sensitivity.png",bbox_inches='tight',dpi=300)
plt.show()


# plt.scatter(sp_data_600MW, norm_cost_ratio_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW, norm_cost_ratio_1000MW, s = s,marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW, norm_cost_ratio_1400MW, s = s,marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized cost ratio', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
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
# cost_ratio_600MW = [(c-min(cost_ratio_600MW))/(max(cost_ratio_600MW) - min(cost_ratio_600MW)) for c in cost_ratio_600MW]
# cost_ratio_1000MW = [(c-min(cost_ratio_1000MW))/(max(cost_ratio_1000MW) - min(cost_ratio_1000MW)) for c in cost_ratio_1000MW]
# cost_ratio_1400MW = [(c-min(cost_ratio_1400MW))/(max(cost_ratio_1400MW) - min(cost_ratio_1400MW)) for c in cost_ratio_1400MW]


cost_ratio_600MW = [c/max(cost_ratio_600MW) for c in cost_ratio_600MW]
cost_ratio_1000MW = [c/max(cost_ratio_1000MW) for c in cost_ratio_1000MW]
cost_ratio_1400MW = [c/max(cost_ratio_1400MW) for c in cost_ratio_1400MW]

num_600MW = [c/max(num_600MW) for c in num_600MW]
num_1000MW = [c/max(num_1000MW) for c in num_1000MW]
num_1400MW = [c/max(num_1400MW) for c in num_1400MW]

cr600 = np.array(cost_ratio_600MW)
cr1000 = np.array(cost_ratio_1000MW)
cr1400 = np.array(cost_ratio_1400MW)
grad_cr_sp_600 = np.gradient(cr600, sp_data_600MW)
grad_cr_sp_1000 = np.gradient(cr1000, sp_data_1000MW)
grad_cr_sp_1400 = np.gradient(cr1400, sp_data_1400MW)

# grad_cr_sp_600 = [grad/max(grad_cr_sp_600) for grad in grad_cr_sp_600]
# grad_cr_sp_1000 = [grad/max(grad_cr_sp_1000) for grad in grad_cr_sp_1000]
# grad_cr_sp_1400 = [grad/max(grad_cr_sp_1400) for grad in grad_cr_sp_1400]

# plt.scatter(sp_data_600MW, cost_ratio_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW,cost_ratio_1000MW,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW,cost_ratio_1400MW ,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Normalized Cost ratio', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()
#
# z_aep_600MW = [(a-min(z_aep_600MW))/(max(z_aep_600MW) - min(z_aep_600MW)) for a in z_aep_600MW]
# z_aep_1000MW = [(a-min(z_aep_1000MW))/(max(z_aep_1000MW) - min(z_aep_1000MW)) for a in z_aep_1000MW]
# z_aep_1400MW = [(a-min(z_aep_1400MW))/(max(z_aep_1400MW) - min(z_aep_1400MW)) for a in z_aep_1400MW]

z_aep_600MW = [a/max(z_aep_600MW) for a in z_aep_600MW]
z_aep_1000MW = [a/max(z_aep_1000MW) for a in z_aep_1000MW]
z_aep_1400MW = [a/max(z_aep_1400MW) for a in z_aep_1400MW]

# wake_600MW = [a/max(wake_600MW) for a in wake_600MW]
# wake_1000MW = [a/max(wake_1000MW) for a in wake_1000MW]
# wake_1400MW = [a/max(wake_1400MW) for a in wake_1400MW]

aep600 = np.array(z_aep_600MW)
aep1000 = np.array(z_aep_1000MW)
aep1400 = np.array(z_aep_1400MW)
grad_aep_sp_600 = np.gradient(aep600, sp_data_600MW)
grad_aep_sp_1000 = np.gradient(aep1000, sp_data_1000MW)
grad_aep_sp_1400 = np.gradient(aep1400, sp_data_1400MW)

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
axs[2].set_ylabel('Normalized Wake factor', fontsize = fs)
axs[2].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[2].legend()

plt.savefig("plots/farmpower_sensitivity.png",bbox_inches='tight',dpi=100)
plt.show()

# plt.scatter(sp_data_600MW, z_aep_600MW,s = s, marker = '^', label = '600 MW')
# plt.scatter(sp_data_1000MW,z_aep_1000MW ,s = s, marker = 'o', label = '1000 MW')
# plt.scatter(sp_data_1400MW,z_aep_1400MW,s = s, marker = 'v', label = '1400 MW')
# plt.xlabel('Turbine specific power (W/m2)', fontsize = fs)
# plt.ylabel('Gradient of AEP', fontsize = fs)
# plt.grid(axis = 'both', alpha = 0.1)
# plt.title('Power and Area constrained')
# plt.legend()
# plt.show()



##### Analyze farm area case ####

sp_data_baseline = []
z_aep_area100 = []
cost_ratio_area100 = []
wake_area100 = []
num_area100 = []

with open("aep_area100.txt", "r") as f:
  for line in f:
    z_aep_area100.append(float(line.strip()))

with open("sp_baseline.txt", "r") as f:
  for line in f:
    sp_data_baseline.append(float(line.strip()))

with open("cost_ratio_area100.txt", "r") as f:
  for line in f:
    cost_ratio_area100.append(float(line.strip()))

with open("wake_area100.txt", "r") as f:
  for line in f:
    wake_area100.append(float(line.strip()))

with open("num_area100.txt", "r") as f:
  for line in f:
    num_area100.append(float(line.strip()))


# cond = [i for i in range(len(sp_data_baseline)) if sp_data_baseline[i] > 200 and sp_data_baseline[i] < 600] #remove specific power values below 200 and above 600
# sp_data_baseline= [sp_data_baseline[idx] for idx in cond]
# z_aep_area100= [z_aep_area100[idx] for idx in cond]
# cost_ratio_area100 = [cost_ratio_area100[idx] for idx in cond]
# wake_area100 = [wake_area100[idx] for idx in cond]

z_aep_area200 = []
cost_ratio_area200 = []
wake_area200 = []
num_area200 = []

with open("aep_area200.txt", "r") as f:
  for line in f:
    z_aep_area200.append(float(line.strip()))


with open("cost_ratio_area200.txt", "r") as f:
  for line in f:
    cost_ratio_area200.append(float(line.strip()))

with open("wake_area200.txt", "r") as f:
  for line in f:
    wake_area200.append(float(line.strip()))

with open("num_area200.txt", "r") as f:
  for line in f:
    num_area200.append(float(line.strip()))

# z_aep_area200= [z_aep_area200[idx] for idx in cond]
# cost_ratio_area200 = [cost_ratio_area200[idx] for idx in cond]
# wake_area200 = [wake_area200[idx] for idx in cond]



cost_ratio_area100= [a/max(cost_ratio_area100) for a in cost_ratio_area100]
cost_ratio_area200 = [a/max(cost_ratio_area200) for a in cost_ratio_area200]

num_area100= [a/max(num_area100) for a in num_area100]
num_area200 = [a/max(num_area200) for a in num_area200]


z_aep_area100= [a/max(z_aep_area100) for a in z_aep_area100]
z_aep_area200 = [a/max(z_aep_area200) for a in z_aep_area200]

wake_loss_factor_area100 = [1-w for w in wake_area100]
wake_loss_factor_area200 = [1-w for w in wake_area200]

wake_loss_factor_area100 = [a/max(wake_loss_factor_area100) for a in wake_loss_factor_area100]
wake_loss_factor_area200 = [a/max(wake_loss_factor_area200) for a in wake_loss_factor_area200]

# wake_area100 = [a/max(wake_area100) for a in wake_area100]
# wake_area200 = [a/max(wake_area200) for a in wake_area200]

# wake_area100= [a/max(wake_loss_factor_area100) for a in wake_loss_factor_area100]
# wake_area200 = [a/max(wake_loss_factor_area200) for a in wake_loss_factor_area200]

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

#
# axs[0].scatter(sp_data_baseline, cost_ratio_area100,s = s, marker = '^', label = 'Area: 100 km2')
# axs[0].scatter(sp_data_baseline,cost_ratio_area200,s = s, marker = 'o', label = 'Area: 200 km2')
# axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[0].set_ylabel('Normalized cost ratio', fontsize = fs)
# axs[0].legend()

axs[0].scatter(sp_data_baseline, num_area100,s = s, marker = '^', label = 'Area: 100 km2')
axs[0].scatter(sp_data_baseline,num_area200,s = s, marker = 'o', label = 'Area: 200 km2')
axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[0].set_ylabel('Normalized costs', fontsize = fs)
axs[0].legend()

axs[1].scatter(sp_data_baseline, z_aep_area100,s = s, marker = '^', label = 'Area: 100 km2')
axs[1].scatter(sp_data_baseline,z_aep_area200,s = s, marker = 'o', label = 'Area: 200 km2')
axs[1].set_ylabel('Normalized AEP', fontsize = fs)
axs[1].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[1].legend()

axs[2].scatter(sp_data_baseline, wake_loss_factor_area100,s = s, marker = '^', label = 'Area: 100 km2')
axs[2].scatter(sp_data_baseline,wake_loss_factor_area200,s = s, marker = 'o', label = 'Area: 200 km2')
axs[2].set_ylabel('Normalized Wake factor', fontsize = fs)
axs[2].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[2].legend()

plt.savefig("plots/farmarea_sensitivity.png",bbox_inches='tight',dpi=100)
plt.show()







##### Analyze wind speed case ####

sp_data_baseline = []
z_aep_baseline = []
cost_ratio_baseline = []
wake_baseline = []
aep_turbine_baseline = []
num_baseline = []

with open("aep_baseline.txt", "r") as f:
  for line in f:
    z_aep_baseline.append(float(line.strip()))

with open("aep_turbine_baseline.txt", "r") as f:
  for line in f:
    aep_turbine_baseline.append(float(line.strip()))

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

z_aep_lowwind = []
cost_ratio_lowwind = []
wake_lowwind = []
aep_turbine_lowwind = []
num_lowwind = []

with open("aep_lowwind.txt", "r") as f:
  for line in f:
    z_aep_lowwind.append(float(line.strip()))

with open("aep_turbine_lowwind.txt", "r") as f:
  for line in f:
    aep_turbine_lowwind.append(float(line.strip()))


with open("cost_ratio_lowwind.txt", "r") as f:
  for line in f:
    cost_ratio_lowwind.append(float(line.strip()))

with open("wake_lowwind.txt", "r") as f:
  for line in f:
    wake_lowwind.append(float(line.strip()))

with open("num_lowwind.txt", "r") as f:
  for line in f:
    num_lowwind.append(float(line.strip()))


# z_aep_area200= [z_aep_area200[idx] for idx in cond]
# cost_ratio_area200 = [cost_ratio_area200[idx] for idx in cond]
# wake_area200 = [wake_area200[idx] for idx in cond]


# cost_ratio_area100= [(a-min(cost_ratio_area100))/(max(cost_ratio_area100) - min(cost_ratio_area100)) for a in cost_ratio_area100]
# cost_ratio_area200 = [(a-min(cost_ratio_area200))/(max(cost_ratio_area200) - min(cost_ratio_area200)) for a in cost_ratio_area200]

cost_ratio_baseline= [a/max(cost_ratio_baseline) for a in cost_ratio_baseline]
cost_ratio_lowwind = [a/max(cost_ratio_lowwind) for a in cost_ratio_lowwind]

num_baseline = [a/max(num_baseline) for a in num_baseline]
num_lowwind = [a/max(num_lowwind) for a in num_lowwind]

# z_aep_area100= [(a-min(z_aep_area100))/(max(z_aep_area100) - min(z_aep_area100)) for a in z_aep_area100]
# z_aep_area200 = [(a-min(z_aep_area200))/(max(z_aep_area200) - min(z_aep_area200)) for a in z_aep_area200]

z_aep_baseline= [a/max(z_aep_baseline) for a in z_aep_baseline]
z_aep_lowwind = [a/max(z_aep_lowwind) for a in z_aep_lowwind]

aep_turbine_baseline= [a/max(aep_turbine_baseline) for a in aep_turbine_baseline]
aep_turbine_lowwind = [a/max(aep_turbine_lowwind) for a in aep_turbine_lowwind]

wake_loss_factor_baseline = [1-w for w in wake_baseline]
wake_loss_factor_lowwind = [1-w for w in wake_lowwind]

wake_loss_factor_baseline = [a/max(wake_loss_factor_baseline) for a in wake_loss_factor_baseline]
wake_loss_factor_lowwind = [a/max(wake_loss_factor_lowwind) for a in wake_loss_factor_lowwind]
#
# wake_baseline = [a/max(wake_baseline) for a in wake_baseline]
# wake_lowwind = [a/max(wake_lowwind) for a in wake_lowwind]

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



fig, axs = plt.subplots(nrows =1, ncols= 4, figsize=(22,4))


# axs[0].scatter(sp_data_baseline, cost_ratio_baseline,s = s, marker = '^', label = 'High wind')
# axs[0].scatter(sp_data_baseline,cost_ratio_lowwind,s = s, marker = 'o', label = 'Low wind')
# axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[0].set_ylabel('Normalized cost ratio', fontsize = fs)
# axs[0].legend()

axs[0].scatter(sp_data_baseline, num_baseline,s = s, marker = '^', label = 'High wind')
axs[0].scatter(sp_data_baseline,num_lowwind,s = s, marker = 'o', label = 'Low wind')
axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[0].set_ylabel('Normalized costs', fontsize = fs)
axs[0].legend()

axs[1].scatter(sp_data_baseline, z_aep_baseline,s = s, marker = '^', label = 'High wind')
axs[1].scatter(sp_data_baseline,z_aep_lowwind,s = s, marker = 'o', label = 'Low wind')
axs[1].set_ylabel('Normalized AEP', fontsize = fs)
axs[1].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[1].legend()

axs[2].scatter(sp_data_baseline, wake_loss_factor_baseline,s = s, marker = '^', label = 'High wind')
axs[2].scatter(sp_data_baseline,wake_loss_factor_lowwind,s = s, marker = 'o', label = 'Low wind')
axs[2].set_ylabel('Normalized wake factor', fontsize = fs)
axs[2].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[2].legend()

axs[3].scatter(sp_data_baseline, aep_turbine_baseline,s = s, marker = '^', label = 'High wind')
axs[3].scatter(sp_data_baseline,aep_turbine_lowwind,s = s, marker = 'o', label = 'Low wind')
axs[3].set_ylabel('Normalized AEP (No wake losses)', fontsize = fs)
axs[3].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[3].legend()

plt.savefig("plots/windspeed_sensitivity.png",bbox_inches='tight',dpi=300)
plt.show()


#
# wake_baseline = [a/max(wake_baseline) for a in wake_baseline]
# wake_lowwind = [a/max(wake_lowwind) for a in wake_lowwind]
#
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
#
#
# axs[0].scatter(sp_data_baseline, cost_ratio_baseline,s = s, marker = '^', label = 'High wind')
# axs[0].scatter(sp_data_baseline,cost_ratio_lowwind,s = s, marker = 'o', label = 'Low wind')
# axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[0].set_ylabel('Normalized cost ratio', fontsize = fs)
# axs[0].legend()
#
# axs[1].scatter(sp_data_baseline, z_aep_baseline,s = s, marker = '^', label = 'High wind')
# axs[1].scatter(sp_data_baseline,z_aep_lowwind,s = s, marker = 'o', label = 'Low wind')
# axs[1].set_ylabel('Normalized AEP', fontsize = fs)
# axs[1].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[1].legend()
#
# plt.savefig("plots/windspeed_sensitivity_part1.png",bbox_inches='tight',dpi=300)
# plt.show()
#
# fig, axs = plt.subplots(nrows =1, ncols= 2, figsize=(10,4))
#
# axs[0].scatter(sp_data_baseline, wake_baseline,s = s, marker = '^', label = 'High wind')
# axs[0].scatter(sp_data_baseline,wake_lowwind,s = s, marker = 'o', label = 'Low wind')
# axs[0].set_ylabel('Wake losses', fontsize = fs)
# axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[0].legend()
#
# axs[1].scatter(sp_data_baseline, aep_turbine_baseline,s = s, marker = '^', label = 'High wind')
# axs[1].scatter(sp_data_baseline,aep_turbine_lowwind,s = s, marker = 'o', label = 'Low wind')
# axs[1].set_ylabel('Normalized AEP (No wake losses)', fontsize = fs)
# axs[1].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
# axs[1].legend()
#
# # plt.savefig("plots/windspeed_sensitivity_part2.png",bbox_inches='tight',dpi=300)
# plt.show()