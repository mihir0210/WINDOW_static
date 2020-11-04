%%%% Plots for GA static and dynamic results compared against 5MW %%%%
%% Compare 5MW against static optimum
load('static_sp1_init.mat');

chord_profile_sp1_init = cell2mat(Chord_profile);
twist_profile_sp1_init = Twist_profile+0.098;

points_chord_sp1_init = [chord_profile_sp1_init(1:7:end), chord_profile_sp1_init(end)] ;
points_twist_sp1_init = [twist_profile_sp1_init(1:7:end), twist_profile_sp1_init(end)];

load('GA_mutation0.5_opt.mat');
chord_profile_case3 = cell2mat(Chord_profile);
twist_profile_case3 = Twist_profile+2.774201605;

points_chord_case3 = [chord_profile_case3(1:7:end), chord_profile_case3(end)];
points_twist_case3 = [twist_profile_case3(1:7:end), twist_profile_case3(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_sp1_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_case3, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp1_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_case3, 'r*', 'MarkerSize',4);

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
ylabel('\textbf{Chord distribution (m)}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');
legend('\textbf{NREL5MW}', '\textbf{Optimum design}','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_sp1_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_case3, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp1_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_case3, 'r*', 'MarkerSize',4);

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
ylabel('\textbf{Twist distribution ($^\circ$)}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');
legend('\textbf{NREL5MW}', '\textbf{Optimum design}','Interpreter','latex'); 
ylim([0 18]);






%% Compare 5MW against dynamic optimum
load('static_sp1_init.mat');

chord_profile_sp1_init = cell2mat(Chord_profile);
twist_profile_sp1_init = Twist_profile+0.098;

points_chord_sp1_init = [chord_profile_sp1_init(1:7:end), chord_profile_sp1_init(end)] ;
points_twist_sp1_init = [twist_profile_sp1_init(1:7:end), twist_profile_sp1_init(end)];


load('dynamic_GA_opt.mat');
chord_profile_dynamicGA = cell2mat(Chord_profile);
twist_profile_dynamicGA = Twist_profile+ 1.17744515;

points_chord_dynamicGA = [chord_profile_dynamicGA(1:7:end), chord_profile_dynamicGA(end)];
points_twist_dynamicGA = [twist_profile_dynamicGA(1:7:end), twist_profile_dynamicGA(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_sp1_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_dynamicGA, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp1_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_dynamicGA, 'r*', 'MarkerSize',4);

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
ylabel('\textbf{Chord distribution (m)}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');
legend('\textbf{NREL5MW}', '\textbf{Optimum design}','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_sp1_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_dynamicGA, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp1_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_dynamicGA, 'r*', 'MarkerSize',4);

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
ylabel('\textbf{Twist distribution ($^\circ$)}','Interpreter','latex');
xlabel('\textbf{Normalized blade radius (-)}','Interpreter','latex');
legend('\textbf{NREL5MW}', '\textbf{Optimum design}','Interpreter','latex'); 
ylim([0 20]);