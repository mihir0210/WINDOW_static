function [Fatigue, DEL]= Fatigue_calculator_detailed(Stress, slope, UCS)
 %load([pwd,'\Stress.mat']);
  
fatigue_sf = 1.38;
Stress_ts = fatigue_sf*Stress;
 
%% Cumulative probabilites of different wind speed bins
Fatigue_speeds=4:24;
j=1;
prob=zeros(1,21);
for i=Fatigue_speeds
    prob(j)=PDF_detailed(i);
    j=j+1;
end

%% Rainflow and fatigue calculation


%Stress_ts is a matrix wherein each row is a time series 
Range={};
for i=1:size(Stress_ts,1)
    Range{i}=rainflow(Stress_ts(i,:));
end

for i=1:length(Range)
    Range{1,i}(Range{1,i}==0)=[];
    upper(i)=ceil(max(Range{1,i}));
end

% hist=histogram(Range,upper); 
% ylabel('Number of Occurences');
% xlabel('Stress Range (MPa)');

%Determine cycles to failure from S-N
% UCS is the ultimate compressive strength in MPa
bincounts={};
abs_value={};
for i=1:size(Stress_ts)
bincounts{i}= histcounts(Range{1,i},0:upper(i));
abs_value{i}=zeros(1,upper(i));
x=-0.5; 
abs_value{i}=x+1:upper(i);

N_failure{i}=10.^(slope*(log10(UCS)-log10(abs_value{i})+log10(2)));
Eq_damage{i}=sum(bincounts{i}./N_failure{i});
Damage(i)=Eq_damage{i}*prob(i)*8760*6*20; %no of 10 minute periods
end

Fatigue=sum(Damage);

%%% Assume a load of frequency 1 Hz and calculate Damage equivalent load

n=20*8760*3600; %no of cycles for a load of 1 Hz

% Get cycles to failure for this frequency of load and damage
% equal to the fatigue damage obtained

N_failure_new=n/Fatigue; 

%Calculate Stress that corresponds to this N
DEL=10^(log10(UCS)-(log10(N_failure_new)/slope));













