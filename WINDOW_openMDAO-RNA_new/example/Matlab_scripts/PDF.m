%% determine cumulative probability for fatigue
function [prob]=PDF(velocity)
% avg_speed=10; % 10m/s for class 1
% k=2; % assumed for Rayleigh and weibull
% C=avg_speed/gamma(1+(1/k));
% syms V 
% P=1-exp(-(V/C)^k);
% Cpdf=matlabFunction(P);

avg_speed=10; % 10m/s for class 1
% for Rayleigh distribution
syms V 
P=1-exp(-pi*(V/(2*avg_speed))^2);
Cpdf=matlabFunction(P);


%% probability for different bin sizes
if velocity==6
prob=Cpdf(6)-Cpdf(0); % bin size 0 to 6
end
if velocity==8
prob=Cpdf(10)-Cpdf(6);% bin size 6 to 10
end

if velocity==12
prob=Cpdf(14)-Cpdf(10); %bin size 10 to 14
end

if velocity==16
prob=Cpdf(18)-Cpdf(14); %bin size 14 to 18
end

if velocity==20
prob=Cpdf(22)-Cpdf(18); %bin size 18 to 22
end

if velocity==23.5
prob=Cpdf(25)-Cpdf(22); %bin size 22 to 25
end





