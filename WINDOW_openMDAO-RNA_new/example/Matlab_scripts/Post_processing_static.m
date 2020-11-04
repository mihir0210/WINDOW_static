
load('Internal_layup.mat');

I_flapwise = zeros(1,49);
y_flapwise_spar = zeros(1,49);
y_flapwise_skin = zeros(1,49);
I_edgewise = zeros(1,49);
y_edgewise_te_reinf = zeros(1,49);
y_edgewise_skin = zeros(1,49);
rel_xc_section = zeros(1,49);
rel_yc_section = zeros(1,49);


for i=1:length(le_core_span)
    [EI_flap(i), EI_edge(i), ~, ~, ~, y_flapwise_spar(i), y_flapwise_skin(i),...
        y_edgewise_te_reinf(i),...
        y_edgewise_skin(i), ~,~, E]= extract_properties_parameterize_latest(...
        span_radius(i), root_span(i), skin_span(i), le_core_span(i),...
    spar_span(i), te_core_span(i), te_reinf_span(i), web_span(i));
end

%load('NREL5MW (gain scheduled).mat');

[Stress_root_skin, Stress_span]=Post_processor(EI_flap, EI_edge,...
    y_flapwise_spar, y_flapwise_skin,...
        y_edgewise_te_reinf,...
        y_edgewise_skin, E); 
    
save('Ultimate_Results_Static.mat', 'Stress_root_skin','Stress_span');

% %% plots 
% load('Static_moment.mat');
% yyaxis left
% plot(Stress_span(1,:));
% hold on;
% yyaxis right
% plot(y_flapwise_skin);
% %plot(I_flapwise./y_flapwise_skin);





%% Function definition

function [Stress_root_skin, Stress_span]=Post_processor(EI_flap, EI_edge,...
    y_flapwise_spar, y_flapwise_skin,...
        y_edgewise_te_reinf,...
        y_edgewise_skin, E)
    Ex_triax = E(1);
    Ex_C_UD = E(2);
    Ex_G_UD =E(3);
    
    
%%%Post processing data%%%
load('Static_moment.mat');
%% For ultimate limit states

PSF = 1.755;
static2dynamic = 1.5; % Assumed by Tanuj

PSF = PSF*static2dynamic; 
%PSF = 2.46;  %GL
%PSF = 2.43; %Tanuj Safety factors
%%% Root stresses
resultant_moment_flap_edge=sqrt(MFlap(1)^2+MEdge(1)^2); %resultant of flap-edge
%resultant_moment_out_in=sqrt(RootMIP.^2+RootMOoP.^2); %resultant of out-in plane


%% Bending Stress calculations 
%%%% Stress at the root in MPa %%% 
% Stress_root_skin=PSF*resultant_moment_flap_edge*y_flapwise_skin(1)/I_flapwise(1)/1e6;
% 
% Stress_flapwise_skin = MFlap.*y_flapwise_skin./I_flapwise/1e6;
% Stress_flapwise_spar = MFlap.*y_flapwise_spar./I_flapwise/1e6;
% 
% Stress_edgewise_skin = (MEdge+MGravity).*y_edgewise_skin./I_edgewise/1e6;
% Stress_edgewise_te_reinf = (MEdge+MGravity).*y_edgewise_te_reinf./I_edgewise/1e6;
% 
% Stress_span = PSF*[Stress_flapwise_skin; Stress_flapwise_spar; Stress_edgewise_skin; Stress_edgewise_te_reinf];

%% Calculate Strain first 

Strain_root = resultant_moment_flap_edge*y_flapwise_skin(1)/EI_flap(1);
Stress_root_skin = PSF*Ex_triax * Strain_root;

Strain_flapwise_skin = MFlap.*y_flapwise_skin./EI_flap;
Stress_flapwise_skin = Ex_triax*Strain_flapwise_skin;

Strain_flapwise_spar = MFlap.*y_flapwise_spar./EI_flap;
Stress_flapwise_spar = Ex_C_UD*Strain_flapwise_spar; 

Strain_edgewise_skin = (MEdge+MGravity).*y_edgewise_skin./EI_edge; 
Stress_edgewise_skin = Ex_triax*Strain_edgewise_skin;

Strain_edgewise_te_reinf = (MEdge+MGravity).*y_edgewise_te_reinf./EI_edge;
Stress_edgewise_te_reinf = Ex_G_UD*Strain_edgewise_te_reinf;

Stress_span = PSF*[Stress_flapwise_skin; Stress_flapwise_spar; 
Stress_edgewise_skin; Stress_edgewise_te_reinf];






% %% Tower stiffness properties
% tower_base_Iarea=(pi/64)*(Tower.Diameter(1)^4-(Tower.Diameter(1)-2*Tower.BottomThickness)^4); %m^4
% tower_base_Ipolar=2*tower_base_Iarea;
% tower_y=Tower.Diameter(1)/2;
% TwrBsM=[TwrBsMxt;TwrBsMyt];
% max_towermoment=max(TwrBsM);
% max_towermoment_torsion=max(TwrBsMzt);
% 
% %% Stress at tower base
% Stress.Tower_base=max_towermoment*1e3*tower_y/tower_base_Iarea/1e6;
% Stress.Tower_base_shear=max_towermoment_torsion*1e3*tower_y/tower_base_Ipolar/1e6;

end
