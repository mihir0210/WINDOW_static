%%%% Plots and comparisons %%%%
%% Load mat files
seed1_70 = load(fullfile(cd,'70s\DLC1.3_seed=1.mat'));
seed2_70 = load(fullfile(cd,'70s\DLC1.3_seed=2.mat'));
seed3_70 = load(fullfile(cd,'70s\DLC1.3_seed=3.mat'));
seed4_70 = load(fullfile(cd,'70s\DLC1.3_seed=4.mat'));
seed5_70 = load(fullfile(cd,'70s\DLC1.3_seed=5.mat'));
seed6_70 = load(fullfile(cd,'70s\DLC1.3_seed=6.mat'));

seed1_100 = load(fullfile(cd,'100s\DLC1.3_100_seed=1.mat'));
seed2_100 = load(fullfile(cd,'100s\DLC1.3_100_seed=2.mat'));
seed3_100 = load(fullfile(cd,'100s\DLC1.3_100_seed=3.mat'));
seed4_100 = load(fullfile(cd,'100s\DLC1.3_100_seed=4.mat'));
seed5_100 = load(fullfile(cd,'100s\DLC1.3_100_seed=5.mat'));
seed6_100 = load(fullfile(cd,'100s\DLC1.3_100_seed=6.mat'));


seed1_150 = load(fullfile(cd,'150s\DLC1.3_150_seed=1.mat'));
seed2_150 = load(fullfile(cd,'150s\DLC1.3_150_seed=2.mat'));
seed3_150 = load(fullfile(cd,'150s\DLC1.3_150_seed=3.mat'));
seed4_150 = load(fullfile(cd,'150s\DLC1.3_150_seed=4.mat'));
seed5_150 = load(fullfile(cd,'150s\DLC1.3_150_seed=5.mat'));
seed6_150 = load(fullfile(cd,'150s\DLC1.3_150_seed=6.mat'));

seed1_200 = load(fullfile(cd,'200s\DLC1.3_200_seed=1.mat'));
seed2_200 = load(fullfile(cd,'200s\DLC1.3_200_seed=2.mat'));
seed3_200 = load(fullfile(cd,'200s\DLC1.3_200_seed=3.mat'));
seed4_200 = load(fullfile(cd,'200s\DLC1.3_200_seed=4.mat'));
seed5_200 = load(fullfile(cd,'200s\DLC1.3_200_seed=5.mat'));
seed6_200 = load(fullfile(cd,'200s\DLC1.3_200_seed=6.mat'));

seed1_250 = load(fullfile(cd,'250s\DLC1.3_250_seed=1.mat'));
seed2_250 = load(fullfile(cd,'250s\DLC1.3_250_seed=2.mat'));
seed3_250 = load(fullfile(cd,'250s\DLC1.3_250_seed=3.mat'));
seed4_250 = load(fullfile(cd,'250s\DLC1.3_250_seed=4.mat'));
seed5_250 = load(fullfile(cd,'250s\DLC1.3_250_seed=5.mat'));
seed6_250 = load(fullfile(cd,'250s\DLC1.3_250_seed=6.mat'));

seed1_300 = load(fullfile(cd,'300s\DLC1.3_300_seed=1.mat'));
seed2_300 = load(fullfile(cd,'300s\DLC1.3_300_seed=2.mat'));
seed3_300 = load(fullfile(cd,'300s\DLC1.3_300_seed=3.mat'));
seed4_300 = load(fullfile(cd,'300s\DLC1.3_300_seed=4.mat'));
seed5_300 = load(fullfile(cd,'300s\DLC1.3_300_seed=5.mat'));
seed6_300 = load(fullfile(cd,'300s\DLC1.3_300_seed=6.mat'));


seed1_350 = load(fullfile(cd,'350s\DLC1.3_350_seed=1.mat'));
seed2_350 = load(fullfile(cd,'350s\DLC1.3_350_seed=2.mat'));
seed3_350 = load(fullfile(cd,'350s\DLC1.3_350_seed=3.mat'));
seed4_350 = load(fullfile(cd,'350s\DLC1.3_350_seed=4.mat'));
seed5_350 = load(fullfile(cd,'350s\DLC1.3_350_seed=5.mat'));
seed6_350 = load(fullfile(cd,'350s\DLC1.3_350_seed=6.mat'));


seed1_400 = load(fullfile(cd,'400s\DLC1.3_400_seed=1.mat'));
seed2_400 = load(fullfile(cd,'400s\DLC1.3_400_seed=2.mat'));
seed3_400 = load(fullfile(cd,'400s\DLC1.3_400_seed=3.mat'));
seed4_400 = load(fullfile(cd,'400s\DLC1.3_400_seed=4.mat'));
seed5_400 = load(fullfile(cd,'400s\DLC1.3_400_seed=5.mat'));
seed6_400 = load(fullfile(cd,'400s\DLC1.3_400_seed=6.mat'));

seed1_450 = load(fullfile(cd,'450s\DLC1.3_450_seed=1.mat'));
seed2_450 = load(fullfile(cd,'450s\DLC1.3_450_seed=2.mat'));
seed3_450 = load(fullfile(cd,'450s\DLC1.3_450_seed=3.mat'));
seed4_450 = load(fullfile(cd,'450s\DLC1.3_450_seed=4.mat'));
seed5_450 = load(fullfile(cd,'450s\DLC1.3_450_seed=5.mat'));
seed6_450 = load(fullfile(cd,'450s\DLC1.3_450_seed=6.mat'));


seed1_500 = load(fullfile(cd,'500s\DLC1.3_500_seed=1.mat'));
seed2_500 = load(fullfile(cd,'500s\DLC1.3_500_seed=2.mat'));
seed3_500 = load(fullfile(cd,'500s\DLC1.3_500_seed=3.mat'));
seed4_500 = load(fullfile(cd,'500s\DLC1.3_500_seed=4.mat'));
seed5_500 = load(fullfile(cd,'500s\DLC1.3_500_seed=5.mat'));
seed6_500 = load(fullfile(cd,'500s\DLC1.3_500_seed=6.mat'));

seed1_550 = load(fullfile(cd,'550s\DLC1.3_550_seed=1.mat'));
seed2_550 = load(fullfile(cd,'550s\DLC1.3_550_seed=2.mat'));
seed3_550 = load(fullfile(cd,'550s\DLC1.3_550_seed=3.mat'));
seed4_550 = load(fullfile(cd,'550s\DLC1.3_550_seed=4.mat'));
seed5_550 = load(fullfile(cd,'550s\DLC1.3_550_seed=5.mat'));
seed6_550 = load(fullfile(cd,'550s\DLC1.3_550_seed=6.mat'));

seed1_600 = load(fullfile(cd,'600s\DLC1.3_600_seed=1.mat'));
seed2_600 = load(fullfile(cd,'600s\DLC1.3_600_seed=2.mat'));
seed3_600 = load(fullfile(cd,'600s\DLC1.3_600_seed=3.mat'));
seed4_600 = load(fullfile(cd,'600s\DLC1.3_600_seed=4.mat'));
seed5_600 = load(fullfile(cd,'600s\DLC1.3_600_seed=5.mat'));
seed6_600 = load(fullfile(cd,'600s\DLC1.3_600_seed=6.mat'));


seed1_660 = load(fullfile(cd,'660s\DLC1.3_660_seed=1.mat'));
seed2_660 = load(fullfile(cd,'660s\DLC1.3_660_seed=2.mat'));
seed3_660 = load(fullfile(cd,'660s\DLC1.3_660_seed=3.mat'));
seed4_660 = load(fullfile(cd,'660s\DLC1.3_660_seed=4.mat'));
seed5_660 = load(fullfile(cd,'660s\DLC1.3_660_seed=5.mat'));
seed6_660 = load(fullfile(cd,'660s\DLC1.3_660_seed=6.mat'));

t_remove = 30; 

%% Compare Tip deflections

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 70 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_70.OoPDefl1(1:t_remove/0.008)=0;
seed1_70.OoPDefl2(1:t_remove/0.008) = 0;
seed1_70.OoPDefl3(1:t_remove/0.008)=0;
seed2_70.OoPDefl1(1:t_remove/0.008)=0;
seed2_70.OoPDefl2(1:t_remove/0.008) = 0;
seed2_70.OoPDefl3(1:t_remove/0.008)=0;
seed3_70.OoPDefl1(1:t_remove/0.008)=0;
seed3_70.OoPDefl2(1:t_remove/0.008) = 0;
seed3_70.OoPDefl3(1:t_remove/0.008)=0;
seed4_70.OoPDefl1(1:t_remove/0.008)=0;
seed4_70.OoPDefl2(1:t_remove/0.008) = 0;
seed4_70.OoPDefl3(1:t_remove/0.008)=0;
seed5_70.OoPDefl1(1:t_remove/0.008)=0;
seed5_70.OoPDefl2(1:t_remove/0.008) = 0;
seed5_70.OoPDefl3(1:t_remove/0.008)=0;
seed6_70.OoPDefl1(1:t_remove/0.008)=0;
seed6_70.OoPDefl2(1:t_remove/0.008) = 0;
seed6_70.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_70.OoPDefl1; seed1_70.OoPDefl2; seed1_70.OoPDefl3];
seed2_OoPDefl = [seed2_70.OoPDefl1; seed2_70.OoPDefl2; seed2_70.OoPDefl3];
seed3_OoPDefl = [seed3_70.OoPDefl1; seed3_70.OoPDefl2; seed3_70.OoPDefl3];
seed4_OoPDefl = [seed4_70.OoPDefl1; seed4_70.OoPDefl2; seed4_70.OoPDefl3];
seed5_OoPDefl = [seed5_70.OoPDefl1; seed5_70.OoPDefl2; seed5_70.OoPDefl3];
seed6_OoPDefl = [seed6_70.OoPDefl1; seed6_70.OoPDefl2; seed6_70.OoPDefl3];


tip_seeds70 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_70 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 100 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_100.OoPDefl1(1:t_remove/0.008)=0;
seed1_100.OoPDefl2(1:t_remove/0.008) = 0;
seed1_100.OoPDefl3(1:t_remove/0.008)=0;
seed2_100.OoPDefl1(1:t_remove/0.008)=0;
seed2_100.OoPDefl2(1:t_remove/0.008) = 0;
seed2_100.OoPDefl3(1:t_remove/0.008)=0;
seed3_100.OoPDefl1(1:t_remove/0.008)=0;
seed3_100.OoPDefl2(1:t_remove/0.008) = 0;
seed3_100.OoPDefl3(1:t_remove/0.008)=0;
seed4_100.OoPDefl1(1:t_remove/0.008)=0;
seed4_100.OoPDefl2(1:t_remove/0.008) = 0;
seed4_100.OoPDefl3(1:t_remove/0.008)=0;
seed5_100.OoPDefl1(1:t_remove/0.008)=0;
seed5_100.OoPDefl2(1:t_remove/0.008) = 0;
seed5_100.OoPDefl3(1:t_remove/0.008)=0;
seed6_100.OoPDefl1(1:t_remove/0.008)=0;
seed6_100.OoPDefl2(1:t_remove/0.008) = 0;
seed6_100.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_100.OoPDefl1; seed1_100.OoPDefl2; seed1_100.OoPDefl3];
seed2_OoPDefl = [seed2_100.OoPDefl1; seed2_100.OoPDefl2; seed2_100.OoPDefl3];
seed3_OoPDefl = [seed3_100.OoPDefl1; seed3_100.OoPDefl2; seed3_100.OoPDefl3];
seed4_OoPDefl = [seed4_100.OoPDefl1; seed4_100.OoPDefl2; seed4_100.OoPDefl3];
seed5_OoPDefl = [seed5_100.OoPDefl1; seed5_100.OoPDefl2; seed5_100.OoPDefl3];
seed6_OoPDefl = [seed6_100.OoPDefl1; seed6_100.OoPDefl2; seed6_100.OoPDefl3];


tip_seeds100 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_100 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 150 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_150.OoPDefl1(1:t_remove/0.008)=0;
seed1_150.OoPDefl2(1:t_remove/0.008) = 0;
seed1_150.OoPDefl3(1:t_remove/0.008)=0;
seed2_150.OoPDefl1(1:t_remove/0.008)=0;
seed2_150.OoPDefl2(1:t_remove/0.008) = 0;
seed2_150.OoPDefl3(1:t_remove/0.008)=0;
seed3_150.OoPDefl1(1:t_remove/0.008)=0;
seed3_150.OoPDefl2(1:t_remove/0.008) = 0;
seed3_150.OoPDefl3(1:t_remove/0.008)=0;
seed4_150.OoPDefl1(1:t_remove/0.008)=0;
seed4_150.OoPDefl2(1:t_remove/0.008) = 0;
seed4_150.OoPDefl3(1:t_remove/0.008)=0;
seed5_150.OoPDefl1(1:t_remove/0.008)=0;
seed5_150.OoPDefl2(1:t_remove/0.008) = 0;
seed5_150.OoPDefl3(1:t_remove/0.008)=0;
seed6_150.OoPDefl1(1:t_remove/0.008)=0;
seed6_150.OoPDefl2(1:t_remove/0.008) = 0;
seed6_150.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_150.OoPDefl1; seed1_150.OoPDefl2; seed1_150.OoPDefl3];
seed2_OoPDefl = [seed2_150.OoPDefl1; seed2_150.OoPDefl2; seed2_150.OoPDefl3];
seed3_OoPDefl = [seed3_150.OoPDefl1; seed3_150.OoPDefl2; seed3_150.OoPDefl3];
seed4_OoPDefl = [seed4_150.OoPDefl1; seed4_150.OoPDefl2; seed4_150.OoPDefl3];
seed5_OoPDefl = [seed5_150.OoPDefl1; seed5_150.OoPDefl2; seed5_150.OoPDefl3];
seed6_OoPDefl = [seed6_150.OoPDefl1; seed6_150.OoPDefl2; seed6_150.OoPDefl3];


tip_seeds150 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_150 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 200 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_200.OoPDefl1(1:20/0.008)=0;
seed1_200.OoPDefl2(1:20/0.008) = 0;
seed1_200.OoPDefl3(1:20/0.008)=0;
seed2_200.OoPDefl1(1:20/0.008)=0;
seed2_200.OoPDefl2(1:20/0.008) = 0;
seed2_200.OoPDefl3(1:20/0.008)=0;
seed3_200.OoPDefl1(1:20/0.008)=0;
seed3_200.OoPDefl2(1:20/0.008) = 0;
seed3_200.OoPDefl3(1:20/0.008)=0;
seed4_200.OoPDefl1(1:20/0.008)=0;
seed4_200.OoPDefl2(1:20/0.008) = 0;
seed4_200.OoPDefl3(1:20/0.008)=0;
seed5_200.OoPDefl1(1:20/0.008)=0;
seed5_200.OoPDefl2(1:20/0.008) = 0;
seed5_200.OoPDefl3(1:20/0.008)=0;
seed6_200.OoPDefl1(1:20/0.008)=0;
seed6_200.OoPDefl2(1:20/0.008) = 0;
seed6_200.OoPDefl3(1:20/0.008)=0;

seed1_OoPDefl = [seed1_200.OoPDefl1; seed1_200.OoPDefl2; seed1_200.OoPDefl3];
seed2_OoPDefl = [seed2_200.OoPDefl1; seed2_200.OoPDefl2; seed2_200.OoPDefl3];
seed3_OoPDefl = [seed3_200.OoPDefl1; seed3_200.OoPDefl2; seed3_200.OoPDefl3];
seed4_OoPDefl = [seed4_200.OoPDefl1; seed4_200.OoPDefl2; seed4_200.OoPDefl3];
seed5_OoPDefl = [seed5_200.OoPDefl1; seed5_200.OoPDefl2; seed5_200.OoPDefl3];
seed6_OoPDefl = [seed6_200.OoPDefl1; seed6_200.OoPDefl2; seed6_200.OoPDefl3];


tip_seeds200 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_200 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 250 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_250.OoPDefl1(1:t_remove/0.008)=0;
seed1_250.OoPDefl2(1:t_remove/0.008) = 0;
seed1_250.OoPDefl3(1:t_remove/0.008)=0;
seed2_250.OoPDefl1(1:t_remove/0.008)=0;
seed2_250.OoPDefl2(1:t_remove/0.008) = 0;
seed2_250.OoPDefl3(1:t_remove/0.008)=0;
seed3_250.OoPDefl1(1:t_remove/0.008)=0;
seed3_250.OoPDefl2(1:t_remove/0.008) = 0;
seed3_250.OoPDefl3(1:t_remove/0.008)=0;
seed4_250.OoPDefl1(1:t_remove/0.008)=0;
seed4_250.OoPDefl2(1:t_remove/0.008) = 0;
seed4_250.OoPDefl3(1:t_remove/0.008)=0;
seed5_250.OoPDefl1(1:t_remove/0.008)=0;
seed5_250.OoPDefl2(1:t_remove/0.008) = 0;
seed5_250.OoPDefl3(1:t_remove/0.008)=0;
seed6_250.OoPDefl1(1:t_remove/0.008)=0;
seed6_250.OoPDefl2(1:t_remove/0.008) = 0;
seed6_250.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_250.OoPDefl1; seed1_250.OoPDefl2; seed1_250.OoPDefl3];
seed2_OoPDefl = [seed2_250.OoPDefl1; seed2_250.OoPDefl2; seed2_250.OoPDefl3];
seed3_OoPDefl = [seed3_250.OoPDefl1; seed3_250.OoPDefl2; seed3_250.OoPDefl3];
seed4_OoPDefl = [seed4_250.OoPDefl1; seed4_250.OoPDefl2; seed4_250.OoPDefl3];
seed5_OoPDefl = [seed5_250.OoPDefl1; seed5_250.OoPDefl2; seed5_250.OoPDefl3];
seed6_OoPDefl = [seed6_250.OoPDefl1; seed6_250.OoPDefl2; seed6_250.OoPDefl3];


tip_seeds250 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_250 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 300 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_300.OoPDefl1(1:t_remove/0.008)=0;
seed1_300.OoPDefl2(1:t_remove/0.008) = 0;
seed1_300.OoPDefl3(1:t_remove/0.008)=0;
seed2_300.OoPDefl1(1:t_remove/0.008)=0;
seed2_300.OoPDefl2(1:t_remove/0.008) = 0;
seed2_300.OoPDefl3(1:t_remove/0.008)=0;
seed3_300.OoPDefl1(1:t_remove/0.008)=0;
seed3_300.OoPDefl2(1:t_remove/0.008) = 0;
seed3_300.OoPDefl3(1:t_remove/0.008)=0;
seed4_300.OoPDefl1(1:t_remove/0.008)=0;
seed4_300.OoPDefl2(1:t_remove/0.008) = 0;
seed4_300.OoPDefl3(1:t_remove/0.008)=0;
seed5_300.OoPDefl1(1:t_remove/0.008)=0;
seed5_300.OoPDefl2(1:t_remove/0.008) = 0;
seed5_300.OoPDefl3(1:t_remove/0.008)=0;
seed6_300.OoPDefl1(1:t_remove/0.008)=0;
seed6_300.OoPDefl2(1:t_remove/0.008) = 0;
seed6_300.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_300.OoPDefl1; seed1_300.OoPDefl2; seed1_300.OoPDefl3];
seed2_OoPDefl = [seed2_300.OoPDefl1; seed2_300.OoPDefl2; seed2_300.OoPDefl3];
seed3_OoPDefl = [seed3_300.OoPDefl1; seed3_300.OoPDefl2; seed3_300.OoPDefl3];
seed4_OoPDefl = [seed4_300.OoPDefl1; seed4_300.OoPDefl2; seed4_300.OoPDefl3];
seed5_OoPDefl = [seed5_300.OoPDefl1; seed5_300.OoPDefl2; seed5_300.OoPDefl3];
seed6_OoPDefl = [seed6_300.OoPDefl1; seed6_300.OoPDefl2; seed6_300.OoPDefl3];


tip_seeds300 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_300 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 350 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_350.OoPDefl1(1:t_remove/0.008)=0;
seed1_350.OoPDefl2(1:t_remove/0.008) = 0;
seed1_350.OoPDefl3(1:t_remove/0.008)=0;
seed2_350.OoPDefl1(1:t_remove/0.008)=0;
seed2_350.OoPDefl2(1:t_remove/0.008) = 0;
seed2_350.OoPDefl3(1:t_remove/0.008)=0;
seed3_350.OoPDefl1(1:t_remove/0.008)=0;
seed3_350.OoPDefl2(1:t_remove/0.008) = 0;
seed3_350.OoPDefl3(1:t_remove/0.008)=0;
seed4_350.OoPDefl1(1:t_remove/0.008)=0;
seed4_350.OoPDefl2(1:t_remove/0.008) = 0;
seed4_350.OoPDefl3(1:t_remove/0.008)=0;
seed5_350.OoPDefl1(1:t_remove/0.008)=0;
seed5_350.OoPDefl2(1:t_remove/0.008) = 0;
seed5_350.OoPDefl3(1:t_remove/0.008)=0;
seed6_350.OoPDefl1(1:t_remove/0.008)=0;
seed6_350.OoPDefl2(1:t_remove/0.008) = 0;
seed6_350.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_350.OoPDefl1; seed1_350.OoPDefl2; seed1_350.OoPDefl3];
seed2_OoPDefl = [seed2_350.OoPDefl1; seed2_350.OoPDefl2; seed2_350.OoPDefl3];
seed3_OoPDefl = [seed3_350.OoPDefl1; seed3_350.OoPDefl2; seed3_350.OoPDefl3];
seed4_OoPDefl = [seed4_350.OoPDefl1; seed4_350.OoPDefl2; seed4_350.OoPDefl3];
seed5_OoPDefl = [seed5_350.OoPDefl1; seed5_350.OoPDefl2; seed5_350.OoPDefl3];
seed6_OoPDefl = [seed6_350.OoPDefl1; seed6_350.OoPDefl2; seed6_350.OoPDefl3];


tip_seeds350 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_350 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 400 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_400.OoPDefl1(1:t_remove/0.008)=0;
seed1_400.OoPDefl2(1:t_remove/0.008) = 0;
seed1_400.OoPDefl3(1:t_remove/0.008)=0;
seed2_400.OoPDefl1(1:t_remove/0.008)=0;
seed2_400.OoPDefl2(1:t_remove/0.008) = 0;
seed2_400.OoPDefl3(1:t_remove/0.008)=0;
seed3_400.OoPDefl1(1:t_remove/0.008)=0;
seed3_400.OoPDefl2(1:t_remove/0.008) = 0;
seed3_400.OoPDefl3(1:t_remove/0.008)=0;
seed4_400.OoPDefl1(1:t_remove/0.008)=0;
seed4_400.OoPDefl2(1:t_remove/0.008) = 0;
seed4_400.OoPDefl3(1:t_remove/0.008)=0;
seed5_400.OoPDefl1(1:t_remove/0.008)=0;
seed5_400.OoPDefl2(1:t_remove/0.008) = 0;
seed5_400.OoPDefl3(1:t_remove/0.008)=0;
seed6_400.OoPDefl1(1:t_remove/0.008)=0;
seed6_400.OoPDefl2(1:t_remove/0.008) = 0;
seed6_400.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_400.OoPDefl1; seed1_400.OoPDefl2; seed1_400.OoPDefl3];
seed2_OoPDefl = [seed2_400.OoPDefl1; seed2_400.OoPDefl2; seed2_400.OoPDefl3];
seed3_OoPDefl = [seed3_400.OoPDefl1; seed3_400.OoPDefl2; seed3_400.OoPDefl3];
seed4_OoPDefl = [seed4_400.OoPDefl1; seed4_400.OoPDefl2; seed4_400.OoPDefl3];
seed5_OoPDefl = [seed5_400.OoPDefl1; seed5_400.OoPDefl2; seed5_400.OoPDefl3];
seed6_OoPDefl = [seed6_400.OoPDefl1; seed6_400.OoPDefl2; seed6_400.OoPDefl3];


tip_seeds400 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_400 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 450 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_450.OoPDefl1(1:t_remove/0.008)=0;
seed1_450.OoPDefl2(1:t_remove/0.008) = 0;
seed1_450.OoPDefl3(1:t_remove/0.008)=0;
seed2_450.OoPDefl1(1:t_remove/0.008)=0;
seed2_450.OoPDefl2(1:t_remove/0.008) = 0;
seed2_450.OoPDefl3(1:t_remove/0.008)=0;
seed3_450.OoPDefl1(1:t_remove/0.008)=0;
seed3_450.OoPDefl2(1:t_remove/0.008) = 0;
seed3_450.OoPDefl3(1:t_remove/0.008)=0;
seed4_450.OoPDefl1(1:t_remove/0.008)=0;
seed4_450.OoPDefl2(1:t_remove/0.008) = 0;
seed4_450.OoPDefl3(1:t_remove/0.008)=0;
seed5_450.OoPDefl1(1:t_remove/0.008)=0;
seed5_450.OoPDefl2(1:t_remove/0.008) = 0;
seed5_450.OoPDefl3(1:t_remove/0.008)=0;
seed6_450.OoPDefl1(1:t_remove/0.008)=0;
seed6_450.OoPDefl2(1:t_remove/0.008) = 0;
seed6_450.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_450.OoPDefl1; seed1_450.OoPDefl2; seed1_450.OoPDefl3];
seed2_OoPDefl = [seed2_450.OoPDefl1; seed2_450.OoPDefl2; seed2_450.OoPDefl3];
seed3_OoPDefl = [seed3_450.OoPDefl1; seed3_450.OoPDefl2; seed3_450.OoPDefl3];
seed4_OoPDefl = [seed4_450.OoPDefl1; seed4_450.OoPDefl2; seed4_450.OoPDefl3];
seed5_OoPDefl = [seed5_450.OoPDefl1; seed5_450.OoPDefl2; seed5_450.OoPDefl3];
seed6_OoPDefl = [seed6_450.OoPDefl1; seed6_450.OoPDefl2; seed6_450.OoPDefl3];


tip_seeds450 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_450 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 500 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_500.OoPDefl1(1:t_remove/0.008)=0;
seed1_500.OoPDefl2(1:t_remove/0.008) = 0;
seed1_500.OoPDefl3(1:t_remove/0.008)=0;
seed2_500.OoPDefl1(1:t_remove/0.008)=0;
seed2_500.OoPDefl2(1:t_remove/0.008) = 0;
seed2_500.OoPDefl3(1:t_remove/0.008)=0;
seed3_500.OoPDefl1(1:t_remove/0.008)=0;
seed3_500.OoPDefl2(1:t_remove/0.008) = 0;
seed3_500.OoPDefl3(1:t_remove/0.008)=0;
seed4_500.OoPDefl1(1:t_remove/0.008)=0;
seed4_500.OoPDefl2(1:t_remove/0.008) = 0;
seed4_500.OoPDefl3(1:t_remove/0.008)=0;
seed5_500.OoPDefl1(1:t_remove/0.008)=0;
seed5_500.OoPDefl2(1:t_remove/0.008) = 0;
seed5_500.OoPDefl3(1:t_remove/0.008)=0;
seed6_500.OoPDefl1(1:t_remove/0.008)=0;
seed6_500.OoPDefl2(1:t_remove/0.008) = 0;
seed6_500.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_500.OoPDefl1; seed1_500.OoPDefl2; seed1_500.OoPDefl3];
seed2_OoPDefl = [seed2_500.OoPDefl1; seed2_500.OoPDefl2; seed2_500.OoPDefl3];
seed3_OoPDefl = [seed3_500.OoPDefl1; seed3_500.OoPDefl2; seed3_500.OoPDefl3];
seed4_OoPDefl = [seed4_500.OoPDefl1; seed4_500.OoPDefl2; seed4_500.OoPDefl3];
seed5_OoPDefl = [seed5_500.OoPDefl1; seed5_500.OoPDefl2; seed5_500.OoPDefl3];
seed6_OoPDefl = [seed6_500.OoPDefl1; seed6_500.OoPDefl2; seed6_500.OoPDefl3];


tip_seeds500 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_500 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 550 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_550.OoPDefl1(1:t_remove/0.008)=0;
seed1_550.OoPDefl2(1:t_remove/0.008) = 0;
seed1_550.OoPDefl3(1:t_remove/0.008)=0;
seed2_550.OoPDefl1(1:t_remove/0.008)=0;
seed2_550.OoPDefl2(1:t_remove/0.008) = 0;
seed2_550.OoPDefl3(1:t_remove/0.008)=0;
seed3_550.OoPDefl1(1:t_remove/0.008)=0;
seed3_550.OoPDefl2(1:t_remove/0.008) = 0;
seed3_550.OoPDefl3(1:t_remove/0.008)=0;
seed4_550.OoPDefl1(1:t_remove/0.008)=0;
seed4_550.OoPDefl2(1:t_remove/0.008) = 0;
seed4_550.OoPDefl3(1:t_remove/0.008)=0;
seed5_550.OoPDefl1(1:t_remove/0.008)=0;
seed5_550.OoPDefl2(1:t_remove/0.008) = 0;
seed5_550.OoPDefl3(1:t_remove/0.008)=0;
seed6_550.OoPDefl1(1:t_remove/0.008)=0;
seed6_550.OoPDefl2(1:t_remove/0.008) = 0;
seed6_550.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_550.OoPDefl1; seed1_550.OoPDefl2; seed1_550.OoPDefl3];
seed2_OoPDefl = [seed2_550.OoPDefl1; seed2_550.OoPDefl2; seed2_550.OoPDefl3];
seed3_OoPDefl = [seed3_550.OoPDefl1; seed3_550.OoPDefl2; seed3_550.OoPDefl3];
seed4_OoPDefl = [seed4_550.OoPDefl1; seed4_550.OoPDefl2; seed4_550.OoPDefl3];
seed5_OoPDefl = [seed5_550.OoPDefl1; seed5_550.OoPDefl2; seed5_550.OoPDefl3];
seed6_OoPDefl = [seed6_550.OoPDefl1; seed6_550.OoPDefl2; seed6_550.OoPDefl3];


tip_seeds550 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_550 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 600 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

seed1_600.OoPDefl1(1:t_remove/0.008)=0;
seed1_600.OoPDefl2(1:t_remove/0.008) = 0;
seed1_600.OoPDefl3(1:t_remove/0.008)=0;
seed2_600.OoPDefl1(1:t_remove/0.008)=0;
seed2_600.OoPDefl2(1:t_remove/0.008) = 0;
seed2_600.OoPDefl3(1:t_remove/0.008)=0;
seed3_600.OoPDefl1(1:t_remove/0.008)=0;
seed3_600.OoPDefl2(1:t_remove/0.008) = 0;
seed3_600.OoPDefl3(1:t_remove/0.008)=0;
seed4_600.OoPDefl1(1:t_remove/0.008)=0;
seed4_600.OoPDefl2(1:t_remove/0.008) = 0;
seed4_600.OoPDefl3(1:t_remove/0.008)=0;
seed5_600.OoPDefl1(1:t_remove/0.008)=0;
seed5_600.OoPDefl2(1:t_remove/0.008) = 0;
seed5_600.OoPDefl3(1:t_remove/0.008)=0;
seed6_600.OoPDefl1(1:t_remove/0.008)=0;
seed6_600.OoPDefl2(1:t_remove/0.008) = 0;
seed6_600.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_600.OoPDefl1; seed1_600.OoPDefl2; seed1_600.OoPDefl3];
seed2_OoPDefl = [seed2_600.OoPDefl1; seed2_600.OoPDefl2; seed2_600.OoPDefl3];
seed3_OoPDefl = [seed3_600.OoPDefl1; seed3_600.OoPDefl2; seed3_600.OoPDefl3];
seed4_OoPDefl = [seed4_600.OoPDefl1; seed4_600.OoPDefl2; seed4_600.OoPDefl3];
seed5_OoPDefl = [seed5_600.OoPDefl1; seed5_600.OoPDefl2; seed5_600.OoPDefl3];
seed6_OoPDefl = [seed6_600.OoPDefl1; seed6_600.OoPDefl2; seed6_600.OoPDefl3];


tip_seeds600 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_600 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 660 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


seed1_660.OoPDefl1(1:t_remove/0.008)=0;
seed1_660.OoPDefl2(1:t_remove/0.008) = 0;
seed1_660.OoPDefl3(1:t_remove/0.008)=0;
seed2_660.OoPDefl1(1:t_remove/0.008)=0;
seed2_660.OoPDefl2(1:t_remove/0.008) = 0;
seed2_660.OoPDefl3(1:t_remove/0.008)=0;
seed3_660.OoPDefl1(1:t_remove/0.008)=0;
seed3_660.OoPDefl2(1:t_remove/0.008) = 0;
seed3_660.OoPDefl3(1:t_remove/0.008)=0;
seed4_660.OoPDefl1(1:t_remove/0.008)=0;
seed4_660.OoPDefl2(1:t_remove/0.008) = 0;
seed4_660.OoPDefl3(1:t_remove/0.008)=0;
seed5_660.OoPDefl1(1:t_remove/0.008)=0;
seed5_660.OoPDefl2(1:t_remove/0.008) = 0;
seed5_660.OoPDefl3(1:t_remove/0.008)=0;
seed6_660.OoPDefl1(1:t_remove/0.008)=0;
seed6_660.OoPDefl2(1:t_remove/0.008) = 0;
seed6_660.OoPDefl3(1:t_remove/0.008)=0;

seed1_OoPDefl = [seed1_660.OoPDefl1; seed1_660.OoPDefl2; seed1_660.OoPDefl3];
seed2_OoPDefl = [seed2_660.OoPDefl1; seed2_660.OoPDefl2; seed2_660.OoPDefl3];
seed3_OoPDefl = [seed3_660.OoPDefl1; seed3_660.OoPDefl2; seed3_660.OoPDefl3];
seed4_OoPDefl = [seed4_660.OoPDefl1; seed4_660.OoPDefl2; seed4_660.OoPDefl3];
seed5_OoPDefl = [seed5_660.OoPDefl1; seed5_660.OoPDefl2; seed5_660.OoPDefl3];
seed6_OoPDefl = [seed6_660.OoPDefl1; seed6_660.OoPDefl2; seed6_660.OoPDefl3];


tip_seeds660 = [max(seed1_OoPDefl), max(seed2_OoPDefl), max(seed3_OoPDefl), ...
    max(seed4_OoPDefl), max(seed5_OoPDefl), max(seed6_OoPDefl)];

tip_defl_660 = (max(seed1_OoPDefl) + max(seed2_OoPDefl) + max(seed3_OoPDefl)...
    + max(seed4_OoPDefl)+ max(seed5_OoPDefl)+ max(seed6_OoPDefl))/6;


tip_defl =[ tip_defl_70, tip_defl_100, tip_defl_150,tip_defl_200,...
    tip_defl_250, tip_defl_300, tip_defl_350, tip_defl_400, tip_defl_450,...
    tip_defl_500,tip_defl_550, tip_defl_600, tip_defl_660]; 

%% Compare root Moments 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 70 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_70.RootMFlp1(1:t_remove/0.008)=0;
seed1_70.RootMFlp2(1:t_remove/0.008)=0;
seed1_70.RootMFlp3(1:t_remove/0.008)=0;
seed2_70.RootMFlp1(1:t_remove/0.008)=0;
seed2_70.RootMFlp2(1:t_remove/0.008)=0;
seed2_70.RootMFlp3(1:t_remove/0.008)=0;
seed3_70.RootMFlp1(1:t_remove/0.008)=0;
seed3_70.RootMFlp2(1:t_remove/0.008)=0;
seed3_70.RootMFlp3(1:t_remove/0.008)=0;
seed4_70.RootMFlp1(1:t_remove/0.008)=0;
seed4_70.RootMFlp2(1:t_remove/0.008)=0;
seed4_70.RootMFlp3(1:t_remove/0.008)=0;
seed5_70.RootMFlp1(1:t_remove/0.008)=0;
seed5_70.RootMFlp2(1:t_remove/0.008)=0;
seed5_70.RootMFlp3(1:t_remove/0.008)=0;
seed6_70.RootMFlp1(1:t_remove/0.008)=0;
seed6_70.RootMFlp2(1:t_remove/0.008)=0;
seed6_70.RootMFlp3(1:t_remove/0.008)=0;

seed1_70.RootMEdg1(1:t_remove/0.008)=0;
seed1_70.RootMEdg2(1:t_remove/0.008)=0;
seed1_70.RootMEdg3(1:t_remove/0.008)=0;
seed2_70.RootMEdg1(1:t_remove/0.008)=0;
seed2_70.RootMEdg2(1:t_remove/0.008)=0;
seed2_70.RootMEdg3(1:t_remove/0.008)=0;
seed3_70.RootMEdg1(1:t_remove/0.008)=0;
seed3_70.RootMEdg2(1:t_remove/0.008)=0;
seed3_70.RootMEdg3(1:t_remove/0.008)=0;
seed4_70.RootMEdg1(1:t_remove/0.008)=0;
seed4_70.RootMEdg2(1:t_remove/0.008)=0;
seed4_70.RootMEdg3(1:t_remove/0.008)=0;
seed5_70.RootMEdg1(1:t_remove/0.008)=0;
seed5_70.RootMEdg2(1:t_remove/0.008)=0;
seed5_70.RootMEdg3(1:t_remove/0.008)=0;
seed6_70.RootMEdg1(1:t_remove/0.008)=0;
seed6_70.RootMEdg2(1:t_remove/0.008)=0;
seed6_70.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_70.RootMFlp1; seed1_70.RootMFlp2; seed1_70.RootMFlp3];
seed2_flpmoment = [seed2_70.RootMFlp1; seed2_70.RootMFlp2; seed2_70.RootMFlp3];
seed3_flpmoment = [seed3_70.RootMFlp1; seed3_70.RootMFlp2; seed3_70.RootMFlp3];
seed4_flpmoment = [seed4_70.RootMFlp1; seed4_70.RootMFlp2; seed4_70.RootMFlp3];
seed5_flpmoment = [seed5_70.RootMFlp1; seed5_70.RootMFlp2; seed5_70.RootMFlp3];
seed6_flpmoment = [seed6_70.RootMFlp1; seed6_70.RootMFlp2; seed6_70.RootMFlp3];

seed1_edgemoment = [seed1_70.RootMEdg1; seed1_70.RootMEdg2; seed1_70.RootMEdg3];
seed2_edgemoment = [seed2_70.RootMEdg1; seed2_70.RootMEdg2; seed2_70.RootMEdg3];
seed3_edgemoment = [seed3_70.RootMEdg1; seed3_70.RootMEdg2; seed3_70.RootMEdg3];
seed4_edgemoment = [seed4_70.RootMEdg1; seed4_70.RootMEdg2; seed4_70.RootMEdg3];
seed5_edgemoment = [seed5_70.RootMEdg1; seed5_70.RootMEdg2; seed5_70.RootMEdg3];
seed6_edgemoment = [seed6_70.RootMEdg1; seed6_70.RootMEdg2; seed6_70.RootMEdg3];

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
seed1_100.RootMFlp1(1:t_remove/0.008)=0;
seed1_100.RootMFlp2(1:t_remove/0.008)=0;
seed1_100.RootMFlp3(1:t_remove/0.008)=0;
seed2_100.RootMFlp1(1:t_remove/0.008)=0;
seed2_100.RootMFlp2(1:t_remove/0.008)=0;
seed2_100.RootMFlp3(1:t_remove/0.008)=0;
seed3_100.RootMFlp1(1:t_remove/0.008)=0;
seed3_100.RootMFlp2(1:t_remove/0.008)=0;
seed3_100.RootMFlp3(1:t_remove/0.008)=0;
seed4_100.RootMFlp1(1:t_remove/0.008)=0;
seed4_100.RootMFlp2(1:t_remove/0.008)=0;
seed4_100.RootMFlp3(1:t_remove/0.008)=0;
seed5_100.RootMFlp1(1:t_remove/0.008)=0;
seed5_100.RootMFlp2(1:t_remove/0.008)=0;
seed5_100.RootMFlp3(1:t_remove/0.008)=0;
seed6_100.RootMFlp1(1:t_remove/0.008)=0;
seed6_100.RootMFlp2(1:t_remove/0.008)=0;
seed6_100.RootMFlp3(1:t_remove/0.008)=0;

seed1_100.RootMEdg1(1:t_remove/0.008)=0;
seed1_100.RootMEdg2(1:t_remove/0.008)=0;
seed1_100.RootMEdg3(1:t_remove/0.008)=0;
seed2_100.RootMEdg1(1:t_remove/0.008)=0;
seed2_100.RootMEdg2(1:t_remove/0.008)=0;
seed2_100.RootMEdg3(1:t_remove/0.008)=0;
seed3_100.RootMEdg1(1:t_remove/0.008)=0;
seed3_100.RootMEdg2(1:t_remove/0.008)=0;
seed3_100.RootMEdg3(1:t_remove/0.008)=0;
seed4_100.RootMEdg1(1:t_remove/0.008)=0;
seed4_100.RootMEdg2(1:t_remove/0.008)=0;
seed4_100.RootMEdg3(1:t_remove/0.008)=0;
seed5_100.RootMEdg1(1:t_remove/0.008)=0;
seed5_100.RootMEdg2(1:t_remove/0.008)=0;
seed5_100.RootMEdg3(1:t_remove/0.008)=0;
seed6_100.RootMEdg1(1:t_remove/0.008)=0;
seed6_100.RootMEdg2(1:t_remove/0.008)=0;
seed6_100.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_100.RootMFlp1; seed1_100.RootMFlp2; seed1_100.RootMFlp3];
seed2_flpmoment = [seed2_100.RootMFlp1; seed2_100.RootMFlp2; seed2_100.RootMFlp3];
seed3_flpmoment = [seed3_100.RootMFlp1; seed3_100.RootMFlp2; seed3_100.RootMFlp3];
seed4_flpmoment = [seed4_100.RootMFlp1; seed4_100.RootMFlp2; seed4_100.RootMFlp3];
seed5_flpmoment = [seed5_100.RootMFlp1; seed5_100.RootMFlp2; seed5_100.RootMFlp3];
seed6_flpmoment = [seed6_100.RootMFlp1; seed6_100.RootMFlp2; seed6_100.RootMFlp3];

seed1_edgemoment = [seed1_100.RootMEdg1; seed1_100.RootMEdg2; seed1_100.RootMEdg3];
seed2_edgemoment = [seed2_100.RootMEdg1; seed2_100.RootMEdg2; seed2_100.RootMEdg3];
seed3_edgemoment = [seed3_100.RootMEdg1; seed3_100.RootMEdg2; seed3_100.RootMEdg3];
seed4_edgemoment = [seed4_100.RootMEdg1; seed4_100.RootMEdg2; seed4_100.RootMEdg3];
seed5_edgemoment = [seed5_100.RootMEdg1; seed5_100.RootMEdg2; seed5_100.RootMEdg3];
seed6_edgemoment = [seed6_100.RootMEdg1; seed6_100.RootMEdg2; seed6_100.RootMEdg3];

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
seed1_150.RootMFlp1(1:t_remove/0.008)=0;
seed1_150.RootMFlp2(1:t_remove/0.008)=0;
seed1_150.RootMFlp3(1:t_remove/0.008)=0;
seed2_150.RootMFlp1(1:t_remove/0.008)=0;
seed2_150.RootMFlp2(1:t_remove/0.008)=0;
seed2_150.RootMFlp3(1:t_remove/0.008)=0;
seed3_150.RootMFlp1(1:t_remove/0.008)=0;
seed3_150.RootMFlp2(1:t_remove/0.008)=0;
seed3_150.RootMFlp3(1:t_remove/0.008)=0;
seed4_150.RootMFlp1(1:t_remove/0.008)=0;
seed4_150.RootMFlp2(1:t_remove/0.008)=0;
seed4_150.RootMFlp3(1:t_remove/0.008)=0;
seed5_150.RootMFlp1(1:t_remove/0.008)=0;
seed5_150.RootMFlp2(1:t_remove/0.008)=0;
seed5_150.RootMFlp3(1:t_remove/0.008)=0;
seed6_150.RootMFlp1(1:t_remove/0.008)=0;
seed6_150.RootMFlp2(1:t_remove/0.008)=0;
seed6_150.RootMFlp3(1:t_remove/0.008)=0;

seed1_150.RootMEdg1(1:t_remove/0.008)=0;
seed1_150.RootMEdg2(1:t_remove/0.008)=0;
seed1_150.RootMEdg3(1:t_remove/0.008)=0;
seed2_150.RootMEdg1(1:t_remove/0.008)=0;
seed2_150.RootMEdg2(1:t_remove/0.008)=0;
seed2_150.RootMEdg3(1:t_remove/0.008)=0;
seed3_150.RootMEdg1(1:t_remove/0.008)=0;
seed3_150.RootMEdg2(1:t_remove/0.008)=0;
seed3_150.RootMEdg3(1:t_remove/0.008)=0;
seed4_150.RootMEdg1(1:t_remove/0.008)=0;
seed4_150.RootMEdg2(1:t_remove/0.008)=0;
seed4_150.RootMEdg3(1:t_remove/0.008)=0;
seed5_150.RootMEdg1(1:t_remove/0.008)=0;
seed5_150.RootMEdg2(1:t_remove/0.008)=0;
seed5_150.RootMEdg3(1:t_remove/0.008)=0;
seed6_150.RootMEdg1(1:t_remove/0.008)=0;
seed6_150.RootMEdg2(1:t_remove/0.008)=0;
seed6_150.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_150.RootMFlp1; seed1_150.RootMFlp2; seed1_150.RootMFlp3];
seed2_flpmoment = [seed2_150.RootMFlp1; seed2_150.RootMFlp2; seed2_150.RootMFlp3];
seed3_flpmoment = [seed3_150.RootMFlp1; seed3_150.RootMFlp2; seed3_150.RootMFlp3];
seed4_flpmoment = [seed4_150.RootMFlp1; seed4_150.RootMFlp2; seed4_150.RootMFlp3];
seed5_flpmoment = [seed5_150.RootMFlp1; seed5_150.RootMFlp2; seed5_150.RootMFlp3];
seed6_flpmoment = [seed6_150.RootMFlp1; seed6_150.RootMFlp2; seed6_150.RootMFlp3];

seed1_edgemoment = [seed1_150.RootMEdg1; seed1_150.RootMEdg2; seed1_150.RootMEdg3];
seed2_edgemoment = [seed2_150.RootMEdg1; seed2_150.RootMEdg2; seed2_150.RootMEdg3];
seed3_edgemoment = [seed3_150.RootMEdg1; seed3_150.RootMEdg2; seed3_150.RootMEdg3];
seed4_edgemoment = [seed4_150.RootMEdg1; seed4_150.RootMEdg2; seed4_150.RootMEdg3];
seed5_edgemoment = [seed5_150.RootMEdg1; seed5_150.RootMEdg2; seed5_150.RootMEdg3];
seed6_edgemoment = [seed6_150.RootMEdg1; seed6_150.RootMEdg2; seed6_150.RootMEdg3];

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
seed1_200.RootMFlp1(1:20/0.008)=0;
seed1_200.RootMFlp2(1:20/0.008)=0;
seed1_200.RootMFlp3(1:20/0.008)=0;
seed2_200.RootMFlp1(1:20/0.008)=0;
seed2_200.RootMFlp2(1:20/0.008)=0;
seed2_200.RootMFlp3(1:20/0.008)=0;
seed3_200.RootMFlp1(1:20/0.008)=0;
seed3_200.RootMFlp2(1:20/0.008)=0;
seed3_200.RootMFlp3(1:20/0.008)=0;
seed4_200.RootMFlp1(1:20/0.008)=0;
seed4_200.RootMFlp2(1:20/0.008)=0;
seed4_200.RootMFlp3(1:20/0.008)=0;
seed5_200.RootMFlp1(1:20/0.008)=0;
seed5_200.RootMFlp2(1:20/0.008)=0;
seed5_200.RootMFlp3(1:20/0.008)=0;
seed6_200.RootMFlp1(1:20/0.008)=0;
seed6_200.RootMFlp2(1:20/0.008)=0;
seed6_200.RootMFlp3(1:20/0.008)=0;

seed1_200.RootMEdg1(1:20/0.008)=0;
seed1_200.RootMEdg2(1:20/0.008)=0;
seed1_200.RootMEdg3(1:20/0.008)=0;
seed2_200.RootMEdg1(1:20/0.008)=0;
seed2_200.RootMEdg2(1:20/0.008)=0;
seed2_200.RootMEdg3(1:20/0.008)=0;
seed3_200.RootMEdg1(1:20/0.008)=0;
seed3_200.RootMEdg2(1:20/0.008)=0;
seed3_200.RootMEdg3(1:20/0.008)=0;
seed4_200.RootMEdg1(1:20/0.008)=0;
seed4_200.RootMEdg2(1:20/0.008)=0;
seed4_200.RootMEdg3(1:20/0.008)=0;
seed5_200.RootMEdg1(1:20/0.008)=0;
seed5_200.RootMEdg2(1:20/0.008)=0;
seed5_200.RootMEdg3(1:20/0.008)=0;
seed6_200.RootMEdg1(1:20/0.008)=0;
seed6_200.RootMEdg2(1:20/0.008)=0;
seed6_200.RootMEdg3(1:20/0.008)=0;

seed1_flpmoment = [seed1_200.RootMFlp1; seed1_200.RootMFlp2; seed1_200.RootMFlp3];
seed2_flpmoment = [seed2_200.RootMFlp1; seed2_200.RootMFlp2; seed2_200.RootMFlp3];
seed3_flpmoment = [seed3_200.RootMFlp1; seed3_200.RootMFlp2; seed3_200.RootMFlp3];
seed4_flpmoment = [seed4_200.RootMFlp1; seed4_200.RootMFlp2; seed4_200.RootMFlp3];
seed5_flpmoment = [seed5_200.RootMFlp1; seed5_200.RootMFlp2; seed5_200.RootMFlp3];
seed6_flpmoment = [seed6_200.RootMFlp1; seed6_200.RootMFlp2; seed6_200.RootMFlp3];

seed1_edgemoment = [seed1_200.RootMEdg1; seed1_200.RootMEdg2; seed1_200.RootMEdg3];
seed2_edgemoment = [seed2_200.RootMEdg1; seed2_200.RootMEdg2; seed2_200.RootMEdg3];
seed3_edgemoment = [seed3_200.RootMEdg1; seed3_200.RootMEdg2; seed3_200.RootMEdg3];
seed4_edgemoment = [seed4_200.RootMEdg1; seed4_200.RootMEdg2; seed4_200.RootMEdg3];
seed5_edgemoment = [seed5_200.RootMEdg1; seed5_200.RootMEdg2; seed5_200.RootMEdg3];
seed6_edgemoment = [seed6_200.RootMEdg1; seed6_200.RootMEdg2; seed6_200.RootMEdg3];

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
seed1_250.RootMFlp1(1:t_remove/0.008)=0;
seed1_250.RootMFlp2(1:t_remove/0.008)=0;
seed1_250.RootMFlp3(1:t_remove/0.008)=0;
seed2_250.RootMFlp1(1:t_remove/0.008)=0;
seed2_250.RootMFlp2(1:t_remove/0.008)=0;
seed2_250.RootMFlp3(1:t_remove/0.008)=0;
seed3_250.RootMFlp1(1:t_remove/0.008)=0;
seed3_250.RootMFlp2(1:t_remove/0.008)=0;
seed3_250.RootMFlp3(1:t_remove/0.008)=0;
seed4_250.RootMFlp1(1:t_remove/0.008)=0;
seed4_250.RootMFlp2(1:t_remove/0.008)=0;
seed4_250.RootMFlp3(1:t_remove/0.008)=0;
seed5_250.RootMFlp1(1:t_remove/0.008)=0;
seed5_250.RootMFlp2(1:t_remove/0.008)=0;
seed5_250.RootMFlp3(1:t_remove/0.008)=0;
seed6_250.RootMFlp1(1:t_remove/0.008)=0;
seed6_250.RootMFlp2(1:t_remove/0.008)=0;
seed6_250.RootMFlp3(1:t_remove/0.008)=0;

seed1_250.RootMEdg1(1:t_remove/0.008)=0;
seed1_250.RootMEdg2(1:t_remove/0.008)=0;
seed1_250.RootMEdg3(1:t_remove/0.008)=0;
seed2_250.RootMEdg1(1:t_remove/0.008)=0;
seed2_250.RootMEdg2(1:t_remove/0.008)=0;
seed2_250.RootMEdg3(1:t_remove/0.008)=0;
seed3_250.RootMEdg1(1:t_remove/0.008)=0;
seed3_250.RootMEdg2(1:t_remove/0.008)=0;
seed3_250.RootMEdg3(1:t_remove/0.008)=0;
seed4_250.RootMEdg1(1:t_remove/0.008)=0;
seed4_250.RootMEdg2(1:t_remove/0.008)=0;
seed4_250.RootMEdg3(1:t_remove/0.008)=0;
seed5_250.RootMEdg1(1:t_remove/0.008)=0;
seed5_250.RootMEdg2(1:t_remove/0.008)=0;
seed5_250.RootMEdg3(1:t_remove/0.008)=0;
seed6_250.RootMEdg1(1:t_remove/0.008)=0;
seed6_250.RootMEdg2(1:t_remove/0.008)=0;
seed6_250.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_250.RootMFlp1; seed1_250.RootMFlp2; seed1_250.RootMFlp3];
seed2_flpmoment = [seed2_250.RootMFlp1; seed2_250.RootMFlp2; seed2_250.RootMFlp3];
seed3_flpmoment = [seed3_250.RootMFlp1; seed3_250.RootMFlp2; seed3_250.RootMFlp3];
seed4_flpmoment = [seed4_250.RootMFlp1; seed4_250.RootMFlp2; seed4_250.RootMFlp3];
seed5_flpmoment = [seed5_250.RootMFlp1; seed5_250.RootMFlp2; seed5_250.RootMFlp3];
seed6_flpmoment = [seed6_250.RootMFlp1; seed6_250.RootMFlp2; seed6_250.RootMFlp3];

seed1_edgemoment = [seed1_250.RootMEdg1; seed1_250.RootMEdg2; seed1_250.RootMEdg3];
seed2_edgemoment = [seed2_250.RootMEdg1; seed2_250.RootMEdg2; seed2_250.RootMEdg3];
seed3_edgemoment = [seed3_250.RootMEdg1; seed3_250.RootMEdg2; seed3_250.RootMEdg3];
seed4_edgemoment = [seed4_250.RootMEdg1; seed4_250.RootMEdg2; seed4_250.RootMEdg3];
seed5_edgemoment = [seed5_250.RootMEdg1; seed5_250.RootMEdg2; seed5_250.RootMEdg3];
seed6_edgemoment = [seed6_250.RootMEdg1; seed6_250.RootMEdg2; seed6_250.RootMEdg3];

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
seed1_300.RootMFlp1(1:t_remove/0.008)=0;
seed1_300.RootMFlp2(1:t_remove/0.008)=0;
seed1_300.RootMFlp3(1:t_remove/0.008)=0;
seed2_300.RootMFlp1(1:t_remove/0.008)=0;
seed2_300.RootMFlp2(1:t_remove/0.008)=0;
seed2_300.RootMFlp3(1:t_remove/0.008)=0;
seed3_300.RootMFlp1(1:t_remove/0.008)=0;
seed3_300.RootMFlp2(1:t_remove/0.008)=0;
seed3_300.RootMFlp3(1:t_remove/0.008)=0;
seed4_300.RootMFlp1(1:t_remove/0.008)=0;
seed4_300.RootMFlp2(1:t_remove/0.008)=0;
seed4_300.RootMFlp3(1:t_remove/0.008)=0;
seed5_300.RootMFlp1(1:t_remove/0.008)=0;
seed5_300.RootMFlp2(1:t_remove/0.008)=0;
seed5_300.RootMFlp3(1:t_remove/0.008)=0;
seed6_300.RootMFlp1(1:t_remove/0.008)=0;
seed6_300.RootMFlp2(1:t_remove/0.008)=0;
seed6_300.RootMFlp3(1:t_remove/0.008)=0;

seed1_300.RootMEdg1(1:t_remove/0.008)=0;
seed1_300.RootMEdg2(1:t_remove/0.008)=0;
seed1_300.RootMEdg3(1:t_remove/0.008)=0;
seed2_300.RootMEdg1(1:t_remove/0.008)=0;
seed2_300.RootMEdg2(1:t_remove/0.008)=0;
seed2_300.RootMEdg3(1:t_remove/0.008)=0;
seed3_300.RootMEdg1(1:t_remove/0.008)=0;
seed3_300.RootMEdg2(1:t_remove/0.008)=0;
seed3_300.RootMEdg3(1:t_remove/0.008)=0;
seed4_300.RootMEdg1(1:t_remove/0.008)=0;
seed4_300.RootMEdg2(1:t_remove/0.008)=0;
seed4_300.RootMEdg3(1:t_remove/0.008)=0;
seed5_300.RootMEdg1(1:t_remove/0.008)=0;
seed5_300.RootMEdg2(1:t_remove/0.008)=0;
seed5_300.RootMEdg3(1:t_remove/0.008)=0;
seed6_300.RootMEdg1(1:t_remove/0.008)=0;
seed6_300.RootMEdg2(1:t_remove/0.008)=0;
seed6_300.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_300.RootMFlp1; seed1_300.RootMFlp2; seed1_300.RootMFlp3];
seed2_flpmoment = [seed2_300.RootMFlp1; seed2_300.RootMFlp2; seed2_300.RootMFlp3];
seed3_flpmoment = [seed3_300.RootMFlp1; seed3_300.RootMFlp2; seed3_300.RootMFlp3];
seed4_flpmoment = [seed4_300.RootMFlp1; seed4_300.RootMFlp2; seed4_300.RootMFlp3];
seed5_flpmoment = [seed5_300.RootMFlp1; seed5_300.RootMFlp2; seed5_300.RootMFlp3];
seed6_flpmoment = [seed6_300.RootMFlp1; seed6_300.RootMFlp2; seed6_300.RootMFlp3];

seed1_edgemoment = [seed1_300.RootMEdg1; seed1_300.RootMEdg2; seed1_300.RootMEdg3];
seed2_edgemoment = [seed2_300.RootMEdg1; seed2_300.RootMEdg2; seed2_300.RootMEdg3];
seed3_edgemoment = [seed3_300.RootMEdg1; seed3_300.RootMEdg2; seed3_300.RootMEdg3];
seed4_edgemoment = [seed4_300.RootMEdg1; seed4_300.RootMEdg2; seed4_300.RootMEdg3];
seed5_edgemoment = [seed5_300.RootMEdg1; seed5_300.RootMEdg2; seed5_300.RootMEdg3];
seed6_edgemoment = [seed6_300.RootMEdg1; seed6_300.RootMEdg2; seed6_300.RootMEdg3];

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
seed1_350.RootMFlp1(1:t_remove/0.008)=0;
seed1_350.RootMFlp2(1:t_remove/0.008)=0;
seed1_350.RootMFlp3(1:t_remove/0.008)=0;
seed2_350.RootMFlp1(1:t_remove/0.008)=0;
seed2_350.RootMFlp2(1:t_remove/0.008)=0;
seed2_350.RootMFlp3(1:t_remove/0.008)=0;
seed3_350.RootMFlp1(1:t_remove/0.008)=0;
seed3_350.RootMFlp2(1:t_remove/0.008)=0;
seed3_350.RootMFlp3(1:t_remove/0.008)=0;
seed4_350.RootMFlp1(1:t_remove/0.008)=0;
seed4_350.RootMFlp2(1:t_remove/0.008)=0;
seed4_350.RootMFlp3(1:t_remove/0.008)=0;
seed5_350.RootMFlp1(1:t_remove/0.008)=0;
seed5_350.RootMFlp2(1:t_remove/0.008)=0;
seed5_350.RootMFlp3(1:t_remove/0.008)=0;
seed6_350.RootMFlp1(1:t_remove/0.008)=0;
seed6_350.RootMFlp2(1:t_remove/0.008)=0;
seed6_350.RootMFlp3(1:t_remove/0.008)=0;

seed1_350.RootMEdg1(1:t_remove/0.008)=0;
seed1_350.RootMEdg2(1:t_remove/0.008)=0;
seed1_350.RootMEdg3(1:t_remove/0.008)=0;
seed2_350.RootMEdg1(1:t_remove/0.008)=0;
seed2_350.RootMEdg2(1:t_remove/0.008)=0;
seed2_350.RootMEdg3(1:t_remove/0.008)=0;
seed3_350.RootMEdg1(1:t_remove/0.008)=0;
seed3_350.RootMEdg2(1:t_remove/0.008)=0;
seed3_350.RootMEdg3(1:t_remove/0.008)=0;
seed4_350.RootMEdg1(1:t_remove/0.008)=0;
seed4_350.RootMEdg2(1:t_remove/0.008)=0;
seed4_350.RootMEdg3(1:t_remove/0.008)=0;
seed5_350.RootMEdg1(1:t_remove/0.008)=0;
seed5_350.RootMEdg2(1:t_remove/0.008)=0;
seed5_350.RootMEdg3(1:t_remove/0.008)=0;
seed6_350.RootMEdg1(1:t_remove/0.008)=0;
seed6_350.RootMEdg2(1:t_remove/0.008)=0;
seed6_350.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_350.RootMFlp1; seed1_350.RootMFlp2; seed1_350.RootMFlp3];
seed2_flpmoment = [seed2_350.RootMFlp1; seed2_350.RootMFlp2; seed2_350.RootMFlp3];
seed3_flpmoment = [seed3_350.RootMFlp1; seed3_350.RootMFlp2; seed3_350.RootMFlp3];
seed4_flpmoment = [seed4_350.RootMFlp1; seed4_350.RootMFlp2; seed4_350.RootMFlp3];
seed5_flpmoment = [seed5_350.RootMFlp1; seed5_350.RootMFlp2; seed5_350.RootMFlp3];
seed6_flpmoment = [seed6_350.RootMFlp1; seed6_350.RootMFlp2; seed6_350.RootMFlp3];

seed1_edgemoment = [seed1_350.RootMEdg1; seed1_350.RootMEdg2; seed1_350.RootMEdg3];
seed2_edgemoment = [seed2_350.RootMEdg1; seed2_350.RootMEdg2; seed2_350.RootMEdg3];
seed3_edgemoment = [seed3_350.RootMEdg1; seed3_350.RootMEdg2; seed3_350.RootMEdg3];
seed4_edgemoment = [seed4_350.RootMEdg1; seed4_350.RootMEdg2; seed4_350.RootMEdg3];
seed5_edgemoment = [seed5_350.RootMEdg1; seed5_350.RootMEdg2; seed5_350.RootMEdg3];
seed6_edgemoment = [seed6_350.RootMEdg1; seed6_350.RootMEdg2; seed6_350.RootMEdg3];

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
seed1_400.RootMFlp1(1:t_remove/0.008)=0;
seed1_400.RootMFlp2(1:t_remove/0.008)=0;
seed1_400.RootMFlp3(1:t_remove/0.008)=0;
seed2_400.RootMFlp1(1:t_remove/0.008)=0;
seed2_400.RootMFlp2(1:t_remove/0.008)=0;
seed2_400.RootMFlp3(1:t_remove/0.008)=0;
seed3_400.RootMFlp1(1:t_remove/0.008)=0;
seed3_400.RootMFlp2(1:t_remove/0.008)=0;
seed3_400.RootMFlp3(1:t_remove/0.008)=0;
seed4_400.RootMFlp1(1:t_remove/0.008)=0;
seed4_400.RootMFlp2(1:t_remove/0.008)=0;
seed4_400.RootMFlp3(1:t_remove/0.008)=0;
seed5_400.RootMFlp1(1:t_remove/0.008)=0;
seed5_400.RootMFlp2(1:t_remove/0.008)=0;
seed5_400.RootMFlp3(1:t_remove/0.008)=0;
seed6_400.RootMFlp1(1:t_remove/0.008)=0;
seed6_400.RootMFlp2(1:t_remove/0.008)=0;
seed6_400.RootMFlp3(1:t_remove/0.008)=0;

seed1_400.RootMEdg1(1:t_remove/0.008)=0;
seed1_400.RootMEdg2(1:t_remove/0.008)=0;
seed1_400.RootMEdg3(1:t_remove/0.008)=0;
seed2_400.RootMEdg1(1:t_remove/0.008)=0;
seed2_400.RootMEdg2(1:t_remove/0.008)=0;
seed2_400.RootMEdg3(1:t_remove/0.008)=0;
seed3_400.RootMEdg1(1:t_remove/0.008)=0;
seed3_400.RootMEdg2(1:t_remove/0.008)=0;
seed3_400.RootMEdg3(1:t_remove/0.008)=0;
seed4_400.RootMEdg1(1:t_remove/0.008)=0;
seed4_400.RootMEdg2(1:t_remove/0.008)=0;
seed4_400.RootMEdg3(1:t_remove/0.008)=0;
seed5_400.RootMEdg1(1:t_remove/0.008)=0;
seed5_400.RootMEdg2(1:t_remove/0.008)=0;
seed5_400.RootMEdg3(1:t_remove/0.008)=0;
seed6_400.RootMEdg1(1:t_remove/0.008)=0;
seed6_400.RootMEdg2(1:t_remove/0.008)=0;
seed6_400.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_400.RootMFlp1; seed1_400.RootMFlp2; seed1_400.RootMFlp3];
seed2_flpmoment = [seed2_400.RootMFlp1; seed2_400.RootMFlp2; seed2_400.RootMFlp3];
seed3_flpmoment = [seed3_400.RootMFlp1; seed3_400.RootMFlp2; seed3_400.RootMFlp3];
seed4_flpmoment = [seed4_400.RootMFlp1; seed4_400.RootMFlp2; seed4_400.RootMFlp3];
seed5_flpmoment = [seed5_400.RootMFlp1; seed5_400.RootMFlp2; seed5_400.RootMFlp3];
seed6_flpmoment = [seed6_400.RootMFlp1; seed6_400.RootMFlp2; seed6_400.RootMFlp3];

seed1_edgemoment = [seed1_400.RootMEdg1; seed1_400.RootMEdg2; seed1_400.RootMEdg3];
seed2_edgemoment = [seed2_400.RootMEdg1; seed2_400.RootMEdg2; seed2_400.RootMEdg3];
seed3_edgemoment = [seed3_400.RootMEdg1; seed3_400.RootMEdg2; seed3_400.RootMEdg3];
seed4_edgemoment = [seed4_400.RootMEdg1; seed4_400.RootMEdg2; seed4_400.RootMEdg3];
seed5_edgemoment = [seed5_400.RootMEdg1; seed5_400.RootMEdg2; seed5_400.RootMEdg3];
seed6_edgemoment = [seed6_400.RootMEdg1; seed6_400.RootMEdg2; seed6_400.RootMEdg3];

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
seed1_450.RootMFlp1(1:t_remove/0.008)=0;
seed1_450.RootMFlp2(1:t_remove/0.008)=0;
seed1_450.RootMFlp3(1:t_remove/0.008)=0;
seed2_450.RootMFlp1(1:t_remove/0.008)=0;
seed2_450.RootMFlp2(1:t_remove/0.008)=0;
seed2_450.RootMFlp3(1:t_remove/0.008)=0;
seed3_450.RootMFlp1(1:t_remove/0.008)=0;
seed3_450.RootMFlp2(1:t_remove/0.008)=0;
seed3_450.RootMFlp3(1:t_remove/0.008)=0;
seed4_450.RootMFlp1(1:t_remove/0.008)=0;
seed4_450.RootMFlp2(1:t_remove/0.008)=0;
seed4_450.RootMFlp3(1:t_remove/0.008)=0;
seed5_450.RootMFlp1(1:t_remove/0.008)=0;
seed5_450.RootMFlp2(1:t_remove/0.008)=0;
seed5_450.RootMFlp3(1:t_remove/0.008)=0;
seed6_450.RootMFlp1(1:t_remove/0.008)=0;
seed6_450.RootMFlp2(1:t_remove/0.008)=0;
seed6_450.RootMFlp3(1:t_remove/0.008)=0;

seed1_450.RootMEdg1(1:t_remove/0.008)=0;
seed1_450.RootMEdg2(1:t_remove/0.008)=0;
seed1_450.RootMEdg3(1:t_remove/0.008)=0;
seed2_450.RootMEdg1(1:t_remove/0.008)=0;
seed2_450.RootMEdg2(1:t_remove/0.008)=0;
seed2_450.RootMEdg3(1:t_remove/0.008)=0;
seed3_450.RootMEdg1(1:t_remove/0.008)=0;
seed3_450.RootMEdg2(1:t_remove/0.008)=0;
seed3_450.RootMEdg3(1:t_remove/0.008)=0;
seed4_450.RootMEdg1(1:t_remove/0.008)=0;
seed4_450.RootMEdg2(1:t_remove/0.008)=0;
seed4_450.RootMEdg3(1:t_remove/0.008)=0;
seed5_450.RootMEdg1(1:t_remove/0.008)=0;
seed5_450.RootMEdg2(1:t_remove/0.008)=0;
seed5_450.RootMEdg3(1:t_remove/0.008)=0;
seed6_450.RootMEdg1(1:t_remove/0.008)=0;
seed6_450.RootMEdg2(1:t_remove/0.008)=0;
seed6_450.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_450.RootMFlp1; seed1_450.RootMFlp2; seed1_450.RootMFlp3];
seed2_flpmoment = [seed2_450.RootMFlp1; seed2_450.RootMFlp2; seed2_450.RootMFlp3];
seed3_flpmoment = [seed3_450.RootMFlp1; seed3_450.RootMFlp2; seed3_450.RootMFlp3];
seed4_flpmoment = [seed4_450.RootMFlp1; seed4_450.RootMFlp2; seed4_450.RootMFlp3];
seed5_flpmoment = [seed5_450.RootMFlp1; seed5_450.RootMFlp2; seed5_450.RootMFlp3];
seed6_flpmoment = [seed6_450.RootMFlp1; seed6_450.RootMFlp2; seed6_450.RootMFlp3];

seed1_edgemoment = [seed1_450.RootMEdg1; seed1_450.RootMEdg2; seed1_450.RootMEdg3];
seed2_edgemoment = [seed2_450.RootMEdg1; seed2_450.RootMEdg2; seed2_450.RootMEdg3];
seed3_edgemoment = [seed3_450.RootMEdg1; seed3_450.RootMEdg2; seed3_450.RootMEdg3];
seed4_edgemoment = [seed4_450.RootMEdg1; seed4_450.RootMEdg2; seed4_450.RootMEdg3];
seed5_edgemoment = [seed5_450.RootMEdg1; seed5_450.RootMEdg2; seed5_450.RootMEdg3];
seed6_edgemoment = [seed6_450.RootMEdg1; seed6_450.RootMEdg2; seed6_450.RootMEdg3];

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
seed1_500.RootMFlp1(1:t_remove/0.008)=0;
seed1_500.RootMFlp2(1:t_remove/0.008)=0;
seed1_500.RootMFlp3(1:t_remove/0.008)=0;
seed2_500.RootMFlp1(1:t_remove/0.008)=0;
seed2_500.RootMFlp2(1:t_remove/0.008)=0;
seed2_500.RootMFlp3(1:t_remove/0.008)=0;
seed3_500.RootMFlp1(1:t_remove/0.008)=0;
seed3_500.RootMFlp2(1:t_remove/0.008)=0;
seed3_500.RootMFlp3(1:t_remove/0.008)=0;
seed4_500.RootMFlp1(1:t_remove/0.008)=0;
seed4_500.RootMFlp2(1:t_remove/0.008)=0;
seed4_500.RootMFlp3(1:t_remove/0.008)=0;
seed5_500.RootMFlp1(1:t_remove/0.008)=0;
seed5_500.RootMFlp2(1:t_remove/0.008)=0;
seed5_500.RootMFlp3(1:t_remove/0.008)=0;
seed6_500.RootMFlp1(1:t_remove/0.008)=0;
seed6_500.RootMFlp2(1:t_remove/0.008)=0;
seed6_500.RootMFlp3(1:t_remove/0.008)=0;

seed1_500.RootMEdg1(1:t_remove/0.008)=0;
seed1_500.RootMEdg2(1:t_remove/0.008)=0;
seed1_500.RootMEdg3(1:t_remove/0.008)=0;
seed2_500.RootMEdg1(1:t_remove/0.008)=0;
seed2_500.RootMEdg2(1:t_remove/0.008)=0;
seed2_500.RootMEdg3(1:t_remove/0.008)=0;
seed3_500.RootMEdg1(1:t_remove/0.008)=0;
seed3_500.RootMEdg2(1:t_remove/0.008)=0;
seed3_500.RootMEdg3(1:t_remove/0.008)=0;
seed4_500.RootMEdg1(1:t_remove/0.008)=0;
seed4_500.RootMEdg2(1:t_remove/0.008)=0;
seed4_500.RootMEdg3(1:t_remove/0.008)=0;
seed5_500.RootMEdg1(1:t_remove/0.008)=0;
seed5_500.RootMEdg2(1:t_remove/0.008)=0;
seed5_500.RootMEdg3(1:t_remove/0.008)=0;
seed6_500.RootMEdg1(1:t_remove/0.008)=0;
seed6_500.RootMEdg2(1:t_remove/0.008)=0;
seed6_500.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_500.RootMFlp1; seed1_500.RootMFlp2; seed1_500.RootMFlp3];
seed2_flpmoment = [seed2_500.RootMFlp1; seed2_500.RootMFlp2; seed2_500.RootMFlp3];
seed3_flpmoment = [seed3_500.RootMFlp1; seed3_500.RootMFlp2; seed3_500.RootMFlp3];
seed4_flpmoment = [seed4_500.RootMFlp1; seed4_500.RootMFlp2; seed4_500.RootMFlp3];
seed5_flpmoment = [seed5_500.RootMFlp1; seed5_500.RootMFlp2; seed5_500.RootMFlp3];
seed6_flpmoment = [seed6_500.RootMFlp1; seed6_500.RootMFlp2; seed6_500.RootMFlp3];

seed1_edgemoment = [seed1_500.RootMEdg1; seed1_500.RootMEdg2; seed1_500.RootMEdg3];
seed2_edgemoment = [seed2_500.RootMEdg1; seed2_500.RootMEdg2; seed2_500.RootMEdg3];
seed3_edgemoment = [seed3_500.RootMEdg1; seed3_500.RootMEdg2; seed3_500.RootMEdg3];
seed4_edgemoment = [seed4_500.RootMEdg1; seed4_500.RootMEdg2; seed4_500.RootMEdg3];
seed5_edgemoment = [seed5_500.RootMEdg1; seed5_500.RootMEdg2; seed5_500.RootMEdg3];
seed6_edgemoment = [seed6_500.RootMEdg1; seed6_500.RootMEdg2; seed6_500.RootMEdg3];

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
seed1_550.RootMFlp1(1:t_remove/0.008)=0;
seed1_550.RootMFlp2(1:t_remove/0.008)=0;
seed1_550.RootMFlp3(1:t_remove/0.008)=0;
seed2_550.RootMFlp1(1:t_remove/0.008)=0;
seed2_550.RootMFlp2(1:t_remove/0.008)=0;
seed2_550.RootMFlp3(1:t_remove/0.008)=0;
seed3_550.RootMFlp1(1:t_remove/0.008)=0;
seed3_550.RootMFlp2(1:t_remove/0.008)=0;
seed3_550.RootMFlp3(1:t_remove/0.008)=0;
seed4_550.RootMFlp1(1:t_remove/0.008)=0;
seed4_550.RootMFlp2(1:t_remove/0.008)=0;
seed4_550.RootMFlp3(1:t_remove/0.008)=0;
seed5_550.RootMFlp1(1:t_remove/0.008)=0;
seed5_550.RootMFlp2(1:t_remove/0.008)=0;
seed5_550.RootMFlp3(1:t_remove/0.008)=0;
seed6_550.RootMFlp1(1:t_remove/0.008)=0;
seed6_550.RootMFlp2(1:t_remove/0.008)=0;
seed6_550.RootMFlp3(1:t_remove/0.008)=0;

seed1_550.RootMEdg1(1:t_remove/0.008)=0;
seed1_550.RootMEdg2(1:t_remove/0.008)=0;
seed1_550.RootMEdg3(1:t_remove/0.008)=0;
seed2_550.RootMEdg1(1:t_remove/0.008)=0;
seed2_550.RootMEdg2(1:t_remove/0.008)=0;
seed2_550.RootMEdg3(1:t_remove/0.008)=0;
seed3_550.RootMEdg1(1:t_remove/0.008)=0;
seed3_550.RootMEdg2(1:t_remove/0.008)=0;
seed3_550.RootMEdg3(1:t_remove/0.008)=0;
seed4_550.RootMEdg1(1:t_remove/0.008)=0;
seed4_550.RootMEdg2(1:t_remove/0.008)=0;
seed4_550.RootMEdg3(1:t_remove/0.008)=0;
seed5_550.RootMEdg1(1:t_remove/0.008)=0;
seed5_550.RootMEdg2(1:t_remove/0.008)=0;
seed5_550.RootMEdg3(1:t_remove/0.008)=0;
seed6_550.RootMEdg1(1:t_remove/0.008)=0;
seed6_550.RootMEdg2(1:t_remove/0.008)=0;
seed6_550.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_550.RootMFlp1; seed1_550.RootMFlp2; seed1_550.RootMFlp3];
seed2_flpmoment = [seed2_550.RootMFlp1; seed2_550.RootMFlp2; seed2_550.RootMFlp3];
seed3_flpmoment = [seed3_550.RootMFlp1; seed3_550.RootMFlp2; seed3_550.RootMFlp3];
seed4_flpmoment = [seed4_550.RootMFlp1; seed4_550.RootMFlp2; seed4_550.RootMFlp3];
seed5_flpmoment = [seed5_550.RootMFlp1; seed5_550.RootMFlp2; seed5_550.RootMFlp3];
seed6_flpmoment = [seed6_550.RootMFlp1; seed6_550.RootMFlp2; seed6_550.RootMFlp3];

seed1_edgemoment = [seed1_550.RootMEdg1; seed1_550.RootMEdg2; seed1_550.RootMEdg3];
seed2_edgemoment = [seed2_550.RootMEdg1; seed2_550.RootMEdg2; seed2_550.RootMEdg3];
seed3_edgemoment = [seed3_550.RootMEdg1; seed3_550.RootMEdg2; seed3_550.RootMEdg3];
seed4_edgemoment = [seed4_550.RootMEdg1; seed4_550.RootMEdg2; seed4_550.RootMEdg3];
seed5_edgemoment = [seed5_550.RootMEdg1; seed5_550.RootMEdg2; seed5_550.RootMEdg3];
seed6_edgemoment = [seed6_550.RootMEdg1; seed6_550.RootMEdg2; seed6_550.RootMEdg3];

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
seed1_600.RootMFlp1(1:t_remove/0.008)=0;
seed1_600.RootMFlp2(1:t_remove/0.008)=0;
seed1_600.RootMFlp3(1:t_remove/0.008)=0;
seed2_600.RootMFlp1(1:t_remove/0.008)=0;
seed2_600.RootMFlp2(1:t_remove/0.008)=0;
seed2_600.RootMFlp3(1:t_remove/0.008)=0;
seed3_600.RootMFlp1(1:t_remove/0.008)=0;
seed3_600.RootMFlp2(1:t_remove/0.008)=0;
seed3_600.RootMFlp3(1:t_remove/0.008)=0;
seed4_600.RootMFlp1(1:t_remove/0.008)=0;
seed4_600.RootMFlp2(1:t_remove/0.008)=0;
seed4_600.RootMFlp3(1:t_remove/0.008)=0;
seed5_600.RootMFlp1(1:t_remove/0.008)=0;
seed5_600.RootMFlp2(1:t_remove/0.008)=0;
seed5_600.RootMFlp3(1:t_remove/0.008)=0;
seed6_600.RootMFlp1(1:t_remove/0.008)=0;
seed6_600.RootMFlp2(1:t_remove/0.008)=0;
seed6_600.RootMFlp3(1:t_remove/0.008)=0;

seed1_600.RootMEdg1(1:t_remove/0.008)=0;
seed1_600.RootMEdg2(1:t_remove/0.008)=0;
seed1_600.RootMEdg3(1:t_remove/0.008)=0;
seed2_600.RootMEdg1(1:t_remove/0.008)=0;
seed2_600.RootMEdg2(1:t_remove/0.008)=0;
seed2_600.RootMEdg3(1:t_remove/0.008)=0;
seed3_600.RootMEdg1(1:t_remove/0.008)=0;
seed3_600.RootMEdg2(1:t_remove/0.008)=0;
seed3_600.RootMEdg3(1:t_remove/0.008)=0;
seed4_600.RootMEdg1(1:t_remove/0.008)=0;
seed4_600.RootMEdg2(1:t_remove/0.008)=0;
seed4_600.RootMEdg3(1:t_remove/0.008)=0;
seed5_600.RootMEdg1(1:t_remove/0.008)=0;
seed5_600.RootMEdg2(1:t_remove/0.008)=0;
seed5_600.RootMEdg3(1:t_remove/0.008)=0;
seed6_600.RootMEdg1(1:t_remove/0.008)=0;
seed6_600.RootMEdg2(1:t_remove/0.008)=0;
seed6_600.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_600.RootMFlp1; seed1_600.RootMFlp2; seed1_600.RootMFlp3];
seed2_flpmoment = [seed2_600.RootMFlp1; seed2_600.RootMFlp2; seed2_600.RootMFlp3];
seed3_flpmoment = [seed3_600.RootMFlp1; seed3_600.RootMFlp2; seed3_600.RootMFlp3];
seed4_flpmoment = [seed4_600.RootMFlp1; seed4_600.RootMFlp2; seed4_600.RootMFlp3];
seed5_flpmoment = [seed5_600.RootMFlp1; seed5_600.RootMFlp2; seed5_600.RootMFlp3];
seed6_flpmoment = [seed6_600.RootMFlp1; seed6_600.RootMFlp2; seed6_600.RootMFlp3];

seed1_edgemoment = [seed1_600.RootMEdg1; seed1_600.RootMEdg2; seed1_600.RootMEdg3];
seed2_edgemoment = [seed2_600.RootMEdg1; seed2_600.RootMEdg2; seed2_600.RootMEdg3];
seed3_edgemoment = [seed3_600.RootMEdg1; seed3_600.RootMEdg2; seed3_600.RootMEdg3];
seed4_edgemoment = [seed4_600.RootMEdg1; seed4_600.RootMEdg2; seed4_600.RootMEdg3];
seed5_edgemoment = [seed5_600.RootMEdg1; seed5_600.RootMEdg2; seed5_600.RootMEdg3];
seed6_edgemoment = [seed6_600.RootMEdg1; seed6_600.RootMEdg2; seed6_600.RootMEdg3];

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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 660 s %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
seed1_660.RootMFlp1(1:t_remove/0.008)=0;
seed1_660.RootMFlp2(1:t_remove/0.008)=0;
seed1_660.RootMFlp3(1:t_remove/0.008)=0;
seed2_660.RootMFlp1(1:t_remove/0.008)=0;
seed2_660.RootMFlp2(1:t_remove/0.008)=0;
seed2_660.RootMFlp3(1:t_remove/0.008)=0;
seed3_660.RootMFlp1(1:t_remove/0.008)=0;
seed3_660.RootMFlp2(1:t_remove/0.008)=0;
seed3_660.RootMFlp3(1:t_remove/0.008)=0;
seed4_660.RootMFlp1(1:t_remove/0.008)=0;
seed4_660.RootMFlp2(1:t_remove/0.008)=0;
seed4_660.RootMFlp3(1:t_remove/0.008)=0;
seed5_660.RootMFlp1(1:t_remove/0.008)=0;
seed5_660.RootMFlp2(1:t_remove/0.008)=0;
seed5_660.RootMFlp3(1:t_remove/0.008)=0;
seed6_660.RootMFlp1(1:t_remove/0.008)=0;
seed6_660.RootMFlp2(1:t_remove/0.008)=0;
seed6_660.RootMFlp3(1:t_remove/0.008)=0;

seed1_660.RootMEdg1(1:t_remove/0.008)=0;
seed1_660.RootMEdg2(1:t_remove/0.008)=0;
seed1_660.RootMEdg3(1:t_remove/0.008)=0;
seed2_660.RootMEdg1(1:t_remove/0.008)=0;
seed2_660.RootMEdg2(1:t_remove/0.008)=0;
seed2_660.RootMEdg3(1:t_remove/0.008)=0;
seed3_660.RootMEdg1(1:t_remove/0.008)=0;
seed3_660.RootMEdg2(1:t_remove/0.008)=0;
seed3_660.RootMEdg3(1:t_remove/0.008)=0;
seed4_660.RootMEdg1(1:t_remove/0.008)=0;
seed4_660.RootMEdg2(1:t_remove/0.008)=0;
seed4_660.RootMEdg3(1:t_remove/0.008)=0;
seed5_660.RootMEdg1(1:t_remove/0.008)=0;
seed5_660.RootMEdg2(1:t_remove/0.008)=0;
seed5_660.RootMEdg3(1:t_remove/0.008)=0;
seed6_660.RootMEdg1(1:t_remove/0.008)=0;
seed6_660.RootMEdg2(1:t_remove/0.008)=0;
seed6_660.RootMEdg3(1:t_remove/0.008)=0;

seed1_flpmoment = [seed1_660.RootMFlp1; seed1_660.RootMFlp2; seed1_660.RootMFlp3];
seed2_flpmoment = [seed2_660.RootMFlp1; seed2_660.RootMFlp2; seed2_660.RootMFlp3];
seed3_flpmoment = [seed3_660.RootMFlp1; seed3_660.RootMFlp2; seed3_660.RootMFlp3];
seed4_flpmoment = [seed4_660.RootMFlp1; seed4_660.RootMFlp2; seed4_660.RootMFlp3];
seed5_flpmoment = [seed5_660.RootMFlp1; seed5_660.RootMFlp2; seed5_660.RootMFlp3];
seed6_flpmoment = [seed6_660.RootMFlp1; seed6_660.RootMFlp2; seed6_660.RootMFlp3];

seed1_edgemoment = [seed1_660.RootMEdg1; seed1_660.RootMEdg2; seed1_660.RootMEdg3];
seed2_edgemoment = [seed2_660.RootMEdg1; seed2_660.RootMEdg2; seed2_660.RootMEdg3];
seed3_edgemoment = [seed3_660.RootMEdg1; seed3_660.RootMEdg2; seed3_660.RootMEdg3];
seed4_edgemoment = [seed4_660.RootMEdg1; seed4_660.RootMEdg2; seed4_660.RootMEdg3];
seed5_edgemoment = [seed5_660.RootMEdg1; seed5_660.RootMEdg2; seed5_660.RootMEdg3];
seed6_edgemoment = [seed6_660.RootMEdg1; seed6_660.RootMEdg2; seed6_660.RootMEdg3];

seed1_rootmoment = sqrt(seed1_flpmoment.^2 + seed1_edgemoment.^2);
seed2_rootmoment = sqrt(seed2_flpmoment.^2 + seed2_edgemoment.^2);
seed3_rootmoment = sqrt(seed3_flpmoment.^2 + seed3_edgemoment.^2);
seed4_rootmoment = sqrt(seed4_flpmoment.^2 + seed4_edgemoment.^2);
seed5_rootmoment = sqrt(seed5_flpmoment.^2 + seed5_edgemoment.^2);
seed6_rootmoment = sqrt(seed6_flpmoment.^2 + seed6_edgemoment.^2);


root_seeds660 = [max(seed1_rootmoment), max(seed2_rootmoment), max(seed3_rootmoment),...
    max(seed4_rootmoment), max(seed5_rootmoment), max(seed6_rootmoment)];

seed_660_rootmoment = (max(seed1_rootmoment) + max(seed2_rootmoment) + max(seed3_rootmoment)+...
    max(seed4_rootmoment)+ max(seed5_rootmoment)+ max(seed6_rootmoment))/6;



rootmoment =[seed_70_rootmoment, seed_100_rootmoment, seed_150_rootmoment, seed_200_rootmoment,...
    seed_250_rootmoment, seed_300_rootmoment, seed_350_rootmoment,...
    seed_400_rootmoment, seed_450_rootmoment, seed_500_rootmoment,...
    seed_550_rootmoment, seed_600_rootmoment, seed_660_rootmoment]; 

%% Plot tip defl

%%%%% plot individual seeds %%%% 
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

x=[660, 660, 660, 660, 660, 660];
plot(x, tip_seeds660, '+');

x=[70, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 660];
plot(x,tip_defl);
grid on;
ylabel('Tip Deflection (m)','Interpreter','latex');
xlabel('Simulation Time (s)','Interpreter','latex');

ylim([5 9]);



%% Plot root moment

%%%%% plot individual seeds %%%% 
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

x=[660, 660, 660, 660, 660, 660];
plot(x, root_seeds660, '+');


x=[70, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 660]; 
plot(x,rootmoment);
grid on;
ylabel('Root Moment(KNm)','Interpreter','latex');
xlabel('Simulation Time (s)','Interpreter','latex');

ylim([10000 18000]);
