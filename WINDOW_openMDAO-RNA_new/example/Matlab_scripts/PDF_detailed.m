%% determine cumulative probability for fatigue
function [prob]=PDF_detailed(velocity)
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



%% probability: Bin size is 1 m/s

prob = Cpdf(velocity)-Cpdf(velocity-1);





