function [Kp,Ki]=Control_gains(rated_windspeed, rated_omega)
rated_windspeed=double(rated_windspeed);

% Turbine_properties=Preprocessing(2);
% load(Turbine_properties);
% Preprocessing_new(2);
% load([pwd,'\Airfoil.mat']);
% load([pwd,'\Blade.mat']);
% load([pwd,'\Control.mat']);
% load([pwd,'\Drivetrain.mat']);
% load([pwd,'\Nacelle.mat']);
% load([pwd,'\Tower.mat']);
load('NREL5MW (gain scheduled).mat');
LinModel=Linearization(rated_windspeed,Airfoil,Blade,Control,Drivetrain,Nacelle,Tower);

%% Load mat file and convert data format
load(LinModel);
%%
data=cell2mat(data);

%% Calculate aerodynamic power sensitivity 
WindSpeeds=[rated_windspeed,ceil(rated_windspeed):25];
%WindSpeeds=[5:floor(rated_windspeed),rated_windspeed,ceil(rated_windspeed):25];
I=find(WindSpeeds==rated_windspeed);
J=I:2:length(WindSpeeds);
WindSpeeds_new=WindSpeeds(J);
%WindSpeeds_new=WindSpeeds(I:end);
aero_sensitivity=zeros(length(WindSpeeds_new),1);
theta=zeros(length(WindSpeeds_new),1);
for i=1:length(WindSpeeds_new)
    aero_sensitivity(i)=data(I).D(36,9)*1000;
    theta(i)=data(I).u_op{9};
    I=I+2;
end

c=polyfit(theta,aero_sensitivity,1);
aero_sensitivity_new=c(1)*theta+c(2);
%value of theta at which aerodynamic power sensitivity doubled from intial
%value, the value at first pitch angle
theta_k=(2*aero_sensitivity_new(1)-c(2))/c(1);

GK=1./(1+theta/theta_k);
%recommended values of natural_freq and damping ratio
%(http://orbit.dtu.dk/files/7710881/ris_r_1500.pdf)
natural_freq=0.6; %rad/s
damping_ratio=0.7; %range 0.6-0.7

%rated omega in rpm at LSS
Kp=-2*Drivetrain.LSSInertia*rated_omega*natural_freq*damping_ratio*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity(1)*-1);
Ki=-Drivetrain.LSSInertia*rated_omega*natural_freq^2*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity(1)*-1);

Control.Pitch.ScheduledPitchAngles=theta;
Control.Pitch.KpGS=Kp;
Control.Pitch.KiGS=Ki;

%add other variables as well
%save(Turbine_properties,'Airfoil','Blade','CertificationSettings','Control','Drivetrain','Nacelle','Tower');
%theta=theta*180/pi; %convert radians to Degrees
save([pwd,'\Control.mat'],'Control');
% %% plots
% yyaxis right
% plot(theta,Kp,'b');
% hold on;
% plot(theta,Ki,'r');
% ylim([0 0.025])
% ylabel('Kp and Ki');
% 
% yyaxis left
% plot(theta,GK,'k');
% ylim([0 1]);
% ylabel('Gain correction factor');
% grid on;
end



