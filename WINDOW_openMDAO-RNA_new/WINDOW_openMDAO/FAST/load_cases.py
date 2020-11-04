'''
Load case decider
'''

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
'''

def load_case(dlc_type, wind_type, operating_mode, rated_ws):

    # Certification settings required to run the analysis
    settings_run_time = 100.0
    settings_run_seeds = 1.0
    settings_wind_t = 100.0
    settings_wind_ly = 126.0
    settings_wind_lz = 126.0
    settings_wind_dt = 0.1
    settings_wind_ny = 20.0
    settings_wind_nz = 20.0
    settings_wind_class = np.array([1,2])
    settings_wind_class=settings_wind_class.reshape(2,1)
    settings_wind_step = 5.0
    settings_wind_ews = 60.0
    settings_wind_eog = 60.0
    settings_wind_edc = 60.0
    settings_wind_ecg = 60.0
    settings_mode_actiontime = 60.0

    if dlc_type=='fatigue':
        settings_run_windspeed = np.arange(4, 26, 2)
        settings_wind_type = 4.0
        settings_mode_type = 1.0


    if dlc_type=='ultimate':
        settings_run_windspeed = rated_ws
        if wind_type=='steady':
            settings_wind_type = 1.0
        elif wind_type=='stepped':
            settings_wind_type = 2.0

        elif wind_type=='NWP':
            settings_wind_type = 3.0

        elif wind_type=='NTM':
            settings_wind_type = 4.0

        elif wind_type=='EWM1':
            settings_wind_type = 5.0

        elif wind_type=='EWM50':
            settings_wind_type = 6.0

        elif wind_type=='EWS':
            settings_wind_type = 7.0

        elif wind_type=='ETM':
            settings_wind_type = 8.0

        elif wind_type=='EOG':
            settings_wind_type = 9.0

        elif wind_type=='EDC':
            settings_wind_type = 10.0

        elif wind_type=='ECG':
            settings_wind_type = 11.0

        # operating mode
        if operating_mode=='normal':
            settings_mode_type = 1.0

        elif operating_mode=='grid loss':
            settings_mode_type = 2.0

        elif operating_mode=='startup':
            settings_mode_type = 3.0

        elif operating_mode=='normal shutdown':
            settings_mode_type = 4.0

        elif operating_mode=='emergency shutdown':
            settings_mode_type = 5.0

        elif operating_mode=='idling':
            settings_mode_type = 6.0

        elif operating_mode=='parked':
            settings_mode_type = 7.0




    scipy.io.savemat('CertificationSettings.mat',
                         dict(settings_run_time=settings_run_time, settings_run_seeds=settings_run_seeds,
                              settings_run_windspeed=settings_run_windspeed, settings_wind_type=settings_wind_type,
                              settings_wind_t=settings_wind_t, settings_wind_ly=settings_wind_ly,
                              settings_wind_lz=settings_wind_lz, settings_wind_dt=settings_wind_dt,
                              settings_wind_ny=settings_wind_ny, settings_wind_nz=settings_wind_nz,
                              settings_wind_class=settings_wind_class, settings_wind_step=settings_wind_step,
                              settings_wind_ews=settings_wind_ews, settings_wind_eog=settings_wind_eog,
                              settings_wind_edc=settings_wind_edc, settings_wind_ecg=settings_wind_ecg,
                              settings_mode_type=settings_mode_type, settings_mode_actiontime=settings_mode_actiontime))