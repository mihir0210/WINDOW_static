
import matplotlib.pyplot as plt

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


with open("wake_baseline.txt", "r") as f:
  for line in f:
    wake_baseline.append(float(line.strip()))

with open("num_baseline.txt", "r") as f:
  for line in f:
    num_baseline.append(float(line.strip()))


sp_data_fixedarea = []
z_aep_fixedarea = []
cost_ratio_fixedarea = []
wake_fixedarea = []
num_fixedarea = []

with open("aep_fixedarea.txt", "r") as f:
  for line in f:
    z_aep_fixedarea.append(float(line.strip()))


with open("sp_fixedarea.txt", "r") as f:
  for line in f:
    sp_data_fixedarea.append(float(line.strip()))


with open("wake_fixedarea.txt", "r") as f:
  for line in f:
    wake_fixedarea.append(float(line.strip()))

with open("num_fixedarea.txt", "r") as f:
  for line in f:
    num_fixedarea.append(float(line.strip()))

cond = [i for i in range(len(sp_data_fixedarea)) if sp_data_fixedarea[i] < 900] #remove specific power values above 900
sp_data_fixedarea= [sp_data_fixedarea[idx] for idx in cond]
z_aep_fixedarea= [z_aep_fixedarea[idx] for idx in cond]
num_fixedarea = [num_fixedarea[idx] for idx in cond]
wake_fixedarea = [wake_fixedarea[idx] for idx in cond]


num_baseline = [a/max(num_baseline) for a in num_baseline]
num_fixedarea = [a/max(num_fixedarea) for a in num_fixedarea]


z_aep_baseline = [a/max(z_aep_baseline) for a in z_aep_baseline]
z_aep_fixedarea = [a/max(z_aep_fixedarea) for a in z_aep_fixedarea]


wake_loss_factor_baseline = [1-w for w in wake_baseline]
wake_loss_factor_fixedarea = [1-w for w in wake_fixedarea]


wake_loss_factor_baseline = [a/max(wake_loss_factor_baseline) for a in wake_loss_factor_baseline]
wake_loss_factor_fixedarea = [a/max(wake_loss_factor_fixedarea) for a in wake_loss_factor_fixedarea]


fs= 16
s = 20

fig, axs = plt.subplots(nrows =1, ncols= 3, figsize=(16,4))



axs[0].scatter(sp_data_baseline, num_baseline, s = s, marker = '^', label = 'Baseline')
axs[0].scatter(sp_data_fixedarea, num_fixedarea, s = s, marker = 'v', label = 'Fixed area only')
axs[0].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[0].set_ylabel('Normalized Costs', fontsize = fs)
axs[0].legend()


axs[1].scatter(sp_data_baseline, z_aep_baseline, s = s, marker = '^', label = 'Baseline')
axs[1].scatter(sp_data_fixedarea, z_aep_fixedarea, s = s, marker = 'v', label = 'Fixed area only')
axs[1].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[1].set_ylabel('Normalized AEP', fontsize = fs)
axs[1].legend()

axs[2].scatter(sp_data_baseline, wake_loss_factor_baseline, s = s, marker = '^', label = 'Baseline')
axs[2].scatter(sp_data_fixedarea, wake_loss_factor_fixedarea, s = s, marker = 'v', label = 'Fixed area only')
axs[2].set_ylabel('Normalized wake factor', fontsize = fs)
axs[2].set_xlabel(r'Turbine specific power ($\frac{W}{m^2}$)', fontsize = fs)
axs[2].legend()

plt.savefig("plots/fixed_farmarea_sensitivity.png",bbox_inches='tight',dpi=300)
plt.show()