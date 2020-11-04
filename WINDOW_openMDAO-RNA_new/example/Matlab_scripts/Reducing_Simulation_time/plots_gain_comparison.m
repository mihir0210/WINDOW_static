%% data
load('5MW_gains_old.mat');

Kp_old = Kp;
Ki_old = Ki;
theta_old = [0; 3.83; 6.6; 8.7; 10.45; 12.06; 13.54; 14.92; 16.23; 17.47; 18.70; 19.94; 21.18; 22.35; 23.47]';

load('5MW_gains_new.mat');

Kp_new = Kp;
Ki_new = Ki;
theta_new = [0; 3.83; 6.6; 8.7; 10.45; 12.06; 13.54; 14.92; 16.23; 17.47; 18.70; 19.94; 21.18; 22.35; 23.47]';





%% plot
%%%%%Kp %%%

figure(1)
plot(theta_old, -1*Kp_old, 'b-*'); hold on;
plot(theta_old, -1*Kp_new, 'r-*');


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
ylim([0 0.024]);
xlim([0 23.5]);

xlabel('\textbf{Blade collective pitch angle ($^\circ$)}','Interpreter','latex');
ylabel('\textbf{Proportional gain (-)}', 'Interpreter','latex');

legend('\textbf{Recommended parameters}','\textbf{Changed parameters}', 'Interpreter','latex');

figure(2)
plot(theta_old, -1*Ki_old, 'b-*'); hold on;
plot(theta_old, -1*Ki_new, 'r-*');


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

xlabel('\textbf{Blade collective pitch angle ($^\circ$)}','Interpreter','latex');
ylabel('\textbf{Integral gain (-)}', 'Interpreter','latex');

legend('\textbf{Recommended parameters}','\textbf{Changed parameters}', 'Interpreter','latex');

ylim([0 10]*1e-3);
xlim([0 23.5]);

