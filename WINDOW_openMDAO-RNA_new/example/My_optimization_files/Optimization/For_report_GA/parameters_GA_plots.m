%% Plots for GA parameters
penalty = fliplr([15 10 5 5 2 2 1 1 0.5 0.5]);
LCOE = fliplr([8.413 8.403 8.37 8.396 8.390 8.376 8.375 8.364 8.370 8.38]);
deflection = fliplr([ 6.35 6.45 6.69 6.92 6.55 6.82 6.78 6.77 6.94 6.7]);

%% plot penalty vs LCOE

semilogx(penalty, LCOE,'bo','MarkerSize',5);
a=char(8364);
  
grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.7)
set(gca,'TickDir','out');

ylabel('LCOE (Euro cents/kWh)','Interpreter','latex');
xlabel('Penalty coefficient (-)','Interpreter','latex');

xticks([0.5 1 2 5 10 15]);
xticklabels({'0.5','1', '2', '5', '10', '15'});
xlim([0.4 20]);

%legend('Starting point 1', 'Starting point 2','Interpreter','latex'); 

%% plot penalty vs deflection

semilogx(penalty, deflection,'ro','MarkerSize',5);

  
grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.7)
set(gca,'TickDir','out');

ylabel('Deflection (m)','Interpreter','latex');
xlabel('Penalty coefficient (-)','Interpreter','latex');

xticks([0.5 1 2 5 10 15]);
xticklabels({'0.5','1', '2', '5', '10', '15'});
xlim([0.4 20]);
ylim([6 7.2]);



%% comparing chord and twist for pop size 20 and 50

load('GA_20_opt.mat');
chord_profile_20_opt = cell2mat(Chord_profile);
twist_profile_20_opt = Twist_profile + 2.46;

points_chord_20_opt = [chord_profile_20_opt(1:7:end), chord_profile_20_opt(end)];
points_twist_20_opt = [twist_profile_20_opt(1:7:end), twist_profile_20_opt(end)];



load('GA_50_opt.mat');

chord_profile_50_opt = cell2mat(Chord_profile);
twist_profile_50_opt = Twist_profile + 2.22;

points_chord_50_opt = [chord_profile_50_opt(1:7:end), chord_profile_50_opt(end)] ;
points_twist_50_opt = [twist_profile_50_opt(1:7:end), twist_profile_50_opt(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];


%% plot chord values for 20 and 50
plot(normalized_radius, chord_profile_20_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_50_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_20_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_50_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Population size:20', 'Population size:50','Interpreter','latex'); 

%% plot twist values for 20 and 50
plot(normalized_radius, twist_profile_20_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_50_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_20_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_50_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Population size:20', 'Population size:50','Interpreter','latex'); 
ylim([-2 15]);


%% plot chord and twist for all 3 mutation cases

load('GA_20_opt.mat');
chord_profile_case1 = cell2mat(Chord_profile);
twist_profile_case1 = Twist_profile +2.46;

points_chord_case1 = [chord_profile_case1(1:7:end), chord_profile_case1(end)];
points_twist_case1 = [twist_profile_case1(1:7:end), twist_profile_case1(end)];

load('GA_mutation0.5_opt.mat');
chord_profile_case2 = cell2mat(Chord_profile);
twist_profile_case2 = Twist_profile+2.34;

points_chord_case2 = [chord_profile_case2(1:7:end), chord_profile_case2(end)];
points_twist_case2 = [twist_profile_case2(1:7:end), twist_profile_case2(end)];


load('GA_mutation1_opt.mat');
chord_profile_case3 = cell2mat(Chord_profile);
twist_profile_case3 = Twist_profile+2.34;

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
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Case 1', 'Case 2','Case 3','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_case1, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_case2, 'r-', 'LineWidth', 0.8);
plot(normalized_radius, twist_profile_case3, 'g-', 'LineWidth', 0.8);
plot(points_radius, points_twist_case1, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_case2, 'r*', 'MarkerSize',4);
plot(points_radius, points_twist_case3, 'g*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Case 1', 'Case 2','Case 3','Interpreter','latex'); 
ylim([0 17]);


