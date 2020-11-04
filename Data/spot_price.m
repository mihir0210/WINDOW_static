%%  spot time series

NL_spot_2018 = csvread('Day_ahead_Prices_NL.csv', 1,1);

NL_spot_2018(1) =[];

csvwrite('NL_spot_2018.csv', NL_spot_2018); 

%%

DK_spot_2018 = csvread('Day_ahead_Prices_DK.csv', 1,1);

DK_spot_2018(1) =[];

csvwrite('DK_spot_2018.csv', DK_spot_2018); 


