%%% Plots chord and twist for all design configurations on the same plot


load('static_sp2_opt.mat');

chord_profile_static_slsqp = cell2mat(Chord_profile);
twist_profile_static_slsqp = Twist_profile +2.15;

points_chord_static_slsqp = [chord_profile_static_slsqp(1:7:end), chord_profile_static_slsqp(end)] ;
points_twist_static_slsqp = [twist_profile_static_slsqp(1:7:end), twist_profile_static_slsqp(end)];

load('GA_mutation1_opt.mat');
chord_profile_static_ga = cell2mat(Chord_profile);
twist_profile_static_ga = Twist_profile +2.34;

points_chord_static_ga = [chord_profile_static_ga(1:7:end), chord_profile_static_ga(end)];
points_twist_static_ga = [twist_profile_static_ga(1:7:end), twist_profile_static_ga(end)];


load('dynamic_sp2_opt.mat');

chord_profile_dynamic_slsqp = cell2mat(Chord_profile);
twist_profile_dynamic_slsqp = Twist_profile +2.13;

points_chord_dynamic_slsqp = [chord_profile_dynamic_slsqp(1:7:end), chord_profile_dynamic_slsqp(end)] ;
points_twist_dynamic_slsqp = [twist_profile_dynamic_slsqp(1:7:end), twist_profile_dynamic_slsqp(end)];

load('GA_dynamic_opt.mat');

chord_profile_dynamic_ga = cell2mat(Chord_profile);
twist_profile_dynamic_ga = Twist_profile+2.22;

points_chord_dynamic_ga = [chord_profile_dynamic_ga(1:7:end), chord_profile_dynamic_ga(end)] ;
points_twist_dynamic_ga = [twist_profile_dynamic_ga(1:7:end), twist_profile_dynamic_ga(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_static_slsqp, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_static_ga, 'r-', 'LineWidth', 0.8);
plot(normalized_radius, chord_profile_dynamic_slsqp, 'k-', 'LineWidth', 0.8); 
plot(normalized_radius, chord_profile_dynamic_ga, 'g-', 'LineWidth', 0.8);



plot(points_radius, points_chord_static_slsqp, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_static_ga, 'r*', 'MarkerSize',4);
plot(points_radius, points_chord_dynamic_slsqp, 'k*', 'MarkerSize',4); 
plot(points_radius, points_chord_dynamic_ga, 'g*', 'MarkerSize',4);


grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Static SLSQP', 'Static GA','Dynamic SLSQP','Dynamic GA','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_static_slsqp, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_static_ga, 'r-', 'LineWidth', 0.8);
plot(normalized_radius, twist_profile_dynamic_slsqp, 'k-', 'LineWidth', 0.8); 
plot(normalized_radius, twist_profile_dynamic_ga, 'g-', 'LineWidth', 0.8);



plot(points_radius, points_twist_static_slsqp, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_static_ga, 'r*', 'MarkerSize',4);
plot(points_radius, points_twist_dynamic_slsqp, 'k*', 'MarkerSize',4); 
plot(points_radius, points_twist_dynamic_ga, 'g*', 'MarkerSize',4);


grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Static SLSQP', 'Static GA','Dynamic SLSQP','Dynamic GA','Interpreter','latex'); 