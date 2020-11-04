%%
function [Stress_root_Fatigue, Stress_span_Fatigue]=Fatigue_stresses(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file)
 %%%Post processing data%%%
load(file);

Ex_triax = E(1);
Ex_C_UD = E(2);
Ex_G_UD = E(3);


%% For ultimate limit states
% remove first 60 seconds ( sampling time of 0.008 s)
t_remove = 0.0125;
RootMEdg1(1:60/t_remove)=[];
RootMEdg2(1:60/t_remove)=[];
RootMEdg3(1:60/t_remove)=[];
RootMFlp1(1:60/t_remove)=[];
RootMFlp2(1:60/t_remove)=[];
RootMFlp3(1:60/t_remove)=[];

Spn1MLxb1(1:60/t_remove) =[]; %Blade 1 edgewise moment at Span 1 at node 7
Spn1MLyb1(1:60/t_remove) =[]; %Blade 1 flapwise moment at Span 1 at node 7
Spn2MLxb1(1:60/t_remove) = []; %Blade 1 edgewise moment at Span 2 at node 15 
Spn2MLyb1(1:60/t_remove) = []; %Blade 1 flapwise moment at Span 2 at node 15 
Spn3MLxb1(1:60/t_remove) =[]; %Blade 1 edgewise moment at Span 3 at node 24
Spn3MLyb1(1:60/t_remove) =[]; %Blade 1 flapwise moment at Span 3 at node 24
Spn4MLxb1(1:60/t_remove) = []; %Blade 1 edgewise moment at Span 4 at node 37 
Spn4MLyb1(1:60/t_remove) = []; %Blade 1 flapwise moment at Span 4 at node 37
Spn5MLxb1(1:60/t_remove) = []; %Blade 1 edgewise moment at Span 5 at node 47 
Spn5MLyb1(1:60/t_remove) = []; %Blade 1 flapwise moment at Span 5 at node 47

RootMEdg=RootMEdg1; %RootMEdg2; RootMEdg3];
RootMFlp=RootMFlp1; %RootMFlp2; RootMFlp3];


PSF =1.755; % IEC factors given in SANDIA labs document

% Overall safety factor by GL (material = 2.94, uncertainty in loads : 1.35)

%% Bending Stress calculations 

%%% Root Stress for fatigue at 45 degree point %%% 

Strain_root_Fatigue = RootMEdg*1e3*y_edgewise_skin(1)*cosd(45)/EI_edge(1)...
                            + RootMFlp*1e3*y_flapwise_skin(1)*cosd(45)/EI_flap(1);
Stress_root_Fatigue = (PSF*Strain_root_Fatigue*Ex_triax)'; %in MPa 

%%%%%%% Spanwise Stresses %%%%%

%% Calculate Strain First 

%%%%% Stresses at node 37 for flapwise and node 7 for edgewise were found
%%%%% to be maximum 

%%% Stress at Node 7 %%% 

Strain_span1_edgewise_skin = Spn1MLxb1*1e3*y_edgewise_skin(7)/EI_edge(7);
Stress_span1_edgewise_skin_nm =  Ex_triax*Strain_span1_edgewise_skin;

Strain_span1_edgewise_te_reinf = Spn1MLxb1*1e3*y_edgewise_te_reinf(7)/EI_edge(7);
Stress_span1_edgewise_te_reinf_nm =  Ex_G_UD*Strain_span1_edgewise_te_reinf; 




%%% Stress at Node 37 %%% 
Strain_span4_flapwise_skin = Spn4MLyb1*1e3*y_flapwise_skin(37)/EI_flap(37);
Stress_span4_flapwise_skin_nm =  Ex_triax*Strain_span4_flapwise_skin;

Strain_span4_flapwise_spar = Spn4MLyb1*1e3*y_flapwise_spar(37)/EI_flap(37);
Stress_span4_flapwise_spar_nm =  Ex_C_UD*Strain_span4_flapwise_spar;



Stress_span_Fatigue = PSF*[Stress_span1_edgewise_skin_nm'; 
                   Stress_span1_edgewise_te_reinf_nm';
                   Stress_span4_flapwise_skin_nm';
                   Stress_span4_flapwise_spar_nm'                   
                   ];
