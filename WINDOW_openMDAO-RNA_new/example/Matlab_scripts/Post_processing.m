
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
    [EI_flap(i), EI_edge(i), ~, ~, ~, I_flapwise(i), y_flapwise_spar(i), y_flapwise_skin(i),...
        I_edgewise(i), y_edgewise_te_reinf(i),...
        y_edgewise_skin(i), ~, ~, E]= extract_properties_parameterize(...
        span_radius(i), root_span(i), skin_span(i), le_core_span(i),...
    spar_span(i), te_core_span(i), te_reinf_span(i), web_span(i));
end

%load('NREL5MW (gain scheduled).mat');
load([pwd,'\WT_design.mat']);
% 

n =  CertificationSettings.Run.Seeds ;
file = cell(1,n);
if n > 1

   for i=1:n
       file{i}=['DLC_','seed=', int2str(i), '.mat'];
   end
else
  file = 'DLC.mat'; 
end


[Stress_root, Stress_span, Deflection]=Post_processor(EI_flap, EI_edge,...
    y_flapwise_spar, y_flapwise_skin,...
        y_edgewise_te_reinf,...
        y_edgewise_skin,E, file); 
    
save('Ultimate_Results.mat', 'Stress_root','Stress_span','Deflection');




function [Stress_root, Stress_span, Deflection]=Post_processor(EI_flap, EI_edge,...
         y_flapwise_spar, y_flapwise_skin, y_edgewise_te_reinf,...
        y_edgewise_skin,E, file)
 
 %%%Post processing data%%%
seed1_70=load(file{1});
seed2_70=load(file{2});
seed3_70=load(file{3});
 

Ex_triax = E(1);
Ex_C_UD = E(2);
Ex_G_UD = E(3);


%% For ultimate limit states
% remove first 60 seconds ( sampling time of 0.008 s)
% RootMEdg1(1:60/0.008)=[];
% RootMEdg2(1:60/0.008)=[];
% RootMEdg3(1:60/0.008)=[];
% RootMFlp1(1:60/0.008)=[];
% RootMFlp2(1:60/0.008)=[];
% RootMFlp3(1:60/0.008)=[];
% RootMIP1(1:60/0.008)=[];
% RootMIP2(1:60/0.008)=[];
% RootMIP3(1:60/0.008)=[];
% RootMOoP1(1:60/0.008)=[];
% RootMOoP2(1:60/0.008)=[];
% RootMOoP3(1:60/0.008)=[];
% 
% Spn1MLxb1(1:60/0.008) =[]; %Blade 1 edgewise moment at Span 1 at node 7
% Spn1MLyb1(1:60/0.008) =[]; %Blade 1 flapwise moment at Span 1 at node 7
% Spn2MLxb1(1:60/0.008) = []; %Blade 1 edgewise moment at Span 2 at node 15 
% Spn2MLyb1(1:60/0.008) = []; %Blade 1 flapwise moment at Span 2 at node 15 
% Spn3MLxb1(1:60/0.008) =[]; %Blade 1 edgewise moment at Span 3 at node 24
% Spn3MLyb1(1:60/0.008) =[]; %Blade 1 flapwise moment at Span 3 at node 24
% Spn4MLxb1(1:60/0.008) = []; %Blade 1 edgewise moment at Span 4 at node 37 
% Spn4MLyb1(1:60/0.008) = []; %Blade 1 flapwise moment at Span 4 at node 37
% Spn5MLxb1(1:60/0.008) = []; %Blade 1 edgewise moment at Span 5 at node 47 
% Spn5MLyb1(1:60/0.008) = []; %Blade 1 flapwise moment at Span 5 at node 47
% 
% 
% OoPDefl1(1:60/0.008)=[];
% OoPDefl2(1:60/0.008)=[];
% OoPDefl3(1:60/0.008)=[];


% RootMEdg=[RootMEdg1; RootMEdg2; RootMEdg3];
% RootMFlp=[RootMFlp1; RootMFlp2; RootMFlp3];
% RootMIP=[RootMIP1; RootMIP2; RootMIP3];
% RootMOoP=[RootMOoP1; RootMOoP2; RootMOoP3];

PSF =1.755; % IEC factors given in SANDIA labs document

% Overall safety factor by GL ( material = 2.94, uncertainty in loads : 1.35)


%%%%%% Tip deflection %%%%%%%
seed1_70.OoPDefl1(1:10/0.008)=0;
seed1_70.OoPDefl2(1:10/0.008) = 0;
seed1_70.OoPDefl3(1:10/0.008)=0;
seed2_70.OoPDefl1(1:10/0.008)=0;
seed2_70.OoPDefl2(1:10/0.008) = 0;
seed2_70.OoPDefl3(1:10/0.008)=0;
seed3_70.OoPDefl1(1:10/0.008)=0;
seed3_70.OoPDefl2(1:10/0.008) = 0;
seed3_70.OoPDefl3(1:10/0.008)=0;

seed1_OoPDefl = [seed1_70.OoPDefl1; seed1_70.OoPDefl2; seed1_70.OoPDefl3];
seed2_OoPDefl = [seed2_70.OoPDefl1; seed2_70.OoPDefl2; seed2_70.OoPDefl3];
seed3_OoPDefl = [seed3_70.OoPDefl1; seed3_70.OoPDefl2; seed3_70.OoPDefl3];


Deflection = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl))/3;

%% Root stresses
seed1_70.RootMFlp1(1:10/0.008)=0;
seed1_70.RootMFlp2(1:10/0.008)=0;
seed1_70.RootMFlp3(1:10/0.008)=0;
seed2_70.RootMFlp1(1:10/0.008)=0;
seed2_70.RootMFlp2(1:10/0.008)=0;
seed2_70.RootMFlp3(1:10/0.008)=0;
seed3_70.RootMFlp1(1:10/0.008)=0;
seed3_70.RootMFlp2(1:10/0.008)=0;
seed3_70.RootMFlp3(1:10/0.008)=0;
seed1_70.RootMEdg1(1:10/0.008)=0;
seed1_70.RootMEdg2(1:10/0.008)=0;
seed1_70.RootMEdg3(1:10/0.008)=0;
seed2_70.RootMEdg1(1:10/0.008)=0;
seed2_70.RootMEdg2(1:10/0.008)=0;
seed2_70.RootMEdg3(1:10/0.008)=0;
seed3_70.RootMEdg1(1:10/0.008)=0;
seed3_70.RootMEdg2(1:10/0.008)=0;
seed3_70.RootMEdg3(1:10/0.008)=0;


seed1_flpmoment = [seed1_70.RootMFlp1; seed1_70.RootMFlp2; seed1_70.RootMFlp3];
seed2_flpmoment = [seed2_70.RootMFlp1; seed2_70.RootMFlp2; seed2_70.RootMFlp3];
seed3_flpmoment = [seed3_70.RootMFlp1; seed3_70.RootMFlp2; seed3_70.RootMFlp3];

seed1_edgemoment = [seed1_70.RootMEdg1; seed1_70.RootMEdg2; seed1_70.RootMEdg3];
seed2_edgemoment = [seed2_70.RootMEdg1; seed2_70.RootMEdg2; seed2_70.RootMEdg3];
seed3_edgemoment = [seed3_70.RootMEdg1; seed3_70.RootMEdg2; seed3_70.RootMEdg3];


seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);

seed_70_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment))/3;

% resultant_moment_flap_edge=sqrt(RootMEdg.^2+RootMFlp.^2); %resultant of flap-edge
% %resultant_moment_out_in=sqrt(RootMIP.^2+RootMOoP.^2); %resultant of out-in plane
% 
% max_resultant_flap_edge=max(resultant_moment_flap_edge);
%max_resultant_out_in=max(resultant_moment_out_in);
% 
% OoPDefl=[OoPDefl1; OoPDefl2; OoPDefl3];
% Deflection=max(OoPDefl);

%% Bending Stress calculations 
%%%% Stress at the root %%% 
%Stress_root=PSF*max_resultant_flap_edge*1e3*y_flapwise_skin(1)/I_flapwise(1)/1e6;


Strain_root = seed_70_rootmoment*1e3*y_flapwise_skin(1)/EI_flap(1); 
Stress_root = PSF*Strain_root*Ex_triax; %in MPa 


%%%%%%% Spanwise Stresses %%%%%
seed1_70.Spn1MLxb1(1:10/0.008)=0;
seed1_70.Spn2MLxb1(1:10/0.008)=0;
seed1_70.Spn3MLxb1(1:10/0.008)=0;
seed1_70.Spn4MLxb1(1:10/0.008)=0;
seed1_70.Spn5MLxb1(1:10/0.008)=0;

seed2_70.Spn1MLxb1(1:10/0.008)=0;
seed2_70.Spn2MLxb1(1:10/0.008)=0;
seed2_70.Spn3MLxb1(1:10/0.008)=0;
seed2_70.Spn4MLxb1(1:10/0.008)=0;
seed2_70.Spn5MLxb1(1:10/0.008)=0;

seed3_70.Spn1MLxb1(1:10/0.008)=0;
seed3_70.Spn2MLxb1(1:10/0.008)=0;
seed3_70.Spn3MLxb1(1:10/0.008)=0;
seed3_70.Spn4MLxb1(1:10/0.008)=0;
seed3_70.Spn5MLxb1(1:10/0.008)=0;

seed1_70.Spn1MLyb1(1:10/0.008)=0;
seed1_70.Spn2MLyb1(1:10/0.008)=0;
seed1_70.Spn3MLyb1(1:10/0.008)=0;
seed1_70.Spn4MLyb1(1:10/0.008)=0;
seed1_70.Spn5MLyb1(1:10/0.008)=0;

seed2_70.Spn1MLyb1(1:10/0.008)=0;
seed2_70.Spn2MLyb1(1:10/0.008)=0;
seed2_70.Spn3MLyb1(1:10/0.008)=0;
seed2_70.Spn4MLyb1(1:10/0.008)=0;
seed2_70.Spn5MLyb1(1:10/0.008)=0;

seed3_70.Spn1MLyb1(1:10/0.008)=0;
seed3_70.Spn2MLyb1(1:10/0.008)=0;
seed3_70.Spn3MLyb1(1:10/0.008)=0;
seed3_70.Spn4MLyb1(1:10/0.008)=0;
seed3_70.Spn5MLyb1(1:10/0.008)=0;


Spn1MLxb1 =  (max(abs(seed1_70.Spn1MLxb1)) + max(abs(seed2_70.Spn1MLxb1)) + max(abs(seed3_70.Spn1MLxb1)))/3;
Spn2MLxb1 =  (max(abs(seed1_70.Spn2MLxb1)) + max(abs(seed2_70.Spn2MLxb1)) + max(abs(seed3_70.Spn2MLxb1)))/3;
Spn3MLxb1 =  (max(abs(seed1_70.Spn3MLxb1)) + max(abs(seed2_70.Spn3MLxb1)) + max(abs(seed3_70.Spn3MLxb1)))/3;
Spn4MLxb1 =  (max(abs(seed1_70.Spn4MLxb1)) + max(abs(seed2_70.Spn4MLxb1)) + max(abs(seed3_70.Spn4MLxb1)))/3;
Spn5MLxb1 =  (max(abs(seed1_70.Spn5MLxb1)) + max(abs(seed2_70.Spn5MLxb1)) + max(abs(seed3_70.Spn5MLxb1)))/3;


Spn1MLyb1 =  (max(abs(seed1_70.Spn1MLyb1)) + max(abs(seed2_70.Spn1MLyb1)) + max(abs(seed3_70.Spn1MLyb1)))/3;
Spn2MLyb1 =  (max(abs(seed1_70.Spn2MLyb1)) + max(abs(seed2_70.Spn2MLyb1)) + max(abs(seed3_70.Spn2MLyb1)))/3;
Spn3MLyb1 =  (max(abs(seed1_70.Spn3MLyb1)) + max(abs(seed2_70.Spn3MLyb1)) + max(abs(seed3_70.Spn3MLyb1)))/3;
Spn4MLyb1 =  (max(abs(seed1_70.Spn4MLyb1)) + max(abs(seed2_70.Spn4MLyb1)) + max(abs(seed3_70.Spn4MLyb1)))/3;
Spn5MLyb1 =  (max(abs(seed1_70.Spn5MLyb1)) + max(abs(seed2_70.Spn5MLyb1)) + max(abs(seed3_70.Spn5MLyb1)))/3;

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


Stress_span = PSF*[Stress_loc1; Stress_loc2; Stress_loc3; Stress_loc4; Stress_loc5];



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
