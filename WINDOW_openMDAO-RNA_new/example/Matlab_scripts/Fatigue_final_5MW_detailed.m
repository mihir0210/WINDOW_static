%%%%%%%%%% Script to estimate Fatigue Damage for the 5 MW turbine %%%%%%%%%%%%%%

%%%%% Stress Span is a matrix of time series data points of stresss 
%%%%% Row 1: Edgewise stresses in the skin at Node 7 
%%%%% Row 2: Edgewise stresses in TE Reinf at Node 7
%%%%% Row 3: Flapwise sresses in the skin at Node 37
%%%%% Row 4: Flapwise sresses in the spar at Node 37

load('Internal_layup_5MW.mat');
%span_radius = span_radius + 2.1276; 
I_flapwise = zeros(1,49);
y_flapwise_spar = zeros(1,49);
y_flapwise_skin = zeros(1,49);
I_edgewise = zeros(1,49);
y_edgewise_te_reinf = zeros(1,49);
y_edgewise_skin = zeros(1,49);
EI_flap = zeros(1,49);
EI_edge = zeros(1,49);

for i=1:49
    [EI_flap(i), EI_edge(i), ~, ~, ~, ~, y_flapwise_spar(i), y_flapwise_skin(i),...
        ~, y_edgewise_te_reinf(i),...
        y_edgewise_skin(i), ~, ~, E]= extract_properties_parameterize(...
        span_radius(i), root_span(i), skin_span(i), le_core_span(i),...
    spar_span(i), te_core_span(i), te_reinf_span(i), web_span(i));
end

fatigue_sf = 1.38; %Safety factor for fatigue. This is used to shift the
%S-N curve down

%%%%% Slopes and UCS of different materials 
m_skin = 10;
UCS_skin = 700/fatigue_sf; 
m_spar = 14;
UCS_spar = 1047/fatigue_sf; %1546 UTS;
m_te_reinf = 10; 
UCS_te_reinf = 700/fatigue_sf; %1000 UTS;

% EI_flap = Blade.EIflap;
% EI_edge = Blade.EIedge; 
Stress_root_Fatigue = cell(1,24);
Stress_span_Fatigue = cell(1,24);

for i=4:24
    file = strcat('Fatigue_5MW_U=',num2str(i),'.00.mat');
    [Stress_root_Fatigue{i-3}, Stress_span_Fatigue{i-3}]= Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file);
end


%%%% Fatigue damage in root skin
for i=1:21
 Stress(i,:) = Stress_root_Fatigue{i};
end

% Stress = [Stress_root_Fatigue_6;
%     Stress_root_Fatigue_8;
%     Stress_root_Fatigue_12;
%     Stress_root_Fatigue_16;
%     Stress_root_Fatigue_20;
%     Stress_root_Fatigue_23_5];
 
[Fatigue_root_skin, DEL_root_skin]= Fatigue_calculator_detailed(Stress, m_skin, UCS_skin);


%%%% Edgewise Fatigue Damage in the skin 

for i=1:21
 Stress(i,:) = Stress_span_Fatigue{i}(1,:);
end


[Fatigue_edgewise_skin, DEL_edgewise_skin]= Fatigue_calculator_detailed(Stress, m_skin, UCS_skin);

%%%% Edgewise Fatigue Damage in the TE Reinf

for i=1:21
 Stress(i,:) = Stress_span_Fatigue{i}(2,:);
end



 
[Fatigue_edgewise_te_reinf, DEL_edgewise_te_reinf]= Fatigue_calculator_detailed(Stress, m_te_reinf, UCS_te_reinf);


%%%% Flapwise Fatigue Damage in the skin

for i=1:21
 Stress(i,:) = Stress_span_Fatigue{i}(3,:);
end

 
[Fatigue_flapwise_skin, DEL_flapwise_skin]= Fatigue_calculator_detailed(Stress, m_skin, UCS_skin);      


%%%% Flapwise Fatigue Damage in the spar

for i=1:21
 Stress(i,:) = Stress_span_Fatigue{i}(4,:);
end

 
[Fatigue_flapwise_spar, DEL_flapwise_spar]= Fatigue_calculator_detailed(Stress, m_spar, UCS_spar);


