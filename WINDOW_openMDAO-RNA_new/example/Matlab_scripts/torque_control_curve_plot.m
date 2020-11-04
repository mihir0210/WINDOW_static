%%%%% torque control curve %%%%

%% determine points
load('NREL5MW (gain scheduled).mat');

%%%% gen rpm %%%
omega_points = [Control.Torque.SpeedA Control.Torque.SpeedB Control.Torque.SpeedB2 Control.Torque.SpeedC];

Control.Torque.OptGain = Control.Torque.OptGain*4*pi^2/60/60; %(rad/s)^2 to rpm^2

gain = Control.Torque.OptGain ;

gain= 0.0255764; % from the 5MW pdf



torque_A =0;
torque_B = gain*Control.Torque.SpeedB^2; 
torque_B2 = gain*Control.Torque.SpeedB2^2; 
torque_C = Control.Torque.Demanded; 

torque_points = [torque_A, torque_B, torque_B2, torque_C];

rpm_region2 = Control.Torque.SpeedB:5:Control.Torque.SpeedB2;
torque_region2 = gain*rpm_region2.^2;
rpm_region3 = Control.Torque.SpeedC:5:1400;
torque_region3 = 5*10^6./(rpm_region3*2*pi/60)/0.944;


rpm_plot = [Control.Torque.SpeedA rpm_region2 Control.Torque.SpeedC rpm_region3];
torque_plot = [torque_A, torque_region2, torque_C, torque_region3]; 

rpm_opt = 0:5:1400;
torque_opt = gain*rpm_opt.^2; 


plot(rpm_plot, torque_plot,'b-', 'LineWidth', 0.8); hold on;
plot(rpm_opt, torque_opt, 'K--', 'LineWidth', 0.8);
line([Control.Torque.SpeedA Control.Torque.SpeedA],[0 50000], 'LineWidth', 0.7, 'Color', 'r');
line([Control.Torque.SpeedB Control.Torque.SpeedB],[0 50000], 'LineWidth', 0.7, 'Color', 'r');
line([Control.Torque.SpeedB2 Control.Torque.SpeedB2],[0 50000], 'LineWidth', 0.7, 'Color', 'r');
line([Control.Torque.SpeedC Control.Torque.SpeedC],[0 50000], 'LineWidth', 0.7, 'Color', 'r');

dim1 = [.4 .45 .3 .3];
str1 = '1';
annotation('textbox',dim1,'String',str1,'FitBoxToText','on');

dim2 = [.51 .45 .3 .3];
str2 = '1 1/2';
annotation('textbox',dim2,'String',str2,'FitBoxToText','on');

dim3 = [.63 .45 .3 .3];
str3 = '2';
annotation('textbox',dim3,'String',str3,'FitBoxToText','on');

dim4 = [.7 .55 .3 .3];
str4 = '2 1/2';
annotation('textbox',dim4,'String',str4,'FitBoxToText','on');

dim5 = [.82 .45 .3 .3];
str5 = '3';
annotation('textbox',dim5,'String',str5,'FitBoxToText','on');

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


xlim([0 1400]);
ylim([0 50000]);
ylabel('\textbf{Generator Torque (Nm)}','Interpreter','latex');
xlabel('\textbf{Generator speed (rpm)}','Interpreter','latex');
