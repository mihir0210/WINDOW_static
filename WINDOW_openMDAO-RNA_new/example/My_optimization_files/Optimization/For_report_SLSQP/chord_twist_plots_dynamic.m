%%%% Chord and Twist distribution plotting for comparison of optimum points%%%%

load('dynamic_sp1_init.mat');

chord_profile_sp1_init = cell2mat(Chord_profile);
twist_profile_sp1_init = Twist_profile+0.098;

points_chord_sp1_init = [chord_profile_sp1_init(1:7:end), chord_profile_sp1_init(end)] ;
points_twist_sp1_init = [twist_profile_sp1_init(1:7:end), twist_profile_sp1_init(end)];

load('dynamic_sp2_init.mat');

chord_profile_sp2_init = cell2mat(Chord_profile);
twist_profile_sp2_init = Twist_profile+2.28;

points_chord_sp2_init = [chord_profile_sp2_init(1:7:end), chord_profile_sp2_init(end)] ;
points_twist_sp2_init = [twist_profile_sp2_init(1:7:end), twist_profile_sp2_init(end)];



load('dynamic_sp1_opt.mat');
chord_profile_sp1_opt = cell2mat(Chord_profile);
twist_profile_sp1_opt = Twist_profile+0.82;

points_chord_sp1_opt = [chord_profile_sp1_opt(1:7:end), chord_profile_sp1_opt(end)];
points_twist_sp1_opt = [twist_profile_sp1_opt(1:7:end), twist_profile_sp1_opt(end)];



load('dynamic_sp2_opt.mat');

chord_profile_sp2_opt = cell2mat(Chord_profile);
twist_profile_sp2_opt = Twist_profile+2.13;

points_chord_sp2_opt = [chord_profile_sp2_opt(1:7:end), chord_profile_sp2_opt(end)] ;
points_twist_sp2_opt = [twist_profile_sp2_opt(1:7:end), twist_profile_sp2_opt(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];




%% plot comparing chord : starting point1 results for dynamic SLSQP
plot(normalized_radius, chord_profile_sp1_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_sp1_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp1_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_sp1_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 



%% plot comparing chord : starting point2 results for dynamic SLSQP
plot(normalized_radius, chord_profile_sp2_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_sp2_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp2_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_sp2_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 




%% plot comparing chord: 2 optimums for dynamic SLSQP
plot(normalized_radius, chord_profile_sp1_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_sp2_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp1_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_sp2_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Starting point 1', 'Starting point 2','Interpreter','latex'); 


%% plot comparing twist : starting point1 results for dynamic SLSQP
plot(normalized_radius, twist_profile_sp1_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_sp1_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp1_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_sp1_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 
ylim([-2 15]);


%% plot comparing twist : starting point2 results for dynamic SLSQP
plot(normalized_radius, twist_profile_sp2_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_sp2_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp2_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_sp2_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 
ylim([-2 15]);

%% plot comparing twist : 2 optimums for dynamic SLSQP

plot(normalized_radius, twist_profile_sp1_opt, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_sp2_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp1_opt, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_sp2_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Starting point 1', 'Starting point 2','Interpreter','latex'); 
ylim([-2 15]);


%% For starting point 3


load('dynamic_sp3_init.mat');

chord_profile_sp3_init = cell2mat(Chord_profile);
twist_profile_sp3_init = Twist_profile+0.035;

points_chord_sp3_init = [chord_profile_sp3_init(1:7:end), chord_profile_sp3_init(end)] ;
points_twist_sp3_init = [twist_profile_sp3_init(1:7:end), twist_profile_sp3_init(end)];

load('dynamic_sp3_opt.mat');

chord_profile_sp3_opt = cell2mat(Chord_profile);
twist_profile_sp3_opt = Twist_profile+ 0.004;

points_chord_sp3_opt = [chord_profile_sp3_opt(1:7:end), chord_profile_sp3_opt(end)] ;
points_twist_sp3_opt = [twist_profile_sp3_opt(1:7:end), twist_profile_sp3_opt(end)];

normalized_radius = Blade_radius/63;
points_radius = [normalized_radius(1:7:end), normalized_radius(end)];

figure(1)
plot(normalized_radius, chord_profile_sp3_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, chord_profile_sp3_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_chord_sp3_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_chord_sp3_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Chord distribution (m)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 

figure(2)
plot(normalized_radius, twist_profile_sp3_init, 'b-', 'LineWidth', 0.8); hold on;
plot(normalized_radius, twist_profile_sp3_opt, 'r-', 'LineWidth', 0.8);
plot(points_radius, points_twist_sp3_init, 'b*', 'MarkerSize',4);
plot(points_radius, points_twist_sp3_opt, 'r*', 'MarkerSize',4);

grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');

%ax.GridAlpha = 1;
ylabel('Twist distribution ($^\circ$)','Interpreter','latex');
xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 
ylim([-2 18]);



