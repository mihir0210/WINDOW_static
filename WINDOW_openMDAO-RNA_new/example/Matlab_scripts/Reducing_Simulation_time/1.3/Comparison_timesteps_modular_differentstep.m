%% load main 600 s files 

% seed1 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=1.mat'));
% seed2 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=2.mat'));
% seed3 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=3.mat'));
% seed4 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=4.mat'));
% seed5 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=5.mat'));
% seed6 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=6.mat'));
% seed7 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=7.mat'));
% seed8 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=8.mat'));
% seed9 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=9.mat'));
% seed10 = load(fullfile(cd,'New_simulations_seeds\DLC1.3_600_seed=10.mat'));


seed1 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=1.mat'));
seed2 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=2.mat'));
seed3 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=3.mat'));
seed4 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=4.mat'));
seed5 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=5.mat'));
seed6 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=6.mat'));
seed7 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=7.mat'));
seed8 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=8.mat'));
seed9 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=9.mat'));
seed10 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_600_seed=10.mat'));

nd_seed1 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed1.mat'));
nd_seed2 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed2.mat'));
nd_seed3 =load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed3.mat'));
nd_seed4 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed4.mat'));
nd_seed5 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed5.mat'));
nd_seed6 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed6.mat'));
nd_seed7 =load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed7.mat'));
nd_seed8 =load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed8.mat'));
nd_seed9 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed9.mat'));
nd_seed10 = load(fullfile(cd,'Latest_simulations_seeds\DLC1.3_60_newdesign_seed10.mat'));



t_remove = 20; 

step_size_s = 0.008;


step_size_l = 0.0125;



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

seed7_deflectionb1 = seed7.OoPDefl1; %(1:t_remove/0.008);
seed7_deflectionb2 = seed7.OoPDefl2; %(1:t_remove/0.008);
seed7_deflectionb3 = seed7.OoPDefl3; %(1:t_remove/0.008);

seed8_deflectionb1 = seed8.OoPDefl1; %(1:t_remove/0.008);
seed8_deflectionb2 = seed8.OoPDefl2; %(1:t_remove/0.008);
seed8_deflectionb3 = seed8.OoPDefl3; %(1:t_remove/0.008);

seed9_deflectionb1 = seed9.OoPDefl1; %(1:t_remove/0.008);
seed9_deflectionb2 = seed9.OoPDefl2; %(1:t_remove/0.008);
seed9_deflectionb3 = seed9.OoPDefl3; %(1:t_remove/0.008);

seed10_deflectionb1 = seed10.OoPDefl1; %(1:t_remove/0.008);
seed10_deflectionb2 = seed10.OoPDefl2; %(1:t_remove/0.008);
seed10_deflectionb3 = seed10.OoPDefl3; %(1:t_remove/0.008);
                    
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

seed7_rootflap1 = seed7.RootMFlp1; %(1:t_remove/0.008);
seed7_rootflap2 = seed7.RootMFlp2; %(1:t_remove/0.008);
seed7_rootflap3 = seed7.RootMFlp3; %(1:t_remove/0.008);
seed7_rootedge1 = seed7.RootMEdg1; %(1:t_remove/0.008);
seed7_rootedge2 = seed7.RootMEdg2; %(1:t_remove/0.008);
seed7_rootedge3 = seed7.RootMEdg3; %(1:t_remove/0.008);

seed8_rootflap1 = seed8.RootMFlp1; %(1:t_remove/0.008);
seed8_rootflap2 = seed8.RootMFlp2; %(1:t_remove/0.008);
seed8_rootflap3 = seed8.RootMFlp3; %(1:t_remove/0.008);
seed8_rootedge1 = seed8.RootMEdg1; %(1:t_remove/0.008);
seed8_rootedge2 = seed8.RootMEdg2; %(1:t_remove/0.008);
seed8_rootedge3 = seed8.RootMEdg3; %(1:t_remove/0.008);

seed9_rootflap1 = seed9.RootMFlp1; %(1:t_remove/0.008);
seed9_rootflap2 = seed9.RootMFlp2; %(1:t_remove/0.008);
seed9_rootflap3 = seed9.RootMFlp3; %(1:t_remove/0.008);
seed9_rootedge1 = seed9.RootMEdg1; %(1:t_remove/0.008);
seed9_rootedge2 = seed9.RootMEdg2; %(1:t_remove/0.008);
seed9_rootedge3 = seed9.RootMEdg3; %(1:t_remove/0.008);

seed10_rootflap1 = seed10.RootMFlp1; %(1:t_remove/0.008);
seed10_rootflap2 = seed10.RootMFlp2; %(1:t_remove/0.008);
seed10_rootflap3 = seed10.RootMFlp3; %(1:t_remove/0.008);
seed10_rootedge1 = seed10.RootMEdg1; %(1:t_remove/0.008);
seed10_rootedge2 = seed10.RootMEdg2; %(1:t_remove/0.008);
seed10_rootedge3 = seed10.RootMEdg3; %(1:t_remove/0.008);


%%% Tip Deflection for new design %%%

%---------------Tip Deflections ----------------------
nd_seed1_deflectionb1 = nd_seed1.OoPDefl1; %(1:t_remove/0.008);
nd_seed1_deflectionb2 = nd_seed1.OoPDefl2; %(1:t_remove/0.008);
nd_seed1_deflectionb3 = nd_seed1.OoPDefl3; %(1:t_remove/0.008);

nd_seed2_deflectionb1 = nd_seed2.OoPDefl1; %(1:t_remove/0.008);
nd_seed2_deflectionb2 = nd_seed2.OoPDefl2; %(1:t_remove/0.008);
nd_seed2_deflectionb3 = nd_seed2.OoPDefl3; %(1:t_remove/0.008);

nd_seed3_deflectionb1 = nd_seed3.OoPDefl1; %(1:t_remove/0.008);
nd_seed3_deflectionb2 = nd_seed3.OoPDefl2; %(1:t_remove/0.008);
nd_seed3_deflectionb3 = nd_seed3.OoPDefl3; %(1:t_remove/0.008);

nd_seed4_deflectionb1 = nd_seed4.OoPDefl1; %(1:t_remove/0.008);
nd_seed4_deflectionb2 = nd_seed4.OoPDefl2; %(1:t_remove/0.008);
nd_seed4_deflectionb3 = nd_seed4.OoPDefl3; %(1:t_remove/0.008);

nd_seed5_deflectionb1 = nd_seed5.OoPDefl1; %(1:t_remove/0.008);
nd_seed5_deflectionb2 = nd_seed5.OoPDefl2; %(1:t_remove/0.008);
nd_seed5_deflectionb3 = nd_seed5.OoPDefl3; %(1:t_remove/0.008);

nd_seed6_deflectionb1 = nd_seed6.OoPDefl1; %(1:t_remove/0.008);
nd_seed6_deflectionb2 = nd_seed6.OoPDefl2; %(1:t_remove/0.008);
nd_seed6_deflectionb3 = nd_seed6.OoPDefl3; %(1:t_remove/0.008);

nd_seed7_deflectionb1 = nd_seed7.OoPDefl1; %(1:t_remove/0.008);
nd_seed7_deflectionb2 = nd_seed7.OoPDefl2; %(1:t_remove/0.008);
nd_seed7_deflectionb3 = nd_seed7.OoPDefl3; %(1:t_remove/0.008);

nd_seed8_deflectionb1 = nd_seed8.OoPDefl1; %(1:t_remove/0.008);
nd_seed8_deflectionb2 = nd_seed8.OoPDefl2; %(1:t_remove/0.008);
nd_seed8_deflectionb3 = nd_seed8.OoPDefl3; %(1:t_remove/0.008);

nd_seed9_deflectionb1 = nd_seed9.OoPDefl1; %(1:t_remove/0.008);
nd_seed9_deflectionb2 = nd_seed9.OoPDefl2; %(1:t_remove/0.008);
nd_seed9_deflectionb3 = nd_seed9.OoPDefl3; %(1:t_remove/0.008);

nd_seed10_deflectionb1 = nd_seed10.OoPDefl1; %(1:t_remove/0.008);
nd_seed10_deflectionb2 = nd_seed10.OoPDefl2; %(1:t_remove/0.008);
nd_seed10_deflectionb3 = nd_seed10.OoPDefl3; %(1:t_remove/0.008);

%% Compare Tip deflections

%%%%% Time steps = [60, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
%%%%% 600]


deflectionb1_ = [seed1_deflectionb1, seed2_deflectionb1, seed3_deflectionb1,...
                seed4_deflectionb1, seed5_deflectionb1, seed6_deflectionb1];
            
deflectionb1_n= [seed7_deflectionb1, seed8_deflectionb1, seed9_deflectionb1,...
                seed10_deflectionb1];  
            
deflectionb2_ = [seed1_deflectionb2, seed2_deflectionb2, seed3_deflectionb2,...
                seed4_deflectionb2, seed5_deflectionb2, seed6_deflectionb2];
            
deflectionb2_n =[seed7_deflectionb2, seed8_deflectionb2, seed9_deflectionb2,...
                seed10_deflectionb2]; 

deflectionb3_ = [seed1_deflectionb3, seed2_deflectionb3, seed3_deflectionb3,...
                seed4_deflectionb3, seed5_deflectionb3, seed6_deflectionb3];
            
deflectionb3_n =[seed7_deflectionb3, seed8_deflectionb3, seed9_deflectionb3,...
                seed10_deflectionb3]; 
i=1;

for t=[60, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
    
    deflectionb1 = deflectionb1_(1:t/step_size_l,:);
    deflectionb1n = deflectionb1_n(1:t/step_size_s,:);
    deflectionb2 = deflectionb2_(1:t/step_size_l,:);
    deflectionb2n = deflectionb2_n(1:t/step_size_s,:);
    deflectionb3 = deflectionb3_(1:t/step_size_l,:);
    deflectionb3n = deflectionb3_n(1:t/step_size_s,:);
    
    deflectionb1(1:t_remove/step_size_l,:)=[];
    deflectionb1n(1:t_remove/step_size_s,:)=[];
    deflectionb2(1:t_remove/step_size_l,:)=[];
    deflectionb2n(1:t_remove/step_size_s,:)=[];
    deflectionb3(1:t_remove/step_size_l,:)=[];
    deflectionb3n(1:t_remove/step_size_s,:)=[];
    
    % a row vector with max for all seeds per blade
    deflectionb1 = max(deflectionb1,[],1); 
    deflectionb1n = max(deflectionb1n,[],1); 
    deflectionb2 = max(deflectionb2,[],1);
    deflectionb2n = max(deflectionb2n,[],1); 
    deflectionb3 = max(deflectionb3,[],1);
    deflectionb3n = max(deflectionb3n,[],1); 
    
    deflectionb1_10 = [deflectionb1, deflectionb1n];
    deflectionb2_10 = [deflectionb2, deflectionb2n];
    deflectionb3_10 = [deflectionb3, deflectionb3n];
    
    % 3 rows for 3 blades, each having max value for 10 seeds
    deflection_ = [deflectionb1_10; deflectionb2_10; deflectionb3_10];
    
    % row vector with max deflection for all 10 seeds 
    deflection(i,:) = max(deflection_,[],1);
    i = i+1;

end

nd_deflectionb1 = [nd_seed1_deflectionb1, nd_seed2_deflectionb1, nd_seed3_deflectionb1,...
    nd_seed4_deflectionb1, nd_seed5_deflectionb1, nd_seed6_deflectionb1, nd_seed7_deflectionb1,...
    nd_seed8_deflectionb1, nd_seed9_deflectionb1, nd_seed10_deflectionb1];

nd_deflectionb2 = [nd_seed1_deflectionb2, nd_seed2_deflectionb2, nd_seed3_deflectionb2,...
    nd_seed4_deflectionb2, nd_seed5_deflectionb2, nd_seed6_deflectionb2, nd_seed7_deflectionb2,...
    nd_seed8_deflectionb2, nd_seed9_deflectionb2, nd_seed10_deflectionb2];

nd_deflectionb3 = [nd_seed1_deflectionb3, nd_seed2_deflectionb3, nd_seed3_deflectionb3,...
    nd_seed4_deflectionb3, nd_seed5_deflectionb3, nd_seed6_deflectionb3, nd_seed7_deflectionb3,...
    nd_seed8_deflectionb3, nd_seed9_deflectionb3, nd_seed10_deflectionb3];

nd_deflectionb1(1:t_remove/step_size_l,:)=[];
nd_deflectionb2(1:t_remove/step_size_l,:)=[];
nd_deflectionb3(1:t_remove/step_size_l,:)=[];

nd_deflectionb1 = max(nd_deflectionb1,[],1);
nd_deflectionb2 = max(nd_deflectionb2,[],1);
nd_deflectionb3 = max(nd_deflectionb3,[],1);


nd_deflection = [nd_deflectionb1; nd_deflectionb2; nd_deflectionb3];
nd_deflection = max(nd_deflection, [],1);
%% Compare root moments 


rootflap1_ = [seed1_rootflap1, seed2_rootflap1, seed3_rootflap1, ...
              seed4_rootflap1, seed5_rootflap1, seed6_rootflap1];

rootflap1_n = [seed7_rootflap1, seed8_rootflap1, seed9_rootflap1,...
              seed10_rootflap1];

rootedge1_ = [seed1_rootedge1, seed2_rootedge1, seed3_rootedge1, ...
              seed4_rootedge1, seed5_rootedge1, seed6_rootedge1];

rootedge1_n = [seed7_rootedge1, seed8_rootedge1, seed9_rootedge1,...
              seed10_rootedge1];
          

          
rootflap2_ = [seed1_rootflap2, seed2_rootflap2, seed3_rootflap2, ...
              seed4_rootflap2, seed5_rootflap2, seed6_rootflap2];
          
rootflap2_n =[seed7_rootflap2, seed8_rootflap2, seed9_rootflap2,...
              seed10_rootflap2];

rootedge2_ = [seed1_rootedge2, seed2_rootedge2, seed3_rootedge2, ...
              seed4_rootedge2, seed5_rootedge2, seed6_rootedge2]; 
              
rootedge2_n =[seed7_rootedge2, seed8_rootedge2, seed9_rootedge2,...
              seed10_rootedge2];    
          
          
rootflap3_ = [seed1_rootflap3, seed2_rootflap3, seed3_rootflap3, ...
              seed4_rootflap3, seed5_rootflap3, seed6_rootflap3];

rootflap3_n = [seed7_rootflap3, seed8_rootflap3, seed9_rootflap3,...
              seed10_rootflap3];         
          
              
rootedge3_ = [seed1_rootedge3, seed2_rootedge3, seed3_rootedge3, ...
              seed4_rootedge3, seed5_rootedge3, seed6_rootedge3]; 

rootedge3_n = [seed7_rootedge3, seed8_rootedge3, seed9_rootedge3,...
              seed10_rootedge3];
          
 
i=1;

for t=[60, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
    
    rootflap1 = rootflap1_(1:t/step_size_l,:);
    rootflap1n = rootflap1_n(1:t/step_size_s,:);
    rootedge1 = rootedge1_(1:t/step_size_l,:);
    rootedge1n = rootedge1_n(1:t/step_size_s,:);
    rootflap2 = rootflap2_(1:t/step_size_l,:);
    rootflap2n = rootflap2_n(1:t/step_size_s,:);
    rootedge2 = rootedge2_(1:t/step_size_l,:);
    rootedge2n = rootedge2_n(1:t/step_size_s,:);
    rootflap3 = rootflap3_(1:t/step_size_l,:);
    rootflap3n = rootflap3_n(1:t/step_size_s,:);
    rootedge3 = rootedge3_(1:t/step_size_l,:);
    rootedge3n = rootedge3_n(1:t/step_size_s,:);
    
    
    
    rootflap1(1:t_remove/step_size_l,:)=[];
    rootflap1n(1:t_remove/step_size_s,:)=[];
    rootedge1(1:t_remove/step_size_l,:)=[];
    rootedge1n(1:t_remove/step_size_s,:)=[];
    rootflap2(1:t_remove/step_size_l,:)=[];
    rootflap2n(1:t_remove/step_size_s,:)=[];
    rootedge2(1:t_remove/step_size_l,:)=[];
    rootedge2n(1:t_remove/step_size_s,:)=[]; 
    rootflap3(1:t_remove/step_size_l,:)=[];
    rootflap3n(1:t_remove/step_size_s,:)=[];
    rootedge3(1:t_remove/step_size_l,:)=[];  
    rootedge3n(1:t_remove/step_size_s,:)=[];
  
    
    
    rootmoment1_ = sqrt(rootflap1.^2 + rootedge1.^2);
    rootmoment1_n= sqrt(rootflap1n.^2 + rootedge1n.^2);
    rootmoment2_ = sqrt(rootflap2.^2 + rootedge2.^2);
    rootmoment2_n = sqrt(rootflap2n.^2 + rootedge2n.^2);
    rootmoment3_ = sqrt(rootflap3.^2 + rootedge3.^2);
    rootmoment3_n = sqrt(rootflap3n.^2 + rootedge3n.^2);
    
    rootmoment1 = max(rootmoment1_,[],1);
    rootmoment1n = max(rootmoment1_n,[],1);
    rootmoment2 = max(rootmoment2_,[],1);
    rootmoment2n = max(rootmoment2_n,[],1);
    rootmoment3 = max(rootmoment3_,[],1);
    rootmoment3n = max(rootmoment3_n,[],1);
    
    rootmoment1_10 = [rootmoment1, rootmoment1n];
    rootmoment2_10 = [rootmoment2, rootmoment2n];
    rootmoment3_10 = [rootmoment3, rootmoment3n];
    
    rootmoment_ =[rootmoment1_10 ; rootmoment2_10; rootmoment3_10];
    rootmoment(i,:) = max(rootmoment_,[],1);
    
    i=i+1;
        
end

mean_tipdeflection = mean(deflection,2);
mean_rootmoment = mean(rootmoment,2);



%% Plot tip defl
 
% %%%%% plot individual seeds and mean %%%% 

n_seeds = 10;
t=[60, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600];


x_60 = t(1)*ones(1, n_seeds);
x_100 = t(2)*ones(1, n_seeds);
x_150 = t(3)*ones(1, n_seeds);
x_200 = t(4)*ones(1, n_seeds);
x_250 = t(5)*ones(1, n_seeds);
x_300 = t(6)*ones(1, n_seeds);
x_350 = t(7)*ones(1, n_seeds);
x_400 = t(8)*ones(1, n_seeds);
x_450 = t(9)*ones(1, n_seeds);
x_500 = t(10)*ones(1, n_seeds);
x_550 = t(11)*ones(1, n_seeds);
x_600 = t(12)*ones(1, n_seeds);

x=[60, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600];

figure(1)
plot(x,mean_tipdeflection, 'k'); hold on;


%plot(x, deflection(:,10), 'r');
plot(x_60, deflection(1,:), 'bo','MarkerSize',5);
plot(x_100, deflection(2,:), 'bo','MarkerSize',5);
plot(x_150, deflection(3,:), 'bo','MarkerSize',5);
plot(x_200, deflection(4,:), 'bo','MarkerSize',5);
plot(x_250, deflection(5,:), 'bo','MarkerSize',5);
plot(x_300, deflection(6,:), 'bo','MarkerSize',5);
plot(x_350, deflection(7,:), 'bo','MarkerSize',5);
plot(x_400, deflection(8,:), 'bo','MarkerSize',5);
plot(x_450, deflection(9,:), 'bo','MarkerSize',5);
plot(x_500, deflection(10,:), 'bo','MarkerSize',5);
plot(x_550, deflection(11,:), 'bo','MarkerSize',5);
plot(x_600, deflection(12,:), 'bo','MarkerSize',5);

plot(x(1), max(deflection(1,:)), 'r*','MarkerSize',10);

plot(x(end), max(deflection(end,:)), 'r*','MarkerSize',10);


%plot(x_60, nd_deflection, '*');

%ax.Layer = 'top';
grid on
a = gca;
% set box property to off and remove background color
set(a,'box','off','color','none')
% create new, empty axes with box but without ticks
b = axes('Position',get(a,'Position'),'box','on','xtick',[],'ytick',[]);
% set original axes as active
axes(a)
% link axes in case of zooming
linkaxes([a b])
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
set(gca,'GridLineStyle','--')
set(gca,'GridAlpha',0.8)
set(gca,'TickDir','out');
axesH = gca;
axesH.XAxis.TickLabelInterpreter = 'latex';
axesH.XAxis.TickLabelFormat      = '\\textbf{%g}';
axesH.YAxis.TickLabelInterpreter = 'latex';
axesH.YAxis.TickLabelFormat      = '\\textbf{%g}';

%ax.GridAlpha = 1;
ylabel('\textbf{Tip Deflection (m)}','Interpreter','latex');
xlabel('\textbf{Simulation Time (s)}','Interpreter','latex');
legend('\textbf{Mean tip deflection}','Interpreter','latex');
xlim([0 650]);
ylim([4 9]);


%% Plot root moment
 
%%%%% plot individual seeds and mean %%%% 
figure(2)
plot(x,mean_rootmoment); hold on;

plot(x_60, rootmoment(1,:), 'o');
plot(x_100, rootmoment(2,:), 'o');
plot(x_150, rootmoment(3,:), 'o');
plot(x_200, rootmoment(4,:), 'o');
plot(x_250, rootmoment(5,:), 'o');
plot(x_300, rootmoment(6,:), 'o');
plot(x_350, rootmoment(7,:), 'o');
plot(x_400, rootmoment(8,:), 'o');
plot(x_450, rootmoment(9,:), 'o');
plot(x_500, rootmoment(10,:), 'o');
plot(x_550, rootmoment(11,:), 'o');
plot(x_600, rootmoment(12,:), 'o');

%ax.Layer = 'top';
grid on
set(gca,'GridLineStyle','--')
%ax.GridAlpha = 1;

ylabel('Root Moment(KNm)','Interpreter','latex');
xlabel('Simulation Time (s)','Interpreter','latex');

xlim([0 650]);
ylim([10000 18000]);
