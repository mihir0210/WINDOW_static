%% Compare chord and twist for optimum for static from SLSQP and GA
load('static_sp2_opt.mat');

chord_profile_sp2_opt = cell2mat(Chord_profile);
twist_profile_sp2_opt = Twist_profile;

points_chord_sp2_opt = [chord_profile_sp2_opt(1:7:end), chord_profile_sp2_opt(end)] ;
points_twist_sp2_opt = [twist_profile_sp2_opt(1:7:end), twist_profile_sp2_opt(end)];

load('GA_mutation1_opt.mat');
chord_profile_case3 = cell2mat(Chord_profile);
twist_profile_case3 = Twist_profile;

points_chord_case3 = [chord_profile_case3(1:7:end), chord_profile_case3(end)];
points_twist_case3 = [twist_profile_case3(1:7:end), twist_profile_case3(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_sp2_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_case3, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp2_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_case3, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('SLSQP', 'GA','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_sp2_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_case3, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp2_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_case3, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('SLSQP', 'GA','Interpreter','latex'); 
ylim([-2 15]);


%% Compare chord and twist for optimum for dynamic from SLSQP and GA
load('dynamic_sp2_opt.mat');

chord_profile_sp2_opt = cell2mat(Chord_profile);
twist_profile_sp2_opt = Twist_profile;

points_chord_sp2_opt = [chord_profile_sp2_opt(1:7:end), chord_profile_sp2_opt(end)] ;
points_twist_sp2_opt = [twist_profile_sp2_opt(1:7:end), twist_profile_sp2_opt(end)];

load('GA_dynamic_opt.mat');

chord_profile_dynamicGA_opt = cell2mat(Chord_profile);
twist_profile_dynamicGA_opt = Twist_profile;

points_chord_dynamicGA_opt = [chord_profile_dynamicGA_opt(1:7:end), chord_profile_dynamicGA_opt(end)] ;
points_twist_dynamicGA_opt = [twist_profile_dynamicGA_opt(1:7:end), twist_profile_dynamicGA_opt(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(4)
plot(normalized_radius, chord_profile_sp2_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_dynamicGA_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp2_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_dynamicGA_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('SLSQP', 'GA','Interpreter','latex'); 

figure(5)
plot(normalized_radius, twist_profile_sp2_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_dynamicGA_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp2_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_dynamicGA_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('SLSQP', 'GA','Interpreter','latex'); 
ylim([-2 17]);