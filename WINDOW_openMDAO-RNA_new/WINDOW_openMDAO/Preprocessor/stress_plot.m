%% Plots flapwise stresses  along the span %%%%%
load('Ultimate_Results.mat');
span = [0 0.15 0.3 0.5 0.75 0.95];

flapwise_stress_skin = [Stress.Blade.root Stress.Blade.span1_flapwise_skin Stress.Blade.span2_flapwise_skin...
    Stress.Blade.span3_flapwise_skin Stress.Blade.span4_flapwise_skin Stress.Blade.span5_flapwise_skin];

flapwise_stress_spar = [Stress.Blade.root Stress.Blade.span1_flapwise_spar Stress.Blade.span2_flapwise_spar...
    Stress.Blade.span3_flapwise_spar Stress.Blade.span4_flapwise_spar Stress.Blade.span5_flapwise_spar];


%plot(span, flapwise_stress_skin); hold on;
plot(span, flapwise_stress_spar);
xlabel('Blade span [-]','Interpreter','latex');
ylabel('Spar caps - Flapwise stresses (MPa)','Interpreter','latex')
grid on;


%% Plots edgewise stresses  along the span %%%%%
load('Ultimate_Results.mat');
span = [0 0.15 0.3 0.5 0.75 0.95];

edgewise_stress_skin = [Stress.Blade.root Stress.Blade.span1_edgewise_skin Stress.Blade.span2_edgewise_skin...
    Stress.Blade.span3_edgewise_skin Stress.Blade.span4_edgewise_skin Stress.Blade.span5_edgewise_skin];

edgewise_stress_te_reinf = [Stress.Blade.root Stress.Blade.span1_edgewise_te_reinf Stress.Blade.span2_edgewise_te_reinf...
    Stress.Blade.span3_edgewise_te_reinf Stress.Blade.span4_edgewise_te_reinf Stress.Blade.span5_edgewise_te_reinf];


%plot(span, edgewise_stress_skin); hold on;
plot(span, edgewise_stress_te_reinf);
grid on; 
xlabel('Blade span [-]','Interpreter','latex');
ylabel('Spar caps - Edgewise stresses (MPa)','Interpreter','latex')