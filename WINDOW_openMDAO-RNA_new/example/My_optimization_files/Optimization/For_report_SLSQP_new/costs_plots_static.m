%%%% Bar plots for cost comparison %%%
%% Static compare costs for starting point 1
set(groot,'defaultAxesTickLabelInterpreter','latex');  
set(groot,'defaulttextinterpreter','latex');
set(groot,'defaultLegendInterpreter','latex');


static_support_costs = [381255877.9, 345609139.2]/381255877.9; %/10^6; %%Initial point followed by optimum
static_blade_costs = [816870.9753, 592666.3144]/816870.9753; %/10^6; 
static_gearbox_costs = [708498.4725, 793712.6221]/708498.4725; %/10^6; 

static_oandm_costs = [24201317.33, 23700016.24]/24201317.33;
static_total_investment_costs = [9.98E+08, 9.31E+08]/9.98E+08;

static_component_costs = [static_support_costs; static_blade_costs; static_gearbox_costs];
static_farm_costs = [static_oandm_costs; static_total_investment_costs];

x=[1,2,3];
b=bar(x,static_component_costs,0.7);
set(b(2),'facecolor','r')

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
set(gca,'TickLabelInterpreter', 'tex');

axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

%ax.GridAlpha = 1;
ylabel('\textbf{Normalized Cost}','Interpreter','latex');
set(gca, 'XTick', [1 2 3])
set(gca, 'XTickLabel', {'\textbf{Support structure}' '\textbf{Blade cost}' '\textbf{Gearbox cost}'})
% xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('\textbf{Initial: sp1}', '\textbf{Optimum: sp1}','Interpreter','latex'); 
ylim([0 1.3])
xlim([0.5 3.5])
%ylabel('Cost (Million EUR)');


%% Static compare costs for starting point 2


static_support_costs = [394925723.2, 339496887.3]/394925723.2; %/10^6; %%Initial point followed by optimum
static_blade_costs = [739235.2995, 592375.5687]/739235.2995; %10^6; 
static_gearbox_costs = [646870.1641, 781852.2091]/646870.1641; %10^6; 

static_oandm_costs = [24057874.73, 23639318.76];
static_total_investment_costs = [9.91E+08, 9.24E+08];

static_component_costs = [static_support_costs; static_blade_costs; static_gearbox_costs];
static_farm_costs = [static_oandm_costs; static_total_investment_costs];

x=[1,2,3];
b=bar(x,static_component_costs,0.7);
set(b(2),'facecolor','r')

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
set(gca,'TickLabelInterpreter', 'tex');

axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

%ax.GridAlpha = 1;
ylabel('\textbf{Normalized Cost}','Interpreter','latex');
set(gca, 'XTick', [1 2 3])
set(gca, 'XTickLabel', {'\textbf{Support structure}' '\textbf{Blade cost}' '\textbf{Gearbox cost}'})
% xlabel('Normalized blade radius (-)','Interpreter','latex');
legend('\textbf{Initial: sp2}', '\textbf{Optimum: sp2}','Interpreter','latex'); 
ylim([0 1.4])
xlim([0.5 3.5])



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

blade_costs = 816870.9753;
gearbox_costs = 708498.4725;
hub_costs = 335610.5904;
generator_costs = 325000.0005;
mainframe_costs = 268877.6497;
transformer_costs = 259844.2;
electrical_costs = 200000; 

RNA_costs = 4090264.846;

others = RNA_costs - blade_costs - gearbox_costs - hub_costs - generator_costs - mainframe_costs -...
    transformer_costs - electrical_costs;

X = [ blade_costs, gearbox_costs, hub_costs, generator_costs, mainframe_costs, transformer_costs, electrical_costs, others]; 
%explode =[1 1 0 0 0 0 0 1];
explode = ones(1,8);
labels = {'Blade','Gearbox','Hub', 'Generator','Mainframe','Transformer', 'Electrical', 'Others'};
pie(X,explode, labels);










