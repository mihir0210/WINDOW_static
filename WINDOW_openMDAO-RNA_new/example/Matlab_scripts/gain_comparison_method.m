%%%% gains comparison

%% new method
load('Linearized_model_5MW.mat'); 
rated_windspeed = 11.4;
WindSpeeds=[5:floor(rated_windspeed),rated_windspeed,ceil(rated_windspeed):25];
I=find(WindSpeeds==rated_windspeed);
J=I:2:length(WindSpeeds);
WindSpeeds_new=WindSpeeds(J);
aero_sensitivity=zeros(length(WindSpeeds_new),1);
theta=zeros(length(WindSpeeds_new),1);

for i=1:length(WindSpeeds_new)
    aero_sensitivity(i)=data{I}.D(36,9)*1000;
    theta(i)=data{I}.u_op{9};
    I=I+2;
end

c=polyfit(theta, aero_sensitivity,1);

%theta_new = theta;
theta_new = (pi/180)*[0; 3.83; 6.6; 8.7; 10.45; 12.06; 13.54; 14.92; 16.23; 17.47; 18.70; 19.94; 21.18; 22.35; 23.47];

aero_sensitivity_new=c(1)*theta_new+c(2);

%value of theta at which aerodynamic power sensitivity doubled from intial
%value, the value at first pitch angle
theta_k=(2*aero_sensitivity_new(1)-c(2))/c(1);

GK=1./(1+theta_new/theta_k);
%recommended values of natural_freq and damping ratio
%(http://orbit.dtu.dk/files/7710881/ris_r_1500.pdf)
natural_freq=0.6; %rad/s
damping_ratio=0.7; %range 0.6-0.7
% 
rated_omega=12.1;
Drivetrain.LSSInertia = 5025500; % Use only for 5MW 
Drivetrain.Gearbox.Ratio = 97;

%rated omega in rpm at LSS
Kp=-2*Drivetrain.LSSInertia*rated_omega*natural_freq*damping_ratio*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);
Ki=-Drivetrain.LSSInertia*rated_omega*natural_freq^2*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);

save('5MW_gains_new', 'Kp', 'Ki', 'theta_new');


%% old method 

% load('Linearized_model_5MW_oldmethod.mat'); 
% rated_windspeed = 11.4;
% WindSpeeds=[5:floor(rated_windspeed),rated_windspeed,ceil(rated_windspeed):25];
% I=find(WindSpeeds==rated_windspeed);
% J=I:length(WindSpeeds);
% WindSpeeds_new=WindSpeeds(J);
% aero_sensitivity=zeros(length(WindSpeeds_new),1);
% theta=zeros(length(WindSpeeds_new),1);
% 
% for i=1:length(WindSpeeds_new)
%     aero_sensitivity(i)=data{I}.D(36,9)*1000;
%     theta(i)=data{I}.u_op{9};
%     I=I+1;
% end
% 
% c=polyfit(theta, aero_sensitivity,1);
% 
% theta_new = theta;
% %theta_new = (pi/180)*[0; 3.83; 6.6; 8.7; 10.45; 12.06; 13.54; 14.92; 16.23; 17.47; 18.70; 19.94; 21.18; 22.35; 23.47];
% 
% aero_sensitivity_new=c(1)*theta_new+c(2);
% 
% %value of theta at which aerodynamic power sensitivity doubled from intial
% %value, the value at first pitch angle
% theta_k=(2*aero_sensitivity_new(1)-c(2))/c(1);
% 
% GK=1./(1+theta_new/theta_k);
% %recommended values of natural_freq and damping ratio
% %(http://orbit.dtu.dk/files/7710881/ris_r_1500.pdf)
% natural_freq=0.6; %rad/s
% damping_ratio=0.7; %range 0.6-0.7
% % 
% rated_omega=12.1;
% Drivetrain.LSSInertia = 5025500; % Use only for 5MW 
% Drivetrain.Gearbox.Ratio = 97;
% 
% %rated omega in rpm at LSS
% Kp=-2*Drivetrain.LSSInertia*rated_omega*natural_freq*damping_ratio*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);
% Ki=-Drivetrain.LSSInertia*rated_omega*natural_freq^2*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);

%save('5MW_gains_new', 'Kp', 'Ki', 'theta');

%% 5 MW turbine aero sensitivity

aero_sensitivity = -1*[28.24e6; 43.73e6; 51.66e6; 58.44e6; 64.44e6; 70.46e6; 76.53e6; 83.94e6;
    90.67e6; 94.71e6; 99.04e6; 105.9e6; 114.30e6; 120.20e6; 125.3e6]; 


theta = [0; 3.83; 6.6; 8.7; 10.45; 12.06; 13.54; 14.92; 16.23; 17.47; 18.70; 19.94; 21.18; 22.35; 23.47];

c=polyfit(theta, aero_sensitivity,1);

% I=find(WindSpeeds==rated_windspeed);
% theta_new = Lin.Pitch(I:end);

theta_new = theta;
%theta_new = (pi/180)*[0; 3.83; 6.6; 8.7; 10.45; 12.06; 13.54; 14.92; 16.23; 17.47; 18.70; 19.94; 21.18; 22.35; 23.47];

aero_sensitivity_new=c(1)*theta_new+c(2);

%value of theta at which aerodynamic power sensitivity doubled from intial
%value, the value at first pitch angle
theta_k=(2*aero_sensitivity_new(1)-c(2))/c(1);

GK=1./(1+theta_new/theta_k);
%recommended values of natural_freq and damping ratio
%(http://orbit.dtu.dk/files/7710881/ris_r_1500.pdf)
natural_freq=0.6; %rad/s
damping_ratio=0.7; %range 0.6-0.7
% 
rated_omega=12.1;
Drivetrain.LSSInertia = 5025500; % Use only for 5MW 
Drivetrain.Gearbox.Ratio = 97;

%rated omega in rpm at LSS
Kp=-2*Drivetrain.LSSInertia*rated_omega*natural_freq*damping_ratio*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);
Ki=-Drivetrain.LSSInertia*rated_omega*natural_freq^2*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);

save('5MW_gains_old', 'Kp', 'Ki', 'theta');
