

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

'''

Explanation and script on 
https://blogs.sas.com/content/iml/2020/12/17/generate-correlated-vector.html

'''

def center(v):
    return (v-np.mean(v))

def unitvec(v):
    return (v/np.linalg.norm(v))

def corrvec(x, rho, guess, mean, std):

    u = unitvec(center(x))
    z = unitvec(center(guess))

    w = np.dot(z.transpose(),u)*u
    wperp = z - w


    v1 = rho*unitvec(w)
    v2 = np.sqrt(1-rho**2)*unitvec(wperp)
    y = v1+v2

    if np.sign(np.dot(y.transpose(),u)) != np.sign(rho):
        y = -y

    std = std*np.sqrt(len(x)-1)
    hourly_price = mean + std*y

    return hourly_price



def spot_data_test(loc):

    if loc == 'NL':
        filename_wind_speed = 'NL_onshore_windspeed_2016_2019.csv'
        filename_spot_price = 'NL_spot_price_2016_2019.csv'


        ###### FOR NL: rho, mean, std = -0.16, 39.5, 15.34 #######

        wind_speed = genfromtxt(filename_wind_speed, delimiter=',')
        spot_price = genfromtxt(filename_spot_price, delimiter=',')

        x = wind_speed
        rho = -0.16
        guess = np.random.normal(size=len(x))
        mean, std = 39.5, 15.3


    if loc == 'DK':
        filename_wind_speed = 'DK_onshore_windspeed_2016_2020.csv'
        filename_spot_price = 'DK_spot_price_2016_2020.csv'
        wind_speed = genfromtxt(filename_wind_speed, delimiter=',')
        spot_price = genfromtxt(filename_spot_price, delimiter=',')

        ###### FOR DK: rho, mean, std = -0.37, 33, 15.34 #######
        x = wind_speed
        rho = -0.37
        guess = np.random.normal(size=len(x))
        mean, std = 33, 15.3

    spot_price_generated = corrvec(x, rho, guess, mean, std)


    # plt.scatter(wind_speed, spot_price, c='C0', alpha=1, label='Historic data')
    # plt.scatter(x,spot_price_generated, c='r',alpha=0.3, label ='Generated data')
    # # plt.scatter(wind_speed, spot_price, c='C0', alpha=1)
    # # plt.text(15,90, r'$\rho_\mathrm{correlation}$ = -0.16', fontsize=18)
    # # plt.ylim([-20, 120])
    # plt.xlabel('Wind speed (m/s)', fontsize=16)
    # plt.ylabel('Spot prices (\N{euro sign}/MWh)', fontsize=16)
    # plt.legend(fontsize=14)
    # plt.ylim([-25, 125])
    # plt.xlim([0,26])
    # plt.show()
    #
    # ax = sns.distplot(spot_price, color ='C0', label='Historic data')
    # ax = sns.distplot(spot_price_generated, color ='r',label ='Generated data')
    #
    #
    # plt.text(60, 0.025, r'$\mu_\mathrm{spot}$ = 40', fontsize=18)
    # plt.text(60, 0.022, r'$\sigma_\mathrm{spot}$ = 15', fontsize=18)
    # plt.xlim([-25, 100])
    # ax.set_xlabel('Spot price (\N{euro sign}/MWh)', fontsize=16)
    # ax.set_ylabel('Density', fontsize=16)
    # plt.legend(fontsize=14)
    # plt.show()

def revenue_test():
    wind_file = 'DK_offshore_2018_100m_hourly_ERA5_withdir.csv'
    ws_wd = pd.read_csv(wind_file)
    wind_speed = ws_wd['wind_speed']


    spot_price = np.genfromtxt('DK_spot_2018.csv')

    print(np.corrcoef(wind_speed, spot_price), np.mean(spot_price), np.std(spot_price))
    p = 14.93
    r = 240/ 2

    # filename_power = '1000MW_baseline/farm_power_' + str(p) + '_' + str(r * 2) + '.csv'
    # filename_power = '1000MW_lowwind/farm_power_' + str(p) + '_' + str(r * 2) + '.csv'
    filename_power = 'farm_power_' + str(p) + '_' + str(r * 2) + '.csv'

    df_power = pd.read_csv(filename_power, header=None)
    farm_power_ts = df_power.iloc[1::, 1]  # farm power time series in MW
    farm_power_ts = pd.Series.to_numpy(farm_power_ts)

    elec_power = farm_power_ts * 0.95 * 0.97
    #
    # plt.scatter(wind_speed, elec_power)
    # plt.show()

    revenue_data = np.sum(elec_power * spot_price)

    x = wind_speed
    rho = -0.378
    guess = np.random.normal(size=len(x))
    mean, std = 44.05, 15.06



    spot_price_generated = corrvec(x, rho, guess, mean, std)

    revenue_model = np.sum(elec_power*spot_price_generated)

    # print(revenue_data, revenue_model)


spot_data_test('DK') #'NL' or 'DK'

# revenue_test()