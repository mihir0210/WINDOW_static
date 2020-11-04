%%% plot 5 MW, Brian and my values %%%5
%% brian's values
x=[0 0.0065  0.111 0.146 0.1667 0.195 0.233 0.276 0.333 0.4 0.4333...
    0.5 0.567 0.63 0.73 0.833 0.933 0.977 1];
EI_flap_brian = [2.338e10, 2.437e10, 1.224e10, 6.122e9, 4.908e9, 4.39e9, 4.1e9,...
    3.564e9, 2.944e9, 1.981e9, 1.587e9, 1.301e9, 7.378e8, 5.843e8, 2.541e8, 1.22e8, 3.814e7,7.697e6, 3.66e6];
EI_edge_brian = [2.323e10, 2.383e10, 9.69e9, 4.835e9, 5.069e9, 5.158e9, 5.21e9, 5.025e9, 4.441e9, 3.671e9, 3.234e9, 2.599e9, 2e9, 1.564e9, 9.227e8,...
    5.823e8, 3.029e8, 9.486e7, 4.69e7];

mass_brian = [1128, 1141, 548.1, 340.5, 337.3, 336.3, 336.3, 330.2, 316, 268.2, 255.4, 237.1, 212.2, 194.5, 136.4, 105.7, 75.46, 40.25, 26.98];

load('Internal_layup.mat');
load('Preprocessor.mat'); 
load('NREL5MW (gain scheduled).mat','Blade');
Blade.EIflap(46) = 2.384e7;
Blade.EIflap(47) = 1.1e7;
Blade.EIflap(48) = 0.755e7;
Blade.EIflap(49) = 0.17e6;

Blade.EIedge(46)= 26.17e7;
Blade.EIedge(47)= 13e7;
Blade.EIedge(48)= 8.5e7;
Blade.EIedge(49)= 5.01e6;




%span_radius = span_radius;
Blade.Radius= Blade.Radius-1.5;

points_EI_flap = [EI_flap(1:4:end), EI_flap(end)] ;
points_EI_edge = [EI_edge(1:4:end), EI_edge(end)] ;
points_mass = [M_L(1:4:end), M_L(end)] ;
points_radius = [span_radius(1:4:end), span_radius(end)];

points_NREL_flap = [Blade.EIflap(1:4:end)', Blade.EIflap(end')] ;
points_NREL_edge = [Blade.EIedge(1:4:end)', Blade.EIedge(end)'] ;
points_NREL_mass = [Blade.Mass(1:4:end)', Blade.Mass(end)'] ;
points_NREL_radius = [Blade.Radius(1:4:end)', Blade.Radius(end)'] ;

%% plot flapwise against 5 MW

semilogy(Blade.Radius/61.5,EI_flap,'LineWidth', 0.8);
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.EIflap, 'LineWidth', 0.8);
semilogy(x, EI_flap_brian, 'LineWidth', 0.8);

%semilogy(points_radius/61.5, points_EI_flap, 'o','MarkerSize',4);
%semilogy(points_NREL_radius/61.5, points_NREL_flap, 'o','MarkerSize',4);
%semilogy(x, EI_flap_brian, 'o','MarkerSize',4);




grid on; 

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

ylabel('\textbf{FlapStiff ($Nm^2$)}','Interpreter','latex');
xlabel('\textbf{Spanwise location}','Interpreter','latex');

legend('\textbf{ESP}', '\textbf{5 MW}', '\textbf{SANDIA}', 'Interpreter','latex' );

%% plot edgewise against 5 MW
semilogy(Blade.Radius/61.5,EI_edge, 'LineWidth', 0.8);
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.EIedge, 'LineWidth', 0.8);
semilogy(x, EI_edge_brian,'LineWidth', 0.8);
ylabel('EdgeStiff ($Nm^2$)','Interpreter','latex');
xlabel('Spanwise location','Interpreter','latex');
grid on; 

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
ylabel('\textbf{EdgeStiff ($Nm^2$)}','Interpreter','latex');
xlabel('\textbf{Spanwise location}','Interpreter','latex');
legend('\textbf{ESP}', '\textbf{5 MW}', '\textbf{SANDIA}', 'Interpreter','latex' );

%% plot torsional stiffness 
semilogy(span_radius/61.5,G_stiffness, '-o');
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.GJ, '-');
%semilogy(x, EI_edge_brian,'-*');
ylabel('EdgeStiff ($Nm^2$)','Interpreter','latex');
xlabel('Spanwise location');
grid on;
legend('Analytical', '5 MW', 'SANDIA labs');

%% plot axial stiffness
semilogy(span_radius/span_radius(end),EA, '-o');
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.EA, '-');
%semilogy(x, EI_edge_brian,'-*');
ylabel('EdgeStiff ($Nm^2$)','Interpreter','latex');
xlabel('Spanwise location');
grid on;
legend('Analytical', '5 MW', 'SANDIA labs');

%% plot mass against 5 MW
semilogy(Blade.Radius/61.5,M_L, 'LineWidth', 0.8);
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.Mass, 'LineWidth', 0.8);
semilogy(x, mass_brian, 'LineWidth', 0.8);


grid on; 

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
ylabel('\textbf{BMassDens ($\frac{kg}{m}$)}','Interpreter','latex');
xlabel('\textbf{Spanwise location}','Interpreter','latex');
legend('\textbf{ESP}', '\textbf{5 MW}', '\textbf{SANDIA}', 'Interpreter','latex' );
