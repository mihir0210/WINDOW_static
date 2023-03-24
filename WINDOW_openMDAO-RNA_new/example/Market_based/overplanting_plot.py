import matplotlib.dates
import numpy as np
import matplotlib.pyplot as plt

lcoe_baseline = np.load("lcoe_matrix_baseline.dat", allow_pickle=True)
cf_baseline = np.load("capacity_factor_baseline.dat", allow_pickle=True)
# lcoe_overplanted850 = np.load("lcoe_matrix_overplanted850.dat", allow_pickle=True)
# cf_overplanted850 = np.load("capacity_factor_overplanted850.dat", allow_pickle=True)
# lcoe_overplanted950 = np.load("lcoe_matrix_overplanted950.dat", allow_pickle=True)
# cf_overplanted950 = np.load("capacity_factor_overplanted950.dat", allow_pickle=True)
lcoe_overplanted1200 = np.load("lcoe_matrix_overplanted1200.dat", allow_pickle=True)
cf_overplanted1200 = np.load("capacity_factor_overplanted1200.dat", allow_pickle=True)
p_rated = np.load("power_matrix_baseline_course.dat", allow_pickle=True)
d_rotor = np.load("diameter_matrix_baseline_course.dat", allow_pickle=True)



# irr_overplanted850 = np.load("IRR_overplanted850.dat", allow_pickle=True)
# npv_overplanted850 = np.load("NPV_overplanted850.dat", allow_pickle=True)
# irr_overplanted950 = np.load("IRR_overplanted950.dat", allow_pickle=True)
# npv_overplanted950 = np.load("NPV_overplanted950.dat", allow_pickle=True)
irr_overplanted1200 = np.load("IRR_overplanted1200.dat", allow_pickle=True)
npv_overplanted1200 = np.load("NPV_overplanted1200.dat", allow_pickle=True)

irr_baseline = np.load("IRR_baseline.dat", allow_pickle=True)
npv_baseline = np.load("NPV_baseline.dat", allow_pickle=True)


# cf_increase = np.divide(cf_overplanted, cf_baseline)
# lcoe_increase = np.divide(lcoe_overplanted, lcoe_baseline)
#
# cf_by_lcoe = np.divide(cf_increase, lcoe_increase)
# y_label = r'$\frac{\delta Cf}{\delta LCoE}$'

fs = 16
lw = 1.5
la = 0.3

# n_colorbars = (np.amax(capacity_factor) - np.amin(capacity_factor)) / 0.05


fig, ax = plt.subplots()

import seaborn as sns
from matplotlib.colors import ListedColormap

my_cmap = sns.color_palette("rocket", as_cmap=True)
# my_cmap = sns.color_palette("mako", as_cmap=True)
# c = plt.contourf(d_rotor,p_rated,property, 50, cmap='YlOrRd')
# c = plt.contourf(d_rotor, p_rated, cf_increase, 100, cmap=my_cmap.reversed())
# c = plt.contourf(d_rotor,p_rated,property, round(n_colorbars), cmap = my_cmap.reversed())
#
# c = plt.contourf(d_eval,p_eval,z_pred, round(n_colorbars)-1, cmap = my_cmap.reversed())
# cbar = fig.colorbar(c)

# plt.plot(d_sp, p_sp,'k--',linewidth=lw, alpha=la,label ='Constant specific power line')

# plt.plot(d_eval[result_deterministic[0]], p_eval[result_deterministic[1]], 'ko')
# plt.scatter(d_eval[result_deterministic[1]], p_eval[result_deterministic[0]], marker = 'o', c='w', s = 60, alpha = 0.5) #, label='Baseline')
# plt.text(222, 15.7, 'Global optimum (Baseline)', horizontalalignment='center', verticalalignment='center', size = '10')
# plt.plot(opt_d_lcoe, power_scatter,'k-.',linewidth=lw, alpha=la,label ='Optimum Rotor Diameter')

# plt.scatter(x_fixedpower, y_fixedpower, marker = 'o', c='k', s = 60, alpha = 0.5)
# plt.text(230, 13.5, 'Global optimum (Fixed power only)', horizontalalignment='center', verticalalignment='center', size = '10')
# plt.scatter(x_fixedarea, y_fixedarea, marker = 'o', c='k', s = 60, alpha = 0.5)
# plt.text(230, 17.2, 'Global optimum (Fixed area only)', horizontalalignment='center', verticalalignment='center', size = '10')
plt.scatter(cf_baseline, lcoe_baseline, marker='o', c='C0', s=20,  label ='Baseline')
plt.scatter(cf_overplanted1200, lcoe_overplanted1200, marker='o', c='C1', s=20,  label ='Overplanted (20%)')
# plt.scatter(cf_baseline, irr_baseline*100, marker='o', c='C0', s=20,  label ='Baseline')
# plt.scatter(cf_overplanted1200, irr_overplanted1200*100, marker='o', c='C1', s=20,  label ='Overplanted (20%)')
# plt.scatter(cf_baseline, npv_baseline, marker='o', c='C0', s=20,  label ='Baseline')
# plt.scatter(cf_overplanted1200, npv_overplanted1200, marker='o', c='C1', s=20,  label ='Overplanted (20%)')


# plt.scatter(cf_baseline, irr_baseline*100, marker='o', c='C0', s=20,  label ='Baseline')
# plt.scatter(cf_overplanted950, irr_overplanted950*100, marker='o', c='C1', s=20,  label ='Overplanted (5 %)')
# plt.scatter(cf_overplanted850, irr_overplanted850*100, marker='o', c='C2', s=20,  label ='Overplanted (15 %)')
# plt.scatter(cf_baseline, npv_baseline, marker='o', c='C0', s=20,  label ='Baseline')
# plt.scatter(cf_overplanted950, npv_overplanted950, marker='o', c='C1', s=20,  label ='Overplanted (5 %)')
# plt.scatter(cf_overplanted850, npv_overplanted850, marker='o', c='C2', s=20,  label ='Overplanted (15 %)')


# plt.scatter(x_wind, y_wind, marker='o', c='k', s=20) #,  label ='Wind speed'
# plt.scatter(x_area, y_area, marker='o', c='k', s=20) #, label ='Area')
# plt.scatter(x_dg, y_dg, marker='o', c='k', s=20) #,  label ='Distance to grid')
# plt.scatter(x_farmpower, y_farmpower, marker='o', c='k', s=20) #,  label ='Farm power')

plt.xlabel('Capacity factor (-)', fontsize=fs)
plt.ylabel('LCoE (Euros/MWh)', fontsize=fs)
# plt.ylabel('NPV (Million Euros)', fontsize=fs)
# plt.ylabel('IRR (%)', fontsize=fs)
# plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
# cbar.ax.set_ylabel(y_label, fontsize=fs)
plt.legend(loc='upper left',fancybox=True, framealpha=0.5, fontsize=fs)
# plt.xlim(rad_values[0]*2, rad_values[-1]*2)
# plt.ylim(10,20)
plt.grid(axis='both', alpha=0.1)
ax.tick_params(axis='both', direction='in', length=5)

# plt.savefig('cf_lcoe_base_vs_overplanted.png',bbox_inches='tight',dpi=300)
# plt.savefig('cf_irr_base_vs_overplanted.png',bbox_inches='tight',dpi=300)
# plt.savefig('cf_npv_base_vs_overplanted.png',bbox_inches='tight',dpi=300)
# plt.savefig('cf_lcoe_base_vs_overplanted1200.png',bbox_inches='tight',dpi=300)
# plt.savefig('cf_irr_base_vs_overplanted1200.png',bbox_inches='tight',dpi=300)
# plt.savefig('cf_npv_base_vs_overplanted1200.png',bbox_inches='tight',dpi=300)
plt.show()



###### farm power vs wind speed and spot prices vs wind speed ############
import pandas as pd

wind_file = 'NorthSea_2019_100m_hourly_ERA5_withdir.csv'
ws_wd = pd.read_csv(wind_file)
wind_speed = ws_wd['wind_speed']

spot_prices = np.genfromtxt('NL_2019_spot_price_hourly.csv')

bins = np.linspace(0, 25, 26)
digitized = np.digitize(wind_speed, bins)

bin_mean_spot = [spot_prices[digitized == i].mean() for i in range(1, len(bins))]
bin_spotprices = [spot_prices[digitized == i] for i in range(1, len(bins))]

print(bin_spotprices)

#COMPARE POWER CURVE OF TWO DESIGNS WITH SAME CAPACITY FACTOR (0.5)

p = 12.05
r = 227/2


filename_power = '1000MW_fixed_power/farm_power_' + str(p) + '_' + str(r * 2) + '.csv'
df_power = pd.read_csv(filename_power, header=None)
farm_power_ts = df_power.iloc[1::, 1]  # farm power time series in MW
farm_power_ts_baseline = pd.Series.to_numpy(farm_power_ts)

bin_mean_baseline = [farm_power_ts_baseline[digitized == i].mean() for i in range(1, len(bins))]



p = 16.67
r = 120.0

filename_power = '1200MW_overplanted_fixed_power/farm_power_' + str(p) + '_' + str(r * 2) + '.csv'
df_power = pd.read_csv(filename_power, header=None)
farm_power_ts = df_power.iloc[1::, 1]  # farm power time series in MW
farm_power_ts_overplanted = pd.Series.to_numpy(farm_power_ts)

bin_mean_overplanted = [farm_power_ts_overplanted[digitized == i].mean() for i in range(1, len(bins))]



bins = np.delete(bins, 0)

fig, ax = plt.subplots()


# plt.scatter(wind_speed, farm_power_ts_baseline, marker='o', c='C0', s=10,  label ='Baseline')
# plt.scatter(wind_speed, farm_power_ts_overplanted, marker='o', c='C1', s=10,  label ='Overplanted (20%)')

plt.scatter(bins, bin_mean_baseline, marker='o', c='C0', s=60,  label ='Baseline')
plt.scatter(bins, bin_mean_overplanted, marker='o', c='C1', s=40,  label ='Overplanted (20%)')

plt.xlabel('Wind speed (m/s)', fontsize=fs)
plt.ylabel('Mean Farm power (MW)', fontsize=fs)
# plt.ylabel('NPV (Million Euros)', fontsize=fs)
# plt.ylabel('IRR (%)', fontsize=fs)
# plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
# cbar.ax.set_ylabel(y_label, fontsize=fs)
plt.legend(loc='lower right',fancybox=True, framealpha=0.5, fontsize=fs)
plt.xlim(5,15)
# plt.ylim(10,20)
plt.grid(axis='both', alpha=0.1)
ax.tick_params(axis='both', direction='in', length=5)
# plt.savefig('farm_powercurve_baseline_vs_overplanted.png',bbox_inches='tight',dpi=300)

plt.show()

fig, ax = plt.subplots(figsize =(12, 5))

plt.scatter(wind_speed, spot_prices, marker='o', c='blue', s=10)
plt.scatter(bins, bin_mean_spot, marker='o', c='red', s=20)

# plt.boxplot(bin_spotprices)
# plt.scatter(bins, bin_mean_spot, marker='o', c='red', s=10, label ='Mean spot price')
plt.xlabel('Wind speed (m/s)', fontsize=fs)
plt.ylabel('Spot prices (Euros/MWh)', fontsize=fs)
# plt.ylabel('NPV (Million Euros)', fontsize=fs)
# plt.ylabel('IRR (%)', fontsize=fs)
# plt.text(270, 15, '300 W/m$^2$', horizontalalignment='center', verticalalignment='center', size = '13')
# cbar.ax.set_ylabel(y_label, fontsize=fs)
plt.legend(loc='upper right',fancybox=True, framealpha=0.5, fontsize=fs)
# plt.xlim(5,15)
# plt.ylim(10,20)
plt.grid(axis='both', alpha=0.1)
ax.tick_params(axis='both', direction='in', length=5)
# plt.savefig('NL_2019_spotprices_vs_windspeed.png',bbox_inches='tight',dpi=300)
plt.show()