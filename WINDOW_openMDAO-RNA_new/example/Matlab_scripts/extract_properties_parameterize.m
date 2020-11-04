function [EI_flap, EI_edge, G_stiffness, EA, M_L, I_xx, y_flapwise_spar, y_flapwise_skin,...
        I_yy, y_edgewise_te_reinf,...
        y_edgewise_skin,rel_xc_section, rel_yc_section, E] = extract_properties_parameterize(location, root, skin, le_core, spar, te_core, te_reinf, web)
% convert all values from mm to m
root=root/1000;
skin=skin/1000;
le_core=le_core/1000;
spar=spar/1000;
te_core=te_core/1000;
te_reinf=te_reinf/1000;
web=web/1000;

%% Load and Prepare Airfoils and Blade Data 
load('Airfoil_layup.mat');
Airfoil.Geometry{1,1}=Airfoil_Geometry1;
Airfoil.Geometry{1,2}=Airfoil_Geometry2;
Airfoil.Geometry{1,3}=Airfoil_Geometry3;
Airfoil.Geometry{1,4}=Airfoil_Geometry4;
Airfoil.Geometry{1,5}=Airfoil_Geometry5;
Airfoil.Geometry{1,6}=Airfoil_Geometry6;
Airfoil.Geometry{1,7}=Airfoil_Geometry7;
Airfoil.Geometry{1,8}=Airfoil_Geometry8;

%load('Blade_layup_static_opt.mat');
load('Blade_layup.mat');



Blade.Radius = Blade_Radius;
Blade.NFoil = Blade_Nfoil+1;
Blade.Chord = Blade_Chord;



%load('NREL5MW.mat','Blade');
%load('NREL5MW (gain scheduled).mat','Blade', 'Airfoil');

%Blade.Radius=Blade.Radius-1.5; %subtracting hub radius blade now goes from 0-61.5
diff=abs(location-Blade.Radius);
I=find(diff==min(diff)); %index for Blade chord to be used
section=Blade.Radius(I)/Blade.Radius(end);

J=Blade.NFoil(I); %index for blade airfoil type

%% Material properties and fixed thicknesses
Ex_gelcoat=3440; % all values are in MPa

%Ex_UD= 41800;
%Ey_UD= 14000;  

%%UPWIND layup
%Ex_UD = 38887;
%Ey_UD = 9000;

%%Brian's layup
Ex_G_UD= 41800;
Ey_G_UD= 14000;
E1_Triax=27700;
E2_Triax=13650;
Ex_DB=13600;
Ey_DB=13300;
E_foam=256;
Ex_C_UD=114500;
Ey_C_UD=8390;

G_gelcoat = 1380; %Shear modulus
G_G_UD = 2630;
G12_Triax = 7200;
G_DB = 11800;
G_foam = 22;
G_C_UD = 5990;

rho_gelcoat=1235;
rho_Triax=1850;
rho_DB=1780;
rho_foam=200;
rho_carbon=1220;
rho_glass=1920;

%%%fixed thicknesses %%%

%thickness in m
t_gelcoat=0.0004;
% t_triax_skin=0.00282;
% t_triax_root=55*0.00094;
% t_double_bias=0.002;
% t_sw_foam=0.05;
% 
% t_le_foam=0*0.001;
% t_UD_C=0*0.00047;
% t_te_foam=0*0.001;
% t_UD_G=0*0.00047;

%%% parameterize individual thicknesses in terms of variables %%% 
% LE PANEL THICKNESS INCLUDES TRIAX SKINS WHILE TE PANEL THICKNESS INCLUDES
% TE FOAM AND TE GLASS FIBRE REINFORCEMENT  
t_triax_skin=skin; % TRIAX SKIN THAT WILL BE USED FOR THE ENTIRE BLADE DEFINITON 
t_triax_root=root; % THICKNESS OF TRIAX ROOT ONLY 
t_double_bias=0.07*web; %THICKNESS OF DOUBLE BIAS AROUND SPAR WEB FOAM
t_sw_foam=0.86*web; %THICKNESS OF SHEAR WEB FOAM

t_le_foam = le_core; 
t_UD_C = spar;
t_te_foam = te_core;
t_UD_G = te_reinf;

%% Find equivalent Ex and Gx for Triax Skins 
% Converting E1 and E2 of Triax to Ex 
v12 = 0.39; % For Triax
alpha = 45; % ply angle 
c= cosd(alpha);
s = sind(alpha);

Ex_ply_45 = 1/((c^4/E1_Triax)+((1/G12_Triax)-(2*v12/E1_Triax))*s^2*c^2+(s^4/E2_Triax));
% It will be the same for -45 ply angle 


Ex_ply_0 = E1_Triax;
t_ply_skin = t_triax_skin/3; % Thickness of one single ply 

Ex_Triax = (Ex_ply_45*2*t_ply_skin + Ex_ply_0*t_ply_skin)/t_triax_skin;


Gx_ply_45 = 1/(((4/E2_Triax)+ (4+8*v12)/E1_Triax -2/G12_Triax)*s^2*c^2 + (s^4+c^4)/G12_Triax);
Gx_ply_0 = G12_Triax; 

G_Triax = (Gx_ply_45*2*t_ply_skin + Gx_ply_0*t_ply_skin)/t_triax_skin;

E = [Ex_Triax, Ex_C_UD, Ex_G_UD]; 


%% Maintain constant width of spar caps and TE Reinf throughout the span 

spar_cap_width=0.6; % absolute value in m
relative_spar_cap_width=spar_cap_width/Blade.Chord(I);

te_reinf_width=0.4; % absolute value in m
rel_te_reinf_width=te_reinf_width/Blade.Chord(I);

if section > 0.75

    te_reinf_width=0; % absolute value in m
    rel_te_reinf_width=te_reinf_width/Blade.Chord(I);
end


%% break down airfoil data in upper and lower half
airfoil=Airfoil.Geometry{1,J};
start=find(airfoil(1,:)== min(airfoil(1,:)));
airfoil_lower_x=airfoil(1,start:end);
airfoil_lower_y=airfoil(2,start:end);

airfoil_lower=[airfoil_lower_x;airfoil_lower_y];

airfoil_upper_x=airfoil(1,start:-1:1);
airfoil_upper_y=airfoil(2,start:-1:1);

airfoil_upper=[airfoil_upper_x;airfoil_upper_y];

%convert to absolute values
airfoil_upper_x_abs=airfoil_upper_x*Blade.Chord(I);
airfoil_upper_y_abs=airfoil_upper_y*Blade.Chord(I);

airfoil_lower_x_abs=airfoil_lower_x*Blade.Chord(I);
airfoil_lower_y_abs=airfoil_lower_y*Blade.Chord(I);

index=find(airfoil_upper_y==max(airfoil_upper_y));
max_thickness_section=airfoil_upper_x(index);

%% Leading edge

%%% leading edge panel

t_eq_le_panel=t_triax_skin*2+t_triax_root+t_gelcoat+t_le_foam;

%le_panel_end_=Blade.PitchAxis(I)-(relative_spar_cap_width)/2;
le_panel_end_=max_thickness_section(1)-(relative_spar_cap_width)/2;

diff=abs(airfoil_upper_x-le_panel_end_);
I_le_panel_end=find(diff==min(diff));
le_panel_end=airfoil_upper_x(I_le_panel_end);
I_le_panel_start=find(airfoil_upper_x==min(airfoil_upper_x));
le_panel_start=airfoil_upper_x(I_le_panel_start);


%% Compute leading edge properties

i=I_le_panel_start:I_le_panel_end-1;

length_element_upper_le(i)=sqrt((airfoil_upper_x_abs(i+1)-airfoil_upper_x_abs(i)).^2+...
    (airfoil_upper_y_abs(i+1)-airfoil_upper_y_abs(i)).^2);
area_element_upper_le(i)=length_element_upper_le(i)*t_eq_le_panel;

length_element_lower_le(i)=sqrt((airfoil_lower_x_abs(i+1)-airfoil_lower_x_abs(i)).^2+...
    (abs(airfoil_lower_y_abs(i+1))-abs(airfoil_lower_y_abs(i))).^2);
area_element_lower_le(i)=length_element_lower_le(i)*t_eq_le_panel;

element_x_upper_le(i)=(airfoil_upper_x_abs(i+1)+airfoil_upper_x_abs(i))/2;
element_y_upper_le(i)=(airfoil_upper_y_abs(i+1)+airfoil_upper_y_abs(i))/2 -(t_eq_le_panel/2);

element_x_lower_le(i)=(airfoil_lower_x_abs(i+1)+airfoil_lower_x_abs(i))/2;
element_y_lower_le(i)=(airfoil_lower_y_abs(i+1)+airfoil_lower_y_abs(i))/2 +(t_eq_le_panel/2);


element_xa_upper_le(i)=element_x_upper_le(i).*area_element_upper_le(i);
element_ya_upper_le(i)=element_y_upper_le(i).*area_element_upper_le(i);

element_xa_lower_le(i)=element_x_lower_le(i).*area_element_lower_le(i);
element_ya_lower_le(i)=element_y_lower_le(i).*area_element_lower_le(i);



xc_le=(sum(element_xa_upper_le)+sum(element_xa_lower_le))/(sum(area_element_upper_le)+sum(area_element_lower_le));
yc_le=(sum(element_ya_upper_le)+sum(element_ya_lower_le))/(sum(area_element_upper_le)+sum(area_element_lower_le));


I_xx_upper_le(i)=(element_y_upper_le(i)-yc_le).^2.*area_element_upper_le(i);
I_xx_lower_le_(i)=(abs(element_y_lower_le(i))+yc_le).^2.*area_element_lower_le(i);

I_yy_upper_le(i)=(element_x_upper_le(i)-xc_le).^2.*area_element_upper_le(i);
I_yy_lower_le(i)=(element_x_lower_le(i)-xc_le).^2.*area_element_lower_le(i);

I_own_xx_le=sum(I_xx_upper_le)+sum(I_xx_lower_le_);
I_own_yy_le=sum(I_yy_upper_le)+sum(I_yy_lower_le);


%%  Spar caps

t_eq_sc=t_gelcoat+2*t_triax_skin+t_triax_root+ t_UD_C;

%spar_cap_end_=Blade.PitchAxis(I)+(relative_spar_cap_width)/2;
spar_cap_end_=max_thickness_section(1)+(relative_spar_cap_width)/2;

diff=abs(airfoil_upper_x-spar_cap_end_);
I_spar_cap_end=find(diff==min(diff));
spar_cap_end=airfoil_upper_x(I_spar_cap_end);
I_spar_cap_start=I_le_panel_end;
spar_cap_start=airfoil_upper_x(I_spar_cap_start);


i=I_spar_cap_start:I_spar_cap_end-1;
no_segments=I_spar_cap_end-I_spar_cap_start;
j=1:no_segments;

length_element_upper_sc(j)=sqrt((airfoil_upper_x_abs(i+1)-airfoil_upper_x_abs(i)).^2+...
    (airfoil_upper_y_abs(i+1)-airfoil_upper_y_abs(i)).^2);
area_element_upper_sc(j)=length_element_upper_sc(j)*t_eq_sc;

length_element_lower_sc(j)=sqrt((airfoil_lower_x_abs(i+1)-airfoil_lower_x_abs(i)).^2+...
    (abs(airfoil_lower_y_abs(i+1))-abs(airfoil_lower_y_abs(i))).^2);
area_element_lower_sc(j)=length_element_lower_sc(j)*t_eq_sc;

element_x_upper_sc(j)=(airfoil_upper_x_abs(i+1)+airfoil_upper_x_abs(i))/2;
element_y_upper_sc(j)=(airfoil_upper_y_abs(i+1)+airfoil_upper_y_abs(i))/2 -(t_eq_sc/2);

element_x_lower_sc(j)=(airfoil_lower_x_abs(i+1)+airfoil_lower_x_abs(i))/2;
element_y_lower_sc(j)=(airfoil_lower_y_abs(i+1)+airfoil_lower_y_abs(i))/2 +(t_eq_sc/2);


element_xa_upper_sc(j)=element_x_upper_sc(j).*area_element_upper_sc(j);
element_ya_upper_sc(j)=element_y_upper_sc(j).*area_element_upper_sc(j);

element_xa_lower_sc(j)=element_x_lower_sc(j).*area_element_lower_sc(j);
element_ya_lower_sc(j)=element_y_lower_sc(j).*area_element_lower_sc(j);



xc_sc=(sum(element_xa_upper_sc)+sum(element_xa_lower_sc))/(sum(area_element_upper_sc)+sum(area_element_lower_sc));
yc_sc=(sum(element_ya_upper_sc)+sum(element_ya_lower_sc))/(sum(area_element_upper_sc)+sum(area_element_lower_sc));



I_xx_upper_sc(j)=(element_y_upper_sc(j)-yc_sc).^2.*area_element_upper_sc(j);
I_xx_lower_sc(i)=(abs(element_y_lower_sc(j))+yc_sc).^2.*area_element_lower_sc(j);

I_yy_upper_sc(j)=(element_x_upper_sc(j)-xc_sc).^2.*area_element_upper_sc(j);
I_yy_lower_sc(j)=(element_x_lower_sc(j)-xc_sc).^2.*area_element_lower_sc(j);

I_own_xx_sc=sum(I_xx_upper_sc)+sum(I_xx_lower_sc);
I_own_yy_sc=sum(I_yy_upper_sc)+sum(I_yy_lower_sc);


%% Trailing edge Re-inforcement properties

t_eq_te_reinf=t_gelcoat+2*t_triax_skin+t_triax_root+t_UD_G+t_te_foam;

I_te_reinf_end=find(airfoil_upper_x==max(airfoil_upper_x));
te_reinf_end=airfoil_upper_x(I_te_reinf_end);

te_reinf_start_=te_reinf_end-rel_te_reinf_width;
diff=abs(airfoil_upper_x-te_reinf_start_);
I_te_reinf_start=find(diff==min(diff));
te_reinf_start=airfoil_upper_x(I_te_reinf_start);


i=I_te_reinf_start:I_te_reinf_end-1;
no_segments=I_te_reinf_end-I_te_reinf_start;
j=1:no_segments;

length_element_upper_te_reinf(j)=sqrt((airfoil_upper_x_abs(i+1)-airfoil_upper_x_abs(i)).^2+...
    (airfoil_upper_y_abs(i+1)-airfoil_upper_y_abs(i)).^2);
area_element_upper_te_reinf(j)=length_element_upper_te_reinf(j)*t_eq_te_reinf;

length_element_lower_te_reinf(j)=sqrt((airfoil_lower_x_abs(i+1)-airfoil_lower_x_abs(i)).^2+...
    (abs(airfoil_lower_y_abs(i+1))-abs(airfoil_lower_y_abs(i))).^2);
area_element_lower_te_reinf(j)=length_element_lower_te_reinf(j)*t_eq_te_reinf;

element_x_upper_te_reinf(j)=(airfoil_upper_x_abs(i+1)+airfoil_upper_x_abs(i))/2;
element_y_upper_te_reinf(j)=(airfoil_upper_y_abs(i+1)+airfoil_upper_y_abs(i))/2 -(t_eq_te_reinf/2);

element_x_lower_te_reinf(j)=(airfoil_lower_x_abs(i+1)+airfoil_lower_x_abs(i))/2;
element_y_lower_te_reinf(j)=(airfoil_lower_y_abs(i+1)+airfoil_lower_y_abs(i))/2 +(t_eq_te_reinf/2);


element_xa_upper_te_reinf(j)=element_x_upper_te_reinf(j).*area_element_upper_te_reinf(j);
element_ya_upper_te_reinf(j)=element_y_upper_te_reinf(j).*area_element_upper_te_reinf(j);

element_xa_lower_te_reinf(j)=element_x_lower_te_reinf(j).*area_element_lower_te_reinf(j);
element_ya_lower_te_reinf(j)=element_y_lower_te_reinf(j).*area_element_lower_te_reinf(j);


xc_te_reinf=(sum(element_xa_upper_te_reinf)+sum(element_xa_lower_te_reinf))/(sum(area_element_upper_te_reinf)+sum(area_element_lower_te_reinf));
yc_te_reinf=(sum(element_ya_upper_te_reinf)+sum(element_ya_lower_te_reinf))/(sum(area_element_upper_te_reinf)+sum(area_element_lower_te_reinf));


I_xx_upper_te_reinf(j)=(element_y_upper_te_reinf(j)-yc_te_reinf).^2.*area_element_upper_te_reinf(j);
I_xx_lower_te_reinf(i)=(abs(element_y_lower_te_reinf(j))+yc_te_reinf).^2.*area_element_lower_te_reinf(j);

I_yy_upper_te_reinf(j)=(element_x_upper_te_reinf(j)-xc_te_reinf).^2.*area_element_upper_te_reinf(j);
I_yy_lower_te_reinf(j)=(element_x_lower_te_reinf(j)-xc_te_reinf).^2.*area_element_lower_te_reinf(j);

I_own_xx_te_reinf=sum(I_xx_upper_te_reinf)+sum(I_xx_lower_te_reinf);
I_own_yy_te_reinf=sum(I_yy_upper_te_reinf)+sum(I_yy_lower_te_reinf);

if section > 0.75
    
    xc_te_reinf = 0;
    yc_te_reinf = 0;
    I_own_xx_te_reinf = 0;
    I_own_yy_te_reinf = 0;
end


%% Trailing edge properties

t_eq_te_panel=t_gelcoat+2*t_triax_skin+t_triax_root+t_te_foam;

I_te_panel_start=I_spar_cap_end;
te_panel_start=airfoil_upper_x(I_te_panel_start);
I_te_panel_end=I_te_reinf_start;
te_panel_end=airfoil_upper_x(I_te_panel_end);


i=I_te_panel_start:I_te_panel_end-1;
no_segments=I_te_panel_end-I_te_panel_start;
j=1:no_segments;

length_element_upper_te(j)=sqrt((airfoil_upper_x_abs(i+1)-airfoil_upper_x_abs(i)).^2+...
    (airfoil_upper_y_abs(i+1)-airfoil_upper_y_abs(i)).^2);
area_element_upper_te(j)=length_element_upper_te(j)*t_eq_te_panel;

length_element_lower_te(j)=sqrt((airfoil_lower_x_abs(i+1)-airfoil_lower_x_abs(i)).^2+...
    (abs(airfoil_lower_y_abs(i+1))-abs(airfoil_lower_y_abs(i))).^2);
area_element_lower_te(j)=length_element_lower_te(j)*t_eq_te_panel;

element_x_upper_te(j)=(airfoil_upper_x_abs(i+1)+airfoil_upper_x_abs(i))/2;
element_y_upper_te(j)=(airfoil_upper_y_abs(i+1)+airfoil_upper_y_abs(i))/2 -(t_eq_te_panel/2);

element_x_lower_te(j)=(airfoil_lower_x_abs(i+1)+airfoil_lower_x_abs(i))/2;
element_y_lower_te(j)=(airfoil_lower_y_abs(i+1)+airfoil_lower_y_abs(i))/2 +(t_eq_te_panel/2);


element_xa_upper_te(j)=element_x_upper_te(j).*area_element_upper_te(j);
element_ya_upper_te(j)=element_y_upper_te(j).*area_element_upper_te(j);

element_xa_lower_te(j)=element_x_lower_te(j).*area_element_lower_te(j);
element_ya_lower_te(j)=element_y_lower_te(j).*area_element_lower_te(j);


xc_te=(sum(element_xa_upper_te)+sum(element_xa_lower_te))/(sum(area_element_upper_te)+sum(area_element_lower_te));
yc_te=(sum(element_ya_upper_te)+sum(element_ya_lower_te))/(sum(area_element_upper_te)+sum(area_element_lower_te));


I_xx_upper_te(j)=(element_y_upper_te(j)-yc_te).^2.*area_element_upper_te(j);
I_xx_lower_te(i)=(abs(element_y_lower_te(j))+yc_te).^2.*area_element_lower_te(j);

I_yy_upper_te(j)=(element_x_upper_te(j)-xc_te).^2.*area_element_upper_te(j);
I_yy_lower_te(j)=(element_x_lower_te(j)-xc_te).^2.*area_element_lower_te(j);

I_own_xx_te=sum(I_xx_upper_te)+sum(I_xx_lower_te);
I_own_yy_te=sum(I_yy_upper_te)+sum(I_yy_lower_te);


%% Shear webs

t_eq_sw=2*t_double_bias+t_sw_foam;

I_shear_web1_start=I_spar_cap_start;
shear_web1_start=airfoil_upper_x(I_shear_web1_start);
diff=abs(airfoil_upper_x-(shear_web1_start+(t_eq_sw/Blade.Chord(I))));
I_shear_web1_end=find(diff==min(diff));
shear_web1_end=airfoil_upper_x(I_shear_web1_end);

I_shear_web1=round((I_shear_web1_start+I_shear_web1_end)/2);
y_upper_shear_web1=airfoil_upper_y_abs(I_shear_web1)-t_eq_sc;
y_lower_shear_web1=airfoil_lower_y_abs(I_shear_web1)+t_eq_sc;


yc_sw1=(y_upper_shear_web1+y_lower_shear_web1)/2;
xc_sw1=((shear_web1_start+shear_web1_end)/2)*Blade.Chord(I);
area_shear_web1=(y_upper_shear_web1-y_lower_shear_web1)*t_eq_sw;

I_shear_web2_end=I_spar_cap_end;
shear_web2_end=airfoil_upper_x(I_spar_cap_end);
diff=abs(airfoil_upper_x-(shear_web2_end-(t_eq_sw/Blade.Chord(I))));
I_shear_web2_start=find(diff==min(diff));
shear_web2_start=airfoil_upper_x(I_shear_web2_start);

I_shear_web2=round((I_shear_web2_start+I_shear_web2_end)/2);
y_upper_shear_web2=airfoil_upper_y_abs(I_shear_web2)-t_eq_sc;
y_lower_shear_web2=airfoil_lower_y_abs(I_shear_web2)+t_eq_sc;

yc_sw2=(y_upper_shear_web2+y_lower_shear_web2)/2;
xc_sw2=((shear_web2_start+shear_web2_end)/2)*Blade.Chord(I);
area_shear_web2=(y_upper_shear_web2-y_lower_shear_web2)*t_eq_sw;

xc_sw=(xc_sw1*area_shear_web1+xc_sw2*area_shear_web2)/(area_shear_web1+area_shear_web2);
yc_sw=(yc_sw1*area_shear_web1+yc_sw2*area_shear_web2)/(area_shear_web1+area_shear_web2);

I_xx_sw1=(yc_sw1-yc_sw)^2*area_shear_web1;
I_xx_sw2=(yc_sw2-yc_sw)^2*area_shear_web2;

I_yy_sw1=(xc_sw1-xc_sw)^2*area_shear_web1;
I_yy_sw2=(xc_sw2-xc_sw)^2*area_shear_web2;

I_own_xx_sw=I_xx_sw1+I_xx_sw2;
I_own_yy_sw=I_yy_sw1+I_yy_sw2;

if section >0.95
    I_own_xx_sw=0;
    I_own_yy_sw=0;
end

%% Section centroids and parallel axis

E_equivalent_le_x=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_le_foam*E_foam)/t_eq_le_panel; % in MPa
E_equivalent_le_y=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_le_foam*E_foam)/t_eq_le_panel;
G_equivalent_le = (t_gelcoat*G_gelcoat+2*t_triax_skin*G_Triax+ t_triax_root*G_Triax+t_le_foam*G_foam)/t_eq_le_panel;

E_equivalent_sc_x=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_UD_C*Ex_C_UD)/t_eq_sc;
E_equivalent_sc_y=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_UD_C*Ex_C_UD)/t_eq_sc;
G_equivalent_sc = (t_gelcoat*G_gelcoat+2*t_triax_skin*G_Triax+ t_triax_root*G_Triax+t_UD_C*G_C_UD)/t_eq_sc;

E_equivalent_te_x=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_te_foam*E_foam)/t_eq_te_panel; % in MPa
E_equivalent_te_y=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_te_foam*E_foam)/t_eq_te_panel;
G_equivalent_te = (t_gelcoat*G_gelcoat+2*t_triax_skin*G_Triax+ t_triax_root*G_Triax+t_te_foam*G_foam)/t_eq_te_panel;

E_equivalent_te_reinf_x=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_te_foam*E_foam+t_UD_G*Ex_G_UD)/t_eq_te_reinf; % in MPa
E_equivalent_te_reinf_y=(t_gelcoat*Ex_gelcoat+2*t_triax_skin*Ex_Triax+ t_triax_root*Ex_Triax+t_te_foam*E_foam+t_UD_G*Ex_G_UD)/t_eq_te_reinf;
G_equivalent_te_reinf = (t_gelcoat*G_gelcoat+2*t_triax_skin*G_Triax+ t_triax_root*G_Triax+t_te_foam*G_foam+t_UD_G*G_G_UD)/t_eq_te_reinf;

E_equivalent_sw_x=(2*t_double_bias*Ex_DB+t_sw_foam*E_foam)/t_eq_sw; %in MPa
E_equivalent_sw_y=(2*t_double_bias*Ey_DB+t_sw_foam*E_foam)/t_eq_sw; %in MPa
G_equivalent_sw = (2*t_double_bias*G_DB+t_sw_foam*G_foam)/t_eq_sw; %in MPa

Area_equivalent_le=sum(area_element_upper_le)+sum(area_element_lower_le);
Area_equivalent_sc=sum(area_element_upper_sc)+sum(area_element_lower_sc);
Area_equivalent_te=sum(area_element_upper_te)+sum(area_element_lower_te);
Area_equivalent_te_reinf=sum(area_element_upper_te_reinf)+sum(area_element_lower_te_reinf);
Area_equivalent_sw=area_shear_web1+area_shear_web2;

if section>0.75
    Area_equivalent_te_reinf = 0;
end

if section >0.95
    Area_equivalent_sw=0;
end

    
xc_section=(E_equivalent_le_x*Area_equivalent_le*xc_le+E_equivalent_sc_x*Area_equivalent_sc*xc_sc...
    +E_equivalent_te_x*Area_equivalent_te*xc_te+E_equivalent_sw_x*Area_equivalent_sw*xc_sw+E_equivalent_te_reinf_x*Area_equivalent_te_reinf*xc_te_reinf)/...
    (E_equivalent_le_x*Area_equivalent_le+E_equivalent_sc_x*Area_equivalent_sc...
    +E_equivalent_te_x*Area_equivalent_te+E_equivalent_sw_x*Area_equivalent_sw+ E_equivalent_te_reinf_x*Area_equivalent_te_reinf);

yc_section=(E_equivalent_le_x*Area_equivalent_le*yc_le+E_equivalent_sc_x*Area_equivalent_sc*yc_sc...
    +E_equivalent_te_x*Area_equivalent_te*yc_te+E_equivalent_sw_x*Area_equivalent_sw*yc_sw+E_equivalent_te_reinf_x*Area_equivalent_te_reinf*yc_te_reinf)/...
    (E_equivalent_le_x*Area_equivalent_le+E_equivalent_sc_x*Area_equivalent_sc...
    +E_equivalent_te_x*Area_equivalent_te+E_equivalent_sw_y*Area_equivalent_sw+E_equivalent_te_reinf_y*Area_equivalent_te_reinf);

rel_xc_section=xc_section/Blade.Chord(I);
rel_yc_section=yc_section/Blade.Chord(I);

rho_equivalent_le=(rho_gelcoat*t_gelcoat+rho_Triax*t_triax_skin*2+ rho_Triax*t_triax_root+rho_foam*t_le_foam)/t_eq_le_panel;
rho_equivalent_sc=(rho_gelcoat*t_gelcoat+rho_Triax*t_triax_skin*2+ rho_Triax*t_triax_root+rho_carbon*t_UD_C)/t_eq_sc;
rho_equivalent_te_reinf=(rho_gelcoat*t_gelcoat+rho_Triax*t_triax_skin*2+ rho_Triax*t_triax_root+rho_foam*t_te_foam+rho_glass*t_UD_G)/t_eq_te_reinf;
rho_equivalent_te=(rho_gelcoat*t_gelcoat+rho_Triax*t_triax_skin*2+ rho_Triax*t_triax_root+rho_foam*t_te_foam)/t_eq_te_panel;
rho_equivalent_sw=(rho_DB*2*t_double_bias+rho_foam*t_sw_foam)/t_eq_sw;

%% M.O.I. about section centroid

I_xx_LE=I_own_xx_le+Area_equivalent_le*(yc_le-yc_section)^2;
I_xx_SC=I_own_xx_sc+ Area_equivalent_sc*(yc_sc-yc_section)^2;
I_xx_TE=I_own_xx_te+Area_equivalent_te*(yc_te-yc_section)^2;
I_xx_TE_REINF=I_own_xx_te_reinf+Area_equivalent_te_reinf*(yc_te_reinf-yc_section)^2;
I_xx_SW=I_own_xx_sw+ Area_equivalent_sw*(yc_sw-yc_section)^2;

I_xx = I_xx_LE + I_xx_SC + I_xx_TE + I_xx_TE_REINF + I_xx_SW; % flapwise MOI

I_yy_LE=I_own_yy_le+Area_equivalent_le*(xc_le-xc_section)^2;
I_yy_SC=I_own_yy_sc+ Area_equivalent_sc*(xc_sc-xc_section)^2;
I_yy_TE=I_own_yy_te+Area_equivalent_te*(xc_te-xc_section)^2;
I_yy_TE_REINF=I_own_yy_te_reinf+Area_equivalent_te_reinf*(xc_te_reinf-xc_section)^2;
I_yy_SW=I_own_yy_sw+ Area_equivalent_sw*(xc_sw-xc_section)^2;

I_yy = I_yy_LE + I_yy_SC + I_yy_TE + I_yy_TE_REINF + I_yy_SW; %edgewise MOI

G_LE = I_xx_LE + I_yy_LE;
G_SC = I_xx_SC + I_yy_SC;
G_TE = I_xx_TE + I_yy_TE;
G_TE_REINF = I_xx_TE_REINF + I_yy_TE_REINF;
G_SW = I_xx_SW + I_yy_SW;


%% Final Results

    

EI_flap=(E_equivalent_le_x*I_xx_LE+ E_equivalent_sc_x*I_xx_SC+...
    E_equivalent_te_x*I_xx_TE+E_equivalent_sw_x*I_xx_SW+ E_equivalent_te_reinf_x*I_xx_TE_REINF)*10^6;

EI_edge=(E_equivalent_le_y*I_yy_LE+ E_equivalent_sc_y*I_yy_SC+...
    E_equivalent_te_y*I_yy_TE+E_equivalent_sw_y*I_yy_SW+ E_equivalent_te_reinf_y*I_yy_TE_REINF)*10^6;

G_stiffness = (G_equivalent_le*G_LE+ G_equivalent_sc*G_SC+...
    G_equivalent_te*G_TE+G_equivalent_sw*G_SW+ G_equivalent_te_reinf*G_TE_REINF)*10^6;

EA = (E_equivalent_le_x*Area_equivalent_le+ E_equivalent_sc_x*Area_equivalent_sc+...
    E_equivalent_te_x*Area_equivalent_te+E_equivalent_sw_x*Area_equivalent_sw+ E_equivalent_te_reinf_x*Area_equivalent_te_reinf)*10^6/((Blade.Radius(end)-Blade.Radius(1))/48);

M_L=rho_equivalent_le*Area_equivalent_le+rho_equivalent_sc*Area_equivalent_sc+rho_equivalent_te_reinf*Area_equivalent_te_reinf...
    +rho_equivalent_te*Area_equivalent_te+rho_equivalent_sw*Area_equivalent_sw;



%% For stress analysis
%%% Stress check at spar cap, skin at spar cap, TE reinforcement and skin
%%% at TE reinforcement

y_flapwise_spar = max(element_y_upper_sc);
y_flapwise_skin = max(element_y_upper_sc)+(t_eq_sc/2)-(t_triax_skin/2);


if section > 0.75
    
y_edgewise_te_reinf = max(element_x_upper_te)-xc_section;
y_edgewise_skin = max(element_x_upper_te) + (t_eq_te_panel/2)-(t_triax_skin/2)-xc_section;

else

y_edgewise_te_reinf = max(element_x_upper_te_reinf)-xc_section;
y_edgewise_skin = max(element_x_upper_te_reinf) + (t_eq_te_reinf/2)-(t_triax_skin/2)-xc_section;

end



end
