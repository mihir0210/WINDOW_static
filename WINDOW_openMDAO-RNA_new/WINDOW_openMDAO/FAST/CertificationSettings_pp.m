function CertificationSettings=CertificationSettings_pp
load([pwd,'\CertificationSettings.mat']);
%% Certification Settings pre-processing
CertificationSettings.Wind.Type=settings_wind_type;
CertificationSettings.Wind.T=settings_wind_t;
CertificationSettings.Wind.Ly=settings_wind_ly;
CertificationSettings.Wind.Lz=settings_wind_lz;
CertificationSettings.Wind.dt=settings_wind_dt;
CertificationSettings.Wind.Ny=settings_wind_ny;
CertificationSettings.Wind.Nz=settings_wind_nz;
CertificationSettings.Wind.Class=settings_wind_class;
CertificationSettings.Wind.Step=settings_wind_step;
CertificationSettings.Wind.EWS=settings_wind_ews;
CertificationSettings.Wind.EOG=settings_wind_eog;
CertificationSettings.Wind.EDC=settings_wind_edc;
CertificationSettings.Wind.ECG=settings_wind_ecg;
CertificationSettings.Mode.Type=settings_mode_type;
CertificationSettings.Mode.Actiontime=settings_mode_actiontime;
CertificationSettings.Run.WindSpeed=settings_run_windspeed;
CertificationSettings.Run.Seeds=settings_run_seeds;
CertificationSettings.Run.Time=settings_run_time;
save([pwd,'\CertificationSettings.mat'],'CertificationSettings');