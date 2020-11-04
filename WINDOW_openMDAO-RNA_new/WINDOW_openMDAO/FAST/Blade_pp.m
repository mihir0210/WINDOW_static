function Blade=Blade_pp
load([pwd,'\Blade.mat']);
%% Blade pre-processing
Blade.Mass=Blade_Mass;
Blade.EIflap=Blade_EIflap;
Blade.EIedge=Blade_EIedge;
Blade.Radius=Blade_Radius;
Blade.Chord=Blade_Chord;
Blade.Twist=Blade_Twist;
Blade.PitchAxis=Blade_PitchAxis;
Blade.NFoil=Blade_NFoil+1; %python and Matlab indexing
Blade.IFoil=Blade_IFoil+1; %python and Matlab indexing
Blade.Cone=Blade_Cone;
Blade.Number=Blade_Number;
Blade.Thickness=Blade_Thickness;
Blade.cg=Blade_cg;
Blade.sc=Blade_sc;
Blade.ac=Blade_ac;
Blade.eo=Blade_eo;
Blade.FlapIner=Blade_FlapIner;
Blade.EdgeIner=Blade_EdgeIner;
Blade.GJ=Blade_GJ;
Blade.EA=Blade_EA;
save([pwd,'\Blade.mat'],'Blade');