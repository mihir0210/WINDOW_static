
%load('Internal_layup.mat');
%load('Internal_layup_static_opt.mat');

load('Internal_layup_5MW.mat');
I_flapwise = zeros(1,49);
y_flapwise_spar = zeros(1,49);
y_flapwise_skin = zeros(1,49);
I_edgewise = zeros(1,49);
y_edgewise_te_reinf = zeros(1,49);
y_edgewise_skin = zeros(1,49);
EI_flap = zeros(1,49);
EI_edge = zeros(1,49);

for i=1:49
    [EI_flap(i), EI_edge(i), ~, ~, ~, y_flapwise_spar(i), y_flapwise_skin(i),...
        y_edgewise_te_reinf(i),...
        y_edgewise_skin(i), ~, ~, E]= extract_properties_parameterize_latest(...
        span_radius(i), root_span(i), skin_span(i), le_core_span(i),...
    spar_span(i), te_core_span(i), te_reinf_span(i), web_span(i));
end


% load([pwd,'\WT_design.mat']);
% file = 'DLC1.3.mat';

load('NREL5MW (gain scheduled).mat');
file = 'DLC1.3_5MW.mat';


% load([pwd,'\WT_design_static_opt.mat']);
% file = 'DLC1.3_static_opt.mat';





[Stress_root, Stress_span, Deflection]=Post_processor(EI_flap, EI_edge,...
    y_flapwise_spar, y_flapwise_skin,...
        y_edgewise_te_reinf,...
        y_edgewise_skin,E, file); 
    
save('Ultimate_Results.mat', 'Stress_root','Stress_span','Deflection');   
%save('Ultimate_Results_static_opt.mat', 'Stress_root','Stress_span','Deflection');
%save('Ultimate_Results_5MW.mat', 'Stress_root','Stress_span','Deflection');
%quit



function [Stress_root, Stress_span, Deflection]=Post_processor(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file)
 
 %%%Post processing data%%%
load(file); 
 

Ex_triax = E(1);
Ex_C_UD = E(2);
Ex_G_UD = E(3);


%% For ultimate limit states
% remove first few seconds (sampling time of 0.008 or 0.0125 s)
t_remove = 20;
step_size = 0.0125; 
RootMEdg1(1:t_remove/step_size)=[];
RootMEdg2(1:t_remove/step_size)=[];
RootMEdg3(1:t_remove/step_size)=[];
RootMFlp1(1:t_remove/step_size)=[];
RootMFlp2(1:t_remove/step_size)=[];
RootMFlp3(1:t_remove/step_size)=[];
RootMIP1(1:t_remove/step_size)=[];
RootMIP2(1:t_remove/step_size)=[];
RootMIP3(1:t_remove/step_size)=[];
RootMOoP1(1:t_remove/step_size)=[];
RootMOoP2(1:t_remove/step_size)=[];
RootMOoP3(1:t_remove/step_size)=[];

Spn1MLxb1(1:t_remove/step_size) =[]; %Blade 1 edgewise moment at Span 1 at node 7
Spn1MLyb1(1:t_remove/step_size) =[]; %Blade 1 flapwise moment at Span 1 at node 7
Spn2MLxb1(1:t_remove/step_size) = []; %Blade 1 edgewise moment at Span 2 at node 15 
Spn2MLyb1(1:t_remove/step_size) = []; %Blade 1 flapwise moment at Span 2 at node 15 
Spn3MLxb1(1:t_remove/step_size) =[]; %Blade 1 edgewise moment at Span 3 at node 24
Spn3MLyb1(1:t_remove/step_size) =[]; %Blade 1 flapwise moment at Span 3 at node 24
Spn4MLxb1(1:t_remove/step_size) = []; %Blade 1 edgewise moment at Span 4 at node 37 
Spn4MLyb1(1:t_remove/step_size) = []; %Blade 1 flapwise moment at Span 4 at node 37
Spn5MLxb1(1:t_remove/step_size) = []; %Blade 1 edgewise moment at Span 5 at node 47 
Spn5MLyb1(1:t_remove/step_size) = []; %Blade 1 flapwise moment at Span 5 at node 47


OoPDefl1(1:t_remove/step_size)=[];
OoPDefl2(1:t_remove/step_size)=[];
OoPDefl3(1:t_remove/step_size)=[];


RootMEdg=[RootMEdg1; RootMEdg2; RootMEdg3];
RootMFlp=[RootMFlp1; RootMFlp2; RootMFlp3];


PSF =1.755; % IEC factors given in SANDIA labs document
%PSF=2.46;

SSF_tip = 1.1; %% Based on new simulations. 
SSF_stress = 1.1; 

%PSF_deflection = 1.485; 
% Overall safety factor by GL ( material = 2.94, uncertainty in loads : 1.35)


%%%%%% Tip deflection %%%%%%%

OoPDefl = [OoPDefl1; OoPDefl2; OoPDefl3];

Deflection = SSF_tip*max(OoPDefl);

%% Root stresses


rootmoment = sqrt(RootMFlp.^2 + RootMEdg.^2);
[max_rootmoment,I] = max(rootmoment);

%theta = atan(RootMFlp(I)/RootMEdg(I));

% resultant_moment_flap_edge=sqrt(RootMEdg.^2+RootMFlp.^2); %resultant of flap-edge
% %resultant_moment_out_in=sqrt(RootMIP.^2+RootMOoP.^2); %resultant of out-in plane
% 
% max_resultant_flap_edge=max(resultant_moment_flap_edge);
%max_resultant_out_in=max(resultant_moment_out_in);
% 


%% Bending Stress calculations 
%%%% Stress at the root %%% 
%Stress_root=PSF*max_resultant_flap_edge*1e3*y_flapwise_skin(1)/I_flapwise(1)/1e6;


%Strain_root = max_rootmoment*1e3*y_flapwise_skin(1)/EI_flap(1); 
Strain_root = RootMEdg(I)*1e3*y_edgewise_skin(1)*cosd(45)/EI_edge(1)...
                            + RootMFlp(I)*1e3*y_flapwise_skin(1)*cosd(45)/EI_flap(1);
          

Stress_root = SSF_stress*PSF*Strain_root*Ex_triax; %in MPa 


%%%%%%% Spanwise Stresses %%%%%
Spn1MLxb1(1:t_remove/step_size)=0;
Spn2MLxb1(1:t_remove/step_size)=0;
Spn3MLxb1(1:t_remove/step_size)=0;
Spn4MLxb1(1:t_remove/step_size)=0;
Spn5MLxb1(1:t_remove/step_size)=0;


Spn1MLyb1(1:t_remove/step_size)=0;
Spn2MLyb1(1:t_remove/step_size)=0;
Spn3MLyb1(1:t_remove/step_size)=0;
Spn4MLyb1(1:t_remove/step_size)=0;
Spn5MLyb1(1:t_remove/step_size)=0;



Spn1MLxb1 =  max(abs(Spn1MLxb1));
Spn2MLxb1 =  max(abs(Spn2MLxb1));
Spn3MLxb1 =  max(abs(Spn3MLxb1));
Spn4MLxb1 =  max(abs(Spn4MLxb1));
Spn5MLxb1 =  max(abs(Spn5MLxb1));

Spn1MLyb1 =  max(abs(Spn1MLyb1));
Spn2MLyb1 =  max(abs(Spn2MLyb1));
Spn3MLyb1 =  max(abs(Spn3MLyb1));
Spn4MLyb1 =  max(abs(Spn4MLyb1));
Spn5MLyb1 =  max(abs(Spn5MLyb1));

%% Calculate Strain First 

%%% Stress at Node 7 %%% 
Strain_span1_flapwise_skin = Spn1MLyb1*1e3*y_flapwise_skin(7)/EI_flap(7);
Stress_span1_flapwise_skin_nm =  Ex_triax*Strain_span1_flapwise_skin;

Strain_span1_flapwise_spar = Spn1MLyb1*1e3*y_flapwise_spar(7)/EI_flap(7);
Stress_span1_flapwise_spar_nm =  Ex_C_UD*Strain_span1_flapwise_spar;

Strain_span1_edgewise_skin = Spn1MLxb1*1e3*y_edgewise_skin(7)/EI_edge(7);
Stress_span1_edgewise_skin_nm =  Ex_triax*Strain_span1_edgewise_skin;

Strain_span1_edgewise_te_reinf = Spn1MLxb1*1e3*y_edgewise_te_reinf(7)/EI_edge(7);
Stress_span1_edgewise_te_reinf_nm =  Ex_G_UD*Strain_span1_edgewise_te_reinf; 


%%% Stress at Node 15 %%% 
Strain_span2_flapwise_skin = Spn2MLyb1*1e3*y_flapwise_skin(15)/EI_flap(15);
Stress_span2_flapwise_skin_nm =  Ex_triax*Strain_span2_flapwise_skin;

Strain_span2_flapwise_spar = Spn2MLyb1*1e3*y_flapwise_spar(15)/EI_flap(15);
Stress_span2_flapwise_spar_nm =  Ex_C_UD*Strain_span2_flapwise_spar;

Strain_span2_edgewise_skin = Spn2MLxb1*1e3*y_edgewise_skin(15)/EI_edge(15);
Stress_span2_edgewise_skin_nm =  Ex_triax*Strain_span2_edgewise_skin;

Strain_span2_edgewise_te_reinf = Spn2MLxb1*1e3*y_edgewise_te_reinf(15)/EI_edge(15);
Stress_span2_edgewise_te_reinf_nm =  Ex_G_UD*Strain_span2_edgewise_te_reinf; 


%%% Stress at Node 24 %%% 
Strain_span3_flapwise_skin = Spn3MLyb1*1e3*y_flapwise_skin(24)/EI_flap(24);
Stress_span3_flapwise_skin_nm =  Ex_triax*Strain_span3_flapwise_skin;

Strain_span3_flapwise_spar = Spn3MLyb1*1e3*y_flapwise_spar(24)/EI_flap(24);
Stress_span3_flapwise_spar_nm =  Ex_C_UD*Strain_span3_flapwise_spar;

Strain_span3_edgewise_skin = Spn3MLxb1*1e3*y_edgewise_skin(24)/EI_edge(24);
Stress_span3_edgewise_skin_nm =  Ex_triax*Strain_span3_edgewise_skin;

Strain_span3_edgewise_te_reinf = Spn3MLxb1*1e3*y_edgewise_te_reinf(24)/EI_edge(24);
Stress_span3_edgewise_te_reinf_nm =  Ex_G_UD*Strain_span3_edgewise_te_reinf; 


%%% Stress at Node 37 %%% 
Strain_span4_flapwise_skin = Spn4MLyb1*1e3*y_flapwise_skin(37)/EI_flap(37);
Stress_span4_flapwise_skin_nm =  Ex_triax*Strain_span4_flapwise_skin;

Strain_span4_flapwise_spar = Spn4MLyb1*1e3*y_flapwise_spar(37)/EI_flap(37);
Stress_span4_flapwise_spar_nm =  Ex_C_UD*Strain_span4_flapwise_spar;

Strain_span4_edgewise_skin = Spn4MLxb1*1e3*y_edgewise_skin(37)/EI_edge(37);
Stress_span4_edgewise_skin_nm =  Ex_triax*Strain_span4_edgewise_skin;

Strain_span4_edgewise_te_reinf = Spn4MLxb1*1e3*y_edgewise_te_reinf(37)/EI_edge(37);
Stress_span4_edgewise_te_reinf_nm =  Ex_G_UD*Strain_span4_edgewise_te_reinf; 



%%% Stress at Node 47 %%% 
Strain_span5_flapwise_skin = Spn5MLyb1*1e3*y_flapwise_skin(47)/EI_flap(47);
Stress_span5_flapwise_skin_nm =  Ex_triax*Strain_span5_flapwise_skin;

Strain_span5_flapwise_spar = Spn5MLyb1*1e3*y_flapwise_spar(47)/EI_flap(47);
Stress_span5_flapwise_spar_nm =  Ex_C_UD*Strain_span5_flapwise_spar;

Strain_span5_edgewise_skin = Spn5MLxb1*1e3*y_edgewise_skin(47)/EI_edge(47);
Stress_span5_edgewise_skin_nm =  Ex_triax*Strain_span5_edgewise_skin;

Strain_span5_edgewise_te_reinf = Spn5MLxb1*1e3*y_edgewise_te_reinf(47)/EI_edge(47);
Stress_span5_edgewise_te_reinf_nm =  Ex_G_UD*Strain_span5_edgewise_te_reinf; 

Stress_loc1 = [Stress_span1_flapwise_skin_nm, Stress_span1_flapwise_spar_nm, Stress_span1_edgewise_skin_nm, Stress_span1_edgewise_te_reinf_nm];
Stress_loc2 = [Stress_span2_flapwise_skin_nm, Stress_span2_flapwise_spar_nm, Stress_span2_edgewise_skin_nm, Stress_span2_edgewise_te_reinf_nm];
Stress_loc3 = [Stress_span3_flapwise_skin_nm, Stress_span3_flapwise_spar_nm, Stress_span3_edgewise_skin_nm, Stress_span3_edgewise_te_reinf_nm];
Stress_loc4 = [Stress_span4_flapwise_skin_nm, Stress_span4_flapwise_spar_nm, Stress_span4_edgewise_skin_nm, Stress_span4_edgewise_te_reinf_nm];
Stress_loc5 = [Stress_span5_flapwise_skin_nm, Stress_span5_flapwise_spar_nm, Stress_span5_edgewise_skin_nm, Stress_span5_edgewise_te_reinf_nm];


Stress_span = SSF_stress*PSF*[Stress_loc1; Stress_loc2; Stress_loc3; Stress_loc4; Stress_loc5];



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
