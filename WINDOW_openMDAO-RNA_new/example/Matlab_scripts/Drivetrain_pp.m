function Drivetrain=Drivetrain_pp
load([pwd,'\Drivetrain.mat']);
%% Drivetrain pre-processing
Drivetrain.Generator.Efficiency=Drivetrain_Generator_Efficiency;
Drivetrain.Generator.HSSInertia=Drivetrain_Generator_HSSInertia;
Drivetrain.Gearbox.Ratio=Drivetrain_Gearbox_Ratio;
Drivetrain.Gearbox.Efficiency=Drivetrain_Gearbox_eff;
Drivetrain.LSSInertia=Drivetrain_LSSInertia;
save([pwd,'\Drivetrain.mat'],'Drivetrain');