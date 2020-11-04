%% Compare chord and twist for GA static and GA dynamic
load('GA_mutation1_opt.mat');

chord_profile_static_opt = cell2mat(Chord_profile);
twist_profile_static_opt = Twist_profile+2.34;

points_chord_static_opt = [chord_profile_static_opt(1:7:end), chord_profile_static_opt(end)] ;
points_twist_static_opt = [twist_profile_static_opt(1:7:end), twist_profile_static_opt(end)];

load('GA_dynamic_opt.mat');

chord_profile_dynamic_opt = cell2mat(Chord_profile);
twist_profile_dynamic_opt = Twist_profile+2.22;

points_chord_dynamic_opt = [chord_profile_dynamic_opt(1:7:end), chord_profile_dynamic_opt(end)] ;
points_twist_dynamic_opt = [twist_profile_dynamic_opt(1:7:end), twist_profile_dynamic_opt(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_static_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_dynamic_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_static_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_dynamic_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Design : Static model', 'Design : Dynamic model','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_static_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_dynamic_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_static_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_dynamic_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Design : Static model', 'Design : Dynamic model','Interpreter','latex'); 
ylim([0 18]);


%% plot flapwise and edgewise moment for the static and dynamic design
load('DLC1.3_static_opt.mat');

flapwise_moment_static = RootMFlp1;
edgewise_moment_static = RootMEdg1;
rotor_thrust_static = RotThrust;

deflection_static = OoPDefl2;

load('DLC1.3_dynamic_opt.mat');

flapwise_moment_dynamic = RootMFlp1;
edgewise_moment_dynamic = RootMEdg1;
rotor_thrust_dynamic = RotThrust;

deflection_dynamic = OoPDefl2;


figure(1)
plot(Time,deflection_static, 'b-'); hold on;
plot(Time, deflection_dynamic,'r-');

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
ylim([1.5 6.5])


%ax.GridAlpha = 1;
ylabel('Tip deflection (m)','Interpreter','latex');
xlabel('Simulation time (s)','Interpreter','latex');
legend('Design : Static model', 'Design : Dynamic model','Interpreter','latex'); 

figure(2)
plot(Time,flapwise_moment_static, 'b-'); hold on;
plot(Time,flapwise_moment_dynamic,'r-');

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');


%ax.GridAlpha = 1;
ylabel('Root Flapwise Moment (kNm)','Interpreter','latex');
xlabel('Simulation time (s)','Interpreter','latex');
legend('Design : Static model', 'Design : Dynamic model','Interpreter','latex'); 

figure(3)
plot(Time,rotor_thrust_static, 'b-'); hold on;
plot(Time,rotor_thrust_dynamic,'r-');


grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');


%ax.GridAlpha = 1;
ylabel('Rotor Thrust (kN)','Interpreter','latex');
xlabel('Simulation time (s)','Interpreter','latex');
legend('Design : Static model', 'Design : Dynamic model','Interpreter','latex'); 

ylim([500 850])

figure(4)
plot(Time,edgewise_moment_static, 'b-'); hold on;
plot(Time,edgewise_moment_dynamic,'r-');

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');


%ax.GridAlpha = 1;
ylabel('Root Edgewise Moment (kNm)','Interpreter','latex');
xlabel('Simulation time (s)','Interpreter','latex');
legend('Design : Static model', 'Design : Dynamic model','Interpreter','latex'); 
