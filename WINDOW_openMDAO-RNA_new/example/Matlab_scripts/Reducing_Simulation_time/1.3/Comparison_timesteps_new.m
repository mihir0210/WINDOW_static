%% load main 600 s files 

seed1 = load(fullfile(cd,'New_simulations\DLC1.3_600_seed=1.mat'));
seed2 = load(fullfile(cd,'New_simulations\DLC1.3_600_seed=2.mat'));
seed3 = load(fullfile(cd,'New_simulations\DLC1.3_600_seed=3.mat'));
seed4 = load(fullfile(cd,'New_simulations\DLC1.3_600_seed=4.mat'));
seed5 = load(fullfile(cd,'New_simulations\DLC1.3_600_seed=5.mat'));
seed6 = load(fullfile(cd,'New_simulations\DLC1.3_600_seed=6.mat'));

t_remove = 10; 
NREL_deflection_ss = 5.382;
NREL_rootmoment_ss = 11674; 

%%%% NREL steady state values %%%% 

%---------------Tip Deflections ----------------------
seed1_deflectionb1 = seed1.OoPDefl1; %(1:t_remove/0.008);
seed1_deflectionb2 = seed1.OoPDefl2; %(1:t_remove/0.008);
seed1_deflectionb3 = seed1.OoPDefl3; %(1:t_remove/0.008);

seed2_deflectionb1 = seed2.OoPDefl1; %(1:t_remove/0.008);
seed2_deflectionb2 = seed2.OoPDefl2; %(1:t_remove/0.008);
seed2_deflectionb3 = seed2.OoPDefl3; %(1:t_remove/0.008);

seed3_deflectionb1 = seed3.OoPDefl1; %(1:t_remove/0.008);
seed3_deflectionb2 = seed3.OoPDefl2; %(1:t_remove/0.008);
seed3_deflectionb3 = seed3.OoPDefl3; %(1:t_remove/0.008);

seed4_deflectionb1 = seed4.OoPDefl1; %(1:t_remove/0.008);
seed4_deflectionb2 = seed4.OoPDefl2; %(1:t_remove/0.008);
seed4_deflectionb3 = seed4.OoPDefl3; %(1:t_remove/0.008);

seed5_deflectionb1 = seed5.OoPDefl1; %(1:t_remove/0.008);
seed5_deflectionb2 = seed5.OoPDefl2; %(1:t_remove/0.008);
seed5_deflectionb3 = seed5.OoPDefl3; %(1:t_remove/0.008);

seed6_deflectionb1 = seed6.OoPDefl1; %(1:t_remove/0.008);
seed6_deflectionb2 = seed6.OoPDefl2; %(1:t_remove/0.008);
seed6_deflectionb3 = seed6.OoPDefl3; %(1:t_remove/0.008);
                    
%----------------------- Root Moments ----------------------------
seed1_rootflap1 = seed1.RootMFlp1; %(1:t_remove/0.008);
seed1_rootflap2 = seed1.RootMFlp2; %(1:t_remove/0.008);
seed1_rootflap3 = seed1.RootMFlp3; %(1:t_remove/0.008);
seed1_rootedge1 = seed1.RootMEdg1; %(1:t_remove/0.008);
seed1_rootedge2 = seed1.RootMEdg2; %(1:t_remove/0.008);
seed1_rootedge3 = seed1.RootMEdg3; %(1:t_remove/0.008);

seed2_rootflap1 = seed2.RootMFlp1; %(1:t_remove/0.008);
seed2_rootflap2 = seed2.RootMFlp2;%(1:t_remove/0.008);
seed2_rootflap3 = seed2.RootMFlp3; %(1:t_remove/0.008);
seed2_rootedge1 = seed2.RootMEdg1; %(1:t_remove/0.008);
seed2_rootedge2 = seed2.RootMEdg2; %(1:t_remove/0.008);
seed2_rootedge3 = seed2.RootMEdg3; %(1:t_remove/0.008);

seed3_rootflap1 = seed3.RootMFlp1; %(1:t_remove/0.008);
seed3_rootflap2 = seed3.RootMFlp2; %(1:t_remove/0.008);
seed3_rootflap3 = seed3.RootMFlp3; %(1:t_remove/0.008);
seed3_rootedge1 = seed3.RootMEdg1; %(1:t_remove/0.008);
seed3_rootedge2 = seed3.RootMEdg2; %(1:t_remove/0.008);
seed3_rootedge3 = seed3.RootMEdg3; %(1:t_remove/0.008);

seed4_rootflap1 = seed4.RootMFlp1; %(1:t_remove/0.008);
seed4_rootflap2 = seed4.RootMFlp2; %(1:t_remove/0.008);
seed4_rootflap3 = seed4.RootMFlp3; %(1:t_remove/0.008);
seed4_rootedge1 = seed4.RootMEdg1; %(1:t_remove/0.008);
seed4_rootedge2 = seed4.RootMEdg2; %(1:t_remove/0.008);
seed4_rootedge3 = seed4.RootMEdg3; %(1:t_remove/0.008);

seed5_rootflap1 = seed5.RootMFlp1; %(1:t_remove/0.008);
seed5_rootflap2 = seed5.RootMFlp2; %(1:t_remove/0.008);
seed5_rootflap3 = seed5.RootMFlp3; %(1:t_remove/0.008);
seed5_rootedge1 = seed5.RootMEdg1; %(1:t_remove/0.008);
seed5_rootedge2 = seed5.RootMEdg2; %(1:t_remove/0.008);
seed5_rootedge3 = seed5.RootMEdg3; %(1:t_remove/0.008);

seed6_rootflap1 = seed6.RootMFlp1; %(1:t_remove/0.008);
seed6_rootflap2 = seed6.RootMFlp2; %(1:t_remove/0.008);
seed6_rootflap3 = seed6.RootMFlp3; %(1:t_remove/0.008);
seed6_rootedge1 = seed6.RootMEdg1; %(1:t_remove/0.008);
seed6_rootedge2 = seed6.RootMEdg2; %(1:t_remove/0.008);
seed6_rootedge3 = seed6.RootMEdg3; %(1:t_remove/0.008);




%% Compare Tip deflections

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 70 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_deflectionb1_70 = seed1_deflectionb1(1:70/0.008);
seed1_deflectionb2_70 = seed1_deflectionb2(1:70/0.008);
seed1_deflectionb3_70 = seed1_deflectionb3(1:70/0.008);


seed2_deflectionb1_70 = seed2_deflectionb1(1:70/0.008);
seed2_deflectionb2_70 = seed2_deflectionb2(1:70/0.008);
seed2_deflectionb3_70 = seed2_deflectionb3(1:70/0.008);

seed3_deflectionb1_70 = seed3_deflectionb1(1:70/0.008);
seed3_deflectionb2_70 = seed3_deflectionb2(1:70/0.008);
seed3_deflectionb3_70 = seed3_deflectionb3(1:70/0.008);


seed4_deflectionb1_70 = seed4_deflectionb1(1:70/0.008);
seed4_deflectionb2_70 = seed4_deflectionb2(1:70/0.008);
seed4_deflectionb3_70 = seed4_deflectionb3(1:70/0.008);


seed5_deflectionb1_70 = seed5_deflectionb1(1:70/0.008);
seed5_deflectionb2_70 = seed5_deflectionb2(1:70/0.008);
seed5_deflectionb3_70 = seed5_deflectionb3(1:70/0.008);


seed6_deflectionb1_70 = seed6_deflectionb1(1:70/0.008);
seed6_deflectionb2_70 = seed6_deflectionb2(1:70/0.008);
seed6_deflectionb3_70 = seed6_deflectionb3(1:70/0.008);

seed1_deflectionb1_70(1:t_remove/0.008)=[];
seed1_deflectionb2_70(1:t_remove/0.008)=[];
seed1_deflectionb3_70(1:t_remove/0.008)=[];
seed2_deflectionb1_70(1:t_remove/0.008)=[];
seed2_deflectionb2_70(1:t_remove/0.008)=[];
seed2_deflectionb3_70(1:t_remove/0.008)=[];
seed3_deflectionb1_70(1:t_remove/0.008)=[];
seed3_deflectionb2_70(1:t_remove/0.008)=[];
seed3_deflectionb3_70(1:t_remove/0.008)=[];
seed4_deflectionb1_70(1:t_remove/0.008)=[];
seed4_deflectionb2_70(1:t_remove/0.008)=[];
seed4_deflectionb3_70(1:t_remove/0.008)=[];
seed5_deflectionb1_70(1:t_remove/0.008)=[];
seed5_deflectionb2_70(1:t_remove/0.008)=[];
seed5_deflectionb3_70(1:t_remove/0.008)=[];
seed6_deflectionb1_70(1:t_remove/0.008)=[];
seed6_deflectionb2_70(1:t_remove/0.008)=[];
seed6_deflectionb3_70(1:t_remove/0.008)=[];


seed1_OoPDefl = [seed1_deflectionb1_70; seed1_deflectionb2_70; seed1_deflectionb3_70];
seed2_OoPDefl = [seed2_deflectionb1_70; seed2_deflectionb2_70; seed2_deflectionb3_70];
seed3_OoPDefl = [seed3_deflectionb1_70; seed3_deflectionb2_70; seed3_deflectionb3_70];
seed4_OoPDefl = [seed4_deflectionb1_70; seed4_deflectionb2_70; seed4_deflectionb3_70];
seed5_OoPDefl = [seed5_deflectionb1_70; seed5_deflectionb2_70; seed5_deflectionb3_70];
seed6_OoPDefl = [seed6_deflectionb1_70; seed6_deflectionb2_70; seed6_deflectionb3_70];


tip_seeds70 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_70 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 100 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_deflectionb1_100 = seed1_deflectionb1(1:100/0.008);
seed1_deflectionb2_100 = seed1_deflectionb2(1:100/0.008);
seed1_deflectionb3_100 = seed1_deflectionb3(1:100/0.008);

seed2_deflectionb1_100 = seed2_deflectionb1(1:100/0.008);
seed2_deflectionb2_100 = seed2_deflectionb2(1:100/0.008);
seed2_deflectionb3_100 = seed2_deflectionb3(1:100/0.008);

seed3_deflectionb1_100 = seed3_deflectionb1(1:100/0.008);
seed3_deflectionb2_100 = seed3_deflectionb2(1:100/0.008);
seed3_deflectionb3_100 = seed3_deflectionb3(1:100/0.008);

seed4_deflectionb1_100 = seed4_deflectionb1(1:100/0.008);
seed4_deflectionb2_100 = seed4_deflectionb2(1:100/0.008);
seed4_deflectionb3_100 = seed4_deflectionb3(1:100/0.008);

seed5_deflectionb1_100 = seed5_deflectionb1(1:100/0.008);
seed5_deflectionb2_100 = seed5_deflectionb2(1:100/0.008);
seed5_deflectionb3_100 = seed5_deflectionb3(1:100/0.008);

seed6_deflectionb1_100 = seed6_deflectionb1(1:100/0.008);
seed6_deflectionb2_100 = seed6_deflectionb2(1:100/0.008);
seed6_deflectionb3_100 = seed6_deflectionb3(1:100/0.008);

seed1_deflectionb1_100(1:t_remove/0.008)=[];
seed1_deflectionb2_100(1:t_remove/0.008)=[];
seed1_deflectionb3_100(1:t_remove/0.008)=[];
seed2_deflectionb1_100(1:t_remove/0.008)=[];
seed2_deflectionb2_100(1:t_remove/0.008)=[];
seed2_deflectionb3_100(1:t_remove/0.008)=[];
seed3_deflectionb1_100(1:t_remove/0.008)=[];
seed3_deflectionb2_100(1:t_remove/0.008)=[];
seed3_deflectionb3_100(1:t_remove/0.008)=[];
seed4_deflectionb1_100(1:t_remove/0.008)=[];
seed4_deflectionb2_100(1:t_remove/0.008)=[];
seed4_deflectionb3_100(1:t_remove/0.008)=[];
seed5_deflectionb1_100(1:t_remove/0.008)=[];
seed5_deflectionb2_100(1:t_remove/0.008)=[];
seed5_deflectionb3_100(1:t_remove/0.008)=[];
seed6_deflectionb1_100(1:t_remove/0.008)=[];
seed6_deflectionb2_100(1:t_remove/0.008)=[];
seed6_deflectionb3_100(1:t_remove/0.008)=[];



seed1_OoPDefl = [seed1_deflectionb1_100; seed1_deflectionb2_100; seed1_deflectionb3_100];
seed2_OoPDefl = [seed2_deflectionb1_100; seed2_deflectionb2_100; seed2_deflectionb3_100];
seed3_OoPDefl = [seed3_deflectionb1_100; seed3_deflectionb2_100; seed3_deflectionb3_100];
seed4_OoPDefl = [seed4_deflectionb1_100; seed4_deflectionb2_100; seed4_deflectionb3_100];
seed5_OoPDefl = [seed5_deflectionb1_100; seed5_deflectionb2_100; seed5_deflectionb3_100];
seed6_OoPDefl = [seed6_deflectionb1_100; seed6_deflectionb2_100; seed6_deflectionb3_100];


tip_seeds100 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_100 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 150 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_deflectionb1_150 = seed1_deflectionb1(1:150/0.008);
seed1_deflectionb2_150 = seed1_deflectionb2(1:150/0.008);
seed1_deflectionb3_150 = seed1_deflectionb3(1:150/0.008);

seed2_deflectionb1_150 = seed2_deflectionb1(1:150/0.008);
seed2_deflectionb2_150 = seed2_deflectionb2(1:150/0.008);
seed2_deflectionb3_150 = seed2_deflectionb3(1:150/0.008);

seed3_deflectionb1_150 = seed3_deflectionb1(1:150/0.008);
seed3_deflectionb2_150 = seed3_deflectionb2(1:150/0.008);
seed3_deflectionb3_150 = seed3_deflectionb3(1:150/0.008);

seed4_deflectionb1_150 = seed4_deflectionb1(1:150/0.008);
seed4_deflectionb2_150 = seed4_deflectionb2(1:150/0.008);
seed4_deflectionb3_150 = seed4_deflectionb3(1:150/0.008);

seed5_deflectionb1_150 = seed5_deflectionb1(1:150/0.008);
seed5_deflectionb2_150 = seed5_deflectionb2(1:150/0.008);
seed5_deflectionb3_150 = seed5_deflectionb3(1:150/0.008);

seed6_deflectionb1_150 = seed6_deflectionb1(1:150/0.008);
seed6_deflectionb2_150 = seed6_deflectionb2(1:150/0.008);
seed6_deflectionb3_150 = seed6_deflectionb3(1:150/0.008);

seed1_deflectionb1_150(1:t_remove/0.008)=[];
seed1_deflectionb2_150(1:t_remove/0.008)=[];
seed1_deflectionb3_150(1:t_remove/0.008)=[];
seed2_deflectionb1_150(1:t_remove/0.008)=[];
seed2_deflectionb2_150(1:t_remove/0.008)=[];
seed2_deflectionb3_150(1:t_remove/0.008)=[];
seed3_deflectionb1_150(1:t_remove/0.008)=[];
seed3_deflectionb2_150(1:t_remove/0.008)=[];
seed3_deflectionb3_150(1:t_remove/0.008)=[];
seed4_deflectionb1_150(1:t_remove/0.008)=[];
seed4_deflectionb2_150(1:t_remove/0.008)=[];
seed4_deflectionb3_150(1:t_remove/0.008)=[];
seed5_deflectionb1_150(1:t_remove/0.008)=[];
seed5_deflectionb2_150(1:t_remove/0.008)=[];
seed5_deflectionb3_150(1:t_remove/0.008)=[];
seed6_deflectionb1_150(1:t_remove/0.008)=[];
seed6_deflectionb2_150(1:t_remove/0.008)=[];
seed6_deflectionb3_150(1:t_remove/0.008)=[];


seed1_OoPDefl = [seed1_deflectionb1_150; seed1_deflectionb2_150; seed1_deflectionb3_150];
seed2_OoPDefl = [seed2_deflectionb1_150; seed2_deflectionb2_150; seed2_deflectionb3_150];
seed3_OoPDefl = [seed3_deflectionb1_150; seed3_deflectionb2_150; seed3_deflectionb3_150];
seed4_OoPDefl = [seed4_deflectionb1_150; seed4_deflectionb2_150; seed4_deflectionb3_150];
seed5_OoPDefl = [seed5_deflectionb1_150; seed5_deflectionb2_150; seed5_deflectionb3_150];
seed6_OoPDefl = [seed6_deflectionb1_150; seed6_deflectionb2_150; seed6_deflectionb3_150];


tip_seeds150 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_150 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 200 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_deflectionb1_200 = seed1_deflectionb1(1:200/0.008);
seed1_deflectionb2_200 = seed1_deflectionb2(1:200/0.008);
seed1_deflectionb3_200 = seed1_deflectionb3(1:200/0.008);

seed2_deflectionb1_200 = seed2_deflectionb1(1:200/0.008);
seed2_deflectionb2_200 = seed2_deflectionb2(1:200/0.008);
seed2_deflectionb3_200 = seed2_deflectionb3(1:200/0.008);

seed3_deflectionb1_200 = seed3_deflectionb1(1:200/0.008);
seed3_deflectionb2_200 = seed3_deflectionb2(1:200/0.008);
seed3_deflectionb3_200 = seed3_deflectionb3(1:200/0.008);

seed4_deflectionb1_200 = seed4_deflectionb1(1:200/0.008);
seed4_deflectionb2_200 = seed4_deflectionb2(1:200/0.008);
seed4_deflectionb3_200 = seed4_deflectionb3(1:200/0.008);

seed5_deflectionb1_200 = seed5_deflectionb1(1:200/0.008);
seed5_deflectionb2_200 = seed5_deflectionb2(1:200/0.008);
seed5_deflectionb3_200 = seed5_deflectionb3(1:200/0.008);

seed6_deflectionb1_200 = seed6_deflectionb1(1:200/0.008);
seed6_deflectionb2_200 = seed6_deflectionb2(1:200/0.008);
seed6_deflectionb3_200 = seed6_deflectionb3(1:200/0.008);


seed1_deflectionb1_200(1:t_remove/0.008)=[];
seed1_deflectionb2_200(1:t_remove/0.008)=[];
seed1_deflectionb3_200(1:t_remove/0.008)=[];
seed2_deflectionb1_200(1:t_remove/0.008)=[];
seed2_deflectionb2_200(1:t_remove/0.008)=[];
seed2_deflectionb3_200(1:t_remove/0.008)=[];
seed3_deflectionb1_200(1:t_remove/0.008)=[];
seed3_deflectionb2_200(1:t_remove/0.008)=[];
seed3_deflectionb3_200(1:t_remove/0.008)=[];
seed4_deflectionb1_200(1:t_remove/0.008)=[];
seed4_deflectionb2_200(1:t_remove/0.008)=[];
seed4_deflectionb3_200(1:t_remove/0.008)=[];
seed5_deflectionb1_200(1:t_remove/0.008)=[];
seed5_deflectionb2_200(1:t_remove/0.008)=[];
seed5_deflectionb3_200(1:t_remove/0.008)=[];
seed6_deflectionb1_200(1:t_remove/0.008)=[];
seed6_deflectionb2_200(1:t_remove/0.008)=[];
seed6_deflectionb3_200(1:t_remove/0.008)=[];

seed1_OoPDefl = [seed1_deflectionb1_200; seed1_deflectionb2_200; seed1_deflectionb3_200];
seed2_OoPDefl = [seed2_deflectionb1_200; seed2_deflectionb2_200; seed2_deflectionb3_200];
seed3_OoPDefl = [seed3_deflectionb1_200; seed3_deflectionb2_200; seed3_deflectionb3_200];
seed4_OoPDefl = [seed4_deflectionb1_200; seed4_deflectionb2_200; seed4_deflectionb3_200];
seed5_OoPDefl = [seed5_deflectionb1_200; seed5_deflectionb2_200; seed5_deflectionb3_200];
seed6_OoPDefl = [seed6_deflectionb1_200; seed6_deflectionb2_200; seed6_deflectionb3_200];


tip_seeds200 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_200 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 250 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_deflectionb1_250 = seed1_deflectionb1(1:250/0.008);
seed1_deflectionb2_250 = seed1_deflectionb2(1:250/0.008);
seed1_deflectionb3_250 = seed1_deflectionb3(1:250/0.008);

seed2_deflectionb1_250 = seed2_deflectionb1(1:250/0.008);
seed2_deflectionb2_250 = seed2_deflectionb2(1:250/0.008);
seed2_deflectionb3_250 = seed2_deflectionb3(1:250/0.008);

seed3_deflectionb1_250 = seed3_deflectionb1(1:250/0.008);
seed3_deflectionb2_250 = seed3_deflectionb2(1:250/0.008);
seed3_deflectionb3_250 = seed3_deflectionb3(1:250/0.008);

seed4_deflectionb1_250 = seed4_deflectionb1(1:250/0.008);
seed4_deflectionb2_250 = seed4_deflectionb2(1:250/0.008);
seed4_deflectionb3_250 = seed4_deflectionb3(1:250/0.008);

seed5_deflectionb1_250 = seed5_deflectionb1(1:250/0.008);
seed5_deflectionb2_250 = seed5_deflectionb2(1:250/0.008);
seed5_deflectionb3_250 = seed5_deflectionb3(1:250/0.008);

seed6_deflectionb1_250 = seed6_deflectionb1(1:250/0.008);
seed6_deflectionb2_250 = seed6_deflectionb2(1:250/0.008);
seed6_deflectionb3_250 = seed6_deflectionb3(1:250/0.008);

seed1_deflectionb1_250(1:t_remove/0.008)=[];
seed1_deflectionb2_250(1:t_remove/0.008)=[];
seed1_deflectionb3_250(1:t_remove/0.008)=[];
seed2_deflectionb1_250(1:t_remove/0.008)=[];
seed2_deflectionb2_250(1:t_remove/0.008)=[];
seed2_deflectionb3_250(1:t_remove/0.008)=[];
seed3_deflectionb1_250(1:t_remove/0.008)=[];
seed3_deflectionb2_250(1:t_remove/0.008)=[];
seed3_deflectionb3_250(1:t_remove/0.008)=[];
seed4_deflectionb1_250(1:t_remove/0.008)=[];
seed4_deflectionb2_250(1:t_remove/0.008)=[];
seed4_deflectionb3_250(1:t_remove/0.008)=[];
seed5_deflectionb1_250(1:t_remove/0.008)=[];
seed5_deflectionb2_250(1:t_remove/0.008)=[];
seed5_deflectionb3_250(1:t_remove/0.008)=[];
seed6_deflectionb1_250(1:t_remove/0.008)=[];
seed6_deflectionb2_250(1:t_remove/0.008)=[];
seed6_deflectionb3_250(1:t_remove/0.008)=[];


seed1_OoPDefl = [seed1_deflectionb1_250; seed1_deflectionb2_250; seed1_deflectionb3_250];
seed2_OoPDefl = [seed2_deflectionb1_250; seed2_deflectionb2_250; seed2_deflectionb3_250];
seed3_OoPDefl = [seed3_deflectionb1_250; seed3_deflectionb2_250; seed3_deflectionb3_250];
seed4_OoPDefl = [seed4_deflectionb1_250; seed4_deflectionb2_250; seed4_deflectionb3_250];
seed5_OoPDefl = [seed5_deflectionb1_250; seed5_deflectionb2_250; seed5_deflectionb3_250];
seed6_OoPDefl = [seed6_deflectionb1_250; seed6_deflectionb2_250; seed6_deflectionb3_250];


tip_seeds250 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_250 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 300 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_deflectionb1_300 = seed1_deflectionb1(1:300/0.008);
seed1_deflectionb2_300 = seed1_deflectionb2(1:300/0.008);
seed1_deflectionb3_300 = seed1_deflectionb3(1:300/0.008);

seed2_deflectionb1_300 = seed2_deflectionb1(1:300/0.008);
seed2_deflectionb2_300 = seed2_deflectionb2(1:300/0.008);
seed2_deflectionb3_300 = seed2_deflectionb3(1:300/0.008);

seed3_deflectionb1_300 = seed3_deflectionb1(1:300/0.008);
seed3_deflectionb2_300 = seed3_deflectionb2(1:300/0.008);
seed3_deflectionb3_300 = seed3_deflectionb3(1:300/0.008);

seed4_deflectionb1_300 = seed4_deflectionb1(1:300/0.008);
seed4_deflectionb2_300 = seed4_deflectionb2(1:300/0.008);
seed4_deflectionb3_300 = seed4_deflectionb3(1:300/0.008);

seed5_deflectionb1_300 = seed5_deflectionb1(1:300/0.008);
seed5_deflectionb2_300 = seed5_deflectionb2(1:300/0.008);
seed5_deflectionb3_300 = seed5_deflectionb3(1:300/0.008);

seed6_deflectionb1_300 = seed6_deflectionb1(1:300/0.008);
seed6_deflectionb2_300 = seed6_deflectionb2(1:300/0.008);
seed6_deflectionb3_300 = seed6_deflectionb3(1:300/0.008);

seed1_deflectionb1_300(1:t_remove/0.008)=[];
seed1_deflectionb2_300(1:t_remove/0.008)=[];
seed1_deflectionb3_300(1:t_remove/0.008)=[];
seed2_deflectionb1_300(1:t_remove/0.008)=[];
seed2_deflectionb2_300(1:t_remove/0.008)=[];
seed2_deflectionb3_300(1:t_remove/0.008)=[];
seed3_deflectionb1_300(1:t_remove/0.008)=[];
seed3_deflectionb2_300(1:t_remove/0.008)=[];
seed3_deflectionb3_300(1:t_remove/0.008)=[];
seed4_deflectionb1_300(1:t_remove/0.008)=[];
seed4_deflectionb2_300(1:t_remove/0.008)=[];
seed4_deflectionb3_300(1:t_remove/0.008)=[];
seed5_deflectionb1_300(1:t_remove/0.008)=[];
seed5_deflectionb2_300(1:t_remove/0.008)=[];
seed5_deflectionb3_300(1:t_remove/0.008)=[];
seed6_deflectionb1_300(1:t_remove/0.008)=[];
seed6_deflectionb2_300(1:t_remove/0.008)=[];
seed6_deflectionb3_300(1:t_remove/0.008)=[];


seed1_OoPDefl = [seed1_deflectionb1_300; seed1_deflectionb2_300; seed1_deflectionb3_300];
seed2_OoPDefl = [seed2_deflectionb1_300; seed2_deflectionb2_300; seed2_deflectionb3_300];
seed3_OoPDefl = [seed3_deflectionb1_300; seed3_deflectionb2_300; seed3_deflectionb3_300];
seed4_OoPDefl = [seed4_deflectionb1_300; seed4_deflectionb2_300; seed4_deflectionb3_300];
seed5_OoPDefl = [seed5_deflectionb1_300; seed5_deflectionb2_300; seed5_deflectionb3_300];
seed6_OoPDefl = [seed6_deflectionb1_300; seed6_deflectionb2_300; seed6_deflectionb3_300];


tip_seeds300 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_300 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 350 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_deflectionb1_350 = seed1_deflectionb1(1:350/0.008);
seed1_deflectionb2_350 = seed1_deflectionb2(1:350/0.008);
seed1_deflectionb3_350 = seed1_deflectionb3(1:350/0.008);

seed2_deflectionb1_350 = seed2_deflectionb1(1:350/0.008);
seed2_deflectionb2_350 = seed2_deflectionb2(1:350/0.008);
seed2_deflectionb3_350 = seed2_deflectionb3(1:350/0.008);

seed3_deflectionb1_350 = seed3_deflectionb1(1:350/0.008);
seed3_deflectionb2_350 = seed3_deflectionb2(1:350/0.008);
seed3_deflectionb3_350 = seed3_deflectionb3(1:350/0.008);

seed4_deflectionb1_350 = seed4_deflectionb1(1:350/0.008);
seed4_deflectionb2_350 = seed4_deflectionb2(1:350/0.008);
seed4_deflectionb3_350 = seed4_deflectionb3(1:350/0.008);

seed5_deflectionb1_350 = seed5_deflectionb1(1:350/0.008);
seed5_deflectionb2_350 = seed5_deflectionb2(1:350/0.008);
seed5_deflectionb3_350 = seed5_deflectionb3(1:350/0.008);

seed6_deflectionb1_350 = seed6_deflectionb1(1:350/0.008);
seed6_deflectionb2_350 = seed6_deflectionb2(1:350/0.008);
seed6_deflectionb3_350 = seed6_deflectionb3(1:350/0.008);

seed1_deflectionb1_350(1:t_remove/0.008)=[];
seed1_deflectionb2_350(1:t_remove/0.008)=[];
seed1_deflectionb3_350(1:t_remove/0.008)=[];
seed2_deflectionb1_350(1:t_remove/0.008)=[];
seed2_deflectionb2_350(1:t_remove/0.008)=[];
seed2_deflectionb3_350(1:t_remove/0.008)=[];
seed3_deflectionb1_350(1:t_remove/0.008)=[];
seed3_deflectionb2_350(1:t_remove/0.008)=[];
seed3_deflectionb3_350(1:t_remove/0.008)=[];
seed4_deflectionb1_350(1:t_remove/0.008)=[];
seed4_deflectionb2_350(1:t_remove/0.008)=[];
seed4_deflectionb3_350(1:t_remove/0.008)=[];
seed5_deflectionb1_350(1:t_remove/0.008)=[];
seed5_deflectionb2_350(1:t_remove/0.008)=[];
seed5_deflectionb3_350(1:t_remove/0.008)=[];
seed6_deflectionb1_350(1:t_remove/0.008)=[];
seed6_deflectionb2_350(1:t_remove/0.008)=[];
seed6_deflectionb3_350(1:t_remove/0.008)=[];


seed1_OoPDefl = [seed1_deflectionb1_350; seed1_deflectionb2_350; seed1_deflectionb3_350];
seed2_OoPDefl = [seed2_deflectionb1_350; seed2_deflectionb2_350; seed2_deflectionb3_350];
seed3_OoPDefl = [seed3_deflectionb1_350; seed3_deflectionb2_350; seed3_deflectionb3_350];
seed4_OoPDefl = [seed4_deflectionb1_350; seed4_deflectionb2_350; seed4_deflectionb3_350];
seed5_OoPDefl = [seed5_deflectionb1_350; seed5_deflectionb2_350; seed5_deflectionb3_350];
seed6_OoPDefl = [seed6_deflectionb1_350; seed6_deflectionb2_350; seed6_deflectionb3_350];


tip_seeds350 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_350 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 400 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_deflectionb1_400 = seed1_deflectionb1(1:400/0.008);
seed1_deflectionb2_400 = seed1_deflectionb2(1:400/0.008);
seed1_deflectionb3_400 = seed1_deflectionb3(1:400/0.008);

seed2_deflectionb1_400 = seed2_deflectionb1(1:400/0.008);
seed2_deflectionb2_400 = seed2_deflectionb2(1:400/0.008);
seed2_deflectionb3_400 = seed2_deflectionb3(1:400/0.008);

seed3_deflectionb1_400 = seed3_deflectionb1(1:400/0.008);
seed3_deflectionb2_400 = seed3_deflectionb2(1:400/0.008);
seed3_deflectionb3_400 = seed3_deflectionb3(1:400/0.008);

seed4_deflectionb1_400 = seed4_deflectionb1(1:400/0.008);
seed4_deflectionb2_400 = seed4_deflectionb2(1:400/0.008);
seed4_deflectionb3_400 = seed4_deflectionb3(1:400/0.008);

seed5_deflectionb1_400 = seed5_deflectionb1(1:400/0.008);
seed5_deflectionb2_400 = seed5_deflectionb2(1:400/0.008);
seed5_deflectionb3_400 = seed5_deflectionb3(1:400/0.008);

seed6_deflectionb1_400 = seed6_deflectionb1(1:400/0.008);
seed6_deflectionb2_400 = seed6_deflectionb2(1:400/0.008);
seed6_deflectionb3_400 = seed6_deflectionb3(1:400/0.008);


seed1_deflectionb1_400(1:t_remove/0.008)=[];
seed1_deflectionb2_400(1:t_remove/0.008)=[];
seed1_deflectionb3_400(1:t_remove/0.008)=[];
seed2_deflectionb1_400(1:t_remove/0.008)=[];
seed2_deflectionb2_400(1:t_remove/0.008)=[];
seed2_deflectionb3_400(1:t_remove/0.008)=[];
seed3_deflectionb1_400(1:t_remove/0.008)=[];
seed3_deflectionb2_400(1:t_remove/0.008)=[];
seed3_deflectionb3_400(1:t_remove/0.008)=[];
seed4_deflectionb1_400(1:t_remove/0.008)=[];
seed4_deflectionb2_400(1:t_remove/0.008)=[];
seed4_deflectionb3_400(1:t_remove/0.008)=[];
seed5_deflectionb1_400(1:t_remove/0.008)=[];
seed5_deflectionb2_400(1:t_remove/0.008)=[];
seed5_deflectionb3_400(1:t_remove/0.008)=[];
seed6_deflectionb1_400(1:t_remove/0.008)=[];
seed6_deflectionb2_400(1:t_remove/0.008)=[];
seed6_deflectionb3_400(1:t_remove/0.008)=[];

seed1_OoPDefl = [seed1_deflectionb1_400; seed1_deflectionb2_400; seed1_deflectionb3_400];
seed2_OoPDefl = [seed2_deflectionb1_400; seed2_deflectionb2_400; seed2_deflectionb3_400];
seed3_OoPDefl = [seed3_deflectionb1_400; seed3_deflectionb2_400; seed3_deflectionb3_400];
seed4_OoPDefl = [seed4_deflectionb1_400; seed4_deflectionb2_400; seed4_deflectionb3_400];
seed5_OoPDefl = [seed5_deflectionb1_400; seed5_deflectionb2_400; seed5_deflectionb3_400];
seed6_OoPDefl = [seed6_deflectionb1_400; seed6_deflectionb2_400; seed6_deflectionb3_400];


tip_seeds400 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_400 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 450 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_deflectionb1_450 = seed1_deflectionb1(1:450/0.008);
seed1_deflectionb2_450 = seed1_deflectionb2(1:450/0.008);
seed1_deflectionb3_450 = seed1_deflectionb3(1:450/0.008);

seed2_deflectionb1_450 = seed2_deflectionb1(1:450/0.008);
seed2_deflectionb2_450 = seed2_deflectionb2(1:450/0.008);
seed2_deflectionb3_450 = seed2_deflectionb3(1:450/0.008);

seed3_deflectionb1_450 = seed3_deflectionb1(1:450/0.008);
seed3_deflectionb2_450 = seed3_deflectionb2(1:450/0.008);
seed3_deflectionb3_450 = seed3_deflectionb3(1:450/0.008);

seed4_deflectionb1_450 = seed4_deflectionb1(1:450/0.008);
seed4_deflectionb2_450 = seed4_deflectionb2(1:450/0.008);
seed4_deflectionb3_450 = seed4_deflectionb3(1:450/0.008);

seed5_deflectionb1_450 = seed5_deflectionb1(1:450/0.008);
seed5_deflectionb2_450 = seed5_deflectionb2(1:450/0.008);
seed5_deflectionb3_450 = seed5_deflectionb3(1:450/0.008);

seed6_deflectionb1_450 = seed6_deflectionb1(1:450/0.008);
seed6_deflectionb2_450 = seed6_deflectionb2(1:450/0.008);
seed6_deflectionb3_450 = seed6_deflectionb3(1:450/0.008);


seed1_deflectionb1_450(1:t_remove/0.008)=[];
seed1_deflectionb2_450(1:t_remove/0.008)=[];
seed1_deflectionb3_450(1:t_remove/0.008)=[];
seed2_deflectionb1_450(1:t_remove/0.008)=[];
seed2_deflectionb2_450(1:t_remove/0.008)=[];
seed2_deflectionb3_450(1:t_remove/0.008)=[];
seed3_deflectionb1_450(1:t_remove/0.008)=[];
seed3_deflectionb2_450(1:t_remove/0.008)=[];
seed3_deflectionb3_450(1:t_remove/0.008)=[];
seed4_deflectionb1_450(1:t_remove/0.008)=[];
seed4_deflectionb2_450(1:t_remove/0.008)=[];
seed4_deflectionb3_450(1:t_remove/0.008)=[];
seed5_deflectionb1_450(1:t_remove/0.008)=[];
seed5_deflectionb2_450(1:t_remove/0.008)=[];
seed5_deflectionb3_450(1:t_remove/0.008)=[];
seed6_deflectionb1_450(1:t_remove/0.008)=[];
seed6_deflectionb2_450(1:t_remove/0.008)=[];
seed6_deflectionb3_450(1:t_remove/0.008)=[];

seed1_OoPDefl = [seed1_deflectionb1_450; seed1_deflectionb2_450; seed1_deflectionb3_450];
seed2_OoPDefl = [seed2_deflectionb1_450; seed2_deflectionb2_450; seed2_deflectionb3_450];
seed3_OoPDefl = [seed3_deflectionb1_450; seed3_deflectionb2_450; seed3_deflectionb3_450];
seed4_OoPDefl = [seed4_deflectionb1_450; seed4_deflectionb2_450; seed4_deflectionb3_450];
seed5_OoPDefl = [seed5_deflectionb1_450; seed5_deflectionb2_450; seed5_deflectionb3_450];
seed6_OoPDefl = [seed6_deflectionb1_450; seed6_deflectionb2_450; seed6_deflectionb3_450];


tip_seeds450 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_450 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 500 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_deflectionb1_500 = seed1_deflectionb1(1:500/0.008);
seed1_deflectionb2_500 = seed1_deflectionb2(1:500/0.008);
seed1_deflectionb3_500 = seed1_deflectionb3(1:500/0.008);

seed2_deflectionb1_500 = seed2_deflectionb1(1:500/0.008);
seed2_deflectionb2_500 = seed2_deflectionb2(1:500/0.008);
seed2_deflectionb3_500 = seed2_deflectionb3(1:500/0.008);

seed3_deflectionb1_500 = seed3_deflectionb1(1:500/0.008);
seed3_deflectionb2_500 = seed3_deflectionb2(1:500/0.008);
seed3_deflectionb3_500 = seed3_deflectionb3(1:500/0.008);

seed4_deflectionb1_500 = seed4_deflectionb1(1:500/0.008);
seed4_deflectionb2_500 = seed4_deflectionb2(1:500/0.008);
seed4_deflectionb3_500 = seed4_deflectionb3(1:500/0.008);

seed5_deflectionb1_500 = seed5_deflectionb1(1:500/0.008);
seed5_deflectionb2_500 = seed5_deflectionb2(1:500/0.008);
seed5_deflectionb3_500 = seed5_deflectionb3(1:500/0.008);

seed6_deflectionb1_500 = seed6_deflectionb1(1:500/0.008);
seed6_deflectionb2_500 = seed6_deflectionb2(1:500/0.008);
seed6_deflectionb3_500 = seed6_deflectionb3(1:500/0.008);


seed1_deflectionb1_500(1:t_remove/0.008)=[];
seed1_deflectionb2_500(1:t_remove/0.008)=[];
seed1_deflectionb3_500(1:t_remove/0.008)=[];
seed2_deflectionb1_500(1:t_remove/0.008)=[];
seed2_deflectionb2_500(1:t_remove/0.008)=[];
seed2_deflectionb3_500(1:t_remove/0.008)=[];
seed3_deflectionb1_500(1:t_remove/0.008)=[];
seed3_deflectionb2_500(1:t_remove/0.008)=[];
seed3_deflectionb3_500(1:t_remove/0.008)=[];
seed4_deflectionb1_500(1:t_remove/0.008)=[];
seed4_deflectionb2_500(1:t_remove/0.008)=[];
seed4_deflectionb3_500(1:t_remove/0.008)=[];
seed5_deflectionb1_500(1:t_remove/0.008)=[];
seed5_deflectionb2_500(1:t_remove/0.008)=[];
seed5_deflectionb3_500(1:t_remove/0.008)=[];
seed6_deflectionb1_500(1:t_remove/0.008)=[];
seed6_deflectionb2_500(1:t_remove/0.008)=[];
seed6_deflectionb3_500(1:t_remove/0.008)=[];

seed1_OoPDefl = [seed1_deflectionb1_500; seed1_deflectionb2_500; seed1_deflectionb3_500];
seed2_OoPDefl = [seed2_deflectionb1_500; seed2_deflectionb2_500; seed2_deflectionb3_500];
seed3_OoPDefl = [seed3_deflectionb1_500; seed3_deflectionb2_500; seed3_deflectionb3_500];
seed4_OoPDefl = [seed4_deflectionb1_500; seed4_deflectionb2_500; seed4_deflectionb3_500];
seed5_OoPDefl = [seed5_deflectionb1_500; seed5_deflectionb2_500; seed5_deflectionb3_500];
seed6_OoPDefl = [seed6_deflectionb1_500; seed6_deflectionb2_500; seed6_deflectionb3_500];


tip_seeds500 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_500 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 550 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_deflectionb1_550 = seed1_deflectionb1(1:550/0.008);
seed1_deflectionb2_550 = seed1_deflectionb2(1:550/0.008);
seed1_deflectionb3_550 = seed1_deflectionb3(1:550/0.008);

seed2_deflectionb1_550 = seed2_deflectionb1(1:550/0.008);
seed2_deflectionb2_550 = seed2_deflectionb2(1:550/0.008);
seed2_deflectionb3_550 = seed2_deflectionb3(1:550/0.008);

seed3_deflectionb1_550 = seed3_deflectionb1(1:550/0.008);
seed3_deflectionb2_550 = seed3_deflectionb2(1:550/0.008);
seed3_deflectionb3_550 = seed3_deflectionb3(1:550/0.008);

seed4_deflectionb1_550 = seed4_deflectionb1(1:550/0.008);
seed4_deflectionb2_550 = seed4_deflectionb2(1:550/0.008);
seed4_deflectionb3_550 = seed4_deflectionb3(1:550/0.008);

seed5_deflectionb1_550 = seed5_deflectionb1(1:550/0.008);
seed5_deflectionb2_550 = seed5_deflectionb2(1:550/0.008);
seed5_deflectionb3_550 = seed5_deflectionb3(1:550/0.008);

seed6_deflectionb1_550 = seed6_deflectionb1(1:550/0.008);
seed6_deflectionb2_550 = seed6_deflectionb2(1:550/0.008);
seed6_deflectionb3_550 = seed6_deflectionb3(1:550/0.008);

seed1_deflectionb1_550(1:t_remove/0.008)=[];
seed1_deflectionb2_550(1:t_remove/0.008)=[];
seed1_deflectionb3_550(1:t_remove/0.008)=[];
seed2_deflectionb1_550(1:t_remove/0.008)=[];
seed2_deflectionb2_550(1:t_remove/0.008)=[];
seed2_deflectionb3_550(1:t_remove/0.008)=[];
seed3_deflectionb1_550(1:t_remove/0.008)=[];
seed3_deflectionb2_550(1:t_remove/0.008)=[];
seed3_deflectionb3_550(1:t_remove/0.008)=[];
seed4_deflectionb1_550(1:t_remove/0.008)=[];
seed4_deflectionb2_550(1:t_remove/0.008)=[];
seed4_deflectionb3_550(1:t_remove/0.008)=[];
seed5_deflectionb1_550(1:t_remove/0.008)=[];
seed5_deflectionb2_550(1:t_remove/0.008)=[];
seed5_deflectionb3_550(1:t_remove/0.008)=[];
seed6_deflectionb1_550(1:t_remove/0.008)=[];
seed6_deflectionb2_550(1:t_remove/0.008)=[];
seed6_deflectionb3_550(1:t_remove/0.008)=[];



seed1_OoPDefl = [seed1_deflectionb1_550; seed1_deflectionb2_550; seed1_deflectionb3_550];
seed2_OoPDefl = [seed2_deflectionb1_550; seed2_deflectionb2_550; seed2_deflectionb3_550];
seed3_OoPDefl = [seed3_deflectionb1_550; seed3_deflectionb2_550; seed3_deflectionb3_550];
seed4_OoPDefl = [seed4_deflectionb1_550; seed4_deflectionb2_550; seed4_deflectionb3_550];
seed5_OoPDefl = [seed5_deflectionb1_550; seed5_deflectionb2_550; seed5_deflectionb3_550];
seed6_OoPDefl = [seed6_deflectionb1_550; seed6_deflectionb2_550; seed6_deflectionb3_550];


tip_seeds550 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_550 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 600 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_deflectionb1_600 = seed1_deflectionb1(1:600/0.008);
seed1_deflectionb2_600 = seed1_deflectionb2(1:600/0.008);
seed1_deflectionb3_600 = seed1_deflectionb3(1:600/0.008);

seed2_deflectionb1_600 = seed2_deflectionb1(1:600/0.008);
seed2_deflectionb2_600 = seed2_deflectionb2(1:600/0.008);
seed2_deflectionb3_600 = seed2_deflectionb3(1:600/0.008);

seed3_deflectionb1_600 = seed3_deflectionb1(1:600/0.008);
seed3_deflectionb2_600 = seed3_deflectionb2(1:600/0.008);
seed3_deflectionb3_600 = seed3_deflectionb3(1:600/0.008);

seed4_deflectionb1_600 = seed4_deflectionb1(1:600/0.008);
seed4_deflectionb2_600 = seed4_deflectionb2(1:600/0.008);
seed4_deflectionb3_600 = seed4_deflectionb3(1:600/0.008);

seed5_deflectionb1_600 = seed5_deflectionb1(1:600/0.008);
seed5_deflectionb2_600 = seed5_deflectionb2(1:600/0.008);
seed5_deflectionb3_600 = seed5_deflectionb3(1:600/0.008);

seed6_deflectionb1_600 = seed6_deflectionb1(1:600/0.008);
seed6_deflectionb2_600 = seed6_deflectionb2(1:600/0.008);
seed6_deflectionb3_600 = seed6_deflectionb3(1:600/0.008);


seed1_deflectionb1_600(1:t_remove/0.008)=[];
seed1_deflectionb2_600(1:t_remove/0.008)=[];
seed1_deflectionb3_600(1:t_remove/0.008)=[];
seed2_deflectionb1_600(1:t_remove/0.008)=[];
seed2_deflectionb2_600(1:t_remove/0.008)=[];
seed2_deflectionb3_600(1:t_remove/0.008)=[];
seed3_deflectionb1_600(1:t_remove/0.008)=[];
seed3_deflectionb2_600(1:t_remove/0.008)=[];
seed3_deflectionb3_600(1:t_remove/0.008)=[];
seed4_deflectionb1_600(1:t_remove/0.008)=[];
seed4_deflectionb2_600(1:t_remove/0.008)=[];
seed4_deflectionb3_600(1:t_remove/0.008)=[];
seed5_deflectionb1_600(1:t_remove/0.008)=[];
seed5_deflectionb2_600(1:t_remove/0.008)=[];
seed5_deflectionb3_600(1:t_remove/0.008)=[];
seed6_deflectionb1_600(1:t_remove/0.008)=[];
seed6_deflectionb2_600(1:t_remove/0.008)=[];
seed6_deflectionb3_600(1:t_remove/0.008)=[];

seed1_OoPDefl = [seed1_deflectionb1_600; seed1_deflectionb2_600; seed1_deflectionb3_600];
seed2_OoPDefl = [seed2_deflectionb1_600; seed2_deflectionb2_600; seed2_deflectionb3_600];
seed3_OoPDefl = [seed3_deflectionb1_600; seed3_deflectionb2_600; seed3_deflectionb3_600];
seed4_OoPDefl = [seed4_deflectionb1_600; seed4_deflectionb2_600; seed4_deflectionb3_600];
seed5_OoPDefl = [seed5_deflectionb1_600; seed5_deflectionb2_600; seed5_deflectionb3_600];
seed6_OoPDefl = [seed6_deflectionb1_600; seed6_deflectionb2_600; seed6_deflectionb3_600];


tip_seeds600 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_600 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

tip_defl = [tip_defl_70, tip_defl_100, tip_defl_150, tip_defl_200, ...
            tip_defl_250, tip_defl_300, tip_defl_350, tip_defl_400, ...
            tip_defl_450, tip_defl_500, tip_defl_550, tip_defl_600];
            


%% Compare root Moments 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 70 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_70 = seed1_rootflap1(1:70/0.008);
seed1_rootflap2_70 = seed1_rootflap2(1:70/0.008);
seed1_rootflap3_70 = seed1_rootflap3(1:70/0.008);
seed1_rootedge1_70 = seed1_rootedge1(1:70/0.008);
seed1_rootedge2_70 = seed1_rootedge2(1:70/0.008);
seed1_rootedge3_70 = seed1_rootedge3(1:70/0.008);


seed2_rootflap1_70 = seed2_rootflap1(1:70/0.008);
seed2_rootflap2_70 = seed2_rootflap2(1:70/0.008);
seed2_rootflap3_70 = seed2_rootflap3(1:70/0.008);
seed2_rootedge1_70 = seed2_rootedge1(1:70/0.008);
seed2_rootedge2_70 = seed2_rootedge2(1:70/0.008);
seed2_rootedge3_70 = seed2_rootedge3(1:70/0.008);

seed3_rootflap1_70 = seed3_rootflap1(1:70/0.008);
seed3_rootflap2_70 = seed3_rootflap2(1:70/0.008);
seed3_rootflap3_70 = seed3_rootflap3(1:70/0.008);
seed3_rootedge1_70 = seed3_rootedge1(1:70/0.008);
seed3_rootedge2_70 = seed3_rootedge2(1:70/0.008);
seed3_rootedge3_70 = seed3_rootedge3(1:70/0.008);

seed4_rootflap1_70 = seed4_rootflap1(1:70/0.008);
seed4_rootflap2_70 = seed4_rootflap2(1:70/0.008);
seed4_rootflap3_70 = seed4_rootflap3(1:70/0.008);
seed4_rootedge1_70 = seed4_rootedge1(1:70/0.008);
seed4_rootedge2_70 = seed4_rootedge2(1:70/0.008);
seed4_rootedge3_70 = seed4_rootedge3(1:70/0.008);

seed5_rootflap1_70 = seed5_rootflap1(1:70/0.008);
seed5_rootflap2_70 = seed5_rootflap2(1:70/0.008);
seed5_rootflap3_70 = seed5_rootflap3(1:70/0.008);
seed5_rootedge1_70 = seed5_rootedge1(1:70/0.008);
seed5_rootedge2_70 = seed5_rootedge2(1:70/0.008);
seed5_rootedge3_70 = seed5_rootedge3(1:70/0.008);

seed6_rootflap1_70 = seed6_rootflap1(1:70/0.008);
seed6_rootflap2_70 = seed6_rootflap2(1:70/0.008);
seed6_rootflap3_70 = seed6_rootflap3(1:70/0.008);
seed6_rootedge1_70 = seed6_rootedge1(1:70/0.008);
seed6_rootedge2_70 = seed6_rootedge2(1:70/0.008);
seed6_rootedge3_70 = seed6_rootedge3(1:70/0.008);

seed1_rootflap1_70(1:t_remove/0.008)=[];
seed1_rootflap2_70(1:t_remove/0.008)=[];
seed1_rootflap3_70(1:t_remove/0.008)=[];
seed1_rootedge1_70(1:t_remove/0.008)=[];
seed1_rootedge2_70(1:t_remove/0.008)=[];
seed1_rootedge3_70(1:t_remove/0.008)=[];
seed2_rootflap1_70(1:t_remove/0.008)=[];
seed2_rootflap2_70(1:t_remove/0.008)=[];
seed2_rootflap3_70(1:t_remove/0.008)=[];
seed2_rootedge1_70(1:t_remove/0.008)=[];
seed2_rootedge2_70(1:t_remove/0.008)=[];
seed2_rootedge3_70(1:t_remove/0.008)=[];
seed3_rootflap1_70(1:t_remove/0.008)=[];
seed3_rootflap2_70(1:t_remove/0.008)=[];
seed3_rootflap3_70(1:t_remove/0.008)=[];
seed3_rootedge1_70(1:t_remove/0.008)=[];
seed3_rootedge2_70(1:t_remove/0.008)=[];
seed3_rootedge3_70(1:t_remove/0.008)=[];
seed4_rootflap1_70(1:t_remove/0.008)=[];
seed4_rootflap2_70(1:t_remove/0.008)=[];
seed4_rootflap3_70(1:t_remove/0.008)=[];
seed4_rootedge1_70(1:t_remove/0.008)=[];
seed4_rootedge2_70(1:t_remove/0.008)=[];
seed4_rootedge3_70(1:t_remove/0.008)=[];
seed5_rootflap1_70(1:t_remove/0.008)=[];
seed5_rootflap2_70(1:t_remove/0.008)=[];
seed5_rootflap3_70(1:t_remove/0.008)=[];
seed5_rootedge1_70(1:t_remove/0.008)=[];
seed5_rootedge2_70(1:t_remove/0.008)=[];
seed5_rootedge3_70(1:t_remove/0.008)=[];
seed6_rootflap1_70(1:t_remove/0.008)=[];
seed6_rootflap2_70(1:t_remove/0.008)=[];
seed6_rootflap3_70(1:t_remove/0.008)=[];
seed6_rootedge1_70(1:t_remove/0.008)=[];
seed6_rootedge2_70(1:t_remove/0.008)=[];
seed6_rootedge3_70(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_70 ; seed1_rootflap2_70 ; seed1_rootflap3_70];
seed2_flpmoment = [seed2_rootflap1_70 ; seed2_rootflap2_70 ; seed2_rootflap3_70];
seed3_flpmoment = [seed3_rootflap1_70 ; seed3_rootflap2_70 ; seed3_rootflap3_70];
seed4_flpmoment = [seed4_rootflap1_70 ; seed4_rootflap2_70 ; seed4_rootflap3_70];
seed5_flpmoment = [seed5_rootflap1_70 ; seed5_rootflap2_70 ; seed5_rootflap3_70];
seed6_flpmoment = [seed6_rootflap1_70 ; seed6_rootflap2_70 ; seed6_rootflap3_70];

seed1_edgemoment = [seed1_rootedge1_70; seed1_rootedge2_70; seed1_rootedge3_70];
seed2_edgemoment = [seed2_rootedge1_70; seed2_rootedge2_70; seed2_rootedge3_70];
seed3_edgemoment = [seed3_rootedge1_70; seed3_rootedge2_70; seed3_rootedge3_70];
seed4_edgemoment = [seed4_rootedge1_70; seed4_rootedge2_70; seed4_rootedge3_70];
seed5_edgemoment = [seed5_rootedge1_70; seed5_rootedge2_70; seed5_rootedge3_70];
seed6_edgemoment = [seed6_rootedge1_70; seed6_rootedge2_70; seed6_rootedge3_70];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds70 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_70_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 100 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_100 = seed1_rootflap1(1:100/0.008);
seed1_rootflap2_100 = seed1_rootflap2(1:100/0.008);
seed1_rootflap3_100 = seed1_rootflap3(1:100/0.008);
seed1_rootedge1_100 = seed1_rootedge1(1:100/0.008);
seed1_rootedge2_100 = seed1_rootedge2(1:100/0.008);
seed1_rootedge3_100 = seed1_rootedge3(1:100/0.008);


seed2_rootflap1_100 = seed2_rootflap1(1:100/0.008);
seed2_rootflap2_100 = seed2_rootflap2(1:100/0.008);
seed2_rootflap3_100 = seed2_rootflap3(1:100/0.008);
seed2_rootedge1_100 = seed2_rootedge1(1:100/0.008);
seed2_rootedge2_100 = seed2_rootedge2(1:100/0.008);
seed2_rootedge3_100 = seed2_rootedge3(1:100/0.008);

seed3_rootflap1_100 = seed3_rootflap1(1:100/0.008);
seed3_rootflap2_100 = seed3_rootflap2(1:100/0.008);
seed3_rootflap3_100 = seed3_rootflap3(1:100/0.008);
seed3_rootedge1_100 = seed3_rootedge1(1:100/0.008);
seed3_rootedge2_100 = seed3_rootedge2(1:100/0.008);
seed3_rootedge3_100 = seed3_rootedge3(1:100/0.008);

seed4_rootflap1_100 = seed4_rootflap1(1:100/0.008);
seed4_rootflap2_100 = seed4_rootflap2(1:100/0.008);
seed4_rootflap3_100 = seed4_rootflap3(1:100/0.008);
seed4_rootedge1_100 = seed4_rootedge1(1:100/0.008);
seed4_rootedge2_100 = seed4_rootedge2(1:100/0.008);
seed4_rootedge3_100 = seed4_rootedge3(1:100/0.008);

seed5_rootflap1_100 = seed5_rootflap1(1:100/0.008);
seed5_rootflap2_100 = seed5_rootflap2(1:100/0.008);
seed5_rootflap3_100 = seed5_rootflap3(1:100/0.008);
seed5_rootedge1_100 = seed5_rootedge1(1:100/0.008);
seed5_rootedge2_100 = seed5_rootedge2(1:100/0.008);
seed5_rootedge3_100 = seed5_rootedge3(1:100/0.008);

seed6_rootflap1_100 = seed6_rootflap1(1:100/0.008);
seed6_rootflap2_100 = seed6_rootflap2(1:100/0.008);
seed6_rootflap3_100 = seed6_rootflap3(1:100/0.008);
seed6_rootedge1_100 = seed6_rootedge1(1:100/0.008);
seed6_rootedge2_100 = seed6_rootedge2(1:100/0.008);
seed6_rootedge3_100 = seed6_rootedge3(1:100/0.008);

seed1_rootflap1_100(1:t_remove/0.008)=[];
seed1_rootflap2_100(1:t_remove/0.008)=[];
seed1_rootflap3_100(1:t_remove/0.008)=[];
seed1_rootedge1_100(1:t_remove/0.008)=[];
seed1_rootedge2_100(1:t_remove/0.008)=[];
seed1_rootedge3_100(1:t_remove/0.008)=[];
seed2_rootflap1_100(1:t_remove/0.008)=[];
seed2_rootflap2_100(1:t_remove/0.008)=[];
seed2_rootflap3_100(1:t_remove/0.008)=[];
seed2_rootedge1_100(1:t_remove/0.008)=[];
seed2_rootedge2_100(1:t_remove/0.008)=[];
seed2_rootedge3_100(1:t_remove/0.008)=[];
seed3_rootflap1_100(1:t_remove/0.008)=[];
seed3_rootflap2_100(1:t_remove/0.008)=[];
seed3_rootflap3_100(1:t_remove/0.008)=[];
seed3_rootedge1_100(1:t_remove/0.008)=[];
seed3_rootedge2_100(1:t_remove/0.008)=[];
seed3_rootedge3_100(1:t_remove/0.008)=[];
seed4_rootflap1_100(1:t_remove/0.008)=[];
seed4_rootflap2_100(1:t_remove/0.008)=[];
seed4_rootflap3_100(1:t_remove/0.008)=[];
seed4_rootedge1_100(1:t_remove/0.008)=[];
seed4_rootedge2_100(1:t_remove/0.008)=[];
seed4_rootedge3_100(1:t_remove/0.008)=[];
seed5_rootflap1_100(1:t_remove/0.008)=[];
seed5_rootflap2_100(1:t_remove/0.008)=[];
seed5_rootflap3_100(1:t_remove/0.008)=[];
seed5_rootedge1_100(1:t_remove/0.008)=[];
seed5_rootedge2_100(1:t_remove/0.008)=[];
seed5_rootedge3_100(1:t_remove/0.008)=[];
seed6_rootflap1_100(1:t_remove/0.008)=[];
seed6_rootflap2_100(1:t_remove/0.008)=[];
seed6_rootflap3_100(1:t_remove/0.008)=[];
seed6_rootedge1_100(1:t_remove/0.008)=[];
seed6_rootedge2_100(1:t_remove/0.008)=[];
seed6_rootedge3_100(1:t_remove/0.008)=[];





seed1_flpmoment = [seed1_rootflap1_100 ; seed1_rootflap2_100 ; seed1_rootflap3_100];
seed2_flpmoment = [seed2_rootflap1_100 ; seed2_rootflap2_100 ; seed2_rootflap3_100];
seed3_flpmoment = [seed3_rootflap1_100 ; seed3_rootflap2_100 ; seed3_rootflap3_100];
seed4_flpmoment = [seed4_rootflap1_100 ; seed4_rootflap2_100 ; seed4_rootflap3_100];
seed5_flpmoment = [seed5_rootflap1_100 ; seed5_rootflap2_100 ; seed5_rootflap3_100];
seed6_flpmoment = [seed6_rootflap1_100 ; seed6_rootflap2_100 ; seed6_rootflap3_100];

seed1_edgemoment = [seed1_rootedge1_100; seed1_rootedge2_100; seed1_rootedge3_100];
seed2_edgemoment = [seed2_rootedge1_100; seed2_rootedge2_100; seed2_rootedge3_100];
seed3_edgemoment = [seed3_rootedge1_100; seed3_rootedge2_100; seed3_rootedge3_100];
seed4_edgemoment = [seed4_rootedge1_100; seed4_rootedge2_100; seed4_rootedge3_100];
seed5_edgemoment = [seed5_rootedge1_100; seed5_rootedge2_100; seed5_rootedge3_100];
seed6_edgemoment = [seed6_rootedge1_100; seed6_rootedge2_100; seed6_rootedge3_100];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds100 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_100_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 150 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_150 = seed1_rootflap1(1:150/0.008);
seed1_rootflap2_150 = seed1_rootflap2(1:150/0.008);
seed1_rootflap3_150 = seed1_rootflap3(1:150/0.008);
seed1_rootedge1_150 = seed1_rootedge1(1:150/0.008);
seed1_rootedge2_150 = seed1_rootedge2(1:150/0.008);
seed1_rootedge3_150 = seed1_rootedge3(1:150/0.008);


seed2_rootflap1_150 = seed2_rootflap1(1:150/0.008);
seed2_rootflap2_150 = seed2_rootflap2(1:150/0.008);
seed2_rootflap3_150 = seed2_rootflap3(1:150/0.008);
seed2_rootedge1_150 = seed2_rootedge1(1:150/0.008);
seed2_rootedge2_150 = seed2_rootedge2(1:150/0.008);
seed2_rootedge3_150 = seed2_rootedge3(1:150/0.008);

seed3_rootflap1_150 = seed3_rootflap1(1:150/0.008);
seed3_rootflap2_150 = seed3_rootflap2(1:150/0.008);
seed3_rootflap3_150 = seed3_rootflap3(1:150/0.008);
seed3_rootedge1_150 = seed3_rootedge1(1:150/0.008);
seed3_rootedge2_150 = seed3_rootedge2(1:150/0.008);
seed3_rootedge3_150 = seed3_rootedge3(1:150/0.008);

seed4_rootflap1_150 = seed4_rootflap1(1:150/0.008);
seed4_rootflap2_150 = seed4_rootflap2(1:150/0.008);
seed4_rootflap3_150 = seed4_rootflap3(1:150/0.008);
seed4_rootedge1_150 = seed4_rootedge1(1:150/0.008);
seed4_rootedge2_150 = seed4_rootedge2(1:150/0.008);
seed4_rootedge3_150 = seed4_rootedge3(1:150/0.008);

seed5_rootflap1_150 = seed5_rootflap1(1:150/0.008);
seed5_rootflap2_150 = seed5_rootflap2(1:150/0.008);
seed5_rootflap3_150 = seed5_rootflap3(1:150/0.008);
seed5_rootedge1_150 = seed5_rootedge1(1:150/0.008);
seed5_rootedge2_150 = seed5_rootedge2(1:150/0.008);
seed5_rootedge3_150 = seed5_rootedge3(1:150/0.008);

seed6_rootflap1_150 = seed6_rootflap1(1:150/0.008);
seed6_rootflap2_150 = seed6_rootflap2(1:150/0.008);
seed6_rootflap3_150 = seed6_rootflap3(1:150/0.008);
seed6_rootedge1_150 = seed6_rootedge1(1:150/0.008);
seed6_rootedge2_150 = seed6_rootedge2(1:150/0.008);
seed6_rootedge3_150 = seed6_rootedge3(1:150/0.008);

seed1_rootflap1_150(1:t_remove/0.008)=[];
seed1_rootflap2_150(1:t_remove/0.008)=[];
seed1_rootflap3_150(1:t_remove/0.008)=[];
seed1_rootedge1_150(1:t_remove/0.008)=[];
seed1_rootedge2_150(1:t_remove/0.008)=[];
seed1_rootedge3_150(1:t_remove/0.008)=[];
seed2_rootflap1_150(1:t_remove/0.008)=[];
seed2_rootflap2_150(1:t_remove/0.008)=[];
seed2_rootflap3_150(1:t_remove/0.008)=[];
seed2_rootedge1_150(1:t_remove/0.008)=[];
seed2_rootedge2_150(1:t_remove/0.008)=[];
seed2_rootedge3_150(1:t_remove/0.008)=[];
seed3_rootflap1_150(1:t_remove/0.008)=[];
seed3_rootflap2_150(1:t_remove/0.008)=[];
seed3_rootflap3_150(1:t_remove/0.008)=[];
seed3_rootedge1_150(1:t_remove/0.008)=[];
seed3_rootedge2_150(1:t_remove/0.008)=[];
seed3_rootedge3_150(1:t_remove/0.008)=[];
seed4_rootflap1_150(1:t_remove/0.008)=[];
seed4_rootflap2_150(1:t_remove/0.008)=[];
seed4_rootflap3_150(1:t_remove/0.008)=[];
seed4_rootedge1_150(1:t_remove/0.008)=[];
seed4_rootedge2_150(1:t_remove/0.008)=[];
seed4_rootedge3_150(1:t_remove/0.008)=[];
seed5_rootflap1_150(1:t_remove/0.008)=[];
seed5_rootflap2_150(1:t_remove/0.008)=[];
seed5_rootflap3_150(1:t_remove/0.008)=[];
seed5_rootedge1_150(1:t_remove/0.008)=[];
seed5_rootedge2_150(1:t_remove/0.008)=[];
seed5_rootedge3_150(1:t_remove/0.008)=[];
seed6_rootflap1_150(1:t_remove/0.008)=[];
seed6_rootflap2_150(1:t_remove/0.008)=[];
seed6_rootflap3_150(1:t_remove/0.008)=[];
seed6_rootedge1_150(1:t_remove/0.008)=[];
seed6_rootedge2_150(1:t_remove/0.008)=[];
seed6_rootedge3_150(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_150 ; seed1_rootflap2_150 ; seed1_rootflap3_150];
seed2_flpmoment = [seed2_rootflap1_150 ; seed2_rootflap2_150 ; seed2_rootflap3_150];
seed3_flpmoment = [seed3_rootflap1_150 ; seed3_rootflap2_150 ; seed3_rootflap3_150];
seed4_flpmoment = [seed4_rootflap1_150 ; seed4_rootflap2_150 ; seed4_rootflap3_150];
seed5_flpmoment = [seed5_rootflap1_150 ; seed5_rootflap2_150 ; seed5_rootflap3_150];
seed6_flpmoment = [seed6_rootflap1_150 ; seed6_rootflap2_150 ; seed6_rootflap3_150];

seed1_edgemoment = [seed1_rootedge1_150; seed1_rootedge2_150; seed1_rootedge3_150];
seed2_edgemoment = [seed2_rootedge1_150; seed2_rootedge2_150; seed2_rootedge3_150];
seed3_edgemoment = [seed3_rootedge1_150; seed3_rootedge2_150; seed3_rootedge3_150];
seed4_edgemoment = [seed4_rootedge1_150; seed4_rootedge2_150; seed4_rootedge3_150];
seed5_edgemoment = [seed5_rootedge1_150; seed5_rootedge2_150; seed5_rootedge3_150];
seed6_edgemoment = [seed6_rootedge1_150; seed6_rootedge2_150; seed6_rootedge3_150];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds150 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_150_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 200 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_200 = seed1_rootflap1(1:200/0.008);
seed1_rootflap2_200 = seed1_rootflap2(1:200/0.008);
seed1_rootflap3_200 = seed1_rootflap3(1:200/0.008);
seed1_rootedge1_200 = seed1_rootedge1(1:200/0.008);
seed1_rootedge2_200 = seed1_rootedge2(1:200/0.008);
seed1_rootedge3_200 = seed1_rootedge3(1:200/0.008);


seed2_rootflap1_200 = seed2_rootflap1(1:200/0.008);
seed2_rootflap2_200 = seed2_rootflap2(1:200/0.008);
seed2_rootflap3_200 = seed2_rootflap3(1:200/0.008);
seed2_rootedge1_200 = seed2_rootedge1(1:200/0.008);
seed2_rootedge2_200 = seed2_rootedge2(1:200/0.008);
seed2_rootedge3_200 = seed2_rootedge3(1:200/0.008);

seed3_rootflap1_200 = seed3_rootflap1(1:200/0.008);
seed3_rootflap2_200 = seed3_rootflap2(1:200/0.008);
seed3_rootflap3_200 = seed3_rootflap3(1:200/0.008);
seed3_rootedge1_200 = seed3_rootedge1(1:200/0.008);
seed3_rootedge2_200 = seed3_rootedge2(1:200/0.008);
seed3_rootedge3_200 = seed3_rootedge3(1:200/0.008);

seed4_rootflap1_200 = seed4_rootflap1(1:200/0.008);
seed4_rootflap2_200 = seed4_rootflap2(1:200/0.008);
seed4_rootflap3_200 = seed4_rootflap3(1:200/0.008);
seed4_rootedge1_200 = seed4_rootedge1(1:200/0.008);
seed4_rootedge2_200 = seed4_rootedge2(1:200/0.008);
seed4_rootedge3_200 = seed4_rootedge3(1:200/0.008);

seed5_rootflap1_200 = seed5_rootflap1(1:200/0.008);
seed5_rootflap2_200 = seed5_rootflap2(1:200/0.008);
seed5_rootflap3_200 = seed5_rootflap3(1:200/0.008);
seed5_rootedge1_200 = seed5_rootedge1(1:200/0.008);
seed5_rootedge2_200 = seed5_rootedge2(1:200/0.008);
seed5_rootedge3_200 = seed5_rootedge3(1:200/0.008);

seed6_rootflap1_200 = seed6_rootflap1(1:200/0.008);
seed6_rootflap2_200 = seed6_rootflap2(1:200/0.008);
seed6_rootflap3_200 = seed6_rootflap3(1:200/0.008);
seed6_rootedge1_200 = seed6_rootedge1(1:200/0.008);
seed6_rootedge2_200 = seed6_rootedge2(1:200/0.008);
seed6_rootedge3_200 = seed6_rootedge3(1:200/0.008);

seed1_rootflap1_200(1:t_remove/0.008)=[];
seed1_rootflap2_200(1:t_remove/0.008)=[];
seed1_rootflap3_200(1:t_remove/0.008)=[];
seed1_rootedge1_200(1:t_remove/0.008)=[];
seed1_rootedge2_200(1:t_remove/0.008)=[];
seed1_rootedge3_200(1:t_remove/0.008)=[];
seed2_rootflap1_200(1:t_remove/0.008)=[];
seed2_rootflap2_200(1:t_remove/0.008)=[];
seed2_rootflap3_200(1:t_remove/0.008)=[];
seed2_rootedge1_200(1:t_remove/0.008)=[];
seed2_rootedge2_200(1:t_remove/0.008)=[];
seed2_rootedge3_200(1:t_remove/0.008)=[];
seed3_rootflap1_200(1:t_remove/0.008)=[];
seed3_rootflap2_200(1:t_remove/0.008)=[];
seed3_rootflap3_200(1:t_remove/0.008)=[];
seed3_rootedge1_200(1:t_remove/0.008)=[];
seed3_rootedge2_200(1:t_remove/0.008)=[];
seed3_rootedge3_200(1:t_remove/0.008)=[];
seed4_rootflap1_200(1:t_remove/0.008)=[];
seed4_rootflap2_200(1:t_remove/0.008)=[];
seed4_rootflap3_200(1:t_remove/0.008)=[];
seed4_rootedge1_200(1:t_remove/0.008)=[];
seed4_rootedge2_200(1:t_remove/0.008)=[];
seed4_rootedge3_200(1:t_remove/0.008)=[];
seed5_rootflap1_200(1:t_remove/0.008)=[];
seed5_rootflap2_200(1:t_remove/0.008)=[];
seed5_rootflap3_200(1:t_remove/0.008)=[];
seed5_rootedge1_200(1:t_remove/0.008)=[];
seed5_rootedge2_200(1:t_remove/0.008)=[];
seed5_rootedge3_200(1:t_remove/0.008)=[];
seed6_rootflap1_200(1:t_remove/0.008)=[];
seed6_rootflap2_200(1:t_remove/0.008)=[];
seed6_rootflap3_200(1:t_remove/0.008)=[];
seed6_rootedge1_200(1:t_remove/0.008)=[];
seed6_rootedge2_200(1:t_remove/0.008)=[];
seed6_rootedge3_200(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_200 ; seed1_rootflap2_200 ; seed1_rootflap3_200];
seed2_flpmoment = [seed2_rootflap1_200 ; seed2_rootflap2_200 ; seed2_rootflap3_200];
seed3_flpmoment = [seed3_rootflap1_200 ; seed3_rootflap2_200 ; seed3_rootflap3_200];
seed4_flpmoment = [seed4_rootflap1_200 ; seed4_rootflap2_200 ; seed4_rootflap3_200];
seed5_flpmoment = [seed5_rootflap1_200 ; seed5_rootflap2_200 ; seed5_rootflap3_200];
seed6_flpmoment = [seed6_rootflap1_200 ; seed6_rootflap2_200 ; seed6_rootflap3_200];

seed1_edgemoment = [seed1_rootedge1_200; seed1_rootedge2_200; seed1_rootedge3_200];
seed2_edgemoment = [seed2_rootedge1_200; seed2_rootedge2_200; seed2_rootedge3_200];
seed3_edgemoment = [seed3_rootedge1_200; seed3_rootedge2_200; seed3_rootedge3_200];
seed4_edgemoment = [seed4_rootedge1_200; seed4_rootedge2_200; seed4_rootedge3_200];
seed5_edgemoment = [seed5_rootedge1_200; seed5_rootedge2_200; seed5_rootedge3_200];
seed6_edgemoment = [seed6_rootedge1_200; seed6_rootedge2_200; seed6_rootedge3_200];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds200 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_200_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 250 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_250 = seed1_rootflap1(1:250/0.008);
seed1_rootflap2_250 = seed1_rootflap2(1:250/0.008);
seed1_rootflap3_250 = seed1_rootflap3(1:250/0.008);
seed1_rootedge1_250 = seed1_rootedge1(1:250/0.008);
seed1_rootedge2_250 = seed1_rootedge2(1:250/0.008);
seed1_rootedge3_250 = seed1_rootedge3(1:250/0.008);


seed2_rootflap1_250 = seed2_rootflap1(1:250/0.008);
seed2_rootflap2_250 = seed2_rootflap2(1:250/0.008);
seed2_rootflap3_250 = seed2_rootflap3(1:250/0.008);
seed2_rootedge1_250 = seed2_rootedge1(1:250/0.008);
seed2_rootedge2_250 = seed2_rootedge2(1:250/0.008);
seed2_rootedge3_250 = seed2_rootedge3(1:250/0.008);

seed3_rootflap1_250 = seed3_rootflap1(1:250/0.008);
seed3_rootflap2_250 = seed3_rootflap2(1:250/0.008);
seed3_rootflap3_250 = seed3_rootflap3(1:250/0.008);
seed3_rootedge1_250 = seed3_rootedge1(1:250/0.008);
seed3_rootedge2_250 = seed3_rootedge2(1:250/0.008);
seed3_rootedge3_250 = seed3_rootedge3(1:250/0.008);

seed4_rootflap1_250 = seed4_rootflap1(1:250/0.008);
seed4_rootflap2_250 = seed4_rootflap2(1:250/0.008);
seed4_rootflap3_250 = seed4_rootflap3(1:250/0.008);
seed4_rootedge1_250 = seed4_rootedge1(1:250/0.008);
seed4_rootedge2_250 = seed4_rootedge2(1:250/0.008);
seed4_rootedge3_250 = seed4_rootedge3(1:250/0.008);

seed5_rootflap1_250 = seed5_rootflap1(1:250/0.008);
seed5_rootflap2_250 = seed5_rootflap2(1:250/0.008);
seed5_rootflap3_250 = seed5_rootflap3(1:250/0.008);
seed5_rootedge1_250 = seed5_rootedge1(1:250/0.008);
seed5_rootedge2_250 = seed5_rootedge2(1:250/0.008);
seed5_rootedge3_250 = seed5_rootedge3(1:250/0.008);

seed6_rootflap1_250 = seed6_rootflap1(1:250/0.008);
seed6_rootflap2_250 = seed6_rootflap2(1:250/0.008);
seed6_rootflap3_250 = seed6_rootflap3(1:250/0.008);
seed6_rootedge1_250 = seed6_rootedge1(1:250/0.008);
seed6_rootedge2_250 = seed6_rootedge2(1:250/0.008);
seed6_rootedge3_250 = seed6_rootedge3(1:250/0.008);

seed1_rootflap1_250(1:t_remove/0.008)=[];
seed1_rootflap2_250(1:t_remove/0.008)=[];
seed1_rootflap3_250(1:t_remove/0.008)=[];
seed1_rootedge1_250(1:t_remove/0.008)=[];
seed1_rootedge2_250(1:t_remove/0.008)=[];
seed1_rootedge3_250(1:t_remove/0.008)=[];
seed2_rootflap1_250(1:t_remove/0.008)=[];
seed2_rootflap2_250(1:t_remove/0.008)=[];
seed2_rootflap3_250(1:t_remove/0.008)=[];
seed2_rootedge1_250(1:t_remove/0.008)=[];
seed2_rootedge2_250(1:t_remove/0.008)=[];
seed2_rootedge3_250(1:t_remove/0.008)=[];
seed3_rootflap1_250(1:t_remove/0.008)=[];
seed3_rootflap2_250(1:t_remove/0.008)=[];
seed3_rootflap3_250(1:t_remove/0.008)=[];
seed3_rootedge1_250(1:t_remove/0.008)=[];
seed3_rootedge2_250(1:t_remove/0.008)=[];
seed3_rootedge3_250(1:t_remove/0.008)=[];
seed4_rootflap1_250(1:t_remove/0.008)=[];
seed4_rootflap2_250(1:t_remove/0.008)=[];
seed4_rootflap3_250(1:t_remove/0.008)=[];
seed4_rootedge1_250(1:t_remove/0.008)=[];
seed4_rootedge2_250(1:t_remove/0.008)=[];
seed4_rootedge3_250(1:t_remove/0.008)=[];
seed5_rootflap1_250(1:t_remove/0.008)=[];
seed5_rootflap2_250(1:t_remove/0.008)=[];
seed5_rootflap3_250(1:t_remove/0.008)=[];
seed5_rootedge1_250(1:t_remove/0.008)=[];
seed5_rootedge2_250(1:t_remove/0.008)=[];
seed5_rootedge3_250(1:t_remove/0.008)=[];
seed6_rootflap1_250(1:t_remove/0.008)=[];
seed6_rootflap2_250(1:t_remove/0.008)=[];
seed6_rootflap3_250(1:t_remove/0.008)=[];
seed6_rootedge1_250(1:t_remove/0.008)=[];
seed6_rootedge2_250(1:t_remove/0.008)=[];
seed6_rootedge3_250(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_250 ; seed1_rootflap2_250 ; seed1_rootflap3_250];
seed2_flpmoment = [seed2_rootflap1_250 ; seed2_rootflap2_250 ; seed2_rootflap3_250];
seed3_flpmoment = [seed3_rootflap1_250 ; seed3_rootflap2_250 ; seed3_rootflap3_250];
seed4_flpmoment = [seed4_rootflap1_250 ; seed4_rootflap2_250 ; seed4_rootflap3_250];
seed5_flpmoment = [seed5_rootflap1_250 ; seed5_rootflap2_250 ; seed5_rootflap3_250];
seed6_flpmoment = [seed6_rootflap1_250 ; seed6_rootflap2_250 ; seed6_rootflap3_250];

seed1_edgemoment = [seed1_rootedge1_250; seed1_rootedge2_250; seed1_rootedge3_250];
seed2_edgemoment = [seed2_rootedge1_250; seed2_rootedge2_250; seed2_rootedge3_250];
seed3_edgemoment = [seed3_rootedge1_250; seed3_rootedge2_250; seed3_rootedge3_250];
seed4_edgemoment = [seed4_rootedge1_250; seed4_rootedge2_250; seed4_rootedge3_250];
seed5_edgemoment = [seed5_rootedge1_250; seed5_rootedge2_250; seed5_rootedge3_250];
seed6_edgemoment = [seed6_rootedge1_250; seed6_rootedge2_250; seed6_rootedge3_250];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds250 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_250_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 300 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_300 = seed1_rootflap1(1:300/0.008);
seed1_rootflap2_300 = seed1_rootflap2(1:300/0.008);
seed1_rootflap3_300 = seed1_rootflap3(1:300/0.008);
seed1_rootedge1_300 = seed1_rootedge1(1:300/0.008);
seed1_rootedge2_300 = seed1_rootedge2(1:300/0.008);
seed1_rootedge3_300 = seed1_rootedge3(1:300/0.008);


seed2_rootflap1_300 = seed2_rootflap1(1:300/0.008);
seed2_rootflap2_300 = seed2_rootflap2(1:300/0.008);
seed2_rootflap3_300 = seed2_rootflap3(1:300/0.008);
seed2_rootedge1_300 = seed2_rootedge1(1:300/0.008);
seed2_rootedge2_300 = seed2_rootedge2(1:300/0.008);
seed2_rootedge3_300 = seed2_rootedge3(1:300/0.008);

seed3_rootflap1_300 = seed3_rootflap1(1:300/0.008);
seed3_rootflap2_300 = seed3_rootflap2(1:300/0.008);
seed3_rootflap3_300 = seed3_rootflap3(1:300/0.008);
seed3_rootedge1_300 = seed3_rootedge1(1:300/0.008);
seed3_rootedge2_300 = seed3_rootedge2(1:300/0.008);
seed3_rootedge3_300 = seed3_rootedge3(1:300/0.008);

seed4_rootflap1_300 = seed4_rootflap1(1:300/0.008);
seed4_rootflap2_300 = seed4_rootflap2(1:300/0.008);
seed4_rootflap3_300 = seed4_rootflap3(1:300/0.008);
seed4_rootedge1_300 = seed4_rootedge1(1:300/0.008);
seed4_rootedge2_300 = seed4_rootedge2(1:300/0.008);
seed4_rootedge3_300 = seed4_rootedge3(1:300/0.008);

seed5_rootflap1_300 = seed5_rootflap1(1:300/0.008);
seed5_rootflap2_300 = seed5_rootflap2(1:300/0.008);
seed5_rootflap3_300 = seed5_rootflap3(1:300/0.008);
seed5_rootedge1_300 = seed5_rootedge1(1:300/0.008);
seed5_rootedge2_300 = seed5_rootedge2(1:300/0.008);
seed5_rootedge3_300 = seed5_rootedge3(1:300/0.008);

seed6_rootflap1_300 = seed6_rootflap1(1:300/0.008);
seed6_rootflap2_300 = seed6_rootflap2(1:300/0.008);
seed6_rootflap3_300 = seed6_rootflap3(1:300/0.008);
seed6_rootedge1_300 = seed6_rootedge1(1:300/0.008);
seed6_rootedge2_300 = seed6_rootedge2(1:300/0.008);
seed6_rootedge3_300 = seed6_rootedge3(1:300/0.008);

seed1_rootflap1_300(1:t_remove/0.008)=[];
seed1_rootflap2_300(1:t_remove/0.008)=[];
seed1_rootflap3_300(1:t_remove/0.008)=[];
seed1_rootedge1_300(1:t_remove/0.008)=[];
seed1_rootedge2_300(1:t_remove/0.008)=[];
seed1_rootedge3_300(1:t_remove/0.008)=[];
seed2_rootflap1_300(1:t_remove/0.008)=[];
seed2_rootflap2_300(1:t_remove/0.008)=[];
seed2_rootflap3_300(1:t_remove/0.008)=[];
seed2_rootedge1_300(1:t_remove/0.008)=[];
seed2_rootedge2_300(1:t_remove/0.008)=[];
seed2_rootedge3_300(1:t_remove/0.008)=[];
seed3_rootflap1_300(1:t_remove/0.008)=[];
seed3_rootflap2_300(1:t_remove/0.008)=[];
seed3_rootflap3_300(1:t_remove/0.008)=[];
seed3_rootedge1_300(1:t_remove/0.008)=[];
seed3_rootedge2_300(1:t_remove/0.008)=[];
seed3_rootedge3_300(1:t_remove/0.008)=[];
seed4_rootflap1_300(1:t_remove/0.008)=[];
seed4_rootflap2_300(1:t_remove/0.008)=[];
seed4_rootflap3_300(1:t_remove/0.008)=[];
seed4_rootedge1_300(1:t_remove/0.008)=[];
seed4_rootedge2_300(1:t_remove/0.008)=[];
seed4_rootedge3_300(1:t_remove/0.008)=[];
seed5_rootflap1_300(1:t_remove/0.008)=[];
seed5_rootflap2_300(1:t_remove/0.008)=[];
seed5_rootflap3_300(1:t_remove/0.008)=[];
seed5_rootedge1_300(1:t_remove/0.008)=[];
seed5_rootedge2_300(1:t_remove/0.008)=[];
seed5_rootedge3_300(1:t_remove/0.008)=[];
seed6_rootflap1_300(1:t_remove/0.008)=[];
seed6_rootflap2_300(1:t_remove/0.008)=[];
seed6_rootflap3_300(1:t_remove/0.008)=[];
seed6_rootedge1_300(1:t_remove/0.008)=[];
seed6_rootedge2_300(1:t_remove/0.008)=[];
seed6_rootedge3_300(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_300 ; seed1_rootflap2_300 ; seed1_rootflap3_300];
seed2_flpmoment = [seed2_rootflap1_300 ; seed2_rootflap2_300 ; seed2_rootflap3_300];
seed3_flpmoment = [seed3_rootflap1_300 ; seed3_rootflap2_300 ; seed3_rootflap3_300];
seed4_flpmoment = [seed4_rootflap1_300 ; seed4_rootflap2_300 ; seed4_rootflap3_300];
seed5_flpmoment = [seed5_rootflap1_300 ; seed5_rootflap2_300 ; seed5_rootflap3_300];
seed6_flpmoment = [seed6_rootflap1_300 ; seed6_rootflap2_300 ; seed6_rootflap3_300];

seed1_edgemoment = [seed1_rootedge1_300; seed1_rootedge2_300; seed1_rootedge3_300];
seed2_edgemoment = [seed2_rootedge1_300; seed2_rootedge2_300; seed2_rootedge3_300];
seed3_edgemoment = [seed3_rootedge1_300; seed3_rootedge2_300; seed3_rootedge3_300];
seed4_edgemoment = [seed4_rootedge1_300; seed4_rootedge2_300; seed4_rootedge3_300];
seed5_edgemoment = [seed5_rootedge1_300; seed5_rootedge2_300; seed5_rootedge3_300];
seed6_edgemoment = [seed6_rootedge1_300; seed6_rootedge2_300; seed6_rootedge3_300];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds300 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_300_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 350 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_350 = seed1_rootflap1(1:350/0.008);
seed1_rootflap2_350 = seed1_rootflap2(1:350/0.008);
seed1_rootflap3_350 = seed1_rootflap3(1:350/0.008);
seed1_rootedge1_350 = seed1_rootedge1(1:350/0.008);
seed1_rootedge2_350 = seed1_rootedge2(1:350/0.008);
seed1_rootedge3_350 = seed1_rootedge3(1:350/0.008);


seed2_rootflap1_350 = seed2_rootflap1(1:350/0.008);
seed2_rootflap2_350 = seed2_rootflap2(1:350/0.008);
seed2_rootflap3_350 = seed2_rootflap3(1:350/0.008);
seed2_rootedge1_350 = seed2_rootedge1(1:350/0.008);
seed2_rootedge2_350 = seed2_rootedge2(1:350/0.008);
seed2_rootedge3_350 = seed2_rootedge3(1:350/0.008);

seed3_rootflap1_350 = seed3_rootflap1(1:350/0.008);
seed3_rootflap2_350 = seed3_rootflap2(1:350/0.008);
seed3_rootflap3_350 = seed3_rootflap3(1:350/0.008);
seed3_rootedge1_350 = seed3_rootedge1(1:350/0.008);
seed3_rootedge2_350 = seed3_rootedge2(1:350/0.008);
seed3_rootedge3_350 = seed3_rootedge3(1:350/0.008);

seed4_rootflap1_350 = seed4_rootflap1(1:350/0.008);
seed4_rootflap2_350 = seed4_rootflap2(1:350/0.008);
seed4_rootflap3_350 = seed4_rootflap3(1:350/0.008);
seed4_rootedge1_350 = seed4_rootedge1(1:350/0.008);
seed4_rootedge2_350 = seed4_rootedge2(1:350/0.008);
seed4_rootedge3_350 = seed4_rootedge3(1:350/0.008);

seed5_rootflap1_350 = seed5_rootflap1(1:350/0.008);
seed5_rootflap2_350 = seed5_rootflap2(1:350/0.008);
seed5_rootflap3_350 = seed5_rootflap3(1:350/0.008);
seed5_rootedge1_350 = seed5_rootedge1(1:350/0.008);
seed5_rootedge2_350 = seed5_rootedge2(1:350/0.008);
seed5_rootedge3_350 = seed5_rootedge3(1:350/0.008);

seed6_rootflap1_350 = seed6_rootflap1(1:350/0.008);
seed6_rootflap2_350 = seed6_rootflap2(1:350/0.008);
seed6_rootflap3_350 = seed6_rootflap3(1:350/0.008);
seed6_rootedge1_350 = seed6_rootedge1(1:350/0.008);
seed6_rootedge2_350 = seed6_rootedge2(1:350/0.008);
seed6_rootedge3_350 = seed6_rootedge3(1:350/0.008);

seed1_rootflap1_350(1:t_remove/0.008)=[];
seed1_rootflap2_350(1:t_remove/0.008)=[];
seed1_rootflap3_350(1:t_remove/0.008)=[];
seed1_rootedge1_350(1:t_remove/0.008)=[];
seed1_rootedge2_350(1:t_remove/0.008)=[];
seed1_rootedge3_350(1:t_remove/0.008)=[];
seed2_rootflap1_350(1:t_remove/0.008)=[];
seed2_rootflap2_350(1:t_remove/0.008)=[];
seed2_rootflap3_350(1:t_remove/0.008)=[];
seed2_rootedge1_350(1:t_remove/0.008)=[];
seed2_rootedge2_350(1:t_remove/0.008)=[];
seed2_rootedge3_350(1:t_remove/0.008)=[];
seed3_rootflap1_350(1:t_remove/0.008)=[];
seed3_rootflap2_350(1:t_remove/0.008)=[];
seed3_rootflap3_350(1:t_remove/0.008)=[];
seed3_rootedge1_350(1:t_remove/0.008)=[];
seed3_rootedge2_350(1:t_remove/0.008)=[];
seed3_rootedge3_350(1:t_remove/0.008)=[];
seed4_rootflap1_350(1:t_remove/0.008)=[];
seed4_rootflap2_350(1:t_remove/0.008)=[];
seed4_rootflap3_350(1:t_remove/0.008)=[];
seed4_rootedge1_350(1:t_remove/0.008)=[];
seed4_rootedge2_350(1:t_remove/0.008)=[];
seed4_rootedge3_350(1:t_remove/0.008)=[];
seed5_rootflap1_350(1:t_remove/0.008)=[];
seed5_rootflap2_350(1:t_remove/0.008)=[];
seed5_rootflap3_350(1:t_remove/0.008)=[];
seed5_rootedge1_350(1:t_remove/0.008)=[];
seed5_rootedge2_350(1:t_remove/0.008)=[];
seed5_rootedge3_350(1:t_remove/0.008)=[];
seed6_rootflap1_350(1:t_remove/0.008)=[];
seed6_rootflap2_350(1:t_remove/0.008)=[];
seed6_rootflap3_350(1:t_remove/0.008)=[];
seed6_rootedge1_350(1:t_remove/0.008)=[];
seed6_rootedge2_350(1:t_remove/0.008)=[];
seed6_rootedge3_350(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_350 ; seed1_rootflap2_350 ; seed1_rootflap3_350];
seed2_flpmoment = [seed2_rootflap1_350 ; seed2_rootflap2_350 ; seed2_rootflap3_350];
seed3_flpmoment = [seed3_rootflap1_350 ; seed3_rootflap2_350 ; seed3_rootflap3_350];
seed4_flpmoment = [seed4_rootflap1_350 ; seed4_rootflap2_350 ; seed4_rootflap3_350];
seed5_flpmoment = [seed5_rootflap1_350 ; seed5_rootflap2_350 ; seed5_rootflap3_350];
seed6_flpmoment = [seed6_rootflap1_350 ; seed6_rootflap2_350 ; seed6_rootflap3_350];

seed1_edgemoment = [seed1_rootedge1_350; seed1_rootedge2_350; seed1_rootedge3_350];
seed2_edgemoment = [seed2_rootedge1_350; seed2_rootedge2_350; seed2_rootedge3_350];
seed3_edgemoment = [seed3_rootedge1_350; seed3_rootedge2_350; seed3_rootedge3_350];
seed4_edgemoment = [seed4_rootedge1_350; seed4_rootedge2_350; seed4_rootedge3_350];
seed5_edgemoment = [seed5_rootedge1_350; seed5_rootedge2_350; seed5_rootedge3_350];
seed6_edgemoment = [seed6_rootedge1_350; seed6_rootedge2_350; seed6_rootedge3_350];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds350 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_350_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 400 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_400 = seed1_rootflap1(1:400/0.008);
seed1_rootflap2_400 = seed1_rootflap2(1:400/0.008);
seed1_rootflap3_400 = seed1_rootflap3(1:400/0.008);
seed1_rootedge1_400 = seed1_rootedge1(1:400/0.008);
seed1_rootedge2_400 = seed1_rootedge2(1:400/0.008);
seed1_rootedge3_400 = seed1_rootedge3(1:400/0.008);


seed2_rootflap1_400 = seed2_rootflap1(1:400/0.008);
seed2_rootflap2_400 = seed2_rootflap2(1:400/0.008);
seed2_rootflap3_400 = seed2_rootflap3(1:400/0.008);
seed2_rootedge1_400 = seed2_rootedge1(1:400/0.008);
seed2_rootedge2_400 = seed2_rootedge2(1:400/0.008);
seed2_rootedge3_400 = seed2_rootedge3(1:400/0.008);

seed3_rootflap1_400 = seed3_rootflap1(1:400/0.008);
seed3_rootflap2_400 = seed3_rootflap2(1:400/0.008);
seed3_rootflap3_400 = seed3_rootflap3(1:400/0.008);
seed3_rootedge1_400 = seed3_rootedge1(1:400/0.008);
seed3_rootedge2_400 = seed3_rootedge2(1:400/0.008);
seed3_rootedge3_400 = seed3_rootedge3(1:400/0.008);

seed4_rootflap1_400 = seed4_rootflap1(1:400/0.008);
seed4_rootflap2_400 = seed4_rootflap2(1:400/0.008);
seed4_rootflap3_400 = seed4_rootflap3(1:400/0.008);
seed4_rootedge1_400 = seed4_rootedge1(1:400/0.008);
seed4_rootedge2_400 = seed4_rootedge2(1:400/0.008);
seed4_rootedge3_400 = seed4_rootedge3(1:400/0.008);

seed5_rootflap1_400 = seed5_rootflap1(1:400/0.008);
seed5_rootflap2_400 = seed5_rootflap2(1:400/0.008);
seed5_rootflap3_400 = seed5_rootflap3(1:400/0.008);
seed5_rootedge1_400 = seed5_rootedge1(1:400/0.008);
seed5_rootedge2_400 = seed5_rootedge2(1:400/0.008);
seed5_rootedge3_400 = seed5_rootedge3(1:400/0.008);

seed6_rootflap1_400 = seed6_rootflap1(1:400/0.008);
seed6_rootflap2_400 = seed6_rootflap2(1:400/0.008);
seed6_rootflap3_400 = seed6_rootflap3(1:400/0.008);
seed6_rootedge1_400 = seed6_rootedge1(1:400/0.008);
seed6_rootedge2_400 = seed6_rootedge2(1:400/0.008);
seed6_rootedge3_400 = seed6_rootedge3(1:400/0.008);

seed1_rootflap1_400(1:t_remove/0.008)=[];
seed1_rootflap2_400(1:t_remove/0.008)=[];
seed1_rootflap3_400(1:t_remove/0.008)=[];
seed1_rootedge1_400(1:t_remove/0.008)=[];
seed1_rootedge2_400(1:t_remove/0.008)=[];
seed1_rootedge3_400(1:t_remove/0.008)=[];
seed2_rootflap1_400(1:t_remove/0.008)=[];
seed2_rootflap2_400(1:t_remove/0.008)=[];
seed2_rootflap3_400(1:t_remove/0.008)=[];
seed2_rootedge1_400(1:t_remove/0.008)=[];
seed2_rootedge2_400(1:t_remove/0.008)=[];
seed2_rootedge3_400(1:t_remove/0.008)=[];
seed3_rootflap1_400(1:t_remove/0.008)=[];
seed3_rootflap2_400(1:t_remove/0.008)=[];
seed3_rootflap3_400(1:t_remove/0.008)=[];
seed3_rootedge1_400(1:t_remove/0.008)=[];
seed3_rootedge2_400(1:t_remove/0.008)=[];
seed3_rootedge3_400(1:t_remove/0.008)=[];
seed4_rootflap1_400(1:t_remove/0.008)=[];
seed4_rootflap2_400(1:t_remove/0.008)=[];
seed4_rootflap3_400(1:t_remove/0.008)=[];
seed4_rootedge1_400(1:t_remove/0.008)=[];
seed4_rootedge2_400(1:t_remove/0.008)=[];
seed4_rootedge3_400(1:t_remove/0.008)=[];
seed5_rootflap1_400(1:t_remove/0.008)=[];
seed5_rootflap2_400(1:t_remove/0.008)=[];
seed5_rootflap3_400(1:t_remove/0.008)=[];
seed5_rootedge1_400(1:t_remove/0.008)=[];
seed5_rootedge2_400(1:t_remove/0.008)=[];
seed5_rootedge3_400(1:t_remove/0.008)=[];
seed6_rootflap1_400(1:t_remove/0.008)=[];
seed6_rootflap2_400(1:t_remove/0.008)=[];
seed6_rootflap3_400(1:t_remove/0.008)=[];
seed6_rootedge1_400(1:t_remove/0.008)=[];
seed6_rootedge2_400(1:t_remove/0.008)=[];
seed6_rootedge3_400(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_400 ; seed1_rootflap2_400 ; seed1_rootflap3_400];
seed2_flpmoment = [seed2_rootflap1_400 ; seed2_rootflap2_400 ; seed2_rootflap3_400];
seed3_flpmoment = [seed3_rootflap1_400 ; seed3_rootflap2_400 ; seed3_rootflap3_400];
seed4_flpmoment = [seed4_rootflap1_400 ; seed4_rootflap2_400 ; seed4_rootflap3_400];
seed5_flpmoment = [seed5_rootflap1_400 ; seed5_rootflap2_400 ; seed5_rootflap3_400];
seed6_flpmoment = [seed6_rootflap1_400 ; seed6_rootflap2_400 ; seed6_rootflap3_400];

seed1_edgemoment = [seed1_rootedge1_400; seed1_rootedge2_400; seed1_rootedge3_400];
seed2_edgemoment = [seed2_rootedge1_400; seed2_rootedge2_400; seed2_rootedge3_400];
seed3_edgemoment = [seed3_rootedge1_400; seed3_rootedge2_400; seed3_rootedge3_400];
seed4_edgemoment = [seed4_rootedge1_400; seed4_rootedge2_400; seed4_rootedge3_400];
seed5_edgemoment = [seed5_rootedge1_400; seed5_rootedge2_400; seed5_rootedge3_400];
seed6_edgemoment = [seed6_rootedge1_400; seed6_rootedge2_400; seed6_rootedge3_400];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds400 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_400_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 450 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_450 = seed1_rootflap1(1:450/0.008);
seed1_rootflap2_450 = seed1_rootflap2(1:450/0.008);
seed1_rootflap3_450 = seed1_rootflap3(1:450/0.008);
seed1_rootedge1_450 = seed1_rootedge1(1:450/0.008);
seed1_rootedge2_450 = seed1_rootedge2(1:450/0.008);
seed1_rootedge3_450 = seed1_rootedge3(1:450/0.008);


seed2_rootflap1_450 = seed2_rootflap1(1:450/0.008);
seed2_rootflap2_450 = seed2_rootflap2(1:450/0.008);
seed2_rootflap3_450 = seed2_rootflap3(1:450/0.008);
seed2_rootedge1_450 = seed2_rootedge1(1:450/0.008);
seed2_rootedge2_450 = seed2_rootedge2(1:450/0.008);
seed2_rootedge3_450 = seed2_rootedge3(1:450/0.008);

seed3_rootflap1_450 = seed3_rootflap1(1:450/0.008);
seed3_rootflap2_450 = seed3_rootflap2(1:450/0.008);
seed3_rootflap3_450 = seed3_rootflap3(1:450/0.008);
seed3_rootedge1_450 = seed3_rootedge1(1:450/0.008);
seed3_rootedge2_450 = seed3_rootedge2(1:450/0.008);
seed3_rootedge3_450 = seed3_rootedge3(1:450/0.008);

seed4_rootflap1_450 = seed4_rootflap1(1:450/0.008);
seed4_rootflap2_450 = seed4_rootflap2(1:450/0.008);
seed4_rootflap3_450 = seed4_rootflap3(1:450/0.008);
seed4_rootedge1_450 = seed4_rootedge1(1:450/0.008);
seed4_rootedge2_450 = seed4_rootedge2(1:450/0.008);
seed4_rootedge3_450 = seed4_rootedge3(1:450/0.008);

seed5_rootflap1_450 = seed5_rootflap1(1:450/0.008);
seed5_rootflap2_450 = seed5_rootflap2(1:450/0.008);
seed5_rootflap3_450 = seed5_rootflap3(1:450/0.008);
seed5_rootedge1_450 = seed5_rootedge1(1:450/0.008);
seed5_rootedge2_450 = seed5_rootedge2(1:450/0.008);
seed5_rootedge3_450 = seed5_rootedge3(1:450/0.008);

seed6_rootflap1_450 = seed6_rootflap1(1:450/0.008);
seed6_rootflap2_450 = seed6_rootflap2(1:450/0.008);
seed6_rootflap3_450 = seed6_rootflap3(1:450/0.008);
seed6_rootedge1_450 = seed6_rootedge1(1:450/0.008);
seed6_rootedge2_450 = seed6_rootedge2(1:450/0.008);
seed6_rootedge3_450 = seed6_rootedge3(1:450/0.008);

seed1_rootflap1_450(1:t_remove/0.008)=[];
seed1_rootflap2_450(1:t_remove/0.008)=[];
seed1_rootflap3_450(1:t_remove/0.008)=[];
seed1_rootedge1_450(1:t_remove/0.008)=[];
seed1_rootedge2_450(1:t_remove/0.008)=[];
seed1_rootedge3_450(1:t_remove/0.008)=[];
seed2_rootflap1_450(1:t_remove/0.008)=[];
seed2_rootflap2_450(1:t_remove/0.008)=[];
seed2_rootflap3_450(1:t_remove/0.008)=[];
seed2_rootedge1_450(1:t_remove/0.008)=[];
seed2_rootedge2_450(1:t_remove/0.008)=[];
seed2_rootedge3_450(1:t_remove/0.008)=[];
seed3_rootflap1_450(1:t_remove/0.008)=[];
seed3_rootflap2_450(1:t_remove/0.008)=[];
seed3_rootflap3_450(1:t_remove/0.008)=[];
seed3_rootedge1_450(1:t_remove/0.008)=[];
seed3_rootedge2_450(1:t_remove/0.008)=[];
seed3_rootedge3_450(1:t_remove/0.008)=[];
seed4_rootflap1_450(1:t_remove/0.008)=[];
seed4_rootflap2_450(1:t_remove/0.008)=[];
seed4_rootflap3_450(1:t_remove/0.008)=[];
seed4_rootedge1_450(1:t_remove/0.008)=[];
seed4_rootedge2_450(1:t_remove/0.008)=[];
seed4_rootedge3_450(1:t_remove/0.008)=[];
seed5_rootflap1_450(1:t_remove/0.008)=[];
seed5_rootflap2_450(1:t_remove/0.008)=[];
seed5_rootflap3_450(1:t_remove/0.008)=[];
seed5_rootedge1_450(1:t_remove/0.008)=[];
seed5_rootedge2_450(1:t_remove/0.008)=[];
seed5_rootedge3_450(1:t_remove/0.008)=[];
seed6_rootflap1_450(1:t_remove/0.008)=[];
seed6_rootflap2_450(1:t_remove/0.008)=[];
seed6_rootflap3_450(1:t_remove/0.008)=[];
seed6_rootedge1_450(1:t_remove/0.008)=[];
seed6_rootedge2_450(1:t_remove/0.008)=[];
seed6_rootedge3_450(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_450 ; seed1_rootflap2_450 ; seed1_rootflap3_450];
seed2_flpmoment = [seed2_rootflap1_450 ; seed2_rootflap2_450 ; seed2_rootflap3_450];
seed3_flpmoment = [seed3_rootflap1_450 ; seed3_rootflap2_450 ; seed3_rootflap3_450];
seed4_flpmoment = [seed4_rootflap1_450 ; seed4_rootflap2_450 ; seed4_rootflap3_450];
seed5_flpmoment = [seed5_rootflap1_450 ; seed5_rootflap2_450 ; seed5_rootflap3_450];
seed6_flpmoment = [seed6_rootflap1_450 ; seed6_rootflap2_450 ; seed6_rootflap3_450];

seed1_edgemoment = [seed1_rootedge1_450; seed1_rootedge2_450; seed1_rootedge3_450];
seed2_edgemoment = [seed2_rootedge1_450; seed2_rootedge2_450; seed2_rootedge3_450];
seed3_edgemoment = [seed3_rootedge1_450; seed3_rootedge2_450; seed3_rootedge3_450];
seed4_edgemoment = [seed4_rootedge1_450; seed4_rootedge2_450; seed4_rootedge3_450];
seed5_edgemoment = [seed5_rootedge1_450; seed5_rootedge2_450; seed5_rootedge3_450];
seed6_edgemoment = [seed6_rootedge1_450; seed6_rootedge2_450; seed6_rootedge3_450];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds450 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_450_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 500 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_500 = seed1_rootflap1(1:500/0.008);
seed1_rootflap2_500 = seed1_rootflap2(1:500/0.008);
seed1_rootflap3_500 = seed1_rootflap3(1:500/0.008);
seed1_rootedge1_500 = seed1_rootedge1(1:500/0.008);
seed1_rootedge2_500 = seed1_rootedge2(1:500/0.008);
seed1_rootedge3_500 = seed1_rootedge3(1:500/0.008);


seed2_rootflap1_500 = seed2_rootflap1(1:500/0.008);
seed2_rootflap2_500 = seed2_rootflap2(1:500/0.008);
seed2_rootflap3_500 = seed2_rootflap3(1:500/0.008);
seed2_rootedge1_500 = seed2_rootedge1(1:500/0.008);
seed2_rootedge2_500 = seed2_rootedge2(1:500/0.008);
seed2_rootedge3_500 = seed2_rootedge3(1:500/0.008);

seed3_rootflap1_500 = seed3_rootflap1(1:500/0.008);
seed3_rootflap2_500 = seed3_rootflap2(1:500/0.008);
seed3_rootflap3_500 = seed3_rootflap3(1:500/0.008);
seed3_rootedge1_500 = seed3_rootedge1(1:500/0.008);
seed3_rootedge2_500 = seed3_rootedge2(1:500/0.008);
seed3_rootedge3_500 = seed3_rootedge3(1:500/0.008);

seed4_rootflap1_500 = seed4_rootflap1(1:500/0.008);
seed4_rootflap2_500 = seed4_rootflap2(1:500/0.008);
seed4_rootflap3_500 = seed4_rootflap3(1:500/0.008);
seed4_rootedge1_500 = seed4_rootedge1(1:500/0.008);
seed4_rootedge2_500 = seed4_rootedge2(1:500/0.008);
seed4_rootedge3_500 = seed4_rootedge3(1:500/0.008);

seed5_rootflap1_500 = seed5_rootflap1(1:500/0.008);
seed5_rootflap2_500 = seed5_rootflap2(1:500/0.008);
seed5_rootflap3_500 = seed5_rootflap3(1:500/0.008);
seed5_rootedge1_500 = seed5_rootedge1(1:500/0.008);
seed5_rootedge2_500 = seed5_rootedge2(1:500/0.008);
seed5_rootedge3_500 = seed5_rootedge3(1:500/0.008);

seed6_rootflap1_500 = seed6_rootflap1(1:500/0.008);
seed6_rootflap2_500 = seed6_rootflap2(1:500/0.008);
seed6_rootflap3_500 = seed6_rootflap3(1:500/0.008);
seed6_rootedge1_500 = seed6_rootedge1(1:500/0.008);
seed6_rootedge2_500 = seed6_rootedge2(1:500/0.008);
seed6_rootedge3_500 = seed6_rootedge3(1:500/0.008);

seed1_rootflap1_500(1:t_remove/0.008)=[];
seed1_rootflap2_500(1:t_remove/0.008)=[];
seed1_rootflap3_500(1:t_remove/0.008)=[];
seed1_rootedge1_500(1:t_remove/0.008)=[];
seed1_rootedge2_500(1:t_remove/0.008)=[];
seed1_rootedge3_500(1:t_remove/0.008)=[];
seed2_rootflap1_500(1:t_remove/0.008)=[];
seed2_rootflap2_500(1:t_remove/0.008)=[];
seed2_rootflap3_500(1:t_remove/0.008)=[];
seed2_rootedge1_500(1:t_remove/0.008)=[];
seed2_rootedge2_500(1:t_remove/0.008)=[];
seed2_rootedge3_500(1:t_remove/0.008)=[];
seed3_rootflap1_500(1:t_remove/0.008)=[];
seed3_rootflap2_500(1:t_remove/0.008)=[];
seed3_rootflap3_500(1:t_remove/0.008)=[];
seed3_rootedge1_500(1:t_remove/0.008)=[];
seed3_rootedge2_500(1:t_remove/0.008)=[];
seed3_rootedge3_500(1:t_remove/0.008)=[];
seed4_rootflap1_500(1:t_remove/0.008)=[];
seed4_rootflap2_500(1:t_remove/0.008)=[];
seed4_rootflap3_500(1:t_remove/0.008)=[];
seed4_rootedge1_500(1:t_remove/0.008)=[];
seed4_rootedge2_500(1:t_remove/0.008)=[];
seed4_rootedge3_500(1:t_remove/0.008)=[];
seed5_rootflap1_500(1:t_remove/0.008)=[];
seed5_rootflap2_500(1:t_remove/0.008)=[];
seed5_rootflap3_500(1:t_remove/0.008)=[];
seed5_rootedge1_500(1:t_remove/0.008)=[];
seed5_rootedge2_500(1:t_remove/0.008)=[];
seed5_rootedge3_500(1:t_remove/0.008)=[];
seed6_rootflap1_500(1:t_remove/0.008)=[];
seed6_rootflap2_500(1:t_remove/0.008)=[];
seed6_rootflap3_500(1:t_remove/0.008)=[];
seed6_rootedge1_500(1:t_remove/0.008)=[];
seed6_rootedge2_500(1:t_remove/0.008)=[];
seed6_rootedge3_500(1:t_remove/0.008)=[];

seed1_flpmoment = [seed1_rootflap1_500 ; seed1_rootflap2_500 ; seed1_rootflap3_500];
seed2_flpmoment = [seed2_rootflap1_500 ; seed2_rootflap2_500 ; seed2_rootflap3_500];
seed3_flpmoment = [seed3_rootflap1_500 ; seed3_rootflap2_500 ; seed3_rootflap3_500];
seed4_flpmoment = [seed4_rootflap1_500 ; seed4_rootflap2_500 ; seed4_rootflap3_500];
seed5_flpmoment = [seed5_rootflap1_500 ; seed5_rootflap2_500 ; seed5_rootflap3_500];
seed6_flpmoment = [seed6_rootflap1_500 ; seed6_rootflap2_500 ; seed6_rootflap3_500];

seed1_edgemoment = [seed1_rootedge1_500; seed1_rootedge2_500; seed1_rootedge3_500];
seed2_edgemoment = [seed2_rootedge1_500; seed2_rootedge2_500; seed2_rootedge3_500];
seed3_edgemoment = [seed3_rootedge1_500; seed3_rootedge2_500; seed3_rootedge3_500];
seed4_edgemoment = [seed4_rootedge1_500; seed4_rootedge2_500; seed4_rootedge3_500];
seed5_edgemoment = [seed5_rootedge1_500; seed5_rootedge2_500; seed5_rootedge3_500];
seed6_edgemoment = [seed6_rootedge1_500; seed6_rootedge2_500; seed6_rootedge3_500];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds500 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_500_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 550 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_550 = seed1_rootflap1(1:550/0.008);
seed1_rootflap2_550 = seed1_rootflap2(1:550/0.008);
seed1_rootflap3_550 = seed1_rootflap3(1:550/0.008);
seed1_rootedge1_550 = seed1_rootedge1(1:550/0.008);
seed1_rootedge2_550 = seed1_rootedge2(1:550/0.008);
seed1_rootedge3_550 = seed1_rootedge3(1:550/0.008);


seed2_rootflap1_550 = seed2_rootflap1(1:550/0.008);
seed2_rootflap2_550 = seed2_rootflap2(1:550/0.008);
seed2_rootflap3_550 = seed2_rootflap3(1:550/0.008);
seed2_rootedge1_550 = seed2_rootedge1(1:550/0.008);
seed2_rootedge2_550 = seed2_rootedge2(1:550/0.008);
seed2_rootedge3_550 = seed2_rootedge3(1:550/0.008);

seed3_rootflap1_550 = seed3_rootflap1(1:550/0.008);
seed3_rootflap2_550 = seed3_rootflap2(1:550/0.008);
seed3_rootflap3_550 = seed3_rootflap3(1:550/0.008);
seed3_rootedge1_550 = seed3_rootedge1(1:550/0.008);
seed3_rootedge2_550 = seed3_rootedge2(1:550/0.008);
seed3_rootedge3_550 = seed3_rootedge3(1:550/0.008);

seed4_rootflap1_550 = seed4_rootflap1(1:550/0.008);
seed4_rootflap2_550 = seed4_rootflap2(1:550/0.008);
seed4_rootflap3_550 = seed4_rootflap3(1:550/0.008);
seed4_rootedge1_550 = seed4_rootedge1(1:550/0.008);
seed4_rootedge2_550 = seed4_rootedge2(1:550/0.008);
seed4_rootedge3_550 = seed4_rootedge3(1:550/0.008);

seed5_rootflap1_550 = seed5_rootflap1(1:550/0.008);
seed5_rootflap2_550 = seed5_rootflap2(1:550/0.008);
seed5_rootflap3_550 = seed5_rootflap3(1:550/0.008);
seed5_rootedge1_550 = seed5_rootedge1(1:550/0.008);
seed5_rootedge2_550 = seed5_rootedge2(1:550/0.008);
seed5_rootedge3_550 = seed5_rootedge3(1:550/0.008);

seed6_rootflap1_550 = seed6_rootflap1(1:550/0.008);
seed6_rootflap2_550 = seed6_rootflap2(1:550/0.008);
seed6_rootflap3_550 = seed6_rootflap3(1:550/0.008);
seed6_rootedge1_550 = seed6_rootedge1(1:550/0.008);
seed6_rootedge2_550 = seed6_rootedge2(1:550/0.008);
seed6_rootedge3_550 = seed6_rootedge3(1:550/0.008);

seed1_rootflap1_550(1:t_remove/0.008)=[];
seed1_rootflap2_550(1:t_remove/0.008)=[];
seed1_rootflap3_550(1:t_remove/0.008)=[];
seed1_rootedge1_550(1:t_remove/0.008)=[];
seed1_rootedge2_550(1:t_remove/0.008)=[];
seed1_rootedge3_550(1:t_remove/0.008)=[];
seed2_rootflap1_550(1:t_remove/0.008)=[];
seed2_rootflap2_550(1:t_remove/0.008)=[];
seed2_rootflap3_550(1:t_remove/0.008)=[];
seed2_rootedge1_550(1:t_remove/0.008)=[];
seed2_rootedge2_550(1:t_remove/0.008)=[];
seed2_rootedge3_550(1:t_remove/0.008)=[];
seed3_rootflap1_550(1:t_remove/0.008)=[];
seed3_rootflap2_550(1:t_remove/0.008)=[];
seed3_rootflap3_550(1:t_remove/0.008)=[];
seed3_rootedge1_550(1:t_remove/0.008)=[];
seed3_rootedge2_550(1:t_remove/0.008)=[];
seed3_rootedge3_550(1:t_remove/0.008)=[];
seed4_rootflap1_550(1:t_remove/0.008)=[];
seed4_rootflap2_550(1:t_remove/0.008)=[];
seed4_rootflap3_550(1:t_remove/0.008)=[];
seed4_rootedge1_550(1:t_remove/0.008)=[];
seed4_rootedge2_550(1:t_remove/0.008)=[];
seed4_rootedge3_550(1:t_remove/0.008)=[];
seed5_rootflap1_550(1:t_remove/0.008)=[];
seed5_rootflap2_550(1:t_remove/0.008)=[];
seed5_rootflap3_550(1:t_remove/0.008)=[];
seed5_rootedge1_550(1:t_remove/0.008)=[];
seed5_rootedge2_550(1:t_remove/0.008)=[];
seed5_rootedge3_550(1:t_remove/0.008)=[];
seed6_rootflap1_550(1:t_remove/0.008)=[];
seed6_rootflap2_550(1:t_remove/0.008)=[];
seed6_rootflap3_550(1:t_remove/0.008)=[];
seed6_rootedge1_550(1:t_remove/0.008)=[];
seed6_rootedge2_550(1:t_remove/0.008)=[];
seed6_rootedge3_550(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_550 ; seed1_rootflap2_550 ; seed1_rootflap3_550];
seed2_flpmoment = [seed2_rootflap1_550 ; seed2_rootflap2_550 ; seed2_rootflap3_550];
seed3_flpmoment = [seed3_rootflap1_550 ; seed3_rootflap2_550 ; seed3_rootflap3_550];
seed4_flpmoment = [seed4_rootflap1_550 ; seed4_rootflap2_550 ; seed4_rootflap3_550];
seed5_flpmoment = [seed5_rootflap1_550 ; seed5_rootflap2_550 ; seed5_rootflap3_550];
seed6_flpmoment = [seed6_rootflap1_550 ; seed6_rootflap2_550 ; seed6_rootflap3_550];

seed1_edgemoment = [seed1_rootedge1_550; seed1_rootedge2_550; seed1_rootedge3_550];
seed2_edgemoment = [seed2_rootedge1_550; seed2_rootedge2_550; seed2_rootedge3_550];
seed3_edgemoment = [seed3_rootedge1_550; seed3_rootedge2_550; seed3_rootedge3_550];
seed4_edgemoment = [seed4_rootedge1_550; seed4_rootedge2_550; seed4_rootedge3_550];
seed5_edgemoment = [seed5_rootedge1_550; seed5_rootedge2_550; seed5_rootedge3_550];
seed6_edgemoment = [seed6_rootedge1_550; seed6_rootedge2_550; seed6_rootedge3_550];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds550 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_550_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 600 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_rootflap1_600 = seed1_rootflap1(1:600/0.008);
seed1_rootflap2_600 = seed1_rootflap2(1:600/0.008);
seed1_rootflap3_600 = seed1_rootflap3(1:600/0.008);
seed1_rootedge1_600 = seed1_rootedge1(1:600/0.008);
seed1_rootedge2_600 = seed1_rootedge2(1:600/0.008);
seed1_rootedge3_600 = seed1_rootedge3(1:600/0.008);


seed2_rootflap1_600 = seed2_rootflap1(1:600/0.008);
seed2_rootflap2_600 = seed2_rootflap2(1:600/0.008);
seed2_rootflap3_600 = seed2_rootflap3(1:600/0.008);
seed2_rootedge1_600 = seed2_rootedge1(1:600/0.008);
seed2_rootedge2_600 = seed2_rootedge2(1:600/0.008);
seed2_rootedge3_600 = seed2_rootedge3(1:600/0.008);

seed3_rootflap1_600 = seed3_rootflap1(1:600/0.008);
seed3_rootflap2_600 = seed3_rootflap2(1:600/0.008);
seed3_rootflap3_600 = seed3_rootflap3(1:600/0.008);
seed3_rootedge1_600 = seed3_rootedge1(1:600/0.008);
seed3_rootedge2_600 = seed3_rootedge2(1:600/0.008);
seed3_rootedge3_600 = seed3_rootedge3(1:600/0.008);

seed4_rootflap1_600 = seed4_rootflap1(1:600/0.008);
seed4_rootflap2_600 = seed4_rootflap2(1:600/0.008);
seed4_rootflap3_600 = seed4_rootflap3(1:600/0.008);
seed4_rootedge1_600 = seed4_rootedge1(1:600/0.008);
seed4_rootedge2_600 = seed4_rootedge2(1:600/0.008);
seed4_rootedge3_600 = seed4_rootedge3(1:600/0.008);

seed5_rootflap1_600 = seed5_rootflap1(1:600/0.008);
seed5_rootflap2_600 = seed5_rootflap2(1:600/0.008);
seed5_rootflap3_600 = seed5_rootflap3(1:600/0.008);
seed5_rootedge1_600 = seed5_rootedge1(1:600/0.008);
seed5_rootedge2_600 = seed5_rootedge2(1:600/0.008);
seed5_rootedge3_600 = seed5_rootedge3(1:600/0.008);

seed6_rootflap1_600 = seed6_rootflap1(1:600/0.008);
seed6_rootflap2_600 = seed6_rootflap2(1:600/0.008);
seed6_rootflap3_600 = seed6_rootflap3(1:600/0.008);
seed6_rootedge1_600 = seed6_rootedge1(1:600/0.008);
seed6_rootedge2_600 = seed6_rootedge2(1:600/0.008);
seed6_rootedge3_600 = seed6_rootedge3(1:600/0.008);

seed1_rootflap1_600(1:t_remove/0.008)=[];
seed1_rootflap2_600(1:t_remove/0.008)=[];
seed1_rootflap3_600(1:t_remove/0.008)=[];
seed1_rootedge1_600(1:t_remove/0.008)=[];
seed1_rootedge2_600(1:t_remove/0.008)=[];
seed1_rootedge3_600(1:t_remove/0.008)=[];
seed2_rootflap1_600(1:t_remove/0.008)=[];
seed2_rootflap2_600(1:t_remove/0.008)=[];
seed2_rootflap3_600(1:t_remove/0.008)=[];
seed2_rootedge1_600(1:t_remove/0.008)=[];
seed2_rootedge2_600(1:t_remove/0.008)=[];
seed2_rootedge3_600(1:t_remove/0.008)=[];
seed3_rootflap1_600(1:t_remove/0.008)=[];
seed3_rootflap2_600(1:t_remove/0.008)=[];
seed3_rootflap3_600(1:t_remove/0.008)=[];
seed3_rootedge1_600(1:t_remove/0.008)=[];
seed3_rootedge2_600(1:t_remove/0.008)=[];
seed3_rootedge3_600(1:t_remove/0.008)=[];
seed4_rootflap1_600(1:t_remove/0.008)=[];
seed4_rootflap2_600(1:t_remove/0.008)=[];
seed4_rootflap3_600(1:t_remove/0.008)=[];
seed4_rootedge1_600(1:t_remove/0.008)=[];
seed4_rootedge2_600(1:t_remove/0.008)=[];
seed4_rootedge3_600(1:t_remove/0.008)=[];
seed5_rootflap1_600(1:t_remove/0.008)=[];
seed5_rootflap2_600(1:t_remove/0.008)=[];
seed5_rootflap3_600(1:t_remove/0.008)=[];
seed5_rootedge1_600(1:t_remove/0.008)=[];
seed5_rootedge2_600(1:t_remove/0.008)=[];
seed5_rootedge3_600(1:t_remove/0.008)=[];
seed6_rootflap1_600(1:t_remove/0.008)=[];
seed6_rootflap2_600(1:t_remove/0.008)=[];
seed6_rootflap3_600(1:t_remove/0.008)=[];
seed6_rootedge1_600(1:t_remove/0.008)=[];
seed6_rootedge2_600(1:t_remove/0.008)=[];
seed6_rootedge3_600(1:t_remove/0.008)=[];


seed1_flpmoment = [seed1_rootflap1_600 ; seed1_rootflap2_600 ; seed1_rootflap3_600];
seed2_flpmoment = [seed2_rootflap1_600 ; seed2_rootflap2_600 ; seed2_rootflap3_600];
seed3_flpmoment = [seed3_rootflap1_600 ; seed3_rootflap2_600 ; seed3_rootflap3_600];
seed4_flpmoment = [seed4_rootflap1_600 ; seed4_rootflap2_600 ; seed4_rootflap3_600];
seed5_flpmoment = [seed5_rootflap1_600 ; seed5_rootflap2_600 ; seed5_rootflap3_600];
seed6_flpmoment = [seed6_rootflap1_600 ; seed6_rootflap2_600 ; seed6_rootflap3_600];

seed1_edgemoment = [seed1_rootedge1_600; seed1_rootedge2_600; seed1_rootedge3_600];
seed2_edgemoment = [seed2_rootedge1_600; seed2_rootedge2_600; seed2_rootedge3_600];
seed3_edgemoment = [seed3_rootedge1_600; seed3_rootedge2_600; seed3_rootedge3_600];
seed4_edgemoment = [seed4_rootedge1_600; seed4_rootedge2_600; seed4_rootedge3_600];
seed5_edgemoment = [seed5_rootedge1_600; seed5_rootedge2_600; seed5_rootedge3_600];
seed6_edgemoment = [seed6_rootedge1_600; seed6_rootedge2_600; seed6_rootedge3_600];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds600 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_600_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;


rootmoment =[seed_70_rootmoment, seed_100_rootmoment, seed_150_rootmoment, seed_200_rootmoment,...
    seed_250_rootmoment, seed_300_rootmoment, seed_350_rootmoment,...
    seed_400_rootmoment, seed_450_rootmoment, seed_500_rootmoment,...
    seed_550_rootmoment, seed_600_rootmoment]; 

%% Plot tip defl

%%%%% plot individual seeds %%%% 
figure(1)
x = [70, 70, 70, 70, 70, 70];
plot(x, tip_seeds70, '+'); hold on;

x=[100, 100, 100, 100, 100, 100];
plot(x, tip_seeds100, '+'); 

x=[150,150,150 150,150,150];
plot(x, tip_seeds150, '+'); 

x=[200, 200, 200, 200, 200, 200];
plot(x, tip_seeds200, '+');

x=[250, 250, 250, 250, 250, 250];
plot(x, tip_seeds250, '+');

x=[300, 300, 300, 300, 300, 300];
plot(x, tip_seeds300, '+');

x=[350, 350, 350, 350, 350, 350];
plot(x, tip_seeds350, '+');

x=[400, 400, 400, 400, 400, 400];
plot(x, tip_seeds400, '+');

x=[450, 450, 450, 450, 450, 450];
plot(x, tip_seeds450, '+');

x=[500, 500, 500, 500, 500, 500];
plot(x, tip_seeds500, '+');

x=[550, 550, 550, 550, 550, 550];
plot(x, tip_seeds550, '+');

x=[600, 600, 600, 600, 600, 600];
plot(x, tip_seeds600, '+');


x=[70, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600];
plot(x,tip_defl);
grid on;
ylabel('Tip Deflection (m)','Interpreter','latex');
xlabel('Simulation Time (s)','Interpreter','latex');

ylim([5 9]);



%% Plot root moment

%%%%% plot individual seeds %%%% 
figure(2)
x = [70, 70, 70, 70, 70, 70];
plot(x, root_seeds70,'+'); hold on; %, '+'); hold on;

x=[100, 100, 100, 100, 100, 100];
plot(x, root_seeds100, '+'); 

x=[150,150,150 150,150,150];
plot(x, root_seeds150, '+'); 

x=[200, 200, 200, 200, 200, 200];
plot(x, root_seeds200, '+');

x=[250, 250, 250, 250, 250, 250];
plot(x, root_seeds250,'+');

x=[300, 300, 300, 300, 300, 300];
plot(x, root_seeds300, '+');

x=[350, 350, 350, 350, 350, 350];
plot(x, root_seeds350, '+');

x=[400, 400, 400, 400, 400, 400];
plot(x, root_seeds400, '+');

x=[450, 450, 450, 450, 450, 450];
plot(x, root_seeds450, '+');

x=[500, 500, 500, 500, 500, 500];
plot(x, root_seeds500,'+');

x=[550, 550, 550, 550, 550, 550];
plot(x, root_seeds550,'+');

x=[600, 600, 600, 600, 600, 600];
plot(x, root_seeds600,'+');



x=[70, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]; 
plot(x,rootmoment);
grid on;
ylabel('Root Moment(KNm)','Interpreter','latex');
xlabel('Simulation Time (s)','Interpreter','latex');

ylim([10000 18000]);
