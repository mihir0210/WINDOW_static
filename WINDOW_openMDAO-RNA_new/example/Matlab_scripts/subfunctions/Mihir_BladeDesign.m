function Blade=Mihir_BladeDesign
%% read standard blade
std_blade=csvread('AeroDyn_blade.csv'); 
%% taking values from the optimizer, where chord and twist are design variables
Blade.length=61.499;
Blade.span_1=0;
Blade.span_2=10.25; % in m
Blade.span_3=24.34;
Blade.span_4=46.125;
Blade.span_5=60.218;
Blade.span_6=61.499; 
span=[Blade.span_1 Blade.span_2 Blade.span_3 Blade.span_4 Blade.span_5 Blade.span_6];
Blade.chord_1=3.386; % at x=0
Blade.chord_2=4.557; % at span 1
Blade.chord_3=4.1464; 
Blade.chord_4=2.8255;
Blade.chord_5=1.39; 
Blade.chord_6=0.96; 
chord=[Blade.chord_1 Blade.chord_2 Blade.chord_3 Blade.chord_4 Blade.chord_5 Blade.chord_6];
Blade.twist_1=13.235;
Blade.twist_2=13.235; % in deg
Blade.twist_3=8.412;
Blade.twist_4=2.4415;
Blade.twist_5=0.0286;
Blade.twist_6=0;
twist=[Blade.twist_1 Blade.twist_2 Blade.twist_3 Blade.twist_4 Blade.twist_5 Blade.twist_6]; 
%% interpolate these to get 49 values 
Blade.span=linspace(0,Blade.length,49);
cf_chord=polyfit(span,chord,4);
cf_twist=polyfit(span,twist,4); 
Blade.chord=cf_chord(1)*Blade.span.^4+cf_chord(2)*Blade.span.^3+cf_chord(3)*Blade.span.^2+...
cf_chord(4)*Blade.span+cf_chord(5);
Blade.twist=cf_twist(1)*Blade.span.^4+cf_twist(2)*Blade.span.^3+cf_twist(3)*Blade.span.^2+...
cf_twist(4)*Blade.span+cf_twist(5);

