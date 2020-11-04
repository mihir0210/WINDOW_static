%% data
tsr = xlsread('Response.xlsx','TSR','B3:B12'); 
stress_dynamic = xlsread('Response.xlsx','TSR', 'K3:K12');
lcoe = xlsread('Response.xlsx','TSR', 'C3:C12');
td_dynamic = xlsread('Response.xlsx','TSR', 'J3:J12');
td_static = xlsread('Response.xlsx','TSR', 'E3:E12');
stress_static = xlsread('Response.xlsx','TSR', 'F3:F12');


% %% curve fit
% a=polyfit(tsr,stress, 3);
% tsr_new = 6.5:0.1:8.5;
% stress_new = a(1)*tsr_new.^3+a(2)*tsr_new.^2 + a(3)*tsr_new + a(4);

%% plot


plot(tsr,stress_dynamic,'b-*');  hold on; 

plot(tsr,stress_static,'r-*'); 



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
set(gca,'GridLineStyle','--');
set(gca,'GridAlpha',0.8);
set(gca,'TickDir','out');

set(gca,'ycolor','k') 
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

ylabel('\textbf{Flapwise stress in Spar caps (MPa)}','Interpreter','latex');
legend('\textbf{Dynamic model}', '\textbf{Static model}','Interpreter','latex');

xlabel('\textbf{TSR ($\lambda$)}','Interpreter','latex');
xlim([6.2 9]);
ylim([400 850]);



%% plot tip deflection
plot(tsr,td_dynamic,'b-*'); hold on; 
plot(tsr,td_static,'r-*');  



set(gca,'ycolor','k')




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
set(gca,'GridLineStyle','--');
set(gca,'GridAlpha',0.8);
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';
ylabel('\textbf{Tip deflection (m)}','Interpreter','latex');


legend('\textbf{Dynamic model}', '\textbf{Static model}','Interpreter','latex');

xlabel('\textbf{TSR ($\lambda$)}','Interpreter','latex');

ylim([5 9]);
xlim([6.3 8.7]);
%% plot lcoe

plot(tsr,lcoe/8.934,'b*'); hold on; 
plot(tsr,lcoe/8.934,'k-'); 

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
set(gca,'GridLineStyle','--');
set(gca,'GridAlpha',0.8);
set(gca,'TickDir','out');

axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

ylabel('\textbf{Normalized LCOE (-)}','Interpreter','latex');


xlabel('\textbf{TSR ($\lambda$)}','Interpreter','latex');
xlim([6.2 9]);
ylim([0.98 1.04]);


