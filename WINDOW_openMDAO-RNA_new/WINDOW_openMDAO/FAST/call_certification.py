
import scipy.io
import matlab.engine
eng = matlab.engine.start_matlab()


#Certification settings required to run the analysis
settings_run_time = 660.0
settings_run_seeds = 1.0
settings_run_windspeed = 12.0
settings_wind_type = 1.0
settings_wind_t = 660.0
settings_wind_ly = 126.0
settings_wind_lz = 126.0
settings_wind_dt = 0.1
settings_wind_ny = 20.0
settings_wind_nz = 20.0
settings_wind_class = [1.0, 2.0]
settings_wind_step = 5.0
settings_wind_ews = 60.0
settings_wind_eog = 60.0
settings_wind_edc = 60.0
settings_wind_ecg = 60.0
settings_mode_type = 1.0
settings_mode_actiontime = 30.0

scipy.io.savemat('Cert_settings.mat', dict(settings_run_time=settings_run_time, settings_run_seeds=settings_run_seeds,
                                      settings_run_windspeed=settings_run_windspeed, settings_wind_type=settings_wind_type,
                                      settings_wind_t=settings_wind_t, settings_wind_ly=settings_wind_ly,
                                      settings_wind_lz=settings_wind_lz, settings_wind_dt=settings_wind_dt,
                                      settings_wind_ny=settings_wind_ny, settings_wind_nz=settings_wind_nz,
                                      settings_wind_class=settings_wind_class, settings_wind_step=settings_wind_step,
                                      settings_wind_ews=settings_wind_ews, settings_wind_eog=settings_wind_eog,
                                      settings_wind_edc=settings_wind_edc, settings_wind_ecg=settings_wind_ecg,
                                      settings_mode_type=settings_mode_type, settings_mode_actiontime=settings_mode_actiontime ))


# blade properties

blade_number = 3.0
blade_cone = 2.5
blade_ifoil = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]


scipy.io.savemat('blade_file.mat', dict(blade_number=blade_number, blade_cone =blade_cone, blade_ifoil=blade_ifoil))

ret = eng.Certification(nargout=0)