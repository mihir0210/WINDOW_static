%%%% Bar plots for cost comparison %%%
%% dynamic compare costs for starting point 1
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(groot,'defaulttextinterpreter','latex');
set(groot,'defaultLegendInterpreter','latex');


dynamic_support_costs = [380932426.4, 333145308.4]/380932426.4; %/10^6; %%Initial point followed by optimum
dynamic_blade_costs = [791287.3937, 524175.5455]/791287.3937; %/10^6; 
dynamic_gearbox_costs = [708498.4725, 780295.4883]/708498.4725; %/10^6; 

dynamic_oandm_costs = [24201317.33, 23101869.44]/24201317.33;
dynamic_total_investment_costs = [9.95E+08, 9.09E+08]/9.95E+08;

dynamic_component_costs = [dynamic_support_costs; dynamic_blade_costs; dynamic_gearbox_costs; dynamic_oandm_costs];
dynamic_farm_costs = [dynamic_oandm_costs; dynamic_total_investment_costs];

bar(dynamic_component_costs)
grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
set(gca,'TickLabelInterpreter', 'tex');

%ax.GridAlpha = 1;
ylabel('Normalized Cost','Interpreter','latex');
set(gca, 'XTick', [1 2 3 4])
set(gca, 'XTickLabel', {'Support structure' 'Blade' 'Gearbox' 'O&M'})
% xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 
ylim([0 1.3])
%ylabel('Cost (Million EUR)');


%% dynamic compare costs for starting point 2


dynamic_support_costs = [339149053.6, 335707416.3]/339149053.6; %/10^6; %%Initial point followed by optimum
dynamic_blade_costs = [610444.4434, 550697.5683]/610444.4434; %10^6; 
dynamic_gearbox_costs = [660019.2472, 688737.0268]/660019.2472; %10^6; 

dynamic_oandm_costs = [23479860.31, 23710800.57]/23479860.31;
dynamic_total_investment_costs = [9.16E+08, 9.06E+08];

dynamic_component_costs = [dynamic_support_costs; dynamic_blade_costs; dynamic_gearbox_costs];
dynamic_farm_costs = [dynamic_oandm_costs; dynamic_total_investment_costs];

bar(dynamic_component_costs)
grid on
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
set(gca,'TickLabelInterpreter', 'tex');

%ax.GridAlpha = 1;
ylabel('Normalized Cost','Interpreter','latex');
set(gca, 'XTick', [1 2 3])
set(gca, 'XTickLabel', {'Support structure' 'Blade cost' 'Gearbox cost'})
% xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('Initial', 'Optimum','Interpreter','latex'); 



%% dynamic compare costs for 2 optimum points (point 1 first)
dynamic_support_costs = [4660330.835, 4622318.925]; %%point 1 followed by point 2
dynamic_blade_costs = [579520.8965, 575710.3316]; 
dynamic_gearbox_costs = [795508.5658, 686640.967]; 

dynamic_oandm_costs = [23632310.06, 23710800.57];
dynamic_total_investment_costs = [9.29E+08, 9.16E+08];

dynamic_component_costs = [dynamic_support_costs; dynamic_blade_costs; dynamic_gearbox_costs];
dynamic_farm_costs = [dynamic_oandm_costs; dynamic_total_investment_costs];

bar(dynamic_component_costs)
ylim([500000 800000]);
%bar(dynamic_farm_costs)


%% Pie chart for 5 MW turbine

blade_costs = 791287.3937;
gearbox_costs = 708498.4725;
hub_costs = 331212.1311;
generator_costs = 325000.0005;
mainframe_costs = 267031.4481;
transformer_costs = 259844.2;
electrical_costs = 200000; 

RNA_costs = 4052599.375;

others = RNA_costs - blade_costs - gearbox_costs - hub_costs - generator_costs - mainframe_costs -...
    transformer_costs - electrical_costs;

X = [ blade_costs, gearbox_costs, hub_costs, generator_costs, mainframe_costs, transformer_costs, electrical_costs, others]; 
%explode =[1 1 0 0 0 0 0 1];
explode = ones(1,8);
labels = {'Blade','Gearbox','Hub', 'Generator','Mainframe','Transformer', 'Electrical', 'Others'};
pie(X,explode, labels);










