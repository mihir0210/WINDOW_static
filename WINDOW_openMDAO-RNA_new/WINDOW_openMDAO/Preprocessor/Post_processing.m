
%load('Internal_layup.mat');
I_flapwise = zeros(1,49);
y_flapwise_spar = zeros(1,49);
y_flapwise_skin = zeros(1,49);
I_edgewise = zeros(1,49);
y_edgewise_te_reinf = zeros(1,49);
y_edgewise_skin = zeros(1,49);

for i=1:49
    [~, ~, ~, ~, ~,I_flapwise(i), y_flapwise_spar(i), y_flapwise_skin(i),...
        I_edgewise(i), y_edgewise_te_reinf(i),...
        y_edgewise_skin(i)]= extract_properties_parameterize(...
        span_radius(i), root_span(i), skin_span(i), le_core_span(i),...
    spar_span(i), te_core_span(i), te_reinf_span(i), web_span(i));
end

load('NREL5MW (gain scheduled).mat');

[Stress, Deflection]=Post_processor(I_flapwise,...
    y_flapwise_spar, y_flapwise_skin,...
        I_edgewise, y_edgewise_te_reinf,...
        y_edgewise_skin); 
    
save('Ultimate_Results.mat', 'Stress','Deflection');

function [Stress, Deflection]=Post_processor(I_flapwise,...
    y_flapwise_spar, y_flapwise_skin,...
        I_edgewise, y_edgewise_te_reinf,...
        y_edgewise_skin)
%%%Post processing data%%%
load('DLC.mat');
%% For ultimate limit states
% remove first 60 seconds ( sampling time of 0.008 s)
RootMEdg1(1:60/0.008)=[];
RootMEdg2(1:60/0.008)=[];
RootMEdg3(1:60/0.008)=[];
RootMFlp1(1:60/0.008)=[];
RootMFlp2(1:60/0.008)=[];
RootMFlp3(1:60/0.008)=[];
RootMIP1(1:60/0.008)=[];
RootMIP2(1:60/0.008)=[];
RootMIP3(1:60/0.008)=[];
RootMOoP1(1:60/0.008)=[];
RootMOoP2(1:60/0.008)=[];
RootMOoP3(1:60/0.008)=[];
Spn1MLxb1(1:60/0.008) =[]; %Blade 1 edgewise moment at Span 1 at node 7
Spn1MLyb1(1:60/0.008) =[]; %Blade 1 flapwise moment at Span 1 at node 7
Spn2MLxb1(1:60/0.008) = []; %Blade 1 edgewise moment at Span 2 at node 15 
Spn2MLyb1(1:60/0.008) = []; %Blade 1 flapwise moment at Span 2 at node 15 
Spn3MLxb1(1:60/0.008) =[]; %Blade 1 edgewise moment at Span 3 at node 24
Spn3MLyb1(1:60/0.008) =[]; %Blade 1 flapwise moment at Span 3 at node 24
Spn4MLxb1(1:60/0.008) = []; %Blade 1 edgewise moment at Span 4 at node 37 
Spn4MLyb1(1:60/0.008) = []; %Blade 1 flapwise moment at Span 4 at node 37
Spn5MLxb1(1:60/0.008) = []; %Blade 1 edgewise moment at Span 5 at node 47 
Spn5MLyb1(1:60/0.008) = []; %Blade 1 flapwise moment at Span 5 at node 47

OoPDefl1(1:60/0.008)=[];
OoPDefl2(1:60/0.008)=[];
OoPDefl3(1:60/0.008)=[];
TwrBsMxt(1:60/0.008)=[]; %xt axis along the wind. Side-Side motion
TwrBsMyt(1:60/0.008)=[]; % yt axis perpendiculat to wind. Fore-Aft motion
TwrBsMzt(1:60/0.008)=[]; %zt axis along the tower axis

%%%%%%%%%%%%%%%%%%% Blades %%%%%%%%%%%%%%%%
RootMEdg=[RootMEdg1; RootMEdg2; RootMEdg3];
RootMFlp=[RootMFlp1; RootMFlp2; RootMFlp3];
RootMIP=[RootMIP1; RootMIP2; RootMIP3];
RootMOoP=[RootMOoP1; RootMOoP2; RootMOoP3];


%% Root stresses
resultant_moment_flap_edge=sqrt(RootMEdg.^2+RootMFlp.^2); %resultant of flap-edge
%resultant_moment_out_in=sqrt(RootMIP.^2+RootMOoP.^2); %resultant of out-in plane

[max_resultant_flap_edge, I]=max(resultant_moment_flap_edge);
%max_resultant_out_in=max(resultant_moment_out_in);

OoPDefl=[OoPDefl1; OoPDefl2; OoPDefl3];
Deflection=max(OoPDefl);

%% Bending Stress calculations 
%%%% Stress at the root in MPa %%% 
Stress.Blade.root=max_resultant_flap_edge*1e3*y_flapwise_skin(1)/I_flapwise(1)/1e6;

%%% Root Stress for fatigue at 45 degree point %%% 

Stress_Blade_root_Fatigue = RootMEdg(I)*1e3*y_edgewise_skin(1)*cosd(45)/I_edgewise(1)/1e6...
                           + RootMFlp(I)*1e3*y_flapwise_skin(1)*cosd(45)/I_flapwise(1)/1e6;

%%% Stress at Node 7 %%% 
Stress.Blade.span1_flapwise_skin =  max(Spn1MLyb1)*1e3*y_flapwise_skin(7)/I_flapwise(7)/1e6;
Stress.Blade.span1_flapwise_spar =  max(Spn1MLyb1)*1e3*y_flapwise_spar(7)/I_flapwise(7)/1e6;

Stress.Blade.span1_edgewise_skin =  max(abs(Spn1MLxb1))*1e3*y_edgewise_skin(7)/I_edgewise(7)/1e6;
Stress.Blade.span1_edgewise_te_reinf =  max(abs(Spn1MLxb1))*1e3*y_edgewise_te_reinf(7)/I_edgewise(7)/1e6;


%%% Stress at Node 15 %%% 
Stress.Blade.span2_flapwise_skin =  max(abs(Spn2MLyb1))*1e3*y_flapwise_skin(15)/I_flapwise(15)/1e6;
Stress.Blade.span2_flapwise_spar =  max(abs(Spn2MLyb1))*1e3*y_flapwise_spar(15)/I_flapwise(15)/1e6;

Stress.Blade.span2_edgewise_skin =  max(abs(Spn2MLxb1))*1e3*y_edgewise_skin(15)/I_edgewise(15)/1e6;
Stress.Blade.span2_edgewise_te_reinf =  max(abs(Spn2MLxb1))*1e3*y_edgewise_te_reinf(15)/I_edgewise(15)/1e6;


%%% Stress at Node 24 %%% 
Stress.Blade.span3_flapwise_skin =  max(abs(Spn3MLyb1))*1e3*y_flapwise_skin(24)/I_flapwise(24)/1e6;
Stress.Blade.span3_flapwise_spar =  max(abs(Spn3MLyb1))*1e3*y_flapwise_spar(24)/I_flapwise(24)/1e6;

Stress.Blade.span3_edgewise_skin =  max(abs(Spn3MLxb1))*1e3*y_edgewise_skin(24)/I_edgewise(24)/1e6;
Stress.Blade.span3_edgewise_te_reinf =  max(abs(Spn3MLxb1))*1e3*y_edgewise_te_reinf(24)/I_edgewise(24)/1e6;


%%% Stress at Node 37 %%% 
Stress.Blade.span4_flapwise_skin =  max(abs(Spn4MLyb1))*1e3*y_flapwise_skin(37)/I_flapwise(37)/1e6;
Stress.Blade.span4_flapwise_spar =  max(abs(Spn4MLyb1))*1e3*y_flapwise_spar(37)/I_flapwise(37)/1e6;

Stress.Blade.span4_edgewise_skin =  max(abs(Spn4MLxb1))*1e3*y_edgewise_skin(37)/I_edgewise(37)/1e6;
Stress.Blade.span4_edgewise_te_reinf =  max(abs(Spn4MLxb1))*1e3*y_edgewise_te_reinf(37)/I_edgewise(37)/1e6;

%%% Stress at Node 47 %%% 
Stress.Blade.span5_flapwise_skin =  max(abs(Spn5MLyb1))*1e3*y_flapwise_skin(47)/I_flapwise(47)/1e6;
Stress.Blade.span5_flapwise_spar =  max(abs(Spn5MLyb1))*1e3*y_flapwise_spar(47)/I_flapwise(47)/1e6;

Stress.Blade.span5_edgewise_skin =  max(abs(Spn5MLxb1))*1e3*y_edgewise_skin(47)/I_edgewise(47)/1e6;
Stress.Blade.span5_edgewise_te_reinf =  max(abs(Spn5MLxb1))*1e3*y_edgewise_te_reinf(47)/I_edgewise(47)/1e6;




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
