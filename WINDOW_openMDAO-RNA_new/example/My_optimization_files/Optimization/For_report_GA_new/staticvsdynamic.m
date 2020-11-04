%% Compare chord and twist for GA static and GA dynamic
load('GA_mutation0.5_opt.mat');
chord_profile_case3 = cell2mat(Chord_profile);
twist_profile_case3 = Twist_profile+2.774201605;

points_chord_case3 = [chord_profile_case3(1:7:end), chord_profile_case3(end)];
points_twist_case3 = [twist_profile_case3(1:7:end), twist_profile_case3(end)];

load('dynamic_GA_opt.mat');
chord_profile_dynamicGA = cell2mat(Chord_profile);
twist_profile_dynamicGA = Twist_profile+ 1.17744515;

points_chord_dynamicGA = [chord_profile_dynamicGA(1:7:end), chord_profile_dynamicGA(end)];
points_twist_dynamicGA = [twist_profile_dynamicGA(1:7:end), twist_profile_dynamicGA(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_case3, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_dynamicGA, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_case3, 'b*', 'MarkerSize',4);
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
legend('\textbf{Static model}', '\textbf{Dynamic model}','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_case3, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_dynamicGA, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_case3, 'b*', 'MarkerSize',4);
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
legend('\textbf{Static model}', '\textbf{Dynamic model}','Interpreter','latex'); 
ylim([0 20]);


%% plot flapwise and edgewise moment for the static and dynamic design
load('DLC1.3_static_opt.mat');

flapwise_moment_static = RootMFlp1;
edgewise_moment_static = RootMEdg1;
rotor_thrust_static = RotThrust;

deflection_static = 1.1*OoPDefl1;

load('DLC1.3_dynamic_opt.mat');

flapwise_moment_dynamic = RootMFlp1;
edgewise_moment_dynamic = RootMEdg1;
rotor_thrust_dynamic = RotThrust;

deflection_dynamic = 1.1*OoPDefl1;


figure(1)
plot(Time,deflection_static, 'b-'); hold on;
plot(Time, deflection_dynamic,'r-');

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

ylim([1.5 7.5])




%ax.GridAlpha = 1;
ylabel('\textbf{Tip deflection (m)}','Interpreter','latex');
xlabel('\textbf{Simulation time (s)}','Interpreter','latex');
legend('\textbf{Static$_{opt}$}', '\textbf{Dynamic$_{opt}$}','Interpreter','latex'); 

figure(2)
plot(Time,flapwise_moment_static, 'b-'); hold on;
plot(Time,flapwise_moment_dynamic,'r-');

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


%ax.GridAlpha = 1;
ylabel('Root Flapwise Moment (kNm)','Interpreter','latex');
xlabel('Simulation time (s)','Interpreter','latex');
legend('Static$_{opt}$', '$Dynamic$_{opt}$','Interpreter','latex'); 

figure(3)
plot(Time,rotor_thrust_static, 'b-'); hold on;
plot(Time,rotor_thrust_dynamic,'r-');


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
ylabel('\textbf{Rotor Thrust (kN)}','Interpreter','latex');
xlabel('\textbf{Simulation time (s)}','Interpreter','latex');
legend('\textbf{Static$_{opt}$}', '\textbf{Dynamic$_{opt}$}','Interpreter','latex'); 

ylim([500 850])

figure(4)
plot(Time,edgewise_moment_static, 'b-'); hold on;
plot(Time,edgewise_moment_dynamic,'r-');

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


%ax.GridAlpha = 1;
ylabel('Root Edgewise Moment (kNm)','Interpreter','latex');
xlabel('Simulation time (s)','Interpreter','latex');
legend('Static$_{opt}$', 'Dynamic$_{opt}$','Interpreter','latex'); 
