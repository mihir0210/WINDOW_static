%%%% Bar plots for cost comparison %%%
%% Static compare costs for starting point 1
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(groot,'defaulttextinterpreter','latex');
set(groot,'defaultLegendInterpreter','latex');


static_support_costs = [5147735.492, 4660330.835]/5147735.492; %/10^6; %%Initial point followed by optimum
static_blade_costs = [791287.3937, 579520.8965]/791287.3937; %/10^6; 
static_gearbox_costs = [708498.4725, 795508.5658]/708498.4725; %/10^6; 

static_oandm_costs = [23632310.06, 23710800.57]/23632310.06;
static_total_investment_costs = [9.29E+08, 9.16E+08]/9.29E+08;

static_component_costs = [static_support_costs; static_blade_costs; static_gearbox_costs];
static_farm_costs = [static_oandm_costs; static_total_investment_costs];

bar(static_component_costs)
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
ylim([0 1.3])
%ylabel('Cost (Million EUR)');


%% Static compare costs for starting point 2


static_support_costs = [4591181.706, 4622318.925]/4591181.706; %/10^6; %%Initial point followed by optimum
static_blade_costs = [650146.1174, 575710.3316]/650146.1174; %10^6; 
static_gearbox_costs = [660019.2472, 686640.967]/660019.2472; %10^6; 

static_oandm_costs = [23479860.31, 23710800.57];
static_total_investment_costs = [9.22E+08, 9.22E+08];

static_component_costs = [static_support_costs; static_blade_costs; static_gearbox_costs];
static_farm_costs = [static_oandm_costs; static_total_investment_costs];

bar(static_component_costs)
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



%% Static compare costs for 2 optimum points (point 1 first)
static_support_costs = [4660330.835, 4622318.925]; %%point 1 followed by point 2
static_blade_costs = [579520.8965, 575710.3316]; 
static_gearbox_costs = [795508.5658, 686640.967]; 

static_oandm_costs = [23632310.06, 23710800.57];
static_total_investment_costs = [9.29E+08, 9.16E+08];

static_component_costs = [static_support_costs; static_blade_costs; static_gearbox_costs];
static_farm_costs = [static_oandm_costs; static_total_investment_costs];

bar(static_component_costs)
ylim([500000 800000]);
%bar(static_farm_costs)


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










