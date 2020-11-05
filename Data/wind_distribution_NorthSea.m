%% Read 2014-2019 data %%


% Step 1: Read wind speed data at 100 m for all the years
% Step 2: Fit a weibull distribution to the wind speed data and extract parameters
% Directional probability to be determined later
% Step 3: Collect the timeseries data for 2018 only
% 
% or 
% 
% Step 3: Make a wind-spot correlation from available data

%% Step 1

%%%%% import data in the workspace by opening CSV in the MATLAB reader %%

wind_speed = table2array(KNW1);

wind_speed(wind_speed<0) = 0.1;

%% Step 2

[parmHat,parmCI] = wblfit(wind_speed);

histogram(wind_speed); hold on;

a = parmHat(1); b = parmHat(2);
 
pd = makedist('Weibull', 'a', a, 'b', b); 
X = 0:30;
y = wblpdf(X, a,b);
plot(X,y); 

%% Step 3

% 2014,15,16,17 to be skipped

n_hours_skipped = 8760*3 + 8784; % 2016 being a leap year

%wind_2018_100 = wind_speed(n_hours_skipped:n_hours_skipped + 8759); 
%csvwrite('North_sea_2018_100.csv', wind_2018_100 ); 

wind_2018_150 = wind_speed(n_hours_skipped:n_hours_skipped + 8759); 

csvwrite('North_sea_2018_150.csv', wind_2018_150 ); 



