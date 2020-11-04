#Critical load cases derived from the database of the 5 MW turbine

import scipy.io
import numpy as np
'''
wind_type:
1 - steady wind (steady)
2 - stepped wind (stepped)
3 - normal wind profile (NWP)
4 - normal turbulence model (NTM)
5 - Annual extreme wind speed ( EWM1)
6 - 50 year extreme wind speed (EWM50)
7 - Extreme wind shear (EWS)
8 - Extreme turbulence model (ETM)
9 - Extreme operating gust (EOG)
10 - Extreme direction change (EDC)
11 - Extreme coherent gust (ECG)

operating mode type:
1 - normal power production (normal)
2 - power production with fault (grid loss)
3 - startup 
4 - normal shutdown 
5 - emergency shutdown
6 - idling
7 - parked


Based on max Tip Deflection 
-DLC 1.3 at 11.4 m/s

Based on max Oop moment
-DLC 1.3 at 11.4 m/s

Based on max Ip moment
-DLC 3.3 at 4m/s

Based on max Flapwise moment
-DLC 3.3 at 4m/s

Based on max Edgewise moment
-DLC 2.1 at 11.4 m/s

'''

#General settings
#Settings for ly an lz have to change depending on the diameter.


def load_case_selector(load_case, rotor_diameter, rated_ws):

    settings_run_seeds = []
    settings_wind_dt = 0.1
    settings_wind_ny = 20.0
    settings_wind_nz = 20.0
    settings_wind_class = np.array([1, 2])
    settings_wind_class = settings_wind_class.reshape(2, 1)
    settings_wind_step = 5.0
    settings_wind_ews = 60.0
    settings_wind_eog = 60.0
    settings_wind_ecg = 60.0
    settings_wind_ly = rotor_diameter  #+ 3.0 #To ensure entire rotor coverage
    settings_wind_lz = rotor_diameter  #+ 3.0
    settings_wind_edc = 60.0
    settings_mode_actiontime = 60.0
    settings_run_time = []
    settings_wind_t = []
    settings_run_windspeed = []
    settings_wind_type = []
    settings_mode_type = []

    if load_case==1.3:
        settings_run_time = 60.0
        settings_wind_t = 600.0
        settings_run_windspeed = rated_ws #11.4
        settings_wind_type = 8.0
        settings_mode_type = 1.0
        settings_run_seeds = 1.0


    elif load_case==2.1:
        settings_run_time = 100.0
        settings_wind_t = 100.0
        settings_run_windspeed = rated_ws #11.4
        settings_wind_type = 4.0
        settings_mode_type = 2.0



    elif load_case==3.3:
        settings_run_time = 100.0
        settings_wind_t = 100.0
        settings_run_windspeed = 4.0
        settings_wind_type = 10.0
        settings_mode_type = 3.0
        settings_mode_actiontime = 70.0
        settings_wind_edc = 75.0
        settings_wind_ny = 30.0
        settings_wind_nz = 30.0



    elif load_case=='Fatigue':
        settings_run_seeds = 1.0
        settings_run_time = 660.0
        settings_wind_t = 660.0
        settings_run_windspeed = np.array([6.0, 8.0, 12.0, 16.0, 20.0, 23.5])
        settings_wind_type = 4.0
        settings_mode_type = 1.0

    scipy.io.savemat('Matlab_scripts\CertificationSettings.mat', dict(settings_run_time=settings_run_time, settings_run_seeds=settings_run_seeds,
                              settings_run_windspeed=settings_run_windspeed, settings_wind_type=settings_wind_type,
                              settings_wind_t=settings_wind_t, settings_wind_ly=settings_wind_ly,
                              settings_wind_lz=settings_wind_lz, settings_wind_dt=settings_wind_dt,
                              settings_wind_ny=settings_wind_ny, settings_wind_nz=settings_wind_nz,
                              settings_wind_class=settings_wind_class, settings_wind_step=settings_wind_step,
                              settings_wind_ews=settings_wind_ews, settings_wind_eog=settings_wind_eog,
                              settings_wind_edc=settings_wind_edc, settings_wind_ecg=settings_wind_ecg,
                              settings_mode_type=settings_mode_type, settings_mode_actiontime=settings_mode_actiontime))








