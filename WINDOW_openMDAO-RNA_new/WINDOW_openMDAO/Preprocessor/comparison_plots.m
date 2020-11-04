%%% plot 5 MW, Brian and my values %%%5
%% brian's values
x=[0 0.0065 0.00976 0.013 0.022 0.111 0.146 0.1667 0.195 0.233 0.276 0.333 0.4 0.4333...
    0.5 0.567 0.63 0.73 0.833 0.933 0.977 1];
EI_flap_brian = [2.338e10, 2.383e10, 2.437e10, 2.32e10, 1.629e10, 1.224e10, 6.122e9, 4.908e9, 4.39e9, 4.1e9,...
    3.564e9, 2.944e9, 1.981e9, 1.587e9, 1.301e9, 7.378e8, 5.843e8, 2.541e8, 1.22e8, 3.814e7,7.697e6, 3.66e6];
EI_edge_brian = [2.323e10, 2.383e10, 2.383e10, 2.27e10, 1.583e10, 9.69e9, 4.835e9, 5.069e9, 5.158e9, 5.21e9, 5.025e9, 4.441e9, 3.671e9, 3.234e9, 2.599e9, 2e9, 1.564e9, 9.227e8,...
    5.823e8, 3.029e8, 9.486e7, 4.69e7];
mass_brian = [1128, 1141, 1141, 1085, 859, 548.1, 340.5, 337.3, 336.3, 336.3, 330.2, 316, 268.2, 255.4, 237.1, 212.2, 194.5, 136.4, 105.7, 75.46, 40.25, 26.98];

load('Internal_layup.mat');
load('Preprocessor.mat'); 
load('NREL5MW (gain scheduled).mat','Blade');
%span_radius = span_radius;
Blade.Radius= Blade.Radius-1.5;

%% plot flapwise against 5 MW
semilogy(span_radius/span_radius(end),EI_flap, '-o');
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.EIflap, '-');
semilogy(x, EI_flap_brian,'-*');
ylabel('FlapStiff ($Nm^2$)','Interpreter','latex');
xlabel('Spanwise location');
grid on;
legend('Analytical', '5 MW', 'SANDIA labs');

%% plot edgewise against 5 MW
semilogy(span_radius/span_radius(end),EI_edge, '-o');
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.EIedge, '-');
semilogy(x, EI_edge_brian,'-*');
ylabel('EdgeStiff ($Nm^2$)','Interpreter','latex');
xlabel('Spanwise location');
grid on;
legend('Analytical', '5 MW', 'SANDIA labs');

%% plot torsional stiffness 
semilogy(span_radius/span_radius(end),G_stiffness, '-o');
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
semilogy(span_radius/span_radius(end),M_L, '-o');
hold on;
semilogy(Blade.Radius/Blade.Radius(end), Blade.Mass, '-');
semilogy(x, mass_brian,'-*');
ylabel('BMassDens ($\frac{kg}{m}$)','Interpreter','latex');
xlabel('Spanwise location');
grid on;
legend('Analytical', '5 MW', 'SANDIA labs');
