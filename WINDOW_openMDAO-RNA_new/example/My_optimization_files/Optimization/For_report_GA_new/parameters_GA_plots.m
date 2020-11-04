%% Plots for GA parameters
penalty = fliplr([15 10 5 5 2 2 1 1 0.5 0.5]);
LCOE = fliplr([8.413 8.403 8.37 8.396 8.390 8.376 8.375 8.364 8.370 8.38]/8.413);
deflection = fliplr([ 6.35 6.45 6.69 6.92 6.55 6.82 6.78 6.77 6.94 6.7]/7.07);

%% plot penalty vs LCOE

semilogx(penalty, LCOE,'bo','MarkerSize',8);
%a=char(8364);
  
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
set(gca,'GridAlpha',0.7)
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

ylabel('\textbf{LCOE (Euro cents/kWh)}','Interpreter','latex');
xlabel('\textbf{Penalty coefficient (-)}','Interpreter','latex');

xticks([0.5 1 2 5 10 15]);
xticklabels({'\textbf{0.5}','\textbf{1}', '\textbf{2}', '\textbf{5}', '\textbf{10}', '\textbf{15}'});
xlim([0.4 20]);
ylim([0.993 1.001])

%legend('Starting point 1', 'Starting point 2','Interpreter','latex'); 

%% plot penalty vs deflection

semilogx(penalty, deflection,'ro','MarkerSize',8);

  
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
set(gca,'GridAlpha',0.7)
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

ylabel('\textbf{Deflection (m)}','Interpreter','latex');
xlabel('\textbf{Penalty coefficient (-)}','Interpreter','latex');

xticks([0.5 1 2 5 10 15]);
xticklabels({'\textbf{0.5}','\textbf{1}', '\textbf{2}', '\textbf{5}', '\textbf{10}', '\textbf{15}'});
xlim([0.4 20]);
ylim([0.85 1]);



%% comparing chord and twist for pop size 20 and 40

load('GA_20_opt.mat');
chord_profile_20_opt = cell2mat(Chord_profile);
twist_profile_20_opt = Twist_profile + 2.338722575;

points_chord_20_opt = [chord_profile_20_opt(1:7:end), chord_profile_20_opt(end)];
points_twist_20_opt = [twist_profile_20_opt(1:7:end), twist_profile_20_opt(end)];



load('GA_40_opt.mat');

chord_profile_40_opt = cell2mat(Chord_profile);
twist_profile_40_opt = Twist_profile + 2.338722575;

points_chord_40_opt = [chord_profile_40_opt(1:7:end), chord_profile_40_opt(end)] ;
points_twist_40_opt = [twist_profile_40_opt(1:7:end), twist_profile_40_opt(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];


%% plot chord values for 20 and 40
plot(normalized_radius, chord_profile_20_opt, 'b-', 'LineWidth', 1); hold on;
plot(normalized_radius, chord_profile_40_opt, 'r-', 'LineWidth', 0.7);
plot(points_radius, points_chord_20_opt, 'b*', 'MarkerSize',5);
plot(points_radius, points_chord_40_opt, 'r*', 'MarkerSize',5);

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
legend('\textbf{Population size: 20}', '\textbf{Population size: 40}','Interpreter','latex'); 

%% plot twist values for 20 and 40
plot(normalized_radius, twist_profile_20_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_40_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_20_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_40_opt, 'r*', 'MarkerSize',4);

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
legend('\textbf{Population size: 20}', '\textbf{Population size: 40}','Interpreter','latex');
ylim([-2 19]);


%% plot chord and twist for all 3 mutation cases

load('GA_20_opt.mat');
chord_profile_case1 = cell2mat(Chord_profile);
twist_profile_case1 = Twist_profile +2.338722575;

points_chord_case1 = [chord_profile_case1(1:7:end), chord_profile_case1(end)];
points_twist_case1 = [twist_profile_case1(1:7:end), twist_profile_case1(end)];

load('GA_mutation0.5_opt.mat');
chord_profile_case2 = cell2mat(Chord_profile);
twist_profile_case2 = Twist_profile+2.774201605;

points_chord_case2 = [chord_profile_case2(1:7:end), chord_profile_case2(end)];
points_twist_case2 = [twist_profile_case2(1:7:end), twist_profile_case2(end)];


load('GA_mutation5_opt.mat');
chord_profile_case3 = cell2mat(Chord_profile);
twist_profile_case3 = Twist_profile+3.06452097;

points_chord_case3 = [chord_profile_case3(1:7:end), chord_profile_case3(end)];
points_twist_case3 = [twist_profile_case3(1:7:end), twist_profile_case3(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_case1, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_case2, 'r-', 'LineWidth', 0.8);
plot(normalized_radius, chord_profile_case3, 'g-', 'LineWidth', 0.8);
plot(points_radius, points_chord_case1, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_case2, 'r*', 'MarkerSize',4);
plot(points_radius, points_chord_case3, 'g*', 'MarkerSize',4);

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
legend('\textbf{Case 1}', '\textbf{Case 2}','\textbf{Case 3}','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_case1, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_case2, 'r-', 'LineWidth', 0.8);
plot(normalized_radius, twist_profile_case3, 'g-', 'LineWidth', 0.8);
plot(points_radius, points_twist_case1, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_case2, 'r*', 'MarkerSize',4);
plot(points_radius, points_twist_case3, 'g*', 'MarkerSize',4);

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
legend('\textbf{Case 1}', '\textbf{Case 2}','\textbf{Case 3}','Interpreter','latex'); 
ylim([0 18]);


