%%%% plot aero power sensitivity and gains %%%


%% 5 MW turbine aero sensitivity

aero_sensitivity = -1*[28.24e6; 43.73e6; 51.66e6; 58.44e6; 64.44e6; 70.46e6; 76.53e6; 83.94e6;
    90.67e6; 94.71e6; 99.04e6; 105.9e6; 114.30e6; 120.20e6; 125.3e6]; 


theta = [0; 3.83; 6.6; 8.7; 10.45; 12.06; 13.54; 14.92; 16.23; 17.47; 18.70; 19.94; 21.18; 22.35; 23.47];
%% Gains
c=polyfit(theta, aero_sensitivity,1);

% I=find(WindSpeeds==rated_windspeed);
% theta_new = Lin.Pitch(I:end);

% theta_new = theta;


aero_sensitivity_new=c(1)*theta+c(2);



%% plot aero sensitivity
plot(theta, aero_sensitivity, 'b*', 'MarkerSize',5); hold on;
plot(theta, aero_sensitivity_new, 'k-', 'LineWidth', 0.8); 

grid on
    a = gca;
    % set box property to off and remove background color
    set(a,'box','off','color','none')
    % create new, empty axes with box but without ticks
    b = axes('Position',get(a,'Position'),'box','on','xtick',[],'ytick',[]);
    % set original axes as active
    axes(a)
    % link axes in case of zooming
    linkaxes([a b])
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

%ax.GridAlpha = 1;
ylabel('\textbf{Aerodynamic power sensitivity \bigg($\frac{W}{rad}$\bigg)}','Interpreter','latex');
xlabel('\textbf{Collective blade pitch angle ($^\circ$)}','Interpreter','latex');
legend('\textbf{Original data}', '\textbf{Best fit line}','Interpreter','latex');
xlim([0 23.5]);

%% gains
%value of theta at which aerodynamic power sensitivity doubled from intial
%value, the value at first pitch angle

theta_k=(2*aero_sensitivity_new(1)-c(2))/c(1);
GK=1./(1+theta/theta_k);

% %recommended values of natural_freq and damping ratio
% %(http://orbit.dtu.dk/files/7710881/ris_r_1500.pdf)
natural_freq=0.6; %rad/s
damping_ratio=0.7; %range 0.6-0.7
% % 
% rated_omega=12.1;
Drivetrain.LSSInertia = 5025500; % Use only for 5MW 
Drivetrain.Gearbox.Ratio = 97;
% 
rated_omega = 12.1; 
%rated omega in rpm at LSS
Kp=-2*Drivetrain.LSSInertia*rated_omega*natural_freq*damping_ratio*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);
Ki=-Drivetrain.LSSInertia*rated_omega*natural_freq^2*GK./(Drivetrain.Gearbox.Ratio*aero_sensitivity_new(1)*-1);

%% plot gains 

plot(theta, -Kp, 'LineWidth', 1); hold on;
plot(theta, -Ki, 'LineWidth', 1); 

grid on
    a = gca;
    % set box property to off and remove background color
    set(a,'box','off','color','none')
    % create new, empty axes with box but without ticks
    b = axes('Position',get(a,'Position'),'box','on','xtick',[],'ytick',[]);
    % set original axes as active
    axes(a)
    % link axes in case of zooming
    linkaxes([a b])
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

%ax.GridAlpha = 1;
ylabel('\textbf{Controller gains}','Interpreter','latex');
xlabel('\textbf{Collective blade pitch angle ($^\circ$)}','Interpreter','latex');
legend('\textbf{Proportional gain}', '\textbf{Integral gain}','Interpreter','latex');
xlim([0 23.5]);
ylim([0 0.025]);