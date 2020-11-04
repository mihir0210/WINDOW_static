
load('Internal_layup.mat');

I_flapwise = zeros(1,49);
y_flapwise_spar = zeros(1,49);
y_flapwise_skin = zeros(1,49);
I_edgewise = zeros(1,49);
y_edgewise_te_reinf = zeros(1,49);
y_edgewise_skin = zeros(1,49);

for i=1:length(le_core_span)
    [~, ~, ~, ~, ~,I_flapwise(i), y_flapwise_spar(i), y_flapwise_skin(i),...
        I_edgewise(i), y_edgewise_te_reinf(i),...
        y_edgewise_skin(i)]= extract_properties_parameterize(...
        span_radius(i), root_span(i), skin_span(i), le_core_span(i),...
    spar_span(i), te_core_span(i), te_reinf_span(i), web_span(i));
end

%load('NREL5MW (gain scheduled).mat');

[Stress]=Post_processor(I_flapwise,...
    y_flapwise_spar, y_flapwise_skin,...
        I_edgewise, y_edgewise_te_reinf,...
        y_edgewise_skin); 
    
save('Ultimate_Results_Static.mat', 'Stress');

function [Stress]=Post_processor(I_flapwise,...
    y_flapwise_spar, y_flapwise_skin,...
        I_edgewise, y_edgewise_te_reinf,...
        y_edgewise_skin)
    
%%%Post processing data%%%
load('Static_moment.mat');
%% For ultimate limit states
MFlap = span_moment_flap;
MEdge = span_moment_edge;
MGravity = span_moment_gravity;



%% Root stresses
resultant_moment_flap_edge=sqrt(MFlap(1)^2+MEdge(1)^2); %resultant of flap-edge
%resultant_moment_out_in=sqrt(RootMIP.^2+RootMOoP.^2); %resultant of out-in plane


%% Bending Stress calculations 
%%%% Stress at the root in MPa %%% 
Stress.Blade.root=resultant_moment_flap_edge*1e3*y_flapwise_skin(1)/I_flapwise(1)/1e6;


%%% Stress at Node 5 %%% 
Stress.Blade.span1_flapwise_skin =  MFlap(5)*1e3*y_flapwise_skin(5)/I_flapwise(5)/1e6;
Stress.Blade.span1_flapwise_spar =  MFlap(5)*1e3*y_flapwise_spar(5)/I_flapwise(5)/1e6;

Stress.Blade.span1_edgewise_skin =  MEdge(5)*1e3*y_edgewise_skin(5)/I_edgewise(5)/1e6;
Stress.Blade.span1_edgewise_te_reinf =  MEdge(5)*1e3*y_edgewise_te_reinf(5)/I_edgewise(5)/1e6;


%%% Stress at Node 35 %%% 
Stress.Blade.span2_flapwise_skin =  MFlap(35)*1e3*y_flapwise_skin(35)/I_flapwise(35)/1e6;
Stress.Blade.span2_flapwise_spar =  MFlap(35)*1e3*y_flapwise_spar(35)/I_flapwise(35)/1e6;

Stress.Blade.span2_edgewise_skin =  MEdge(35)*1e3*y_edgewise_skin(35)/I_edgewise(35)/1e6;
Stress.Blade.span2_edgewise_te_reinf =  MEdge(35)*1e3*y_edgewise_te_reinf(35)/I_edgewise(35)/1e6;



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
