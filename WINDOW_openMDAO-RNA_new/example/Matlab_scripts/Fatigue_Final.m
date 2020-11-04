%%%%%%%%%% Script to estimate Fatigue Damage %%%%%%%%%%%%%%

%%%%% Stress Span is a matrix of time series data points of stresss 
%%%%% Row 1: Edgewise stresses in the skin at Node 7 
%%%%% Row 2: Edgewise stresses in TE Reinf at Node 7
%%%%% Row 3: Flapwise sresses in the skin at Node 37
%%%%% Row 4: Flapwise sresses in the spar at Node 37

load('Internal_layup.mat');
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

fatigue_sf = 1.38;
%%%%% Slopes and UCS of different materials 
m_skin = 10;
UCS_skin = 700/fatigue_sf; 
m_spar = 14;
UCS_spar = 1047/fatigue_sf; %1546;
m_te_reinf = 10; 
UCS_te_reinf = 700/fatigue_sf; %1000;

file = 'DLC_U=6.00.mat'; 
[Stress_root_Fatigue_6, Stress_span_Fatigue_6]= Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file);
    
    
file = 'DLC_U=8.00.mat'; 
[Stress_root_Fatigue_8, Stress_span_Fatigue_8]= Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file);

file = 'DLC_U=12.00.mat';
[Stress_root_Fatigue_12, Stress_span_Fatigue_12]= Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file);
    
file = 'DLC_U=16.00.mat'; 
[Stress_root_Fatigue_16, Stress_span_Fatigue_16]= Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file);

file = 'DLC_U=20.00.mat';
[Stress_root_Fatigue_20, Stress_span_Fatigue_20]= Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file);
    

file = 'DLC_U=23.50.mat';
[Stress_root_Fatigue_23_5, Stress_span_Fatigue_23_5]= Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file);

%%%% Fatigue damage in root skin 

Stress = [Stress_root_Fatigue_6;
        Stress_root_Fatigue_8;
        Stress_root_Fatigue_12;
        Stress_root_Fatigue_16;
        Stress_root_Fatigue_20;
        Stress_root_Fatigue_23_5]; 
 
[Fatigue_root_skin, DEL_root_skin]= Fatigue_calculator(Stress, m_skin, UCS_skin);


%%%% Edgewise Fatigue Damage in the skin 

Stress = [Stress_span_Fatigue_6(1,:);
        Stress_span_Fatigue_8(1,:);
        Stress_span_Fatigue_12(1,:);
        Stress_span_Fatigue_16(1,:);
        Stress_span_Fatigue_20(1,:);
        Stress_span_Fatigue_23_5(1,:)]; 
 
[Fatigue_edgewise_skin, DEL_edgewise_skin]= Fatigue_calculator(Stress, m_skin, UCS_skin);

%%%% Edgewise Fatigue Damage in the TE Reinf

Stress = [Stress_span_Fatigue_6(2,:);
        Stress_span_Fatigue_8(2,:);
        Stress_span_Fatigue_12(2,:);
        Stress_span_Fatigue_16(2,:);
        Stress_span_Fatigue_20(2,:);
        Stress_span_Fatigue_23_5(2,:)]; 
 
[Fatigue_edgewise_te_reinf, DEL_edgewise_te_reinf]= Fatigue_calculator(Stress, m_te_reinf, UCS_te_reinf);


%%%% Flapwise Fatigue Damage in the skin

Stress = [Stress_span_Fatigue_6(3,:);
        Stress_span_Fatigue_8(3,:);
        Stress_span_Fatigue_12(3,:);
        Stress_span_Fatigue_16(3,:);
        Stress_span_Fatigue_20(3,:);
        Stress_span_Fatigue_23_5(3,:)]; 
 
[Fatigue_flapwise_skin, DEL_flapwise_skin]= Fatigue_calculator(Stress, m_skin, UCS_skin);      


%%%% Flapwise Fatigue Damage in the spar

Stress = [Stress_span_Fatigue_6(4,:);
        Stress_span_Fatigue_8(4,:);
        Stress_span_Fatigue_12(4,:);
        Stress_span_Fatigue_16(4,:);
        Stress_span_Fatigue_20(4,:);
        Stress_span_Fatigue_23_5(4,:)]; 
 
[Fatigue_flapwise_spar, DEL_flapwise_spar]= Fatigue_calculator(Stress, m_spar, UCS_spar);


